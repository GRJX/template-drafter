#!/usr/bin/env python3
"""
Command Line Interface for the Issue Generator tool.
"""

import os
import argparse
import sys
import time

from issue_generator import TemplateManager, OllamaClient, IssueGenerator


def main():
    """Main entry point for the issue generator script."""
    parser = argparse.ArgumentParser(description="Generate issue descriptions from templates using AI")
    parser.add_argument("context", help="Context for the issue to generate")
    parser.add_argument("--template", default="issue_template.md", help="Name of the template file")
    parser.add_argument("--template-dir", default="templates", help="Directory containing templates")
    parser.add_argument("--output", help="Output file (stdout if not specified)")
    parser.add_argument("--model", default="gemma3:12b", help="Ollama model to use")
    
    args = parser.parse_args()
    
    print(f"Initializing issue generator with model: {args.model}")
    
    # Initialize components
    template_manager = TemplateManager(args.template_dir)
    ollama_client = OllamaClient(model=args.model)
    issue_generator = IssueGenerator(template_manager, ollama_client)
    
    # Generate the issue
    try:
        print(f"Loading template: {args.template}")
        print(f"Generating issue from context: '{args.context}'")
        
        start_time = time.time()
        issue_content = issue_generator.generate_full_issue(args.context, args.template)
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Output the result
        if args.output:
            with open(args.output, 'w') as f:
                f.write(issue_content)
            print(f"Issue written to {args.output}")
        else:
            print("\n--- Generated Issue ---\n")
            print(issue_content)
            print("\n----------------------\n")
        
        print(f"Generation completed in {generation_time:.2f} seconds")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()