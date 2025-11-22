import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { 
  Send, 
  Mic, 
  Plus, 
  FileText, 
  X, 
  Upload,
  CheckCircle,
  Star,
  Loader2,
  Volume2,
  VolumeX
} from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import toast from 'react-hot-toast';
import { ChatAreaProps, ResumeData } from '../types';
import { API_ENDPOINTS } from '../config/api';

interface ChatMessage {
  id: string;
  type: 'user' | 'system' | 'file-list' | 'analysis-result' | 'resume-details' | 'ai-message' | 'smart-ai-message';
  content: string;
  files?: File[];
  jobDescription?: string;
  data?: any;
  timestamp: Date;
  intent?: any;
  suggested_actions?: string[];
}

const ChatArea: React.FC<ChatAreaProps> = ({ setCurrentView }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [isListening, setIsListening] = useState<boolean>(false);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [allPdfFiles, setAllPdfFiles] = useState<string[]>([]);
  const [selectedResume, setSelectedResume] = useState<ResumeData | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    fetchAllPdfFiles();
    initializeSpeechRecognition();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const initializeSpeechRecognition = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setIsListening(false);
        toast.success('Voice input captured!');
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        toast.error('Voice input failed. Please try again.');
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  };

  const startVoiceInput = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.start();
        setIsListening(true);
        toast.success('Listening... Speak now!');
      } catch (error) {
        console.error('Error starting speech recognition:', error);
        toast.error('Voice input not available');
      }
    } else {
      toast.error('Voice input not supported in this browser');
    }
  };

  const stopVoiceInput = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchAllPdfFiles = async (): Promise<void> => {
    try {
      const response = await axios.get(API_ENDPOINTS.RESUMES);
      setAllPdfFiles(response.data.resumes || []);
    } catch (error) {
      console.error('Error fetching PDF files:', error);
    }
  };

  const onDrop = (acceptedFiles: File[]): void => {
    const pdfFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
    if (pdfFiles.length !== acceptedFiles.length) {
      toast.error('Only PDF files are supported');
    }
    if (pdfFiles.length > 0) {
      setUploadedFiles(prev => [...prev, ...pdfFiles]);
      toast.success(`${pdfFiles.length} PDF file(s) added`);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: true
  });

  const addMessage = (message: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    const newMessage: ChatMessage = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date()
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const handleAIChat = async (userInput: string) => {
    try {
      const formData = new FormData();
      formData.append('message', userInput);
      formData.append('context', 'resume_analyzer');
      
      const response = await axios.post(API_ENDPOINTS.SMART_CHAT, formData);
      
      addMessage({
        type: 'smart-ai-message',
        content: response.data.response,
        intent: response.data.intent,
        suggested_actions: response.data.suggested_actions
      });
    } catch (error) {
      console.error('Error with AI chat:', error);
      addMessage({
        type: 'system',
        content: 'I can help you analyze resumes. Please upload PDF files and/or provide a job description.'
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();
    if (!input.trim() && uploadedFiles.length === 0) return;

    const userInput = input.trim();
    setInput('');

    // Add user message
    addMessage({
      type: 'user',
      content: userInput || `Uploaded ${uploadedFiles.length} PDF file(s)`,
      files: uploadedFiles.length > 0 ? [...uploadedFiles] : undefined
    });

    setIsLoading(true);

    try {
      // Check for "show me full details" command
      const showDetailsPattern = /show\s+(me\s+)?(full\s+)?details?\s+(of\s+)?(this\s+)?(pdf|resume|file)/i;
      if (showDetailsPattern.test(userInput)) {
        // Get the most recent resume data
        const recentResume = messages
          .filter(msg => msg.type === 'analysis-result' || msg.type === 'file-list')
          .pop();
        
        if (recentResume?.data?.resume_data) {
          // Show the resume details
          addMessage({
            type: 'resume-details',
            content: `Full details for ${recentResume.data.resume_data.filename}`,
            data: recentResume.data.resume_data
          });
        } else if (allPdfFiles.length > 0) {
          // Show details of the first available file
          await handleResumeSelect(allPdfFiles[0]);
        } else {
          addMessage({
            type: 'system',
            content: 'No resume data available. Please upload a PDF file first.'
          });
        }
      } else {
        // Check if it's a general question (no files, no job description keywords)
        const jobKeywords = ['job', 'position', 'role', 'developer', 'engineer', 'manager', 'analyst', 'designer', 'developer'];
        const isJobDescription = jobKeywords.some(keyword => userInput.toLowerCase().includes(keyword));
        
        // Case 1: Only PDFs uploaded (no job description)
        if (uploadedFiles.length > 0 && !userInput) {
          await handlePdfOnlyUpload();
        }
        // Case 2: Only job description (no PDFs)
        else if (userInput && uploadedFiles.length === 0 && isJobDescription) {
          await handleJobDescriptionOnly(userInput);
        }
        // Case 3: Both PDFs and job description
        else if (uploadedFiles.length > 0 && userInput && isJobDescription) {
          await handleFullAnalysis(userInput);
        }
        // Case 4: General question or AI chat
        else if (userInput) {
          await handleAIChat(userInput);
        }
      }

      // Clear uploaded files after processing
      setUploadedFiles([]);
    } catch (error) {
      console.error('Error processing input:', error);
      toast.error('Failed to process input. Please try again.');
      addMessage({
        type: 'system',
        content: 'Sorry, there was an error processing your request. Please try again.'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handlePdfOnlyUpload = async () => {
    // Upload files and show file list
    const uploadPromises = uploadedFiles.map(async (file) => {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post(API_ENDPOINTS.UPLOAD_RESUME, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    });

    await Promise.all(uploadPromises);
    await fetchAllPdfFiles(); // Refresh file list

    addMessage({
      type: 'file-list',
      content: `Successfully uploaded ${uploadedFiles.length} PDF file(s). Here are all available files:`,
      data: { files: allPdfFiles }
    });
  };

  const handleJobDescriptionOnly = async (jd: string) => {
    setJobDescription(jd);
    
    // Get all available PDFs and analyze them against the job description
    const analysisPromises = allPdfFiles.map(async (filename) => {
      try {
        const response = await axios.get(API_ENDPOINTS.RESUME(filename));
        const resumeData = response.data;
        
        // Simple analysis logic
        const jdWords = new Set(jd.toLowerCase().match(/\b[a-zA-Z]{3,}\b/g) || []);
        const resumeSkills = new Set(resumeData.skills?.map((s: string) => s.toLowerCase()) || []);
        
        const matchedSkills = Array.from(jdWords).filter(word => 
          Array.from(resumeSkills as Set<string>).some((skill: string) => skill.includes(word) || word.includes(skill))
        );
        
        const score = jdWords.size > 0 ? Math.round((matchedSkills.length / jdWords.size) * 100) : 0;
        
        return {
          filename,
          score,
          matched_skills: matchedSkills,
          resume_data: resumeData
        };
      } catch (error) {
        return {
          filename,
          score: 0,
          matched_skills: [],
          resume_data: { filename, name: 'Unknown' }
        };
      }
    });

    const results = await Promise.all(analysisPromises);
    const sortedResults = results.sort((a, b) => b.score - a.score);

    addMessage({
      type: 'file-list',
      content: `Analyzed ${allPdfFiles.length} files against your job description. Here are the best matches:`,
      data: { 
        files: allPdfFiles,
        results: sortedResults,
        jobDescription: jd,
        showScores: true
      }
    });
  };

  const handleFullAnalysis = async (jd: string) => {
    setJobDescription(jd);

    if (uploadedFiles.length === 1) {
      // Single file analysis
      const formData = new FormData();
      formData.append('jd', jd);
      formData.append('file', uploadedFiles[0]);
      
      const response = await axios.post(API_ENDPOINTS.PROCESS_INPUT, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      addMessage({
        type: 'analysis-result',
        content: `Analysis complete for ${uploadedFiles[0].name}`,
        data: response.data
      });
    } else {
      // Multiple file analysis
      const formData = new FormData();
      formData.append('jd', jd);
      uploadedFiles.forEach(file => {
        formData.append('files', file);
      });
      
      const response = await axios.post(API_ENDPOINTS.BATCH_ANALYZE, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      addMessage({
        type: 'analysis-result',
        content: `Batch analysis complete for ${uploadedFiles.length} files`,
        data: response.data
      });
    }
  };

  const handleResumeSelect = async (filename: string) => {
    try {
      const response = await axios.get(API_ENDPOINTS.RESUME_ANALYSIS(filename));
      setSelectedResume(response.data.resume_data);
      
      addMessage({
        type: 'resume-details',
        content: `Details for ${filename}`,
        data: response.data
      });
    } catch (error) {
      console.error('Error fetching resume:', error);
      toast.error('Failed to load resume details');
    }
  };

  const handleShowFileList = () => {
    addMessage({
      type: 'file-list',
      content: `Here are all available files:`,
      data: { files: allPdfFiles }
    });
  };

  const handleShowHelp = () => {
    addMessage({
      type: 'smart-ai-message',
      content: "I'm your AI assistant for resume analysis! Here's what I can help you with:",
      intent: { intent: "get_help", confidence: 0.9 },
      suggested_actions: [
        "📄 Upload resumes using the + button",
        "🔍 Analyze resumes against job descriptions", 
        "📁 View all uploaded files with the file icon",
        "🎯 Get detailed resume analysis with 'show me full details'",
        "🎤 Use voice input with the microphone button",
        "💬 Ask me anything about the application"
      ]
    });
  };

  const handleQuickAction = (action: string) => {
    switch (action) {
      case 'upload':
        addMessage({
          type: 'smart-ai-message',
          content: "Great! Let's upload your resume. You can:",
          intent: { intent: "upload_resume", confidence: 0.9 },
          suggested_actions: [
            "Click the + button to select PDF files",
            "Drag and drop PDF files into the chat area",
            "Upload multiple resumes at once for batch analysis"
          ]
        });
        break;
      case 'analyze':
        addMessage({
          type: 'smart-ai-message',
          content: "Let's analyze your resume! Here's how:",
          intent: { intent: "analyze_resume", confidence: 0.9 },
          suggested_actions: [
            "First, upload your resume using the + button",
            "Then type your job description in the chat box",
            "I'll analyze the match and show you detailed results"
          ]
        });
        break;
      case 'view_files':
        handleShowFileList();
        break;
      case 'help':
        handleShowHelp();
        break;
    }
  };

  const renderMessage = (message: ChatMessage) => {
    switch (message.type) {
      case 'user':
        return (
          <div className="flex justify-end mb-4">
            <div className="bg-primary-500 text-white rounded-2xl px-4 py-3 max-w-xs md:max-w-md lg:max-w-lg">
              <p className="text-sm">{message.content}</p>
              {message.files && message.files.length > 0 && (
                <div className="mt-2 space-y-1">
                  {message.files.map((file, index) => (
                    <div key={index} className="flex items-center gap-2 text-xs bg-white/10 rounded-lg px-2 py-1">
                      <FileText size={12} />
                      <span className="truncate">{file.name}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        );

      case 'system':
        return (
          <div className="flex justify-start mb-4">
            <div className="bg-white/10 text-white rounded-2xl px-4 py-3 max-w-xs md:max-w-md lg:max-w-lg">
              <p className="text-sm">{message.content}</p>
            </div>
          </div>
        );

      case 'ai-message':
        return (
          <div className="flex justify-start mb-4">
            <div className="bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-white rounded-2xl px-4 py-3 max-w-xs md:max-w-md lg:max-w-lg border border-purple-500/30">
              <div className="flex items-center gap-2 mb-2">
                <Star size={14} className="text-purple-400" />
                <span className="text-xs font-semibold text-purple-300">AI Assistant</span>
              </div>
              <p className="text-sm">{message.content}</p>
            </div>
          </div>
        );

      case 'file-list':
        return (
          <div className="flex justify-start mb-4">
            <div className="bg-white/10 text-white rounded-2xl px-4 py-3 max-w-xs md:max-w-md lg:max-w-lg">
              <p className="text-sm mb-3">{message.content}</p>
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {message.data?.files?.map((filename: string, index: number) => {
                  const result = message.data?.results?.find((r: any) => r.filename === filename);
                  return (
                    <motion.button
                      key={index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      onClick={() => handleResumeSelect(filename)}
                      className="w-full flex items-center justify-between p-3 bg-white/5 rounded-xl hover:bg-white/10 transition-all duration-300 text-left"
                    >
                      <div className="flex items-center gap-3 flex-1 min-w-0">
                        <FileText size={16} className="text-primary-400 flex-shrink-0" />
                        <span className="text-sm truncate">{filename}</span>
                      </div>
                      {result && message.data?.showScores && (
                        <div className={`px-2 py-1 rounded-full text-xs font-semibold ${
                          result.score >= 80 ? 'bg-green-500/20 text-green-300' :
                          result.score >= 60 ? 'bg-yellow-500/20 text-yellow-300' :
                          'bg-red-500/20 text-red-300'
                        }`}>
                          {result.score}%
                        </div>
                      )}
                    </motion.button>
                  );
                })}
                {(!message.data?.files || message.data.files.length === 0) && (
                  <div className="text-center py-4">
                    <FileText size={24} className="text-white/30 mx-auto mb-2" />
                    <p className="text-xs text-white/50">No PDF files available</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        );

      case 'analysis-result':
        return (
          <div className="flex justify-start mb-4">
            <div className="bg-white/10 text-white rounded-2xl px-4 py-3 max-w-xs md:max-w-md lg:max-w-lg">
              <p className="text-sm mb-3">{message.content}</p>
              {message.data && (
                <div className="space-y-3">
                  {message.data.score && (
                    <div className="text-center">
                      <div className="text-2xl font-bold text-primary-400">{message.data.score}%</div>
                      <div className="text-xs text-white/60">Match Score</div>
                    </div>
                  )}
                  {message.data.matched && message.data.matched.length > 0 && (
                    <div>
                      <div className="text-xs font-semibold text-green-400 mb-2">Matched Skills:</div>
                      <div className="flex flex-wrap gap-1">
                        {message.data.matched.slice(0, 5).map((skill: string, index: number) => (
                          <span key={index} className="px-2 py-1 bg-green-500/20 border border-green-500/30 rounded-full text-xs text-green-300">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {message.data.missing && message.data.missing.length > 0 && (
                    <div>
                      <div className="text-xs font-semibold text-orange-400 mb-2">Missing Skills:</div>
                      <div className="flex flex-wrap gap-1">
                        {message.data.missing.slice(0, 5).map((skill: string, index: number) => (
                          <span key={index} className="px-2 py-1 bg-orange-500/20 border border-orange-500/30 rounded-full text-xs text-orange-300">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {message.data.resume_data && (
                    <button
                      onClick={() => handleResumeSelect(message.data.resume_data.filename)}
                      className="w-full btn-secondary text-xs py-2"
                    >
                      View Full Details
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>
        );

      case 'resume-details':
        return (
          <div className="flex justify-start mb-4">
            <div className="bg-white/10 text-white rounded-2xl px-4 py-3 max-w-xs md:max-w-md lg:max-w-lg">
              <p className="text-sm mb-3">{message.content}</p>
              {message.data && (
                <div className="space-y-4">
                  {/* Analysis Results */}
                  {message.data.match_score !== null && message.data.match_score !== undefined && (
                    <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-lg p-3 border border-green-500/20">
                      <div className="text-xs font-semibold text-green-300 mb-2">📊 Analysis Results</div>
                      <div className="flex items-center gap-2 mb-2">
                        <div className="text-lg font-bold text-green-400">{message.data.match_score}%</div>
                        <div className="text-xs text-white/70">Match Score</div>
                      </div>
                      
                      {/* Matched Skills */}
                      {message.data.matched_skills && message.data.matched_skills.length > 0 && (
                        <div className="mb-2">
                          <div className="text-xs font-semibold text-green-300 mb-1">✅ Matched Skills</div>
                          <div className="flex flex-wrap gap-1">
                            {message.data.matched_skills.map((skill: string, index: number) => (
                              <span
                                key={index}
                                className="px-2 py-1 bg-green-500/20 border border-green-500/30 rounded-full text-xs text-green-300"
                              >
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {/* Missing Skills */}
                      {message.data.missing_skills && message.data.missing_skills.length > 0 && (
                        <div className="mb-2">
                          <div className="text-xs font-semibold text-red-300 mb-1">❌ Missing Skills</div>
                          <div className="flex flex-wrap gap-1">
                            {message.data.missing_skills.map((skill: string, index: number) => (
                              <span
                                key={index}
                                className="px-2 py-1 bg-red-500/20 border border-red-500/30 rounded-full text-xs text-red-300"
                              >
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {/* Extra Skills */}
                      {message.data.extra_skills && message.data.extra_skills.length > 0 && (
                        <div>
                          <div className="text-xs font-semibold text-blue-300 mb-1">💡 Extra Skills</div>
                          <div className="flex flex-wrap gap-1">
                            {message.data.extra_skills.slice(0, 5).map((skill: string, index: number) => (
                              <span
                                key={index}
                                className="px-2 py-1 bg-blue-500/20 border border-blue-500/30 rounded-full text-xs text-blue-300"
                              >
                                {skill}
                              </span>
                            ))}
                            {message.data.extra_skills.length > 5 && (
                              <span className="px-2 py-1 bg-blue-500/20 border border-blue-500/30 rounded-full text-xs text-blue-300">
                                +{message.data.extra_skills.length - 5} more
                              </span>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Basic Info */}
                  <div className="space-y-2">
                    {message.data.resume_data?.name && (
                      <div>
                        <div className="text-xs font-semibold text-white/60">Name</div>
                        <div className="text-sm">{message.data.resume_data.name}</div>
                      </div>
                    )}
                    {message.data.resume_data?.email && (
                      <div>
                        <div className="text-xs font-semibold text-white/60">Email</div>
                        <div className="text-sm">{message.data.resume_data.email}</div>
                      </div>
                    )}
                    {message.data.resume_data?.phone && (
                      <div>
                        <div className="text-xs font-semibold text-white/60">Phone</div>
                        <div className="text-sm">{message.data.resume_data.phone}</div>
                      </div>
                    )}
                  </div>

                  {/* Skills */}
                  {message.data.resume_data?.skills && message.data.resume_data.skills.length > 0 && (
                    <div>
                      <div className="text-xs font-semibold text-white/60 mb-2">Skills</div>
                      <div className="flex flex-wrap gap-1">
                        {message.data.resume_data.skills.slice(0, 6).map((skill: string, index: number) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-primary-500/20 border border-primary-500/30 rounded-full text-xs text-primary-300"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Education */}
                  {message.data.resume_data?.education && message.data.resume_data.education.length > 0 && (
                    <div>
                      <div className="text-xs font-semibold text-white/60 mb-2">Education</div>
                      <div className="space-y-2">
                        {message.data.resume_data.education.slice(0, 2).map((edu: any, index: number) => (
                          <div key={index} className="bg-white/5 rounded-lg p-2">
                            {edu.degree && <div className="text-xs font-medium">{edu.degree}</div>}
                            {edu.institution && <div className="text-xs text-white/70">{edu.institution}</div>}
                            {(edu.year || edu.gpa) && (
                              <div className="text-xs text-white/50">
                                {edu.year && <span>{edu.year}</span>}
                                {edu.year && edu.gpa && <span> • </span>}
                                {edu.gpa && <span>GPA: {edu.gpa}</span>}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                      {message.data.resume_data?.education_summary && (
                        <div className="mt-2 p-2 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-lg border border-blue-500/20">
                          <div className="text-xs font-semibold text-blue-300 mb-1">AI Analysis</div>
                          <div className="text-xs text-white/80">{message.data.resume_data.education_summary}</div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Experience */}
                  {message.data.resume_data?.experience && message.data.resume_data.experience.length > 0 && (
                    <div>
                      <div className="text-xs font-semibold text-white/60 mb-2">Experience</div>
                      <div className="space-y-2">
                        {message.data.resume_data.experience.slice(0, 2).map((exp: any, index: number) => (
                          <div key={index} className="bg-white/5 rounded-lg p-2">
                            {exp.title && <div className="text-xs font-medium">{exp.title}</div>}
                            {exp.company && <div className="text-xs text-white/70">{exp.company}</div>}
                            {exp.duration && <div className="text-xs text-white/50">{exp.duration}</div>}
                            {exp.responsibilities && exp.responsibilities.length > 0 && (
                              <div className="mt-1">
                                <div className="text-xs text-white/60">Key responsibilities:</div>
                                <ul className="text-xs text-white/70 mt-1 space-y-1">
                                  {exp.responsibilities.slice(0, 2).map((resp: string, respIndex: number) => (
                                    <li key={respIndex} className="flex items-start gap-1">
                                      <span className="text-primary-400 mt-1">•</span>
                                      <span>{resp}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                      {message.data.resume_data?.experience_summary && (
                        <div className="mt-2 p-2 bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-lg border border-green-500/20">
                          <div className="text-xs font-semibold text-green-300 mb-1">AI Analysis</div>
                          <div className="text-xs text-white/80">{message.data.resume_data.experience_summary}</div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Projects */}
                  {message.data.resume_data?.projects && message.data.resume_data.projects.length > 0 && (
                    <div>
                      <div className="text-xs font-semibold text-white/60 mb-2">Projects</div>
                      <div className="space-y-2">
                        {message.data.resume_data.projects.slice(0, 2).map((proj: any, index: number) => (
                          <div key={index} className="bg-white/5 rounded-lg p-2">
                            {proj.name && <div className="text-xs font-medium">{proj.name}</div>}
                            {proj.technologies && proj.technologies.length > 0 && (
                              <div className="flex flex-wrap gap-1 mt-1">
                                {proj.technologies.slice(0, 3).map((tech: string, techIndex: number) => (
                                  <span
                                    key={techIndex}
                                    className="px-1 py-0.5 bg-orange-500/20 border border-orange-500/30 rounded text-xs text-orange-300"
                                  >
                                    {tech}
                                  </span>
                                ))}
                              </div>
                            )}
                            {proj.description && proj.description.length > 0 && (
                              <div className="mt-1">
                                <div className="text-xs text-white/60">Description:</div>
                                <div className="text-xs text-white/70 mt-1">
                                  {proj.description[0]?.substring(0, 100)}
                                  {proj.description[0]?.length > 100 && '...'}
                                </div>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                      {message.data.resume_data?.projects_summary && (
                        <div className="mt-2 p-2 bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-lg border border-purple-500/20">
                          <div className="text-xs font-semibold text-purple-300 mb-1">AI Analysis</div>
                          <div className="text-xs text-white/80">{message.data.resume_data.projects_summary}</div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        );

      case 'smart-ai-message':
        return (
          <div className="flex justify-start mb-4">
            <div className="bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-white rounded-2xl px-4 py-3 max-w-xs md:max-w-md lg:max-w-lg border border-purple-500/30">
              <div className="flex items-center gap-2 mb-2">
                <Star size={14} className="text-purple-400" />
                <span className="text-xs font-semibold text-purple-300">AI Assistant</span>
                {message.intent && (
                  <span className="text-xs text-purple-200 bg-purple-500/20 px-2 py-1 rounded-full">
                    {message.intent.intent}
                  </span>
                )}
              </div>
              <p className="text-sm">{message.content}</p>
              {message.suggested_actions && message.suggested_actions.length > 0 && (
                <div className="mt-3 pt-2 border-t border-purple-500/20">
                  <div className="text-xs font-semibold text-purple-300 mb-2">💡 Suggested Actions:</div>
                  <div className="space-y-1">
                    {message.suggested_actions.map((action, index) => (
                      <div key={index} className="text-xs text-white/80 flex items-start gap-2">
                        <span className="text-purple-400 mt-0.5">•</span>
                        <span>{action}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-16 h-16 md:w-20 md:h-20 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-6">
              <FileText size={32} className="text-white" />
            </div>
            <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold gradient-text mb-4">
              Welcome to Resume Analyzer
            </h1>
            <p className="text-base md:text-lg text-white/70 mb-8 leading-relaxed max-w-2xl">
              Upload PDF resumes and describe the job you're applying for. 
              Our AI will analyze your skills and provide personalized insights.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
              <button
                onClick={() => handleQuickAction('upload')}
                className="glass-card p-4 md:p-6 text-center hover:bg-white/10 transition-all duration-300"
              >
                <Upload size={24} className="text-primary-400 mx-auto mb-3" />
                <h3 className="font-semibold text-white mb-2">Upload Resume</h3>
                <p className="text-sm text-white/60">Drag & drop your PDF resume</p>
              </button>
              <button
                onClick={() => handleQuickAction('analyze')}
                className="glass-card p-4 md:p-6 text-center hover:bg-white/10 transition-all duration-300"
              >
                <Star size={24} className="text-primary-400 mx-auto mb-3" />
                <h3 className="font-semibold text-white mb-2">AI Analysis</h3>
                <p className="text-sm text-white/60">Get detailed skill analysis</p>
              </button>
              <button
                onClick={() => handleQuickAction('view_files')}
                className="glass-card p-4 md:p-6 text-center hover:bg-white/10 transition-all duration-300"
              >
                <FileText size={24} className="text-primary-400 mx-auto mb-3" />
                <h3 className="font-semibold text-white mb-2">View Files</h3>
                <p className="text-sm text-white/60">See all uploaded resumes</p>
              </button>
              <button
                onClick={() => handleQuickAction('help')}
                className="glass-card p-4 md:p-6 text-center hover:bg-white/10 transition-all duration-300"
              >
                <CheckCircle size={24} className="text-primary-400 mx-auto mb-3" />
                <h3 className="font-semibold text-white mb-2">Get Help</h3>
                <p className="text-sm text-white/60">Learn how to use the app</p>
              </button>
            </div>
            
            <div className="text-center">
              <p className="text-sm text-white/50 mb-4">Or simply start typing in the chat box below!</p>
              <div className="flex flex-wrap justify-center gap-2">
                <button
                  onClick={() => setInput("How do I upload a resume?")}
                  className="px-3 py-1 bg-white/10 rounded-full text-xs text-white/70 hover:bg-white/20 transition-all"
                >
                  How do I upload a resume?
                </button>
                <button
                  onClick={() => setInput("Show me all files")}
                  className="px-3 py-1 bg-white/10 rounded-full text-xs text-white/70 hover:bg-white/20 transition-all"
                >
                  Show me all files
                </button>
                <button
                  onClick={() => setInput("Help me analyze my resume")}
                  className="px-3 py-1 bg-white/10 rounded-full text-xs text-white/70 hover:bg-white/20 transition-all"
                >
                  Help me analyze my resume
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                {renderMessage(message)}
              </motion.div>
            ))}
            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="bg-white/10 text-white rounded-2xl px-4 py-3">
                  <div className="flex items-center gap-3">
                    <Loader2 size={16} className="animate-spin" />
                    <span className="text-sm">Analyzing...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Chatbox Input - Always visible */}
      <div className="flex-shrink-0 p-4 md:p-6">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-3 md:p-4">
            <div className="flex items-end gap-2 md:gap-3">
              {/* Left Side */}
              <div className="flex gap-2">
                <button
                  type="button"
                  {...getRootProps()}
                  className="p-2 md:p-3 rounded-xl bg-white/10 border border-white/20 text-white/70 hover:text-white hover:bg-white/15 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-primary-500/50"
                  aria-label="Upload file"
                >
                  <input {...getInputProps()} />
                  <Plus size={18} />
                </button>
                <button
                  type="button"
                  onClick={() => handleShowFileList()}
                  className="p-2 md:p-3 rounded-xl bg-white/10 border border-white/20 text-white/70 hover:text-white hover:bg-white/15 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-primary-500/50"
                  aria-label="Show file list"
                >
                  <FileText size={18} />
                </button>
              </div>

              {/* Center Input */}
              <div className="flex-1">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Upload your resume and describe the job you're applying for..."
                  className="w-full bg-transparent border-none outline-none resize-none text-sm md:text-base text-white placeholder-white/50"
                  rows={1}
                  disabled={isLoading}
                />
                {uploadedFiles.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {uploadedFiles.map((file, index) => (
                      <div key={index} className="flex items-center gap-1 px-2 py-1 bg-primary-500/20 rounded-lg text-xs">
                        <FileText size={12} className="text-primary-300" />
                        <span className="text-primary-300 truncate max-w-20">{file.name}</span>
                        <button
                          type="button"
                          onClick={() => setUploadedFiles(prev => prev.filter((_, i) => i !== index))}
                          className="text-primary-300 hover:text-white"
                        >
                          <X size={12} />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Right Side */}
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={isListening ? stopVoiceInput : startVoiceInput}
                  className={`p-2 md:p-3 rounded-xl border transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-primary-500/50 ${
                    isListening
                      ? 'bg-red-500/20 border-red-500/30 text-red-400'
                      : 'bg-white/10 border-white/20 text-white/70 hover:text-white hover:bg-white/15'
                  }`}
                  aria-label="Toggle voice input"
                >
                  {isListening ? <VolumeX size={18} /> : <Mic size={18} />}
                </button>
                <button
                  type="submit"
                  disabled={(!input.trim() && uploadedFiles.length === 0) || isLoading}
                  className="p-2 md:p-3 rounded-xl bg-gradient-primary text-white disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-primary-500/25 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-primary-500/50"
                  aria-label="Send message"
                >
                  {isLoading ? (
                    <Loader2 size={18} className="animate-spin" />
                  ) : (
                    <Send size={18} />
                  )}
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatArea; 