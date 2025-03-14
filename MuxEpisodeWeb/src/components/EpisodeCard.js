import React from "react";
import { Link } from "react-router-dom";

const EpisodeCard = ({ episode }) => {
  return (
    <Link to={`/player/${episode.id}`} style={{ textDecoration: "none" }}>
      <div className="episode-card">
        <div className="episode-thumbnail">
          <div className="thumbnail-text">{episode.title}</div>
          <div className="thumbnail-overlay">
            <div className="play-icon">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M8 5V19L19 12L8 5Z" fill="#333" />
              </svg>
            </div>
          </div>
        </div>
        <div className="episode-info">
          <h3 className="episode-title">{episode.title}</h3>
          <p className="episode-description">{episode.description}</p>
        </div>
      </div>
    </Link>
  );
};

export default EpisodeCard;
