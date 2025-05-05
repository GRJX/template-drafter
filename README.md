# AI Issue Generator

A Python tool for automatically generating detailed issue descriptions (Epics, Stories, AsciiDoc) for agile teams using local LLMs via Ollama.

## Features

-   Generate complete issue descriptions (Epics, Stories) or AsciiDoc documents from simple context.
-   Utilizes customizable templates stored in the `templates` directory.
-   Leverages local text generation using Ollama, keeping your data private.
-   Supports different output formats (Jira-compatible Markdown, AsciiDoc).
-   Configurable generation behavior via `issue_generator/prompts-config.json`.
-   Object-oriented design for extensibility.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/create-issues.git # Replace with your actual repo URL if different
cd create-issues

# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is installed and running
# Visit https://ollama.com for installation instructions
# Make sure the desired model (e.g., gemma3:27b) is pulled: ollama pull gemma3:27b
```

## Usage

The tool is run via the command line:

```bash
python cli.py "<Your issue context>" [options]
```

**Arguments:**

-   `context`: (Required) A string describing the core requirement or topic for the issue/document.

**Options:**

-   `--type`: The type of output to generate. Choices: `epic`, `story`, `adoc`. (Default: `story`)
-   `--output`: The *filename* for the output. If specified, the file will be saved in the `output/` directory (which will be created if it doesn't exist). If omitted, the output is printed to the console.
-   `--model`: The Ollama model to use for generation. (Default: `gemma3:27b`)

## Output Formats

The tool can generate output in two formats, determined by the `--type` argument:

-   **Jira/Markdown (`--type story` or `--type epic`):** Generates content using standard Markdown syntax suitable for pasting into Jira or other Markdown-based systems.
-   **AsciiDoc (`--type adoc`):** Generates content using AsciiDoc syntax, suitable for documentation systems that use AsciiDoc.

The specific formatting rules (e.g., for bullet points, tables) are adjusted based on the selected output format.

## Configuration

-   **Templates:** Issue structure is defined by template files (`epic_template.txt`, `story_template.txt`, `adoc_template.txt`) located in the `templates/` directory. You can customize these templates.
-   **Prompts:** The specific instructions given to the LLM for generating each section of the template are configured in `issue_generator/prompts-config.json`. This file defines the generation `type` (header, sentence, bullets, selection, tables) and associated parameters (word limits, options, table headers, etc.) for each template placeholder (e.g., `{{ title }}`, `{{ acceptance_criteria }}`).

## Examples

1.  **Generate a user story and print to console:**
    ```bash
    python cli.py "Implement login functionality using email and password"
    ```

2.  **Generate an epic and save to `output/epic_auth.md`:**
    ```bash
    python cli.py "User Authentication System" --type epic --output epic_auth.md
    ```

3.  **Generate an AsciiDoc document using a different model and save to `output/tech_spec.adoc`:**
    ```bash
    python cli.py "Technical specification for the new reporting module" --type adoc --model llama3:8b --output tech_spec.adoc
    ```