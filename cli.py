#!/usr/bin/env python3
"""
Command Line Interface for the Issue Generator tool.
"""

import argparse
import sys
import time
import os # Import os

from issue_generator import TemplateManager, OllamaClient, IssueGenerator


def main():
    """Main entry point for the issue generator script."""
    parser = argparse.ArgumentParser(description="Generate issue descriptions from templates using AI")
    parser.add_argument("context", help="Path to the file containing the context for the issue to generate")
    parser.add_argument("--type", choices=["epic", "story", "adoc", "docs"], default="story", help="Type of issue to generate (epic, story, or adoc)")
    parser.add_argument("--output", help="Output file (stdout if not specified)")
    parser.add_argument("--model", default="gemma3:27b", help="Ollama model to use")
    
    args = parser.parse_args()

    # Read the context from the specified file
    try:
        with open(args.context, 'r') as file:
            context = file.read()
    except FileNotFoundError:
        print(f"\033[91mError: Context file '{args.context}' not found\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\033[91mError reading context file: {str(e)}\033[0m")
        sys.exit(1)

    print(f"\033[90mInitializing issue generator with model: {args.model}\033[0m")
    
    # Set template based on issue type
    template_name = f"{args.type}_template.txt"
    template_dir = "templates"  # Hardcoded template directory
    
    # Define path to prompts config relative to this script's location or a fixed path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_config_path = os.path.join(script_dir, 'issue_generator', 'prompts-config.json')
    
    # Determine output format based on type
    output_format = 'adoc' if args.type == 'adoc' else 'jira'
    print(f"\033[90mOutput format set to: {output_format}\033[0m")

    # Initialize components
    try:
        template_manager = TemplateManager(template_dir, prompt_config_path)
        system_prompt = template_manager.get_system_prompt()
        ollama_client = OllamaClient(model=args.model, system_prompt=system_prompt)
        issue_generator = IssueGenerator(template_manager=template_manager, ollama_client=ollama_client, output_format=output_format)
    except FileNotFoundError as e:
        print(f"\033[91mInitialization Error: {str(e)}\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\033[91mUnexpected Initialization Error: {str(e)}\033[0m")
        sys.exit(1)

    # Generate the issue
    try:
        print(f"\033[90mLoading template for {args.type}: {template_name}\033[0m")
        print(f"\033[90mGenerating {args.type} from context file: '{args.context}'\033[0m")
        
        start_time = time.time()
        issue_content = issue_generator.generate_full_issue(context, template_name)
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Output the result
        if args.output:
            output_dir = "output"
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Construct the full path for the output file
            output_path = os.path.join(output_dir, args.output)
            
            with open(output_path, 'w') as f:
                f.write(issue_content)
            print(f"\033[92m{args.type.capitalize()} written to {output_path}\033[0m")
        else:
            print(f"\n--- Generated {args.type.capitalize()} ---\n")
            print(issue_content)
            print("\n----------------------\n")
        
        print(f"\033[92mGeneration completed in {generation_time:.2f} seconds\033[0m")
    except Exception as e:
        print(f"\033[91mError: {str(e)}\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main()