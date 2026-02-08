# GameDevProjectPlanCreator

A Python tool that sets up a complete game development project on GitHub with issues, milestones, and project boards. Based on the patterns from the TBS project.

**✨ Use with any repository** - No forking required! Clone this tool once and use it to set up any GitHub repository you have access to.

## Features

- 📝 Parse user stories from markdown design documents
- 🎯 Create GitHub issues from user stories
- 🏷️ Automatically set up standardized labels
- 📊 Create milestones for 7 development categories
- 📋 Set up project board (with guidance)
- 🎮 Generic workflow applicable to any game genre

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/samsmithnz/GameDevProjectPlanCreator.git
cd GameDevProjectPlanCreator
pip install -r requirements.txt

# 2. Create your user stories document
cp examples/user-stories-template.md my-game-user-stories.md
# Edit my-game-user-stories.md with your game's user stories

# 3. Preview what will be created (dry run)
python setup_game_project.py --design-doc my-game-user-stories.md --owner your-username --repo your-game --dry-run

# 4. Run the setup
export GITHUB_TOKEN=your_github_token
python setup_game_project.py --design-doc my-game-user-stories.md --owner your-username --repo your-game
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip
- GitHub Personal Access Token with `repo` scope

### Setup

1. Clone this repository:
```bash
git clone https://github.com/samsmithnz/GameDevProjectPlanCreator.git
cd GameDevProjectPlanCreator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your GitHub token:
```bash
export GITHUB_TOKEN=your_github_personal_access_token
```

To create a GitHub personal access token:
- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate new token with `repo` scope
- Copy the token and set it as GITHUB_TOKEN environment variable

## Usage

### Main Command

The tool has one main command that sets up everything:

```bash
python setup_game_project.py --design-doc <path-to-user-stories> --owner <github-owner> --repo <github-repo>
```

**Options:**
- `--design-doc` (required) - Path to markdown file with user stories
- `--owner` (required) - GitHub repository owner
- `--repo` (required) - GitHub repository name  
- `--token` (optional) - GitHub PAT token (or use GITHUB_TOKEN env var)
- `--dry-run` (optional) - Preview changes without creating anything

### What It Does

The setup script performs these steps:

1. **Validates inputs** - Checks design doc exists, token is set, repo is accessible
2. **Sets up labels** - Creates/updates 9 standardized labels (enhancement, bug, programming, art, audio, QA, documentation, marketing, business)
3. **Creates milestones** - Sets up 7 milestones matching the development categories
4. **Creates project board** - Automatically creates a GitHub Projects V2 board using GraphQL API
5. **Creates workflow status options with colors** - Adds 6 Kanban workflow status options:
   - **Backlog** - Work that hasn't been started (blue color)
   - **On deck** - Work prioritized and ready next (yellow color)
   - **In progress** - Work actively being worked on (green color)
   - **Blocked** - Work that is blocked (red color)
   - **In review** - Work ready for review/QA (pink color)
   - **Done** - Completed work (purple color)
6. **Creates issues** - Parses user stories and creates GitHub issues with proper labels and milestones
7. **Assigns issues to project** - Automatically adds each issue to the Projects V2 board with Backlog status

**Note:** WIP (Work In Progress) limits must still be set manually in the GitHub UI (max 5 for On deck, max 3 for In progress, max 5 for Blocked, max 5 for In review). Colors are set automatically via GraphQL API.

### Using GitHub Copilot to Generate User Stories

If you have a high-level game description document, you can use GitHub Copilot in your IDE to automatically generate user stories in the required format.

**Steps:**

1. **Open your game description document** in VS Code or your preferred IDE with GitHub Copilot enabled

2. **Create a new file** for your user stories (e.g., `my-game-user-stories.md`)

3. **Use GitHub Copilot Chat** with this prompt:

```
Review this game description document and generate user stories in the following format:

- Use the 7 categories: PROG (programming), ART (art), AUDIO (audio), QA (QA), DOC (documentation), MKT (marketing), BUS (business)
- Format each story as: **US-CATEGORY-###**: As a [user], I want [goal] so that [benefit]
- Include Labels and Acceptance Criteria for each story
- Organize stories by category headings (## Programming, ## Art, etc.)
- Follow the pattern from this GameDevProjectPlanCreator repository

Example format:
## Programming

- **US-PROG-001**: As a player, I want to move my character so that I can explore
  - Labels: `programming`, `gameplay`, `movement`
  - Acceptance Criteria:
    - Character can move in all directions
    - Movement is smooth and responsive

Generate comprehensive user stories for all features described in the game design document.
```

4. **Provide context** by:
   - Including your game description in the chat
   - Referencing the `examples/user-stories-template.md` file from this repository
   - Letting Copilot analyze both files together

5. **Review and refine** the generated user stories, ensuring:
   - All category codes are correct (PROG, ART, AUDIO, QA, DOC, MKT, BUS)
   - Story IDs are sequential within each category
   - Acceptance criteria are specific and testable
   - Labels are appropriate for each story

6. **Save the output** to your user stories file

7. **Run the setup tool** with your generated user stories:
```bash
python setup_game_project.py --design-doc my-game-user-stories.md --owner your-username --repo your-game
```

**Tips for best results:**
- Be specific in your game description document (features, mechanics, goals)
- Include technical requirements and non-functional requirements
- Mention any specific platforms, engines, or technologies
- Describe the target audience and key gameplay elements
- Review and edit the AI-generated stories before running the tool

### Design Document Format

Create a markdown file with user stories in this format:

```markdown
# My Game Project Plan

## Programming

- **US-PROG-001**: As a player, I want to move my character so that I can explore
  - Labels: `programming`, `gameplay`, `movement`
  - Acceptance Criteria:
    - Character can move in all directions
    - Movement is smooth and responsive
    - Obstacles block movement

- **US-PROG-002**: As a player, I want to jump over obstacles
  - Labels: `programming`, `gameplay`
  - Acceptance Criteria:
    - Jump button is responsive
    - Jump height is appropriate

## Art

- **US-ART-001**: As a player, I want appealing character designs
  - Labels: `art`, `characters`
  - Acceptance Criteria:
    - Characters have distinct visual style
    - Animations are smooth
```

**Format Rules:**
- User story IDs: `US-CATEGORY-###` where CATEGORY is PROG, ART, AUDIO, QA, DOC, MKT, or BUS
- Story format: `As a [user type], I want [goal] so that [benefit]`
- Labels: Comma-separated in backticks
- Acceptance Criteria: Bulleted list under the heading

See `examples/user-stories-template.md` for a complete template.

## Categories & Milestones

The tool creates 7 milestones that organize all development work:

1. **programming** - Programming and technical implementation (core mechanics, AI, networking, etc.)
2. **art** - Visual art, graphics, and UI design
3. **audio** - Sound effects and music systems
4. **QA** - Quality assurance, testing, and debugging
5. **documentation** - Documentation and technical writing
6. **marketing** - Marketing and promotional activities
7. **business** - Business operations and analytics

Each user story is automatically assigned to the appropriate milestone based on its category code.

## Example Workflow

```bash
# Setup
git clone https://github.com/samsmithnz/GameDevProjectPlanCreator.git
cd GameDevProjectPlanCreator
pip install -r requirements.txt

# Create your user stories
cp examples/user-stories-template.md my-rpg-game.md
# Edit my-rpg-game.md with your game's user stories

# Preview first (dry run)
python setup_game_project.py --design-doc my-rpg-game.md --owner myusername --repo my-rpg-game --dry-run

# If it looks good, run for real
export GITHUB_TOKEN=your_token_here
python setup_game_project.py --design-doc my-rpg-game.md --owner myusername --repo my-rpg-game

# Your repository now has:
# - All issues created from user stories
# - 9 standardized labels
# - 7 milestones (one per category)
# - GitHub Projects V2 board with 6 Kanban workflow status options
# - Status colors automatically set (blue, yellow, green, red, pink, purple)
# - All issues added to project with Backlog status
# 
# Next steps in GitHub UI:
# - Set WIP limits: On deck (5), In progress (3), Blocked (5), In review (5)
# - Move issues through workflow as work progresses
```

## Credits

This tool is based on the project planning approach used in the [TBS project](https://github.com/samsmithnz/TBS), which uses Python scripts to create comprehensive project plans for game development.

## License

MIT License - See LICENSE file for details
