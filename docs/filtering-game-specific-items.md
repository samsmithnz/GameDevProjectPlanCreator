# How Game-Specific Items are Filtered

## Overview

This tool was created by analyzing the [TurnBasedEngine (TBS)](https://github.com/samsmithnz/TurnBasedEngine) repository, which had many game-specific issues for a turn-based strategy game. The goal was to extract the general patterns and create reusable templates.

## Filtering Approach

### Game-Specific Issues from TBS (Filtered Out)

The following types of issues from TBS were **too specific** and not included:

1. **TBS-Specific Mechanics**
   - Cover system (high/low cover)
   - Field of view (FOV) calculations
   - Overwatch mechanics
   - Flanking mechanics
   - Chance to hit calculations
   - Splash damage
   - Dodge mechanics

2. **TBS-Specific Features**
   - Mission objectives (kill all enemies)
   - Research system (specific to this game)
   - Character ability trees (too game-specific)
   - Stealth mechanics
   - Hunker down ability

3. **Implementation Details**
   - Specific pathfinding bugs (diagonal movement)
   - Specific targeting issues
   - Queue object implementation
   - DLL signing

### Generic Patterns Extracted

Instead, we extracted these **7 broad categories** that apply to most games and align with project milestones:

1. **programming** (from TBS: core mechanics, AI, networking, progression)
   - Game loop and state management
   - AI systems and pathfinding
   - Player progression and leveling
   - Networking and multiplayer
   - Level loading systems

2. **art** (from TBS: UI, graphics, rendering)
   - UI/UX design (menus, HUD)
   - Graphics rendering pipeline
   - Visual effects and animations
   - Camera systems
   - Loading screens

3. **audio** (from TBS: sound systems)
   - Audio system manager
   - Sound effects
   - Background music

4. **QA** (from TBS: testing, optimization, polish)
   - Unit tests and automated testing
   - Debug tools
   - Performance optimization
   - Bug fixing and stability

5. **documentation**
   - Game design documentation
   - Technical documentation
   - Credits and acknowledgments

6. **marketing** (from TBS: launch activities)
   - Marketing materials
   - Social media presence
   - Press kits

7. **business**
   - Analytics and metrics
   - Project management
   - Development roadmap

## How the Tool Decides What to Include

The tool uses the **design document** to determine which categories to include:

### 1. Always Included
- programming (core mechanics essential for any game)
- UI/UX
- Graphics & Rendering
- Level Design
- Testing & QA
- art (visual design essential for any game)
- QA (testing essential for quality)
- documentation (important for project clarity)
- marketing (launch preparation important)
- business (project management essential)

### 2. Conditionally Included (Based on Design Doc)

**audio** - Included if design doc has:
```markdown
### Audio Requirements
- [x] Background music
- [x] Sound effects
- [x] Voice acting
```

Note: With the 7-category structure, most categories are always included as they represent essential aspects of game development. The conditional logic primarily affects the audio category.

## Examples

### TBS Issue → Generic Template

**TBS-Specific:**
```
Title: "Fix pathfinding - you can currently walk in the diagonal between two objects"
Category: Bug fix for specific implementation
Action: Filtered out (too specific)
```

**Generic Template:**
```
Title: "Implement AI pathfinding"
Body: "Add pathfinding logic for AI characters to navigate the game world"
Labels: enhancement, ai
Action: Included as generic template
```

---

**TBS-Specific:**
```
Title: "Cover system needs to differentiate between high and low cover"
Category: TBS-specific game mechanic
Action: Filtered out (specific to tactical games)
```

**Generic Template:**
```
Title: "Create player character controller"
Body: "Implement player character movement and basic controls"
Labels: enhancement, core
Action: Included as generic template
```

---

**TBS-Specific:**
```
Title: "Add field of view calculations"
Category: TBS-specific vision system
Action: Filtered out (too specific)
```

**Generic Template:**
```
Title: "Add camera system"
Body: "Implement camera controls and movement"
Labels: enhancement, graphics
Action: Included as generic template
```

## Design Philosophy

The tool follows this philosophy:

1. **Breadth over Depth**: Include a wide range of common game development tasks rather than deep, specific implementations
2. **Flexibility**: Templates are general enough to apply to any game genre
3. **Customization**: Users can edit templates to fit their specific needs
4. **Guidance**: Templates provide a starting point, not a complete specification

## Adding Game-Specific Issues

While the tool provides generic templates, you can still add game-specific issues by:

1. Manually creating issues on GitHub after running the tool
2. Editing the generated Markdown/JSON files before import
3. Creating custom template files for your specific game genre
4. Using the tool as a foundation and building on top of it

The generic templates ensure you don't forget the fundamentals, while still allowing room for your game's unique features.
