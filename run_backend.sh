#!/bin/bash
# SupportPilot Backend Startup Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}SupportPilot Backend Startup${NC}"
echo -e "${BLUE}================================================${NC}\n"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠  .env file not found${NC}"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env created${NC}"
    echo -e "${YELLOW}⚠  Please edit .env with your Supabase credentials${NC}\n"
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python3 found${NC}"

# Check if venv exists
if [ ! -d venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate venv
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install/update requirements
echo "Installing dependencies..."
pip install -q -r backend/requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Find available port (use lsof if available, fallback to netstat)
PORT=${PORT:-5001}
is_port_in_use(){
    if command -v lsof >/dev/null 2>&1; then
        lsof -i TCP:"$1" -sTCP:LISTEN >/dev/null 2>&1 && return 0 || return 1
    else
        netstat -an 2>/dev/null | grep -E ":$1\b" >/dev/null 2>&1 && return 0 || return 1
    fi
}

while is_port_in_use $PORT; do
    echo -e "${YELLOW}⚠  Port $PORT is in use${NC}"
    PORT=$((PORT + 1))
done

echo -e "${GREEN}✓ Using port $PORT${NC}\n"

# Display environment info
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Configuration${NC}"
echo -e "${BLUE}================================================${NC}"
echo -e "Environment: ${FLASK_ENV:-development}"
echo -e "Supabase: ${SUPABASE_URL:+Connected}${SUPABASE_URL:-Demo Mode}"
echo -e "API URL: http://localhost:$PORT/api"
echo -e "${BLUE}================================================\n${NC}"

# Run Flask app
export FLASK_APP=backend/app.py
python3 -m flask run --host 0.0.0.0 --port $PORT
