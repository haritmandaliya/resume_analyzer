import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, X, Loader2, AlertCircle } from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import toast from 'react-hot-toast';
import { FileUploadProps, AnalysisResult, BatchAnalysisResult } from '../types';
import { API_ENDPOINTS } from '../config/api';

const FileUpload: React.FC<FileUploadProps> = ({ onFilesUploaded, onAnalysisComplete, setCurrentView }) => {
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

  const onDrop = (acceptedFiles: File[]) => {
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

  const removeFile = (index: number) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const uploadFiles = async () => {
    if (uploadedFiles.length === 0) {
      toast.error('Please select at least one PDF file');
      return;
    }

    setIsUploading(true);
    try {
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
      onFilesUploaded(uploadedFiles);
      toast.success('All files uploaded successfully!');
    } catch (error) {
      console.error('Error uploading files:', error);
      toast.error('Failed to upload files. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const analyzeResumes = async () => {
    if (!jobDescription.trim()) {
      toast.error('Please enter a job description');
      return;
    }

    if (uploadedFiles.length === 0) {
      toast.error('Please upload at least one resume');
      return;
    }

    setIsAnalyzing(true);
    try {
      if (uploadedFiles.length === 1) {
        // Single file analysis
        const formData = new FormData();
        formData.append('jd', jobDescription);
        formData.append('file', uploadedFiles[0]);
        
        const response = await axios.post(API_ENDPOINTS.PROCESS_INPUT, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        
        onAnalysisComplete(response.data);
        setCurrentView('single-analysis');
      } else {
        // Batch analysis
        const formData = new FormData();
        formData.append('jd', jobDescription);
        uploadedFiles.forEach(file => {
          formData.append('files', file);
        });
        
        const response = await axios.post(API_ENDPOINTS.BATCH_ANALYZE, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        
        onAnalysisComplete(response.data);
        setCurrentView('batch-analysis');
      }
      
      toast.success('Analysis completed successfully!');
    } catch (error) {
      console.error('Error analyzing resumes:', error);
      toast.error('Failed to analyze resumes. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="h-full flex flex-col items-center justify-center p-4 md:p-6 text-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl w-full"
      >
        <div className="w-16 h-16 md:w-20 md:h-20 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-6">
          <Upload size={32} className="text-white" />
        </div>
        
        <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold gradient-text mb-4">
          Upload Resumes
        </h1>
        
        <p className="text-base md:text-lg text-white/70 mb-8 leading-relaxed">
          Upload one or multiple PDF resumes and provide a job description. 
          Our AI will analyze and rank them based on match criteria.
        </p>

        {/* File Upload Area */}
        <div className="mb-8">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-2xl p-8 md:p-12 transition-all duration-300 cursor-pointer ${
              isDragActive
                ? 'border-primary-500 bg-primary-500/10'
                : 'border-white/20 hover:border-white/40 hover:bg-white/5'
            }`}
          >
            <input {...getInputProps()} />
            <div className="flex flex-col items-center gap-4">
              <Upload size={48} className="text-white/60" />
              <div>
                <p className="text-lg font-semibold text-white mb-2">
                  {isDragActive ? 'Drop PDF files here' : 'Drag & drop PDF files here'}
                </p>
                <p className="text-white/60">or click to select files</p>
              </div>
              <p className="text-sm text-white/50">
                Supports multiple PDF files (up to 1000)
              </p>
            </div>
          </div>
        </div>

        {/* Uploaded Files List */}
        {uploadedFiles.length > 0 && (
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-white mb-4">
              Uploaded Files ({uploadedFiles.length})
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-60 overflow-y-auto">
              {uploadedFiles.map((file, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="flex items-center gap-3 p-3 bg-white/5 rounded-xl border border-white/10"
                >
                  <FileText size={20} className="text-primary-400" />
                  <span className="flex-1 text-sm text-white truncate">{file.name}</span>
                  <button
                    onClick={() => removeFile(index)}
                    className="p-1 hover:bg-white/10 rounded-lg transition-colors"
                  >
                    <X size={16} className="text-white/60" />
                  </button>
                </motion.div>
              ))}
            </div>
          </div>
        )}

        {/* Job Description Input */}
        <div className="mb-8">
          <label className="block text-left text-lg font-semibold text-white mb-4">
            Job Description
          </label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Enter the job description, requirements, and skills needed for the position..."
            className="w-full h-32 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/50 focus:outline-none focus:border-primary-500/50 focus:bg-white/10 transition-all duration-300 resize-none"
          />
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={uploadFiles}
            disabled={uploadedFiles.length === 0 || isUploading}
            className="btn-secondary flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isUploading ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Uploading...
              </>
            ) : (
              <>
                <Upload size={18} />
                Upload Files
              </>
            )}
          </button>
          
          <button
            onClick={analyzeResumes}
            disabled={uploadedFiles.length === 0 || !jobDescription.trim() || isAnalyzing}
            className="btn-primary flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <FileText size={18} />
                {uploadedFiles.length === 1 ? 'Analyze Resume' : 'Analyze All Resumes'}
              </>
            )}
          </button>
        </div>

        {/* Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-12">
          <div className="glass-card p-4 md:p-6 text-center">
            <Upload size={24} className="text-primary-400 mx-auto mb-3" />
            <h3 className="font-semibold text-white mb-2">Multiple Uploads</h3>
            <p className="text-sm text-white/60">Upload up to 1000 PDF resumes at once</p>
          </div>
          <div className="glass-card p-4 md:p-6 text-center">
            <FileText size={24} className="text-primary-400 mx-auto mb-3" />
            <h3 className="font-semibold text-white mb-2">Smart Analysis</h3>
            <p className="text-sm text-white/60">AI-powered skill matching and ranking</p>
          </div>
          <div className="glass-card p-4 md:p-6 text-center">
            <AlertCircle size={24} className="text-primary-400 mx-auto mb-3" />
            <h3 className="font-semibold text-white mb-2">Detailed Results</h3>
            <p className="text-sm text-white/60">Get match scores and skill analysis</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default FileUpload; 