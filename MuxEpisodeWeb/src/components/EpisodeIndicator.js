import React from "react";

const EpisodeIndicator = ({ episodes, currentEpisodeId, onSelectEpisode }) => {
  return (
    <div className="episode-queue">
      {episodes.map((episode) => (
        <div
          key={episode.id}
          className={`episode-indicator ${
            episode.id === currentEpisodeId ? "active" : ""
          }`}
          onClick={() => onSelectEpisode(episode.id)}
          title={episode.title}
        />
      ))}
    </div>
  );
};

export default EpisodeIndicator;
