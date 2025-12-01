#!/bin/bash
# SupportPilot Frontend Startup Script

set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/frontend" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}SupportPilot Frontend Startup${NC}"
echo -e "${BLUE}================================================${NC}\n"

# Check Node
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}✗ Node.js not found. Please install Node 18+${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"

# Install dependencies
if [ ! -d node_modules ]; then
    echo "Installing dependencies..."
    npm install
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

# Start dev server
echo -e "${BLUE}================================================${NC}"
echo -e "Frontend: http://localhost:3000"
echo -e "Backend: http://localhost:5001/api"
echo -e "${BLUE}================================================\n${NC}"

npm start
