#!/usr/bin/env python3
"""
Command Line Interface for the Issue Generator tool.
"""

import argparse
import sys
import time

from issue_generator import TemplateManager, OllamaClient, IssueGenerator


def main():
    """Main entry point for the issue generator script."""
    parser = argparse.ArgumentParser(description="Generate issue descriptions from templates using AI")
    parser.add_argument("context", help="Context for the issue to generate")
    parser.add_argument("--type", choices=["epic", "story"], default="story", help="Type of issue to generate (epic or story)")
    parser.add_argument("--output", help="Output file (stdout if not specified)")
    parser.add_argument("--model", default="gemma3:27b", help="Ollama model to use")
    
    args = parser.parse_args()
    
    print(f"\033[94mInitializing issue generator with model: {args.model}\033[0m")
    
    # Set template based on issue type
    template_name = f"{args.type}_template.md"
    template_dir = "templates"  # Hardcoded template directory
    
    # Initialize components
    template_manager = TemplateManager(template_dir)
    ollama_client = OllamaClient(model=args.model)
    issue_generator = IssueGenerator(template_manager, ollama_client)
    
    # Generate the issue
    try:
        print(f"\033[90mLoading template for {args.type}: {template_name}\033[0m")
        print(f"\033[90mGenerating {args.type} from context: '{args.context}'\033[0m")
        
        start_time = time.time()
        issue_content = issue_generator.generate_full_issue(args.context, template_name)
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Output the result
        if args.output:
            with open(args.output, 'w') as f:
                f.write(issue_content)
            print(f"\033[92m{args.type.capitalize()} written to {args.output}\033[0m")
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