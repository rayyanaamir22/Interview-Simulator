import React, { useState, useEffect } from 'react';

const PHASE_TYPES = [
  'Introduction',
  'Behavioral',
  'Technical',
  'Coding',
  'Closing',
  'Custom'
];

// Helper function to convert HSL to Hex
const hslToHex = (h, s, l) => {
  s /= 100;
  l /= 100;
  const a = s * Math.min(l, 1 - l);
  const f = n => {
    const k = (n + h / 30) % 12;
    const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
    return Math.round(255 * color).toString(16).padStart(2, '0');
  };
  return `#${f(0)}${f(8)}${f(4)}`;
};

// Helper function to generate random pastel color in hex
const generateRandomPastelHex = () => {
  const hue = Math.floor(Math.random() * 360);
  const saturation = 70 + Math.floor(Math.random() * 30);
  const lightness = 60 + Math.floor(Math.random() * 20);
  return hslToHex(hue, saturation, lightness);
};

const AddPhaseModal = ({ isOpen, onClose, onAdd, position, initialPhase }) => {
  const [phaseType, setPhaseType] = useState('Introduction');
  const [customName, setCustomName] = useState('');
  const [duration, setDuration] = useState(15);
  const [isSkippable, setIsSkippable] = useState(false);
  const [isShortenable, setIsShortenable] = useState(true);
  const [customColor, setCustomColor] = useState('#607D8B');

  useEffect(() => {
    if (initialPhase) {
      // If editing an existing phase, set the initial values
      const isCustom = !PHASE_TYPES.includes(initialPhase.name);
      setPhaseType(isCustom ? 'Custom' : initialPhase.name);
      setCustomName(isCustom ? initialPhase.name : '');
      setDuration(initialPhase.duration);
      setIsSkippable(initialPhase.isSkippable);
      setIsShortenable(initialPhase.isShortenable);
      setCustomColor(initialPhase.color || '#607D8B');
    } else {
      // Reset to defaults when adding a new phase
      setPhaseType('Introduction');
      setCustomName('');
      setDuration(15);
      setIsSkippable(false);
      setIsShortenable(true);
      setCustomColor(generateRandomPastelHex());
    }
  }, [initialPhase, isOpen]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd({
      name: phaseType === 'Custom' ? customName : phaseType,
      duration,
      isSkippable,
      isShortenable,
      color: phaseType === 'Custom' ? customColor : undefined
    });
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">
          {initialPhase ? 'Edit Phase' : 'Add New Phase'}
        </h2>
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
            <>
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
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Phase Color
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="color"
                    value={customColor}
                    onChange={(e) => setCustomColor(e.target.value)}
                    className="h-10 w-20 rounded cursor-pointer"
                  />
                  <input
                    type="text"
                    value={customColor}
                    onChange={(e) => setCustomColor(e.target.value)}
                    className="flex-1 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    placeholder="#RRGGBB"
                  />
                </div>
              </div>
            </>
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
            <label className="flex items-center text-gray-900">
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
            <label className="flex items-center text-gray-900">
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
              {initialPhase ? 'Save Changes' : 'Add Phase'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddPhaseModal; 