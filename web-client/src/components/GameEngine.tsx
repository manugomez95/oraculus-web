import React, { useState } from 'react';
import CardStack from './CardStack';
import CharacterCreation from './CharacterCreation';
import { GameState, StoryNode, Protagonist } from '../types';
import './GameEngine.css';

// Mock data based on the Python implementation
const createMockStoryNodes = (protagonist: Protagonist): StoryNode[] => {
  const ageRange = protagonist.age <= 25 ? 'young' : protagonist.age <= 40 ? 'adult' : 'elder';
  
  return [
    {
      id: 'root',
      text: `You are ${protagonist.name}, a ${ageRange} ${protagonist.gender}. ${protagonist.startingSituation} You find yourself at a crossroads, literally and metaphorically. The sun is setting, casting long shadows across the path ahead. What do you choose to do?`,
      choices: [
        { id: 1, text: 'Take the well-traveled road to the nearby village', isAvailable: true },
        { id: 2, text: 'Venture into the mysterious forest path', isAvailable: true },
        { id: 3, text: 'Set up camp here and wait for morning', isAvailable: true }
      ],
      isEndNode: false
    },
    {
      id: 'village_path',
      text: 'The village road is safe but mundane. As you walk, you encounter a traveling merchant whose cart has broken down. They offer valuable information in exchange for help.',
      choices: [
        { id: 4, text: 'Help the merchant fix their cart', isAvailable: true },
        { id: 5, text: 'Listen to their stories but continue on', isAvailable: true }
      ],
      isEndNode: false
    },
    {
      id: 'forest_path',
      text: 'The forest whispers secrets in the wind. Ancient trees tower above you, and you hear the sound of flowing water nearby. A glimmer of light catches your eye deeper in the woods.',
      choices: [
        { id: 6, text: 'Follow the mysterious light', isAvailable: true },
        { id: 7, text: 'Head toward the sound of water', isAvailable: true }
      ],
      isEndNode: false
    },
    {
      id: 'camp_here',
      text: 'The night brings unexpected visitors. A group of fellow travelers approaches your campfire, seeking warmth and companionship. They share tales of their journeys.',
      choices: [
        { id: 8, text: 'Invite them to share your fire', isAvailable: true },
        { id: 9, text: 'Keep to yourself but remain polite', isAvailable: true }
      ],
      isEndNode: false
    }
  ];
};

const GameEngine: React.FC = () => {
  const [gameState, setGameState] = useState<GameState>({
    protagonist: null,
    currentNode: null,
    gameHistory: [],
    isGameStarted: false,
    isLoading: false
  });

  const [storyNodes, setStoryNodes] = useState<StoryNode[]>([]);
  const [currentNodeIndex, setCurrentNodeIndex] = useState(0);

  const handleCharacterCreated = (protagonist: Protagonist) => {
    const nodes = createMockStoryNodes(protagonist);
    setStoryNodes(nodes);
    setGameState(prev => ({
      ...prev,
      protagonist,
      currentNode: nodes[0],
      isGameStarted: true
    }));
  };

  const handleChoiceSelected = (choiceId: number) => {
    const currentNode = storyNodes[currentNodeIndex];
    if (!currentNode) return;

    const selectedChoice = currentNode.choices.find(choice => choice.id === choiceId);
    if (!selectedChoice) return;

    // Add choice to history
    setGameState(prev => ({
      ...prev,
      gameHistory: [...prev.gameHistory, `${currentNode.text} → ${selectedChoice.text}`]
    }));

    // Simulate navigation to next node based on choice
    let nextNodeIndex = currentNodeIndex;
    
    if (currentNode.id === 'root') {
      if (choiceId === 1) nextNodeIndex = 1; // village_path
      else if (choiceId === 2) nextNodeIndex = 2; // forest_path
      else if (choiceId === 3) nextNodeIndex = 3; // camp_here
    } else {
      // For now, create a simple end node
      const endNode: StoryNode = {
        id: `end_${choiceId}`,
        text: `Your choice leads to new adventures. This is where your story continues to evolve based on your decisions. The journey of ${gameState.protagonist?.name} is just beginning...`,
        choices: [],
        isEndNode: true
      };
      
      setStoryNodes(prev => [...prev, endNode]);
      nextNodeIndex = storyNodes.length;
    }

    setCurrentNodeIndex(nextNodeIndex);
    setGameState(prev => ({
      ...prev,
      currentNode: storyNodes[nextNodeIndex]
    }));
  };

  const resetGame = () => {
    setGameState({
      protagonist: null,
      currentNode: null,
      gameHistory: [],
      isGameStarted: false,
      isLoading: false
    });
    setStoryNodes([]);
    setCurrentNodeIndex(0);
  };

  if (!gameState.isGameStarted) {
    return <CharacterCreation onCharacterCreated={handleCharacterCreated} />;
  }

  return (
    <div className="game-engine">
      <div className="game-header">
        <h1>Oraculus</h1>
        <div className="character-info">
          <span>{gameState.protagonist?.name}</span>
          <button onClick={resetGame} className="reset-button">
            New Game
          </button>
        </div>
      </div>

      <CardStack
        nodes={storyNodes}
        onChoiceSelected={handleChoiceSelected}
        currentNodeIndex={currentNodeIndex}
      />

      {gameState.gameHistory.length > 0 && (
        <div className="game-history">
          <details>
            <summary>Story History ({gameState.gameHistory.length})</summary>
            <div className="history-list">
              {gameState.gameHistory.map((entry, index) => (
                <div key={index} className="history-entry">
                  {entry}
                </div>
              ))}
            </div>
          </details>
        </div>
      )}
    </div>
  );
};

export default GameEngine;