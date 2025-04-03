# Issue Generator

A Python tool for automatically generating detailed issue descriptions for agile teams using Ollama for text generation.

## Features

- Generate complete issue descriptions from simple context
- Use customizable templates
- Local text generation using Ollama
- Object-oriented design

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/create-issues.git
cd create-issues

# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is installed and running
# Visit https://ollama.ai for installation instructions
```

## Usage

```bash
python cli.py "Add user authentication to the application"
```

### Options

- `--template` - Template file to use (default: issue_template.md)
- `--template-dir` - Directory containing templates (default: templates)
- `--output` - Output file (prints to console if not specified)
- `--model` - Ollama model to use (default: gamma3:14b)

## Example

```bash
python cli.py "Create a dashboard for admin users" --output issue.md
```