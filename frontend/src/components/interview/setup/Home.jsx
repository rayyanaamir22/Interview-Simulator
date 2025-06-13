import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../context/AuthContext';
import TimelineVisualization from './TimelineVisualization';
import TimelineProgress from './TimelineProgress';
import AddPhaseModal from './AddPhaseModal';

const getPhaseColor = (phaseName) => {
  const colors = {
    'Introduction': '#4CAF50',
    'Behavioral': '#2196F3',
    'Technical': '#FF9800',
    'Coding': '#9C27B0',
    'Closing': '#F44336'
  };
  
  return colors[phaseName] || '#607D8B';
};

const Home = () => {
  const { logout } = useAuth();
  const [phases, setPhases] = useState([
    { name: 'Introduction', duration: 5, isSkippable: false, isShortenable: true, color: getPhaseColor('Introduction') },
    { name: 'Behavioral', duration: 15, isSkippable: false, isShortenable: true, color: getPhaseColor('Behavioral') },
    { name: 'Technical', duration: 20, isSkippable: false, isShortenable: true, color: getPhaseColor('Technical') },
    { name: 'Coding', duration: 30, isSkippable: false, isShortenable: true, color: getPhaseColor('Coding') },
    { name: 'Closing', duration: 5, isSkippable: false, isShortenable: true, color: getPhaseColor('Closing') }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showAddPhaseModal, setShowAddPhaseModal] = useState(false);
  const [newPhaseIndex, setNewPhaseIndex] = useState(null);
  const [editingPhaseIndex, setEditingPhaseIndex] = useState(null);
  const navigate = useNavigate();

  const handlePhasesChange = (newPhases) => {
    setPhases(newPhases);
  };

  const handleAddPhase = (index) => {
    setNewPhaseIndex(index);
    setEditingPhaseIndex(null);
    setShowAddPhaseModal(true);
  };

  const handleEditPhase = (index) => {
    setEditingPhaseIndex(index);
    setNewPhaseIndex(null);
    setShowAddPhaseModal(true);
  };

  const handleNewPhase = (newPhase) => {
    const phaseWithColor = {
      ...newPhase,
      color: newPhase.color || getPhaseColor(newPhase.name)
    };
    
    if (editingPhaseIndex !== null) {
      // Editing existing phase
      const newPhases = [...phases];
      newPhases[editingPhaseIndex] = phaseWithColor;
      setPhases(newPhases);
    } else {
      // Adding new phase
      const newPhases = [...phases];
      newPhases.splice(newPhaseIndex, 0, phaseWithColor);
      setPhases(newPhases);
    }
  };

  const handleDeletePhase = (index) => {
    const newPhases = [...phases];
    newPhases.splice(index, 1);
    setPhases(newPhases);
  };

  const handleStartInterview = async () => {
    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      console.log('Starting interview with phases:', phases);
      const requestBody = {
        phases: phases.map(phase => ({
          phase: phase.name,
          duration_minutes: phase.duration,
          is_skippable: phase.isSkippable,
          is_shortenable: phase.isShortenable
        }))
      };
      console.log('Request body:', JSON.stringify(requestBody, null, 2));

      // Try both URLs to debug the issue
      const urls = [
        'http://localhost:8001/api/interview/start',
        '/api/interview/start'
      ];

      let response;
      let lastError;

      for (const url of urls) {
        try {
          console.log('Trying URL:', url);
          response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
          });
          console.log('Response status:', response.status);
          console.log('Response headers:', Object.fromEntries(response.headers.entries()));
          break;
        } catch (error) {
          console.error(`Failed with URL ${url}:`, error);
          lastError = error;
        }
      }

      if (!response) {
        throw lastError || new Error('All URL attempts failed');
      }

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response text:', errorText);
        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch (e) {
          errorData = { detail: errorText };
        }
        throw new Error(errorData.detail || 'Failed to start interview');
      }

      const responseText = await response.text();
      console.log('Response text:', responseText);
      let data;
      try {
        data = JSON.parse(responseText);
      } catch (e) {
        console.error('Failed to parse response as JSON:', e);
        throw new Error('Invalid response from server');
      }

      // Store interview ID in localStorage for the interview page to use
      localStorage.setItem('currentInterviewId', data.interview_id);
      // Store the complete phase configuration including colors
      localStorage.setItem('interviewConfig', JSON.stringify({
        phases: phases.map(phase => ({
          phase: phase.name,
          duration_minutes: phase.duration,
          is_skippable: phase.isSkippable,
          is_shortenable: phase.isShortenable,
          color: phase.color
        }))
      }));
      // Navigate to interview page
      navigate('/interview');
    } catch (error) {
      setError(error.message);
      console.error('Error starting interview:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="w-full px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Interview Simulator</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={logout}
                className="ml-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <TimelineProgress phases={phases} />

      <main className="w-full py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Configure Your Interview
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Customize the interview phases and their durations
            </p>
          </div>

          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {success && (
            <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
              <p className="font-medium">{success.message}</p>
              <p className="text-sm mt-1">Interview ID: {success.interviewId}</p>
              <p className="text-sm mt-1">Total Duration: {success.schedule.total_duration_minutes} minutes</p>
            </div>
          )}

          <div className="max-w-4xl mx-auto">
            <TimelineVisualization 
              phases={phases}
              onPhasesChange={handlePhasesChange}
              onAddPhase={handleAddPhase}
              onDeletePhase={handleDeletePhase}
              onEditPhase={handleEditPhase}
            />

            <div className="mt-8 text-center">
              <button
                onClick={handleStartInterview}
                disabled={isLoading}
                className={`px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
                  isLoading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {isLoading ? 'Configuring...' : 'Start Interview'}
              </button>
            </div>
          </div>
        </div>
      </main>

      <AddPhaseModal
        isOpen={showAddPhaseModal}
        onClose={() => {
          setShowAddPhaseModal(false);
          setEditingPhaseIndex(null);
        }}
        onAdd={handleNewPhase}
        position={newPhaseIndex}
        initialPhase={editingPhaseIndex !== null ? phases[editingPhaseIndex] : null}
      />
    </div>
  );
};

export default Home; 