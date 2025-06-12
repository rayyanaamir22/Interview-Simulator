import React from 'react';

const TimelineProgress = ({ phases }) => {
  // Calculate total duration and percentages
  const totalDuration = phases.reduce((sum, phase) => sum + phase.duration, 0);
  
  return (
    <div className="w-full h-1 bg-gray-200 relative">
      {phases.map((phase, index) => {
        const width = (phase.duration / totalDuration) * 100;
        const left = phases
          .slice(0, index)
          .reduce((sum, p) => sum + (p.duration / totalDuration) * 100, 0);
        
        return (
          <div
            key={phase.name}
            className="absolute h-full transition-all duration-300"
            style={{
              left: `${left}%`,
              width: `${width}%`,
              backgroundColor: phase.color,
            }}
          />
        );
      })}
    </div>
  );
};

export default TimelineProgress; 