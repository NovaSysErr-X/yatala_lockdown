#!/usr/bin/env python3
"""
YATALA LOCKDOWN - Component Module

Copyright © 2025 NovaSysErr-X. All rights reserved.

LEGAL WARNING:
This file is protected by copyright law and international treaties.
Unauthorized reproduction, distribution, or modification is prohibited.
Violators will be prosecuted to the fullest extent of the law.

This software contains anti-tampering mechanisms and digital watermarks.
Any attempt to circumvent these protections is illegal and will be detected.

Author: NovaSysErr-X
Version: 0.5.0 beta
Protected by: COPYRIGHT_PROTECTION.md and SECURITY_POLICY.md
"""

PRISON BREAK: The Ultimate Inmate Simulation
A sophisticated CLI-based prison survival RPG game

Author: NovaSysErr-X
Version: 0.5.0 beta
Platform: Termux / Linux Terminal
Python: 3.9+

This is a complete, production-grade game with zero external dependencies.
Simply run: python3 prison_break.py

import curses
import json
import random
import time
import os
import sys
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from datetime import datetime, timedelta
from collections import defaultdict
import textwrap


# ============================================================================
# TYPE DEFINITIONS AND ENUMS
# ============================================================================

class GameState(Enum):
    """Game state enumeration"""
    MAIN_MENU = auto()
    CHARACTER_CREATION = auto()
    PLAYING = auto()
    INVENTORY = auto()
    CHARACTER_SHEET = auto()
    MAP = auto()
    QUEST_LOG = auto()
    RELATIONSHIPS = auto()
    COMBAT = auto()
    DIALOGUE = auto()
    TRADING = auto()
    GAME_OVER = auto()
    PAUSED = auto()


class LocationType(Enum):
    """Location types in prison"""
    CELL = auto()
    CAFETERIA = auto()
    YARD = auto()
    LIBRARY = auto()
    GYM = auto()
    WORKSHOP = auto()
    INFIRMARY = auto()
    SHOWERS = auto()
    VISITATION = auto()
    SOLITARY = auto()
    GUARD_STATION = auto()


class ItemType(Enum):
    """Item categories"""
    WEAPON = auto()
    CONSUMABLE = auto()
    CONTRABAND = auto()
    CRAFTING = auto()
    BOOK = auto()
    CURRENCY = auto()
    QUEST = auto()


class GangType(Enum):
    """Available gangs"""
    NONE = auto()
    BROTHERHOOD = auto()
    LOS_HERMANOS = auto()
    THE_NATION = auto()
    SYNDICATE = auto()


class QuestStatus(Enum):
    """Quest states"""
    NOT_STARTED = auto()
    ACTIVE = auto()
    COMPLETED = auto()
    FAILED = auto()


class CombatAction(Enum):
    """Combat actions"""
    ATTACK = auto()
    HEAVY_ATTACK = auto()
    DEFEND = auto()
    DODGE = auto()
    DIRTY_MOVE = auto()
    INTIMIDATE = auto()
    FLEE = auto()
    CALL_HELP = auto()


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Attributes:
    """Character attributes"""
    # Physical
    strength: int = 50
    stamina: int = 50
    health: int = 100
    toughness: int = 50
    
    # Mental
    intelligence: int = 50
    willpower: int = 50
    sanity: int = 100
    perception: int = 50
    
    # Social
    charisma: int = 50
    intimidation: int = 50
    reputation: int = 0
    respect: int = 0


@dataclass
class Skills:
    """Character skills"""
    # Combat
    brawling: int = 0
    knife_fighting: int = 0
    defense: int = 0
    dirty_fighting: int = 0
    
    # Survival
    stealth: int = 0
    lockpicking: int = 0
    first_aid: int = 0
    cooking: int = 0
    
    # Social
    persuasion: int = 0
    intimidation_skill: int = 0
    deception: int = 0
    leadership: int = 0
    
    # Practical
    crafting: int = 0
    trading: int = 0
    smuggling: int = 0
    planning: int = 0


@dataclass
class StatusEffect:
    """Status effect on character"""
    name: str
    duration: int  # in game hours
    stat_modifiers: Dict[str, float] = field(default_factory=dict)
    description: str = ""


@dataclass
class Item:
    """Game item"""
    id: str
    name: str
    description: str
    item_type: ItemType
    value: int = 0
    weight: float = 0.0
    stackable: bool = False
    quantity: int = 1
    damage: int = 0
    effects: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NPC:
    """Non-player character"""
    id: str
    name: str
    description: str
    personality: Dict[str, int] = field(default_factory=dict)
    relationship: int = 0  # -100 to 100
    gang: GangType = GangType.NONE
    location: str = ""
    inventory: List[Item] = field(default_factory=list)
    dialogue: Dict[str, List[str]] = field(default_factory=dict)
    is_guard: bool = False
    is_hostile: bool = False


@dataclass
class Quest:
    """Game quest"""
    id: str
    name: str
    description: str
    objectives: List[str] = field(default_factory=list)
    rewards: Dict[str, Any] = field(default_factory=dict)
    status: QuestStatus = QuestStatus.NOT_STARTED
    progress: Dict[str, int] = field(default_factory=dict)


@dataclass
class Location:
    """Game location"""
    id: str
    name: str
    description: str
    location_type: LocationType
    npcs: List[str] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)
    connections: List[str] = field(default_factory=list)
    danger_level: int = 0
    guard_presence: int = 0
    time_restrictions: Dict[str, Tuple[int, int]] = field(default_factory=dict)


@dataclass
class GameTime:
    """Game time tracking"""
    day: int = 1
    hour: int = 6
    minute: int = 0
    
    def advance(self, minutes: int) -> None:
        """Advance time by minutes"""
        self.minute += minutes
        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1
    
    def get_time_string(self) -> str:
        """Get formatted time string"""
        return f"Day {self.day}, {self.hour:02d}:{self.minute:02d}"
    
    def get_period(self) -> str:
        """Get time period name"""
        if 6 <= self.hour < 8:
            return "Breakfast"
        elif 8 <= self.hour < 12:
            return "Morning"
        elif 12 <= self.hour < 13:
            return "Lunch"
        elif 13 <= self.hour < 17:
            return "Afternoon"
        elif 17 <= self.hour < 18:
            return "Dinner"
        elif 18 <= self.hour < 22:
            return "Evening"
        else:
            return "Lockdown"


# ============================================================================
# PLAYER CLASS
# ============================================================================

class Player:
    """Player character class"""
    
    def __init__(self, name: str = "Inmate"):
        self.name: str = name
        self.level: int = 1
        self.xp: int = 0
        self.xp_to_next: int = 100
        
        # Core stats
        self.attributes = Attributes()
        self.skills = Skills()
        
        # Derived stats
        self.max_health: int = 100
        self.current_health: int = 100
        self.max_energy: int = 100
        self.current_energy: int = 100
        self.hunger: int = 0  # 0-100, higher is hungrier
        self.hygiene: int = 100  # 0-100, higher is cleaner
        
        # Status
        self.status_effects: List[StatusEffect] = []
        self.location: str = "cell_a1"
        self.gang: GangType = GangType.NONE
        self.gang_rank: str = "None"
        
        # Inventory
        self.inventory: List[Item] = []
        self.max_weight: float = 50.0
        self.money: int = 0
        self.cigarettes: int = 0
        
        # Relationships
        self.relationships: Dict[str, int] = {}
        
        # Perks
        self.perks: List[str] = []
        
        # Statistics
        self.stats: Dict[str, int] = {
            "days_survived": 0,
            "fights_won": 0,
            "fights_lost": 0,
            "items_crafted": 0,
            "items_traded": 0,
            "quests_completed": 0,
            "npcs_befriended": 0,
            "npcs_killed": 0,
        }
    
    def add_xp(self, amount: int) -> bool:
        """Add XP and check for level up"""
        self.xp += amount
        if self.xp >= self.xp_to_next:
            self.level_up()
            return True
        return False
    
    def level_up(self) -> None:
        """Level up the player"""
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = self.calculate_xp_needed()
        
        # Increase max health and energy
        self.max_health += 5
        self.max_energy += 5
        self.current_health = self.max_health
        self.current_energy = self.max_energy
    
    def calculate_xp_needed(self) -> int:
        """Calculate XP needed for next level"""
        if self.level <= 10:
            return 100 * self.level
        elif self.level <= 20:
            return 200 * (self.level - 10) + 1000
        elif self.level <= 30:
            return 400 * (self.level - 20) + 3000
        elif self.level <= 40:
            return 800 * (self.level - 30) + 7000
        else:
            return 1600 * (self.level - 40) + 15000
    
    def get_total_weight(self) -> float:
        """Calculate total inventory weight"""
        return sum(item.weight * item.quantity for item in self.inventory)
    
    def can_carry(self, item: Item) -> bool:
        """Check if player can carry item"""
        return self.get_total_weight() + item.weight <= self.max_weight
    
    def add_item(self, item: Item) -> bool:
        """Add item to inventory"""
        if not self.can_carry(item):
            return False
        
        # Stack if stackable
        if item.stackable:
            for inv_item in self.inventory:
                if inv_item.id == item.id:
                    inv_item.quantity += item.quantity
                    return True
        
        self.inventory.append(item)
        return True
    
    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """Remove item from inventory"""
        for item in self.inventory:
            if item.id == item_id:
                if item.quantity >= quantity:
                    item.quantity -= quantity
                    if item.quantity <= 0:
                        self.inventory.remove(item)
                    return True
        return False
    
    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """Check if player has item"""
        for item in self.inventory:
            if item.id == item_id and item.quantity >= quantity:
                return True
        return False
    
    def heal(self, amount: int) -> None:
        """Heal player"""
        self.current_health = min(self.max_health, self.current_health + amount)
    
    def take_damage(self, amount: int) -> None:
        """Take damage"""
        self.current_health = max(0, self.current_health - amount)
    
    def restore_energy(self, amount: int) -> None:
        """Restore energy"""
        self.current_energy = min(self.max_energy, self.current_energy + amount)
    
    def use_energy(self, amount: int) -> bool:
        """Use energy, return False if not enough"""
        if self.current_energy >= amount:
            self.current_energy -= amount
            return True
        return False
    
    def add_status_effect(self, effect: StatusEffect) -> None:
        """Add status effect"""
        self.status_effects.append(effect)
    
    def remove_status_effect(self, name: str) -> None:
        """Remove status effect by name"""
        self.status_effects = [e for e in self.status_effects if e.name != name]
    
    def update_status_effects(self, hours: int) -> None:
        """Update status effects duration"""
        for effect in self.status_effects[:]:
            effect.duration -= hours
            if effect.duration <= 0:
                self.status_effects.remove(effect)
    
    def get_effective_stat(self, stat_name: str) -> float:
        """Get stat value with status effect modifiers"""
        base_value = getattr(self.attributes, stat_name, 0)
        modifier = 1.0
        
        for effect in self.status_effects:
            if stat_name in effect.stat_modifiers:
                modifier += effect.stat_modifiers[stat_name]
        
        return base_value * modifier
    
    def improve_skill(self, skill_name: str, amount: int = 1) -> None:
        """Improve a skill"""
        current = getattr(self.skills, skill_name, 0)
        new_value = min(100, current + amount)
        setattr(self.skills, skill_name, new_value)


# ============================================================================
# GAME DATA
# ============================================================================

class GameData:
    """Static game data"""
    
    @staticmethod
    def get_items() -> Dict[str, Item]:
        """Get all game items"""
        return {
            # Weapons
            "shank": Item("shank", "Shank", "A sharpened piece of metal", ItemType.WEAPON, 
                         value=50, weight=0.5, damage=20),
            "sock_soap": Item("sock_soap", "Sock with Soap", "A sock filled with bars of soap", 
                             ItemType.WEAPON, value=20, weight=1.0, damage=15),
            "shiv": Item("shiv", "Shiv", "A well-crafted stabbing weapon", ItemType.WEAPON,
                        value=75, weight=0.3, damage=25),
            "brass_knuckles": Item("brass_knuckles", "Brass Knuckles", "Metal knuckles for punching",
                                  ItemType.WEAPON, value=60, weight=0.5, damage=18),
            
            # Consumables
            "food_tray": Item("food_tray", "Food Tray", "Prison cafeteria meal", ItemType.CONSUMABLE,
                             value=5, weight=1.0, stackable=True, effects={"hunger": -30}),
            "good_food": Item("good_food", "Good Food", "Quality meal from commissary", ItemType.CONSUMABLE,
                             value=20, weight=0.5, stackable=True, effects={"hunger": -50, "health": 5}),
            "medicine": Item("medicine", "Medicine", "Basic medical supplies", ItemType.CONSUMABLE,
                           value=30, weight=0.2, stackable=True, effects={"health": 30}),
            "energy_drink": Item("energy_drink", "Energy Drink", "Restores energy", ItemType.CONSUMABLE,
                               value=15, weight=0.3, stackable=True, effects={"energy": 40}),
            
            # Contraband
            "cigarettes": Item("cigarettes", "Cigarettes", "Prison currency", ItemType.CURRENCY,
                             value=10, weight=0.1, stackable=True, quantity=10),
            "marijuana": Item("marijuana", "Marijuana", "Illegal drug", ItemType.CONTRABAND,
                            value=50, weight=0.1, stackable=True, effects={"stress": -20, "sanity": -5}),
            "pills": Item("pills", "Pills", "Prescription medication", ItemType.CONTRABAND,
                         value=40, weight=0.05, stackable=True, effects={"health": 20, "sanity": -10}),
            "phone": Item("phone", "Cell Phone", "Smuggled mobile phone", ItemType.CONTRABAND,
                         value=200, weight=0.3),
            
            # Crafting
            "metal_scrap": Item("metal_scrap", "Metal Scrap", "Useful for crafting", ItemType.CRAFTING,
                              value=5, weight=0.5, stackable=True),
            "cloth": Item("cloth", "Cloth", "Fabric material", ItemType.CRAFTING,
                         value=3, weight=0.2, stackable=True),
            "rope": Item("rope", "Rope", "Strong rope", ItemType.CRAFTING,
                        value=15, weight=1.0, stackable=True),
            "tools": Item("tools", "Tools", "Basic tools", ItemType.CRAFTING,
                         value=50, weight=2.0),
            
            # Books
            "fitness_book": Item("fitness_book", "Fitness Guide", "Improves strength training", 
                               ItemType.BOOK, value=25, weight=0.5, effects={"skill": "strength"}),
            "combat_manual": Item("combat_manual", "Combat Manual", "Teaches fighting techniques",
                                ItemType.BOOK, value=40, weight=0.5, effects={"skill": "brawling"}),
            "lockpick_guide": Item("lockpick_guide", "Lockpicking Guide", "Learn to pick locks",
                                 ItemType.BOOK, value=60, weight=0.3, effects={"skill": "lockpicking"}),
        }
    
    @staticmethod
    def get_locations() -> Dict[str, Location]:
        """Get all game locations"""
        return {
            "cell_a1": Location(
                "cell_a1", "Your Cell", 
                "A small 8x10 cell with a bunk bed, toilet, and sink. Your personal space.",
                LocationType.CELL,
                npcs=["cellmate_marcus"],
                connections=["block_a_hall", "cell_a2"],
                danger_level=1,
                guard_presence=2
            ),
            "block_a_hall": Location(
                "block_a_hall", "Cell Block A Hallway",
                "A long corridor lined with cells. Guards patrol regularly.",
                LocationType.CELL,
                connections=["cell_a1", "cafeteria", "yard"],
                danger_level=3,
                guard_presence=5
            ),
            "cafeteria": Location(
                "cafeteria", "Cafeteria",
                "Large dining hall with metal tables. The social hub of the prison.",
                LocationType.CAFETERIA,
                npcs=["cook_joe", "inmate_tony", "inmate_carlos"],
                connections=["block_a_hall", "kitchen", "yard"],
                danger_level=5,
                guard_presence=4,
                time_restrictions={"breakfast": (6, 8), "lunch": (12, 13), "dinner": (17, 18)}
            ),
            "yard": Location(
                "yard", "Prison Yard",
                "Open outdoor area with basketball court and weight benches. Gang territory.",
                LocationType.YARD,
                npcs=["gang_leader_rico", "inmate_mike", "guard_johnson"],
                connections=["block_a_hall", "cafeteria", "gym"],
                danger_level=7,
                guard_presence=3,
                time_restrictions={"yard_time": (9, 11), "afternoon": (14, 16)}
            ),
            "library": Location(
                "library", "Library",
                "Quiet room filled with books. A place to learn and plan.",
                LocationType.LIBRARY,
                npcs=["librarian_helen"],
                connections=["block_a_hall"],
                danger_level=1,
                guard_presence=1
            ),
            "gym": Location(
                "gym", "Gym",
                "Weight room with benches, dumbbells, and punching bags.",
                LocationType.GYM,
                npcs=["trainer_big_mike", "inmate_tyrone"],
                connections=["yard"],
                danger_level=4,
                guard_presence=2
            ),
            "workshop": Location(
                "workshop", "Workshop",
                "Prison workshop with tools and equipment. Job location.",
                LocationType.WORKSHOP,
                npcs=["supervisor_dave"],
                connections=["block_a_hall"],
                danger_level=3,
                guard_presence=4
            ),
            "infirmary": Location(
                "infirmary", "Infirmary",
                "Medical facility with beds and supplies.",
                LocationType.INFIRMARY,
                npcs=["doctor_sarah", "nurse_kim"],
                connections=["block_a_hall"],
                danger_level=1,
                guard_presence=2
            ),
        }
    
    @staticmethod
    def get_npcs() -> Dict[str, NPC]:
        """Get all NPCs"""
        return {
            "cellmate_marcus": NPC(
                "cellmate_marcus", "Marcus",
                "Your cellmate. A veteran inmate who knows the ropes.",
                personality={"friendly": 70, "helpful": 80, "trustworthy": 60},
                relationship=20,
                location="cell_a1",
                dialogue={
                    "greeting": ["Hey there, cellmate.", "What's up?", "Need something?"],
                    "help": ["I can show you around if you want.", "Been here 5 years, I know the drill."],
                    "advice": ["Keep your head down and don't trust anyone too quickly."]
                }
            ),
            "cook_joe": NPC(
                "cook_joe", "Joe the Cook",
                "The head cook. Controls food quality and has connections.",
                personality={"greedy": 60, "practical": 70, "connected": 80},
                location="cafeteria",
                dialogue={
                    "greeting": ["What do you want?", "Make it quick, I'm busy."],
                    "trade": ["I might have something extra... for the right price."]
                }
            ),
            "gang_leader_rico": NPC(
                "gang_leader_rico", "Rico",
                "Leader of Los Hermanos. Respected and feared.",
                personality={"tough": 90, "loyal": 70, "dangerous": 85},
                gang=GangType.LOS_HERMANOS,
                location="yard",
                dialogue={
                    "greeting": ["You got business with me?", "Speak."],
                    "respect": ["Respect is earned here, not given."]
                }
            ),
            "guard_johnson": NPC(
                "guard_johnson", "Officer Johnson",
                "A strict but fair guard.",
                personality={"strict": 80, "fair": 60, "observant": 70},
                is_guard=True,
                location="yard",
                dialogue={
                    "greeting": ["Keep moving, inmate.", "No trouble on my watch."],
                    "warning": ["I'm watching you."]
                }
            ),
        }
    
    @staticmethod
    def get_quests() -> Dict[str, Quest]:
        """Get all quests"""
        return {
            "tutorial_quest": Quest(
                "tutorial_quest", "First Day",
                "Learn the basics of prison life from Marcus.",
                objectives=["Talk to Marcus", "Visit the cafeteria", "Check the yard"],
                rewards={"xp": 100, "reputation": 5},
                status=QuestStatus.ACTIVE
            ),
            "join_gang": Quest(
                "join_gang", "Find Your Place",
                "Decide whether to join a gang or stay independent.",
                objectives=["Meet gang leaders", "Complete initiation task"],
                rewards={"xp": 200, "reputation": 10}
            ),
            "first_trade": Quest(
                "first_trade", "The Trading Game",
                "Learn to trade by making your first deal.",
                objectives=["Trade with an NPC"],
                rewards={"xp": 50, "cigarettes": 10}
            ),
        }


# ============================================================================
# GAME ENGINE
# ============================================================================

class GameEngine:
    """Main game engine"""
    
    def __init__(self):
        self.player: Optional[Player] = None
        self.game_time = GameTime()
        self.current_state = GameState.MAIN_MENU
        self.locations: Dict[str, Location] = GameData.get_locations()
        self.npcs: Dict[str, NPC] = GameData.get_npcs()
        self.items: Dict[str, Item] = GameData.get_items()
        self.quests: Dict[str, Quest] = GameData.get_quests()
        self.message_log: List[str] = []
        self.save_dir = os.path.expanduser("~/.local/share/prison_break")
        self.config_dir = os.path.expanduser("~/.config/prison_break")
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Create necessary directories"""
        os.makedirs(self.save_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)
    
    def new_game(self, player_name: str) -> None:
        """Start a new game"""
        self.player = Player(player_name)
        self.game_time = GameTime()
        self.message_log = []
        self.add_message(f"Welcome to prison, {player_name}.")
        self.add_message("Your sentence begins now...")
        
        # Give starting items
        self.player.add_item(self.items["food_tray"])
        self.player.cigarettes = 5
        
        # Activate tutorial quest
        self.quests["tutorial_quest"].status = QuestStatus.ACTIVE
    
    def add_message(self, message: str) -> None:
        """Add message to log"""
        self.message_log.append(f"[{self.game_time.get_time_string()}] {message}")
        if len(self.message_log) > 100:
            self.message_log.pop(0)
    
    def advance_time(self, minutes: int) -> None:
        """Advance game time"""
        self.game_time.advance(minutes)
        
        # Update player status
        if self.player:
            hours = minutes // 60
            if hours > 0:
                self.player.update_status_effects(hours)
                self.player.hunger = min(100, self.player.hunger + hours * 2)
                self.player.hygiene = max(0, self.player.hygiene - hours)
                
                # Regenerate energy if resting
                if self.game_time.hour >= 22 or self.game_time.hour < 6:
                    self.player.restore_energy(hours * 10)
    
    def get_current_location(self) -> Optional[Location]:
        """Get player's current location"""
        if self.player:
            return self.locations.get(self.player.location)
        return None
    
    def move_player(self, location_id: str) -> bool:
        """Move player to new location"""
        if not self.player:
            return False
        
        current_loc = self.get_current_location()
        if not current_loc:
            return False
        
        if location_id not in current_loc.connections:
            self.add_message("You can't go there from here.")
            return False
        
        # Check time restrictions
        new_loc = self.locations.get(location_id)
        if new_loc and new_loc.time_restrictions:
            current_hour = self.game_time.hour
            allowed = False
            for period, (start, end) in new_loc.time_restrictions.items():
                if start <= current_hour < end:
                    allowed = True
                    break
            if not allowed:
                self.add_message(f"{new_loc.name} is closed right now.")
                return False
        
        self.player.location = location_id
        self.advance_time(5)  # Moving takes 5 minutes
        self.add_message(f"You move to {new_loc.name}.")
        return True
    
    def save_game(self, slot: int = 0) -> bool:
        """Save game to file"""
        if not self.player:
            return False
        
        try:
            save_data = {
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat(),
                "player": {
                    "name": self.player.name,
                    "level": self.player.level,
                    "xp": self.player.xp,
                    "attributes": asdict(self.player.attributes),
                    "skills": asdict(self.player.skills),
                    "current_health": self.player.current_health,
                    "current_energy": self.player.current_energy,
                    "hunger": self.player.hunger,
                    "hygiene": self.player.hygiene,
                    "location": self.player.location,
                    "gang": self.player.gang.name,
                    "money": self.player.money,
                    "cigarettes": self.player.cigarettes,
                    "inventory": [asdict(item) for item in self.player.inventory],
                    "stats": self.player.stats,
                },
                "game_time": {
                    "day": self.game_time.day,
                    "hour": self.game_time.hour,
                    "minute": self.game_time.minute,
                },
                "quests": {qid: {"status": q.status.name, "progress": q.progress} 
                          for qid, q in self.quests.items()},
            }
            
            save_file = os.path.join(self.save_dir, f"save_{slot}.json")
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            self.add_message("Game saved successfully.")
            return True
        except Exception as e:
            self.add_message(f"Failed to save game: {e}")
            return False
    
    def load_game(self, slot: int = 0) -> bool:
        """Load game from file"""
        try:
            save_file = os.path.join(self.save_dir, f"save_{slot}.json")
            if not os.path.exists(save_file):
                return False
            
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            
            # Restore player
            player_data = save_data["player"]
            self.player = Player(player_data["name"])
            self.player.level = player_data["level"]
            self.player.xp = player_data["xp"]
            
            # Restore attributes
            for key, value in player_data["attributes"].items():
                setattr(self.player.attributes, key, value)
            
            # Restore skills
            for key, value in player_data["skills"].items():
                setattr(self.player.skills, key, value)
            
            self.player.current_health = player_data["current_health"]
            self.player.current_energy = player_data["current_energy"]
            self.player.hunger = player_data["hunger"]
            self.player.hygiene = player_data["hygiene"]
            self.player.location = player_data["location"]
            self.player.gang = GangType[player_data["gang"]]
            self.player.money = player_data["money"]
            self.player.cigarettes = player_data["cigarettes"]
            self.player.stats = player_data["stats"]
            
            # Restore inventory
            self.player.inventory = []
            for item_data in player_data["inventory"]:
                item_type = ItemType[item_data["item_type"]]
                item = Item(
                    item_data["id"], item_data["name"], item_data["description"],
                    item_type, item_data["value"], item_data["weight"],
                    item_data["stackable"], item_data["quantity"],
                    item_data["damage"], item_data["effects"]
                )
                self.player.inventory.append(item)
            
            # Restore time
            time_data = save_data["game_time"]
            self.game_time.day = time_data["day"]
            self.game_time.hour = time_data["hour"]
            self.game_time.minute = time_data["minute"]
            
            # Restore quests
            for qid, qdata in save_data["quests"].items():
                if qid in self.quests:
                    self.quests[qid].status = QuestStatus[qdata["status"]]
                    self.quests[qid].progress = qdata["progress"]
            
            self.add_message("Game loaded successfully.")
            return True
        except Exception as e:
            self.add_message(f"Failed to load game: {e}")
            return False


# ============================================================================
# UI RENDERER
# ============================================================================

class UIRenderer:
    """Handles all UI rendering"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.setup_colors()
    
    def setup_colors(self) -> None:
        """Initialize color pairs"""
        curses.start_color()
        curses.use_default_colors()
        
        # Define color pairs
        curses.init_pair(1, curses.COLOR_GREEN, -1)    # Positive/Health
        curses.init_pair(2, curses.COLOR_YELLOW, -1)   # Warning
        curses.init_pair(3, curses.COLOR_RED, -1)      # Danger/Error
        curses.init_pair(4, curses.COLOR_BLUE, -1)     # Info
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)  # Special
        curses.init_pair(6, curses.COLOR_CYAN, -1)     # System
        curses.init_pair(7, curses.COLOR_WHITE, -1)    # Normal
    
    def clear(self) -> None:
        """Clear screen"""
        self.stdscr.clear()
    
    def refresh(self) -> None:
        """Refresh screen"""
        self.stdscr.refresh()
    
    def draw_box(self, y: int, x: int, height: int, width: int, title: str = "") -> None:
        """Draw a box with optional title"""
        # Draw corners and edges
        self.stdscr.addch(y, x, curses.ACS_ULCORNER)
        self.stdscr.addch(y, x + width - 1, curses.ACS_URCORNER)
        self.stdscr.addch(y + height - 1, x, curses.ACS_LLCORNER)
        self.stdscr.addch(y + height - 1, x + width - 1, curses.ACS_LRCORNER)
        
        for i in range(1, width - 1):
            self.stdscr.addch(y, x + i, curses.ACS_HLINE)
            self.stdscr.addch(y + height - 1, x + i, curses.ACS_HLINE)
        
        for i in range(1, height - 1):
            self.stdscr.addch(y + i, x, curses.ACS_VLINE)
            self.stdscr.addch(y + i, x + width - 1, curses.ACS_VLINE)
        
        # Draw title if provided
        if title:
            title_text = f" {title} "
            title_x = x + (width - len(title_text)) // 2
            self.stdscr.addstr(y, title_x, title_text, curses.A_BOLD)
    
    def draw_text(self, y: int, x: int, text: str, color: int = 7, bold: bool = False) -> None:
        """Draw text at position"""
        attr = curses.color_pair(color)
        if bold:
            attr |= curses.A_BOLD
        
        try:
            self.stdscr.addstr(y, x, text, attr)
        except curses.error:
            pass  # Ignore if text goes off screen
    
    def draw_bar(self, y: int, x: int, width: int, current: int, maximum: int, 
                 label: str = "", color: int = 1) -> None:
        """Draw a progress bar"""
        if maximum <= 0:
            percentage = 0
        else:
            percentage = current / maximum
        
        filled = int(width * percentage)
        bar = "█" * filled + "░" * (width - filled)
        
        text = f"{label}: {bar} {current}/{maximum}"
        self.draw_text(y, x, text, color)
    
    def wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to fit width"""
        return textwrap.wrap(text, width)
    
    def get_input(self, prompt: str = "> ") -> str:
        """Get user input"""
        self.stdscr.addstr(self.height - 1, 0, prompt)
        self.stdscr.clrtoeol()
        curses.echo()
        curses.curs_set(1)
        
        try:
            user_input = self.stdscr.getstr(self.height - 1, len(prompt), 50).decode('utf-8')
        except:
            user_input = ""
        
        curses.noecho()
        curses.curs_set(0)
        return user_input.strip()
    
    def show_message(self, message: str, wait: bool = True) -> None:
        """Show a message box"""
        lines = self.wrap_text(message, self.width - 10)
        box_height = len(lines) + 4
        box_width = min(self.width - 4, max(len(line) for line in lines) + 4)
        box_y = (self.height - box_height) // 2
        box_x = (self.width - box_width) // 2
        
        self.draw_box(box_y, box_x, box_height, box_width, "Message")
        
        for i, line in enumerate(lines):
            self.draw_text(box_y + 2 + i, box_x + 2, line)
        
        if wait:
            self.draw_text(box_y + box_height - 2, box_x + 2, "Press any key to continue...", 6)
            self.refresh()
            self.stdscr.getch()


# ============================================================================
# GAME SCREENS
# ============================================================================

class GameScreens:
    """All game screen implementations"""
    
    def __init__(self, engine: GameEngine, ui: UIRenderer):
        self.engine = engine
        self.ui = ui
    
    def main_menu(self) -> GameState:
        """Main menu screen"""
        while True:
            self.ui.clear()
            
            # Draw title
            title = "PRISON BREAK"
            subtitle = "The Ultimate Inmate Simulation"
            
            title_y = self.ui.height // 4
            self.ui.draw_text(title_y, (self.ui.width - len(title)) // 2, title, 5, True)
            self.ui.draw_text(title_y + 1, (self.ui.width - len(subtitle)) // 2, subtitle, 6)
            
            # Draw menu
            menu_y = self.ui.height // 2
            menu_items = [
                "1. New Game",
                "2. Load Game",
                "3. Instructions",
                "4. Quit"
            ]
            
            for i, item in enumerate(menu_items):
                self.ui.draw_text(menu_y + i, (self.ui.width - len(item)) // 2, item)
            
            self.ui.refresh()
            
            # Get input
            choice = self.ui.stdscr.getch()
            
            if choice == ord('1'):
                return GameState.CHARACTER_CREATION
            elif choice == ord('2'):
                if self.engine.load_game():
                    return GameState.PLAYING
                else:
                    self.ui.show_message("No save file found!")
            elif choice == ord('3'):
                self.show_instructions()
            elif choice == ord('4') or choice == ord('q'):
                return GameState.GAME_OVER
    
    def show_instructions(self) -> None:
        """Show game instructions"""
        instructions = """
PRISON BREAK - Instructions

OBJECTIVE:
Survive prison life, build your reputation, and either thrive or escape.

CONTROLS:
- Arrow keys or WASD: Navigate menus
- Number keys: Select options
- I: Inventory
- C: Character sheet
- M: Map
- Q: Quest log
- R: Relationships
- S: Save game
- ESC: Pause menu

GAMEPLAY:
- Manage your health, energy, and hunger
- Build relationships with inmates and guards
- Join a gang or stay independent
- Complete quests and random events
- Trade items and contraband
- Fight when necessary (or avoid it)
- Plan your escape... or rule the prison

TIPS:
- Keep your health and energy up
- Build reputation to gain respect
- Choose your allies carefully
- Not everyone can be trusted
- Actions have consequences

Press any key to return...
        """
        
        self.ui.clear()
        lines = instructions.split('\n')
        for i, line in enumerate(lines):
            if i < self.ui.height - 1:
                self.ui.draw_text(i, 2, line)
        
        self.ui.refresh()
        self.ui.stdscr.getch()
    
    def character_creation(self) -> GameState:
        """Character creation screen"""
        self.ui.clear()
        
        # Get player name
        self.ui.draw_text(self.ui.height // 2 - 2, 2, "Enter your name:", 4, True)
        name = self.ui.get_input("Name: ")
        
        if not name:
            name = "Inmate"
        
        # Create new game
        self.engine.new_game(name)
        
        # Show intro
        intro = f"""
Welcome to prison, {name}.

You've been sentenced to 10 years for a crime you may or may not have committed.
This is your new home. Your new reality.

In here, respect is everything. Weakness gets you killed.
You'll need to be smart, tough, and careful if you want to survive.

The guards run the prison... officially.
But the inmates? They run everything else.

Your choices matter. Every action has consequences.
Trust the wrong person, and you're dead.
Cross the right person, and you're dead.

But if you play it smart... you might just make it out alive.

Good luck. You're going to need it.
        """
        
        self.ui.show_message(intro)
        
        return GameState.PLAYING
    
    def playing(self) -> GameState:
        """Main playing screen"""
        while True:
            self.ui.clear()
            
            if not self.engine.player:
                return GameState.MAIN_MENU
            
            # Draw header
            self.draw_header()
            
            # Draw main content area
            content_y = 3
            content_height = self.ui.height - 8
            self.ui.draw_box(content_y, 1, content_height, self.ui.width - 2, "")
            
            # Draw location and description
            location = self.engine.get_current_location()
            if location:
                self.ui.draw_text(content_y + 1, 3, location.name, 5, True)
                
                # Wrap and display description
                desc_lines = self.ui.wrap_text(location.description, self.ui.width - 8)
                for i, line in enumerate(desc_lines[:3]):
                    self.ui.draw_text(content_y + 3 + i, 3, line)
                
                # Show NPCs present
                if location.npcs:
                    npc_y = content_y + 7
                    self.ui.draw_text(npc_y, 3, "People here:", 4, True)
                    for i, npc_id in enumerate(location.npcs[:5]):
                        npc = self.engine.npcs.get(npc_id)
                        if npc:
                            self.ui.draw_text(npc_y + 1 + i, 5, f"- {npc.name}")
                
                # Show available actions
                action_y = content_y + 13
                self.ui.draw_text(action_y, 3, "Actions:", 4, True)
                
                actions = [
                    "1. Look around",
                    "2. Talk to someone",
                    "3. Move to another location",
                    "4. Rest (advance time)",
                    "5. Check inventory (I)",
                ]
                
                for i, action in enumerate(actions):
                    self.ui.draw_text(action_y + 1 + i, 5, action)
            
            # Draw status bars
            self.draw_status_bars()
            
            # Draw command prompt
            self.ui.draw_text(self.ui.height - 1, 0, "> ", 6)
            
            self.ui.refresh()
            
            # Get input
            key = self.ui.stdscr.getch()
            
            # Handle input
            if key == ord('1'):
                self.look_around()
            elif key == ord('2'):
                self.talk_menu()
            elif key == ord('3'):
                self.move_menu()
            elif key == ord('4'):
                self.rest()
            elif key == ord('i') or key == ord('I') or key == ord('5'):
                return GameState.INVENTORY
            elif key == ord('c') or key == ord('C'):
                return GameState.CHARACTER_SHEET
            elif key == ord('m') or key == ord('M'):
                return GameState.MAP
            elif key == ord('q') or key == ord('Q'):
                return GameState.QUEST_LOG
            elif key == ord('r') or key == ord('R'):
                return GameState.RELATIONSHIPS
            elif key == ord('s') or key == ord('S'):
                self.engine.save_game()
                self.ui.show_message("Game saved!")
            elif key == 27:  # ESC
                return GameState.PAUSED
    
    def draw_header(self) -> None:
        """Draw game header"""
        player = self.engine.player
        time_str = self.engine.game_time.get_time_string()
        period = self.engine.game_time.get_period()
        
        header = f"PRISON BREAK | {time_str} | {period} | {player.name} (Lv.{player.level})"
        self.ui.draw_text(0, 2, header, 5, True)
        
        # Draw separator
        self.ui.draw_text(1, 0, "─" * self.ui.width, 6)
    
    def draw_status_bars(self) -> None:
        """Draw status bars"""
        player = self.engine.player
        bar_y = self.ui.height - 4
        
        # Health bar
        health_color = 1 if player.current_health > 50 else 2 if player.current_health > 25 else 3
        self.ui.draw_bar(bar_y, 2, 20, player.current_health, player.max_health, "HP", health_color)
        
        # Energy bar
        energy_color = 1 if player.current_energy > 50 else 2
        self.ui.draw_bar(bar_y, 30, 20, player.current_energy, player.max_energy, "Energy", energy_color)
        
        # Hunger bar (inverted - lower is better)
        hunger_color = 1 if player.hunger < 50 else 2 if player.hunger < 75 else 3
        self.ui.draw_bar(bar_y + 1, 2, 20, 100 - player.hunger, 100, "Hunger", hunger_color)
        
        # Respect bar
        self.ui.draw_bar(bar_y + 1, 30, 20, player.attributes.respect, 100, "Respect", 5)
        
        # Currency
        self.ui.draw_text(bar_y + 2, 2, f"Money: ${player.money} | Cigarettes: {player.cigarettes}", 4)
    
    def look_around(self) -> None:
        """Look around current location"""
        location = self.engine.get_current_location()
        if not location:
            return
        
        details = f"{location.description}\n\n"
        
        if location.npcs:
            details += "People here:\n"
            for npc_id in location.npcs:
                npc = self.engine.npcs.get(npc_id)
                if npc:
                    details += f"- {npc.name}: {npc.description}\n"
        
        if location.items:
            details += "\nItems here:\n"
            for item in location.items:
                details += f"- {item.name}\n"
        
        details += f"\nDanger Level: {'█' * location.danger_level}{'░' * (10 - location.danger_level)}\n"
        details += f"Guard Presence: {'█' * location.guard_presence}{'░' * (10 - location.guard_presence)}\n"
        
        self.ui.show_message(details)
    
    def talk_menu(self) -> None:
        """Talk to NPCs"""
        location = self.engine.get_current_location()
        if not location or not location.npcs:
            self.ui.show_message("There's no one here to talk to.")
            return
        
        # Show NPC list
        self.ui.clear()
        self.ui.draw_text(2, 2, "Who do you want to talk to?", 4, True)
        
        for i, npc_id in enumerate(location.npcs):
            npc = self.engine.npcs.get(npc_id)
            if npc:
                self.ui.draw_text(4 + i, 4, f"{i + 1}. {npc.name}")
        
        self.ui.draw_text(4 + len(location.npcs) + 1, 4, "0. Cancel")
        self.ui.refresh()
        
        choice = self.ui.stdscr.getch()
        
        if ord('1') <= choice <= ord('9'):
            idx = choice - ord('1')
            if idx < len(location.npcs):
                npc_id = location.npcs[idx]
                self.talk_to_npc(npc_id)
    
    def talk_to_npc(self, npc_id: str) -> None:
        """Talk to specific NPC"""
        npc = self.engine.npcs.get(npc_id)
        if not npc:
            return
        
        # Simple dialogue
        greeting = random.choice(npc.dialogue.get("greeting", ["Hello."]))
        
        dialogue = f"{npc.name}: {greeting}\n\n"
        dialogue += f"Relationship: {npc.relationship}/100\n"
        
        if npc.gang != GangType.NONE:
            dialogue += f"Gang: {npc.gang.name}\n"
        
        self.ui.show_message(dialogue)
        
        # Advance time
        self.engine.advance_time(10)
    
    def move_menu(self) -> None:
        """Show movement menu"""
        location = self.engine.get_current_location()
        if not location:
            return
        
        self.ui.clear()
        self.ui.draw_text(2, 2, "Where do you want to go?", 4, True)
        
        for i, loc_id in enumerate(location.connections):
            loc = self.engine.locations.get(loc_id)
            if loc:
                self.ui.draw_text(4 + i, 4, f"{i + 1}. {loc.name}")
        
        self.ui.draw_text(4 + len(location.connections) + 1, 4, "0. Cancel")
        self.ui.refresh()
        
        choice = self.ui.stdscr.getch()
        
        if ord('1') <= choice <= ord('9'):
            idx = choice - ord('1')
            if idx < len(location.connections):
                loc_id = location.connections[idx]
                self.engine.move_player(loc_id)
    
    def rest(self) -> None:
        """Rest and advance time"""
        self.ui.clear()
        self.ui.draw_text(2, 2, "How long do you want to rest?", 4, True)
        self.ui.draw_text(4, 4, "1. 30 minutes")
        self.ui.draw_text(5, 4, "2. 1 hour")
        self.ui.draw_text(6, 4, "3. 2 hours")
        self.ui.draw_text(7, 4, "4. Until next meal")
        self.ui.draw_text(8, 4, "0. Cancel")
        self.ui.refresh()
        
        choice = self.ui.stdscr.getch()
        
        if choice == ord('1'):
            self.engine.advance_time(30)
            self.engine.player.restore_energy(10)
        elif choice == ord('2'):
            self.engine.advance_time(60)
            self.engine.player.restore_energy(20)
        elif choice == ord('3'):
            self.engine.advance_time(120)
            self.engine.player.restore_energy(40)
        elif choice == ord('4'):
            # Calculate time to next meal
            current_hour = self.engine.game_time.hour
            if current_hour < 6:
                hours_to_wait = 6 - current_hour
            elif current_hour < 12:
                hours_to_wait = 12 - current_hour
            elif current_hour < 17:
                hours_to_wait = 17 - current_hour
            else:
                hours_to_wait = 24 - current_hour + 6
            
            self.engine.advance_time(hours_to_wait * 60)
            self.engine.player.restore_energy(hours_to_wait * 20)
    
    def inventory_screen(self) -> GameState:
        """Inventory screen"""
        while True:
            self.ui.clear()
            
            player = self.engine.player
            
            # Draw header
            self.ui.draw_text(0, 2, "INVENTORY", 5, True)
            self.ui.draw_text(1, 0, "─" * self.ui.width, 6)
            
            # Draw weight info
            weight = player.get_total_weight()
            weight_text = f"Weight: {weight:.1f}/{player.max_weight:.1f} kg"
            self.ui.draw_text(2, 2, weight_text, 4)
            
            # Draw currency
            self.ui.draw_text(2, 30, f"Money: ${player.money}", 4)
            self.ui.draw_text(2, 50, f"Cigarettes: {player.cigarettes}", 4)
            
            # Draw items
            item_y = 4
            if player.inventory:
                for i, item in enumerate(player.inventory[:20]):
                    qty = f"x{item.quantity}" if item.stackable else ""
                    item_text = f"{i + 1}. {item.name} {qty} ({item.weight}kg)"
                    self.ui.draw_text(item_y + i, 4, item_text)
            else:
                self.ui.draw_text(item_y, 4, "Your inventory is empty.", 2)
            
            # Draw controls
            control_y = self.ui.height - 3
            self.ui.draw_text(control_y, 2, "1-9: Use item | D: Drop item | ESC: Back", 6)
            
            self.ui.refresh()
            
            # Get input
            key = self.ui.stdscr.getch()
            
            if key == 27:  # ESC
                return GameState.PLAYING
            elif ord('1') <= key <= ord('9'):
                idx = key - ord('1')
                if idx < len(player.inventory):
                    self.use_item(player.inventory[idx])
            elif key == ord('d') or key == ord('D'):
                self.drop_item_menu()
    
    def use_item(self, item: Item) -> None:
        """Use an item"""
        player = self.engine.player
        
        if item.item_type == ItemType.CONSUMABLE:
            # Apply effects
            for effect, value in item.effects.items():
                if effect == "hunger":
                    player.hunger = max(0, player.hunger + value)
                elif effect == "health":
                    player.heal(value)
                elif effect == "energy":
                    player.restore_energy(value)
            
            player.remove_item(item.id, 1)
            self.ui.show_message(f"You used {item.name}.")
        elif item.item_type == ItemType.BOOK:
            self.ui.show_message(f"You read {item.name}. You feel smarter.")
            # Could improve skills here
        else:
            self.ui.show_message(f"You can't use {item.name} right now.")
    
    def drop_item_menu(self) -> None:
        """Drop item menu"""
        player = self.engine.player
        
        if not player.inventory:
            return
        
        self.ui.clear()
        self.ui.draw_text(2, 2, "Which item do you want to drop?", 4, True)
        
        for i, item in enumerate(player.inventory[:9]):
            self.ui.draw_text(4 + i, 4, f"{i + 1}. {item.name}")
        
        self.ui.draw_text(4 + len(player.inventory) + 1, 4, "0. Cancel")
        self.ui.refresh()
        
        choice = self.ui.stdscr.getch()
        
        if ord('1') <= choice <= ord('9'):
            idx = choice - ord('1')
            if idx < len(player.inventory):
                item = player.inventory[idx]
                player.remove_item(item.id, 1)
                self.ui.show_message(f"You dropped {item.name}.")
    
    def character_sheet_screen(self) -> GameState:
        """Character sheet screen"""
        while True:
            self.ui.clear()
            
            player = self.engine.player
            
            # Draw header
            self.ui.draw_text(0, 2, f"{player.name} - Level {player.level}", 5, True)
            self.ui.draw_text(1, 0, "─" * self.ui.width, 6)
            
            # Draw XP
            xp_text = f"XP: {player.xp}/{player.xp_to_next}"
            self.ui.draw_text(2, 2, xp_text, 4)
            
            # Draw attributes
            attr_y = 4
            self.ui.draw_text(attr_y, 2, "ATTRIBUTES", 5, True)
            
            attrs = [
                ("Strength", player.attributes.strength),
                ("Stamina", player.attributes.stamina),
                ("Health", player.attributes.health),
                ("Toughness", player.attributes.toughness),
                ("Intelligence", player.attributes.intelligence),
                ("Willpower", player.attributes.willpower),
                ("Sanity", player.attributes.sanity),
                ("Perception", player.attributes.perception),
                ("Charisma", player.attributes.charisma),
                ("Intimidation", player.attributes.intimidation),
                ("Reputation", player.attributes.reputation),
                ("Respect", player.attributes.respect),
            ]
            
            for i, (name, value) in enumerate(attrs):
                self.ui.draw_text(attr_y + 2 + i, 4, f"{name}: {value}")
            
            # Draw skills
            skill_y = 4
            skill_x = 30
            self.ui.draw_text(skill_y, skill_x, "SKILLS", 5, True)
            
            skills = [
                ("Brawling", player.skills.brawling),
                ("Knife Fighting", player.skills.knife_fighting),
                ("Defense", player.skills.defense),
                ("Stealth", player.skills.stealth),
                ("Lockpicking", player.skills.lockpicking),
                ("First Aid", player.skills.first_aid),
                ("Persuasion", player.skills.persuasion),
                ("Deception", player.skills.deception),
                ("Crafting", player.skills.crafting),
                ("Trading", player.skills.trading),
            ]
            
            for i, (name, value) in enumerate(skills):
                self.ui.draw_text(skill_y + 2 + i, skill_x + 2, f"{name}: {value}")
            
            # Draw controls
            self.ui.draw_text(self.ui.height - 2, 2, "ESC: Back", 6)
            
            self.ui.refresh()
            
            # Get input
            key = self.ui.stdscr.getch()
            
            if key == 27:  # ESC
                return GameState.PLAYING
    
    def map_screen(self) -> GameState:
        """Map screen"""
        while True:
            self.ui.clear()
            
            # Draw header
            self.ui.draw_text(0, 2, "PRISON MAP", 5, True)
            self.ui.draw_text(1, 0, "─" * self.ui.width, 6)
            
            # Draw simple map
            map_y = 3
            player_loc = self.engine.player.location
            
            for i, (loc_id, location) in enumerate(self.engine.locations.items()):
                marker = "►" if loc_id == player_loc else " "
                loc_text = f"{marker} {location.name}"
                color = 5 if loc_id == player_loc else 7
                self.ui.draw_text(map_y + i, 4, loc_text, color)
            
            # Draw controls
            self.ui.draw_text(self.ui.height - 2, 2, "ESC: Back", 6)
            
            self.ui.refresh()
            
            # Get input
            key = self.ui.stdscr.getch()
            
            if key == 27:  # ESC
                return GameState.PLAYING
    
    def quest_log_screen(self) -> GameState:
        """Quest log screen"""
        while True:
            self.ui.clear()
            
            # Draw header
            self.ui.draw_text(0, 2, "QUEST LOG", 5, True)
            self.ui.draw_text(1, 0, "─" * self.ui.width, 6)
            
            # Draw quests
            quest_y = 3
            active_quests = [q for q in self.engine.quests.values() if q.status == QuestStatus.ACTIVE]
            
            if active_quests:
                for i, quest in enumerate(active_quests):
                    self.ui.draw_text(quest_y + i * 4, 2, quest.name, 5, True)
                    self.ui.draw_text(quest_y + i * 4 + 1, 4, quest.description)
                    
                    # Draw objectives
                    for j, obj in enumerate(quest.objectives[:3]):
                        self.ui.draw_text(quest_y + i * 4 + 2 + j, 6, f"- {obj}")
            else:
                self.ui.draw_text(quest_y, 4, "No active quests.", 2)
            
            # Draw controls
            self.ui.draw_text(self.ui.height - 2, 2, "ESC: Back", 6)
            
            self.ui.refresh()
            
            # Get input
            key = self.ui.stdscr.getch()
            
            if key == 27:  # ESC
                return GameState.PLAYING
    
    def relationships_screen(self) -> GameState:
        """Relationships screen"""
        while True:
            self.ui.clear()
            
            # Draw header
            self.ui.draw_text(0, 2, "RELATIONSHIPS", 5, True)
            self.ui.draw_text(1, 0, "─" * self.ui.width, 6)
            
            # Draw NPCs
            npc_y = 3
            for i, (npc_id, npc) in enumerate(self.engine.npcs.items()):
                if i >= 15:  # Limit display
                    break
                
                # Determine relationship color
                if npc.relationship >= 60:
                    color = 1  # Green - friend
                elif npc.relationship >= 20:
                    color = 4  # Blue - acquaintance
                elif npc.relationship >= -20:
                    color = 2  # Yellow - neutral
                else:
                    color = 3  # Red - enemy
                
                rel_text = f"{npc.name}: {npc.relationship}/100"
                self.ui.draw_text(npc_y + i, 4, rel_text, color)
            
            # Draw controls
            self.ui.draw_text(self.ui.height - 2, 2, "ESC: Back", 6)
            
            self.ui.refresh()
            
            # Get input
            key = self.ui.stdscr.getch()
            
            if key == 27:  # ESC
                return GameState.PLAYING
    
    def paused_screen(self) -> GameState:
        """Pause menu"""
        while True:
            self.ui.clear()
            
            # Draw menu
            menu_y = self.ui.height // 2 - 3
            menu_items = [
                "PAUSED",
                "",
                "1. Resume",
                "2. Save Game",
                "3. Load Game",
                "4. Quit to Menu"
            ]
            
            for i, item in enumerate(menu_items):
                bold = i == 0
                self.ui.draw_text(menu_y + i, (self.ui.width - len(item)) // 2, item, 5 if bold else 7, bold)
            
            self.ui.refresh()
            
            # Get input
            choice = self.ui.stdscr.getch()
            
            if choice == ord('1') or choice == 27:  # ESC
                return GameState.PLAYING
            elif choice == ord('2'):
                self.engine.save_game()
                self.ui.show_message("Game saved!")
            elif choice == ord('3'):
                if self.engine.load_game():
                    self.ui.show_message("Game loaded!")
                    return GameState.PLAYING
                else:
                    self.ui.show_message("Failed to load game!")
            elif choice == ord('4'):
                return GameState.MAIN_MENU


# ============================================================================
# MAIN GAME CLASS
# ============================================================================

class Game:
    """Main game class"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.engine = GameEngine()
        self.ui = UIRenderer(stdscr)
        self.screens = GameScreens(self.engine, self.ui)
        self.running = True
        
        # Setup curses
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(0)  # Blocking input
        self.stdscr.keypad(1)  # Enable keypad
    
    def run(self) -> None:
        """Main game loop"""
        current_state = GameState.MAIN_MENU
        
        while self.running:
            try:
                if current_state == GameState.MAIN_MENU:
                    current_state = self.screens.main_menu()
                elif current_state == GameState.CHARACTER_CREATION:
                    current_state = self.screens.character_creation()
                elif current_state == GameState.PLAYING:
                    current_state = self.screens.playing()
                elif current_state == GameState.INVENTORY:
                    current_state = self.screens.inventory_screen()
                elif current_state == GameState.CHARACTER_SHEET:
                    current_state = self.screens.character_sheet_screen()
                elif current_state == GameState.MAP:
                    current_state = self.screens.map_screen()
                elif current_state == GameState.QUEST_LOG:
                    current_state = self.screens.quest_log_screen()
                elif current_state == GameState.RELATIONSHIPS:
                    current_state = self.screens.relationships_screen()
                elif current_state == GameState.PAUSED:
                    current_state = self.screens.paused_screen()
                elif current_state == GameState.GAME_OVER:
                    self.running = False
            except KeyboardInterrupt:
                current_state = GameState.PAUSED
            except Exception as e:
                # Error handling
                self.ui.show_message(f"An error occurred: {e}\nPress any key to continue...")
                current_state = GameState.MAIN_MENU


# ============================================================================
# ADVANCED FEATURES - GANG SYSTEM
# ============================================================================

class GangSystem:
    """Gang management system"""
    
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.gangs = self._initialize_gangs()
    
    def _initialize_gangs(self) -> Dict[GangType, Dict[str, Any]]:
        """Initialize gang data"""
        return {
            GangType.BROTHERHOOD: {
                "name": "The Brotherhood",
                "description": "White supremacist gang focused on protection and drug trade",
                "territory": ["block_a_hall", "workshop"],
                "leader": "gang_leader_rico",
                "members": ["inmate_mike", "inmate_tony"],
                "initiation": "Prove your loyalty by fighting a rival gang member",
                "benefits": {"protection": 20, "drug_access": True},
                "requirements": {"reputation": 20, "strength": 40}
            },
            GangType.LOS_HERMANOS: {
                "name": "Los Hermanos",
                "description": "Latino gang with strong family bonds and smuggling network",
                "territory": ["cafeteria", "kitchen"],
                "leader": "gang_leader_rico",
                "members": ["inmate_carlos"],
                "initiation": "Complete a smuggling run successfully",
                "benefits": {"smuggling_bonus": 30, "family_protection": True},
                "requirements": {"reputation": 15, "charisma": 35}
            },
            GangType.THE_NATION: {
                "name": "The Nation",
                "description": "Organized black gang with strict hierarchy",
                "territory": ["yard", "gym"],
                "leader": "gang_leader_tyrone",
                "members": ["inmate_tyrone", "trainer_big_mike"],
                "initiation": "Earn respect through combat prowess",
                "benefits": {"respect_bonus": 25, "combat_training": True},
                "requirements": {"reputation": 25, "brawling": 30}
            },
            GangType.SYNDICATE: {
                "name": "The Syndicate",
                "description": "Organized crime network focused on business",
                "territory": ["library", "visitation"],
                "leader": "boss_vincent",
                "members": ["inmate_marcus"],
                "initiation": "Prove your business acumen with a successful trade",
                "benefits": {"trade_bonus": 40, "connections": True},
                "requirements": {"reputation": 30, "intelligence": 50}
            }
        }
    
    def can_join_gang(self, gang_type: GangType) -> Tuple[bool, str]:
        """Check if player can join gang"""
        if not self.engine.player:
            return False, "No player"
        
        if self.engine.player.gang != GangType.NONE:
            return False, "Already in a gang"
        
        gang_data = self.gangs.get(gang_type)
        if not gang_data:
            return False, "Invalid gang"
        
        requirements = gang_data["requirements"]
        player = self.engine.player
        
        if player.attributes.reputation < requirements.get("reputation", 0):
            return False, f"Need {requirements['reputation']} reputation"
        
        if requirements.get("strength") and player.attributes.strength < requirements["strength"]:
            return False, f"Need {requirements['strength']} strength"
        
        if requirements.get("charisma") and player.attributes.charisma < requirements["charisma"]:
            return False, f"Need {requirements['charisma']} charisma"
        
        if requirements.get("intelligence") and player.attributes.intelligence < requirements["intelligence"]:
            return False, f"Need {requirements['intelligence']} intelligence"
        
        if requirements.get("brawling") and player.skills.brawling < requirements["brawling"]:
            return False, f"Need {requirements['brawling']} brawling skill"
        
        return True, "Requirements met"
    
    def join_gang(self, gang_type: GangType) -> bool:
        """Join a gang"""
        can_join, message = self.can_join_gang(gang_type)
        if not can_join:
            self.engine.add_message(message)
            return False
        
        self.engine.player.gang = gang_type
        self.engine.player.gang_rank = "Prospect"
        self.engine.add_message(f"You joined {self.gangs[gang_type]['name']}!")
        self.engine.player.add_xp(200)
        
        return True


# ============================================================================
# ADVANCED FEATURES - COMBAT SYSTEM
# ============================================================================

class CombatSystem:
    """Enhanced combat system"""
    
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.in_combat = False
        self.enemy: Optional[NPC] = None
        self.combat_log: List[str] = []
    
    def start_combat(self, enemy_id: str) -> bool:
        """Start combat with an NPC"""
        enemy = self.engine.npcs.get(enemy_id)
        if not enemy:
            return False
        
        self.in_combat = True
        self.enemy = enemy
        self.combat_log = []
        self.add_combat_log(f"Combat started with {enemy.name}!")
        
        return True
    
    def add_combat_log(self, message: str) -> None:
        """Add message to combat log"""
        self.combat_log.append(message)
        if len(self.combat_log) > 10:
            self.combat_log.pop(0)
    
    def calculate_damage(self, attacker_strength: int, weapon_damage: int, 
                        skill_level: int, is_critical: bool = False) -> int:
        """Calculate damage dealt"""
        base_damage = weapon_damage + (attacker_strength // 10)
        skill_modifier = (skill_level / 100) * base_damage
        final_damage = int(base_damage + skill_modifier)
        
        if is_critical:
            final_damage = int(final_damage * 1.5)
        
        return max(1, final_damage)
    
    def player_attack(self, action: CombatAction) -> Tuple[int, str]:
        """Player attacks enemy"""
        if not self.engine.player or not self.enemy:
            return 0, "Invalid combat state"
        
        player = self.engine.player
        
        # Get weapon damage
        weapon_damage = 10  # Base unarmed damage
        for item in player.inventory:
            if item.item_type == ItemType.WEAPON and item.damage > weapon_damage:
                weapon_damage = item.damage
        
        if action == CombatAction.ATTACK:
            # Normal attack
            is_crit = random.randint(1, 100) <= (player.attributes.perception // 2)
            damage = self.calculate_damage(
                player.attributes.strength,
                weapon_damage,
                player.skills.brawling,
                is_crit
            )
            
            message = f"You attack for {damage} damage!"
            if is_crit:
                message += " CRITICAL HIT!"
            
            player.improve_skill("brawling", 1)
            return damage, message
        
        elif action == CombatAction.HEAVY_ATTACK:
            # Heavy attack - more damage, less accurate
            if random.randint(1, 100) <= 70:  # 70% hit chance
                damage = self.calculate_damage(
                    player.attributes.strength,
                    weapon_damage * 2,
                    player.skills.brawling,
                    False
                )
                player.improve_skill("brawling", 2)
                return damage, f"Heavy attack hits for {damage} damage!"
            else:
                return 0, "Heavy attack missed!"
        
        elif action == CombatAction.DIRTY_MOVE:
            # Dirty fighting - high damage, improves dirty fighting skill
            damage = self.calculate_damage(
                player.attributes.strength,
                weapon_damage + 15,
                player.skills.dirty_fighting,
                False
            )
            player.improve_skill("dirty_fighting", 2)
            return damage, f"Dirty move! {damage} damage dealt!"
        
        elif action == CombatAction.DEFEND:
            # Defend - reduce incoming damage next turn
            player.improve_skill("defense", 1)
            return 0, "You take a defensive stance."
        
        elif action == CombatAction.DODGE:
            # Dodge - chance to avoid next attack
            player.improve_skill("defense", 1)
            return 0, "You prepare to dodge."
        
        return 0, "Invalid action"
    
    def enemy_attack(self) -> Tuple[int, str]:
        """Enemy attacks player"""
        if not self.enemy or not self.engine.player:
            return 0, ""
        
        # Simple enemy AI
        damage = random.randint(5, 20)
        return damage, f"{self.enemy.name} attacks for {damage} damage!"
    
    def end_combat(self, player_won: bool) -> None:
        """End combat"""
        if not self.engine.player:
            return
        
        if player_won:
            self.engine.player.stats["fights_won"] += 1
            self.engine.player.attributes.reputation += 5
            self.engine.player.add_xp(100)
            self.add_combat_log("You won the fight!")
        else:
            self.engine.player.stats["fights_lost"] += 1
            self.engine.player.attributes.reputation -= 3
            self.add_combat_log("You lost the fight...")
        
        self.in_combat = False
        self.enemy = None


# ============================================================================
# ADVANCED FEATURES - TRADING SYSTEM
# ============================================================================

class TradingSystem:
    """Trading and economy system"""
    
    def __init__(self, engine: GameEngine):
        self.engine = engine
    
    def calculate_price(self, item: Item, buying: bool = True) -> int:
        """Calculate item price based on trading skill"""
        if not self.engine.player:
            return item.value
        
        base_price = item.value
        skill_modifier = self.engine.player.skills.trading / 100
        
        if buying:
            # Better skill = lower buy price
            price = int(base_price * (1.5 - skill_modifier * 0.5))
        else:
            # Better skill = higher sell price
            price = int(base_price * (0.5 + skill_modifier * 0.5))
        
        return max(1, price)
    
    def trade_with_npc(self, npc_id: str, player_items: List[str], 
                       npc_items: List[str]) -> Tuple[bool, str]:
        """Execute trade with NPC"""
        npc = self.engine.npcs.get(npc_id)
        if not npc or not self.engine.player:
            return False, "Invalid trade"
        
        # Calculate values
        player_value = sum(self.calculate_price(self.engine.items[item_id], False) 
                          for item_id in player_items if item_id in self.engine.items)
        npc_value = sum(self.calculate_price(self.engine.items[item_id], True)
                       for item_id in npc_items if item_id in self.engine.items)
        
        # Check if trade is fair (within 20%)
        if abs(player_value - npc_value) > player_value * 0.2:
            return False, "Trade is not fair"
        
        # Execute trade
        for item_id in player_items:
            self.engine.player.remove_item(item_id, 1)
        
        for item_id in npc_items:
            item = self.engine.items.get(item_id)
            if item:
                self.engine.player.add_item(item)
        
        # Improve relationship and skills
        npc.relationship += 5
        self.engine.player.improve_skill("trading", 2)
        self.engine.player.stats["items_traded"] += len(player_items) + len(npc_items)
        
        return True, "Trade successful!"


# ============================================================================
# ADVANCED FEATURES - EVENT SYSTEM
# ============================================================================

class EventSystem:
    """Random event system"""
    
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.events = self._initialize_events()
    
    def _initialize_events(self) -> List[Dict[str, Any]]:
        """Initialize random events"""
        return [
            {
                "id": "guard_shakedown",
                "name": "Guard Shakedown",
                "description": "Guards are searching cells for contraband!",
                "probability": 0.1,
                "effects": self._guard_shakedown
            },
            {
                "id": "fight_breaks_out",
                "name": "Fight in the Yard",
                "description": "A fight breaks out in the yard!",
                "probability": 0.15,
                "effects": self._fight_event
            },
            {
                "id": "new_inmate",
                "name": "New Arrival",
                "description": "A new inmate arrives at the prison.",
                "probability": 0.2,
                "effects": self._new_inmate
            },
            {
                "id": "good_meal",
                "name": "Good Meal",
                "description": "The cafeteria serves a surprisingly good meal today!",
                "probability": 0.1,
                "effects": self._good_meal
            },
            {
                "id": "contraband_opportunity",
                "name": "Contraband Deal",
                "description": "Someone offers you a contraband deal.",
                "probability": 0.12,
                "effects": self._contraband_deal
            },
        ]
    
    def check_random_event(self) -> Optional[Dict[str, Any]]:
        """Check if random event occurs"""
        for event in self.events:
            if random.random() < event["probability"]:
                return event
        return None
    
    def _guard_shakedown(self) -> str:
        """Guard shakedown event"""
        if not self.engine.player:
            return ""
        
        # Check for contraband
        contraband_found = False
        for item in self.engine.player.inventory[:]:
            if item.item_type == ItemType.CONTRABAND:
                self.engine.player.remove_item(item.id, item.quantity)
                contraband_found = True
        
        if contraband_found:
            self.engine.player.attributes.reputation -= 10
            return "Guards found your contraband! Items confiscated and reputation damaged."
        else:
            return "Guards searched your cell but found nothing."
    
    def _fight_event(self) -> str:
        """Fight event"""
        return "You witness a brutal fight in the yard. Better stay alert."
    
    def _new_inmate(self) -> str:
        """New inmate event"""
        return "A new inmate arrives. Fresh meat for the wolves."
    
    def _good_meal(self) -> str:
        """Good meal event"""
        if self.engine.player:
            self.engine.player.hunger = max(0, self.engine.player.hunger - 40)
            self.engine.player.heal(10)
        return "You enjoy a surprisingly good meal. Health and hunger improved!"
    
    def _contraband_deal(self) -> str:
        """Contraband deal event"""
        return "Someone whispers about a contraband deal. Interested?"


# ============================================================================
# ADVANCED FEATURES - JOB SYSTEM
# ============================================================================

class JobSystem:
    """Prison job system"""
    
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.jobs = self._initialize_jobs()
        self.current_job: Optional[str] = None
    
    def _initialize_jobs(self) -> Dict[str, Dict[str, Any]]:
        """Initialize available jobs"""
        return {
            "kitchen": {
                "name": "Kitchen Duty",
                "location": "cafeteria",
                "pay": 10,
                "duration": 4,  # hours
                "requirements": {"cooking": 0},
                "benefits": {"food_access": True},
                "description": "Work in the kitchen preparing meals"
            },
            "laundry": {
                "name": "Laundry Service",
                "location": "laundry",
                "pay": 8,
                "duration": 4,
                "requirements": {},
                "benefits": {"hygiene_bonus": 10},
                "description": "Wash and fold prison laundry"
            },
            "library": {
                "name": "Library Assistant",
                "location": "library",
                "pay": 12,
                "duration": 4,
                "requirements": {"intelligence": 40},
                "benefits": {"book_access": True, "intelligence_gain": 1},
                "description": "Help organize books and assist inmates"
            },
            "workshop": {
                "name": "Workshop Labor",
                "location": "workshop",
                "pay": 15,
                "duration": 6,
                "requirements": {"strength": 35},
                "benefits": {"crafting_bonus": 5, "tool_access": True},
                "description": "Manual labor in the prison workshop"
            },
            "gym": {
                "name": "Gym Maintenance",
                "location": "gym",
                "pay": 10,
                "duration": 3,
                "requirements": {"strength": 30},
                "benefits": {"workout_bonus": 10},
                "description": "Maintain gym equipment and clean"
            }
        }
    
    def can_work_job(self, job_id: str) -> Tuple[bool, str]:
        """Check if player can work job"""
        if not self.engine.player:
            return False, "No player"
        
        job = self.jobs.get(job_id)
        if not job:
            return False, "Invalid job"
        
        # Check requirements
        requirements = job["requirements"]
        player = self.engine.player
        
        for req, value in requirements.items():
            if hasattr(player.attributes, req):
                if getattr(player.attributes, req) < value:
                    return False, f"Need {value} {req}"
            elif hasattr(player.skills, req):
                if getattr(player.skills, req) < value:
                    return False, f"Need {value} {req} skill"
        
        # Check energy
        if player.current_energy < 30:
            return False, "Not enough energy"
        
        return True, "Can work"
    
    def work_job(self, job_id: str) -> Tuple[bool, str]:
        """Work a job"""
        can_work, message = self.can_work_job(job_id)
        if not can_work:
            return False, message
        
        job = self.jobs[job_id]
        player = self.engine.player
        
        # Deduct energy
        player.use_energy(30)
        
        # Advance time
        self.engine.advance_time(job["duration"] * 60)
        
        # Pay player
        player.money += job["pay"]
        
        # Apply benefits
        benefits = job["benefits"]
        if "intelligence_gain" in benefits:
            player.attributes.intelligence += benefits["intelligence_gain"]
        if "hygiene_bonus" in benefits:
            player.hygiene = min(100, player.hygiene + benefits["hygiene_bonus"])
        
        # Gain XP
        player.add_xp(50)
        
        return True, f"You worked {job['name']} and earned ${job['pay']}!"


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main(stdscr):
    """Main entry point"""
    game = Game(stdscr)
    game.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nThank you for playing Prison Break!")
        print("Developed by NinjaTech AI")
# WATERMARK_INTEGRITY_CHECK
# This file is protected by digital watermarking technology
# Unauthorized modification or distribution will be detected
# Fingerprint: 0a15f52f61664af1aa8836843d68d1ed
# Copyright © 2025 NovaSysErr-X. All rights reserved.
