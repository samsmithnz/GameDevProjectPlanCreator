# GameDevProjectPlanCreator

A Python tool that automatically generates comprehensive GitHub issues for game development projects based on a design document. This tool helps game developers quickly set up project boards with all necessary tasks, from core mechanics to launch preparation.

## Features

- 📝 Parse game design documents to extract requirements
- 🎯 Generate categorized GitHub issues based on game features
- 🏷️ Automatic labeling and organization
- 📊 Export to JSON or Markdown
- 🚀 Direct GitHub integration to create issues and labels
- 🎮 Generic templates applicable to any game genre

## Installation

### Prerequisites

- Python 3.7 or higher
- pip
- GitHub account (for creating issues)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/samsmithnz/GameDevProjectPlanCreator.git
cd GameDevProjectPlanCreator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) For GitHub integration, set your token as an environment variable:
```bash
export GITHUB_TOKEN=your_github_personal_access_token
```

To create a GitHub personal access token:
- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate new token with `repo` scope
- Copy the token and set it as GITHUB_TOKEN environment variable

## Usage

### Export Issues to Files

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

### Add Labels to Repository

Add standard game development labels to your GitHub repository:

```bash
export GITHUB_TOKEN=your_token_here
python src/add_labels.py --owner your-username --repo your-repo
```

### Create GitHub Issues

Create issues directly on your GitHub repository:

```bash
export GITHUB_TOKEN=your_token_here
python src/create_issues.py examples/sample-design-doc.md --owner your-username --repo your-repo
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

The tool generates issues in the following categories:

1. **Core Mechanics** - Fundamental gameplay systems
   - Game loop, player controls, state management

2. **AI Systems** - Artificial intelligence (if needed)
   - Pathfinding, decision-making, difficulty levels

3. **UI/UX** - User interface elements
   - Menus, HUD, settings, accessibility

4. **Audio** - Sound and music (if needed)
   - Sound effects, background music, audio manager

5. **Graphics & Rendering** - Visual systems
   - Rendering pipeline, camera, animations, effects

6. **Level Design** - Maps and levels
   - Level loader, tutorial, progression

7. **Player Progression** - Character advancement (if needed)
   - Experience system, skill trees, achievements

8. **Multiplayer** - Networking (if needed)
   - Lobby, synchronization, matchmaking

9. **Testing & QA** - Quality assurance
   - Unit tests, debugging, optimization

10. **Polish & Launch** - Final preparation
    - Loading screens, analytics, marketing materials

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

