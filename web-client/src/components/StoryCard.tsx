import React from 'react';
import { motion, PanInfo } from 'framer-motion';
import { StoryNode } from '../types';
import './StoryCard.css';

interface StoryCardProps {
  node: StoryNode;
  onSwipe: (direction: 'left' | 'right', choiceIndex: number) => void;
  onKeyChoice: (choiceIndex: number) => void;
  isActive: boolean;
  stackPosition: number;
}

const StoryCard: React.FC<StoryCardProps> = ({
  node,
  onSwipe,
  onKeyChoice,
  isActive,
  stackPosition
}) => {
  const handleDragEnd = (event: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => {
    const threshold = 100;
    const { offset, velocity } = info;

    // Determine swipe direction based on offset and velocity
    if (Math.abs(offset.x) > threshold || Math.abs(velocity.x) > 500) {
      if (offset.x > 0) {
        // Right swipe - choose first available choice
        const firstChoice = node.choices.find(choice => choice.isAvailable);
        if (firstChoice) {
          onSwipe('right', firstChoice.id);
        }
      } else {
        // Left swipe - choose second available choice
        const availableChoices = node.choices.filter(choice => choice.isAvailable);
        if (availableChoices.length > 1) {
          onSwipe('left', availableChoices[1].id);
        } else if (availableChoices.length === 1) {
          onSwipe('left', availableChoices[0].id);
        }
      }
    }
  };

  const getCardStyle = () => {
    const baseStyle = {
      zIndex: 10 - stackPosition,
      scale: 1 - (stackPosition * 0.05),
      y: stackPosition * 10,
      opacity: stackPosition < 3 ? 1 - (stackPosition * 0.2) : 0
    };
    return baseStyle;
  };

  const availableChoices = node.choices.filter(choice => choice.isAvailable);
  const leftChoice = availableChoices[1] || availableChoices[0];
  const rightChoice = availableChoices[0];

  return (
    <motion.div
      className={`story-card ${isActive ? 'active' : ''}`}
      drag={isActive ? "x" : false}
      dragConstraints={{ left: 0, right: 0 }}
      dragElastic={0.2}
      onDragEnd={handleDragEnd}
      initial={getCardStyle()}
      animate={getCardStyle()}
      exit={{ x: 300, opacity: 0, scale: 0.8 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
      whileDrag={{ scale: 1.05, rotate: 5 }}
    >
      <div className="card-content">
        <div className="story-text">
          {node.text}
        </div>
        
        {!node.isEndNode && (
          <div className="choices-section">
            <div className="swipe-hints">
              <div className="choice-hint left">
                <span className="choice-label">Swipe Left</span>
                <div className="choice-preview">
                  {leftChoice?.text}
                </div>
              </div>
              
              <div className="choice-hint right">
                <span className="choice-label">Swipe Right</span>
                <div className="choice-preview">
                  {rightChoice?.text}
                </div>
              </div>
            </div>

            <div className="choice-buttons">
              {availableChoices.map((choice, index) => (
                <button
                  key={choice.id}
                  className={`choice-button choice-${index + 1}`}
                  onClick={() => onKeyChoice(choice.id)}
                >
                  {index + 1}. {choice.text}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Swipe direction indicators */}
      <div className="swipe-indicator left-indicator">
        <span>👈</span>
      </div>
      <div className="swipe-indicator right-indicator">
        <span>👉</span>
      </div>
    </motion.div>
  );
};

export default StoryCard;