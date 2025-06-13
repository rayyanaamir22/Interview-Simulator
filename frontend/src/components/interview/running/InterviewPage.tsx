import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Dropdown, Space, Progress } from 'antd';
import { MoreOutlined, PauseOutlined, PlayCircleOutlined, CloseOutlined } from '@ant-design/icons';
import axios from 'axios';

interface Phase {
  phase: string;
  duration_minutes: number;
  description: string;
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

const InterviewPage: React.FC = () => {
  const navigate = useNavigate();
  const [isPaused, setIsPaused] = useState(false);
  const [timer, setTimer] = useState(0);
  const [phases, setPhases] = useState<Phase[]>([]);
  const [currentPhase, setCurrentPhase] = useState<string>('');
  const [progress, setProgress] = useState<number>(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const interviewIdRef = useRef<string>('');

  useEffect(() => {
    // Get interview ID from localStorage
    const interviewId = localStorage.getItem('currentInterviewId');
    if (!interviewId) {
      navigate('/');
      return;
    }
    interviewIdRef.current = interviewId;

    // Start polling for interview status
    const pollInterval = setInterval(async () => {
      try {
        const response = await axios.get(`http://localhost:8001/api/interview/${interviewId}/status`);
        const status: InterviewStatus = response.data;
        
        setCurrentPhase(status.current_phase);
        setProgress(status.progress.progress_percentage);
        
        if (status.progress.is_completed) {
          clearInterval(pollInterval);
          // Handle interview completion
        }
      } catch (error) {
        console.error('Failed to get interview status:', error);
      }
    }, 1000);

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
    
    timerRef.current = setInterval(() => {
      if (!isPaused) {
        setTimer(prev => prev + 1);
      }
    }, 1000);
  };

  const handlePause = async () => {
    try {
      await axios.post(`http://localhost:8001/api/interview/${interviewIdRef.current}/pause`);
      setIsPaused(true);
    } catch (error) {
      console.error('Failed to pause interview:', error);
    }
  };

  const handleResume = async () => {
    try {
      await axios.post(`http://localhost:8001/api/interview/${interviewIdRef.current}/resume`);
      setIsPaused(false);
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
    <div className="flex flex-col h-screen">
      {/* Top Navigation Bar */}
      <div className="bg-white shadow-md p-4">
        <div className="flex justify-between items-center">
          {/* Progress Timeline */}
          <div className="flex-1">
            <Progress
              percent={progress}
              showInfo={false}
              strokeColor={{
                '0%': '#108ee9',
                '100%': '#87d068',
              }}
            />
            <div className="text-sm text-gray-600 mt-1">
              Current Phase: {currentPhase}
            </div>
          </div>
          
          {/* Timer */}
          <div className="text-2xl font-bold mx-4">
            {formatTime(timer)}
          </div>
          
          {/* Options Dropdown */}
          <Dropdown
            menu={{ items }}
            placement="bottomRight"
            trigger={['click']}
          >
            <Button icon={<MoreOutlined />} />
          </Dropdown>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 bg-gray-100 p-4">
        {/* Webcam feed will go here */}
        <div className="w-full h-full bg-gray-200 rounded-lg flex items-center justify-center">
          <span className="text-gray-500">Webcam Feed Coming Soon</span>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="bg-white shadow-md p-4">
        {/* This will be populated with dynamic content later */}
      </div>
    </div>
  );
};

export default InterviewPage; 