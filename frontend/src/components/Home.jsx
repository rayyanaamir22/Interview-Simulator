import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import AddPhaseModal from './AddPhaseModal';

const TimelineVisualization = ({ phases, onPhasesChange, onAddPhase, onDeletePhase, onEditPhase }) => {
  const [hoveredPhaseIndex, setHoveredPhaseIndex] = useState(null);
  const [hoveredGapIndex, setHoveredGapIndex] = useState(null);
  
  const handleDragEnd = (result) => {
    if (!result.destination) return;
    
    const items = Array.from(phases);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);
    
    onPhasesChange(items);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
      <h3 className="text-xl font-semibold mb-4">Interview Timeline</h3>
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable direction="vertical">
          {(provided) => (
            <div
              {...provided.droppableProps}
              ref={provided.innerRef}
              className="relative min-h-[400px] w-64"
            >
              {/* Top gap for adding phase */}
              <div
                className="absolute w-64 h-2 -left-4"
                style={{ top: '0' }}
                onMouseEnter={() => setHoveredGapIndex(-1)}
                onMouseLeave={() => setHoveredGapIndex(null)}
              >
                {hoveredGapIndex === -1 && (
                  <button
                    className="absolute right-0 top-1/2 -translate-y-1/2 bg-indigo-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-indigo-600 focus:outline-none"
                    onClick={() => onAddPhase(0)}
                  >
                    +
                  </button>
                )}
              </div>

              {phases.map((phase, index) => (
                <Draggable key={phase.name} draggableId={phase.name} index={index}>
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      className={`relative mb-2 group ${
                        snapshot.isDragging ? 'opacity-50' : ''
                      }`}
                      onMouseEnter={() => setHoveredPhaseIndex(index)}
                      onMouseLeave={() => setHoveredPhaseIndex(null)}
                    >
                      <div
                        className="h-12 rounded flex items-center justify-center text-white font-medium transition-all duration-200 cursor-pointer"
                        style={{
                          backgroundColor: getPhaseColor(phase.name),
                          transform: hoveredPhaseIndex === index ? 'translateX(8px)' : 'translateX(0)',
                        }}
                        onClick={() => onEditPhase(index)}
                      >
                        {phase.name} ({phase.duration}m)
                      </div>
                      
                      {/* Delete button */}
                      <button
                        className={`absolute left-0 top-1/2 -translate-y-1/2 -translate-x-8 
                          bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center
                          transition-all duration-200 opacity-0 group-hover:opacity-100
                          hover:bg-red-600 focus:outline-none`}
                        onClick={() => onDeletePhase(index)}
                        style={{
                          opacity: hoveredPhaseIndex === index ? 1 : 0,
                        }}
                      >
                        ×
                      </button>
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
              
              {/* Gap hover areas between phases */}
              {phases.map((_, index) => (
                <div
                  key={`gap-${index}`}
                  className="absolute w-64 h-2 -left-4"
                  style={{
                    top: `${(index + 1) * 56}px`,
                  }}
                  onMouseEnter={() => setHoveredGapIndex(index)}
                  onMouseLeave={() => setHoveredGapIndex(null)}
                >
                  {hoveredGapIndex === index && (
                    <button
                      className="absolute right-0 top-1/2 -translate-y-1/2 bg-indigo-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-indigo-600 focus:outline-none"
                      onClick={() => onAddPhase(index + 1)}
                    >
                      +
                    </button>
                  )}
                </div>
              ))}

              {/* Bottom gap for adding phase */}
              <div
                className="absolute w-64 h-2 -left-4"
                style={{ top: `${(phases.length + 1) * 56}px` }}
                onMouseEnter={() => setHoveredGapIndex(phases.length)}
                onMouseLeave={() => setHoveredGapIndex(null)}
              >
                {hoveredGapIndex === phases.length && (
                  <button
                    className="absolute right-0 top-1/2 -translate-y-1/2 bg-indigo-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-indigo-600 focus:outline-none"
                    onClick={() => onAddPhase(phases.length)}
                  >
                    +
                  </button>
                )}
              </div>
            </div>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  );
};

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
    { name: 'Introduction', duration: 5, isSkippable: false, isShortenable: true },
    { name: 'Behavioral', duration: 15, isSkippable: false, isShortenable: true },
    { name: 'Technical', duration: 20, isSkippable: false, isShortenable: true },
    { name: 'Coding', duration: 30, isSkippable: false, isShortenable: true },
    { name: 'Closing', duration: 5, isSkippable: false, isShortenable: true }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showAddPhaseModal, setShowAddPhaseModal] = useState(false);
  const [newPhaseIndex, setNewPhaseIndex] = useState(null);
  const [editingPhaseIndex, setEditingPhaseIndex] = useState(null);

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
    if (editingPhaseIndex !== null) {
      // Editing existing phase
      const newPhases = [...phases];
      newPhases[editingPhaseIndex] = newPhase;
      setPhases(newPhases);
    } else {
      // Adding new phase
      const newPhases = [...phases];
      newPhases.splice(newPhaseIndex, 0, newPhase);
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
      const response = await fetch('/api/interview/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phases: phases.map(phase => ({
            phase: phase.name.toLowerCase(),
            duration_minutes: phase.duration,
            is_skippable: phase.isSkippable,
            is_shortenable: phase.isShortenable
          }))
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to start interview');
      }

      const data = await response.json();
      setSuccess({
        message: 'Interview configured successfully!',
        interviewId: data.interview_id,
        schedule: data.schedule
      });
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