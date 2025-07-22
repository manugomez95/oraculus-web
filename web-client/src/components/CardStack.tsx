import React, { useState, useEffect, useCallback } from 'react';
import { AnimatePresence } from 'framer-motion';
import StoryCard from './StoryCard';
import { StoryNode } from '../types';
import './CardStack.css';

interface CardStackProps {
  nodes: StoryNode[];
  onChoiceSelected: (choiceId: number) => void;
  currentNodeIndex: number;
}

const CardStack: React.FC<CardStackProps> = ({
  nodes,
  onChoiceSelected,
  currentNodeIndex
}) => {
  const [activeCardIndex, setActiveCardIndex] = useState(0);

  // Handle keyboard navigation
  const handleKeyPress = useCallback((event: KeyboardEvent) => {
    const currentNode = nodes[activeCardIndex];
    if (!currentNode || currentNode.isEndNode) return;

    const availableChoices = currentNode.choices.filter(choice => choice.isAvailable);
    
    switch (event.key) {
      case 'ArrowLeft':
        event.preventDefault();
        if (availableChoices.length > 1) {
          onChoiceSelected(availableChoices[1].id);
        } else if (availableChoices.length === 1) {
          onChoiceSelected(availableChoices[0].id);
        }
        break;
      case 'ArrowRight':
        event.preventDefault();
        if (availableChoices.length > 0) {
          onChoiceSelected(availableChoices[0].id);
        }
        break;
      case '1':
      case '2':
      case '3':
        event.preventDefault();
        const choiceIndex = parseInt(event.key) - 1;
        if (availableChoices[choiceIndex]) {
          onChoiceSelected(availableChoices[choiceIndex].id);
        }
        break;
    }
  }, [nodes, activeCardIndex, onChoiceSelected]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [handleKeyPress]);

  useEffect(() => {
    setActiveCardIndex(currentNodeIndex);
  }, [currentNodeIndex]);

  const handleSwipe = (direction: 'left' | 'right', choiceId: number) => {
    onChoiceSelected(choiceId);
  };

  const handleKeyChoice = (choiceId: number) => {
    onChoiceSelected(choiceId);
  };

  // Show up to 3 cards in the stack for preview
  const visibleNodes = nodes.slice(activeCardIndex, activeCardIndex + 3);

  return (
    <div className="card-stack-container">
      <div className="card-stack">
        <AnimatePresence mode="popLayout">
          {visibleNodes.map((node, index) => (
            <StoryCard
              key={`${node.id}-${activeCardIndex + index}`}
              node={node}
              onSwipe={handleSwipe}
              onKeyChoice={handleKeyChoice}
              isActive={index === 0}
              stackPosition={index}
            />
          ))}
        </AnimatePresence>
      </div>
      
      <div className="navigation-help">
        <div className="help-text">
          <p><strong>Desktop:</strong> Use ← → arrow keys or click choices</p>
          <p><strong>Mobile:</strong> Swipe left or right</p>
        </div>
      </div>
    </div>
  );
};

export default CardStack;