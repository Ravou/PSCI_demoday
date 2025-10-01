import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import './index.css';

function Home() {
  return (
    <div className="home-center">
      <h1>
        Web security: explaining audits, phishing & RGPD with clarity and pedagogy
      </h1>
      <p className="main-subtitle">
        We use AI to analyze and compare a website against regulations such as RGPD, CNIL, and other data protection rules.
      </p>
    </div>
  );
}

function Login() {
  return <h1>Connecte-toi à ton compte.</h1>;
}

function Profile() {
  return <h1>Bienvenue sur ton profil !</h1>;
}

function Contact() {
  return <h1>Bienvenue sur la page de contact !</h1>;
}

function AboutUs() {
  const cards = [
    {
      title: "Analysis with Consent",
      content: "Before analyzing any website, we explicitly request the owner's or user's consent. This ensures that data is only processed with the user's clear agreement, in compliance with GDPR and other regulations."
    },
    {
      title: "Data Retention and Deletion",
      content: "Data collected is stored only for the time necessary to complete the evaluation. All information is automatically deleted after a defined period."
    },
    {
      title: "Educational Support for Beginners",
      content: "We provide detailed reports highlighting well-implemented aspects, areas to improve, and educational resources to help users correct errors and strengthen skills."
    },
    {
      title: "Security and Compliance",
      content: "We use advanced security protocols including encryption, regular audits, and restricted access. We respect users' rights and maintain full transparency."
    }
  ];

  return (
    <div className="about-us">
      <h1>Get to Know Us</h1>
      <div className="cards-container">
        {cards.map((card, index) => (
          <div key={index} className={`card card-${index % 4} ${index % 2 === 0 ? "left" : "right"}`}>
            <h2>{card.title}</h2>
            <p>{card.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}



function App() {
  return (
    <Router>
      <div className="app">
        <nav className="sidebar">
          <h1 className="main-title">PSCI</h1>
          <div className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/profile">Profile</Link>
            <Link to="/contact">Contact</Link>
            <Link to="/about">About us</Link>
          </div>
          <div className="login-card">
            <Link to="/login"><span role="img" aria-label="lock"></span> Login</Link>
          </div>
        </nav>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/about" element={<AboutUs />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;