# Contributing to GameDevProjectPlanCreator

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists
2. Create a new issue with a clear title and description
3. Include steps to reproduce (for bugs)
4. Include your use case (for feature requests)

### Adding New Issue Templates

To add new issue templates to the system:

1. Open `templates/issue-templates.json`
2. Add a new category or add templates to an existing category
3. Follow this structure:

```json
{
  "categories": {
    "your_new_category": {
      "name": "Display Name",
      "description": "What this category covers",
      "templates": [
        {
          "title": "Issue title",
          "body": "Detailed description of the issue/task",
          "labels": ["label1", "label2"]
        }
      ]
    }
  }
}
```

#### Template Guidelines

- **Title**: Should be action-oriented (e.g., "Add", "Implement", "Create")
- **Body**: Should be clear and provide enough context
- **Labels**: Use consistent labels across templates
  - Common labels: `enhancement`, `bug`, `documentation`, `testing`
  - Category-specific: `core`, `ai`, `ui`, `audio`, `graphics`, etc.

### Improving the Design Doc Parser

The design doc parser in `src/GameDevProjectPlanCreator.js` extracts information from markdown files. To improve it:

1. Look at the `parseDesignDoc()` and `extractFeatures()` methods
2. Add new extraction logic for additional fields
3. Update the design doc template to include new fields
4. Test with a sample design doc

### Adding Export Formats

Currently supported: JSON, Markdown

To add a new export format:

1. Add a method to `GameDevProjectPlanCreator` class (e.g., `exportToCSV()`)
2. Add a CLI option in `src/cli.js`
3. Update README with usage examples
4. Test the export functionality

### Code Style

- Use clear, descriptive variable and function names
- Add comments for complex logic
- Follow existing code formatting
- Use consistent indentation (2 spaces)

### Testing Your Changes

Before submitting:

1. Test the CLI with the sample design doc:
   ```bash
   node src/cli.js examples/sample-design-doc.md --export-md test.md
   ```

2. Verify the generated output is correct

3. Test edge cases (empty design doc, missing sections, etc.)

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request with:
   - Clear description of changes
   - Why the change is needed
   - How to test it

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/GameDevProjectPlanCreator.git
cd GameDevProjectPlanCreator

# Install dependencies
pip install -r requirements.txt

# Test the tool
python src/export_issues.py examples/sample-design-doc.md --markdown output/test.md

# Run with custom design doc
python src/export_issues.py path/to/your-design-doc.md --markdown output.md
```

## Ideas for Contributions

Here are some ideas if you're looking for something to work on:

### Easy
- Add more issue templates for specific game genres
- Improve error messages
- Add more design doc examples
- Improve documentation

### Medium
- Add CSV export format
- Add issue priority/milestone assignment
- Improve design doc parsing (better feature extraction)
- Add issue dependencies/relationships

### Advanced
- Add AI-powered issue generation based on design doc context
- Create a web interface
- Add project board creation via GitHub API
- Add support for other issue trackers (GitLab, Jira, etc.)

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
