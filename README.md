# GameDevProjectPlanCreator

A Python tool that automatically generates comprehensive GitHub issues for game development projects based on a design document. This tool helps game developers quickly set up project boards with all necessary tasks, from core mechanics to launch preparation.

**✨ Use with any repository** - No forking required! Clone this tool once and use it to generate issues on any GitHub repository you have access to.

## Features

- 📝 Parse game design documents to extract requirements
- 🎯 Generate categorized GitHub issues based on game features
- 🏷️ Automatic labeling and organization
- 📊 Export to JSON or Markdown
- 🚀 Direct GitHub integration to create issues and labels
- 🎮 Generic templates applicable to any game genre

## Installation

**No forking required!** This tool can be used to generate issues for any GitHub repository you have access to.

### Prerequisites

- Python 3.7 or higher
- pip
- GitHub Personal Access Token with `repo` scope (for creating issues on your repositories)

### Setup

1. Clone this repository (one-time setup):
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

This tool supports two approaches for creating game project issues:

### Approach 1: Quick Template-Based (Simple)

Use pre-defined generic templates to quickly generate standard game development issues.

**Best for**: Quick project setup, standard game development workflows

### Approach 2: Detailed User Stories (TBS Pattern)

Create detailed user stories in a markdown file, then parse them to create issues. Follows the pattern from the TBS project.

**Best for**: Custom game requirements, detailed planning, specific user stories

---

### Quick Template-Based Approach

**Target any repository**: All commands support `--owner` and `--repo` parameters to target any GitHub repository you have access to.

#### Export Issues to Files

Export to JSON:
```bash
python src/export_issues.py examples/sample-design-doc.md --json output/issues.json
```

Export to Markdown:
```bash
python src/export_issues.py examples/sample-design-doc.md --markdown output/project-plan.md
```

Export to both:
```bash
python src/export_issues.py examples/sample-design-doc.md --json output/issues.json --markdown output/plan.md
```

#### Create Issues from Templates

Create issues directly on **any** GitHub repository:

```bash
export GITHUB_TOKEN=your_token_here
python src/create_issues.py examples/sample-design-doc.md --owner your-username --repo your-game-project
```

---

### Detailed User Stories Approach (TBS Pattern)

#### Create Your User Stories Document

1. Copy the user stories template:
```bash
cp examples/user-stories-template.md my-game-user-stories.md
```

2. Edit the file and add your game's user stories in this format:
```markdown
- **US-PROG-001**: As a player, I want to move my character so that I can explore
  - Labels: `programming`, `gameplay`
  - Acceptance Criteria:
    - Character moves smoothly
    - Movement respects obstacles
    - Animation plays correctly
```

#### Create Issues from User Stories

```bash
export GITHUB_TOKEN=your_token_here
python src/create_issues_from_user_stories.py my-game-user-stories.md --owner your-username --repo your-game-project
```

Preview without creating (dry run):
```bash
python src/create_issues_from_user_stories.py my-game-user-stories.md --owner your-username --repo your-game-project --dry-run
```

---

### Add Labels to Your Repository

Add standard game development labels to **any** GitHub repository:

```bash
export GITHUB_TOKEN=your_token_here
python src/add_labels.py --owner your-username --repo your-game-project
```

### Complete Workflow Example (Template Approach)

```bash
# 1. One-time setup
git clone https://github.com/samsmithnz/GameDevProjectPlanCreator.git
cd GameDevProjectPlanCreator
pip install -r requirements.txt

# 2. Create your game design document (use template as starting point)
cp examples/design-doc-template.md ~/my-game-design.md
# Edit ~/my-game-design.md with your game details

# 3. Add labels to your repository
export GITHUB_TOKEN=your_token_here
python src/add_labels.py --owner your-username --repo your-game-project

# 4. Create issues on your repository
python src/create_issues.py ~/my-game-design.md --owner your-username --repo your-game-project
```

### Parse Design Document Only

To just parse and see what features are extracted:

```bash
python src/parse_design_doc.py examples/sample-design-doc.md
```

## Design Document Format

Create a design document using the provided template in `examples/design-doc-template.md`. The tool extracts information from:

- **Must-Have Features**: Checked items `[x]` will influence which issue categories are included
- **Nice-to-Have Features**: Optional features (currently for reference)
- **Technical Requirements**: AI, audio, multiplayer needs
- **Player Progression**: Leveling, skill trees, achievements
- **Game Genre**: Strategy, RPG, Platformer, etc.

### Example Design Document Structure

```markdown
# Your Game Title

## Game Overview
### Genre
Turn-based Strategy

## Features
### Must-Have Features (MVP)
- [x] Resource management system
- [x] Building placement

### AI Requirements
- [x] Pathfinding required
- [x] Enemy AI needed

### Audio Requirements
- [x] Background music
- [x] Sound effects
```

See `examples/sample-design-doc.md` for a complete example.

## Issue Categories

The tool generates issues organized into **7 broad categories** that align with project milestones:

1. **programming** - Programming and technical implementation
   - Core mechanics, AI systems, gameplay logic, networking, level systems, player progression

2. **art** - Visual art, graphics, and UI design
   - UI/UX design, rendering pipeline, camera systems, visual effects, animations, loading screens

3. **audio** - Sound effects and music
   - Audio system, sound effects, background music, volume controls

4. **QA** - Quality assurance, testing, and debugging
   - Unit tests, automated testing, debug tools, performance optimization, bug fixing

5. **documentation** - Documentation and technical writing
   - Game design docs, technical documentation, credits

6. **marketing** - Marketing and promotion
   - Marketing materials, social media, press kits

7. **business** - Business operations and analytics
   - Analytics, project management, development roadmap

These categories translate directly to GitHub milestones and labels for organized project tracking.

## Python Modules

The tool is organized into separate Python scripts:

### `parse_design_doc.py`
Parses game design documents and extracts features and requirements.

```python
from parse_design_doc import DesignDocParser

parser = DesignDocParser('path/to/design-doc.md')
data = parser.parse()
print(data['features'])
```

### `generate_issues.py`
Generates issues based on design document and templates.

```python
from generate_issues import IssueGenerator

generator = IssueGenerator()
generator.set_design_doc('path/to/design-doc.md')
issues = generator.generate_issues()
```

### `create_issues.py`
Creates issues on GitHub repository (requires GITHUB_TOKEN).

### `add_labels.py`
Adds standard game development labels to repository (requires GITHUB_TOKEN).

### `export_issues.py`
Exports issues to JSON or Markdown files.

## Customization

### Adding Custom Issue Templates

Edit `templates/issue-templates.json` to add your own issue templates or modify existing ones:

```json
{
  "categories": {
    "your_category": {
      "name": "Your Category Name",
      "description": "Description of this category",
      "templates": [
        {
          "title": "Issue title",
          "body": "Issue description",
          "labels": ["label1", "label2"]
        }
      ]
    }
  }
}
```

## Project Structure

```
GameDevProjectPlanCreator/
├── src/
│   ├── parse_design_doc.py    # Design document parser
│   ├── generate_issues.py     # Issue generator
│   ├── create_issues.py       # GitHub issue creation
│   ├── add_labels.py          # GitHub label management
│   └── export_issues.py       # Export to JSON/Markdown
├── templates/
│   └── issue-templates.json   # Issue templates
├── examples/
│   ├── design-doc-template.md # Template for creating design docs
│   └── sample-design-doc.md   # Example design document
├── output/                    # Generated files (created on demand)
├── requirements.txt           # Python dependencies
└── README.md
```

## Contributing

Contributions are welcome! Feel free to:

- Add new issue templates
- Improve design document parsing
- Add new export formats
- Enhance GitHub integration

## License

MIT License - see LICENSE file for details

## Origin Story

This tool was created to generalize the project planning approach used in the [TurnBasedEngine](https://github.com/samsmithnz/TurnBasedEngine) repository. The TBS project had comprehensive issue tracking for game development, and this tool extracts those learnings into a reusable system for any game project.

For details on how game-specific items from TBS were filtered and generalized, see [docs/filtering-game-specific-items.md](docs/filtering-game-specific-items.md).

## Related Projects

- [TurnBasedEngine](https://github.com/samsmithnz/TurnBasedEngine) - The turn-based strategy game that inspired this tool

