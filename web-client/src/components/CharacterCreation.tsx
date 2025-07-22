import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Protagonist } from '../types';
import './CharacterCreation.css';

interface CharacterCreationProps {
  onCharacterCreated: (protagonist: Protagonist) => void;
}

const CharacterCreation: React.FC<CharacterCreationProps> = ({ onCharacterCreated }) => {
  const [formData, setFormData] = useState({
    name: '',
    gender: '',
    age: 25,
    startingSituation: ''
  });

  const [currentStep, setCurrentStep] = useState(0);

  const genderOptions = ['Male', 'Female', 'Non-binary', 'Other'];
  
  const situationOptions = [
    'You are a traveling merchant seeking new opportunities',
    'You are a scholar searching for ancient knowledge',
    'You are a warrior looking for purpose after war',
    'You are an artist seeking inspiration',
    'You are a refugee fleeing from conflict',
    'You are an explorer drawn to the unknown'
  ];

  const steps = [
    { field: 'name', label: 'What is your name?', type: 'text' },
    { field: 'gender', label: 'What is your gender?', type: 'select', options: genderOptions },
    { field: 'age', label: 'How old are you?', type: 'range', min: 16, max: 80 },
    { field: 'startingSituation', label: 'What is your situation?', type: 'select', options: situationOptions }
  ];

  const handleInputChange = (field: string, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(prev => prev + 1);
    } else {
      // Create character
      onCharacterCreated({
        name: formData.name,
        gender: formData.gender,
        age: formData.age,
        startingSituation: formData.startingSituation
      });
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const isStepValid = () => {
    const step = steps[currentStep];
    const value = formData[step.field as keyof typeof formData];
    return value !== '' && value !== undefined;
  };

  const currentStepData = steps[currentStep];

  return (
    <div className="character-creation">
      <motion.div 
        className="creation-card"
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="creation-header">
          <h1>Create Your Character</h1>
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
            />
          </div>
          <span className="step-indicator">
            Step {currentStep + 1} of {steps.length}
          </span>
        </div>

        <motion.div 
          className="step-content"
          key={currentStep}
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          <h2>{currentStepData.label}</h2>
          
          {currentStepData.type === 'text' && (
            <input
              type="text"
              value={formData[currentStepData.field as keyof typeof formData] as string}
              onChange={(e) => handleInputChange(currentStepData.field, e.target.value)}
              placeholder="Enter your name..."
              className="text-input"
              autoFocus
            />
          )}

          {currentStepData.type === 'select' && (
            <div className="option-grid">
              {currentStepData.options?.map((option, index) => (
                <button
                  key={index}
                  className={`option-button ${
                    formData[currentStepData.field as keyof typeof formData] === option ? 'selected' : ''
                  }`}
                  onClick={() => handleInputChange(currentStepData.field, option)}
                >
                  {option}
                </button>
              ))}
            </div>
          )}

          {currentStepData.type === 'range' && (
            <div className="range-input-container">
              <input
                type="range"
                min={currentStepData.min}
                max={currentStepData.max}
                value={formData.age}
                onChange={(e) => handleInputChange(currentStepData.field, parseInt(e.target.value))}
                className="range-input"
              />
              <div className="range-value">{formData.age} years old</div>
            </div>
          )}
        </motion.div>

        <div className="navigation-buttons">
          <button 
            onClick={handlePrevious}
            disabled={currentStep === 0}
            className="nav-button prev-button"
          >
            Previous
          </button>
          
          <button 
            onClick={handleNext}
            disabled={!isStepValid()}
            className="nav-button next-button"
          >
            {currentStep === steps.length - 1 ? 'Start Adventure' : 'Next'}
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default CharacterCreation;