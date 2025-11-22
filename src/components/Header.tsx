import React from 'react';
import { Menu, Sparkles, Settings, User } from 'lucide-react';
import { HeaderProps } from '../types';

const Header: React.FC<HeaderProps> = ({ sidebarOpen, toggleSidebar }) => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-md border-b border-white/10">
      <div className="flex items-center justify-between px-4 md:px-6 py-4">
        <div className="flex items-center gap-3 md:gap-4">
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-xl bg-white/10 border border-white/20 text-white/70 hover:text-white hover:bg-white/15 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-primary-500/50"
            aria-label="Toggle sidebar"
          >
            <Menu size={20} />
          </button>
          <h1 className="text-lg md:text-xl font-bold gradient-text">Resume Analyzer</h1>
        </div>

        <div className="flex items-center gap-2 md:gap-3">
          <button className="btn-primary flex items-center gap-2 text-xs md:text-sm">
            <Sparkles size={16} />
            <span className="hidden sm:inline">Get Plus</span>
          </button>
          <button className="p-2 rounded-xl bg-white/10 border border-white/20 text-white/70 hover:text-white hover:bg-white/15 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-primary-500/50">
            <Settings size={20} />
          </button>
          <button className="p-2 rounded-xl bg-white/10 border border-white/20 text-white/70 hover:text-white hover:bg-white/15 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-primary-500/50">
            <User size={20} />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header; 