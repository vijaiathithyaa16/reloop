import React, { useState, useEffect } from 'react';
import { User, UserRole } from './types';
import { getCurrentSession, getRoleDashboardPath } from './services/auth';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { HomePage } from './components/home/HomePage';
import { LoginPage } from './components/auth/LoginPage';
import { RegisterPage } from './components/auth/RegisterPage';
import { RBACGuard } from './components/auth/RBACGuard';
import { CitizenDashboard } from './components/dashboards/CitizenDashboard';
import { CollectorDashboard } from './components/dashboards/CollectorDashboard';
import { RecyclerDashboard } from './components/dashboards/RecyclerDashboard';
import { BrandDashboard } from './components/dashboards/BrandDashboard';
import { TelegramRedirectorModal } from './components/modals/TelegramRedirectorModal';
import { InteractiveFaceModal } from './components/modals/InteractiveFaceModal';

export default function App() {
  const [currentPath, setCurrentPath] = useState<string>(() => {
    return window.location.pathname || '/';
  });

  const [currentUser, setCurrentUser] = useState<User | null>(() => {
    return getCurrentSession().user;
  });

  const [isTelegramOpen, setIsTelegramOpen] = useState(false);
  const [isFaceModalOpen, setIsFaceModalOpen] = useState(false);

  // Sync auth state
  useEffect(() => {
    const handleAuthChange = () => {
      const session = getCurrentSession();
      setCurrentUser(session.user);
    };

    window.addEventListener('reloop_auth_changed', handleAuthChange);
    window.addEventListener('storage', handleAuthChange);

    const handlePopState = () => {
      setCurrentPath(window.location.pathname || '/');
    };
    window.addEventListener('popstate', handlePopState);

    return () => {
      window.removeEventListener('reloop_auth_changed', handleAuthChange);
      window.removeEventListener('storage', handleAuthChange);
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  const navigate = (path: string) => {
    window.history.pushState({}, '', path);
    setCurrentPath(path);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Route matching
  const renderCurrentView = () => {
    // Exact home
    if (currentPath === '/' || currentPath === '') {
      return (
        <HomePage
          onNavigate={navigate}
          onOpenTelegram={() => setIsTelegramOpen(true)}
          onOpenInteractiveFace={() => setIsFaceModalOpen(true)}
          currentUser={currentUser}
        />
      );
    }

    // Login
    if (currentPath === '/login') {
      return <LoginPage onNavigate={navigate} />;
    }

    // Register
    if (currentPath === '/register') {
      return <RegisterPage onNavigate={navigate} />;
    }

    // Citizen Dashboard
    if (currentPath === '/dashboard/citizen' || currentPath === '/dashboard/user') {
      return (
        <RBACGuard currentUser={currentUser} requiredRole="user" onNavigate={navigate}>
          <CitizenDashboard
            currentUser={currentUser!}
            onOpenTelegram={() => setIsTelegramOpen(true)}
          />
        </RBACGuard>
      );
    }

    // Collector Dashboard
    if (currentPath === '/dashboard/collector') {
      return (
        <RBACGuard currentUser={currentUser} requiredRole="collector" onNavigate={navigate}>
          <CollectorDashboard currentUser={currentUser!} />
        </RBACGuard>
      );
    }

    // Recycler Dashboard
    if (currentPath === '/dashboard/recycler') {
      return (
        <RBACGuard currentUser={currentUser} requiredRole="recycler" onNavigate={navigate}>
          <RecyclerDashboard currentUser={currentUser!} />
        </RBACGuard>
      );
    }

    // Brand / CPCH Dashboard
    if (currentPath === '/dashboard/brand-cpcb' || currentPath === '/dashboard/brand') {
      return (
        <RBACGuard currentUser={currentUser} requiredRole="brand_cpcb" onNavigate={navigate}>
          <BrandDashboard currentUser={currentUser!} />
        </RBACGuard>
      );
    }

    // Fallback: If unknown path, show Home
    return (
      <HomePage
        onNavigate={navigate}
        onOpenTelegram={() => setIsTelegramOpen(true)}
        onOpenInteractiveFace={() => setIsFaceModalOpen(true)}
        currentUser={currentUser}
      />
    );
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f8fafc] text-slate-900 selection:bg-emerald-500 selection:text-white">
      {/* Sticky Top Navigation */}
      <Navbar
        currentUser={currentUser}
        currentPath={currentPath}
        onNavigate={navigate}
        onOpenTelegram={() => setIsTelegramOpen(true)}
        onOpenInteractiveFace={() => setIsFaceModalOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1">{renderCurrentView()}</main>

      {/* Global Footer with Copyright & Regulatory Disclaimers */}
      <Footer
        onNavigate={navigate}
        onOpenTelegram={() => setIsTelegramOpen(true)}
      />

      {/* Telegram Chatbot Redirector Modal */}
      <TelegramRedirectorModal
        isOpen={isTelegramOpen}
        onClose={() => setIsTelegramOpen(false)}
      />

      {/* Interactive Face / AI Avatar Assistant Modal */}
      <InteractiveFaceModal
        isOpen={isFaceModalOpen}
        onClose={() => setIsFaceModalOpen(false)}
      />
    </div>
  );
}
