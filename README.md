# Movie Segmenter and Mux Episode Player

This project consists of two main components:

1. A Movie Segmenter that divides movies into smaller episodes based on scene changes and audio analysis
2. A React Native mobile application for playing these episodic content from Mux

## Movie Segmenter and Mux Processor

This component segments movies into smaller episodes based on scene changes and audio analysis, then uploads them to Mux for streaming.

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
    }
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

## Mux Episode Player

A React Native mobile application for playing episodic content from Mux. This app allows users to browse movies that have been segmented into episodes and stream them using Mux's video delivery platform.

### Features

- Browse available movies
- Play episodes with a custom video player
- Navigate between episodes with swipe gestures
- Portrait mode: Swipe up/down to navigate episodes
- Landscape mode: Swipe left/right to navigate episodes
- Episode queue for quick navigation
- Automatic playback of next episode
- Responsive UI that adapts to different device orientations
- Visual episode queue indicator showing current position

### User Interface

The app features a modern, intuitive user interface designed for optimal video viewing experience:

#### Home Screen

- Clean, card-based layout for browsing available episodes
- Episode thumbnails with title and description
- Tap to play functionality

#### Player Screen

- Full-screen video playback
- Custom player controls (play/pause, seek)
- Episode information overlay
- Swipe navigation between episodes
- Visual indicators for episode transitions
- Orientation-aware layout that adapts to portrait and landscape modes

#### Episode Queue

- Visual representation of all available episodes
- Current episode indicator
- Quick navigation by tapping on episode indicators
- Automatically visible when swiping between episodes

### Prerequisites

- Node.js (v14 or newer)
- npm or yarn
- React Native development environment set up
- iOS: XCode and CocoaPods
- Android: Android Studio and Android SDK

### Installation

1. Navigate to the MuxEpisodePlayer directory
2. Install dependencies:

```bash
npm install
# or
yarn install
```

3. For iOS, install pods:

```bash
cd ios && pod install && cd ..
```

### Configuration

The app uses sample data by default. To use your own Mux content:

1. Update the `episodes` array in `App.js` with your episode data and Mux playback IDs.
2. Make sure your Mux playback IDs are valid and accessible.

Example:

```javascript
const episodes = [
  {
    id: "1",
    title: "Episode 1",
    description: "First episode of the series",
    videoUrl: "https://stream.mux.com/YOUR_PLAYBACK_ID.m3u8",
  },
  // Add more episodes...
];
```

### Running the App

#### iOS

```bash
npx react-native run-ios
```

#### Android

```bash
npx react-native run-android
```

#### Web (Experimental)

The app includes experimental web support:

```bash
npm run web
```

### Project Structure

- `App.js`: Main application component
- `/src`: Source code
  - `/components`: Reusable UI components
  - `/screens`: App screens
  - `/navigation`: Navigation setup
  - `/config`: Configuration files
  - `/utils`: Utility functions

### Key Components

- `VideoPlayer`: Custom video player component using react-native-video
- `HomeScreen`: Screen for browsing available episodes
- `PlayerScreen`: Screen for playing episodes with controls
- `EpisodeIndicator`: Visual indicator for episode navigation
- `CustomControls`: Custom video player controls

### Gestures

The app uses swipe gestures for navigation:

- **Portrait Mode**:

  - Swipe up: Go to previous episode
  - Swipe down: Go to next episode

- **Landscape Mode**:
  - Swipe left: Go to next episode
  - Swipe right: Go to previous episode

### Presentation Layer

The presentation layer of the app is built with a focus on:

#### Responsive Design

- Adapts to different screen sizes and orientations
- Optimized layouts for both phones and tablets
- Proper handling of notches and safe areas

#### Visual Feedback

- Smooth animations for transitions between episodes
- Visual indicators for loading states
- Haptic feedback on navigation (where supported)

#### Accessibility

- Support for screen readers
- Appropriate contrast ratios
- Scalable text that respects system settings

#### Performance

- Optimized rendering for smooth playback
- Efficient memory management for video content
- Minimal UI re-renders during playback

### Integration with Mux

This app is designed to work with content processed by the Movie Segmenter and Mux Processor. It uses the playback IDs generated when uploading segments to Mux to stream the content.

#### Mux Playback URLs

The app uses Mux's HLS streaming URLs in the format:

```
https://stream.mux.com/PLAYBACK_ID.m3u8
```

Replace `PLAYBACK_ID` with the playback ID generated when uploading your video to Mux.

### Troubleshooting

#### iOS Build Issues

If you encounter issues with the iOS build:

1. Make sure you have the latest version of CocoaPods installed
2. Try cleaning the build folder: `cd ios && xcodebuild clean && cd ..`
3. Reinstall pods: `cd ios && pod install && cd ..`

#### Android Build Issues

If you encounter issues with the Android build:

1. Make sure you have the correct Android SDK installed
2. Try cleaning the build: `cd android && ./gradlew clean && cd ..`

## License

MIT
