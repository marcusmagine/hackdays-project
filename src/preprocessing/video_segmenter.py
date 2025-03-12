import os
from scenedetect import detect, ContentDetector, split_video_ffmpeg
import json

def merge_scenes_to_duration(scenes, min_duration=45, max_duration=90):
    """Merge scenes to achieve minimum duration while respecting maximum duration."""
    if not scenes:
        return []

    merged = []
    current_scenes = [scenes[0]]
    current_duration = scenes[0][1].get_seconds() - scenes[0][0].get_seconds()

    for scene in scenes[1:]:
        scene_duration = scene[1].get_seconds() - scene[0].get_seconds()
        potential_duration = current_duration + scene_duration

        if potential_duration <= max_duration:
            # Can merge this scene
            current_scenes.append(scene)
            current_duration = potential_duration
        else:
            # Current group is either good to go or needs splitting
            if current_duration >= min_duration:
                # Current group meets minimum duration
                merged_scene = (current_scenes[0][0], current_scenes[-1][1])
                merged.append(merged_scene)
                current_scenes = [scene]
                current_duration = scene_duration
            else:
                # Need to include this scene even though it exceeds max_duration
                current_scenes.append(scene)
                merged_scene = (current_scenes[0][0], current_scenes[-1][1])
                merged.append(merged_scene)
                current_scenes = []
                current_duration = 0

    # Handle remaining scenes
    if current_scenes:
        if current_duration >= min_duration or len(merged) == 0:
            merged_scene = (current_scenes[0][0], current_scenes[-1][1])
            merged.append(merged_scene)
        else:
            # Merge with last segment if current duration is too short
            last_scene = merged.pop()
            merged_scene = (last_scene[0], current_scenes[-1][1])
            merged.append(merged_scene)

    return merged

def segment_video(video_path, output_dir, threshold=30.0, min_duration=45, max_duration=90):
    """
    Segment video based on scene changes and save timestamps.
    Args:
        video_path: Path to input video
        output_dir: Directory to save segments
        threshold: Scene detection threshold (higher = less sensitive)
        min_duration: Minimum segment duration in seconds (default: 45)
        max_duration: Maximum segment duration in seconds (default: 90)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Detect scenes using content detection
    scenes = detect(video_path, ContentDetector(threshold=threshold))

    # Merge scenes to achieve target duration
    scenes = merge_scenes_to_duration(scenes, min_duration, max_duration)

    # Convert scenes to timestamps
    timestamps = []
    for i, scene in enumerate(scenes):
        start_time = scene[0].get_seconds()
        end_time = scene[1].get_seconds()
        duration = end_time - start_time

        timestamps.append({
            'segment': i,
            'start': start_time,
            'end': end_time,
            'duration': duration
        })

    # Split video into segments
    split_video_ffmpeg(video_path, scenes, output_dir)

    # Save timestamps to JSON file
    timestamps_file = os.path.join(output_dir, 'timestamps.json')
    with open(timestamps_file, 'w') as f:
        json.dump({'segments': timestamps}, f, indent=2)

    print(f"Created {len(scenes)} segments")
    for i, ts in enumerate(timestamps):
        duration = ts['duration']
        status = "OK" if min_duration <= duration <= max_duration else "WARNING"
        print(f"Segment {i}: {duration:.1f}s ({status})")
    print(f"Timestamps saved to {timestamps_file}")

if __name__ == "__main__":
    video_path = "data/input/tears_of_steel_720p.mov"
    output_dir = "data/segments/tears_of_steel"
    segment_video(video_path, output_dir)