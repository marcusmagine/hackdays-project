import os
import json
from typing import Dict, List, Optional, Tuple, cast
import requests
from pathlib import Path
from dotenv import load_dotenv

class MuxProcessor:
    def __init__(self, mux_token_id: Optional[str] = None, mux_token_secret: Optional[str] = None):
        load_dotenv(override=True)
        self.base_url = "https://api.mux.com/video/v1"

        # Get credentials from environment or parameters
        token_id = mux_token_id or os.getenv("MUX_TOKEN_ID")
        token_secret = mux_token_secret or os.getenv("MUX_TOKEN_SECRET")

        if not token_id or not token_secret:
            raise ValueError("Mux credentials not found")

        # Now we know both are not None
        self.auth: Tuple[str, str] = (cast(str, token_id), cast(str, token_secret))

    def create_asset(self, video_path: str, title: Optional[str] = None) -> Dict:
        print(f"Creating asset for {video_path}...")

        # First, check if the file exists and is readable
        video_file_path = Path(video_path)
        if not video_file_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        file_size = video_file_path.stat().st_size
        print(f"File size: {file_size / (1024 * 1024):.2f} MB")

        # Create a direct upload
        upload_response = requests.post(
            f"{self.base_url}/uploads",
            auth=self.auth,
            json={"new_asset_settings": {"playback_policy": ["public"]}}
        )
        upload_response.raise_for_status()
        upload_data = upload_response.json()["data"]

        # Debug: Print upload response data
        print(f"Upload response data keys: {list(upload_data.keys())}")

        # Upload the file using requests
        print(f"Uploading video file to {upload_data['url']}...")
        with open(video_path, "rb") as video_file:
            # Use a proper content-type for the file
            headers = {"Content-Type": "video/mp4"}

            # Use the file object directly
            response = requests.put(
                upload_data["url"],
                data=video_file,
                headers=headers
            )

            # Check for errors
            if response.status_code >= 400:
                print(f"Upload failed with status code {response.status_code}")
                print(f"Response: {response.text}")
                raise Exception(f"Failed to upload file: {response.status_code} {response.reason}")

            print(f"Upload response status code: {response.status_code}")

        print("Waiting for upload to be processed...")
        # Get the upload ID
        upload_id = upload_data["id"]

        # Wait for the upload to be processed and get the asset ID
        asset_id = self.wait_for_upload(upload_id)

        # Now wait for the asset to be ready
        print(f"Upload processed. Waiting for asset {asset_id} to be ready...")
        asset_data = self.wait_for_asset(asset_id)

        playback_id = None
        if asset_data.get("playback_ids"):
            playback_id = asset_data["playback_ids"][0]["id"]

        return {
            "asset_id": asset_id,
            "playback_id": playback_id,
            "status": asset_data.get("status"),
            "duration": asset_data.get("duration")
        }

    def wait_for_upload(self, upload_id: str, timeout: int = 300, interval: int = 5) -> str:
        """Wait for an upload to be processed and return the asset ID."""
        import time
        start_time = time.time()

        print(f"Waiting for upload {upload_id} to be processed...")

        while True:
            # Get the upload status
            response = requests.get(
                f"{self.base_url}/uploads/{upload_id}",
                auth=self.auth
            )
            response.raise_for_status()
            upload_data = response.json()["data"]

            # Debug: Print full upload data for troubleshooting
            print(f"Upload data: {upload_data}")

            # Check if the upload has an asset ID
            if upload_data.get("asset_id"):
                print(f"Upload processed successfully. Asset ID: {upload_data['asset_id']}")
                return upload_data["asset_id"]

            # Check if the upload has failed
            if upload_data.get("status") == "error":
                error_message = upload_data.get("error_message", "Unknown error")
                print(f"Upload failed: {error_message}")
                raise Exception(f"Upload failed: {error_message}")

            # Check if we've timed out
            elapsed = time.time() - start_time
            if elapsed > timeout:
                print(f"Timeout waiting for upload to process after {elapsed:.1f} seconds")
                raise TimeoutError(f"Upload {upload_id} not processed within {timeout}s")

            # Wait and try again
            status = upload_data.get("status", "unknown")
            print(f"Upload status: {status}. Waiting {interval} seconds... (elapsed: {elapsed:.1f}s)")
            time.sleep(interval)

    def wait_for_asset(self, asset_id: str, timeout: int = 300, interval: int = 5) -> Dict:
        """Wait for an asset to be ready and return the asset data."""
        import time
        start_time = time.time()

        print(f"Waiting for asset {asset_id} to be ready...")

        while True:
            try:
                asset_data = self.get_asset_status(asset_id)

                # Debug: Print full asset data for troubleshooting
                print(f"Asset data: {asset_data}")

                status = asset_data.get("status")

                if status == "ready":
                    print(f"Asset {asset_id} is ready!")
                    return asset_data
                elif status == "errored":
                    errors = asset_data.get("errors", [])
                    print(f"Asset processing failed: {errors}")
                    raise Exception(f"Asset processing failed: {errors}")

                # Check if we've timed out
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    print(f"Timeout waiting for asset to be ready after {elapsed:.1f} seconds")
                    raise TimeoutError(f"Asset {asset_id} not ready within {timeout}s")

                # Wait and try again
                print(f"Asset status: {status}. Waiting {interval} seconds... (elapsed: {elapsed:.1f}s)")
                time.sleep(interval)

            except requests.exceptions.HTTPError as e:
                print(f"HTTP error while checking asset status: {e}")

                # If we get a 404, the asset might not be created yet
                if e.response.status_code == 404:
                    print(f"Asset {asset_id} not found yet. Waiting {interval} seconds...")
                    time.sleep(interval)
                    continue

                # For other errors, raise the exception
                raise

    def get_asset_status(self, asset_id: str) -> Dict:
        response = requests.get(
            f"{self.base_url}/assets/{asset_id}",
            auth=self.auth
        )
        response.raise_for_status()
        return response.json()["data"]

    def process_season(self, segments_dir: str, output_file: str) -> Dict:
        """Process all video segments in a directory and create a season metadata file."""
        segment_files = sorted(Path(segments_dir).glob("*.mp4"))

        if not segment_files:
            raise ValueError(f"No MP4 files found in {segments_dir}")

        print(f"Found {len(segment_files)} MP4 files in {segments_dir}")

        timestamps_file = os.path.join(segments_dir, "timestamps.json")
        timestamps = {}
        if os.path.exists(timestamps_file):
            print(f"Loading timestamps from {timestamps_file}")
            with open(timestamps_file, "r") as f:
                timestamps = json.load(f)
        else:
            print("No timestamps.json file found")

        episodes = []
        errors = []

        for i, video_path in enumerate(segment_files, 1):
            print(f"\n{'='*50}")
            print(f"Processing episode {i}/{len(segment_files)}: {video_path.name}")
            print(f"{'='*50}")

            try:
                asset_data = self.create_asset(
                    str(video_path),
                    title=f"Episode {i}"
                )

                timestamp_data = {}
                if timestamps and "segments" in timestamps:
                    for segment in timestamps["segments"]:
                        if segment["segment"] == i - 1:
                            timestamp_data = segment
                            break

                episode = {
                    "episode_number": i,
                    "title": f"Episode {i}",
                    "asset_id": asset_data["asset_id"],
                    "playback_id": asset_data["playback_id"],
                    "status": asset_data["status"],
                    "duration": asset_data["duration"],
                    "filename": video_path.name,
                    "timestamps": timestamp_data
                }

                episodes.append(episode)

                print(f"Episode {i} processed successfully:")
                print(f"  Asset ID: {asset_data['asset_id']}")
                print(f"  Playback ID: {asset_data['playback_id']}")
                print(f"  Status: {asset_data['status']}")
                print(f"  Duration: {asset_data['duration']:.2f}s")

            except Exception as e:
                print(f"Error processing episode {i}: {str(e)}")
                errors.append({
                    "episode_number": i,
                    "filename": video_path.name,
                    "error": str(e)
                })
                continue

        season_data = {
            "total_episodes": len(episodes),
            "episodes": episodes,
            "timestamps_source": timestamps_file if os.path.exists(timestamps_file) else None,
            "errors": errors
        }

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save season data to file
        with open(output_file, "w") as f:
            json.dump(season_data, f, indent=2)

        print(f"\n{'='*50}")
        print(f"Processing complete!")
        print(f"Total episodes processed: {len(episodes)}")
        print(f"Total errors: {len(errors)}")
        print(f"Metadata saved to: {output_file}")

        if errors:
            print("\nErrors encountered:")
            for error in errors:
                print(f"  Episode {error['episode_number']} ({error['filename']}): {error['error']}")

        return season_data

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Process video segments using Mux.")
    parser.add_argument("segments_dir", help="Directory containing video segments")
    parser.add_argument("output_file", help="Path to save season metadata")
    parser.add_argument("--mux-token-id", help="Mux API Token ID (optional if set in .env)")
    parser.add_argument("--mux-token-secret", help="Mux API Token Secret (optional if set in .env)")

    args = parser.parse_args()

    processor = MuxProcessor(args.mux_token_id, args.mux_token_secret)
    season_data = processor.process_season(args.segments_dir, args.output_file)

if __name__ == "__main__":
    main()