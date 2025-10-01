import React from "react";
import "./App.css";

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <div className="logo">PSCI</div>
        <ul className="nav-links">
          <li>Home</li>
          <li>About us</li>
          <li>Services</li>
          <li>Contact</li>
        </ul>
        <button className="btn-cta">Get Started</button>
      </nav>
      <header className="hero">
        <h1>Cyber Defense That Evolves Daily.</h1>
        <p>AI-driven protection that learns, adapts, and grows stronger</p>
        <button className="btn-primary">Get Protected Today</button>
        <button className="btn-secondary">How Oryn Works</button>
      </header>
      <main>
        <section className="services">
          <div className="card">
            <h3>Cloud Security & Compliance</h3>
            <button className="btn-cta">Get Started</button>
          </div>
          <div className="card">
            <h3>AI-Driven Risk Intelligence</h3>
            <button className="btn-cta">Get Started</button>
          </div>
          <div className="card">
            <h3>Cloud Security & Compliance</h3>
            <button className="btn-cta">Get Started</button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;


