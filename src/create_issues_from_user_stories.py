#!/usr/bin/env python3
"""
Create GitHub Issues from User Stories

This script parses a markdown file containing user stories and creates GitHub issues.
Follows the pattern from the TBS project's create_2026_issues.py.

Format expected in markdown file:
- **US-CAT-###**: As a [user], I want [goal] so that [benefit]
  - Labels: `label1`, `label2`
  - Acceptance Criteria:
    - Criterion 1
    - Criterion 2

Prerequisites:
- Python 3.7+
- PyGithub: pip install PyGithub

Usage:
    export GITHUB_TOKEN=your_token_here
    python create_issues_from_user_stories.py <user-stories-file> --owner <owner> --repo <repo>
    
    # Dry run (preview without creating)
    python create_issues_from_user_stories.py <file> --owner <owner> --repo <repo> --dry-run
"""

import os
import re
import sys
import argparse
from typing import List, Dict
from github import Github, GithubException


class UserStory:
    """Represents a user story to be created as a GitHub issue."""
    
    def __init__(self, story_id: str, title: str, description: str,
                 labels: List[str], acceptance_criteria: List[str]):
        self.story_id = story_id
        self.title = f"{story_id}: {title}"
        self.description = description
        self.labels = labels if labels else []
        self.acceptance_criteria = acceptance_criteria if acceptance_criteria else []
    
    def get_body(self) -> str:
        """Generate the issue body in markdown format."""
        body_parts = [self.description]
        
        if self.acceptance_criteria:
            body_parts.append("\n**Acceptance Criteria:**")
            for criterion in self.acceptance_criteria:
                body_parts.append(f"- {criterion}")
        
        if self.labels:
            body_parts.append(f"\n**Labels:** {', '.join(self.labels)}")
        
        return "\n".join(body_parts)


def parse_user_stories(markdown_file: str) -> List[UserStory]:
    """Parse user stories from the markdown file."""
    user_stories = []
    
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {markdown_file} not found.")
        sys.exit(1)
    
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this is a user story line
        # Format: - **US-XXX-###**: As a..., I want... so that...
        if line.startswith('- **US-'):
            # Extract story ID and title
            match = re.match(r'- \*\*([A-Z]+-[A-Z]+-\d+)\*\*: (.+)', line)
            if match:
                story_id = match.group(1)
                title = match.group(2)
                
                # Look ahead for labels and acceptance criteria
                labels = []
                acceptance_criteria = []
                description = title
                
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    if next_line.startswith('- Labels:'):
                        # Parse labels
                        label_text = next_line.replace('- Labels:', '').strip()
                        label_text = label_text.replace('`', '')
                        parsed_labels = [l.strip() for l in label_text.split(',')]
                        labels = [l for l in parsed_labels if l]
                        j += 1
                    elif next_line.startswith('- Acceptance Criteria:'):
                        # Start collecting acceptance criteria
                        j += 1
                        while j < len(lines):
                            criteria_line = lines[j].strip()
                            if criteria_line.startswith('- ') and not criteria_line.startswith('- **US-'):
                                # This is an acceptance criterion
                                criterion = criteria_line.lstrip('- ').strip()
                                if criterion and not criterion.startswith('Labels:') and not criterion.startswith('Acceptance Criteria:'):
                                    acceptance_criteria.append(criterion)
                                j += 1
                            else:
                                break
                        break
                    elif next_line.startswith('- **US-'):
                        # Next user story, stop here
                        break
                    elif next_line == '':
                        # Empty line, continue
                        j += 1
                    else:
                        j += 1
                
                # Create the user story
                story = UserStory(
                    story_id=story_id,
                    title=title,
                    description=description,
                    labels=labels,
                    acceptance_criteria=acceptance_criteria
                )
                user_stories.append(story)
                i = j
                continue
        
        i += 1
    
    return user_stories


def create_github_issues(owner: str, repo: str, user_stories: List[UserStory],
                         dry_run: bool = False, token: str = None):
    """
    Create GitHub issues from user stories.
    
    Args:
        owner: Repository owner
        repo: Repository name
        user_stories: List of UserStory objects
        dry_run: If True, only print what would be created
        token: GitHub personal access token
    
    Returns:
        Tuple of (successful, failed) counts
    """
    if not dry_run:
        if not token:
            token = os.environ.get('GITHUB_TOKEN')
        
        if not token:
            print("Error: GITHUB_TOKEN environment variable not set.")
            print("Create a token at: https://github.com/settings/tokens")
            print("Set it with: export GITHUB_TOKEN=your_token_here")
            sys.exit(1)
    
    # Initialize GitHub API only if not dry run
    successful = 0
    failed = 0
    
    if not dry_run:
        g = Github(token)
        
        try:
            repository = g.get_repo(f"{owner}/{repo}")
            print(f"✓ Connected to repository: {owner}/{repo}\n")
        except GithubException as e:
            print(f"Error accessing repository {owner}/{repo}: {e}")
            sys.exit(1)
    
    print(f"{'[DRY RUN] ' if dry_run else ''}Creating {len(user_stories)} issues...\n")
    
    for story in user_stories:
        try:
            if dry_run:
                print(f"Would create: {story.title}")
                print(f"  Labels: {', '.join(story.labels)}")
                print(f"  Criteria: {len(story.acceptance_criteria)} items")
                successful += 1
            else:
                issue = repository.create_issue(
                    title=story.title,
                    body=story.get_body(),
                    labels=story.labels
                )
                print(f"✓ Created issue #{issue.number}: {story.title}")
                successful += 1
                
                # Rate limiting - wait 500ms between requests
                time.sleep(0.5)
        except GithubException as e:
            print(f"✗ Failed to create {story.title}: {e}")
            failed += 1
    
    return successful, failed


def main():
    parser = argparse.ArgumentParser(
        description='Create GitHub issues from user stories markdown file'
    )
    parser.add_argument(
        'user_stories_file',
        help='Path to the markdown file containing user stories'
    )
    parser.add_argument(
        '--owner',
        required=True,
        help='GitHub repository owner'
    )
    parser.add_argument(
        '--repo',
        required=True,
        help='GitHub repository name'
    )
    parser.add_argument(
        '--token',
        help='GitHub personal access token (or use GITHUB_TOKEN env var)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview issues without creating them'
    )
    
    args = parser.parse_args()
    
    print('🎮 Game Dev Project Plan Creator - User Story Issue Creator')
    print('=' * 65)
    print()
    
    if args.dry_run:
        print("Running in DRY RUN mode (no issues will be created)")
        print("Remove --dry-run flag to create issues for real\n")
    
    # Parse user stories
    print(f"📄 Parsing user stories from: {args.user_stories_file}")
    user_stories = parse_user_stories(args.user_stories_file)
    print(f"✓ Found {len(user_stories)} user stories\n")
    
    if len(user_stories) == 0:
        print("Warning: No user stories found. Check the file format.")
        print("Expected format:")
        print("- **US-CAT-###**: As a user, I want... so that...")
        print("  - Labels: `label1`, `label2`")
        print("  - Acceptance Criteria:")
        print("    - Criterion 1")
        sys.exit(1)
    
    # Show summary by category
    categories = {}
    for story in user_stories:
        # Extract category from story ID (US-PROG-001 -> PROG)
        parts = story.story_id.split('-')
        if len(parts) >= 2:
            category = parts[1]
            categories[category] = categories.get(category, 0) + 1
    
    print("User stories by category:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count}")
    print()
    
    # Confirm before creating (unless dry-run)
    if not args.dry_run:
        response = input(f"Create {len(user_stories)} issues in {args.owner}/{args.repo}? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            sys.exit(0)
        print()
    
    # Create issues
    successful, failed = create_github_issues(
        args.owner,
        args.repo,
        user_stories,
        args.dry_run,
        args.token
    )
    
    # Print summary
    print()
    print("=" * 65)
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Summary:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(user_stories)}")
    
    if not args.dry_run and successful > 0:
        print(f"\nView issues: https://github.com/{args.owner}/{args.repo}/issues")
    
    if args.dry_run:
        print("\nThis was a DRY RUN. No changes were made.")
        print("Run without --dry-run to create issues for real.")
    
    print()


if __name__ == "__main__":
    main()
