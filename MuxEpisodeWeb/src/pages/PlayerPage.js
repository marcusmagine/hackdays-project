import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import EpisodeIndicator from "../components/EpisodeIndicator";
import VideoPlayer from "../components/VideoPlayer";
import { episodes } from "../data";

const PlayerPage = () => {
  const { episodeId } = useParams();
  const navigate = useNavigate();
  const [currentEpisode, setCurrentEpisode] = useState(null);

  useEffect(() => {
    const episode = episodes.find((ep) => ep.id === episodeId);

    if (episode) {
      setCurrentEpisode(episode);
      document.title = `${episode.title} - Mux Episode Player`;
    } else {
      // If episode not found, redirect to home
      navigate("/");
    }
  }, [episodeId, navigate]);

  const handleEpisodeEnd = () => {
    // Find the next episode
    const currentIndex = episodes.findIndex((ep) => ep.id === episodeId);
    const nextIndex = currentIndex + 1;

    if (nextIndex < episodes.length) {
      // Navigate to the next episode
      navigate(`/player/${episodes[nextIndex].id}`);
    } else {
      // If it's the last episode, you could navigate back to home
      // or show a completion screen
      navigate("/");
    }
  };

  const handleSelectEpisode = (id) => {
    navigate(`/player/${id}`);
  };

  if (!currentEpisode) {
    return <div className="container">Loading...</div>;
  }

  return (
    <div className="player-page">
      <div className="player-container">
        <VideoPlayer
          videoUrl={currentEpisode.videoUrl}
          onEnded={handleEpisodeEnd}
        />

        <div className="episode-info-overlay">
          <h2 className="overlay-title">{currentEpisode.title}</h2>
          <p className="overlay-description">{currentEpisode.description}</p>
        </div>
      </div>

      <div className="container">
        <EpisodeIndicator
          episodes={episodes}
          currentEpisodeId={currentEpisode.id}
          onSelectEpisode={handleSelectEpisode}
        />

        <div className="episode-navigation">
          <h3>Episodes</h3>
          <div className="episode-list">
            {episodes.map((episode) => (
              <div
                key={episode.id}
                className={`episode-list-item ${
                  episode.id === currentEpisode.id ? "active" : ""
                }`}
                onClick={() => handleSelectEpisode(episode.id)}
              >
                <div className="episode-number">{episode.id}</div>
                <div className="episode-details">
                  <div className="episode-list-title">{episode.title}</div>
                  <div className="episode-list-description">
                    {episode.description}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlayerPage;
