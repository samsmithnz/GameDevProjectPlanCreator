#!/usr/bin/env node

const GameDevProjectPlanCreator = require('./GameDevProjectPlanCreator');
const path = require('path');
const fs = require('fs');

// Parse command line arguments
const args = process.argv.slice(2);

function printUsage() {
  console.log(`
Game Dev Project Plan Creator
==============================

Usage:
  node src/cli.js <design-doc-path> [options]

Options:
  --export-json <path>     Export issues to JSON file
  --export-md <path>       Export issues to Markdown file
  --create-issues          Create issues on GitHub (requires --owner and --repo)
  --owner <owner>          GitHub repository owner
  --repo <repo>            GitHub repository name
  --help                   Show this help message

Environment Variables:
  GITHUB_TOKEN             GitHub personal access token (required for --create-issues)

Examples:
  # Generate and export to JSON
  node src/cli.js examples/sample-design-doc.md --export-json output.json

  # Generate and export to Markdown
  node src/cli.js examples/sample-design-doc.md --export-md project-plan.md

  # Create issues on GitHub
  export GITHUB_TOKEN=your_token_here
  node src/cli.js examples/sample-design-doc.md --create-issues --owner username --repo repo-name

  # Export both JSON and Markdown
  node src/cli.js examples/sample-design-doc.md --export-json output.json --export-md plan.md
`);
}

// Check for help flag
if (args.includes('--help') || args.length === 0) {
  printUsage();
  process.exit(0);
}

// Get design doc path
const designDocPath = args[0];

if (!designDocPath) {
  console.error('Error: Design document path is required');
  printUsage();
  process.exit(1);
}

if (!fs.existsSync(designDocPath)) {
  console.error(`Error: Design document not found: ${designDocPath}`);
  process.exit(1);
}

// Parse options
const options = {
  exportJson: null,
  exportMd: null,
  createIssues: false,
  owner: null,
  repo: null
};

for (let i = 1; i < args.length; i++) {
  switch (args[i]) {
    case '--export-json':
      options.exportJson = args[++i];
      break;
    case '--export-md':
      options.exportMd = args[++i];
      break;
    case '--create-issues':
      options.createIssues = true;
      break;
    case '--owner':
      options.owner = args[++i];
      break;
    case '--repo':
      options.repo = args[++i];
      break;
  }
}

// Validate options
if (options.createIssues && (!options.owner || !options.repo)) {
  console.error('Error: --owner and --repo are required when using --create-issues');
  process.exit(1);
}

// Main execution
async function main() {
  try {
    console.log('🎮 Game Dev Project Plan Creator');
    console.log('=================================\n');

    // Create instance
    const creator = new GameDevProjectPlanCreator();

    // Parse design doc
    console.log(`📄 Parsing design document: ${designDocPath}`);
    creator.parseDesignDoc(designDocPath);
    console.log('✓ Design document parsed\n');

    // Generate issues
    console.log('🔨 Generating issues...');
    const issues = creator.generateIssues();
    console.log(`✓ Generated ${issues.length} issues\n`);

    // Generate report
    const report = creator.generateReport(issues);
    console.log('📊 Project Plan Summary:');
    console.log(`   Total Issues: ${report.totalIssues}`);
    console.log('\n   By Category:');
    for (const [category, count] of Object.entries(report.byCategory)) {
      console.log(`   - ${category}: ${count}`);
    }
    console.log('\n   By Label:');
    for (const [label, count] of Object.entries(report.byLabel)) {
      console.log(`   - ${label}: ${count}`);
    }
    console.log();

    // Export to JSON
    if (options.exportJson) {
      creator.exportToJson(issues, options.exportJson);
      console.log();
    }

    // Export to Markdown
    if (options.exportMd) {
      creator.exportToMarkdown(issues, options.exportMd);
      console.log();
    }

    // Create GitHub issues
    if (options.createIssues) {
      console.log(`🚀 Creating issues on GitHub (${options.owner}/${options.repo})...`);
      const createdIssues = await creator.createGitHubIssues(options.owner, options.repo, issues);
      console.log(`\n✓ Created ${createdIssues.length} issues on GitHub\n`);
    }

    console.log('✅ Done!');
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
