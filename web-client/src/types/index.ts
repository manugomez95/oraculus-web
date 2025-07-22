export interface Protagonist {
  name: string;
  gender: string;
  age: number;
  startingSituation: string;
}

export interface StoryChoice {
  id: number;
  text: string;
  isAvailable: boolean;
}

export interface StoryNode {
  id: string;
  text: string;
  choices: StoryChoice[];
  isEndNode: boolean;
}

export interface PlayerFeedback {
  nodeId: string;
  choiceIndex: number;
  rating: number; // 1-5 scale
  comment: string;
  timestamp: string;
  protagonistContext?: string;
}

export interface GameState {
  protagonist: Protagonist | null;
  currentNode: StoryNode | null;
  gameHistory: string[];
  isGameStarted: boolean;
  isLoading: boolean;
}

export interface SwipeDirection {
  left: boolean;
  right: boolean;
  up: boolean;
  down: boolean;
}