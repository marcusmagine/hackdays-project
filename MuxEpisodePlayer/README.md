# Mux Episode Player

A React Native mobile application for playing episodic content from Mux. This app allows users to browse movies that have been segmented into episodes and stream them using Mux's video delivery platform.

## Features

- Browse available movies
- Play episodes with a custom video player
- Navigate between episodes with swipe gestures
- Portrait mode: Swipe up/down to navigate episodes
- Landscape mode: Swipe left/right to navigate episodes
- Episode queue for quick navigation
- Automatic playback of next episode
- Responsive UI that adapts to different device orientations
- Visual episode queue indicator showing current position

## User Interface

The app features a modern, intuitive user interface designed for optimal video viewing experience:

### Home Screen

- Clean, card-based layout for browsing available episodes
- Episode thumbnails with title and description
- Tap to play functionality

### Player Screen

- Full-screen video playback
- Custom player controls (play/pause, seek)
- Episode information overlay
- Swipe navigation between episodes
- Visual indicators for episode transitions
- Orientation-aware layout that adapts to portrait and landscape modes

### Episode Queue

- Visual representation of all available episodes
- Current episode indicator
- Quick navigation by tapping on episode indicators
- Automatically visible when swiping between episodes

## Prerequisites

- Node.js (v14 or newer)
- npm or yarn
- React Native development environment set up
- iOS: XCode and CocoaPods
- Android: Android Studio and Android SDK

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:

```bash
npm install
# or
yarn install
```

4. For iOS, install pods:

```bash
cd ios && pod install && cd ..
```

## Configuration

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

## Running the App

### iOS

```bash
npx react-native run-ios
```

### Android

```bash
npx react-native run-android
```

### Web (Experimental)

The app includes experimental web support:

```bash
npm run web
```

## Project Structure

- `App.js`: Main application component
- `/src`: Source code
  - `/components`: Reusable UI components
  - `/screens`: App screens
  - `/navigation`: Navigation setup
  - `/config`: Configuration files
  - `/utils`: Utility functions

## Key Components

- `VideoPlayer`: Custom video player component using react-native-video
- `HomeScreen`: Screen for browsing available episodes
- `PlayerScreen`: Screen for playing episodes with controls
- `EpisodeIndicator`: Visual indicator for episode navigation
- `CustomControls`: Custom video player controls

## Gestures

The app uses swipe gestures for navigation:

- **Portrait Mode**:

  - Swipe up: Go to previous episode
  - Swipe down: Go to next episode

- **Landscape Mode**:
  - Swipe left: Go to next episode
  - Swipe right: Go to previous episode

## Presentation Layer

The presentation layer of the app is built with a focus on:

### Responsive Design

- Adapts to different screen sizes and orientations
- Optimized layouts for both phones and tablets
- Proper handling of notches and safe areas

### Visual Feedback

- Smooth animations for transitions between episodes
- Visual indicators for loading states
- Haptic feedback on navigation (where supported)

### Accessibility

- Support for screen readers
- Appropriate contrast ratios
- Scalable text that respects system settings

### Performance

- Optimized rendering for smooth playback
- Efficient memory management for video content
- Minimal UI re-renders during playback

## Integration with Mux

This app is designed to work with content processed by the Movie Segmenter and Mux Processor. It uses the playback IDs generated when uploading segments to Mux to stream the content.

### Mux Playback URLs

The app uses Mux's HLS streaming URLs in the format:

```
https://stream.mux.com/PLAYBACK_ID.m3u8
```

Replace `PLAYBACK_ID` with the playback ID generated when uploading your video to Mux.

## Troubleshooting

### iOS Build Issues

If you encounter issues with the iOS build:

1. Make sure you have the latest version of CocoaPods installed
2. Try cleaning the build folder: `cd ios && xcodebuild clean && cd ..`
3. Reinstall pods: `cd ios && pod install && cd ..`

### Android Build Issues

If you encounter issues with the Android build:

1. Make sure you have the correct Android SDK installed
2. Try cleaning the build: `cd android && ./gradlew clean && cd ..`

## License

MIT
