import React, { useState } from 'react';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';

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
              className="relative min-h-[400px] select-none"
            >
              {/* Top gap for adding phase */}
              <div
                className="absolute inset-x-0 h-2 -top-1"
                onMouseEnter={() => setHoveredGapIndex(-1)}
                onMouseLeave={() => setHoveredGapIndex(null)}
              >
                {hoveredGapIndex === -1 && (
                  <button
                    className="absolute right-0 top-1/2 -translate-y-1/2 bg-indigo-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-indigo-600 focus:outline-none select-none"
                    onClick={() => onAddPhase(0)}
                  >
                    +
                  </button>
                )}
              </div>

              {phases.map((phase, index) => (
                <Draggable 
                  key={phase.name} 
                  draggableId={phase.name} 
                  index={index}
                >
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      className={`relative mb-2 group ${
                        snapshot.isDragging ? 'opacity-50' : ''
                      }`}
                      onMouseEnter={() => setHoveredPhaseIndex(index)}
                      onMouseLeave={() => setHoveredPhaseIndex(null)}
                    >
                      <div
                        className="h-12 rounded flex items-center text-white font-medium transition-all duration-200"
                        style={{
                          backgroundColor: phase.color,
                          transform: hoveredPhaseIndex === index ? 'translateX(8px)' : 'translateX(0)',
                          ...provided.draggableProps.style,
                          position: snapshot.isDragging ? 'relative' : 'static',
                          left: snapshot.isDragging ? '0' : 'auto',
                          top: snapshot.isDragging ? '0' : 'auto',
                          width: snapshot.isDragging ? '100%' : 'auto',
                        }}
                      >
                        {/* Drag handle */}
                        <div
                          {...provided.dragHandleProps}
                          className="h-full px-3 flex items-center cursor-grab active:cursor-grabbing select-none"
                        >
                          <div className="flex flex-col gap-1">
                            <div className="w-4 h-0.5 bg-white/70"></div>
                            <div className="w-4 h-0.5 bg-white/70"></div>
                            <div className="w-4 h-0.5 bg-white/70"></div>
                          </div>
                        </div>
                        
                        {/* Phase name and duration */}
                        <div 
                          className="flex-1 text-center cursor-pointer select-none"
                          onClick={() => onEditPhase(index)}
                        >
                          {phase.name} ({phase.duration}m)
                        </div>
                      </div>
                      
                      {/* Delete button */}
                      <button
                        className={`absolute left-0 top-1/2 -translate-y-1/2 -translate-x-8 
                          bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center
                          transition-all duration-200 opacity-0 group-hover:opacity-100
                          hover:bg-red-600 focus:outline-none select-none`}
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
                            className="absolute right-0 top-1/2 -translate-y-1/2 bg-indigo-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-indigo-600 focus:outline-none select-none"
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
                    className="absolute right-0 top-1/2 -translate-y-1/2 bg-indigo-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-indigo-600 focus:outline-none select-none"
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