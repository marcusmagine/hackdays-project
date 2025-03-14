import React from "react";
import { Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import HomePage from "./pages/HomePage";
import PlayerPage from "./pages/PlayerPage";

const App = () => {
  return (
    <>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/player/:episodeId" element={<PlayerPage />} />
        </Routes>
      </main>
    </>
  );
};

export default App;
