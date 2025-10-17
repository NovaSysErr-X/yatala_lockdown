# Prison Break: The Ultimate Inmate Simulation - Complete Design Document

## Game Overview

**Title:** Prison Break: The Ultimate Inmate Simulation
**Genre:** Text-based RPG / Survival / Strategy
**Platform:** Termux (Android) / Linux Terminal
**Target:** Single-player, immersive prison life simulation

## Core Game Loop

1. **Wake Up** → Check status (health, hunger, energy)
2. **Daily Activities** → Work, socialize, trade, plan
3. **Events** → Random encounters, opportunities, threats
4. **Progression** → Build skills, reputation, resources
5. **Goal Pursuit** → Survive, thrive, or escape
6. **Sleep** → Day ends, time advances

## Game Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                        GAME ENGINE                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ State Manager│  │ Event System │  │  UI Renderer │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Input Handler │  │  Save/Load   │  │  Time System │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
├─────────────────────────────────────────────────────────────┤
│                      GAME SYSTEMS                           │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Character  │  │   Inventory  │  │  Reputation  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     Gang     │  │   Economy    │  │    Combat    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     Quest    │  │      NPC     │  │   Location   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
├─────────────────────────────────────────────────────────────┤
│                       GAME DATA                             │
├─────────────────────────────────────────────────────────────┤
│  • Player State    • World State    • NPC Database         │
│  • Item Database   • Quest Data     • Event Templates      │
│  • Location Data   • Gang Info      • Dialogue Trees       │
└─────────────────────────────────────────────────────────────┘
```

## Character System

### Attributes (0-100 scale)

**Physical Attributes**
- **Strength**: Affects combat damage, intimidation, physical labor
- **Stamina**: Determines energy pool, work capacity, fight duration
- **Health**: Current health points, affects all activities
- **Toughness**: Damage resistance, pain tolerance

**Mental Attributes**
- **Intelligence**: Learning speed, crafting quality, planning
- **Willpower**: Resist intimidation, addiction, mental breaks
- **Sanity**: Mental health, affects decision making
- **Perception**: Notice details, detect lies, find opportunities

**Social Attributes**
- **Charisma**: Persuasion, making friends, trading
- **Intimidation**: Scare others, gain respect through fear
- **Reputation**: Overall standing in prison hierarchy
- **Respect**: How much others value you

### Skills (0-100 scale, improve through use)

**Combat Skills**
- Brawling: Hand-to-hand fighting
- Knife Fighting: Shank combat
- Defense: Blocking and dodging
- Dirty Fighting: Cheap shots and tricks

**Survival Skills**
- Stealth: Avoid detection, sneak around
- Lockpicking: Open locked doors and containers
- First Aid: Heal injuries
- Cooking: Prepare better food

**Social Skills**
- Persuasion: Convince others
- Intimidation: Threaten effectively
- Deception: Lie convincingly
- Leadership: Command respect and followers

**Practical Skills**
- Crafting: Make items and weapons
- Trading: Better deals, spot fakes
- Smuggling: Hide and move contraband
- Planning: Organize complex operations

### Status Effects

**Positive**
- Well Fed: +10% to all stats
- Well Rested: +20% energy regeneration
- Pumped Up: +15% strength (from working out)
- Focused: +10% intelligence (from reading)
- Protected: Gang protection active
- High: Various effects from drugs

**Negative**
- Hungry: -20% to all stats
- Exhausted: -30% to physical stats
- Injured: -50% to physical activities
- Sick: -30% to all stats
- Addicted: Withdrawal penalties
- Marked: Target for violence
- Paranoid: -20% social interactions

### Character Progression

**Level System**
- Gain XP from activities, events, quests
- Level up grants attribute points
- Every 5 levels: unlock perk
- Max level: 50

**Perks (Choose one per 5 levels)**
- **Tough Guy**: +20% health, +10% toughness
- **Street Smart**: +15% to all social skills
- **Quick Learner**: +50% skill gain rate
- **Iron Will**: Immune to intimidation
- **Natural Leader**: Gang members more loyal
- **Smooth Talker**: Better trading prices
- **Shadow**: +30% stealth effectiveness
- **Brawler**: +25% unarmed damage
- **Survivor**: Heal faster, resist disease
- **Mastermind**: Better escape planning

## Location System

### Prison Layout

```
┌─────────────────────────────────────────────────────────┐
│                    PRISON COMPLEX                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Cell     │  │ Cell     │  │ Cell     │  [BLOCK A] │
│  │ Block A  │  │ Block B  │  │ Block C  │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│                                                         │
│  ┌──────────────────────────────────────┐             │
│  │         COMMON AREAS                 │             │
│  │  • Cafeteria    • Yard               │             │
│  │  • Library      • Gym                │             │
│  │  • Workshop     • Infirmary          │             │
│  │  • Showers      • Visitation         │             │
│  └──────────────────────────────────────┘             │
│                                                         │
│  ┌──────────────────────────────────────┐             │
│  │         RESTRICTED AREAS             │             │
│  │  • Guard Station  • Warden's Office  │             │
│  │  • Solitary       • Storage          │             │
│  │  • Maintenance    • Roof Access      │             │
│  └──────────────────────────────────────┘             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Location Properties

Each location has:
- **Name and Description**: Atmospheric text
- **NPCs Present**: Who you can interact with
- **Available Actions**: What you can do here
- **Danger Level**: Risk of violence/trouble
- **Guard Presence**: How many guards patrol
- **Time Restrictions**: When accessible
- **Connected Locations**: Where you can go

### Key Locations Detail

**Your Cell**
- Personal space, safest location
- Store hidden items
- Rest and sleep
- Plan activities
- Cellmate interactions

**Cafeteria**
- Eat meals (breakfast, lunch, dinner)
- Social hub, meet NPCs
- Trading spot
- Gang meetings
- Potential fights

**Yard**
- Exercise and build strength
- Gang territory battles
- Sports and gambling
- Contraband trading
- Escape planning

**Library**
- Read books (increase intelligence)
- Research and planning
- Quiet social interactions
- Hide contraband in books
- Access to information

**Gym**
- Build physical stats
- Meet tough inmates
- Show off strength
- Settle disputes
- Recruit gang members

**Workshop**
- Prison job location
- Craft items and weapons
- Learn skills
- Access to tools
- Smuggling opportunities

**Infirmary**
- Heal injuries
- Get medicine
- Medical job
- Drug access
- Fake illness

**Showers**
- Hygiene maintenance
- Vulnerable location
- Ambush spot
- Private conversations
- Hidden stashes

**Visitation**
- Meet visitors
- Receive items
- Get news from outside
- Emotional support
- Smuggling point

**Solitary Confinement**
- Punishment location
- Isolation effects
- Time to think/plan
- Sanity challenges
- Reputation impact

## Economy System

### Currencies

**Official Money**
- Earned from prison jobs
- Used at commissary
- Tracked by guards
- Limited amounts

**Cigarettes**
- Primary prison currency
- Widely accepted
- Tradeable commodity
- Can be smoked (addiction risk)

**Favors**
- Owed services
- Social currency
- Can't be stolen
- Reputation based

### Items and Trading

**Consumables**
- Food (various quality levels)
- Cigarettes (currency/consumable)
- Drugs (various types and effects)
- Medicine (healing items)
- Toiletries (hygiene)

**Contraband**
- Weapons (shanks, clubs, improvised)
- Drugs (marijuana, pills, harder stuff)
- Alcohol (pruno, smuggled liquor)
- Phones (communication, information)
- Tools (lockpicks, files, rope)

**Crafting Materials**
- Metal scraps
- Cloth and fabric
- Plastic pieces
- Paper and cardboard
- Chemicals and cleaners

**Books and Media**
- Skill books (increase learning)
- Entertainment (reduce stress)
- Porn (trade value)
- Maps and plans
- Letters and notes

### Trading Mechanics

**Barter System**
- Offer items for items
- Negotiate prices
- Reputation affects deals
- Can be scammed
- Build trading relationships

**Black Market**
- Access through connections
- Rare and valuable items
- Higher prices
- Risk of setup/raid
- Reputation required

**Commissary**
- Official prison store
- Limited selection
- Fair prices
- Safe transactions
- Requires money

## Gang System

### Available Gangs

**The Brotherhood** (White supremacist gang)
- Focus: Protection, drug trade
- Territory: Block A, Workshop
- Initiation: Prove loyalty, fight rival
- Benefits: Protection, drug access
- Drawbacks: Racial tensions, violent

**Los Hermanos** (Latino gang)
- Focus: Family, smuggling
- Territory: Block B, Kitchen
- Initiation: Family connection or prove worth
- Benefits: Smuggling network, loyalty
- Drawbacks: Blood in, blood out

**The Nation** (Black gang)
- Focus: Respect, organization
- Territory: Block C, Yard
- Initiation: Earn respect, complete task
- Benefits: Numbers, organization
- Drawbacks: Strict hierarchy

**The Syndicate** (Organized crime)
- Focus: Business, profit
- Territory: Visitation, Library
- Initiation: Prove usefulness
- Benefits: Resources, connections
- Drawbacks: Debt, obligations

**The Independents** (No gang)
- Focus: Freedom, flexibility
- Territory: None (neutral)
- Benefits: No obligations, flexibility
- Drawbacks: No protection, harder survival

### Gang Mechanics

**Joining Process**
1. Meet gang members
2. Build reputation with gang
3. Complete initiation task
4. Swear loyalty
5. Receive gang benefits

**Gang Ranks**
- Prospect: New member, proving worth
- Soldier: Full member, follow orders
- Lieutenant: Lead small operations
- Captain: Control territory
- Boss: Lead entire gang (rare)

**Gang Activities**
- Territory control and defense
- Contraband operations
- Protection rackets
- Revenge and retaliation
- Recruitment
- Planning operations

**Gang Conflicts**
- Territory disputes
- Revenge cycles
- Resource competition
- Disrespect incidents
- Leadership challenges

## Combat System

### Combat Types

**Brawling** (Unarmed)
- Quick, common fights
- Less lethal
- Builds reputation
- Can be broken up by guards

**Armed Combat** (Weapons)
- More dangerous
- Higher stakes
- Serious consequences
- Harder to stop

**Group Fights** (Gang warfare)
- Multiple participants
- Chaotic and dangerous
- Major reputation impact
- Lockdown risk

### Combat Mechanics

**Turn-Based System**
- Player chooses action
- Enemy responds
- Damage calculated
- Status effects applied
- Continue until victory/defeat/flee

**Actions**
- **Attack**: Standard damage
- **Heavy Attack**: More damage, less accurate
- **Defend**: Reduce incoming damage
- **Dodge**: Avoid attack completely
- **Dirty Move**: Cheap shot, high damage
- **Intimidate**: Scare opponent
- **Flee**: Escape combat (reputation loss)
- **Call for Help**: Gang members assist

**Damage Calculation**
```
Base Damage = Weapon Damage + (Strength / 10)
Skill Modifier = (Skill Level / 100) * Base Damage
Final Damage = (Base + Skill Modifier) - (Target Defense)
Critical Hit = Random(1-100) <= (Perception / 2)
```

**Combat Outcomes**
- **Victory**: Gain reputation, loot, respect
- **Defeat**: Lose items, reputation, health
- **Flee**: Lose reputation, avoid injury
- **Interrupted**: Guards break it up, both punished

### Weapons

**Improvised Weapons**
- Shank (sharpened metal): 15-25 damage
- Sock with soap: 10-20 damage
- Broken glass: 12-22 damage
- Sharpened toothbrush: 8-15 damage
- Lock in sock: 18-28 damage

**Crafted Weapons**
- Quality shank: 20-35 damage
- Shiv: 18-30 damage
- Club: 15-25 damage
- Garrote: 25-40 damage (stealth)
- Brass knuckles: 12-20 damage

**Rare Weapons**
- Real knife: 30-50 damage
- Razor blade: 20-35 damage
- Screwdriver: 22-38 damage

## Quest System

### Main Storyline Quests

**Act 1: Arrival and Survival**
1. **First Day**: Tutorial, learn basics
2. **Find Your Place**: Choose gang or independent
3. **Earn Respect**: Complete tasks for reputation
4. **The Shakedown**: Survive first major threat
5. **Establish Yourself**: Secure position in prison

**Act 2: Rising Through Ranks**
6. **Gang Initiation**: Join gang or build network
7. **Territory Wars**: Participate in conflicts
8. **The Big Score**: Major contraband operation
9. **Betrayal**: Someone turns on you
10. **Revenge**: Get even or show mercy

**Act 3: The Escape**
11. **The Plan**: Begin escape planning
12. **Gather Resources**: Collect needed items
13. **Build Team**: Recruit helpers
14. **The Attempt**: Execute escape plan
15. **Freedom or Death**: Final confrontation

### Side Quests

**Personal Quests**
- Help cellmate with problem
- Settle old scores
- Find lost items
- Deliver messages
- Protect someone

**Gang Quests**
- Recruit new members
- Eliminate rival
- Smuggle contraband
- Collect debts
- Defend territory

**Economic Quests**
- Build trading network
- Find rare items
- Start business
- Pay off debts
- Become wealthy

**Social Quests**
- Make friends
- Romance options
- Mentor newcomer
- Resolve conflicts
- Build reputation

### Quest Mechanics

**Quest Structure**
- Objective: What to accomplish
- Rewards: What you gain
- Consequences: What happens
- Time Limit: Deadline (if any)
- Difficulty: Challenge level

**Quest Outcomes**
- Success: Full rewards
- Partial Success: Reduced rewards
- Failure: Consequences
- Alternative Solutions: Creative approaches

## Event System

### Random Events

**Daily Events** (Common)
- Guard shakedown
- Meal quality variation
- Mail call
- Yard time weather
- Cellmate mood
- Minor conflicts
- Trading opportunities
- Rumors and gossip

**Weekly Events** (Uncommon)
- Visitor day
- Commissary restock
- New inmates arrive
- Guard rotation
- Contraband sweep
- Gang meeting
- Sports tournament
- Movie night

**Major Events** (Rare)
- Riot
- Lockdown
- Escape attempt (others)
- Gang war
- Warden inspection
- Celebrity inmate
- Natural disaster
- Mass punishment

### Event Triggers

**Time-Based**
- Daily schedule events
- Weekly occurrences
- Seasonal changes
- Anniversary events

**Action-Based**
- Player choices trigger events
- Reputation thresholds
- Gang activities
- Quest completion

**Random**
- Dice roll each day
- Weighted probabilities
- Chaos factor
- Luck attribute

### Event Consequences

**Immediate**
- Stat changes
- Item gains/losses
- Reputation shifts
- Location changes

**Long-Term**
- Relationship changes
- Gang standing
- Future opportunities
- Story branches

## NPC System

### NPC Types

**Inmates**
- **Cellmate**: Your roommate, constant presence
- **Gang Members**: Allies or enemies
- **Independents**: Neutral parties
- **Newcomers**: Fresh fish, vulnerable
- **Veterans**: Old timers, wise
- **Snitches**: Informants, dangerous
- **Crazy**: Unpredictable, avoid

**Guards**
- **Corrupt**: Can be bribed
- **Strict**: By the book
- **Brutal**: Violent and cruel
- **Lazy**: Easy to avoid
- **Fair**: Reasonable

**Staff**
- **Warden**: Prison boss
- **Doctor**: Medical care
- **Counselor**: Mental health
- **Chaplain**: Spiritual guidance
- **Cook**: Food service
- **Librarian**: Book access

### NPC Attributes

**Personality Traits**
- Aggressive/Peaceful
- Honest/Deceptive
- Loyal/Treacherous
- Smart/Dumb
- Brave/Cowardly

**Relationship Status**
- Stranger (0-20): Don't know you
- Acquaintance (21-40): Recognize you
- Friend (41-60): Like you
- Close Friend (61-80): Trust you
- Best Friend (81-100): Loyal ally
- Enemy (-100 to -1): Hostile

**NPC Needs**
- Protection
- Items
- Information
- Companionship
- Revenge

### Dialogue System

**Conversation Options**
- Greet: Start conversation
- Ask: Request information
- Trade: Barter items
- Threaten: Intimidate
- Persuade: Convince
- Joke: Build rapport
- Leave: End conversation

**Dialogue Trees**
- Branch based on choices
- Skill checks affect options
- Reputation gates content
- Multiple solutions
- Consequences remembered

## Time System

### Time Scale

**Daily Schedule**
- 06:00 - Wake up, breakfast
- 08:00 - Morning activities
- 12:00 - Lunch
- 13:00 - Afternoon activities
- 17:00 - Dinner
- 18:00 - Evening free time
- 22:00 - Lockdown, sleep

**Time Progression**
- Actions take time (minutes/hours)
- Can skip time (rest, wait)
- Events tied to time
- Schedules enforced
- Seasons change

### Activity Time Costs

**Quick Actions** (5-15 minutes)
- Conversations
- Quick trades
- Eating
- Moving between locations

**Medium Actions** (30-60 minutes)
- Working out
- Reading
- Crafting simple items
- Detailed planning

**Long Actions** (2-4 hours)
- Prison job shift
- Complex crafting
- Deep planning
- Extended socializing

**All Day Actions**
- Major operations
- Escape attempts
- Recovering from injury
- Solitary confinement

## Progression Systems

### Experience and Leveling

**XP Sources**
- Completing quests: 100-1000 XP
- Winning fights: 50-200 XP
- Successful trades: 10-50 XP
- Learning skills: 25-100 XP
- Surviving days: 10 XP/day
- Achievements: 50-500 XP

**Level Requirements**
```
Level 1-10: 100 XP per level
Level 11-20: 200 XP per level
Level 21-30: 400 XP per level
Level 31-40: 800 XP per level
Level 41-50: 1600 XP per level
```

### Skill Improvement

**Practice-Based**
- Use skill to improve
- Diminishing returns
- Faster at low levels
- Slower at high levels
- Can plateau without training

**Training**
- Learn from NPCs
- Read skill books
- Practice with equipment
- Costs time and resources

### Reputation Progression

**Reputation Levels**
- Nobody (0-10): Unknown
- Known (11-25): Recognized
- Respected (26-50): Valued
- Feared (51-75): Intimidating
- Legendary (76-100): Prison celebrity

**Reputation Gains**
- Win fights: +1-5
- Complete quests: +2-10
- Help others: +1-3
- Gang activities: +3-8
- Escape attempts: +10-20

**Reputation Losses**
- Lose fights: -2-5
- Snitch: -20-50
- Betray gang: -30-60
- Show weakness: -1-3
- Get caught: -5-15

## Save System

### Save Features

**Auto-Save**
- Saves every day at sleep
- Saves before major events
- Saves after quest completion
- Configurable frequency

**Manual Save**
- Save anytime (except combat)
- Multiple save slots (5)
- Named saves
- Save descriptions

**Save Data**
- Player character state
- Inventory contents
- NPC relationships
- World state
- Quest progress
- Time and date
- Statistics

### Data Persistence

**Save File Format**
```json
{
  "version": "1.0.0",
  "timestamp": "2025-01-15T10:30:00",
  "player": {
    "name": "John Doe",
    "level": 15,
    "attributes": {...},
    "skills": {...},
    "inventory": [...],
    "location": "cell_a1"
  },
  "world": {
    "day": 45,
    "time": "14:30",
    "npcs": {...},
    "gangs": {...},
    "events": [...]
  },
  "progress": {
    "quests": {...},
    "achievements": [...],
    "statistics": {...}
  }
}
```

## UI Design

### Main Screen Layout

```
┌─────────────────────────────────────────────────────────────┐
│ PRISON BREAK │ Day 45 │ 14:30 │ Cell Block A │ Level 15    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    MAIN VIEW                        │   │
│  │                                                     │   │
│  │  You are in your cell. Your cellmate, Marcus,      │   │
│  │  is lying on his bunk reading a magazine. The      │   │
│  │  cell is small but you've made it your own with    │   │
│  │  a few personal items. The door is locked.         │   │
│  │                                                     │   │
│  │  [1] Talk to Marcus                                │   │
│  │  [2] Check your stash                              │   │
│  │  [3] Work out (push-ups)                           │   │
│  │  [4] Read a book                                   │   │
│  │  [5] Rest until dinner                             │   │
│  │  [6] Check inventory                               │   │
│  │  [7] View character stats                          │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ HP: ████████░░ 80/100 │ Energy: ██████░░░░ 60/100         │
│ Hunger: ████░░░░░░ 40/100 │ Respect: ███████░░░ 75/100    │
├─────────────────────────────────────────────────────────────┤
│ > _                                                         │
└─────────────────────────────────────────────────────────────┘
```

### Screen Types

**Main Game Screen**
- Location description
- Available actions
- Status bars
- Command prompt

**Character Screen**
- Attributes and skills
- Status effects
- Equipment
- Statistics

**Inventory Screen**
- Item list
- Item details
- Use/drop/trade options
- Weight/capacity

**Map Screen**
- Prison layout
- Current location
- Available destinations
- Gang territories

**Quest Log**
- Active quests
- Completed quests
- Quest details
- Objectives

**Relationship Screen**
- NPC list
- Relationship levels
- Recent interactions
- Notes

### Color Scheme

**Status Colors**
- Green: Positive, healthy, safe
- Yellow: Warning, caution, neutral
- Red: Danger, injury, hostile
- Blue: Information, calm, friendly
- Magenta: Special, rare, important
- Cyan: System messages, help

**UI Elements**
- White: Normal text
- Gray: Disabled options
- Bold: Emphasis, headers
- Reverse: Selected items

## Technical Implementation

### Core Classes

```python
class Game:
    """Main game controller"""
    - state_manager
    - ui_renderer
    - input_handler
    - save_system
    - event_system

class Player:
    """Player character"""
    - attributes
    - skills
    - inventory
    - status_effects
    - relationships

class NPC:
    """Non-player character"""
    - personality
    - relationships
    - inventory
    - schedule
    - dialogue

class Location:
    """Game location"""
    - name
    - description
    - npcs_present
    - available_actions
    - connections

class Item:
    """Game item"""
    - name
    - description
    - type
    - value
    - effects

class Quest:
    """Quest/mission"""
    - objectives
    - rewards
    - status
    - consequences
```

### Data Flow

```
User Input → Input Handler → Game State → Event System
                                ↓
                          State Manager
                                ↓
                          UI Renderer → Display
                                ↓
                          Save System → Disk
```

## Conclusion

This comprehensive design document provides the complete blueprint for developing "Prison Break: The Ultimate Inmate Simulation" - a sophisticated, feature-rich CLI game that will set new standards for terminal-based gaming. The design balances complexity with usability, depth with accessibility, and realism with entertainment value.