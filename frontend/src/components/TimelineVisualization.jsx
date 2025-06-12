import React, { useState } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

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
      <h3 className="text-xl font-semibold mb-4 text-gray-900">Interview Timeline</h3>
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="timeline" direction="vertical">
          {(provided) => (
            <div
              {...provided.droppableProps}
              ref={provided.innerRef}
              className="relative min-h-[400px]"
            >
              {/* Top gap for adding phase */}
              <div
                className="absolute inset-x-0 h-2 -top-1"
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
                          backgroundColor: phase.color,
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

                      {/* Gap hover area below current phase */}
                      <div
                        className="absolute inset-x-0 h-4 -bottom-2"
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
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
              
              {/* Bottom gap for adding phase */}
              <div
                className="absolute inset-x-0 h-2"
                style={{ top: `${(phases.length * 56) + 48}px` }}
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

export default TimelineVisualization;