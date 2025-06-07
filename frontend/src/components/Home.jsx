import React from 'react';
import { useAuth } from '../context/AuthContext';

const FeatureCard = ({ title, description, icon }) => (
  <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
    <div className="text-4xl mb-4">{icon}</div>
    <h3 className="text-xl font-semibold mb-2">{title}</h3>
    <p className="text-gray-600">{description}</p>
  </div>
);

const Home = () => {
  const { logout } = useAuth();

  const features = [
    {
      title: 'AI Interview Practice',
      description: 'Practice interviews with our AI interviewer that provides real-time feedback and guidance.',
      icon: '🤖'
    },
    {
      title: 'Speech Analysis',
      description: 'Get instant feedback on your speech patterns and communication style during interviews.',
      icon: '🎤'
    },
    {
      title: 'Facial Expression Analysis',
      description: 'Receive feedback on your facial expressions and body language during the interview.',
      icon: '📹'
    },
    {
      title: 'Coding Interview Practice',
      description: 'Specialized coding interview practice with our fine-tuned AI coding agent.',
      icon: '💻'
    },
    {
      title: 'Time Management',
      description: 'Practice with customizable time schedules and get feedback on your time management.',
      icon: '⏱️'
    },
    {
      title: 'Progress Tracking',
      description: 'Track your interview progress with customizable checklists and feedback.',
      icon: '📊'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
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

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Welcome to Interview Simulator
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Practice your interview skills with our AI-powered platform
            </p>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} />
            ))}
          </div>

          <div className="mt-12 text-center">
            <p className="text-gray-600">
              Select a feature above to start your interview practice session
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home; 