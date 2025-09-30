#!/usr/bin/env python3
"""CLI tool for installing the git hook."""
import os
import sys
import json
import subprocess
from pathlib import Path
from .config import load_config, set_config_value, reset_config, CONFIG_FILE

def install_hook():
    """Install the git hook in a repository."""
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        # Use current directory
        repo_path = os.getcwd()

    repo_path = Path(repo_path).resolve()
    git_dir = repo_path / '.git'

    if not git_dir.exists():
        print(f"Error: {repo_path} is not a git repository", file=sys.stderr)
        print("Usage: install-commit-msg-hook [path-to-git-repo]", file=sys.stderr)
        sys.exit(1)

    # Check if ANTHROPIC_API_KEY is set
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("⚠️  Warning: ANTHROPIC_API_KEY environment variable is not set", file=sys.stderr)
        print("Please add the following to your shell profile (~/.zshrc or ~/.bashrc):", file=sys.stderr)
        print("", file=sys.stderr)
        print("export ANTHROPIC_API_KEY='your-api-key-here'", file=sys.stderr)
        print("", file=sys.stderr)
        print("You can get an API key from: https://console.anthropic.com/", file=sys.stderr)
        print("", file=sys.stderr)

    hooks_dir = git_dir / 'hooks'
    hooks_dir.mkdir(exist_ok=True)

    hook_path = hooks_dir / 'prepare-commit-msg'

    # Create the hook
    hook_content = """#!/bin/bash
# Auto-generated git hook for commit message generation

COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2

# Only run for regular commits (not merge, squash, etc.)
if [ -z "$COMMIT_SOURCE" ] || [ "$COMMIT_SOURCE" = "message" ]; then
    generate-commit-msg "$COMMIT_MSG_FILE"
fi
"""

    with open(hook_path, 'w') as f:
        f.write(hook_content)

    # Make the hook executable
    hook_path.chmod(0o755)

    print(f"✓ Git hook installed successfully at: {hook_path}")
    print("")
    print("Now when you run 'git commit', the LLM will auto-generate a commit message.")
    print("You can edit the message before finalizing the commit.")


def uninstall_hook():
    """Uninstall the git hook from a repository."""
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = os.getcwd()

    repo_path = Path(repo_path).resolve()
    hook_path = repo_path / '.git' / 'hooks' / 'prepare-commit-msg'

    if hook_path.exists():
        hook_path.unlink()
        print(f"✓ Git hook uninstalled from: {repo_path}")
    else:
        print(f"No hook found at: {hook_path}")


def show_config():
    """Show current configuration."""
    config = load_config()
    print(f"Configuration file: {CONFIG_FILE}")
    print("")
    print("Current settings:")
    print(json.dumps(config, indent=2))
    print("")
    print("To modify: commit-msg-config set <key> <value>")
    print("To reset: commit-msg-config reset")


def configure():
    """Configure the commit message generator."""
    if len(sys.argv) < 2:
        show_config()
        return

    command = sys.argv[1]

    if command == "show":
        show_config()
    elif command == "set":
        if len(sys.argv) < 4:
            print("Usage: commit-msg-config set <key> <value>", file=sys.stderr)
            print("", file=sys.stderr)
            print("Available keys:", file=sys.stderr)
            print("  model        - Claude model to use (e.g., claude-3-5-haiku-latest)", file=sys.stderr)
            print("  max_tokens   - Maximum tokens for response (e.g., 500)", file=sys.stderr)
            print("  prompt       - Custom prompt template (must include {diff})", file=sys.stderr)
            sys.exit(1)

        key = sys.argv[2]
        value = sys.argv[3]

        # Type conversion for max_tokens
        if key == "max_tokens":
            try:
                value = int(value)
            except ValueError:
                print(f"Error: max_tokens must be an integer", file=sys.stderr)
                sys.exit(1)

        # Validate prompt has {diff} placeholder
        if key == "prompt" and "{diff}" not in value:
            print("Error: prompt must include {diff} placeholder", file=sys.stderr)
            sys.exit(1)

        # Validate key
        valid_keys = ["model", "max_tokens", "prompt"]
        if key not in valid_keys:
            print(f"Error: Invalid key '{key}'", file=sys.stderr)
            print(f"Valid keys: {', '.join(valid_keys)}", file=sys.stderr)
            sys.exit(1)

        set_config_value(key, value)
        print(f"✓ Set {key} = {value}")
        print(f"Configuration saved to: {CONFIG_FILE}")

    elif command == "reset":
        reset_config()
        print(f"✓ Configuration reset to defaults")
        print(f"Configuration file: {CONFIG_FILE}")

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Usage: commit-msg-config [show|set|reset]", file=sys.stderr)
        sys.exit(1)