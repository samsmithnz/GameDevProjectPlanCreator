# GameDevProjectPlanCreator

A tool that automatically generates comprehensive GitHub issues for game development projects based on a design document. This tool helps game developers quickly set up project boards with all necessary tasks, from core mechanics to launch preparation.

## Features

- 📝 Parse game design documents to extract requirements
- 🎯 Generate categorized GitHub issues based on game features
- 🏷️ Automatic labeling and organization
- 📊 Export to JSON or Markdown
- 🚀 Direct GitHub integration to create issues
- 🎮 Generic templates applicable to any game genre

## Installation

### Prerequisites

- Node.js 14.x or higher
- npm or yarn
- GitHub account (for creating issues)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/samsmithnz/GameDevProjectPlanCreator.git
cd GameDevProjectPlanCreator
```

2. Install dependencies:
```bash
npm install
```

3. (Optional) For GitHub integration, create a `.env` file:
```bash
GITHUB_TOKEN=your_github_personal_access_token
```

To create a GitHub personal access token:
- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate new token with `repo` scope
- Copy the token and add it to your `.env` file

## Usage

### Basic Usage

Generate issues from a design document:

```bash
node src/cli.js examples/sample-design-doc.md --export-md project-plan.md
```

### Export Options

Export to JSON:
```bash
node src/cli.js path/to/design-doc.md --export-json issues.json
```

Export to Markdown:
```bash
node src/cli.js path/to/design-doc.md --export-md project-plan.md
```

Export to both:
```bash
node src/cli.js path/to/design-doc.md --export-json issues.json --export-md plan.md
```

### Create GitHub Issues

Create issues directly on your GitHub repository:

```bash
export GITHUB_TOKEN=your_token_here
node src/cli.js path/to/design-doc.md --create-issues --owner your-username --repo your-repo
```

### Using npm scripts

```bash
# Run the example
npm run example

# Use the CLI directly
npm start -- examples/sample-design-doc.md --export-md output.md
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

## Programmatic Usage

You can also use this tool programmatically in your own Node.js scripts:

```javascript
const GameDevProjectPlanCreator = require('./src/GameDevProjectPlanCreator');

const creator = new GameDevProjectPlanCreator({
  githubToken: 'your_token_here' // Optional
});

// Parse design document
creator.parseDesignDoc('path/to/design-doc.md');

// Generate issues
const issues = creator.generateIssues();

// Export to file
creator.exportToMarkdown(issues, 'project-plan.md');

// Or create on GitHub
await creator.createGitHubIssues('owner', 'repo', issues);
```

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
│   ├── GameDevProjectPlanCreator.js  # Main class
│   └── cli.js                         # Command-line interface
├── templates/
│   └── issue-templates.json           # Issue templates
├── examples/
│   ├── design-doc-template.md         # Template for creating design docs
│   └── sample-design-doc.md           # Example design document
├── output/                            # Generated files (created on demand)
├── package.json
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

