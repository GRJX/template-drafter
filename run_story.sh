#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please set up the environment."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Generate timestamp for unique output file
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="output_${TIMESTAMP}.adoc"

# Run the CLI with all provided arguments
echo "Running CLI with arguments: prompt"
python cli.py prompt --type story --model gpt-oss:latest --quality high --output "$OUTPUT_FILE"
