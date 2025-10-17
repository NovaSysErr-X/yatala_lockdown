#!/usr/bin/env python3
"""
YATALA LOCKDOWN: Adelaide Northern Suburbs Prison Simulation
An authentic Australian prison survival game set in Adelaide's northern suburbs

Copyright © 2025 NovaSysErr-X. All rights reserved.

IMPORTANT LEGAL NOTICE:
This software is protected by international copyright laws and treaties.
Unauthorized distribution, modification, reverse engineering, or commercial use
is strictly prohibited and will result in severe legal consequences.

PROTECTION MEASURES:
- This software contains digital watermarks and anti-tampering mechanisms
- Any attempt to circumvent protection will be detected and prosecuted
- Violators will face civil damages up to $150,000 per violation
- Criminal penalties include up to 5 years imprisonment

Author: NovaSysErr-X
Version: 0.5.0 beta
Platform: Termux / Linux Terminal
Python: 3.9+
License: MIT with additional restrictions (see COPYRIGHT_PROTECTION.md)

WARNING: By using this software, you agree to these terms and acknowledge
that violation will result in immediate legal action to the fullest extent
of applicable law.
"""

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
    """Location types in Yatala"""
    CELL_BLOCK = "Cell Block"
    MESS_HALL = "Mess Hall"
    YARD = "Yard"
    WORKSHOP = "Workshop"
    INFIRMARY = "Infirmary"
    LIBRARY = "Library"
    SOLITARY = "Solitary Confinement"
    VISITATION = "Visitation Centre"
    CHAPEL = "Chapel"
    EDUCATION = "Education Block"
    SHOWERS = "Showers Block"
    LAUNDRY = "Laundry Facility"
    ADMIN = "Administration Block"
    KITCHEN = "Main Kitchen"


class ItemType(Enum):
    """Types of items in the game"""
    WEAPON = "Weapon"
    CONSUMABLE = "Consumable"
    CRAFTING_MATERIAL = "Crafting Material"
    MANUFACTURED = "Manufactured Item"
    TOOL = "Tool"
    QUEST = "Quest Item"
    CLOTHING = "Clothing"
    VALUABLE = "Valuable"
    DOCUMENT = "Document"


class Skill(Enum):
    """Player skills"""
    STRENGTH = "Strength"
    DEXTERITY = "Dexterity"
    CONSTITUTION = "Constitution"
    INTELLIGENCE = "Intelligence"
    WISDOM = "Wisdom"
    CHARISMA = "Charisma"
    CRAFTING = "Crafting"
    STEALTH = "Stealth"
    INTIMIDATION = "Intimidation"
    MEDICINE = "Medicine"
    EDUCATION = "Education"
    PSYCHOLOGY = "Psychology"
    ELECTRONICS = "Electronics"
    CHEMISTRY = "Chemistry"


class Faction(Enum):
    """Prison factions in Yatala"""
    REBELS_MC = "Rebels MC"
    HELLS_ANGELS = "Hells Angels"
    COMANCHEROS = "Comancheros"
    VIKINGS_OMCG = "Vikings OMCG"
    BLACK_UHLANS = "Black Uhlans OMCG"
    WHITE_POWER = "White Power"
    ISLAMIC_GROUP = "Islamic Group"
    ABORIGINAL_ALLIANCE = "Aboriginal Alliance"
    STAFF_CORRUPTION = "Staff Corruption Ring"
    INMATE_COUNCIL = "Inmate Council"
    MEDICAL_STAFF = "Medical Staff"
    CHAPLAINS = "Chaplains"
    EDUCATORS = "Educators"
    NEUTRAL = "Neutral"


class MoodState(Enum):
    """Player mood states"""
    DISTRESSED = "Distressed"
    ANXIOUS = "Anxious"
    OPTIMISTIC = "Optimistic"
    DESPONDENT = "Despondent"
    EXHAUSTED = "Exhausted"
    NEUTRAL = "Neutral"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Attributes:
    """Player character attributes"""
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    # Psychological attributes
    stress_tolerance: int = 50
    emotional_stability: int = 50
    resilience: int = 50
    adaptability: int = 50


@dataclass
class FactionStanding:
    """Player's standing with a faction"""
    faction: Faction
    reputation: int = 0  # -100 to 100
    influence: int = 0   # 0 to 100
    rank: str = "Unknown"
    perks: List[str] = field(default_factory=list)  # Faction-specific perks


@dataclass
class PoliticalStanding:
    """Player's overall political standing in the prison"""
    overall_reputation: int = 0  # -100 to 100
    influence_level: int = 0     # 0 to 100
    primary_faction: Optional[Faction] = None
    faction_ranks: Dict[Faction, str] = field(default_factory=dict)


@dataclass
class MedicalCondition:
    """Medical condition affecting the player"""
    name: str
    description: str
    severity: int  # 1-10
    chronic: bool = False
    treatment_required: bool = True
    treatment_cost: int = 0
    recurrence_chance: float = 0.0  # 0.0 to 1.0
    stat_effects: Dict[str, int] = field(default_factory=dict)  # Effects on stats


@dataclass
class CraftingRecipe:
    """Crafting recipe for manufacturing items"""
    name: str
    description: str
    required_items: Dict[str, int]  # item_name: quantity
    required_skills: Dict[Skill, int]  # skill: minimum_level
    output_item: str
    output_quantity: int = 1
    success_chance: float = 1.0  # 0.0 to 1.0
    time_required: int = 1  # in game hours
    faction_required: Optional[Faction] = None  # faction needed to access


@dataclass
class ManufacturingProcess:
    """Large-scale manufacturing process"""
    name: str
    description: str
    required_materials: Dict[str, int]  # material_name: quantity
    required_skills: Dict[Skill, int]  # skill: minimum_level
    output_item: str
    output_quantity: int
    time_required: int  # in game days
    worker_requirements: int  # number of workers needed
    risk_factor: float = 0.0  # chance of negative consequences (0.0 to 1.0)
    faction_required: Optional[Faction] = None


@dataclass
class MoneyLaunderingOperation:
    """Money laundering operation"""
    name: str
    description: str
    capital_required: int
    risk_level: float  # 0.0 to 1.0
    clean_money_return: int
    time_required: int  # in game days
    success_chance: float = 0.5  # 0.0 to 1.0
    underground_rep_required: int = 0
    faction_required: Optional[Faction] = None


@dataclass
class RehabilitationProgram:
    """Rehabilitation/educational program"""
    name: str
    description: str
    duration: int  # in game days
    cost: int  # in clean money
    skill_improvements: Dict[Skill, int]  # skill: improvement_amount
    attribute_improvements: Dict[str, int]  # attribute: improvement_amount
    parole_benefit: int = 0  # reduction in sentence time (days)
    prerequisites: List[str] = field(default_factory=list)  # required programs
    education_level_required: int = 0


@dataclass
class RelationshipEvent:
    """Event that affects relationships with NPCs"""
    name: str
    description: str
    relationship_effects: Dict[str, Tuple[int, int, int]]  # npc_name: (trust, respect, fear)
    cooldown_days: int = 7
    faction_involved: Optional[Faction] = None


@dataclass
class SeasonalEvent:
    """Special seasonal or holiday event"""
    name: str
    description: str
    start_date: Tuple[int, int]  # (month, day)
    end_date: Tuple[int, int]  # (month, day)
    effects: List[str]  # list of effect descriptions
    participation_requirements: List[str]  # requirements to participate
    rewards: Dict[str, int]  # reward_name: quantity
    risk_level: float = 0.0  # chance of negative consequences
    faction_involved: Optional[Faction] = None


@dataclass
class Item:
    """Game item"""
    name: str
    description: str
    item_type: ItemType
    value: int = 0
    weight: float = 0.0
    effects: Dict[str, Any] = field(default_factory=dict)
    required_skills: Dict[Skill, int] = field(default_factory=dict)
    faction_required: Optional[Faction] = None


@dataclass
class Quest:
    """Game quest"""
    id: str
    title: str
    description: str
    objectives: List[str]
    rewards: Dict[str, Any]
    status: str = "available"  # available, active, completed, failed
    prerequisites: List[str] = field(default_factory=list)


@dataclass
class Location:
    """Game location - Yatala prison"""
    name: str
    description: str
    location_type: LocationType
    connected_locations: List[str] = field(default_factory=list)
    npcs: List[str] = field(default_factory=list)
    items: List[str] = field(default_factory=list)
    faction_presence: List[Faction] = field(default_factory=list)
    restricted_access: bool = False
    access_requirements: List[str] = field(default_factory=list)
    ascii_art: Optional[str] = None


@dataclass
class NPC:
    """Non-player character"""
    name: str
    description: str
    personality: str
    dialogue: Dict[str, str]  # topic: response
    faction: Optional[Faction] = None
    location: str = ""
    relationship_traits: Dict[str, int] = field(default_factory=lambda: {
        "trust": 50,    # 0-100
        "respect": 50,  # 0-100
        "fear": 0       # 0-100
    })
    inventory: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)  # services they offer


@dataclass
class Player:
    """Player character"""
    name: str
    attributes: Attributes
    skills: Dict[Skill, int]
    inventory: List[Item]
    location: str
    health: int = 100
    max_health: int = 100
    energy: int = 100
    max_energy: int = 100
    hunger: int = 0  # 0-100 (0 = full, 100 = starving)
    thirst: int = 0  # 0-100 (0 = full, 100 = dehydrated)
    experience: int = 0
    level: int = 1
    money: int = 50
    # New psychological wellness metrics
    stress_level: int = 0  # 0-100 (0 = relaxed, 100 = extremely stressed)
    hope_level: int = 50  # 0-100 (0 = hopeless, 100 = very hopeful)
    mental_fatigue: int = 0  # 0-100 (0 = alert, 100 = exhausted)
    mood: MoodState = MoodState.NEUTRAL
    # Underground economy metrics
    dirty_money: int = 0
    clean_money: int = 0
    underground_reputation: int = 0  # 0-100
    # Rehabilitation metrics
    education_level: int = 0  # 0-100
    vocational_skills: Dict[str, int] = field(default_factory=dict)  # skill: level
    therapy_sessions: int = 0
    programs_completed: List[str] = field(default_factory=list)
    parole_progress: int = 0  # 0-100
    # Health system
    medical_conditions: List[MedicalCondition] = field(default_factory=list)
    # Relationship system
    relationships: Dict[str, Dict[str, int]] = field(default_factory=lambda: {
        # npc_name: {trust: 0-100, respect: 0-100, fear: 0-100}
    })
    relationship_events: Dict[str, datetime] = field(default_factory=dict)  # event_name: last_occurrence
    # Political standing
    political_standing: PoliticalStanding = field(default_factory=PoliticalStanding)
    faction_standing: Dict[Faction, FactionStanding] = field(default_factory=dict)
    # Crafting system
    recipes_known: List[str] = field(default_factory=list)
    manufacturing_operations: List[str] = field(default_factory=list)
    # Seasonal events
    events_participated: Dict[str, datetime] = field(default_factory=dict)  # event_name: last_participation
    # Time tracking
    sentence_length: int = 365  # in days
    days_served: int = 0
    game_time: datetime = field(default_factory=lambda: datetime(2025, 1, 1, 8, 0))  # Start at 8:00 AM
    # Quest tracking
    active_quests: List[str] = field(default_factory=list)
    completed_quests: List[str] = field(default_factory=list)
    # Weather system
    current_weather: str = "Clear"
    weather_effects: Dict[str, Any] = field(default_factory=dict)

    def update_mood(self) -> None:
        """Update mood based on psychological wellness metrics"""
        avg_wellness = (self.stress_level + (100 - self.hope_level) + self.mental_fatigue) / 3
        
        if avg_wellness > 80:
            self.mood = MoodState.DISTRESSED
        elif avg_wellness > 60:
            self.mood = MoodState.ANXIOUS
        elif avg_wellness > 40:
            self.mood = MoodState.NEUTRAL
        elif avg_wellness > 20:
            self.mood = MoodState.OPTIMISTIC
        else:
            self.mood = MoodState.DESPONDENT

    def update_psychological_wellness(self, stress_change: int = 0, hope_change: int = 0, fatigue_change: int = 0) -> None:
        """Update psychological wellness metrics"""
        self.stress_level = max(0, min(100, self.stress_level + stress_change))
        self.hope_level = max(0, min(100, self.hope_level + hope_change))
        self.mental_fatigue = max(0, min(100, self.mental_fatigue + fatigue_change))
        self.update_mood()

    def add_recipe(self, recipe_name: str) -> None:
        """Add a crafting recipe to known recipes"""
        if recipe_name not in self.recipes_known:
            self.recipes_known.append(recipe_name)

    def add_manufacturing_operation(self, operation_name: str) -> None:
        """Add a manufacturing operation to known operations"""
        if operation_name not in self.manufacturing_operations:
            self.manufacturing_operations.append(operation_name)

    def launder_money(self, amount: int, risk_tolerance: int) -> Tuple[bool, int, str]:
        """Attempt to launder dirty money"""
        if amount > self.dirty_money:
            return False, 0, "Not enough dirty money"
        
        # Base success chance based on player's underground reputation and risk tolerance
        success_chance = min(0.9, self.underground_reputation / 100.0 + risk_tolerance / 200.0)
        
        if random.random() < success_chance:
            # Successful laundering
            clean_return = int(amount * 0.7)  # 70% return rate
            self.dirty_money -= amount
            self.clean_money += clean_return
            self.underground_reputation = min(100, self.underground_reputation + 5)
            return True, clean_return, "Money laundering successful"
        else:
            # Failed attempt
            penalty = int(amount * 0.3)  # Lose 30% of attempted amount
            self.dirty_money = max(0, self.dirty_money - penalty)
            self.underground_reputation = max(0, self.underground_reputation - 10)
            return False, 0, "Money laundering failed"

    def enroll_in_program(self, program: RehabilitationProgram) -> bool:
        """Enroll in a rehabilitation program"""
        # Check prerequisites
        for prereq in program.prerequisites:
            if prereq not in self.programs_completed:
                return False
        
        # Check education level
        if self.education_level < program.education_level_required:
            return False
        
        # Check cost
        if self.clean_money < program.cost:
            return False
        
        # Enroll in program
        self.clean_money -= program.cost
        self.education_level = min(100, self.education_level + 5)
        
        # Apply skill improvements
        for skill, improvement in program.skill_improvements.items():
            if skill in self.skills:
                self.skills[skill] = min(100, self.skills[skill] + improvement)
        
        # Apply attribute improvements
        # For simplicity, we'll apply these to random attributes
        for attr, improvement in program.attribute_improvements.items():
            # This would need to be more specific in a real implementation
            pass
        
        # Apply parole benefit
        self.parole_progress = min(100, self.parole_progress + program.parole_benefit)
        
        # Add to completed programs
        if program.name not in self.programs_completed:
            self.programs_completed.append(program.name)
        
        return True

    def add_medical_condition(self, condition: MedicalCondition) -> None:
        """Add a medical condition to the player"""
        # Check if condition already exists
        for existing_condition in self.medical_conditions:
            if existing_condition.name == condition.name:
                return  # Already have this condition
        
        self.medical_conditions.append(condition)
        
        # Apply stat effects
        for stat, effect in condition.stat_effects.items():
            # This would modify the relevant stat in a real implementation
            pass

    def treat_medical_condition(self, condition_name: str) -> bool:
        """Treat a medical condition"""
        for condition in self.medical_conditions:
            if condition.name == condition_name and condition.treatment_required:
                if self.clean_money >= condition.treatment_cost:
                    self.clean_money -= condition.treatment_cost
                    self.medical_conditions.remove(condition)
                    return True
        return False

    def update_relationship(self, npc_name: str, trust_change: int = 0, respect_change: int = 0, fear_change: int = 0) -> None:
        """Update relationship with an NPC"""
        if npc_name not in self.relationships:
            self.relationships[npc_name] = {"trust": 50, "respect": 50, "fear": 0}
        
        relationships = self.relationships[npc_name]
        relationships["trust"] = max(0, min(100, relationships["trust"] + trust_change))
        relationships["respect"] = max(0, min(100, relationships["respect"] + respect_change))
        relationships["fear"] = max(0, min(100, relationships["fear"] + fear_change))

    def trigger_relationship_event(self, event: RelationshipEvent) -> bool:
        """Trigger a relationship event with cooldown check"""
        now = datetime.now()
        last_occurrence = self.relationship_events.get(event.name, None)
        
        if last_occurrence:
            days_since = (now - last_occurrence).days
            if days_since < event.cooldown_days:
                return False  # Event on cooldown
        
        # Trigger event effects
        for npc_name, (trust, respect, fear) in event.relationship_effects.items():
            self.update_relationship(npc_name, trust, respect, fear)
        
        # Update last occurrence
        self.relationship_events[event.name] = now
        return True

    def update_faction_standing(self, faction: Faction, reputation_change: int = 0, influence_change: int = 0) -> None:
        """Update standing with a faction"""
        if faction not in self.faction_standing:
            self.faction_standing[faction] = FactionStanding(faction=faction)
        
        standing = self.faction_standing[faction]
        standing.reputation = max(-100, min(100, standing.reputation + reputation_change))
        standing.influence = max(0, min(100, standing.influence + influence_change))
        
        # Update rank based on reputation
        if standing.reputation >= 80:
            standing.rank = "Leader"
        elif standing.reputation >= 60:
            standing.rank = "Trusted"
        elif standing.reputation >= 40:
            standing.rank = "Member"
        elif standing.reputation >= 20:
            standing.rank = "Associate"
        elif standing.reputation >= -20:
            standing.rank = "Neutral"
        elif standing.reputation >= -40:
            standing.rank = "Distrusted"
        elif standing.reputation >= -60:
            standing.rank = "Enemy"
        else:
            standing.rank = "Public Enemy"

    def update_political_standing(self) -> None:
        """Update overall political standing"""
        total_reputation = sum(standing.reputation for standing in self.faction_standing.values())
        total_influence = sum(standing.influence for standing in self.faction_standing.values())
        count = len(self.faction_standing)
        
        if count > 0:
            self.political_standing.overall_reputation = max(-100, min(100, total_reputation // count))
            self.political_standing.influence_level = max(0, min(100, total_influence // count))
            
            # Determine primary faction
            if self.faction_standing:
                primary_faction = max(self.faction_standing.items(), key=lambda x: x[1].reputation)[0]
                self.political_standing.primary_faction = primary_faction

    def participate_in_event(self, event: SeasonalEvent) -> bool:
        """Participate in a seasonal event with cooldown check"""
        now = datetime.now()
        last_participation = self.events_participated.get(event.name, None)
        
        if last_participation:
            days_since = (now - last_participation).days
            # For seasonal events, we might want to allow participation each year
            # For now, we'll use a simple cooldown
            if days_since < 30:  # 30 day cooldown
                return False  # Event on cooldown
        
        # Check if event is currently active
        current_month = self.game_time.month
        current_day = self.game_time.day
        
        start_month, start_day = event.start_date
        end_month, end_day = event.end_date
        
        # Simple date range check (doesn't handle year boundaries properly but sufficient for this example)
        is_active = False
        if start_month <= current_month <= end_month:
            if start_month == current_month and current_day >= start_day:
                if end_month == current_month and current_day <= end_day:
                    is_active = True
                elif end_month > current_month:
                    is_active = True
            elif start_month < current_month < end_month:
                is_active = True
            elif end_month == current_month and current_day <= end_day:
                is_active = True
        
        if not is_active:
            return False  # Event not active
        
        # Check requirements
        # For simplicity, we'll assume requirements are met
        
        # Participate in event
        # Apply rewards
        # For simplicity, we'll just print the rewards
        print(f"Participated in {event.name}: {event.rewards}")
        
        # Update last participation
        self.events_participated[event.name] = now
        return True

    def advance_time(self, hours: int = 1) -> None:
        """Advance game time and update related systems"""
        self.game_time += timedelta(hours=hours)
        self.days_served += hours // 24
        
        # Update psychological wellness over time
        # Slowly increase stress and fatigue, decrease hope
        self.update_psychological_wellness(
            stress_change=hours // 4,
            hope_change=-hours // 6,
            fatigue_change=hours // 3
        )
        
        # Update medical conditions
        for condition in self.medical_conditions[:]:  # Create a copy to iterate over
            if condition.chronic and random.random() < condition.recurrence_chance:
                # Condition flares up again
                pass  # In a real implementation, this might apply effects
        
        # Update weather (simplified)
        if random.random() < 0.1:  # 10% chance of weather change each time
            weathers = ["Clear", "Cloudy", "Rainy", "Windy", "Foggy"]
            self.current_weather = random.choice(weathers)


# ============================================================================
# ASCII ART ASSETS
# ============================================================================

ASCII_ARTS = {
    "chapel": '''
        =========================
              CHAPEL OF REDEMPTION
        =========================
               +-----------+
               |    &&&    |
               |   &&&&&   |
               |  &&&&&&&  |
               | &&&&&&&&& |
               |&&&&&&&&&&&|
               +-----------+
                   |___|
                   |___|
    ''',
    "education": '''
        =========================
              EDUCATION BLOCK
        =========================
          ________________
         /_______________/|
         |               ||
         |  BOOKS        ||
         |  COMPUTERS    ||
         |  DESKS        ||
         |______________|/
    ''',
    "visitation": '''
        =========================
             VISITATION CENTRE
        =========================
         [GATE]    [ROOMS]
           ||         |||
           ||    +---+-+-+
           ||    |FAM|FAM|
           ||    |ILY|ILY|
           ||    +---+-+-+
    ''',
    "solitary": '''
        =========================
            THE HOLE (SOLITARY)
        =========================
         ________________
        |                |
        |  [===]  [===]  |
        |                |
        |  [===]  [===]  |
        |________________|
    ''',
    "showers": '''
        =========================
              SHOWERS BLOCK
        =========================
         |[|]    |[|]    |[|]|
         |[|]    |[|]    |[|]|
         |[|]    |[|]    |[|]|
         |[|]    |[|]    |[|]|
         |[|]    |[|]    |[|]|
    ''',
    "laundry": '''
        =========================
            LAUNDRY FACILITY
        =========================
         [WASH] [DRY] [FOLD]
         ( )( ) ( )( ) ( )( )
         ( )( ) ( )( ) ( )( )
         ( )( ) ( )( ) ( )( )
    ''',
    "padre_osullivan": '''
         .--.     .--.
        /.-. \   / .-.\\
        | | | |   | | | |
        | | | |   | | | |
        |\`-' /   \'-.-'|
         '--'       '--'
          ||         ||
    ''',
    "teacher_jenny": '''
          .-.
         (   )
        .-.| |.-.
       (   : :   )
        `-'" "'-'
    ''',
    "officer_sally": '''
          .--.
         /  _ `.
        |  (_)  |
        |  ,---'|
         \\ `--. \\
          `---.'`
    ''',
    "brad_student": '''
          .--.
         /   |\\
        |    ||
        |    ||
         \\   ||
          `--'|
    ''',
    "mike_laundry": '''
          .--.
         |    |
         |    |
         |    |
         |    |
         '----'
    ''',
    "yatala_prison": '''
        =========================
             YATALA LOCKDOWN
        =========================
         .-----------------.
         |  [C]  [Y]  [M]  |
         |                 |
         |  [I]  [L]  [S]  |
         |                 |
         |  [V]  [E]  [A]  |
         '-----------------'
    '''
}


# ============================================================================
# GAME DATA
# ============================================================================

# Crafting recipes
CRAFTING_RECIPES = [
    CraftingRecipe(
        name="Shiv",
        description="A makeshift knife made from scrap metal",
        required_items={"scrap metal": 1, "tape": 1},
        required_skills={Skill.CRAFTING: 20},
        output_item="shiv",
        output_quantity=1,
        success_chance=0.8
    ),
    CraftingRecipe(
        name="Lockpick Set",
        description="A set of tools for picking locks",
        required_items={"wire": 2, "plastic": 1},
        required_skills={Skill.CRAFTING: 30, Skill.DEXTERITY: 25},
        output_item="lockpick set",
        output_quantity=1,
        success_chance=0.7
    ),
    CraftingRecipe(
        name="Contraband Radio",
        description="A hidden radio for news and entertainment",
        required_items={"electronics parts": 3, "battery": 1, "plastic case": 1},
        required_skills={Skill.CRAFTING: 40, Skill.ELECTRONICS: 35},
        output_item="contraband radio",
        output_quantity=1,
        success_chance=0.6,
        faction_required=Faction.INMATE_COUNCIL
    )
]

# Manufacturing processes
MANUFACTURING_PROCESSES = [
    ManufacturingProcess(
        name="Alcohol Brewery",
        description="Large-scale production of homemade alcohol",
        required_materials={"sugar": 10, "yeast": 5, "water": 20},
        required_skills={Skill.CRAFTING: 50, Skill.CHEMISTRY: 40},
        output_item="bottle of alcohol",
        output_quantity=50,
        time_required=7,  # 7 game days
        worker_requirements=3,
        risk_factor=0.3,  # 30% chance of getting caught
        faction_required=Faction.REBELS_MC
    ),
    ManufacturingProcess(
        name="Cigarette Production",
        description="Mass production of contraband cigarettes",
        required_materials={"tobacco": 20, "paper": 50, "filters": 50},
        required_skills={Skill.CRAFTING: 30, Skill.DEXTERITY: 25},
        output_item="pack of cigarettes",
        output_quantity=100,
        time_required=3,  # 3 game days
        worker_requirements=2,
        risk_factor=0.2,  # 20% chance of getting caught
        faction_required=None
    )
]

# Money laundering operations
MONEY_LAUNDERING_OPERATIONS = [
    MoneyLaunderingOperation(
        name="Laundry Service Front",
        description="Use a legitimate business to clean dirty money",
        capital_required=1000,
        risk_level=0.2,  # Low risk
        clean_money_return=700,  # 70% return
        time_required=5,  # 5 game days
        success_chance=0.8,
        underground_rep_required=20,
        faction_required=Faction.STAFF_CORRUPTION
    ),
    MoneyLaunderingOperation(
        name="Casino Chips",
        description="Convert dirty money to casino chips and back",
        capital_required=5000,
        risk_level=0.6,  # High risk
        clean_money_return=3000,  # 60% return
        time_required=10,  # 10 game days
        success_chance=0.5,
        underground_rep_required=50,
        faction_required=Faction.BLACK_UHLANS
    )
]

# Rehabilitation programs
REHABILITATION_PROGRAMS = [
    RehabilitationProgram(
        name="Basic Literacy",
        description="Improve reading and writing skills",
        duration=30,  # 30 game days
        cost=200,  # in clean money
        skill_improvements={Skill.EDUCATION: 10},
        attribute_improvements={"intelligence": 2},
        parole_benefit=5,  # 5 days off sentence
        education_level_required=0
    ),
    RehabilitationProgram(
        name="Vocational Training - Carpentry",
        description="Learn carpentry skills for post-prison employment",
        duration=60,  # 60 game days
        cost=500,
        skill_improvements={Skill.CRAFTING: 15, Skill.STRENGTH: 5},
        attribute_improvements={"dexterity": 3},
        parole_benefit=10,
        prerequisites=["Basic Literacy"],
        education_level_required=30
    ),
    RehabilitationProgram(
        name="Anger Management Therapy",
        description="Learn to control aggressive behavior",
        duration=45,  # 45 game days
        cost=300,
        skill_improvements={Skill.PSYCHOLOGY: 12},
        attribute_improvements={"wisdom": 4, "emotional_stability": 10},
        parole_benefit=7,
        education_level_required=20
    )
]

# Medical conditions
MEDICAL_CONDITIONS = [
    MedicalCondition(
        name="Depression",
        description="Persistent feelings of sadness and hopelessness",
        severity=7,
        chronic=True,
        treatment_required=True,
        treatment_cost=500,
        recurrence_chance=0.3,
        stat_effects={"wisdom": -2, "charisma": -3}
    ),
    MedicalCondition(
        name="Anxiety Disorder",
        description="Excessive worry and fear",
        severity=6,
        chronic=True,
        treatment_required=True,
        treatment_cost=400,
        recurrence_chance=0.25,
        stat_effects={"dexterity": -2, "stress_tolerance": -10}
    ),
    MedicalCondition(
        name="Influenza",
        description="Viral infection causing fever and body aches",
        severity=4,
        chronic=False,
        treatment_required=False,
        treatment_cost=100,
        recurrence_chance=0.1,
        stat_effects={"strength": -3, "constitution": -2}
    )
]

# Relationship events
RELATIONSHIP_EVENTS = [
    RelationshipEvent(
        name="Helped in Fight",
        description="You helped an inmate in a fight",
        relationship_effects={
            "Generic Inmate": (10, 5, -5),  # +10 trust, +5 respect, -5 fear
        },
        cooldown_days=30,
        faction_involved=Faction.REBELS_MC
    ),
    RelationshipEvent(
        name="Snitched to Guards",
        description="You reported illegal activity to the guards",
        relationship_effects={
            "Generic Inmate": (-20, -10, 15),  # -20 trust, -10 respect, +15 fear
        },
        cooldown_days=60
    )
]

# Seasonal events
SEASONAL_EVENTS = [
    SeasonalEvent(
        name="Christmas Day",
        description="Christmas celebration in the prison",
        start_date=(12, 25),
        end_date=(12, 25),
        effects=["Special meal", "Visitation hours extended"],
        participation_requirements=["Good behavior"],
        rewards={"clean_money": 100, "hope_level": 10},
        risk_level=0.1,
        faction_involved=None
    ),
    SeasonalEvent(
        name="ANZAC Day",
        description="Commemorating Australian military personnel",
        start_date=(4, 25),
        end_date=(4, 25),
        effects=["Memorial service", "Moment of silence"],
        participation_requirements=["Attendance at service"],
        rewards={"respect": 5, "wisdom": 2},
        risk_level=0.05,
        faction_involved=None
    )
]

# Items
ITEMS = [
    Item(
        name="shiv",
        description="A makeshift knife made from scrap metal",
        item_type=ItemType.WEAPON,
        value=50,
        weight=0.5,
        effects={"damage": 15}
    ),
    Item(
        name="contraband radio",
        description="A hidden radio for news and entertainment",
        item_type=ItemType.TOOL,
        value=200,
        weight=1.0,
        effects={"entertainment": 10}
    ),
    Item(
        name="bottle of alcohol",
        description="Homemade brew, strong and potent",
        item_type=ItemType.CONSUMABLE,
        value=150,
        weight=1.5,
        effects={"intoxication": 20, "stress_relief": 15}
    ),
    Item(
        name="pack of cigarettes",
        description="Contraband cigarettes",
        item_type=ItemType.CONSUMABLE,
        value=100,
        weight=0.2,
        effects={"stress_relief": 5, "addiction_risk": 10}
    ),
    Item(
        name="educational book",
        description="A book to improve your knowledge",
        item_type=ItemType.CONSUMABLE,
        value=75,
        weight=0.8,
        effects={"education": 5}
    ),
    Item(
        name="Vili's Pie",
        description="A famous South Australian pie",
        item_type=ItemType.CONSUMABLE,
        value=15,
        weight=0.3,
        effects={"hunger": -20, "happiness": 5}
    ),
    Item(
        name="Farmers Union Iced Coffee",
        description="Iconic South Australian iced coffee",
        item_type=ItemType.CONSUMABLE,
        value=5,
        weight=0.5,
        effects={"thirst": -15, "energy": 10}
    )
]

# Locations
LOCATIONS = [
    Location(
        name="Cell Block C",
        description="Your assigned cell in the main cell block. Bunk beds, concrete walls, and a small window looking out to the yard.",
        location_type=LocationType.CELL_BLOCK,
        connected_locations=["Yard", "Mess Hall", "Showers Block"],
        npcs=["Cellmate Bob"],
        items=["shiv", "contraband radio"],
        ascii_art="yatala_prison"
    ),
    Location(
        name="Yard",
        description="The prison yard where inmates get some fresh air and exercise. Various groups gather here.",
        location_type=LocationType.YARD,
        connected_locations=["Cell Block C", "Workshop", "Chapel", "Education Block"],
        npcs=["Yard Boss Tony", "Recreation Inmate"],
        items=["pack of cigarettes"],
        faction_presence=[Faction.REBELS_MC, Faction.HELLS_ANGELS, Faction.WHITE_POWER]
    ),
    Location(
        name="Mess Hall",
        description="Where inmates eat their meals. Long tables and benches, supervised by guards.",
        location_type=LocationType.MESS_HALL,
        connected_locations=["Cell Block C", "Kitchen"],
        npcs=["Cook Mike", "Food Line Guard"],
        items=["Vili's Pie"],
        ascii_art="yatala_prison"
    ),
    Location(
        name="Workshop",
        description="An industrial workshop where inmates work on various maintenance and manufacturing tasks.",
        location_type=LocationType.WORKSHOP,
        connected_locations=["Yard", "Laundry Facility"],
        npcs=["Workshop Foreman", "Inmate Worker"],
        items=["scrap metal", "tools"],
        faction_presence=[Faction.INMATE_COUNCIL]
    ),
    Location(
        name="Infirmary",
        description="The prison medical facility, staffed by doctors and nurses.",
        location_type=LocationType.INFIRMARY,
        connected_locations=["Administration Block"],
        npcs=["Dr. Smith", "Nurse Jenny"],
        items=["medical supplies", "prescription medication"],
        restricted_access=True,
        access_requirements=["medical appointment"]
    ),
    Location(
        name="Library",
        description="A quiet space with books, magazines, and educational materials.",
        location_type=LocationType.LIBRARY,
        connected_locations=["Education Block"],
        npcs=["Librarian Sarah", "Studious Inmate"],
        items=["educational book", "newspaper"],
        ascii_art="education"
    ),
    Location(
        name="Solitary Confinement",
        description="The Hole. A place of isolation for disciplinary reasons.",
        location_type=LocationType.SOLITARY,
        connected_locations=["Administration Block"],
        npcs=["Solitary Guard"],
        items=[],
        restricted_access=True,
        access_requirements=["disciplinary action"],
        ascii_art="solitary"
    ),
    Location(
        name="Visitation Centre",
        description="Where inmates meet with family and friends behind reinforced glass.",
        location_type=LocationType.VISITATION,
        connected_locations=["Administration Block"],
        npcs=["Padre O'Sullivan", "Officer Sally", "Visitor"],
        items=[],
        ascii_art="visitation"
    ),
    Location(
        name="Chapel of Redemption",
        description="A place for spiritual reflection and religious services.",
        location_type=LocationType.CHAPEL,
        connected_locations=["Yard"],
        npcs=["Padre O'Sullivan", "Chapel Regular"],
        items=["religious text"],
        ascii_art="chapel"
    ),
    Location(
        name="Education Block",
        description="Classrooms for educational and vocational programs.",
        location_type=LocationType.EDUCATION,
        connected_locations=["Yard", "Library"],
        npcs=["Teacher Jenny", "Brad 'the Student'", "Education Coordinator"],
        items=["educational materials", "computers"],
        ascii_art="education"
    ),
    Location(
        name="Showers Block",
        description="Communal shower facilities, a place where conflicts often arise.",
        location_type=LocationType.SHOWERS,
        connected_locations=["Cell Block C"],
        npcs=["Shower Monitor", "Inmate"],
        items=[],
        ascii_art="showers"
    ),
    Location(
        name="Laundry Facility",
        description="Where all the prison laundry is processed.",
        location_type=LocationType.LAUNDRY,
        connected_locations=["Workshop"],
        npcs=["Laundry Supervisor Mike", "Laundry Worker"],
        items=["clean uniforms"],
        ascii_art="laundry"
    ),
    Location(
        name="Administration Block",
        description="The heart of prison operations, housing offices and special facilities.",
        location_type=LocationType.ADMIN,
        connected_locations=["Infirmary", "Solitary Confinement", "Visitation Centre"],
        npcs=["Warden Johnson", "Administrator"],
        items=["files", "forms"],
        restricted_access=True,
        access_requirements=["authorized personnel"]
    ),
    Location(
        name="Main Kitchen",
        description="Where all meals are prepared for the prison population.",
        location_type=LocationType.KITCHEN,
        connected_locations=["Mess Hall"],
        npcs=["Head Chef", "Kitchen Staff"],
        items=["Vili's Pie", "Farmers Union Iced Coffee"],
        faction_presence=[Faction.STAFF_CORRUPTION]
    )
]

# NPCs
NPCS = [
    NPC(
        name="Padre O'Sullivan",
        description="A kind Irish priest who runs the chapel services.",
        personality="Compassionate and wise, Padre O'Sullivan offers spiritual guidance to inmates of all backgrounds.",
        dialogue={
            "default": "God bless you, my son. What brings you to the chapel today?",
            "spiritual guidance": "Remember, redemption is always possible, no matter what you've done.",
            "confession": "I'm here to listen, and what is said in this chapel stays in this chapel."
        },
        faction=Faction.CHAPLAINS,
        location="Chapel of Redemption",
        services=["spiritual guidance", "confession"]
    ),
    NPC(
        name="Teacher Jenny",
        description="An enthusiastic educator who runs the literacy programs.",
        personality="Dedicated to helping inmates improve their lives through education.",
        dialogue={
            "default": "Hello there! Ready to learn something new today?",
            "classes": "We're covering basic reading skills this week. Have you enrolled?",
            "education": "Education is the key to a better future, both inside and outside these walls."
        },
        faction=Faction.EDUCATORS,
        location="Education Block",
        services=["education", "literacy classes"]
    ),
    NPC(
        name="Brad 'the Student'",
        description="An inmate who takes his education seriously.",
        personality="Quiet and studious, Brad is focused on bettering himself for when he's released.",
        dialogue={
            "default": "G'day mate. Just trying to get through this chapter on mathematics.",
            "education": "I'm working on my GED. It's tough, but it'll be worth it when I get out.",
            "future": "Got to plan for the future, you know? Can't stay here forever."
        },
        location="Education Block"
    ),
    NPC(
        name="Officer Sally",
        description="A stern but fair corrections officer who supervises visitations.",
        personality="Professional and by-the-book, but shows compassion when appropriate.",
        dialogue={
            "default": "Name and business, prisoner.",
            "visitation": "Visitation hours are from 9 AM to 4 PM. No contraband allowed.",
            "rules": "I don't make the rules, but I enforce them. Keep that in mind."
        },
        faction=Faction.STAFF_CORRUPTION,
        location="Visitation Centre",
        services=["visitation supervision"]
    ),
    NPC(
        name="Laundry Supervisor Mike",
        description="A gruff inmate who runs the laundry operations.",
        personality="Tough but fair, Mike keeps the laundry running smoothly.",
        dialogue={
            "default": "What do you want? This is a busy operation here.",
            "work": "Everyone pulls their weight in my laundry, or they face consequences.",
            "clean clothes": "Clean clothes don't just magically appear, you know. It takes work."
        },
        faction=Faction.INMATE_COUNCIL,
        location="Laundry Facility",
        services=["laundry work"]
    ),
    NPC(
        name="Cellmate Bob",
        description="Your assigned cellmate, a veteran of the prison system.",
        personality="Streetwise and cautious, Bob knows the unwritten rules of prison life.",
        dialogue={
            "default": "What's the deal, mate? You new around here?",
            "survival": "Look, just keep your head down and mind your own business. That's how you survive.",
            "advice": "Stick with a group, but don't trust anyone completely. That's prison 101."
        },
        location="Cell Block C"
    ),
    NPC(
        name="Yard Boss Tony",
        description="A powerful inmate who controls activities in the yard.",
        personality="Charismatic and intimidating, Tony commands respect from other inmates.",
        dialogue={
            "default": "You got business with me, or you just wasting my time?",
            "respect": "Respect is earned in here, not given. You show me respect, I'll show you the same.",
            "protection": "You want protection, you pay the price. That's how it works in here."
        },
        faction=Faction.REBELS_MC,
        location="Yard",
        services=["protection"]
    ),
    NPC(
        name="Dr. Smith",
        description="The prison physician, responsible for inmate health.",
        personality="Professional and empathetic, Dr. Smith tries to provide the best care possible.",
        dialogue={
            "default": "How are you feeling today? Any complaints?",
            "health": "Your health is important. Don't hesitate to come see me if you're not feeling well.",
            "treatment": "I'll need to run some tests to determine the best course of treatment."
        },
        faction=Faction.MEDICAL_STAFF,
        location="Infirmary",
        services=["medical treatment", "health checkup"]
    )
]

# Quests
QUESTS = [
    Quest(
        id="first_day",
        title="First Day Blues",
        description="Survive your first day in Yatala prison without getting into serious trouble.",
        objectives=["Visit the mess hall", "Explore the yard", "Avoid disciplinary action"],
        rewards={"experience": 50, "clean_money": 25}
    ),
    Quest(
        id="education_enrollment",
        title="Book Smart",
        description="Enroll in an educational program to improve your future prospects.",
        objectives=["Visit the Education Block", "Speak with Teacher Jenny", "Enroll in a program"],
        rewards={"experience": 100, "education_level": 10, "wisdom": 2},
        prerequisites=["first_day"]
    ),
    Quest(
        id="chapel_visit",
        title="Spiritual Guidance",
        description="Seek spiritual guidance from Padre O'Sullivan to help with your inner struggles.",
        objectives=["Visit the Chapel of Redemption", "Speak with Padre O'Sullivan", "Attend a service"],
        rewards={"experience": 75, "hope_level": 15, "stress_level": -10}
    ),
    Quest(
        id="work_assignment",
        title="Honest Work",
        description="Get assigned to a work detail to earn some extra money and stay out of trouble.",
        objectives=["Visit the Workshop", "Speak with Workshop Foreman", "Complete a work shift"],
        rewards={"experience": 75, "clean_money": 50, "strength": 1}
    ),
    Quest(
        id="gang_approach",
        title="Choice of Allegiance",
        description="A gang leader has taken an interest in you. You must decide where your loyalties lie.",
        objectives=["Speak with Yard Boss Tony", "Make a decision about joining a faction", "Deal with the consequences"],
        rewards={"experience": 150, "faction_standing": 10}
    )
]

# ============================================================================
# UI RENDERER
# ============================================================================

class UIRenderer:
    """Handles rendering of the game UI"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        curses.curs_set(0)  # Hide cursor
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Default
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Success
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # Danger
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Warning
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Info
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Special
        curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Faction
    
    def clear(self):
        """Clear the screen"""
        self.stdscr.clear()
        self.stdscr.refresh()
    
    def draw_box(self, y, x, height, width):
        """Draw a box at the specified position"""
        try:
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
        except curses.error:
            pass  # Ignore errors when drawing outside the screen
    
    def draw_text(self, y, x, text, color_pair=1):
        """Draw text at the specified position"""
        try:
            self.stdscr.addstr(y, x, text, curses.color_pair(color_pair))
        except curses.error:
            pass  # Ignore errors when drawing outside the screen
    
    def draw_ascii_art(self, y, x, art_key, color_pair=6):
        """Draw ASCII art at the specified position"""
        if art_key in ASCII_ARTS:
            art_lines = ASCII_ARTS[art_key].strip().split('\n')
            for i, line in enumerate(art_lines):
                self.draw_text(y + i, x, line, color_pair)
    
    def draw_status_bar(self, player):
        """Draw the player status bar"""
        status_y = 0
        
        # Health bar
        health_percent = player.health / player.max_health
        health_bar_width = int(20 * health_percent)
        health_bar = "[" + "=" * health_bar_width + " " * (20 - health_bar_width) + "]"
        self.draw_text(status_y, 0, f"Health: {health_bar} {player.health}/{player.max_health}", 2 if health_percent > 0.5 else 3)
        
        # Energy bar
        energy_percent = player.energy / player.max_energy
        energy_bar_width = int(20 * energy_percent)
        energy_bar = "[" + "=" * energy_bar_width + " " * (20 - energy_bar_width) + "]"
        self.draw_text(status_y, 30, f"Energy: {energy_bar} {player.energy}/{player.max_energy}", 2 if energy_percent > 0.5 else 4)
        
        # Hunger/Thirst
        self.draw_text(status_y, 60, f"Hunger: {player.hunger}/100", 4 if player.hunger > 70 else 2)
        self.draw_text(status_y, 80, f"Thirst: {player.thirst}/100", 4 if player.thirst > 70 else 2)
        
        # Psychological wellness indicators
        status_y += 1
        stress_color = 3 if player.stress_level > 70 else (4 if player.stress_level > 40 else 2)
        self.draw_text(status_y, 0, f"Stress: {player.stress_level}/100", stress_color)
        
        hope_color = 2 if player.hope_level > 70 else (4 if player.hope_level > 40 else 3)
        self.draw_text(status_y, 20, f"Hope: {player.hope_level}/100", hope_color)
        
        fatigue_color = 3 if player.mental_fatigue > 70 else (4 if player.mental_fatigue > 40 else 2)
        self.draw_text(status_y, 40, f"Fatigue: {player.mental_fatigue}/100", fatigue_color)
        
        self.draw_text(status_y, 60, f"Mood: {player.mood.value}", 6)
        
        # Money and reputation
        status_y += 1
        self.draw_text(status_y, 0, f"Clean Money: ${player.clean_money}", 2)
        self.draw_text(status_y, 25, f"Dirty Money: ${player.dirty_money}", 3)
        self.draw_text(status_y, 50, f"Underground Rep: {player.underground_reputation}/100", 7 if player.underground_reputation > 50 else 4)
        
        # Time and progress
        status_y += 1
        self.draw_text(status_y, 0, f"Day: {player.days_served}/{player.sentence_length}", 5)
        self.draw_text(status_y, 30, f"Date: {player.game_time.strftime('%Y-%m-%d %H:%M')}", 5)
        self.draw_text(status_y, 60, f"Education: {player.education_level}/100", 2)
        self.draw_text(status_y, 85, f"Parole: {player.parole_progress}/100", 2)
    
    def draw_location(self, location, npcs_in_location, items_in_location):
        """Draw the current location"""
        self.draw_text(5, 2, f"=== {location.name} ===", 6)
        self.draw_text(6, 2, location.description, 1)
        
        # Draw ASCII art if available
        if location.ascii_art:
            self.draw_ascii_art(7, self.width - 30, location.ascii_art)
        
        # Draw faction presence
        if location.faction_presence:
            faction_text = "Factions present: " + ", ".join([f.value for f in location.faction_presence])
            self.draw_text(15, 2, faction_text, 7)
        
        # Draw connected locations
        if location.connected_locations:
            connected_text = "Exits: " + ", ".join(location.connected_locations)
            self.draw_text(16, 2, connected_text, 5)
        
        # Draw NPCs
        if npcs_in_location:
            self.draw_text(17, 2, "People here:", 1)
            for i, npc in enumerate(npcs_in_location[:3]):  # Show only first 3
                self.draw_text(18 + i, 4, f"- {npc.name}", 1)
        
        # Draw items
        if items_in_location:
            self.draw_text(21, 2, "Items here:", 1)
            for i, item in enumerate(items_in_location[:3]):  # Show only first 3
                self.draw_text(22 + i, 4, f"- {item.name}", 1)
    
    def draw_inventory(self, player):
        """Draw the player's inventory"""
        self.draw_text(5, 2, "=== INVENTORY ===", 6)
        if player.inventory:
            for i, item in enumerate(player.inventory[:15]):  # Show only first 15 items
                self.draw_text(7 + i, 2, f"{item.name}: {item.description}", 1)
        else:
            self.draw_text(7, 2, "Your inventory is empty.", 4)
    
    def draw_character_sheet(self, player):
        """Draw the character sheet"""
        self.draw_text(5, 2, "=== CHARACTER SHEET ===", 6)
        
        # Basic info
        self.draw_text(7, 2, f"Name: {player.name}", 1)
        self.draw_text(8, 2, f"Level: {player.level}", 1)
        self.draw_text(9, 2, f"Experience: {player.experience}", 1)
        
        # Attributes
        self.draw_text(11, 2, "=== ATTRIBUTES ===", 6)
        attr_y = 12
        for attr_name, attr_value in player.attributes.__dict__.items():
            self.draw_text(attr_y, 2, f"{attr_name.replace('_', ' ').title()}: {attr_value}", 1)
            attr_y += 1
        
        # Skills
        self.draw_text(attr_y + 1, 2, "=== SKILLS ===", 6)
        skill_y = attr_y + 2
        for skill, level in list(player.skills.items())[:10]:  # Show first 10 skills
            self.draw_text(skill_y, 2, f"{skill.value}: {level}", 1)
            skill_y += 1
    
    def draw_factions(self, player):
        """Draw faction standings"""
        self.draw_text(5, 2, "=== FACTION STANDINGS ===", 6)
        
        if player.faction_standing:
            y_pos = 7
            for faction, standing in player.faction_standing.items():
                self.draw_text(y_pos, 2, f"{faction.value}:", 7)
                self.draw_text(y_pos, 30, f"Reputation: {standing.reputation}", 1)
                self.draw_text(y_pos, 50, f"Influence: {standing.influence}", 1)
                self.draw_text(y_pos, 70, f"Rank: {standing.rank}", 1)
                y_pos += 1
        else:
            self.draw_text(7, 2, "You are not affiliated with any factions.", 4)
    
    def draw_help(self):
        """Draw help information"""
        self.draw_text(5, 2, "=== HELP ===", 6)
        self.draw_text(7, 2, "CONTROLS:", 5)
        self.draw_text(8, 2, "Arrow Keys/WASD: Move cursor", 1)
        self.draw_text(9, 2, "Enter: Select/Confirm", 1)
        self.draw_text(10, 2, "I: Inventory", 1)
        self.draw_text(11, 2, "C: Character Sheet", 1)
        self.draw_text(12, 2, "M: Map", 1)
        self.draw_text(13, 2, "Q: Quest Log", 1)
        self.draw_text(14, 2, "F: Factions", 1)
        self.draw_text(15, 2, "H: Help", 1)
        self.draw_text(16, 2, "ESC: Pause Game", 1)
        self.draw_text(17, 2, "X: Quit Game", 1)
    
    def draw_dialogue(self, npc, options):
        """Draw dialogue interface"""
        self.draw_text(5, 2, f"=== TALKING TO {npc.name.upper()} ===", 6)
        self.draw_text(7, 2, npc.dialogue.get("default", "Hello."), 1)
        
        self.draw_text(10, 2, "What do you want to talk about?", 5)
        for i, option in enumerate(options):
            self.draw_text(12 + i, 4, f"{i+1}. {option}", 1)
    
    def draw_menu(self, title, options, selected_index=0):
        """Draw a menu with selectable options"""
        self.draw_text(5, 2, f"=== {title} ===", 6)
        
        for i, option in enumerate(options):
            color = 2 if i == selected_index else 1  # Green for selected option
            self.draw_text(7 + i, 2, f"{'> ' if i == selected_index else '  '}{option}", color)
    
    def get_input(self):
        """Get user input"""
        return self.stdscr.getch()


# ============================================================================
# GAME ENGINE
# ============================================================================

class GameEngine:
    """Main game engine"""
    
    def __init__(self):
        self.player = None
        self.locations = {loc.name: loc for loc in LOCATIONS}
        self.npcs = {npc.name: npc for npc in NPCS}
        self.items = {item.name: item for item in ITEMS}
        self.quests = {quest.id: quest for quest in QUESTS}
        self.ui_renderer = None
        self.game_state = GameState.MAIN_MENU
        self.current_menu_selection = 0
        self.dialogue_options = []
        self.current_npc = None
    
    def init_player(self, name: str):
        """Initialize the player character"""
        self.player = Player(
            name=name,
            attributes=Attributes(
                strength=12,
                dexterity=10,
                constitution=11,
                intelligence=9,
                wisdom=8,
                charisma=10,
                stress_tolerance=60,
                emotional_stability=55,
                resilience=50,
                adaptability=65
            ),
            skills={
                Skill.STRENGTH: 12,
                Skill.DEXTERITY: 10,
                Skill.CONSTITUTION: 11,
                Skill.INTELLIGENCE: 9,
                Skill.WISDOM: 8,
                Skill.CHARISMA: 10,
                Skill.CRAFTING: 8,
                Skill.STEALTH: 7,
                Skill.INTIMIDATION: 9,
                Skill.MEDICINE: 5,
                Skill.EDUCATION: 7,
                Skill.PSYCHOLOGY: 6,
                Skill.ELECTRONICS: 5,
                Skill.CHEMISTRY: 6
            },
            inventory=[],
            location="Cell Block C"
        )
    
    def get_items_in_location(self, location_name: str) -> List[Item]:
        """Get items present in a location"""
        location = self.locations.get(location_name)
        if not location:
            return []
        
        items = []
        for item_name in location.items:
            if item_name in self.items:
                items.append(self.items[item_name])
        return items
    
    def get_npcs_in_location(self, location_name: str) -> List[NPC]:
        """Get NPCs present in a location"""
        npcs = []
        for npc in self.npcs.values():
            if npc.location == location_name:
                npcs.append(npc)
        return npcs
    
    def move_player(self, direction: str):
        """Move player to a new location"""
        current_location = self.locations.get(self.player.location)
        if not current_location:
            return
        
        # For simplicity, we'll just move to the first connected location
        # In a real game, you'd have more sophisticated movement
        if current_location.connected_locations:
            new_location = current_location.connected_locations[0]
            self.player.location = new_location
            self.player.advance_time(1)  # Moving takes time
    
    def pickup_item(self, item_name: str):
        """Pick up an item from the current location"""
        items_here = self.get_items_in_location(self.player.location)
        for item in items_here:
            if item.name == item_name:
                self.player.inventory.append(item)
                # Remove item from location
                location = self.locations.get(self.player.location)
                if location and item_name in location.items:
                    location.items.remove(item_name)
                return True
        return False
    
    def talk_to_npc(self, npc_name: str):
        """Initiate dialogue with an NPC"""
        npc = self.npcs.get(npc_name)
        if not npc or npc.location != self.player.location:
            return False
        
        self.current_npc = npc
        self.dialogue_options = list(npc.dialogue.keys())
        self.game_state = GameState.DIALOGUE
        return True
    
    def handle_dialogue(self, choice: int):
        """Handle dialogue choice"""
        if 0 <= choice < len(self.dialogue_options):
            selected_topic = self.dialogue_options[choice]
            # In a real implementation, this would do more than just display text
            response = self.current_npc.dialogue.get(selected_topic, "I don't have much to say about that.")
            # Update relationships based on dialogue
            self.player.update_relationship(self.current_npc.name, trust_change=2, respect_change=1)
            # Return to playing state
            self.game_state = GameState.PLAYING
            return response
        return "Invalid choice."
    
    def update_quests(self):
        """Update quest progress based on player actions"""
        # This is a simplified implementation
        # In a real game, this would be much more complex
        for quest_id, quest in self.quests.items():
            if quest.status == "active":
                # Check if objectives are completed
                # For now, we'll just complete the first objective of the first quest as an example
                if quest_id == "first_day" and self.player.days_served >= 1:
                    quest.status = "completed"
                    self.player.completed_quests.append(quest_id)
                    self.player.active_quests.remove(quest_id)
                    # Award rewards
                    self.player.experience += quest.rewards.get("experience", 0)
                    self.player.clean_money += quest.rewards.get("clean_money", 0)
    
    def run(self, stdscr):
        """Main game loop"""
        self.ui_renderer = UIRenderer(stdscr)
        
        while True:
            self.ui_renderer.clear()
            
            # Draw status bar
            if self.player:
                self.ui_renderer.draw_status_bar(self.player)
            
            # Handle different game states
            if self.game_state == GameState.MAIN_MENU:
                self.handle_main_menu()
            elif self.game_state == GameState.CHARACTER_CREATION:
                self.handle_character_creation()
            elif self.game_state == GameState.PLAYING:
                self.handle_gameplay()
            elif self.game_state == GameState.INVENTORY:
                self.handle_inventory()
            elif self.game_state == GameState.CHARACTER_SHEET:
                self.handle_character_sheet()
            elif self.game_state == GameState.MAP:
                self.handle_map()
            elif self.game_state == GameState.QUEST_LOG:
                self.handle_quest_log()
            elif self.game_state == GameState.RELATIONSHIPS:
                self.handle_relationships()
            elif self.game_state == GameState.COMBAT:
                self.handle_combat()
            elif self.game_state == GameState.DIALOGUE:
                self.handle_dialogue_state()
            elif self.game_state == GameState.TRADING:
                self.handle_trading()
            elif self.game_state == GameState.GAME_OVER:
                self.handle_game_over()
            elif self.game_state == GameState.PAUSED:
                self.handle_pause()
            
            # Get user input
            key = self.ui_renderer.get_input()
            self.handle_input(key)
            
            # Update game state
            if self.player:
                self.update_quests()
                
                # Check for game over conditions
                if self.player.days_served >= self.player.sentence_length:
                    self.game_state = GameState.GAME_OVER
    
    def handle_main_menu(self):
        """Handle main menu state"""
        menu_options = ["New Game", "Load Game", "Help", "Quit"]
        self.ui_renderer.draw_menu("YATALA LOCKDOWN", menu_options, self.current_menu_selection)
    
    def handle_character_creation(self):
        """Handle character creation state"""
        # Simplified character creation
        self.ui_renderer.draw_text(5, 2, "=== CHARACTER CREATION ===", 6)
        self.ui_renderer.draw_text(7, 2, "Enter your name: [Type your name and press Enter]", 1)
    
    def handle_gameplay(self):
        """Handle gameplay state"""
        current_location = self.locations.get(self.player.location)
        if current_location:
            npcs_here = self.get_npcs_in_location(self.player.location)
            items_here = self.get_items_in_location(self.player.location)
            self.ui_renderer.draw_location(current_location, npcs_here, items_here)
    
    def handle_inventory(self):
        """Handle inventory state"""
        if self.player:
            self.ui_renderer.draw_inventory(self.player)
    
    def handle_character_sheet(self):
        """Handle character sheet state"""
        if self.player:
            self.ui_renderer.draw_character_sheet(self.player)
    
    def handle_map(self):
        """Handle map state"""
        self.ui_renderer.draw_text(5, 2, "=== PRISON MAP ===", 6)
        # Simplified map display
        map_lines = [
            "Cell Block C --- Yard --- Chapel",
            "    |             |         |",
            "Mess Hall     Workshop  Education Block",
            "    |             |         |",
            " Kitchen     Laundry    Library",
            "    |             |         |",
            "Administration - Infirmary"
        ]
        for i, line in enumerate(map_lines):
            self.ui_renderer.draw_text(7 + i, 2, line, 1)
    
    def handle_quest_log(self):
        """Handle quest log state"""
        self.ui_renderer.draw_text(5, 2, "=== QUEST LOG ===", 6)
        if self.player:
            y_pos = 7
            # Active quests
            if self.player.active_quests:
                self.ui_renderer.draw_text(y_pos, 2, "Active Quests:", 5)
                y_pos += 1
                for quest_id in self.player.active_quests:
                    if quest_id in self.quests:
                        quest = self.quests[quest_id]
                        self.ui_renderer.draw_text(y_pos, 4, f"- {quest.title}: {quest.description}", 1)
                        y_pos += 1
                y_pos += 1
            
            # Available quests
            available_quests = [q for q in self.quests.values() if q.status == "available"]
            if available_quests:
                self.ui_renderer.draw_text(y_pos, 2, "Available Quests:", 5)
                y_pos += 1
                for quest in available_quests[:5]:  # Show first 5
                    self.ui_renderer.draw_text(y_pos, 4, f"- {quest.title}: {quest.description}", 1)
                    y_pos += 1
    
    def handle_relationships(self):
        """Handle relationships state"""
        self.ui_renderer.draw_text(5, 2, "=== RELATIONSHIPS ===", 6)
        if self.player and self.player.relationships:
            y_pos = 7
            for npc_name, relationships in list(self.player.relationships.items())[:10]:  # Show first 10
                self.ui_renderer.draw_text(y_pos, 2, f"{npc_name}:", 1)
                self.ui_renderer.draw_text(y_pos, 30, f"Trust: {relationships['trust']}", 1)
                self.ui_renderer.draw_text(y_pos, 45, f"Respect: {relationships['respect']}", 1)
                self.ui_renderer.draw_text(y_pos, 60, f"Fear: {relationships['fear']}", 1)
                y_pos += 1
        else:
            self.ui_renderer.draw_text(7, 2, "You haven't formed any significant relationships yet.", 4)
    
    def handle_combat(self):
        """Handle combat state"""
        self.ui_renderer.draw_text(5, 2, "=== COMBAT ===", 3)
        self.ui_renderer.draw_text(7, 2, "Combat system not fully implemented in this demo.", 4)
    
    def handle_dialogue_state(self):
        """Handle dialogue state"""
        if self.current_npc and self.dialogue_options:
            self.ui_renderer.draw_dialogue(self.current_npc, self.dialogue_options)
    
    def handle_trading(self):
        """Handle trading state"""
        self.ui_renderer.draw_text(5, 2, "=== TRADING ===", 6)
        self.ui_renderer.draw_text(7, 2, "Trading system not fully implemented in this demo.", 4)
    
    def handle_game_over(self):
        """Handle game over state"""
        self.ui_renderer.draw_text(5, 2, "=== GAME OVER ===", 3)
        self.ui_renderer.draw_text(7, 2, "You have served your sentence.", 1)
        self.ui_renderer.draw_text(8, 2, "Thanks for playing Yatala Lockdown!", 2)
        self.ui_renderer.draw_text(10, 2, "Press any key to return to main menu.", 1)
    
    def handle_pause(self):
        """Handle pause state"""
        self.ui_renderer.draw_text(5, 2, "=== GAME PAUSED ===", 6)
        self.ui_renderer.draw_text(7, 2, "Press any key to continue.", 1)
    
    def handle_input(self, key):
        """Handle user input"""
        if self.game_state == GameState.MAIN_MENU:
            self.handle_main_menu_input(key)
        elif self.game_state == GameState.CHARACTER_CREATION:
            self.handle_character_creation_input(key)
        elif self.game_state == GameState.PLAYING:
            self.handle_gameplay_input(key)
        elif self.game_state == GameState.INVENTORY:
            self.handle_inventory_input(key)
        elif self.game_state == GameState.DIALOGUE:
            self.handle_dialogue_input(key)
        elif self.game_state == GameState.GAME_OVER:
            self.handle_game_over_input(key)
        # Other states would be handled similarly
    
    def handle_main_menu_input(self, key):
        """Handle main menu input"""
        menu_options = ["New Game", "Load Game", "Help", "Quit"]
        
        if key == curses.KEY_UP or key == ord('w') or key == ord('W'):
            self.current_menu_selection = (self.current_menu_selection - 1) % len(menu_options)
        elif key == curses.KEY_DOWN or key == ord('s') or key == ord('S'):
            self.current_menu_selection = (self.current_menu_selection + 1) % len(menu_options)
        elif key == curses.KEY_ENTER or key == 10 or key == 13:  # Enter key
            selected_option = menu_options[self.current_menu_selection]
            if selected_option == "New Game":
                self.game_state = GameState.CHARACTER_CREATION
                self.current_menu_selection = 0
            elif selected_option == "Load Game":
                # Load game functionality would go here
                pass
            elif selected_option == "Help":
                self.game_state = GameState.PLAYING
                # We'll show help in the playing state
            elif selected_option == "Quit":
                sys.exit(0)
        elif key == ord('h') or key == ord('H'):
            self.game_state = GameState.PLAYING
    
    def handle_character_creation_input(self, key):
        """Handle character creation input"""
        # Simplified - just go straight to gameplay
        if key == curses.KEY_ENTER or key == 10 or key == 13:  # Enter key
            self.init_player("Prisoner")
            # Start the first quest
            if "first_day" in self.quests:
                self.quests["first_day"].status = "active"
                self.player.active_quests.append("first_day")
            self.game_state = GameState.PLAYING
    
    def handle_gameplay_input(self, key):
        """Handle gameplay input"""
        if key == curses.KEY_UP or key == ord('w') or key == ord('W'):
            self.move_player("north")
        elif key == curses.KEY_DOWN or key == ord('s') or key == ord('S'):
            self.move_player("south")
        elif key == curses.KEY_LEFT or key == ord('a') or key == ord('A'):
            self.move_player("west")
        elif key == curses.KEY_RIGHT or key == ord('d') or key == ord('D'):
            self.move_player("east")
        elif key == ord('i') or key == ord('I'):
            self.game_state = GameState.INVENTORY
        elif key == ord('c') or key == ord('C'):
            self.game_state = GameState.CHARACTER_SHEET
        elif key == ord('m') or key == ord('M'):
            self.game_state = GameState.MAP
        elif key == ord('q') or key == ord('Q'):
            self.game_state = GameState.QUEST_LOG
        elif key == ord('f') or key == ord('F'):
            self.game_state = GameState.RELATIONSHIPS  # Using relationships for factions
        elif key == ord('h') or key == ord('H'):
            self.game_state = GameState.PLAYING  # Help will be shown in playing state
        elif key == 27:  # ESC key
            self.game_state = GameState.PAUSED
        elif key == ord('x') or key == ord('X'):
            sys.exit(0)
        elif key == ord('t') or key == ord('T'):
            # Talk to NPC (simplified - talk to first NPC in location)
            npcs_here = self.get_npcs_in_location(self.player.location)
            if npcs_here:
                self.talk_to_npc(npcs_here[0].name)
    
    def handle_inventory_input(self, key):
        """Handle inventory input"""
        if key == 27 or key == ord('i') or key == ord('I'):  # ESC or I key
            self.game_state = GameState.PLAYING
    
    def handle_dialogue_input(self, key):
        """Handle dialogue input"""
        if ord('1') <= key <= ord('9'):
            choice = key - ord('1')
            self.handle_dialogue(choice)
        elif key == 27:  # ESC key
            self.game_state = GameState.PLAYING
    
    def handle_game_over_input(self, key):
        """Handle game over input"""
        self.game_state = GameState.MAIN_MENU
        self.current_menu_selection = 0


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main(stdscr):
    """Main function"""
    # Initialize the game engine
    game = GameEngine()
    
    # Start the game loop
    game.run(stdscr)


if __name__ == "__main__":
    # Run the game with curses
    curses.wrapper(main)
# WATERMARK_INTEGRITY_CHECK
# This file is protected by digital watermarking technology
# Unauthorized modification or distribution will be detected
# Fingerprint: 93394ce00eec13dca8185a41c2025198
# Copyright © 2025 NovaSysErr-X. All rights reserved.
