# Mux Episode Web Player

A web application for playing episodic content from Mux. This web client presents content in the same manner as the mobile application, allowing users to browse and stream episodes using Mux's video delivery platform.

## Features

- Browse available episodes
- Play episodes with HLS.js video player
- Navigate between episodes
- Episode queue for quick navigation
- Automatic playback of next episode
- Responsive design that works on desktop and mobile
- Visual episode queue indicator showing current position

## Prerequisites

- Node.js (v14 or newer)
- npm or yarn

## Installation

1. Navigate to the MuxEpisodeWeb directory
2. Install dependencies:

```bash
npm install
# or
yarn install
```

## Configuration

The app uses sample data by default. To use your own Mux content:

1. Update the `episodes` array in `src/data.js` with your episode data and Mux playback IDs.
2. Make sure your Mux playback IDs are valid and accessible.

Example:

```javascript
export const episodes = [
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

Start the development server:

```bash
npm start
# or
yarn start
```

This will start the app on http://localhost:3000

## Building for Production

Build the app for production:

```bash
npm run build
# or
yarn build
```

The build files will be in the `dist` directory.

## Project Structure

- `/src`: Source code
  - `/components`: Reusable UI components
  - `/pages`: App pages
  - `App.js`: Main application component
  - `data.js`: Sample episode data
  - `index.js`: Entry point
  - `styles.css`: Global styles
- `/public`: Static assets

## Key Components

- `VideoPlayer`: Custom video player component using HLS.js
- `HomePage`: Page for browsing available episodes
- `PlayerPage`: Page for playing episodes with controls
- `EpisodeIndicator`: Visual indicator for episode navigation
- `EpisodeCard`: Card component for displaying episode information

## Integration with Mux

This app is designed to work with content processed by the Movie Segmenter and Mux Processor. It uses the playback IDs generated when uploading segments to Mux to stream the content.

### Mux Playback URLs

The app uses Mux's HLS streaming URLs in the format:

```
https://stream.mux.com/PLAYBACK_ID.m3u8
```

Replace `PLAYBACK_ID` with the playback ID generated when uploading your video to Mux.
