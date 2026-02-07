const fs = require('fs');
const path = require('path');
const { Octokit } = require('@octokit/rest');
require('dotenv').config();

class GameDevProjectPlanCreator {
  constructor(options = {}) {
    this.templates = this.loadTemplates();
    this.designDoc = null;
    this.githubToken = options.githubToken || process.env.GITHUB_TOKEN;
    this.octokit = this.githubToken ? new Octokit({ auth: this.githubToken }) : null;
  }

  /**
   * Load issue templates from JSON file
   */
  loadTemplates() {
    const templatesPath = path.join(__dirname, '../templates/issue-templates.json');
    const data = fs.readFileSync(templatesPath, 'utf8');
    return JSON.parse(data);
  }

  /**
   * Parse a design document to extract features and requirements
   * @param {string} designDocPath - Path to the design document markdown file
   */
  parseDesignDoc(designDocPath) {
    const content = fs.readFileSync(designDocPath, 'utf8');
    this.designDoc = {
      raw: content,
      features: this.extractFeatures(content),
      requirements: this.extractRequirements(content)
    };
    return this.designDoc;
  }

  /**
   * Extract checked features from design doc
   */
  extractFeatures(content) {
    const features = {
      mustHave: [],
      niceToHave: [],
      multiplayer: false,
      ai: false,
      audio: false,
      graphics: null,
      progression: []
    };

    // Extract must-have features
    const mustHaveMatch = content.match(/### Must-Have Features.*?\n([\s\S]*?)(?=###|##|$)/);
    if (mustHaveMatch) {
      const items = mustHaveMatch[1].match(/- \[x\] (.+)/g);
      if (items) {
        features.mustHave = items.map(item => item.replace(/- \[x\] /, '').trim());
      }
    }

    // Extract nice-to-have features
    const niceToHaveMatch = content.match(/### Nice-to-Have Features.*?\n([\s\S]*?)(?=###|##|$)/);
    if (niceToHaveMatch) {
      const items = niceToHaveMatch[1].match(/- \[x\] (.+)/g);
      if (items) {
        features.niceToHave = items.map(item => item.replace(/- \[x\] /, '').trim());
      }
    }

    // Check for multiplayer
    features.multiplayer = content.includes('[x] Local multiplayer') || 
                          content.includes('[x] Online multiplayer');

    // Check for AI requirements
    features.ai = content.includes('[x] Enemy AI needed') || 
                 content.includes('[x] NPC AI needed') ||
                 content.includes('[x] Pathfinding required');

    // Check for audio
    features.audio = content.includes('[x] Background music') || 
                    content.includes('[x] Sound effects') ||
                    content.includes('[x] Voice acting');

    // Extract progression systems
    const progressionMatch = content.match(/### Player Progression.*?\n([\s\S]*?)(?=###|##|$)/);
    if (progressionMatch) {
      const items = progressionMatch[1].match(/- \[x\] (.+)/g);
      if (items) {
        features.progression = items.map(item => item.replace(/- \[x\] /, '').trim());
      }
    }

    return features;
  }

  /**
   * Extract requirements from design doc
   */
  extractRequirements(content) {
    return {
      engine: this.extractField(content, 'Engine/Framework'),
      language: this.extractField(content, 'Programming Language'),
      platform: this.extractField(content, 'Target Platform'),
      genre: this.extractField(content, 'Genre')
    };
  }

  /**
   * Extract a specific field value from markdown content
   */
  extractField(content, fieldName) {
    const regex = new RegExp(`### ${fieldName}\\s*\\n([^\\n#]+)`, 'i');
    const match = content.match(regex);
    return match ? match[1].replace(/\[|\]/g, '').trim() : null;
  }

  /**
   * Generate a set of issues based on design doc and templates
   */
  generateIssues() {
    if (!this.designDoc) {
      throw new Error('No design document parsed. Call parseDesignDoc() first.');
    }

    const issues = [];
    const features = this.designDoc.features;

    // Always include core mechanics
    issues.push(...this.templates.categories.core_mechanics.templates);

    // Add AI issues if needed
    if (features.ai) {
      issues.push(...this.templates.categories.ai_systems.templates);
    }

    // Always add UI/UX
    issues.push(...this.templates.categories.ui_ux.templates);

    // Add audio if needed
    if (features.audio) {
      issues.push(...this.templates.categories.audio.templates);
    }

    // Always add graphics/rendering
    issues.push(...this.templates.categories.graphics_rendering.templates);

    // Always add level design
    issues.push(...this.templates.categories.level_design.templates);

    // Add progression if specified
    if (features.progression.length > 0) {
      issues.push(...this.templates.categories.player_progression.templates);
    }

    // Add multiplayer if needed
    if (features.multiplayer) {
      issues.push(...this.templates.categories.multiplayer.templates);
    }

    // Always add testing and polish
    issues.push(...this.templates.categories.testing_qa.templates);
    issues.push(...this.templates.categories.polish.templates);

    return issues;
  }

  /**
   * Create issues on GitHub
   * @param {string} owner - Repository owner
   * @param {string} repo - Repository name
   * @param {Array} issues - Array of issue objects
   */
  async createGitHubIssues(owner, repo, issues) {
    if (!this.octokit) {
      throw new Error('GitHub token not configured. Set GITHUB_TOKEN environment variable.');
    }

    const createdIssues = [];

    for (const issue of issues) {
      try {
        const response = await this.octokit.issues.create({
          owner,
          repo,
          title: issue.title,
          body: issue.body,
          labels: issue.labels || []
        });
        
        createdIssues.push(response.data);
        console.log(`✓ Created issue #${response.data.number}: ${issue.title}`);
        
        // Rate limiting - wait a bit between requests
        await new Promise(resolve => setTimeout(resolve, 500));
      } catch (error) {
        console.error(`✗ Failed to create issue "${issue.title}":`, error.message);
      }
    }

    return createdIssues;
  }

  /**
   * Generate a summary report of the project plan
   */
  generateReport(issues) {
    const report = {
      totalIssues: issues.length,
      byCategory: {},
      byLabel: {}
    };

    // Count by category
    for (const [categoryKey, category] of Object.entries(this.templates.categories)) {
      const categoryIssues = issues.filter(issue => 
        category.templates.some(t => t.title === issue.title)
      );
      if (categoryIssues.length > 0) {
        report.byCategory[category.name] = categoryIssues.length;
      }
    }

    // Count by label
    for (const issue of issues) {
      if (issue.labels) {
        for (const label of issue.labels) {
          report.byLabel[label] = (report.byLabel[label] || 0) + 1;
        }
      }
    }

    return report;
  }

  /**
   * Export issues to a JSON file
   */
  exportToJson(issues, outputPath) {
    fs.writeFileSync(outputPath, JSON.stringify(issues, null, 2));
    console.log(`Exported ${issues.length} issues to ${outputPath}`);
  }

  /**
   * Export issues to a Markdown file
   */
  exportToMarkdown(issues, outputPath) {
    let markdown = '# Game Development Project Plan\n\n';
    markdown += `Generated on: ${new Date().toISOString()}\n\n`;
    markdown += `Total Issues: ${issues.length}\n\n`;
    markdown += '---\n\n';

    // Group by category
    const categorizedIssues = {};
    for (const issue of issues) {
      // Find which category this issue belongs to
      let categoryName = 'Other';
      for (const [categoryKey, category] of Object.entries(this.templates.categories)) {
        if (category.templates.some(t => t.title === issue.title)) {
          categoryName = category.name;
          break;
        }
      }
      
      if (!categorizedIssues[categoryName]) {
        categorizedIssues[categoryName] = [];
      }
      categorizedIssues[categoryName].push(issue);
    }

    // Write categorized issues
    for (const [categoryName, categoryIssues] of Object.entries(categorizedIssues)) {
      markdown += `## ${categoryName}\n\n`;
      for (const issue of categoryIssues) {
        markdown += `### ${issue.title}\n\n`;
        markdown += `${issue.body}\n\n`;
        if (issue.labels && issue.labels.length > 0) {
          markdown += `**Labels:** ${issue.labels.join(', ')}\n\n`;
        }
        markdown += '---\n\n';
      }
    }

    fs.writeFileSync(outputPath, markdown);
    console.log(`Exported ${issues.length} issues to ${outputPath}`);
  }
}

module.exports = GameDevProjectPlanCreator;
