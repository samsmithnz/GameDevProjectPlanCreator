# Game Project Plan - User Stories Template

This template follows the format used in the TBS project. Create detailed user stories for your game using this structure.

## Label Structure

Each user story includes:
- **Category Label** - High-level categorization (choose from):
  - `programming` - Development/coding tasks
  - `art` - Art and visual design
  - `audio` - Sound and music
  - `marketing` - Marketing and community
  - `business` - Business operations
  - `qa` - QA and testing
  - `documentation` - Documentation work

## User Story Format

Use this format for each user story:

```
- **US-CAT-###**: As a [user type], I want [goal] so that [benefit]
  - Labels: `[category]`, `[optional-subcategory]`
  - Acceptance Criteria:
    - [Criterion 1]
    - [Criterion 2]
    - [Criterion 3]
```

Replace:
- `CAT` with category code: PROG, ART, AUDIO, MKT, BUS, QA, DOC
- `###` with sequential number (001, 002, etc.)

---

## Programming - Core Gameplay

### Example User Stories

- **US-PROG-001**: As a player, I want [core mechanic] so that [gameplay benefit]
  - Labels: `programming`, `gameplay`
  - Acceptance Criteria:
    - [What needs to work]
    - [How it should behave]
    - [What the player experiences]

- **US-PROG-002**: As a player, I want [feature description]
  - Labels: `programming`, `[subcategory]`
  - Acceptance Criteria:
    - [Criterion 1]
    - [Criterion 2]

[Add more programming user stories here]

---

## Art - Visual Design

### Example User Stories

- **US-ART-001**: As a player, I want [visual element] so that [visual benefit]
  - Labels: `art`, `[subcategory]`
  - Acceptance Criteria:
    - [Visual quality requirement]
    - [Art style consistency]
    - [Technical specifications]

[Add more art user stories here]

---

## Audio - Sound Design

### Example User Stories

- **US-AUDIO-001**: As a player, I want [audio element] so that [audio benefit]
  - Labels: `audio`, `[subcategory]`
  - Acceptance Criteria:
    - [Sound quality requirement]
    - [Audio implementation details]
    - [Player experience]

[Add more audio user stories here]

---

## Marketing - Community & Promotion

### Example User Stories

- **US-MKT-001**: As a marketing team member, I want [marketing activity] so that [marketing goal]
  - Labels: `marketing`, `[subcategory]`
  - Acceptance Criteria:
    - [Deliverable 1]
    - [Metric/goal]
    - [Timeline]

[Add more marketing user stories here]

---

## Business - Operations & Finance

### Example User Stories

- **US-BUS-001**: As a business owner, I want [business activity] so that [business benefit]
  - Labels: `business`, `[subcategory]`
  - Acceptance Criteria:
    - [Requirement 1]
    - [Requirement 2]
    - [Success criteria]

[Add more business user stories here]

---

## QA - Testing & Quality

### Example User Stories

- **US-QA-001**: As a QA tester, I want [testing activity] so that [quality goal]
  - Labels: `qa`, `testing`
  - Acceptance Criteria:
    - [Testing scope]
    - [Coverage requirement]
    - [Success criteria]

[Add more QA user stories here]

---

## Documentation

### Example User Stories

- **US-DOC-001**: As a [reader type], I want [documentation] so that [information goal]
  - Labels: `documentation`, `[type]`
  - Acceptance Criteria:
    - [Content requirements]
    - [Format/structure]
    - [Accessibility]

[Add more documentation user stories here]

---

## Instructions for Use

1. **Copy this template** and rename it (e.g., `my-game-user-stories.md`)

2. **Fill in user stories** for your game using the format above

3. **Use the create_issues.py script** to parse your file and create GitHub issues:
   ```bash
   python src/create_issues.py your-user-stories.md --owner you --repo your-game
   ```

4. **Organize on GitHub**: Create milestones for phases (Alpha, Beta, Release) and organize issues

## Tips

- Be specific in user stories - describe what the player/user experiences
- Include measurable acceptance criteria
- Group related stories together
- Use consistent numbering within each category
- Consider priority when ordering stories
- Add subcategory labels for filtering (e.g., `combat`, `ui`, `performance`)
