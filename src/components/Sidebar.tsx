import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Bot, 
  Crown, 
  FileText, 
  Briefcase, 
  Upload,
  Home,
  BarChart3,
  History,
  Settings
} from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { SidebarProps } from '../types';
import { API_ENDPOINTS } from '../config/api';

const Sidebar: React.FC<SidebarProps> = ({ currentView, setCurrentView, setData, onClose }) => {
  const [resumeList, setResumeList] = useState<string[]>([]);
  const [jdHistory, setJdHistory] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      // Fetch resume list
      const resumeResponse = await axios.get(API_ENDPOINTS.RESUMES);
      setResumeList(resumeResponse.data.resumes || []);

      // Fetch JD history
      const jdResponse = await axios.get(API_ENDPOINTS.JD_HISTORY);
      setJdHistory(jdResponse.data.jd_list || []);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleNewAnalysis = () => {
    setCurrentView('upload');
    onClose();
  };

  const handleResumeClick = async (filename: string) => {
    try {
      const response = await axios.get(API_ENDPOINTS.RESUME(filename));
      setData(response.data);
      setCurrentView('resume-details');
      onClose();
    } catch (error) {
      console.error('Error fetching resume:', error);
      toast.error('Failed to load resume details');
    }
  };

  const handleJdClick = (jd: string) => {
    // This could open a modal or navigate to a specific view
    toast.success('Job description selected');
    onClose();
  };

  const navigationItems = [
    { id: 'home', label: 'Home', icon: Home, action: () => setCurrentView('home') },
    { id: 'upload', label: 'Upload & Analyze', icon: Upload, action: handleNewAnalysis },
    { id: 'analytics', label: 'Analytics', icon: BarChart3, action: () => setCurrentView('analytics') },
    { id: 'history', label: 'History', icon: History, action: () => setCurrentView('history') },
    { id: 'settings', label: 'Settings', icon: Settings, action: () => setCurrentView('settings') },
  ];

  return (
    <div className="h-full flex flex-col bg-gradient-to-b from-gray-900 to-gray-800">
      {/* Navigation */}
      <div className="p-4 md:p-6">
        <nav className="space-y-2">
          {navigationItems.map((item) => (
            <button
              key={item.id}
              onClick={item.action}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 text-left ${
                currentView === item.id
                  ? 'bg-primary-500/20 border border-primary-500/30 text-primary-300'
                  : 'text-white/70 hover:text-white hover:bg-white/10'
              }`}
            >
              <item.icon size={20} />
              <span className="font-medium">{item.label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* New Analysis Button */}
      <div className="px-4 md:px-6 mb-6">
        <button
          onClick={handleNewAnalysis}
          className="w-full btn-primary flex items-center justify-center gap-3 py-4"
        >
          <Bot size={20} />
          <span className="font-semibold">New Analysis</span>
        </button>
      </div>

      {/* Recent Resumes */}
      <div className="flex-1 overflow-hidden">
        <div className="px-4 md:px-6 mb-4">
          <h3 className="text-sm font-semibold text-white/60 uppercase tracking-wider mb-3">
            Recent Resumes
          </h3>
        </div>
        
        <div className="px-4 md:px-6 space-y-2 max-h-48 overflow-y-auto">
          {loading ? (
            <div className="text-center py-4">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-500 mx-auto"></div>
            </div>
          ) : resumeList.length > 0 ? (
            resumeList.slice(0, 5).map((resume, index) => (
              <motion.button
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                onClick={() => handleResumeClick(resume)}
                className="w-full flex items-center gap-3 p-3 rounded-xl text-left text-white/70 hover:text-white hover:bg-white/10 transition-all duration-300 group"
              >
                <FileText size={16} className="text-primary-400 group-hover:text-primary-300" />
                <span className="flex-1 text-sm truncate">{resume}</span>
              </motion.button>
            ))
          ) : (
            <div className="text-center py-4">
              <FileText size={24} className="text-white/30 mx-auto mb-2" />
              <p className="text-xs text-white/50">No resumes uploaded</p>
            </div>
          )}
        </div>
      </div>

      {/* Recent Job Descriptions */}
      <div className="px-4 md:px-6 mb-4">
        <h3 className="text-sm font-semibold text-white/60 uppercase tracking-wider mb-3">
          Recent Jobs
        </h3>
      </div>
      
      <div className="px-4 md:px-6 space-y-2 max-h-32 overflow-y-auto mb-6">
        {loading ? (
          <div className="text-center py-4">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-500 mx-auto"></div>
          </div>
        ) : jdHistory.length > 0 ? (
          jdHistory.slice(0, 3).map((jd, index) => (
            <motion.button
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => handleJdClick(jd)}
              className="w-full flex items-center gap-3 p-3 rounded-xl text-left text-white/70 hover:text-white hover:bg-white/10 transition-all duration-300 group"
            >
              <Briefcase size={16} className="text-primary-400 group-hover:text-primary-300" />
              <span className="flex-1 text-sm truncate">{jd}</span>
            </motion.button>
          ))
        ) : (
          <div className="text-center py-4">
            <Briefcase size={24} className="text-white/30 mx-auto mb-2" />
            <p className="text-xs text-white/50">No job descriptions</p>
          </div>
        )}
      </div>

      {/* Upgrade Button */}
      <div className="p-4 md:p-6 border-t border-white/10">
        <button className="w-full btn-primary flex items-center justify-center gap-3 py-4 mb-2">
          <Crown size={20} />
          <span className="font-semibold">Upgrade to Plus</span>
        </button>
        <p className="text-xs text-white/50 text-center">Get unlimited access</p>
      </div>
    </div>
  );
};

export default Sidebar; 