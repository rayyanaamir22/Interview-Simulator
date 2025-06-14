import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Dropdown } from 'antd';
import { MoreOutlined, PauseOutlined, PlayCircleOutlined, CloseOutlined, VideoCameraOutlined, AudioOutlined, FileTextOutlined } from '@ant-design/icons';
import axios from 'axios';
import TimelineProgress from '../setup/TimelineProgress';
import ClosedCaptions from './ClosedCaptions';

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

const InterviewPage: React.FC = () => {
  const navigate = useNavigate();
  
  // Interview state
  const [isPaused, setIsPaused] = useState(false);
  const [timer, setTimer] = useState(0);
  const [phases, setPhases] = useState<Phase[]>([]);
  const [currentPhase, setCurrentPhase] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const interviewIdRef = useRef<string>('');
  const timerRef = useRef<number | null>(null);
  const lastPhaseRef = useRef<string | null>(null);

  // Media state
  const [isVideoEnabled, setIsVideoEnabled] = useState(false);
  const [isAudioEnabled, setIsAudioEnabled] = useState(false);
  const [isCaptionsEnabled, setIsCaptionsEnabled] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const recognitionRef = useRef<any>(null);

  // Initialize interview
  useEffect(() => {
    document.title = 'Interview Simulator | Session';
    
    const interviewId = localStorage.getItem('currentInterviewId');
    if (!interviewId) {
      navigate('/');
      return;
    }
    interviewIdRef.current = interviewId;

    const config = JSON.parse(localStorage.getItem('interviewConfig') || '{}');
    if (config.phases) {
      setPhases(config.phases.map((phase: any) => ({
        name: phase.phase,
        duration: phase.duration_minutes,
        color: phase.color || '#607D8B'
      })));
    }

    startTimer();
    startStatusPolling();

    return () => {
      cleanup();
    };
  }, [navigate]);

  // Cleanup function
  const cleanup = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    stopAllTracks();
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  // Timer functions
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

  // Status polling
  const startStatusPolling = () => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await axios.get(`http://localhost:8001/api/interview/${interviewIdRef.current}/status`);
        const status: InterviewStatus = response.data;
        
        if (status.current_phase !== lastPhaseRef.current) {
          lastPhaseRef.current = status.current_phase;
          setCurrentPhase(status.current_phase);
        }
        setProgress(status.progress.progress_percentage);
        
        if (status.progress.is_completed) {
          clearInterval(pollInterval);
          navigate('/interview/completion');
        }
      } catch (error) {
        console.error('Failed to get interview status:', error);
      }
    }, 1000);

    return () => clearInterval(pollInterval);
  };

  // Media control functions
  const stopAllTracks = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => {
        track.stop();
        track.enabled = false;
      });
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  const initializeMediaStream = async (constraints: MediaStreamConstraints) => {
    try {
      // Stop any existing tracks before getting new ones
      stopAllTracks();
      
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      streamRef.current = stream;
      return stream;
    } catch (error) {
      console.error('Error accessing media devices:', error);
      return null;
    }
  };

  const toggleVideo = async () => {
    try {
      if (!isVideoEnabled) {
        const constraints = {
          video: true,
          audio: isAudioEnabled
        };
        const stream = await initializeMediaStream(constraints);
        if (stream) {
          setIsVideoEnabled(true);
        }
      } else {
        if (streamRef.current) {
          const videoTrack = streamRef.current.getVideoTracks()[0];
          if (videoTrack) {
            videoTrack.stop();
            videoTrack.enabled = false;
          }
          
          if (isAudioEnabled) {
            const audioStream = await initializeMediaStream({ audio: true });
            if (!audioStream) {
              setIsAudioEnabled(false);
              stopAllTracks();
            }
          } else {
            stopAllTracks();
          }
        }
        setIsVideoEnabled(false);
      }
    } catch (error) {
      console.error('Error toggling video:', error);
      stopAllTracks();
      setIsVideoEnabled(false);
    }
  };

  const toggleAudio = async () => {
    try {
      if (!isAudioEnabled) {
        const constraints = {
          video: isVideoEnabled,
          audio: true
        };
        const stream = await initializeMediaStream(constraints);
        if (stream) {
          setIsAudioEnabled(true);
        }
      } else {
        if (streamRef.current) {
          const audioTrack = streamRef.current.getAudioTracks()[0];
          if (audioTrack) {
            audioTrack.stop();
            audioTrack.enabled = false;
          }
          
          if (isVideoEnabled) {
            const videoStream = await initializeMediaStream({ video: true });
            if (!videoStream) {
              setIsVideoEnabled(false);
              stopAllTracks();
            }
          } else {
            stopAllTracks();
          }
        }
        setIsAudioEnabled(false);
      }
    } catch (error) {
      console.error('Error toggling audio:', error);
      stopAllTracks();
      setIsAudioEnabled(false);
    }
  };

  // Interview control functions
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
      startTimer();
    } catch (error) {
      console.error('Failed to resume interview:', error);
    }
  };

  const handleExit = () => {
    if (window.confirm('Are you sure you want to exit the interview?')) {
      cleanup();
      localStorage.removeItem('currentInterviewId');
      navigate('/');
    }
  };

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const dropdownItems = [
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
      <nav className="bg-white shadow-sm w-full">
        <div className="w-full px-4">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Interview Simulator</h1>
            </div>
            <div className="flex items-center">
              <Dropdown
                menu={{ items: dropdownItems }}
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
      <main className="w-full mb-20">
        <div className="w-full">
          {/* Current Phase and Timer */}
          <div className="flex justify-between items-center p-4">
            <div className="text-lg font-medium text-gray-700">
              Current Phase: {currentPhase || 'Initial'}
            </div>
            <div className="text-3xl font-bold text-gray-900">
              {formatTime(timer)}
            </div>
          </div>

          {/* Webcam feed */}
          <div className="w-full min-h-[500px] h-[calc(100vh-200px)] bg-gray-200 overflow-hidden relative">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover scale-x-[-1]"
            />
            {!isVideoEnabled && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
                <span className="text-white text-lg">Camera is off</span>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Bottom Bar */}
      <div className="fixed bottom-0 left-0 right-0 bg-white shadow-md p-4 h-20">
        <div className="flex justify-center space-x-6 h-full items-center">
          <Button
            type="text"
            icon={<VideoCameraOutlined style={{ fontSize: '24px', color: isVideoEnabled ? '#1890ff' : '#8c8c8c' }} />}
            onClick={toggleVideo}
            className="flex items-center justify-center w-14 h-14 rounded-full hover:bg-gray-100 border border-gray-200"
          />
          <Button
            type="text"
            icon={<AudioOutlined style={{ fontSize: '24px', color: isAudioEnabled ? '#1890ff' : '#8c8c8c' }} />}
            onClick={toggleAudio}
            className="flex items-center justify-center w-14 h-14 rounded-full hover:bg-gray-100 border border-gray-200"
          />
          <Button
            type="text"
            icon={<FileTextOutlined style={{ fontSize: '24px', color: isCaptionsEnabled ? '#1890ff' : '#8c8c8c' }} />}
            onClick={() => setIsCaptionsEnabled(!isCaptionsEnabled)}
            className="flex items-center justify-center w-14 h-14 rounded-full hover:bg-gray-100 border border-gray-200"
          />
        </div>
      </div>

      {/* Closed Captions */}
      <ClosedCaptions 
        isEnabled={isCaptionsEnabled && isAudioEnabled} 
        audioStream={streamRef.current}
      />
    </div>
  );
};

export default InterviewPage; 