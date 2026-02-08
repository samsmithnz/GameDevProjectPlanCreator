#!/usr/bin/env python3
"""
Game Development Project Setup

This is the main entry point for setting up a complete game development project with:
- GitHub issues organized by category
- Project board with milestones
- Standardized labels

Prerequisites:
- Python 3.7+
- PyGithub: pip install PyGithub

Usage:
    export GITHUB_TOKEN=your_token_here
    python setup_game_project.py --design-doc <path> --owner <owner> --repo <repo>
    
    # Dry run to preview
    python setup_game_project.py --design-doc <path> --owner <owner> --repo <repo> --dry-run
"""

import os
import sys
import argparse
import time
import re
from typing import List, Dict, Tuple, Optional
from github import Github, GithubException


# 7 milestone categories for game development
MILESTONES = [
    {'title': 'programming', 'description': 'Programming and technical implementation'},
    {'title': 'art', 'description': 'Visual art, graphics, and UI design'},
    {'title': 'audio', 'description': 'Sound effects and music systems'},
    {'title': 'QA', 'description': 'Quality assurance, testing, and debugging'},
    {'title': 'documentation', 'description': 'Documentation and technical writing'},
    {'title': 'marketing', 'description': 'Marketing and promotional activities'},
    {'title': 'business', 'description': 'Business operations and analytics'},
]

# Standard labels aligned with milestones
STANDARD_LABELS = [
    {'name': 'enhancement', 'color': 'a2eeef', 'description': 'New feature or request'},
    {'name': 'bug', 'color': 'd73a4a', 'description': 'Something isn\'t working'},
    {'name': 'programming', 'color': '0e8a16', 'description': 'Programming and technical implementation'},
    {'name': 'art', 'color': 'fbca04', 'description': 'Visual art, graphics, and UI design'},
    {'name': 'audio', 'color': 'f9d0c4', 'description': 'Sound effects and music'},
    {'name': 'QA', 'color': 'ededed', 'description': 'Quality assurance, testing, and debugging'},
    {'name': 'documentation', 'color': '0075ca', 'description': 'Documentation and technical writing'},
    {'name': 'marketing', 'color': 'ff69b4', 'description': 'Marketing and promotion'},
    {'name': 'business', 'color': 'd4c5f9', 'description': 'Business operations and analytics'},
]


class UserStory:
    """Represents a user story to be created as a GitHub issue."""
    
    def __init__(self, story_id: str, title: str, description: str,
                 labels: List[str], acceptance_criteria: List[str], milestone: str = None):
        self.story_id = story_id
        self.title = f"{story_id}: {title}"
        self.description = description
        self.labels = labels if labels else []
        self.acceptance_criteria = acceptance_criteria if acceptance_criteria else []
        self.milestone = milestone
    
    def get_body(self) -> str:
        """Generate the issue body in markdown format."""
        body_parts = [self.description]
        
        if self.acceptance_criteria:
            body_parts.append("\n**Acceptance Criteria:**")
            for criterion in self.acceptance_criteria:
                body_parts.append(f"- {criterion}")
        
        return "\n".join(body_parts)


def validate_inputs(design_doc: str, owner: str, repo: str, token: str) -> bool:
    """Validate all required inputs."""
    errors = []
    
    # Check design doc exists
    if not os.path.exists(design_doc):
        errors.append(f"Design document not found: {design_doc}")
    
    # Check token
    if not token:
        errors.append("GitHub token not provided (use GITHUB_TOKEN env var or --token)")
    
    # Check owner and repo
    if not owner:
        errors.append("Repository owner not specified (use --owner)")
    if not repo:
        errors.append("Repository name not specified (use --repo)")
    
    if errors:
        print("❌ Validation Errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True


def parse_user_stories(markdown_file: str) -> List[UserStory]:
    """Parse user stories from the markdown file."""
    user_stories = []
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this is a user story line
        if line.startswith('- **US-'):
            match = re.match(r'- \*\*([A-Z]+-[A-Z]+-\d+)\*\*: (.+)', line)
            if match:
                story_id = match.group(1)
                title = match.group(2)
                
                # Extract category from story ID for milestone
                parts = story_id.split('-')
                category_code = parts[1] if len(parts) >= 2 else None
                
                # Map category code to milestone
                category_map = {
                    'PROG': 'programming',
                    'ART': 'art',
                    'AUDIO': 'audio',
                    'QA': 'QA',
                    'DOC': 'documentation',
                    'MKT': 'marketing',
                    'BUS': 'business',
                }
                milestone = category_map.get(category_code, 'programming')
                
                # Look ahead for labels and acceptance criteria
                labels = []
                acceptance_criteria = []
                description = title
                
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    if next_line.startswith('- Labels:'):
                        label_text = next_line.replace('- Labels:', '').strip()
                        label_text = label_text.replace('`', '')
                        parsed_labels = [l.strip() for l in label_text.split(',')]
                        labels = [l for l in parsed_labels if l]
                        j += 1
                    elif next_line.startswith('- Acceptance Criteria:'):
                        j += 1
                        while j < len(lines):
                            criteria_line = lines[j].strip()
                            if criteria_line.startswith('- ') and not criteria_line.startswith('- **US-'):
                                criterion = criteria_line.lstrip('- ').strip()
                                if criterion and not criterion.startswith('Labels:'):
                                    acceptance_criteria.append(criterion)
                                j += 1
                            else:
                                break
                        break
                    elif next_line.startswith('- **US-') or next_line == '':
                        break
                    else:
                        j += 1
                
                story = UserStory(
                    story_id=story_id,
                    title=title,
                    description=description,
                    labels=labels,
                    acceptance_criteria=acceptance_criteria,
                    milestone=milestone
                )
                user_stories.append(story)
                i = j
                continue
        
        i += 1
    
    return user_stories


def setup_labels(repo, dry_run: bool = False):
    """Create or update standard labels."""
    print("📋 Step 1: Setting up labels")
    print("-" * 65)
    
    if dry_run:
        print(f"  Would create/update {len(STANDARD_LABELS)} labels:")
        for label_def in STANDARD_LABELS:
            print(f"    - {label_def['name']}")
        print()
        return
    
    created = 0
    updated = 0
    
    for label_def in STANDARD_LABELS:
        try:
            try:
                label = repo.get_label(label_def['name'])
                label.edit(
                    name=label_def['name'],
                    color=label_def['color'],
                    description=label_def.get('description', '')
                )
                print(f"  ✓ Updated label: {label_def['name']}")
                updated += 1
            except GithubException as e:
                if e.status == 404:
                    repo.create_label(
                        name=label_def['name'],
                        color=label_def['color'],
                        description=label_def.get('description', '')
                    )
                    print(f"  ✓ Created label: {label_def['name']}")
                    created += 1
                else:
                    raise
        except Exception as e:
            print(f"  ✗ Failed to process label '{label_def['name']}': {str(e)}")
    
    print(f"\n  Labels: {created} created, {updated} updated\n")


def setup_milestones(repo, dry_run: bool = False):
    """Create milestones for each category."""
    print("🎯 Step 2: Setting up milestones")
    print("-" * 65)
    
    if dry_run:
        print(f"  Would create {len(MILESTONES)} milestones:")
        for milestone_def in MILESTONES:
            print(f"    - {milestone_def['title']}: {milestone_def['description']}")
        print()
        return {}
    
    created = 0
    existing = 0
    
    # Get existing milestones
    existing_milestones = {m.title: m for m in repo.get_milestones(state='all')}
    
    for milestone_def in MILESTONES:
        if milestone_def['title'] in existing_milestones:
            print(f"  ✓ Milestone exists: {milestone_def['title']}")
            existing += 1
        else:
            repo.create_milestone(
                title=milestone_def['title'],
                description=milestone_def['description']
            )
            print(f"  ✓ Created milestone: {milestone_def['title']}")
            created += 1
    
    print(f"\n  Milestones: {created} created, {existing} existing\n")
    
    # Return updated milestone map
    return {m.title: m for m in repo.get_milestones(state='all')}


def setup_project(repo, dry_run: bool = False):
    """Create or find project board."""
    print("📊 Step 3: Setting up project board")
    print("-" * 65)
    
    project_name = "Game Development Project Plan"
    
    if dry_run:
        print(f"  Would create project board: '{project_name}'")
        print(f"  Visibility would match repository (private/public)")
        print()
        return None
    
    # Note: GitHub's v3 API for projects is deprecated
    # Using v4 GraphQL API would be better but requires different setup
    # For now, we'll just inform the user
    print(f"  ℹ️  Project board should be created manually:")
    print(f"     1. Go to: https://github.com/{repo.owner.login}/{repo.name}/projects")
    print(f"     2. Create a new project named '{project_name}'")
    print(f"     3. Set visibility to match repository ({repo.private and 'private' or 'public'})")
    print(f"     4. Add columns for each milestone/category")
    print()
    
    return None


def create_issues(repo, user_stories: List[UserStory], milestone_map: Dict, dry_run: bool = False):
    """Create issues from user stories and assign to milestones."""
    print("📝 Step 4: Creating issues")
    print("-" * 65)
    
    successful = 0
    failed = 0
    
    for story in user_stories:
        try:
            if dry_run:
                print(f"  Would create: {story.title}")
                print(f"    Labels: {', '.join(story.labels)}")
                print(f"    Milestone: {story.milestone}")
                print(f"    Criteria: {len(story.acceptance_criteria)} items")
                successful += 1
            else:
                # Get milestone object
                milestone_obj = milestone_map.get(story.milestone)
                
                issue = repo.create_issue(
                    title=story.title,
                    body=story.get_body(),
                    labels=story.labels,
                    milestone=milestone_obj
                )
                print(f"  ✓ Created #{issue.number}: {story.title}")
                successful += 1
                
                # Rate limiting
                time.sleep(0.5)
        except Exception as e:
            print(f"  ✗ Failed: {story.title} - {str(e)}")
            failed += 1
    
    print(f"\n  Issues: {successful} created, {failed} failed\n")
    return successful, failed


def main():
    parser = argparse.ArgumentParser(
        description='Setup complete game development project with issues, milestones, and project board'
    )
    parser.add_argument(
        '--design-doc',
        required=True,
        help='Path to design document with user stories'
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
        help='Preview changes without creating anything'
    )
    
    args = parser.parse_args()
    
    # Get token
    token = args.token or os.environ.get('GITHUB_TOKEN')
    
    # Validate inputs
    print('🎮 Game Development Project Setup')
    print('=' * 65)
    print()
    
    if args.dry_run:
        print("⚠️  DRY RUN MODE - No changes will be made")
        print()
    
    print("Validating inputs...")
    if not validate_inputs(args.design_doc, args.owner, args.repo, token if not args.dry_run else "dry_run"):
        sys.exit(1)
    print("✓ All inputs valid\n")
    
    # Connect to GitHub
    if not args.dry_run:
        print(f"Connecting to GitHub repository: {args.owner}/{args.repo}")
        g = Github(token)
        try:
            repo = g.get_repo(f"{args.owner}/{args.repo}")
            print(f"✓ Connected to {repo.full_name}")
            print(f"  Repository is: {'private' if repo.private else 'public'}")
            print()
        except GithubException as e:
            print(f"❌ Error accessing repository: {e}")
            sys.exit(1)
    else:
        print(f"Would connect to: {args.owner}/{args.repo}\n")
        repo = None
    
    # Parse design document
    print(f"📄 Parsing design document: {args.design_doc}")
    user_stories = parse_user_stories(args.design_doc)
    
    if len(user_stories) == 0:
        print("❌ No user stories found in design document.")
        print("\nExpected format:")
        print("- **US-CAT-###**: As a user, I want... so that...")
        print("  - Labels: `label1`, `label2`")
        print("  - Acceptance Criteria:")
        print("    - Criterion 1")
        sys.exit(1)
    
    print(f"✓ Found {len(user_stories)} user stories")
    
    # Show summary by category
    categories = {}
    for story in user_stories:
        categories[story.milestone] = categories.get(story.milestone, 0) + 1
    
    print("\n  By category:")
    for category in sorted(categories.keys()):
        print(f"    - {category}: {categories[category]}")
    print()
    
    # Confirm if not dry run
    if not args.dry_run:
        response = input(f"Proceed with setup for {args.owner}/{args.repo}? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            sys.exit(0)
        print()
    
    # Execute setup steps
    if not args.dry_run:
        setup_labels(repo, dry_run=False)
        milestone_map = setup_milestones(repo, dry_run=False)
        setup_project(repo, dry_run=False)
        successful, failed = create_issues(repo, user_stories, milestone_map, dry_run=False)
    else:
        setup_labels(None, dry_run=True)
        setup_milestones(None, dry_run=True)
        setup_project(None, dry_run=True)
        successful, failed = create_issues(None, user_stories, {}, dry_run=True)
    
    # Print final summary
    print("=" * 65)
    print("✅ Setup Complete!" if not args.dry_run else "✅ Dry Run Complete!")
    print("=" * 65)
    print(f"  User stories processed: {successful}")
    print(f"  Failures: {failed}")
    print(f"  Total: {len(user_stories)}")
    
    if not args.dry_run:
        print(f"\nView your project:")
        print(f"  Issues: https://github.com/{args.owner}/{args.repo}/issues")
        print(f"  Milestones: https://github.com/{args.owner}/{args.repo}/milestones")
        print(f"  Projects: https://github.com/{args.owner}/{args.repo}/projects")
    else:
        print("\nThis was a dry run. Run without --dry-run to create for real.")
    
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
