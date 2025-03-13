import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the module
sys.path.append(str(Path(__file__).parent))
from mux_proc import MuxProcessor
from dotenv import load_dotenv

def test_mux_processor(segments_dir, output_file, mux_token_id=None, mux_token_secret=None):
    """
    Test the MuxProcessor with existing video files.

    Args:
        segments_dir: Directory containing the preprocessed video segments
        output_file: Path to save the season metadata
        mux_token_id: Optional Mux API Token ID (overrides .env)
        mux_token_secret: Optional Mux API Token Secret (overrides .env)
    """
    # Load environment variables with override
    load_dotenv(override=True)

    # Debug: Print environment variables
    env_token_id = os.getenv("MUX_TOKEN_ID")
    env_token_secret = os.getenv("MUX_TOKEN_SECRET")
    print(f"Environment MUX_TOKEN_ID: {'Found' if env_token_id else 'Not found'}")
    print(f"Environment MUX_TOKEN_SECRET: {'Found' if env_token_secret else 'Not found'}")

    # Use command-line args if provided, otherwise use env vars
    token_id = mux_token_id or env_token_id
    token_secret = mux_token_secret or env_token_secret

    print(f"Using MUX_TOKEN_ID: {'Provided' if token_id else 'Not provided'}")
    print(f"Using MUX_TOKEN_SECRET: {'Provided' if token_secret else 'Not provided'}")

    # Create processor instance
    processor = MuxProcessor(token_id, token_secret)

    try:
        # Process the videos
        print(f"\nProcessing videos from {segments_dir}...")
        season_data = processor.process_season(segments_dir, output_file)

        # Verify the results
        print("\nVerifying results...")
        assert season_data["total_episodes"] > 0, "No episodes were processed"
        assert len(season_data["episodes"]) > 0, "No episode data was returned"

        # Print summary
        print(f"\nProcessed {season_data['total_episodes']} episodes successfully!")

        for episode in season_data["episodes"]:
            print(f"\nEpisode {episode['episode_number']}:")
            print(f"  Asset ID: {episode['asset_id']}")
            print(f"  Playback ID: {episode['playback_id']}")
            print(f"  Status: {episode['status']}")
            print(f"  Duration: {episode['duration']:.2f}s")

        print(f"\nMetadata saved to: {output_file}")

    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        raise

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test the Mux processor with existing video files.")
    parser.add_argument("segments_dir", help="Directory containing video segments")
    parser.add_argument("output_file", help="Path to save season metadata")
    parser.add_argument("--mux-token-id", help="Mux API Token ID (optional if set in .env)")
    parser.add_argument("--mux-token-secret", help="Mux API Token Secret (optional if set in .env)")

    args = parser.parse_args()

    test_mux_processor(
        args.segments_dir,
        args.output_file,
        args.mux_token_id,
        args.mux_token_secret
    )