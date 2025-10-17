# PRISON BREAK - Installation Guide

## Quick Start

### For Termux Users (Recommended)

```bash
# One-line installation
curl -O https://raw.githubusercontent.com/yourusername/prison-break/main/install.sh && chmod +x install.sh && ./install.sh
```

### For Linux Users

```bash
# Download installer
wget https://raw.githubusercontent.com/yourusername/prison-break/main/install.sh

# Make executable
chmod +x install.sh

# Run installer
./install.sh
```

## Detailed Installation

### Step 1: Prerequisites

#### Termux
```bash
# Update packages
pkg update && pkg upgrade

# Install Python (if not installed)
pkg install python

# Verify installation
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
# Update system
sudo apt update

# Install Python
sudo apt install python3

# Verify installation
python3 --version
```

#### Linux (Fedora)
```bash
# Install Python
sudo dnf install python3

# Verify installation
python3 --version
```

#### Linux (Arch)
```bash
# Install Python
sudo pacman -S python

# Verify installation
python3 --version
```

### Step 2: Download Game

#### Method 1: Using Installer (Recommended)
```bash
# Download installer
curl -O https://raw.githubusercontent.com/yourusername/prison-break/main/install.sh

# Or use wget
wget https://raw.githubusercontent.com/yourusername/prison-break/main/install.sh

# Make executable
chmod +x install.sh

# Run installer
./install.sh
```

#### Method 2: Manual Download
```bash
# Download game file
curl -O https://raw.githubusercontent.com/yourusername/prison-break/main/prison_break.py

# Or use wget
wget https://raw.githubusercontent.com/yourusername/prison-break/main/prison_break.py

# Make executable
chmod +x prison_break.py
```

#### Method 3: Git Clone
```bash
# Clone repository
git clone https://github.com/yourusername/prison-break.git

# Enter directory
cd prison-break

# Run installer
./install.sh
```

### Step 3: Verify Installation

```bash
# Check if game is installed
which prison-break

# Or check file directly
ls -la ~/.local/share/prison_break/prison_break.py

# Test run
python3 ~/.local/share/prison_break/prison_break.py
```

### Step 4: First Run

```bash
# Run game
prison-break

# Or run directly
python3 ~/.local/share/prison_break/prison_break.py
```

## Installation Locations

### Game Files
```
~/.local/share/prison_break/
├── prison_break.py          # Main game file
├── save_0.json              # Save slot 0
├── save_1.json              # Save slot 1
├── save_2.json              # Save slot 2
├── save_3.json              # Save slot 3
├── save_4.json              # Save slot 4
└── README.txt               # Documentation
```

### Configuration
```
~/.config/prison_break/
└── (future configuration files)
```

### Launcher
```
~/.local/bin/
└── prison-break             # Launcher script
```

## Troubleshooting Installation

### Python Not Found

**Problem**: `python3: command not found`

**Solution**:
```bash
# Termux
pkg install python

# Ubuntu/Debian
sudo apt install python3

# Fedora
sudo dnf install python3

# Arch
sudo pacman -S python
```

### Permission Denied

**Problem**: `Permission denied` when running installer

**Solution**:
```bash
# Make installer executable
chmod +x install.sh

# Run installer
./install.sh
```

### Command Not Found After Installation

**Problem**: `prison-break: command not found`

**Solution**:
```bash
# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Reload shell configuration
source ~/.bashrc

# Or run directly
python3 ~/.local/share/prison_break/prison_break.py
```

### Installer Fails

**Problem**: Installer script fails

**Solution**:
```bash
# Manual installation
mkdir -p ~/.local/share/prison_break
mkdir -p ~/.local/bin
cp prison_break.py ~/.local/share/prison_break/
chmod +x ~/.local/share/prison_break/prison_break.py

# Create launcher
cat > ~/.local/bin/prison-break << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/prison_break"
python3 prison_break.py
EOF

chmod +x ~/.local/bin/prison-break
```

### Terminal Too Small

**Problem**: Game displays incorrectly

**Solution**:
- Resize terminal to at least 80x24
- Recommended: 120x40 or larger
- Check terminal settings

### Display Issues

**Problem**: Garbled or incorrect display

**Solution**:
```bash
# Check terminal type
echo $TERM

# Try different terminal
# Termux: Use Termux app
# Linux: Try gnome-terminal, xterm, or konsole

# Check color support
tput colors
```

## Uninstallation

### Complete Removal

```bash
# Remove game files
rm -rf ~/.local/share/prison_break

# Remove configuration
rm -rf ~/.config/prison_break

# Remove launcher
rm ~/.local/bin/prison-break

# Remove desktop entry (if exists)
rm ~/.local/share/applications/prison-break.desktop
```

### Keep Save Files

```bash
# Backup saves
cp ~/.local/share/prison_break/save_*.json ~/prison_break_saves/

# Remove game
rm -rf ~/.local/share/prison_break
rm ~/.local/bin/prison-break

# Restore saves later
mkdir -p ~/.local/share/prison_break
cp ~/prison_break_saves/save_*.json ~/.local/share/prison_break/
```

## Updating

### Update to New Version

```bash
# Backup saves
cp ~/.local/share/prison_break/save_*.json ~/backup/

# Download new version
curl -O https://raw.githubusercontent.com/yourusername/prison-break/main/prison_break.py

# Replace old version
cp prison_break.py ~/.local/share/prison_break/

# Restore saves
cp ~/backup/save_*.json ~/.local/share/prison_break/
```

### Check Version

```bash
# Run game and check main menu
prison-break

# Or check file directly
head -n 20 ~/.local/share/prison_break/prison_break.py | grep Version
```

## Advanced Installation

### Custom Installation Directory

```bash
# Set custom directory
INSTALL_DIR="/custom/path/prison_break"

# Create directory
mkdir -p "$INSTALL_DIR"

# Copy game
cp prison_break.py "$INSTALL_DIR/"

# Create launcher
cat > ~/.local/bin/prison-break << EOF
#!/bin/bash
cd "$INSTALL_DIR"
python3 prison_break.py
EOF

chmod +x ~/.local/bin/prison-break
```

### System-Wide Installation (Linux)

```bash
# Install for all users (requires sudo)
sudo mkdir -p /opt/prison_break
sudo cp prison_break.py /opt/prison_break/
sudo chmod +x /opt/prison_break/prison_break.py

# Create system-wide launcher
sudo cat > /usr/local/bin/prison-break << 'EOF'
#!/bin/bash
cd /opt/prison_break
python3 prison_break.py
EOF

sudo chmod +x /usr/local/bin/prison-break
```

### Portable Installation

```bash
# Create portable directory
mkdir prison_break_portable
cd prison_break_portable

# Download game
curl -O https://raw.githubusercontent.com/yourusername/prison-break/main/prison_break.py

# Create run script
cat > run.sh << 'EOF'
#!/bin/bash
python3 prison_break.py
EOF

chmod +x run.sh

# Run from anywhere
./run.sh
```

## Platform-Specific Notes

### Termux (Android)

- **Storage**: Game uses ~1MB + save files
- **Performance**: Optimized for mobile
- **Battery**: Minimal battery usage
- **Permissions**: No special permissions needed

### Linux Desktop

- **Terminal**: Use any terminal emulator
- **Display**: Works best with 256-color support
- **Integration**: Desktop entry created automatically
- **Shortcuts**: Can create custom keyboard shortcuts

### SSH/Remote

- **Works**: Fully functional over SSH
- **Screen/Tmux**: Compatible with terminal multiplexers
- **Latency**: Playable with reasonable latency
- **Bandwidth**: Minimal bandwidth usage

## Verification

### Test Installation

```bash
# Test game starts
prison-break

# Should see main menu
# Press 4 to quit

# Test save directory
ls -la ~/.local/share/prison_break/

# Test launcher
which prison-break
```

### Verify Dependencies

```bash
# Check Python version (should be 3.9+)
python3 --version

# Check curses support
python3 -c "import curses; print('Curses OK')"

# Check JSON support
python3 -c "import json; print('JSON OK')"
```

## Getting Help

### Installation Issues

1. Check this guide thoroughly
2. Verify Python version (3.9+)
3. Check terminal compatibility
4. Review error messages
5. Try manual installation

### Support Resources

- **README.md**: General information
- **GAMEPLAY_GUIDE.md**: How to play
- **TECHNICAL_DOCUMENTATION.md**: Technical details
- **GitHub Issues**: Report problems
- **Community**: Ask for help

## Next Steps

After successful installation:

1. **Read README.md**: Understand the game
2. **Read GAMEPLAY_GUIDE.md**: Learn to play
3. **Start Game**: Run `prison-break`
4. **Create Character**: Follow tutorial
5. **Enjoy**: Have fun in prison!

---

**Installation Support**: For help, see README.md or open an issue
**Version**: 1.0.0
**Last Updated**: January 2025