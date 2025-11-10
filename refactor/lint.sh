#!/bin/bash
# Script to format code with black and check with pylint

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Activate virtual environment
source venv/bin/activate

# Python files to check (excluding venv)
PYTHON_FILES="config.py main.py quiz_data.py resultats_data.py ui.py"

echo -e "${YELLOW}=== Running Black Formatter ===${NC}"
black $PYTHON_FILES
BLACK_EXIT=$?

if [ $BLACK_EXIT -eq 0 ]; then
    echo -e "${GREEN}✓ Black formatting completed${NC}\n"
else
    echo -e "${RED}✗ Black formatting failed${NC}\n"
    exit 1
fi

echo -e "${YELLOW}=== Running Pylint ===${NC}"
pylint $PYTHON_FILES --output-format=text
PYLINT_EXIT=$?

echo -e "\n${YELLOW}=== Summary ===${NC}"
if [ $PYLINT_EXIT -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
else
    echo -e "${RED}✗ Pylint found issues (exit code: $PYLINT_EXIT)${NC}"
fi

exit $PYLINT_EXIT
