import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Dropdown, Space, Progress } from 'antd';
import { MoreOutlined, PauseOutlined, PlayCircleOutlined, CloseOutlined } from '@ant-design/icons';
import axios from 'axios';
import TimelineVisualization from '../setup/TimelineVisualization';
import TimelineProgress from '../setup/TimelineProgress';

interface Phase {
  name: string;
  duration: number;
  color: string;
}

interface InterviewStatus {
  current_phase: string;
  progress: {
    phase: string;
    elapsed_minutes: number;
    total_minutes: number;
    progress_percentage: number;
    is_completed: boolean;
    is_skipped: boolean;
  };
}

const getPhaseColor = (phaseName: string) => {
  const colors: { [key: string]: string } = {
    'Introduction': '#4CAF50',
    'Behavioral': '#2196F3',
    'Technical': '#FF9800',
    'Coding': '#9C27B0',
    'Closing': '#F44336'
  };
  
  return colors[phaseName] || '#607D8B';
};

const InterviewPage: React.FC = () => {
  const navigate = useNavigate();
  const [isPaused, setIsPaused] = useState(false);
  const [timer, setTimer] = useState(0);
  const [phases, setPhases] = useState<Phase[]>([]);
  const [currentPhase, setCurrentPhase] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const timerRef = useRef<number | null>(null);
  const interviewIdRef = useRef<string>('');
  const lastPhaseRef = useRef<string | null>(null);

  useEffect(() => {
    // Get interview ID from localStorage
    const interviewId = localStorage.getItem('currentInterviewId');
    if (!interviewId) {
      navigate('/');
      return;
    }
    interviewIdRef.current = interviewId;

    // Get the interview configuration from localStorage
    const config = JSON.parse(localStorage.getItem('interviewConfig') || '{}');
    if (config.phases) {
      setPhases(config.phases.map((phase: any) => ({
        name: phase.phase,
        duration: phase.duration_minutes,
        color: phase.color || getPhaseColor(phase.phase)
      })));
    }

    // Start polling for interview status
    const pollInterval = setInterval(async () => {
      try {
        const response = await axios.get(`http://localhost:8001/api/interview/${interviewId}/status`);
        const status: InterviewStatus = response.data;
        
        // Update current phase and progress
        if (status.current_phase !== lastPhaseRef.current) {
          console.log('Phase transition:', {
            from: lastPhaseRef.current || 'initial',
            to: status.current_phase
          });
          lastPhaseRef.current = status.current_phase;
          setCurrentPhase(status.current_phase);
        }
        setProgress(status.progress.progress_percentage);
        
        // Log status updates for debugging
        console.log('Interview status:', {
          currentPhase: status.current_phase,
          progress: status.progress.progress_percentage,
          isCompleted: status.progress.is_completed,
          elapsedMinutes: status.progress.elapsed_minutes,
          totalMinutes: status.progress.total_minutes
        });
        
        if (status.progress.is_completed) {
          clearInterval(pollInterval);
          // Handle interview completion
          console.log('Interview completed');
        }
      } catch (error) {
        console.error('Failed to get interview status:', error);
      }
    }, 1000); // Poll every second

    // Start the timer
    startTimer();

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      clearInterval(pollInterval);
    };
  }, [navigate]);

  const startTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    
    timerRef.current = window.setInterval(() => {
      if (!isPaused) {
        setTimer(prev => prev + 1);
      }
    }, 1000);
  };

  const handlePause = async () => {
    try {
      await axios.post(`http://localhost:8001/api/interview/${interviewIdRef.current}/pause`);
      setIsPaused(true);
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    } catch (error) {
      console.error('Failed to pause interview:', error);
    }
  };

  const handleResume = async () => {
    try {
      await axios.post(`http://localhost:8001/api/interview/${interviewIdRef.current}/resume`);
      setIsPaused(false);
      // Clear any existing interval first
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      // Start a new interval
      timerRef.current = window.setInterval(() => {
        setTimer(prev => prev + 1);
      }, 1000);
    } catch (error) {
      console.error('Failed to resume interview:', error);
    }
  };

  const handleExit = () => {
    if (window.confirm('Are you sure you want to exit the interview?')) {
      localStorage.removeItem('currentInterviewId');
      navigate('/');
    }
  };

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const items = [
    {
      key: 'pause',
      icon: isPaused ? <PlayCircleOutlined /> : <PauseOutlined />,
      label: isPaused ? 'Resume' : 'Pause',
      onClick: isPaused ? handleResume : handlePause,
    },
    {
      key: 'exit',
      icon: <CloseOutlined />,
      label: 'Exit Interview',
      onClick: handleExit,
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation Bar */}
      <nav className="bg-white shadow-sm">
        <div className="w-full px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Interview Simulator</h1>
            </div>
            <div className="flex items-center">
              <Dropdown
                menu={{ items }}
                placement="bottomRight"
                trigger={['click']}
              >
                <Button icon={<MoreOutlined />} />
              </Dropdown>
            </div>
          </div>
        </div>
      </nav>

      {/* Timeline Progress */}
      <div className="w-full bg-white shadow-sm">
        <TimelineProgress phases={phases} />
      </div>

      {/* Main Content Area */}
      <main className="w-full py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Current Phase and Timer */}
          <div className="flex justify-between items-center mb-8">
            <div className="text-lg font-medium text-gray-700">
              Current Phase: {currentPhase || 'Initial'}
            </div>
            <div className="text-3xl font-bold text-gray-900">
              {formatTime(timer)}
            </div>
          </div>

          {/* Webcam feed */}
          <div className="w-full h-[calc(100vh-400px)] bg-gray-200 rounded-lg flex items-center justify-center">
            <span className="text-gray-500">Webcam Feed Coming Soon</span>
          </div>
        </div>
      </main>

      {/* Bottom Bar */}
      <div className="bg-white shadow-md p-4">
        {/* This will be populated with dynamic content later */}
      </div>
    </div>
  );
};

export default InterviewPage; 