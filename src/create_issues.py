"""
Create GitHub Issues
Creates issues on GitHub repository from generated issue list.
"""

import os
import sys
import time
import argparse
from typing import List, Dict
from github import Github, GithubException
from generate_issues import IssueGenerator


def create_github_issues(owner: str, repo: str, issues: List[Dict], token: str = None):
    """
    Create issues on GitHub repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
        issues: List of issue dictionaries with title, body, labels
        token: GitHub personal access token (or use GITHUB_TOKEN env var)
    """
    if not token:
        token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        raise ValueError(
            "GitHub token required. Set GITHUB_TOKEN environment variable or pass --token"
        )
    
    # Initialize GitHub API
    g = Github(token)
    repository = g.get_repo(f"{owner}/{repo}")
    
    created_issues = []
    failed_issues = []
    
    print(f"\n🚀 Creating issues on {owner}/{repo}...")
    print("=" * 50)
    
    for issue in issues:
        try:
            # Create the issue
            gh_issue = repository.create_issue(
                title=issue['title'],
                body=issue.get('body', ''),
                labels=issue.get('labels', [])
            )
            
            created_issues.append(gh_issue)
            print(f"✓ Created issue #{gh_issue.number}: {issue['title']}")
            
            # Rate limiting - wait 500ms between requests
            time.sleep(0.5)
            
        except GithubException as e:
            failed_issues.append({'issue': issue, 'error': str(e)})
            print(f"✗ Failed to create issue '{issue['title']}': {e.data.get('message', str(e))}")
        except Exception as e:
            failed_issues.append({'issue': issue, 'error': str(e)})
            print(f"✗ Failed to create issue '{issue['title']}': {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"✓ Created {len(created_issues)} issues")
    if failed_issues:
        print(f"✗ Failed to create {len(failed_issues)} issues")
    
    return created_issues, failed_issues


def main():
    parser = argparse.ArgumentParser(
        description='Create GitHub issues from game design document'
    )
    parser.add_argument(
        'design_doc',
        help='Path to the game design document'
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
    
    print('🎮 Game Dev Project Plan Creator')
    print('=================================\n')
    
    # Parse design doc and generate issues
    print(f"📄 Parsing design document: {args.design_doc}")
    generator = IssueGenerator()
    generator.set_design_doc(args.design_doc)
    print("✓ Design document parsed\n")
    
    print("🔨 Generating issues...")
    issues = generator.generate_issues()
    print(f"✓ Generated {len(issues)} issues\n")
    
    # Show report
    report = generator.generate_report(issues)
    print("📊 Project Plan Summary:")
    print(f"   Total Issues: {report['total_issues']}")
    print("\n   By Category:")
    for category, count in report['by_category'].items():
        print(f"   - {category}: {count}")
    print("\n   By Label:")
    for label, count in report['by_label'].items():
        print(f"   - {label}: {count}")
    
    # Create issues on GitHub
    created, failed = create_github_issues(
        args.owner,
        args.repo,
        issues,
        args.token
    )
    
    print("\n✅ Done!")
    
    if failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
