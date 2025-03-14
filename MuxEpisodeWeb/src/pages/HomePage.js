import React from "react";
import EpisodeCard from "../components/EpisodeCard";
import { episodes } from "../data";

const HomePage = () => {
  return (
    <div className="container">
      <div className="episode-grid">
        {episodes.map((episode) => (
          <EpisodeCard key={episode.id} episode={episode} />
        ))}
      </div>
    </div>
  );
};

export default HomePage;
