"""
Add Labels to Repository
Creates or updates labels on a GitHub repository.
"""

import os
import sys
import argparse
from typing import List, Dict
from github import Github, GithubException


# Standard label definitions for game development
STANDARD_LABELS = [
    {'name': 'enhancement', 'color': 'a2eeef', 'description': 'New feature or request'},
    {'name': 'bug', 'color': 'd73a4a', 'description': 'Something isn\'t working'},
    {'name': 'documentation', 'color': '0075ca', 'description': 'Improvements or additions to documentation'},
    {'name': 'core', 'color': 'e99695', 'description': 'Core game mechanics'},
    {'name': 'ai', 'color': 'fbca04', 'description': 'AI and NPC systems'},
    {'name': 'ui', 'color': 'bfdadc', 'description': 'User interface'},
    {'name': 'audio', 'color': 'f9d0c4', 'description': 'Sound and music'},
    {'name': 'graphics', 'color': 'c5def5', 'description': 'Graphics and rendering'},
    {'name': 'level-design', 'color': 'd4c5f9', 'description': 'Level and map design'},
    {'name': 'progression', 'color': 'fef2c0', 'description': 'Player progression systems'},
    {'name': 'multiplayer', 'color': 'c2e0c6', 'description': 'Multiplayer features'},
    {'name': 'testing', 'color': 'ededed', 'description': 'Testing and QA'},
    {'name': 'optimization', 'color': 'ff7619', 'description': 'Performance optimization'},
    {'name': 'polish', 'color': 'ffa94d', 'description': 'Polish and refinement'},
    {'name': 'analytics', 'color': '006b75', 'description': 'Analytics and metrics'},
    {'name': 'marketing', 'color': 'ff69b4', 'description': 'Marketing and promotion'},
]


def add_labels_to_repo(owner: str, repo: str, labels: List[Dict] = None, token: str = None):
    """
    Add or update labels on a GitHub repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        labels: List of label dicts with name, color, description
        token: GitHub personal access token
    """
    if not token:
        token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        raise ValueError(
            "GitHub token required. Set GITHUB_TOKEN environment variable or pass --token"
        )
    
    if labels is None:
        labels = STANDARD_LABELS
    
    # Initialize GitHub API
    g = Github(token)
    repository = g.get_repo(f"{owner}/{repo}")
    
    print(f"\n🏷️  Adding labels to {owner}/{repo}...")
    print("=" * 50)
    
    created = 0
    updated = 0
    failed = 0
    
    for label_def in labels:
        try:
            # Try to get existing label
            try:
                label = repository.get_label(label_def['name'])
                # Update if it exists
                label.edit(
                    name=label_def['name'],
                    color=label_def['color'],
                    description=label_def.get('description', '')
                )
                print(f"✓ Updated label: {label_def['name']}")
                updated += 1
            except GithubException as e:
                if e.status == 404:
                    # Create if it doesn't exist
                    repository.create_label(
                        name=label_def['name'],
                        color=label_def['color'],
                        description=label_def.get('description', '')
                    )
                    print(f"✓ Created label: {label_def['name']}")
                    created += 1
                else:
                    raise
        except Exception as e:
            print(f"✗ Failed to process label '{label_def['name']}': {str(e)}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"✓ Created {created} labels")
    print(f"✓ Updated {updated} labels")
    if failed:
        print(f"✗ Failed to process {failed} labels")
    
    return created, updated, failed


def main():
    parser = argparse.ArgumentParser(
        description='Add standard game development labels to GitHub repository'
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
    
    args = parser.parse_args()
    
    print('🎮 Game Dev Project Plan Creator - Label Manager')
    print('=================================================\n')
    
    created, updated, failed = add_labels_to_repo(
        args.owner,
        args.repo,
        token=args.token
    )
    
    print("\n✅ Done!")
    
    if failed > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
