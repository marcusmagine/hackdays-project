import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <Link to="/" style={{ textDecoration: "none" }}>
            <h1 className="header-title">Mux Episode Player</h1>
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
