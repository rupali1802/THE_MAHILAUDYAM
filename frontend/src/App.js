import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { LanguageProvider } from './context/LanguageContext';
import Navbar from './components/Navbar';
import BottomNav from './components/BottomNav';

// Pages
import SplashScreen from './pages/SplashScreen';
import LanguageSelection from './pages/LanguageSelection';
import Dashboard from './pages/Dashboard';
import Income from './pages/Income';
import Expense from './pages/Expense';
import Sales from './pages/Sales';
import Profit from './pages/Profit';
import Payment from './pages/Payment';
import MarketPrice from './pages/MarketPrice';
import Schemes from './pages/Schemes';
import Mentor from './pages/Mentor';
import Profile from './pages/Profile';
import VoiceAssistant from './pages/VoiceAssistant';

function AppRoutes() {
  const location = useLocation();
  
  // Hide navbar on splash screen and language selection pages
  const hideNavbar = location.pathname === '/' || location.pathname === '/language';

  return (
    <>
      <Routes>
        {/* Splash → Language Selection → Dashboard (STRICT ORDER) */}
        <Route path="/" element={<SplashScreen />} />
        <Route path="/language" element={<LanguageSelection />} />

        {/* Main App Pages (all with Navbar) */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/income" element={<Income />} />
        <Route path="/expense" element={<Expense />} />
        <Route path="/sales" element={<Sales />} />
        <Route path="/profit" element={<Profit />} />
        <Route path="/payment" element={<Payment />} />
        <Route path="/market" element={<MarketPrice />} />
        <Route path="/schemes" element={<Schemes />} />
        <Route path="/mentor" element={<Mentor />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/voice" element={<VoiceAssistant />} />

        {/* Catch-all → Home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      {!hideNavbar && <Navbar />}
      <BottomNav />
    </>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </LanguageProvider>
  );
}
