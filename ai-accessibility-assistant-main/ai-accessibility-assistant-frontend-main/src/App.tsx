import React, { useState } from 'react';
import Dashboard from './pages/Dashboard';
import Simplifier from './pages/Simplifier';
import Settings from './pages/Settings';
import History from './pages/History';
import About from './pages/About';
import Navbar from './components/Navbar';
import './App.css';

const DEFAULT_USER_ID = 'demo-user-001';

type NavKey = 'home' | 'simplifier' | 'dashboard' | 'history' | 'settings' | 'about';

const App: React.FC = () => {
  const [activeNav, setActiveNav] = useState<NavKey>('home');
  const [userId, setUserId] = useState<string>(DEFAULT_USER_ID);
  const [defaultProfile, setDefaultProfile] = useState<string>('default');
  const [dyslexiaDefault, setDyslexiaDefault] = useState<boolean>(false);
  const [audioDefault, setAudioDefault] = useState<boolean>(false);
  const [fontSize, setFontSize] = useState<'small'|'medium'|'large'>('medium');
  const [theme, setTheme] = useState<'light'|'dark'>('light');
  
  return (
    <div className="app-root">
      <main className="app-shell">
        <Navbar active={activeNav} onChange={setActiveNav} />

        {activeNav === 'home' && (
          <section className="landing">
            <div className="landing-inner">
              <h1 className="landing-title">Cognitive Accessibility Platform</h1>
              <p className="landing-subtitle">
                Adapt complex text for diverse cognitive needs using AI.
              </p>
              <button
                type="button"
                className="primary-button landing-button"
                onClick={() => setActiveNav('simplifier')}
              >
                Start Simplifying
              </button>
            </div>
          </section>
        )}

        {activeNav === 'simplifier' && (
          <Simplifier userId={userId} onUserIdChange={setUserId} />
        )}

        {activeNav === 'dashboard' && (
          <section className="card app-section">
            <Dashboard userId={userId} />
          </section>
        )}

        {activeNav === 'history' && (
          <section className="card app-section">
            <History />
          </section>
        )}

        {activeNav === 'about' && (
          <section className="card app-section">
            <About />
          </section>
        )}

        {activeNav === 'settings' && (
          <section className="card app-section">
            <Settings
              defaultProfile={defaultProfile}
              onProfileChange={setDefaultProfile}
              dyslexiaDefault={dyslexiaDefault}
              onDyslexiaDefaultChange={setDyslexiaDefault}
              audioDefault={audioDefault}
              onAudioDefaultChange={setAudioDefault}
              fontSize={fontSize}
              onFontSizeChange={setFontSize}
              theme={theme}
              onThemeChange={setTheme}
            />
          </section>
        )}
      </main>
    </div>
  );
};

export default App;
