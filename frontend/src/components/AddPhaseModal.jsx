import React, { useState } from 'react';

const PHASE_TYPES = [
  'Introduction',
  'Behavioral',
  'Technical',
  'Coding',
  'Closing',
  'Custom'
];

const AddPhaseModal = ({ isOpen, onClose, onAdd, position }) => {
  const [phaseType, setPhaseType] = useState('Introduction');
  const [customName, setCustomName] = useState('');
  const [duration, setDuration] = useState(15);
  const [isSkippable, setIsSkippable] = useState(false);
  const [isShortenable, setIsShortenable] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd({
      name: phaseType === 'Custom' ? customName : phaseType,
      duration,
      isSkippable,
      isShortenable
    });
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">Add New Phase</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Phase Type
            </label>
            <select
              value={phaseType}
              onChange={(e) => setPhaseType(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              {PHASE_TYPES.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          {phaseType === 'Custom' && (
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Custom Phase Name
              </label>
              <input
                type="text"
                value={customName}
                onChange={(e) => setCustomName(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter phase name"
                required
              />
            </div>
          )}

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Duration (minutes)
            </label>
            <input
              type="number"
              value={duration}
              onChange={(e) => setDuration(parseInt(e.target.value))}
              min="1"
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              required
            />
          </div>

          <div className="mb-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={isSkippable}
                onChange={(e) => setIsSkippable(e.target.checked)}
                className="mr-2"
              />
              Skippable
            </label>
          </div>

          <div className="mb-6">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={isShortenable}
                onChange={(e) => setIsShortenable(e.target.checked)}
                className="mr-2"
              />
              Shortenable
            </label>
          </div>

          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-600 hover:text-gray-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              Add Phase
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddPhaseModal; 