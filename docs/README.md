# YATALA LOCKDOWN: Adelaide Northern Suburbs Prison Simulation

![Version](https://img.shields.io/badge/version-0.5.0%20beta-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A sophisticated, feature-rich CLI-based prison survival RPG game designed for Termux and Linux terminals. Experience life behind bars with deep gameplay mechanics, complex character progression, and meaningful choices.

## 🎮 Features

### Core Gameplay
- **Immersive Prison Life**: Navigate a detailed prison environment with multiple locations
- **Character Progression**: Level up, improve skills, and develop your inmate
- **Dynamic World**: Time-based events, NPC schedules, and realistic prison routines
- **Multiple Endings**: Survive, thrive, or escape - your choices matter

### Advanced Systems
- **Gang System**: Join one of four gangs or stay independent
  - The Brotherhood (Protection & Drugs)
  - Los Hermanos (Smuggling Network)
  - The Nation (Respect & Combat)
  - The Syndicate (Business & Connections)

- **Combat System**: Turn-based tactical combat with multiple actions
  - Brawling, weapons, dirty fighting
  - Skill-based damage calculation
  - Critical hits and special moves

- **Economy & Trading**: 
  - Multiple currencies (money, cigarettes, favors)
  - Contraband system
  - NPC trading with relationship-based prices
  - Black market access

- **Job System**: Work prison jobs to earn money
  - Kitchen duty, laundry, library, workshop, gym
  - Each job has unique benefits and requirements

- **Relationship System**: Build relationships with inmates and guards
  - Dynamic reputation system
  - Friendship, rivalry, and betrayal
  - Relationship affects gameplay opportunities

- **Quest System**: Main storyline and side quests
  - Multiple solution paths
  - Consequences for choices
  - Hidden objectives

- **Random Events**: Dynamic world with unpredictable occurrences
  - Guard shakedowns
  - Prison fights
  - Contraband opportunities
  - New arrivals

### Technical Excellence
- **Zero Dependencies**: Uses only Python standard library
- **Production-Grade Code**: 
  - Comprehensive type hints
  - Robust error handling
  - Clean architecture
  - Extensive documentation

- **Save System**: 
  - Multiple save slots
  - Auto-save functionality
  - JSON-based persistence
  - Save file versioning

- **Optimized for Termux**: 
  - Efficient rendering
  - Mobile-friendly controls
  - Adaptive UI
  - Low resource usage

## 📦 Installation

### Quick Install (Recommended)

```bash
# Download and run the installer
curl -O https://raw.githubusercontent.com/yourusername/prison-break/main/install.sh
chmod +x install.sh
./install.sh
```

### Manual Installation

```bash
# 1. Download the game
wget https://raw.githubusercontent.com/yourusername/prison-break/main/prison_break.py

# 2. Make it executable
chmod +x prison_break.py

# 3. Run the game
python3 prison_break.py
```

### Termux Installation

```bash
# 1. Install Python (if not already installed)
pkg install python

# 2. Download and install
curl -O https://raw.githubusercontent.com/yourusername/prison-break/main/install.sh
chmod +x install.sh
./install.sh

# 3. Start playing
prison-break
```

## 🎯 How to Play

### Starting the Game

```bash
# If installed via installer
prison-break

# Or run directly
python3 prison_break.py
```

### Controls

#### Main Controls
- **Arrow Keys / WASD**: Navigate menus
- **Number Keys (1-9)**: Select options
- **Enter**: Confirm selection
- **ESC**: Pause menu / Go back

#### Quick Access
- **I**: Open inventory
- **C**: View character sheet
- **M**: View map
- **Q**: Quest log
- **R**: Relationships
- **S**: Save game

### Gameplay Tips

1. **Manage Your Stats**: Keep health, energy, and hunger in check
2. **Build Reputation**: Respect is everything in prison
3. **Choose Allies Wisely**: Not everyone can be trusted
4. **Join a Gang**: Protection and resources, but with obligations
5. **Complete Quests**: Main storyline and side quests for rewards
6. **Trade Smart**: Build trading relationships for better deals
7. **Learn Skills**: Practice makes perfect - use skills to improve them
8. **Save Often**: Use multiple save slots for different playthroughs

## 🎨 Game Mechanics

### Character Attributes

**Physical**
- Strength: Combat damage, intimidation, physical labor
- Stamina: Energy pool, work capacity
- Health: Hit points
- Toughness: Damage resistance

**Mental**
- Intelligence: Learning speed, crafting quality
- Willpower: Resist intimidation, addiction
- Sanity: Mental health
- Perception: Notice details, critical hits

**Social**
- Charisma: Persuasion, making friends
- Intimidation: Scare others
- Reputation: Overall standing
- Respect: How much others value you

### Skills (0-100)

**Combat**: Brawling, Knife Fighting, Defense, Dirty Fighting
**Survival**: Stealth, Lockpicking, First Aid, Cooking
**Social**: Persuasion, Intimidation, Deception, Leadership
**Practical**: Crafting, Trading, Smuggling, Planning

### Time System

- **Daily Schedule**: 
  - 06:00 - Wake up, breakfast
  - 08:00 - Morning activities
  - 12:00 - Lunch
  - 13:00 - Afternoon activities
  - 17:00 - Dinner
  - 18:00 - Evening free time
  - 22:00 - Lockdown

- **Time Progression**: Actions take time, plan accordingly
- **Events**: Time-based random events and opportunities

## 📊 System Requirements

### Minimum Requirements
- **OS**: Termux (Android 7+) or Linux
- **Python**: 3.9 or higher
- **Terminal**: 80x24 minimum (larger recommended)
- **Storage**: 1 MB for game + save files

### Recommended
- **Terminal**: 120x40 or larger
- **Colors**: 256-color support
- **Font**: Monospace font with Unicode support

## 🗂️ File Structure

```
~/.local/share/prison_break/
├── prison_break.py          # Main game file
├── save_0.json              # Save slot 0
├── save_1.json              # Save slot 1
└── README.txt               # Documentation

~/.config/prison_break/
└── (future config files)

~/.local/bin/
└── prison-break             # Launcher script
```

## 🔧 Troubleshooting

### Game Won't Start
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Run with error output
python3 prison_break.py 2>&1 | tee error.log
```

### Display Issues
- Ensure terminal is at least 80x24
- Check terminal color support
- Try different terminal emulators

### Save File Issues
```bash
# Check save directory
ls -la ~/.local/share/prison_break/

# Backup saves
cp ~/.local/share/prison_break/save_*.json ~/backup/
```

### Performance Issues
- Close other applications
- Reduce terminal size if too large
- Disable animations (future feature)

## 🎓 Development

### Code Quality Standards

This game follows production-grade development practices:

- **Type Safety**: Comprehensive type hints throughout
- **Error Handling**: Robust exception handling
- **Documentation**: Extensive inline documentation
- **Architecture**: Clean, modular design
- **Testing**: Designed for testability
- **Performance**: Optimized for mobile devices

### Code Structure

```python
# Main Components
- Game Engine: Core game logic and state management
- UI Renderer: Terminal rendering and display
- Game Systems: Combat, trading, gangs, jobs, events
- Data Classes: Type-safe data structures
- Save System: JSON-based persistence
```

## 📝 Changelog

### Version 1.0.0 (2025-01-15)
- Initial release
- Complete core gameplay
- Gang system
- Combat system
- Trading system
- Job system
- Quest system
- Event system
- Save/load functionality
- Full Termux compatibility

## 🤝 Contributing

Contributions are welcome! Areas for contribution:
- New quests and storylines
- Additional NPCs and dialogue
- More random events
- Balance improvements
- Bug fixes
- Documentation improvements

## 📜 License

MIT License - See LICENSE file for details

## 🙏 Credits

**Developed by**: NovaSysErr-X
**Version**: 0.5.0 beta
**Release Date**: October 2025

### Inspiration
- Classic text-based RPGs
- Prison Architect
- The Escapists
- Interactive fiction games

### Special Thanks
- The Termux community
- Python curses library maintainers
- All playtesters and contributors

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation
- Review troubleshooting section

## 🎮 Enjoy Your Sentence!

Remember: In prison, respect is everything. Choose your allies wisely, watch your back, and maybe... just maybe... you'll make it out alive.

Good luck, inmate. You're going to need it.

---

**Note**: This is a game. Any resemblance to real persons, places, or events is purely coincidental. Play responsibly.