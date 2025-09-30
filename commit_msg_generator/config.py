"""Configuration management for commit message generator."""
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

DEFAULT_CONFIG = {
    "model": "claude-3-5-haiku-latest",
    "max_tokens": 1000,  # Max tokens for analyzing the git diff (input)
    "prompt": """Based on the following git diff, write a concise commit message following conventional commit format.

The format should be: <type>: <description>

Types: feat, fix, docs, style, refactor, test, chore

Keep it concise (one line preferred, max 72 characters for the summary).
If needed, add a blank line and then bullet points for details.

Git diff:
{diff}

Respond with ONLY the commit message, no explanations or additional text."""
}

CONFIG_FILE = Path.home() / ".commit-msg-generator.json"


def load_config() -> Dict[str, Any]:
    """Load configuration from file, environment variables, and defaults."""
    config = DEFAULT_CONFIG.copy()

    # Load from config file if it exists
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file: {e}")

    # Override with environment variables if set
    if os.environ.get('COMMIT_MSG_MODEL'):
        config['model'] = os.environ['COMMIT_MSG_MODEL']

    if os.environ.get('COMMIT_MSG_MAX_TOKENS'):
        try:
            config['max_tokens'] = int(os.environ['COMMIT_MSG_MAX_TOKENS'])
        except ValueError:
            print("Warning: COMMIT_MSG_MAX_TOKENS must be an integer")

    if os.environ.get('COMMIT_MSG_PROMPT'):
        config['prompt'] = os.environ['COMMIT_MSG_PROMPT']

    return config


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_config_value(key: str) -> Optional[Any]:
    """Get a specific config value."""
    config = load_config()
    return config.get(key)


def set_config_value(key: str, value: Any) -> None:
    """Set a specific config value."""
    config = load_config()
    config[key] = value
    save_config(config)


def reset_config() -> None:
    """Reset configuration to defaults."""
    save_config(DEFAULT_CONFIG)


def show_config() -> Dict[str, Any]:
    """Show current configuration."""
    return load_config()