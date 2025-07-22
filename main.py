#!/usr/bin/env python3
"""
Oraculus - Dynamic Text-Based Adventure Game
Phase 1: Terminal Version with Core Game Architecture
"""

import os
import json
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from anytree import Node, RenderTree, PreOrderIter
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Protagonist:
    """Player character with customizable attributes"""
    name: str
    gender: str
    age: int
    starting_situation: str
    
    def __str__(self):
        return f"{self.name} ({self.gender}, {self.age}) - {self.starting_situation}"


class VariableSystem:
    """Handles variable resolution for character attributes"""
    
    @staticmethod
    def resolve_age_range(age: int) -> str:
        """Convert specific age to age range variable"""
        if 16 <= age <= 25:
            return "young"
        elif 26 <= age <= 40:
            return "adult"  
        elif 41 <= age <= 60:
            return "middle_aged"
        else:
            return "elder"
    
    @staticmethod
    def resolve_gender_category(gender: str) -> str:
        """Convert gender to standardized category"""
        gender_lower = gender.lower()
        if gender_lower in ["male", "female"]:
            return gender_lower
        else:
            return "other"
    
    @staticmethod
    def create_variable_key(node_id: str, protagonist: 'Protagonist') -> str:
        """Create a cache key using variable ranges instead of specific values"""
        age_range = VariableSystem.resolve_age_range(protagonist.age)
        gender_category = VariableSystem.resolve_gender_category(protagonist.gender)
        return f"{node_id}_{gender_category}_{age_range}"
    
    @staticmethod
    def resolve_variables(text: str, protagonist: 'Protagonist') -> str:
        """Resolve variable placeholders in text using protagonist attributes"""
        variables = {
            'name': protagonist.name,
            'gender': protagonist.gender,
            'age': str(protagonist.age),
            'age_range': VariableSystem.resolve_age_range(protagonist.age),
            'gender_category': VariableSystem.resolve_gender_category(protagonist.gender),
            'situation': protagonist.starting_situation
        }
        
        resolved_text = text
        for var, value in variables.items():
            resolved_text = resolved_text.replace(f"{{{var}}}", value)
            resolved_text = resolved_text.replace(f"${var}", value)
        
        return resolved_text
    
    @staticmethod
    def get_all_variables(protagonist: 'Protagonist') -> Dict[str, str]:
        """Get all available variables for a protagonist"""
        return {
            'name': protagonist.name,
            'gender': protagonist.gender,
            'age': str(protagonist.age),
            'age_range': VariableSystem.resolve_age_range(protagonist.age),
            'gender_category': VariableSystem.resolve_gender_category(protagonist.gender),
            'situation': protagonist.starting_situation
        }


@dataclass
class CustomVariable:
    """Represents a user-defined variable for story generation"""
    name: str
    description: str
    variable_type: str  # 'text', 'choice', 'range', 'boolean'
    options: Optional[List[str]] = None  # For choice type
    min_value: Optional[int] = None  # For range type
    max_value: Optional[int] = None   # For range type
    default_value: Optional[str] = None


class StoryTemplate:
    """Template system for user-defined story generation"""
    
    def __init__(self, template_id: str, title: str, description: str):
        self.template_id = template_id
        self.title = title
        self.description = description
        self.story_template = ""
        self.custom_variables: Dict[str, CustomVariable] = {}
        self.predefined_scenarios: List[Dict[str, str]] = []
    
    def add_custom_variable(self, variable: CustomVariable):
        """Add a custom variable to the template"""
        self.custom_variables[variable.name] = variable
    
    def set_story_template(self, template: str):
        """Set the story template text with variable placeholders"""
        self.story_template = template
    
    def add_predefined_scenario(self, scenario_name: str, variable_values: Dict[str, str]):
        """Add a predefined scenario with preset variable values"""
        scenario = {"name": scenario_name, **variable_values}
        self.predefined_scenarios.append(scenario)
    
    def generate_story(self, variable_values: Dict[str, str], protagonist: Optional[Protagonist] = None) -> str:
        """Generate a story using the template and provided variable values"""
        # Combine custom variables with character variables
        all_variables = variable_values.copy()
        
        if protagonist:
            char_vars = VariableSystem.get_all_variables(protagonist)
            all_variables.update(char_vars)
        
        # Resolve variables in the story template
        story = self.story_template
        for var_name, value in all_variables.items():
            story = story.replace(f"{{{var_name}}}", str(value))
            story = story.replace(f"${var_name}", str(value))
        
        return story
    
    def validate_variables(self, variable_values: Dict[str, str]) -> List[str]:
        """Validate that provided variable values match the template requirements"""
        errors = []
        
        for var_name, variable in self.custom_variables.items():
            if var_name not in variable_values:
                if variable.default_value is None:
                    errors.append(f"Required variable '{var_name}' not provided")
                continue
            
            value = variable_values[var_name]
            
            if variable.variable_type == "choice" and variable.options:
                if value not in variable.options:
                    errors.append(f"Variable '{var_name}' must be one of: {', '.join(variable.options)}")
            
            elif variable.variable_type == "range":
                try:
                    num_value = int(value)
                    if variable.min_value is not None and num_value < variable.min_value:
                        errors.append(f"Variable '{var_name}' must be at least {variable.min_value}")
                    if variable.max_value is not None and num_value > variable.max_value:
                        errors.append(f"Variable '{var_name}' must be at most {variable.max_value}")
                except ValueError:
                    errors.append(f"Variable '{var_name}' must be a number")
        
        return errors


class StoryTemplateManager:
    """Manages story templates for web deployment"""
    
    def __init__(self):
        self.templates: Dict[str, StoryTemplate] = {}
        self._create_default_templates()
    
    def add_template(self, template: StoryTemplate):
        """Add a story template"""
        self.templates[template.template_id] = template
    
    def get_template(self, template_id: str) -> Optional[StoryTemplate]:
        """Get a story template by ID"""
        return self.templates.get(template_id)
    
    def list_templates(self) -> List[Dict[str, str]]:
        """List all available templates"""
        return [
            {
                "id": template.template_id,
                "title": template.title, 
                "description": template.description
            }
            for template in self.templates.values()
        ]
    
    def _create_default_templates(self):
        """Create default story templates"""
        # Fantasy Adventure Template
        fantasy_template = StoryTemplate(
            "fantasy_adventure", 
            "Fantasy Adventure",
            "A customizable fantasy adventure with magical elements"
        )
        
        fantasy_template.add_custom_variable(CustomVariable(
            "setting", "The world/location where the adventure takes place",
            "choice", ["enchanted_forest", "ancient_castle", "mystical_mountains", "underground_dungeon"]
        ))
        
        fantasy_template.add_custom_variable(CustomVariable(
            "magical_item", "A magical item the protagonist encounters",
            "choice", ["glowing_crystal", "ancient_scroll", "enchanted_mirror", "mysterious_amulet"]
        ))
        
        fantasy_template.add_custom_variable(CustomVariable(
            "threat_level", "How dangerous the adventure should be",
            "range", min_value=1, max_value=10, default_value="5"
        ))
        
        fantasy_template.set_story_template("""
You awaken in a {setting}, feeling disoriented and unsure of how you arrived here.
As a {age_range} {gender} {situation}, you notice a {magical_item} nearby that seems to pulse with otherworldly energy.
The air crackles with magic, and you sense that this place holds both great promise and danger (threat level: {threat_level}/10).
The path ahead is shrouded in mystery, and your choices will determine your fate in this realm.
        """.strip())
        
        fantasy_template.add_predefined_scenario("Lost Scholar", {
            "setting": "ancient_castle",
            "magical_item": "ancient_scroll", 
            "threat_level": "3"
        })
        
        fantasy_template.add_predefined_scenario("Dangerous Quest", {
            "setting": "underground_dungeon",
            "magical_item": "glowing_crystal",
            "threat_level": "8" 
        })
        
        self.add_template(fantasy_template)
        
        # Sci-fi Template
        scifi_template = StoryTemplate(
            "scifi_exploration",
            "Sci-Fi Exploration", 
            "A space exploration adventure with technology and alien worlds"
        )
        
        scifi_template.add_custom_variable(CustomVariable(
            "location", "Where the adventure takes place",
            "choice", ["space_station", "alien_planet", "generation_ship", "research_facility"]
        ))
        
        scifi_template.add_custom_variable(CustomVariable(
            "tech_level", "Level of available technology",
            "range", min_value=1, max_value=10, default_value="7"
        ))
        
        scifi_template.add_custom_variable(CustomVariable(
            "alien_presence", "Are there aliens in this scenario",
            "boolean", default_value="true"
        ))
        
        scifi_template.set_story_template("""
You find yourself aboard a {location}, surrounded by technology that hums with energy (tech level: {tech_level}/10).
As a {age_range} {gender} {situation}, you're equipped with advanced gear but face an uncertain situation.
{alien_presence}Your sensors detect unusual readings that suggest you're not alone in this place.
The future of your mission - and perhaps humanity itself - depends on the decisions you make next.
        """.strip())
        
        self.add_template(scifi_template)
    
    def get_template_variables(self, template_id: str) -> Optional[Dict]:
        """Get template variables in API-ready format"""
        template = self.get_template(template_id)
        if not template:
            return None
        
        variables = {}
        for var_name, var in template.custom_variables.items():
            variables[var_name] = {
                "name": var.name,
                "description": var.description,
                "type": var.variable_type,
                "options": var.options,
                "min_value": var.min_value,
                "max_value": var.max_value,
                "default_value": var.default_value
            }
        
        return {
            "template_id": template.template_id,
            "title": template.title,
            "description": template.description,
            "variables": variables,
            "predefined_scenarios": template.predefined_scenarios
        }
    
    def generate_story_api(self, template_id: str, variable_values: Dict[str, str], 
                          character_data: Dict[str, str]) -> Dict[str, str]:
        """Generate story via API call"""
        template = self.get_template(template_id)
        if not template:
            return {"error": "Template not found"}
        
        # Validate variables
        validation_errors = template.validate_variables(variable_values)
        if validation_errors:
            return {"error": "Validation failed", "details": validation_errors}
        
        # Create protagonist from character data
        protagonist = Protagonist(
            name=character_data.get("name", "Adventurer"),
            gender=character_data.get("gender", "other"),
            age=int(character_data.get("age", "25")),
            starting_situation=character_data.get("situation", "An ordinary person in extraordinary circumstances")
        )
        
        # Generate story
        story = template.generate_story(variable_values, protagonist)
        cache_key = VariableSystem.create_variable_key("template_" + template_id, protagonist)
        
        return {
            "success": True,
            "story": story,
            "cache_key": cache_key,
            "character_variables": VariableSystem.get_all_variables(protagonist)
        }


class ChoiceCache:
    """Caching mechanism for LLM-generated choices with variable support"""
    
    def __init__(self):
        self.cache: Dict[str, List[str]] = {}
        self.cache_file = "choice_cache.json"
        self.variable_system = VariableSystem()
        self.load_cache()
    
    def load_cache(self):
        """Load cached choices from file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load cache: {e}")
            self.cache = {}
    
    def save_cache(self):
        """Save cached choices to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")
    
    def get(self, key: str) -> Optional[List[str]]:
        """Get cached choices for a given story node"""
        return self.cache.get(key)
    
    def set(self, key: str, choices: List[str]):
        """Cache choices for a given story node"""
        self.cache[key] = choices
        self.save_cache()


class StoryTree:
    """Manages the story tree structure and navigation"""
    
    def __init__(self):
        self.root = None
        self.current_node = None
        self.choice_cache = ChoiceCache()
        self.anthropic_client = None
        self._initialize_anthropic()
        self._create_seed_tree()
    
    def _initialize_anthropic(self):
        """Initialize Claude API client"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            self.anthropic_client = Anthropic(api_key=api_key)
        else:
            print("Warning: ANTHROPIC_API_KEY not found. LLM features will be limited.")
    
    def _create_seed_tree(self):
        """Create the initial seed tree with 8 nodes"""
        
        # Root node - Beginning
        self.root = Node("start", 
                        story="You wake up in a dimly lit room with no memory of how you got here. "
                              "The air feels thick and mysterious. To your left, you see a dusty mirror "
                              "reflecting strange shadows. To your right, an old wooden door stands slightly ajar.",
                        node_id="start")
        
        # Level 1 choices
        mirror_node = Node("examine_mirror", 
                          parent=self.root,
                          story="You approach the ornate mirror. As you look into it, your reflection "
                                "seems to shimmer and change. For a moment, you see yourself differently - "
                                "older, younger, or perhaps from another time entirely. The mirror's surface "
                                "ripples like water.",
                          node_id="examine_mirror")
        
        door_node = Node("approach_door",
                        parent=self.root, 
                        story="You slowly push the door open and step into a long, winding corridor. "
                              "Ancient torches flicker along the stone walls, casting dancing shadows. "
                              "The corridor splits into two paths: one descends into darkness, the other "
                              "leads toward a faint, warm light.",
                        node_id="approach_door")
        
        # Level 2 choices from mirror
        touch_mirror = Node("touch_mirror",
                           parent=mirror_node,
                           story="As your fingertips touch the mirror's surface, it gives way like liquid. "
                                 "You feel a strange pulling sensation, and suddenly you're standing in what "
                                 "appears to be the same room, but everything is reversed and slightly different. "
                                 "A voice whispers: 'Welcome to the other side.'",
                           node_id="touch_mirror")
        
        step_away = Node("step_away_mirror", 
                        parent=mirror_node,
                        story="You step back from the unsettling mirror, deciding some mysteries are better "
                              "left alone. As you turn away, you notice a small, leather-bound journal on a "
                              "nearby table that wasn't there before. Its pages seem to flutter on their own.",
                        node_id="step_away_mirror")
        
        # Level 2 choices from door
        dark_path = Node("dark_path",
                        parent=door_node,
                        story="You choose the darker path, feeling your way along the cold stone walls. "
                              "After several minutes, you emerge into a vast underground chamber filled with "
                              "glowing crystals. Their light reveals ancient carvings on the walls that seem "
                              "to tell a story about travelers like yourself.",
                        node_id="dark_path")
        
        light_path = Node("light_path", 
                         parent=door_node,
                         story="Following the warm light, you find yourself in a cozy library filled with "
                               "floating books and scrolls. An elderly figure in robes looks up from a desk "
                               "and smiles knowingly. 'Ah, another seeker has arrived. I've been expecting you.'",
                         node_id="light_path")
        
        # Level 3 choices
        investigate_crystals = Node("investigate_crystals",
                                  parent=dark_path,
                                  story="You approach the largest crystal, which pulses with an inner light. "
                                        "As you touch it, visions flood your mind - glimpses of other adventurers "
                                        "who came before you, each making choices that shaped their destiny. "
                                        "You realize this place responds to the decisions of those who enter.",
                                  node_id="investigate_crystals")
        
        meet_librarian = Node("meet_librarian",
                             parent=light_path, 
                             story="The librarian gestures to a chair across from their desk. 'Every story "
                                   "needs a beginning, and every choice creates new possibilities. You have "
                                   "the power to shape not just your path, but the very nature of this realm. "
                                   "What kind of story do you wish to write?'",
                             node_id="meet_librarian")
        
        self.current_node = self.root
    
    def get_current_story(self) -> str:
        """Get the current story text"""
        return self.current_node.story if self.current_node else ""
    
    def get_choices(self, protagonist: Protagonist) -> List[str]:
        """Get available choices for the current node"""
        if not self.current_node:
            return []
        
        # Check for pre-defined children (seed tree)
        if self.current_node.children:
            choices = []
            for child in self.current_node.children:
                choice_text = self._generate_choice_text(child.name)
                choices.append(choice_text)
            return choices
        
        # Generate choices using LLM or fallback
        return self._generate_dynamic_choices(protagonist)
    
    def _generate_choice_text(self, node_name: str) -> str:
        """Convert node names to readable choice text"""
        choice_map = {
            "examine_mirror": "Examine the mysterious mirror",
            "approach_door": "Approach the wooden door", 
            "touch_mirror": "Touch the mirror's surface",
            "step_away_mirror": "Step away from the mirror",
            "dark_path": "Take the dark path downward",
            "light_path": "Follow the path toward the light",
            "investigate_crystals": "Investigate the glowing crystals",
            "meet_librarian": "Speak with the librarian"
        }
        return choice_map.get(node_name, node_name.replace("_", " ").title())
    
    def _generate_dynamic_choices(self, protagonist: Protagonist) -> List[str]:
        """Generate choices using LLM or fallback options"""
        cache_key = VariableSystem.create_variable_key(self.current_node.node_id, protagonist)
        
        # Check cache first
        cached_choices = self.choice_cache.get(cache_key)
        if cached_choices:
            return cached_choices
        
        # Try to generate with LLM
        if self.anthropic_client:
            try:
                choices = self._generate_llm_choices(protagonist)
                self.choice_cache.set(cache_key, choices)
                return choices
            except Exception as e:
                print(f"LLM generation failed: {e}")
        
        # Fallback choices
        fallback_choices = [
            "Continue exploring the area",
            "Look for more clues about your situation", 
            "Try to remember how you got here",
            "Search for a way out"
        ]
        
        # Add some randomness
        random.shuffle(fallback_choices)
        return fallback_choices[:3]
    
    def _generate_llm_choices(self, protagonist: Protagonist) -> List[str]:
        """Generate choices using Claude API"""
        current_story = self.get_current_story()
        
        prompt = f"""You are generating choices for a dynamic text adventure game.

Current situation: {current_story}

Protagonist: {protagonist}

Generate exactly 3 interesting and distinct choices that:
1. Advance the story meaningfully
2. Reflect the protagonist's background
3. Offer different types of approaches (bold, cautious, creative)
4. Are each 6-12 words long

Return only the choices, one per line, without numbers or bullets."""

        message = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        
        choices = [choice.strip() for choice in message.content[0].text.strip().split('\n') if choice.strip()]
        return choices[:3]
    
    def make_choice(self, choice_index: int, protagonist: Protagonist) -> bool:
        """Make a choice and advance the story"""
        if not self.current_node:
            return False
        
        # Handle pre-defined tree navigation
        if self.current_node.children:
            if 0 <= choice_index < len(self.current_node.children):
                self.current_node = list(self.current_node.children)[choice_index]
                return True
            return False
        
        # For dynamic choices, we would generate new nodes here
        # For now, just show a continuation message
        print(f"\n[Dynamic choice {choice_index + 1} selected - this would expand the tree in Phase 2]")
        return False
    
    def print_tree_structure(self):
        """Debug function to print the entire tree structure"""
        if self.root:
            for pre, _, node in RenderTree(self.root):
                print(f"{pre}{node.name}")


class Game:
    """Main game controller"""
    
    def __init__(self):
        self.protagonist = None
        self.story_tree = StoryTree()
        self.running = True
    
    def start(self):
        """Start the game"""
        self.display_welcome()
        self.create_protagonist()
        self.game_loop()
    
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("=" * 60)
        print("         WELCOME TO ORACULUS")
        print("    A Dynamic Text-Based Adventure Game")
        print("=" * 60)
        print("\nIn this game, your choices shape the story.")
        print("Each decision creates new possibilities and branches.")
        print("Your character's background influences available options.\n")
    
    def create_protagonist(self):
        """Create and customize the protagonist"""
        print("First, let's create your character:\n")
        
        name = input("Enter your character's name: ").strip()
        if not name:
            name = "Adventurer"
        
        print("\nSelect gender:")
        print("1. Male")
        print("2. Female") 
        print("3. Non-binary")
        print("4. Other")
        
        gender_choice = input("Enter choice (1-4): ").strip()
        gender_map = {"1": "male", "2": "female", "3": "non-binary", "4": "other"}
        gender = gender_map.get(gender_choice, "other")
        
        while True:
            try:
                age = int(input("\nEnter age (16-100): "))
                if 16 <= age <= 100:
                    break
                else:
                    print("Age must be between 16 and 100.")
            except ValueError:
                print("Please enter a valid number.")
        
        print("\nSelect starting situation:")
        situations = [
            "A mysterious traveler seeking ancient knowledge",
            "A scholar who stumbled into a magical realm", 
            "A warrior searching for a lost artifact",
            "An ordinary person caught in extraordinary circumstances"
        ]
        
        for i, situation in enumerate(situations, 1):
            print(f"{i}. {situation}")
        
        situation_choice = input("Enter choice (1-4): ").strip()
        try:
            situation_index = int(situation_choice) - 1
            if 0 <= situation_index < len(situations):
                starting_situation = situations[situation_index]
            else:
                starting_situation = situations[0]
        except ValueError:
            starting_situation = situations[0]
        
        self.protagonist = Protagonist(name, gender, age, starting_situation)
        
        print(f"\nCharacter created: {self.protagonist}")
        print("\nPress Enter to begin your adventure...")
        input()
    
    def game_loop(self):
        """Main game loop"""
        while self.running:
            self.display_current_situation()
            self.handle_player_input()
    
    def display_current_situation(self):
        """Display the current story and available choices"""
        print("\n" + "=" * 60)
        print(self.story_tree.get_current_story())
        print("\n" + "-" * 40)
        
        choices = self.story_tree.get_choices(self.protagonist)
        if choices:
            print("\nWhat do you choose?")
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")
        else:
            print("\n[End of current story branch - more content coming in Phase 2!]")
            self.running = False
    
    def handle_player_input(self):
        """Handle player input and choices"""
        choices = self.story_tree.get_choices(self.protagonist)
        if not choices:
            return
        
        while True:
            try:
                print(f"\nEnter your choice (1-{len(choices)}) or 'quit' to exit: ", end="")
                user_input = input().strip().lower()
                
                if user_input in ['quit', 'exit', 'q']:
                    self.running = False
                    print("\nThanks for playing Oraculus!")
                    return
                
                choice_num = int(user_input)
                if 1 <= choice_num <= len(choices):
                    success = self.story_tree.make_choice(choice_num - 1, self.protagonist)
                    if not success:
                        print("\n[This choice will be fully implemented in Phase 2]")
                        print("The story continues to evolve based on player feedback...")
                        self.running = False
                    break
                else:
                    print(f"Please enter a number between 1 and {len(choices)}")
                    
            except ValueError:
                print("Please enter a valid number or 'quit'")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                self.running = False
                break


def main():
    """Main entry point"""
    try:
        game = Game()
        game.start()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main()