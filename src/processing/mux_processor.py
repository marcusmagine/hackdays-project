import os
import json
from typing import Dict, List
import requests
from pathlib import Path
from dotenv import load_dotenv

class MuxProcessor:
    def __init__(self, mux_token_id: str = None, mux_token_secret: str = None):
        load_dotenv()
        self.base_url = 'https://api.mux.com/video/v1'
        self.auth = (mux_token_id or os.getenv('MUX_TOKEN_ID'),
                    mux_token_secret or os.getenv('MUX_TOKEN_SECRET'))
        if not all(self.auth):
            raise ValueError('Mux credentials not found')
    def create_asset(self, video_path: str, title: str = None) -> Dict:
        print(f'Creating asset for {video_path}...')
        upload_response = requests.post(
            f'{self.base_url}/uploads',
            auth=self.auth,
            json={'new_asset_settings': {'playback_policy': ['public']}}
        )
        upload_response.raise_for_status()
        upload_data = upload_response.json()['data']

        print('Uploading video file...')
        with open(video_path, 'rb') as video_file:
            upload_url = upload_data['url']
            files = {'file': video_file}
            response = requests.put(upload_url, data=files)
            response.raise_for_status()

        print('Waiting for asset to be ready...')
        asset_id = upload_data['asset_id']
        asset_data = self.wait_for_asset(asset_id)

        playback_id = None
        if asset_data.get('playback_ids'):
            playback_id = asset_data['playback_ids'][0]['id']

        return {
            'asset_id': asset_id,
            'playback_id': playback_id,
            'status': asset_data.get('status'),
            'duration': asset_data.get('duration')
        }

      def get_asset_status(self, asset_id: str) -> Dict:
        response = requests.get(
            f'{self.base_url}/assets/{asset_id}',
            auth=self.auth
        )
        response.raise_for_status()
        return response.json()['data']

    def wait_for_asset(self, asset_id: str, timeout: int = 300, interval: int = 5) -> Dict:
        import time
        start_time = time.time()

        while True:
            asset_data = self.get_asset_status(asset_id)
            status = asset_data.get('status')

            if status == 'ready':
                return asset_data
            elif status == 'errored':
                raise Exception(f'Asset processing failed: {asset_data.get("errors", [])}')

            if time.time() - start_time > timeout:
                raise TimeoutError(f'Asset {asset_id} not ready within {timeout}s')

            print(fAsset status: {status}. Waiting {interval} seconds...')
            time.sleep(interval)


    def process_season(self, segments_dir: str, output_file: str) -> Dict:
        segment_files = sorted(Path(segments_dir).glob('*.mp4'))

        if not segment_files:
            raise ValueError(f'No MP4 files found in {segments_dir}')

        timestamps_file = os.path.join(segments_dir, 'timestamps.json')
        timestamps = {}
        if os.path.exists(timestamps_file):
            with open(timestamps_file, 'r') as f:
                timestamps = json.load(f)

        episodes = []
        for i, video_path in enumerate(segment_files, 1):
            print(f
Processing episode {i}/{len(segment_files)}: {video_path.name}')

            asset_data = self.create_asset(
                str(video_path),
                title=f'Episode {i}'
            )

            timestamp_data = {}
            if timestamps and 'segments' in timestamps:
                for segment in timestamps['segments']:
                    if segment['segment'] == i - 1:
                        timestamp_data = segment
                        break

            episodes.append({
                'episode_number': i,
                'title': f'Episode {i}',
                'asset_id': asset_data['asset_id'],
                'playback_id': asset_data['playback_id'],
                'status': asset_data['status'],
                'duration': asset_data['duration'],
                'filename': video_path.name,
                'timestamps': timestamp_data
            })

            print(fEpisode {i} processed successfully:')
            print(f  Asset ID: {asset_data["asset_id"]}')
            print(f  Playback ID: {asset_data["playback_id"]}')
            print(f  Status: {asset_data["status"]}')
            print(f  Duration: {asset_data["duration"]:.2f}s')

        season_data = {
            'total_episodes': len(episodes),
            'episodes': episodes,
            'timestamps_source': timestamps_file if os.path.exists(timestamps_file) else None
        }

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(season_data, f, indent=2)

        print(f
Processing complete!')
        print(fTotal episodes: {len(episodes)}')
        print(fMetadata saved to: {output_file}')

        return season_data

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Process video segments using Mux.')
    parser.add_argument('segments_dir', help='Directory containing video segments')
    parser.add_argument('output_file', help='Path to save season metadata')
    parser.add_argument('--mux-token-id', help='Mux API Token ID (optional if set in .env)')
    parser.add_argument('--mux-token-secret', help='Mux API Token Secret (optional if set in .env)')

    args = parser.parse_args()

    processor = MuxProcessor(args.mux_token_id, args.mux_token_secret)
    season_data = processor.process_season(args.segments_dir, args.output_file)

if __name__ == '__main__':
    main()