// API Response Types
export interface ResumeData {
  filename: string;
  name?: string;
  email?: string;
  phone?: string;
  skills?: string[];
  education?: EducationItem[];
  experience?: ExperienceItem[];
  projects?: ProjectItem[];
  education_summary?: string;
  experience_summary?: string;
  projects_summary?: string;
  extracted_text?: string;
}

export interface EducationItem {
  degree?: string;
  institution?: string;
  year?: string;
  gpa?: string;
}

export interface ExperienceItem {
  title?: string;
  company?: string;
  duration?: string;
  responsibilities?: string[];
}

export interface ProjectItem {
  name?: string;
  technologies?: string[];
  description?: string[];
}

export interface AnalysisResult {
  score?: number;
  matched_skills?: string[];
  missing_skills?: string[];
  recommendations?: string[];
  resume_data?: ResumeData;
  [key: string]: any;
}

export interface BatchAnalysisResult {
  job_description: string;
  results: Array<{
    filename: string;
    score: number;
    matched_skills: string[];
    missing_skills: string[];
    resume_data: ResumeData;
  }>;
  total_resumes: number;
  average_score: number;
}

export interface JobDescription {
  title?: string;
  company?: string;
  description?: string;
  requirements?: string[];
  [key: string]: any;
}

// Component Props Types
export interface HeaderProps {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
}

export interface SidebarProps {
  currentView: string;
  setCurrentView: (view: string) => void;
  setData: (data: any) => void;
  onClose: () => void;
}

export interface ChatAreaProps {
  currentView: string;
  data: AnalysisResult | BatchAnalysisResult | null;
  setData: (data: any) => void;
  setCurrentView: (view: string) => void;
}

export interface FileUploadProps {
  onFilesUploaded: (files: File[]) => void;
  onAnalysisComplete: (result: AnalysisResult | BatchAnalysisResult) => void;
  setCurrentView: (view: string) => void;
}

export interface ResumeListProps {
  resumes: ResumeData[];
  onResumeSelect: (resume: ResumeData) => void;
}

export interface AnalysisViewProps {
  data: AnalysisResult | BatchAnalysisResult;
  onBack: () => void;
}

export interface BatchAnalysisViewProps {
  results: BatchAnalysisResult;
  onResumeSelect: (resume: ResumeData) => void;
  onBack: () => void;
}

// State Types
export interface AppState {
  sidebarOpen: boolean;
  currentView: string;
  data: AnalysisResult | BatchAnalysisResult | null;
  isMobile: boolean;
  uploadedFiles: File[];
  jobDescription: string;
}

// View Types
export type ViewType = 
  | 'home' 
  | 'upload' 
  | 'single-analysis' 
  | 'batch-analysis' 
  | 'resume-details' 
  | 'file-list' 
  | 'result'; 

export interface SmartAIResponse {
  response: string;
  intent: {
    intent: string;
    confidence: number;
    entities: any;
    response_type: string;
  };
  suggested_actions: string[];
  type: string;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'system' | 'file-list' | 'analysis-result' | 'resume-details' | 'ai-message' | 'smart-ai-message';
  content: string;
  files?: File[];
  jobDescription?: string;
  data?: any;
  intent?: any;
  suggested_actions?: string[];
  timestamp: Date;
} 