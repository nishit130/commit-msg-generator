#!/usr/bin/env python3
import subprocess
import sys
import os
from anthropic import Anthropic
from .config import load_config

def get_staged_diff():
    """Get the staged diff with token limit consideration."""
    try:
        # Get staged diff
        result = subprocess.run(
            ['git', 'diff', '--cached'],
            capture_output=True,
            text=True,
            check=True
        )
        diff = result.stdout

        # Limit to approximately 1000 tokens (roughly 4000 characters)
        # This is a rough estimate: 1 token ≈ 4 characters
        max_chars = 4000
        if len(diff) > max_chars:
            diff = diff[:max_chars] + "\n\n[... diff truncated to fit token limit ...]"

        return diff
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}", file=sys.stderr)
        sys.exit(1)

def generate_commit_message(diff):
    """Generate commit message using Claude API."""
    api_key = os.environ.get('ANTHROPIC_API_KEY')

    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it in your shell profile (e.g., .zshrc or .bashrc)", file=sys.stderr)
        sys.exit(1)

    # Load configuration
    config = load_config()
    model = config['model']
    max_tokens = config['max_tokens']
    prompt_template = config['prompt']

    # Format the prompt with the diff
    prompt = prompt_template.format(diff=diff)

    try:
        client = Anthropic(api_key=api_key)

        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return message.content[0].text.strip()
    except Exception as e:
        print(f"Error calling Claude API: {e}", file=sys.stderr)
        sys.exit(1)

def prepare_commit_msg():
    """Main entry point for the prepare-commit-msg hook."""
    if len(sys.argv) < 2:
        print("Usage: generate-commit-msg <commit-msg-file>", file=sys.stderr)
        sys.exit(1)

    commit_msg_file = sys.argv[1]

    print("🤖 Analyzing your staged changes...", file=sys.stderr)

    # Get the staged diff
    diff = get_staged_diff()

    if not diff or diff.strip() == "":
        print("No staged changes found", file=sys.stderr)
        sys.exit(0)

    print("✨ Generating commit message with AI...", file=sys.stderr)

    # Generate commit message
    commit_message = generate_commit_message(diff)

    print("✓ Commit message generated successfully!", file=sys.stderr)

    # Read existing commit message (if any)
    with open(commit_msg_file, 'r') as f:
        existing_msg = f.read()

    # Only prepend if the file is empty or contains only comments
    if not existing_msg or all(line.startswith('#') for line in existing_msg.split('\n') if line.strip()):
        with open(commit_msg_file, 'w') as f:
            f.write(commit_message + '\n\n')
            if existing_msg:
                f.write(existing_msg)