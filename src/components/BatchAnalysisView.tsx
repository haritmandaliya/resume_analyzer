import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, FileText, Star, TrendingUp, User, Mail, Phone, Award, Eye } from 'lucide-react';
import { BatchAnalysisViewProps, ResumeData } from '../types';

const BatchAnalysisView: React.FC<BatchAnalysisViewProps> = ({ results, onResumeSelect, onBack }) => {
  const [selectedResume, setSelectedResume] = useState<ResumeData | null>(null);
  const [sortBy, setSortBy] = useState<'score' | 'name'>('score');

  const sortedResults = [...results.results].sort((a, b) => {
    if (sortBy === 'score') {
      return b.score - a.score;
    } else {
      return a.resume_data.name?.localeCompare(b.resume_data.name || '') || 0;
    }
  });

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-500/20 border-green-500/30';
    if (score >= 60) return 'bg-yellow-500/20 border-yellow-500/30';
    return 'bg-red-500/20 border-red-500/30';
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 md:p-6 border-b border-white/10">
        <div className="flex items-center gap-4">
          <button
            onClick={onBack}
            className="btn-secondary flex items-center gap-2"
          >
            <ArrowLeft size={16} />
            Back
          </button>
          <div>
            <h1 className="text-xl md:text-2xl font-bold gradient-text">Batch Analysis Results</h1>
            <p className="text-white/60">Analyzed {results.total_resumes} resumes</p>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-white">{results.average_score.toFixed(1)}%</div>
            <div className="text-sm text-white/60">Average Score</div>
          </div>
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'score' | 'name')}
            className="bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-primary-500/50"
          >
            <option value="score">Sort by Score</option>
            <option value="name">Sort by Name</option>
          </select>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        {selectedResume ? (
          /* Resume Details View */
          <div className="h-full overflow-y-auto p-4 md:p-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="max-w-4xl mx-auto"
            >
              {/* Resume Header */}
              <div className="glass-card p-6 md:p-8 mb-6">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center">
                      <FileText size={24} className="text-white" />
                    </div>
                    <div>
                      <h2 className="text-xl md:text-2xl font-bold text-white">{selectedResume.name || 'Unknown'}</h2>
                      <p className="text-white/60">{selectedResume.filename}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => setSelectedResume(null)}
                    className="btn-secondary"
                  >
                    Back to List
                  </button>
                </div>

                {/* Contact Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  {selectedResume.email && (
                    <div className="flex items-center gap-3 p-3 bg-white/5 rounded-xl">
                      <Mail size={20} className="text-primary-400" />
                      <div>
                        <p className="text-sm text-white/60">Email</p>
                        <p className="text-white">{selectedResume.email}</p>
                      </div>
                    </div>
                  )}
                  {selectedResume.phone && (
                    <div className="flex items-center gap-3 p-3 bg-white/5 rounded-xl">
                      <Phone size={20} className="text-primary-400" />
                      <div>
                        <p className="text-sm text-white/60">Phone</p>
                        <p className="text-white">{selectedResume.phone}</p>
                      </div>
                    </div>
                  )}
                </div>

                {/* Skills */}
                {selectedResume.skills && selectedResume.skills.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                      <Award size={20} className="text-primary-400" />
                      Skills
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedResume.skills.map((skill, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-primary-500/20 border border-primary-500/30 rounded-full text-sm text-primary-300"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Extracted Text */}
                {selectedResume.extracted_text && (
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-4">Extracted Text</h3>
                    <div className="bg-white/5 rounded-xl p-4 max-h-96 overflow-y-auto">
                      <p className="text-white/80 text-sm leading-relaxed whitespace-pre-wrap">
                        {selectedResume.extracted_text}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          </div>
        ) : (
          /* Results List View */
          <div className="h-full overflow-y-auto p-4 md:p-6">
            <div className="max-w-6xl mx-auto">
              {/* Job Description */}
              <div className="glass-card p-6 mb-6">
                <h3 className="text-lg font-semibold text-white mb-3">Job Description</h3>
                <p className="text-white/80 leading-relaxed">{results.job_description}</p>
              </div>

              {/* Results Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {sortedResults.map((result, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="glass-card p-6 cursor-pointer hover:shadow-lg hover:shadow-primary-500/10 transition-all duration-300"
                    onClick={() => setSelectedResume(result.resume_data)}
                  >
                    {/* Header */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-primary rounded-xl flex items-center justify-center">
                          <FileText size={20} className="text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="font-semibold text-white truncate">
                            {result.resume_data.name || 'Unknown'}
                          </h4>
                          <p className="text-xs text-white/60 truncate">{result.filename}</p>
                        </div>
                      </div>
                      <div className={`px-3 py-1 rounded-full text-sm font-semibold border ${getScoreBg(result.score)} ${getScoreColor(result.score)}`}>
                        {result.score}%
                      </div>
                    </div>

                    {/* Score Bar */}
                    <div className="mb-4">
                      <div className="flex items-center justify-between text-sm mb-2">
                        <span className="text-white/60">Match Score</span>
                        <span className={getScoreColor(result.score)}>{result.score}%</span>
                      </div>
                      <div className="w-full bg-white/10 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all duration-300 ${
                            result.score >= 80 ? 'bg-green-500' : result.score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${result.score}%` }}
                        />
                      </div>
                    </div>

                    {/* Skills Summary */}
                    <div className="mb-4">
                      <div className="flex items-center justify-between text-sm mb-2">
                        <span className="text-white/60">Matched Skills</span>
                        <span className="text-green-400">{result.matched_skills.length}</span>
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {result.matched_skills.slice(0, 3).map((skill, skillIndex) => (
                          <span
                            key={skillIndex}
                            className="px-2 py-1 bg-green-500/20 border border-green-500/30 rounded-full text-xs text-green-300"
                          >
                            {skill}
                          </span>
                        ))}
                        {result.matched_skills.length > 3 && (
                          <span className="px-2 py-1 bg-white/10 rounded-full text-xs text-white/60">
                            +{result.matched_skills.length - 3} more
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Missing Skills */}
                    {result.missing_skills.length > 0 && (
                      <div className="mb-4">
                        <div className="flex items-center justify-between text-sm mb-2">
                          <span className="text-white/60">Missing Skills</span>
                          <span className="text-orange-400">{result.missing_skills.length}</span>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {result.missing_skills.slice(0, 2).map((skill, skillIndex) => (
                            <span
                              key={skillIndex}
                              className="px-2 py-1 bg-orange-500/20 border border-orange-500/30 rounded-full text-xs text-orange-300"
                            >
                              {skill}
                            </span>
                          ))}
                          {result.missing_skills.length > 2 && (
                            <span className="px-2 py-1 bg-white/10 rounded-full text-xs text-white/60">
                              +{result.missing_skills.length - 2} more
                            </span>
                          )}
                        </div>
                      </div>
                    )}

                    {/* View Details Button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedResume(result.resume_data);
                      }}
                      className="w-full btn-secondary flex items-center justify-center gap-2 text-sm"
                    >
                      <Eye size={16} />
                      View Details
                    </button>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BatchAnalysisView; 