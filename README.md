# Oraculus - Dynamic Text-Based Adventure Game

A dynamic text-based adventure game that evolves based on player choices and feedback, powered by Claude AI.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Claude API key from Anthropic

### Installation

1. **Clone or download the project to your desired directory**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Claude API (optional but recommended):**
   
   Create a `.env` file in the project root:
   ```bash
   echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
   ```
   
   Or set environment variable:
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

4. **Run the game:**
   ```bash
   python main.py
   ```

## How to Play

1. **Character Creation:** Start by creating your protagonist with custom name, gender, age, and starting situation
2. **Story Navigation:** Read the story text and choose from available options (numbered 1-3)
3. **Make Choices:** Type the number of your choice and press Enter
4. **Explore:** Your decisions shape the story and determine available paths

### Game Controls
- Enter `1`, `2`, or `3` to make choices
- Type `quit`, `exit`, or `q` to exit the game
- Press `Ctrl+C` to force quit if needed

## Features

### Phase 1 (Current Implementation)
✅ **Complete Core Game Architecture:**
- Python-based text adventure with tree structure using `anytree`
- Protagonist customization (gender, age, starting situation)
- 8-node seed story tree with branching paths
- Claude API integration for dynamic choice generation
- Local caching system for LLM-generated content
- Terminal-based interface with intuitive navigation

### Phase 2 (Planned)
- User feedback collection system
- Dynamic tree expansion based on player input
- LLM-driven story evaluation and branch selection

### Phase 3 (Planned)
- Flask backend API
- React frontend with real-time updates
- Web-based GUI interface

### Phase 4 (Planned)
- Unit testing framework
- Performance optimization and caching improvements
- Cloud deployment with multi-user support

## Project Structure

```
Oraculus/
├── main.py              # Main game engine and logic
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env                # Environment variables (create this)
└── choice_cache.json   # LLM choice cache (auto-generated)
```

## Claude API Integration

The game works without the Claude API (using fallback choices), but the experience is enhanced with it:

1. **Get API Key:** Sign up at [Anthropic Console](https://console.anthropic.com/)
2. **Set Environment Variable:** Add your key to `.env` file or environment
3. **Enhanced Features:** Dynamic story generation, context-aware choices, personalized content

### Without API Key
- Uses pre-defined seed tree (8 nodes)
- Fallback choice generation
- Basic story progression

### With API Key
- Dynamic choice generation based on protagonist and story context
- Personalized story elements
- Cached responses for better performance

## Dependencies

- **anthropic** (>=0.40.0): Claude API client
- **anytree** (2.12.1): Tree data structure for story branches
- **flask** (3.0.0): Web framework for future phases
- **python-dotenv** (1.0.0): Environment variable management

## Troubleshooting

### Common Issues

**Game won't start:**
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`

**API errors:**
- Verify ANTHROPIC_API_KEY is set correctly
- Check API key validity at Anthropic Console
- Game will continue with fallback choices if API fails

**Permission errors:**
- Ensure write permissions for cache file creation
- Run from project directory: `cd /path/to/Oraculus && python main.py`

## Implementation Plan Summary

### Phase 1: Core Game Architecture (Terminal Version) ✅
- Build Python-based text adventure with a tree structure (using anytree) for story branches
- Include protagonist attributes (gender, age, starting situation)
- Generate and cache LLM choices (via Claude API)
- Start with a premade seed tree of 5-10 nodes, with semi-random elements

### Phase 2: User Feedback and Dynamic Tree Growth
- Allow user comments via input
- Server accumulates feedback, generates possible events incorporating it
- Use LLM to evaluate and select logical branches to expand the tree dynamically

### Phase 3: Transition to Web Version with GUI
- Extend to web app using Flask backend and React frontend for story display, choices, and feedback
- Add real-time updates

### Phase 4: Testing, Optimization, and Deployment
- Unit tests, caching optimization, deployment to cloud
- Ensure scalability for multi-user and semi-random game variants

## Contributing

This project is designed to be modular and extensible. The current implementation provides a solid foundation for the planned features in subsequent phases.