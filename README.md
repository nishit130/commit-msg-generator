# Commit Message Generator

Auto-generate git commit messages using Claude AI. This tool uses AI to analyze your staged changes and create conventional commit messages automatically.

## Features

- 🤖 Automatically generates commit messages using Claude AI
- 📝 Follows conventional commit format (feat, fix, docs, etc.)
- ⚡ Limits context to ~1000 tokens for efficient API usage
- ✏️ Lets you edit the generated message before committing
- 🔧 Easy installation via pip
- ⚙️ Fully configurable (model, tokens, prompt)

## Installation

### Option 1: Install from local directory (for your team)

```bash
pip install git+https://github.com/yourteam/commit-msg-generator.git
```

Or if sharing locally:

```bash
# Clone or copy the repository
cd commit-msg-generator

# Install the package
pip install -e .
```

### Option 2: Direct installation from directory

```bash
pip install /path/to/commit-message
```

## Setup

1. **Get an Anthropic API key** from [console.anthropic.com](https://console.anthropic.com/)

2. **Set your API key** in your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

3. **Install the git hook** in your repository:

```bash
cd your-git-repo
install-commit-msg-hook
```

Or specify a different repository:

```bash
install-commit-msg-hook /path/to/repo
```

## Usage

1. Stage your changes:
```bash
git add .
```

2. Run commit without a message:
```bash
git commit
```

3. The AI will generate a commit message and open your editor
4. Edit the message if needed and save to complete the commit

## Configuration

Customize the behavior of the commit message generator:

### View current configuration

```bash
commit-msg-config show
```

### Change the model

```bash
commit-msg-config set model claude-3-5-sonnet-latest
```

Available models:
- `claude-3-5-haiku-latest` (default, fast and cost-effective)
- `claude-3-5-sonnet-latest` (more capable)
- `claude-opus-4-latest` (most capable)

### Change max tokens

```bash
commit-msg-config set max_tokens 1000
```

### Customize the prompt

```bash
commit-msg-config set prompt "Your custom prompt here. Must include {diff} placeholder."
```

**Note:** Your prompt must include `{diff}` which will be replaced with the git diff.

Example custom prompt:
```bash
commit-msg-config set prompt "Write a brief commit message for:\n{diff}\n\nUse emoji prefixes."
```

### Reset to defaults

```bash
commit-msg-config reset
```

### Configuration via environment variables

You can also override configuration using environment variables:
- `COMMIT_MSG_MODEL` - Model to use
- `COMMIT_MSG_MAX_TOKENS` - Max tokens for response
- `COMMIT_MSG_PROMPT` - Custom prompt template

```bash
export COMMIT_MSG_MODEL="claude-3-5-sonnet-latest"
export COMMIT_MSG_MAX_TOKENS="1000"
```

Configuration file location: `~/.commit-msg-generator.json`

## Uninstalling the Hook

To remove the hook from a repository:

```bash
cd your-git-repo
uninstall-commit-msg-hook
```

## How It Works

- Uses a `prepare-commit-msg` git hook
- Analyzes up to ~1000 tokens of your staged diff
- Calls Claude AI to generate a conventional commit message
- Prepopulates your commit message editor with the suggestion

## Sharing with Your Team

### Method 1: Git Repository

1. Push this package to a git repository (GitHub, GitLab, etc.)
2. Team members install with:
```bash
pip install git+https://github.com/yourteam/commit-msg-generator.git
```

### Method 2: Private PyPI Server

1. Build the package:
```bash
pip install build
python -m build
```

2. Upload to your private PyPI server
3. Team members install with:
```bash
pip install commit-msg-generator --index-url https://your-pypi-server.com
```

### Method 3: Shared Network Drive

1. Share the directory
2. Team members install with:
```bash
pip install /path/to/shared/commit-message
```

## Requirements

- Python 3.8+
- Git
- Anthropic API key

## License

MIT