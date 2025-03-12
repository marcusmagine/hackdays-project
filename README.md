# Movie Segmenter

This project segments movies into smaller episodes based on scene changes and audio analysis.

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

## Usage

1. Place your video file in the project directory
2. Update the `video_path` in `movie_segmenter.py` to point to your video file
3. Run the script:
```bash
python movie_segmenter.py
```

The segmented videos will be saved in the `segments` directory.

## Parameters

You can modify these parameters in the script:
- `target_segment_duration`: Target duration for each segment (default: 120 seconds)
- Scene change threshold: Adjust the threshold value (default: 30) in `analyze_scene_changes()`