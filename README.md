# GameDevProjectPlanCreator

A Python tool that sets up a complete game development project on GitHub with issues, milestones, and project boards. Uses AI-powered customization via GitHub Copilot to generate game-specific issues from a design document. 

**✨ Use with any repository** - No forking required! Clone this tool once and use it to set up any GitHub repository you have access to.

## Features

- 🤖 AI-powered issue generation using GitHub Copilot
- 📝 Customize issue templates based on your game design document
- 🎯 Create GitHub issues from JSON templates
- 🏷️ Automatically set up standardized labels
- 📊 Create milestones for 7 development categories
- 📋 Set up GitHub Projects V2 board with Kanban workflow
- 🎨 Automatic status column colors (blue, yellow, green, red, pink, purple)
- 🎮 Generic workflow applicable to any game genre

## Quick Start

Follow these 5 steps to set up your game development project:

### 1. Clone and Install

```bash
git clone https://github.com/samsmithnz/GameDevProjectPlanCreator.git
cd GameDevProjectPlanCreator
pip install -r requirements.txt
```

### 2. Create Your Game Design Document

Write a high-level description of your game. This can be a simple markdown or text file describing:
- Game concept and genre
- Core gameplay mechanics
- Key features
- Technical requirements
- Art and audio needs
- Marketing and business goals

Save this as `my-game-design.md` (or any name you prefer).

### 3. Create Your GitHub PAT Token

You'll need a GitHub Personal Access Token with the right permissions. See the [Creating a GitHub Personal Access Token](#creating-a-github-personal-access-token) section below for detailed instructions.

Quick summary: Generate a token with `repo` and `project` scopes (Classic token) or Issues + Projects permissions (Fine-grained token).

### 4. Use GitHub Copilot to Update issue-templates.json

Open this repository in VS Code and use GitHub Copilot to customize the `templates/issue-templates.json` file based on your game design document.

In **GitHub Copilot Chat**, use this prompt:

```
Please read the game design document located at [path-to-your-design-doc]. Then, update the templates/issue-templates.json file to generate GitHub issues covering the complete project lifecycle:

1. Business Setup: Company formation, legal requirements, team structure, budget planning
2. Game Development: All technical and creative tasks needed to build the game according to the design document specifications
3. Launch & Operations: Marketing campaigns, community management, customer support infrastructure, and post-launch maintenance
Ensure all issues are tailored to the specific game described in the design document—reference unique features, mechanics, art style, target platforms, and other design-specific requirements when creating issue descriptions

Keep the same JSON structure with 7 categories (programming, art, audio, qa, documentation, marketing, business), but customize the templates to match the specific features and requirements described in my game design document.

For each template, provide:
- title: A clear, actionable task title
- body: Detailed description of what needs to be done
- labels: Array of relevant labels (include at least the category label)

Make sure the templates are specific to my game while remaining actionable development tasks.
```

Review and save the updated `templates/issue-templates.json` file.

### 5. Run Preview and Setup

```bash
# Preview what will be created (dry run)
python setup_game_project.py --owner your-username --repo your-game-repo --dry-run

# Run the actual setup
export GITHUB_TOKEN=your_github_token
python setup_game_project.py --owner your-username --repo your-game-repo
```

That's it! Your GitHub repository will now have:
- ✅ Labels (9 standardized)
- ✅ Milestones (7 categories)
- ✅ Project board with Kanban workflow (6 status columns with colors)
- ✅ Issues created from your customized templates
- ✅ All issues assigned to project in Backlog

## Installation

### Prerequisites

- Python 3.7 or higher
- pip
- GitHub Personal Access Token (Classic with `repo` and `project` scopes, OR Fine-grained with Issues and Projects permissions)

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

### Creating a GitHub Personal Access Token

The tool requires a GitHub Personal Access Token (PAT) with appropriate permissions. You can use either Classic or Fine-grained tokens.

#### Option 1: Classic Personal Access Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)
2. Click "Generate new token" → "Generate new token (classic)"
3. Give your token a descriptive name (e.g., "GameDevProjectPlanCreator")
4. Select the following scopes:
   - ✅ **`repo`** (Full control of private repositories) - Required for:
     - Creating and managing issues
     - Creating and managing milestones
     - Creating and managing labels
     - Reading repository information
   - ✅ **`project`** (Full control of projects) - Required for:
     - Creating Projects V2 boards
     - Creating project fields and status options
     - Adding issues to projects
5. Click "Generate token"
6. Copy the token immediately (you won't be able to see it again)
7. Set it as an environment variable:
   ```bash
   export GITHUB_TOKEN=your_generated_token
   ```

#### Option 2: Fine-grained Personal Access Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens](https://github.com/settings/personal-access-tokens/new)
2. Click "Generate new token"
3. Configure the token:
   - **Token name**: "GameDevProjectPlanCreator"
   - **Expiration**: Choose your preferred expiration period
   - **Repository access**: Select "Only select repositories" and choose your game project repository
4. Under "Permissions", configure **Repository permissions**:
   - ✅ **Issues**: Read and write
   - ✅ **Metadata**: Read-only (automatically selected)
   - ✅ **Projects**: Read and write (Note: This is for repository-level projects)
5. Under "Permissions", configure **Organization permissions** (if creating organization-level projects):
   - ✅ **Projects**: Read and write
6. Click "Generate token"
7. Copy the token immediately
8. Set it as an environment variable:
   ```bash
   export GITHUB_TOKEN=your_generated_token
   ```

**Note**: Fine-grained tokens provide more granular control and are more secure as they can be scoped to specific repositories. However, ensure you grant access to the specific repository you want to set up.

## Usage

### Main Command

The tool has one main command that sets up everything:

```bash
python setup_game_project.py --owner <github-owner> --repo <github-repo>
```

**Options:**
- `--templates` (optional) - Path to issue templates JSON file (default: `templates/issue-templates.json`)
- `--owner` (required) - GitHub repository owner
- `--repo` (required) - GitHub repository name  
- `--token` (optional) - GitHub PAT token (or use GITHUB_TOKEN env var)
- `--dry-run` (optional) - Preview changes without creating anything

### What It Does

The setup script performs these steps:

1. **Validates inputs** - Checks templates JSON file exists, token is set, repo is accessible
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
6. **Creates issues** - Reads templates from JSON and creates GitHub issues with proper labels and milestones
7. **Assigns issues to project** - Automatically adds each issue to the Projects V2 board with Backlog status

**Note:** WIP (Work In Progress) limits must still be set manually in the GitHub UI (max 5 for On deck, max 3 for In progress, max 5 for Blocked, max 5 for In review). Colors are set automatically via GraphQL API.

### Using GitHub Copilot to Customize Issue Templates

The power of this tool comes from using GitHub Copilot to customize the issue templates based on your specific game design.

**Steps:**

1. **Open this repository in VS Code** with GitHub Copilot enabled

2. **Have your game design document ready** (the document you created in step 2 of Quick Start)

3. **Open the file** `templates/issue-templates.json` in your editor

4. **Use GitHub Copilot Chat** with this prompt:

```
I have a game design document at [path-to-your-game-design.md]. 

Please read my game design document and update the templates/issue-templates.json file to create game-specific issues based on my game design.

Requirements:
- Keep the same JSON structure with 7 categories: programming, art, audio, qa, documentation, marketing, business
- Customize the templates array in each category to match the specific features and requirements from my game design
- For each template, provide:
  - title: A clear, actionable task title specific to my game
  - body: Detailed description of what needs to be done for my game
  - labels: Array of relevant labels (include at least the category label)
- Remove generic templates that don't apply to my game
- Add new templates for game-specific features mentioned in my design
- Keep titles concise and bodies detailed

Make the templates specific to my game while remaining actionable development tasks.
```

5. **Review the updated JSON** - Copilot will update the issue-templates.json file with game-specific issues

6. **Save the file** - Make any manual adjustments if needed

7. **Run the setup tool** (see Quick Start step 5)

**Tips for best results:**
- Be detailed in your game design document (features, mechanics, technical requirements)
- Include specific gameplay elements, art style, audio needs, etc.
- Mention platforms, game engines, and technologies you'll use
- Describe multiplayer, progression systems, monetization if applicable
- The more specific your design doc, the better Copilot's customization

### JSON Template Structure

The `templates/issue-templates.json` file follows this structure:

```json
{
  "categories": {
    "programming": {
      "name": "programming",
      "description": "Programming and technical implementation",
      "templates": [
        {
          "title": "Implement core game loop",
          "body": "Create the main game loop that handles:\n- Game state management\n- Update cycle\n- Render cycle",
          "labels": ["enhancement", "programming"]
        }
      ]
    },
    "art": {
      "name": "art",
      "templates": [ ... ]
    }
  }
}
```

Each category contains an array of template objects with:
- **title**: The issue title (concise, actionable)
- **body**: Detailed description (can include markdown formatting like `\n` for newlines, bullet lists)
- **labels**: Array of label names to apply (should include the category label at minimum)

**JSON Format:**
- Each category has a `templates` array
- Each template object needs: `title`, `body`, `labels`
- Labels array should include the category label
- Body supports markdown and escape sequences like `\n` for newlines

See `templates/issue-templates.json` for the default generic template structure. You'll customize this file with GitHub Copilot based on your game design. You can also use `examples/game-design-template.md` as a starting point for your game design document.

## Categories & Milestones

The tool creates 7 milestones that organize all development work:

1. **programming** - Programming and technical implementation (core mechanics, AI, networking, etc.)
2. **art** - Visual art, graphics, and UI design
3. **audio** - Sound effects and music systems
4. **QA** - Quality assurance, testing, and debugging
5. **documentation** - Documentation and technical writing
6. **marketing** - Marketing and promotional activities
7. **business** - Business operations and analytics

Each issue is automatically assigned to the appropriate milestone based on its category.

## Example Workflow

```bash
# Setup
git clone https://github.com/samsmithnz/GameDevProjectPlanCreator.git
cd GameDevProjectPlanCreator
pip install -r requirements.txt

# Write your game design document (my-rpg-design.md)

# Use GitHub Copilot to customize templates/issue-templates.json
# based on your game design (see step 4 in Quick Start above)

# Preview first (dry run)
python setup_game_project.py --owner myusername --repo my-rpg-game --dry-run

# If it looks good, run for real
export GITHUB_TOKEN=your_token_here
python setup_game_project.py --owner myusername --repo my-rpg-game

# Your repository now has:
# - All issues created from customized templates
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
