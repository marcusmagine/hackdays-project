import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from scipy.io import wavfile
from scipy import signal
import librosa
import os
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MovieSegmenter:
    def __init__(self, video_path: str, target_segment_duration: int = 120):
        """
        Initialize the MovieSegmenter.
        
        Args:
            video_path: Path to the video file
            target_segment_duration: Target duration for each segment in seconds (default: 120s / 2 minutes)
        """
        self.video_path = video_path
        self.target_segment_duration = target_segment_duration
        self.video = VideoFileClip(video_path)
        self.duration = self.video.duration
        
    def analyze_scene_changes(self) -> List[float]:
        """
        Detect major scene changes using frame difference analysis.
        
        Returns:
            List of timestamps (in seconds) where significant scene changes occur
        """
        logger.info("Analyzing scene changes...")
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        prev_frame = None
        scene_changes = []
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Calculate frame difference
                diff = cv2.absdiff(gray, prev_frame)
                mean_diff = np.mean(diff)
                
                # If difference is significant, mark as scene change
                if mean_diff > 30:  # Threshold can be adjusted
                    timestamp = frame_count / fps
                    scene_changes.append(timestamp)
            
            prev_frame = gray
            frame_count += 1
            
        cap.release()
        return scene_changes

    def analyze_audio_changes(self) -> List[float]:
        """
        Detect significant audio changes using librosa.
        
        Returns:
            List of timestamps where significant audio changes occur
        """
        logger.info("Analyzing audio changes...")
        # Extract audio from video
        audio = self.video.audio
        if audio is None:
            logger.warning("No audio track found in video")
            return []
            
        # Save audio temporarily
        temp_audio = "temp_audio.wav"
        audio.write_audiofile(temp_audio)
        
        # Load audio with librosa
        y, sr = librosa.load(temp_audio)
        
        # Detect onset strength
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        
        # Find peaks in onset strength
        peaks = signal.find_peaks(onset_env, height=np.mean(onset_env) + np.std(onset_env))[0]
        
        # Convert frame indices to timestamps
        timestamps = librosa.frames_to_time(peaks, sr=sr)
        
        # Clean up
        os.remove(temp_audio)
        
        return timestamps.tolist()

    def find_optimal_segments(self, scene_changes: List[float], audio_changes: List[float]) -> List[float]:
        """
        Find optimal segment boundaries using both scene and audio changes.
        
        Args:
            scene_changes: List of scene change timestamps
            audio_changes: List of audio change timestamps
            
        Returns:
            List of optimal segment boundary timestamps
        """
        logger.info("Finding optimal segments...")
        # Combine and sort all potential change points
        all_changes = sorted(set(scene_changes + audio_changes))
        
        segments = []
        current_time = 0
        
        while current_time < self.duration:
            target_end = current_time + self.target_segment_duration
            
            # Find the closest change point to our target duration
            closest_change = min(
                (t for t in all_changes if t > current_time),
                key=lambda x: abs(x - target_end),
                default=target_end
            )
            
            # If no change point found or it's too far, use target duration
            if abs(closest_change - target_end) > self.target_segment_duration * 0.2:
                segments.append(target_end)
            else:
                segments.append(closest_change)
            
            current_time = segments[-1]
        
        return segments

    def segment_movie(self) -> List[Tuple[float, float]]:
        """
        Segment the movie into micro-episodes.
        
        Returns:
            List of tuples containing start and end times for each segment
        """
        logger.info(f"Starting movie segmentation for {self.video_path}")
        
        # Get scene and audio changes
        scene_changes = self.analyze_scene_changes()
        audio_changes = self.analyze_audio_changes()
        
        # Find optimal segment boundaries
        segment_boundaries = self.find_optimal_segments(scene_changes, audio_changes)
        
        # Create segments
        segments = []
        start_time = 0
        
        for end_time in segment_boundaries:
            segments.append((start_time, end_time))
            start_time = end_time
            
        logger.info(f"Created {len(segments)} segments")
        return segments

    def export_segments(self, output_dir: str, segments: List[Tuple[float, float]]) -> None:
        """
        Export the segments as individual video files.
        
        Args:
            output_dir: Directory to save the segments
            segments: List of (start_time, end_time) tuples
        """
        logger.info(f"Exporting segments to {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
        
        for i, (start, end) in enumerate(segments):
            output_path = os.path.join(output_dir, f"segment_{i+1:03d}.mp4")
            segment = self.video.subclip(start, end)
            segment.write_videofile(output_path)
            
        logger.info("Export complete")

def main():
    # Example usage
    video_path = "your_movie.mp4"  # Replace with your video path
    output_dir = "segments"
    
    segmenter = MovieSegmenter(video_path)
    segments = segmenter.segment_movie()
    segmenter.export_segments(output_dir, segments)

if __name__ == "__main__":
    main()