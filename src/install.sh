#!/bin/bash
# Prison Break - Installation Script for Termux
# This script sets up the game with zero configuration required

set -e

echo "=========================================="
echo "  PRISON BREAK - Installation Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on Termux
if [ -d "$PREFIX" ]; then
    echo -e "${GREEN}✓ Detected Termux environment${NC}"
    IS_TERMUX=true
else
    echo -e "${YELLOW}⚠ Not running on Termux, but will continue...${NC}"
    IS_TERMUX=false
fi

# Check Python version
echo ""
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python 3 found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found!${NC}"
    echo ""
    if [ "$IS_TERMUX" = true ]; then
        echo "Installing Python 3..."
        pkg install python -y
    else
        echo "Please install Python 3.9 or higher:"
        echo "  Ubuntu/Debian: sudo apt install python3"
        echo "  Fedora: sudo dnf install python3"
        echo "  Arch: sudo pacman -S python"
        exit 1
    fi
fi

# Create directories
echo ""
echo "Creating game directories..."
INSTALL_DIR="$HOME/.local/share/prison_break"
CONFIG_DIR="$HOME/.config/prison_break"
BIN_DIR="$HOME/.local/bin"

mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$BIN_DIR"

echo -e "${GREEN}✓ Directories created${NC}"

# Copy game file
echo ""
echo "Installing game files..."
if [ -f "prison_break.py" ]; then
    cp prison_break.py "$INSTALL_DIR/prison_break.py"
    chmod +x "$INSTALL_DIR/prison_break.py"
    echo -e "${GREEN}✓ Game files installed${NC}"
else
    echo -e "${RED}✗ prison_break.py not found!${NC}"
    exit 1
fi

# Create launcher script
echo ""
echo "Creating launcher..."
cat > "$BIN_DIR/prison-break" << 'EOF'
#!/bin/bash
# Prison Break Launcher
cd "$HOME/.local/share/prison_break"
python3 prison_break.py
EOF

chmod +x "$BIN_DIR/prison-break"
echo -e "${GREEN}✓ Launcher created${NC}"

# Add to PATH if needed
echo ""
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "Adding $BIN_DIR to PATH..."
    
    if [ "$IS_TERMUX" = true ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        if [ -f "$HOME/.bashrc" ]; then
            SHELL_RC="$HOME/.bashrc"
        elif [ -f "$HOME/.zshrc" ]; then
            SHELL_RC="$HOME/.zshrc"
        else
            SHELL_RC="$HOME/.profile"
        fi
    fi
    
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
    echo -e "${GREEN}✓ PATH updated in $SHELL_RC${NC}"
    echo -e "${YELLOW}⚠ Please run: source $SHELL_RC${NC}"
else
    echo -e "${GREEN}✓ PATH already configured${NC}"
fi

# Create desktop entry (if not Termux)
if [ "$IS_TERMUX" = false ] && [ -d "$HOME/.local/share/applications" ]; then
    echo ""
    echo "Creating desktop entry..."
    cat > "$HOME/.local/share/applications/prison-break.desktop" << EOF
[Desktop Entry]
Name=Prison Break
Comment=The Ultimate Inmate Simulation
Exec=$BIN_DIR/prison-break
Icon=utilities-terminal
Terminal=true
Type=Application
Categories=Game;
EOF
    echo -e "${GREEN}✓ Desktop entry created${NC}"
fi

# Create README
echo ""
echo "Creating documentation..."
cat > "$INSTALL_DIR/README.txt" << 'EOF'
PRISON BREAK - The Ultimate Inmate Simulation
==============================================

INSTALLATION COMPLETE!

To start the game, run:
    prison-break

Or directly:
    python3 ~/.local/share/prison_break/prison_break.py

CONTROLS:
- Arrow keys or WASD: Navigate
- Number keys: Select options
- I: Inventory
- C: Character sheet
- M: Map
- Q: Quest log
- R: Relationships
- S: Save game
- ESC: Pause menu

GAME FILES:
- Game data: ~/.local/share/prison_break/
- Save files: ~/.local/share/prison_break/save_*.json
- Config: ~/.config/prison_break/

UNINSTALL:
To remove the game:
    rm -rf ~/.local/share/prison_break
    rm -rf ~/.config/prison_break
    rm ~/.local/bin/prison-break

SUPPORT:
For issues or questions, check the documentation or
visit the project repository.

Enjoy your time in prison!
EOF

echo -e "${GREEN}✓ Documentation created${NC}"

# Final message
echo ""
echo "=========================================="
echo -e "${GREEN}✓ Installation Complete!${NC}"
echo "=========================================="
echo ""
echo "To start playing:"
echo -e "  ${YELLOW}prison-break${NC}"
echo ""
echo "Or run directly:"
echo -e "  ${YELLOW}python3 $INSTALL_DIR/prison_break.py${NC}"
echo ""
echo "Documentation: $INSTALL_DIR/README.txt"
echo ""
echo "Have fun surviving in prison!"
echo ""