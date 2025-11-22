import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import { Toaster } from 'react-hot-toast';
import { AnalysisResult, BatchAnalysisResult } from './types';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(window.innerWidth > 1024);
  const [currentView, setCurrentView] = useState<string>('home');
  const [data, setData] = useState<AnalysisResult | BatchAnalysisResult | null>(null);
  const [isMobile, setIsMobile] = useState<boolean>(window.innerWidth <= 1024);

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth <= 1024;
      setIsMobile(mobile);
      
      // Auto-close sidebar on mobile when switching to desktop
      if (!mobile && !sidebarOpen) {
        setSidebarOpen(true);
      } else if (mobile && sidebarOpen) {
        setSidebarOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [sidebarOpen]);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleSidebarClose = () => {
    setSidebarOpen(false);
  };

  return (
    <div className="h-screen overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'rgba(30, 30, 60, 0.95)',
            color: '#fff',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)',
          },
        }}
      />

      {/* Header Component */}
      <Header sidebarOpen={sidebarOpen} toggleSidebar={toggleSidebar} />

      {/* Main Layout Container - Full height with proper spacing */}
      <div className="flex h-screen pt-16">
        {/* Sidebar - Desktop: Static with proper height (below header) */}
        <AnimatePresence>
          {(!isMobile && sidebarOpen) && (
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: 320 }}
              exit={{ width: 0 }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="flex-shrink-0 bg-gradient-to-b from-gray-900 to-gray-800 border-r border-white/10 h-full overflow-hidden"
            >
              <Sidebar
                currentView={currentView}
                setCurrentView={setCurrentView}
                setData={setData}
                onClose={handleSidebarClose}
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Mobile Sidebar Overlay */}
        <AnimatePresence>
          {isMobile && sidebarOpen && (
            <>
              {/* Backdrop */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
                onClick={handleSidebarClose}
              />

              {/* Sidebar */}
              <motion.div
                initial={{ x: -320 }}
                animate={{ x: 0 }}
                exit={{ x: -320 }}
                transition={{ type: "spring", damping: 25, stiffness: 200 }}
                className="fixed top-16 left-0 h-[calc(100vh-4rem)] w-80 z-50 bg-gradient-to-b from-gray-900 to-gray-800 border-r border-white/10"
              >
                <Sidebar
                  currentView={currentView}
                  setCurrentView={setCurrentView}
                  setData={setData}
                  onClose={handleSidebarClose}
                />
              </motion.div>
            </>
          )}
        </AnimatePresence>

        {/* Main Content Area - Full height, scrollable content */}
        <main className="flex-1 h-full overflow-hidden">
          <ChatArea
            currentView={currentView}
            data={data}
            setData={setData}
            setCurrentView={setCurrentView}
          />
        </main>
      </div>
    </div>
  );
}

export default App; 