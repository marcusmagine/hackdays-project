# Movie Segmenter and Mux Processor

This project segments movies into smaller episodes based on scene changes and audio analysis, then uploads them to Mux for streaming.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Mux credentials:
   - Create a `.env` file in the project root
   - Add your Mux API credentials:
   ```
   MUX_TOKEN_ID=your_mux_token_id
   MUX_TOKEN_SECRET=your_mux_token_secret
   ```

## Usage

### Step 1: Segment the Video

1. Place your video file in the project directory
2. Update the `video_path` in `movie_segmenter.py` to point to your video file
3. Run the script:
```bash
python movie_segmenter.py
```

The segmented videos will be saved in the `segments` directory.

### Step 2: Process with Mux

After segmenting the video, you can upload the segments to Mux for streaming:

```bash
python src/processing/mux_proc.py data/segments/your_movie_folder data/output/your_movie_metadata.json
```

This will:
1. Upload each segment to Mux
2. Wait for processing to complete
3. Generate a JSON file with metadata including playback IDs

## Parameters

### Segmenter Parameters
You can modify these parameters in the script:
- `target_segment_duration`: Target duration for each segment (default: 120 seconds)
- Scene change threshold: Adjust the threshold value (default: 30) in `analyze_scene_changes()`

### Mux Processor Parameters
- `segments_dir`: Directory containing the segmented video files
- `output_file`: Path to save the season metadata JSON file
- `--mux-token-id`: Mux API Token ID (optional if set in .env)
- `--mux-token-secret`: Mux API Token Secret (optional if set in .env)

## Testing

You can verify your Mux credentials with:

```bash
python src/processing/verify_mux_credentials.py
```

To test the Mux processor with existing video segments:

```bash
python src/processing/test_mux.py path/to/segments output/metadata.json
```

## Output Format

The Mux processor generates a JSON file with the following structure:

```json
{
  "total_episodes": 8,
  "episodes": [
    {
      "episode_number": 1,
      "title": "Episode 1",
      "asset_id": "asset_id_from_mux",
      "playback_id": "playback_id_from_mux",
      "status": "ready",
      "duration": 84.92,
      "filename": "segment_001.mp4",
      "timestamps": {
        "segment": 0,
        "start": 0.0,
        "end": 84.83,
        "duration": 84.83
      }
    },
    // More episodes...
  ],
  "timestamps_source": "path/to/timestamps.json",
  "errors": []
}
```

You can use the playback IDs with the Mux player or any player that supports Mux URLs:
```
https://stream.mux.com/{playback_id}.m3u8
```