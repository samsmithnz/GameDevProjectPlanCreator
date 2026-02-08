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
    python setup_game_project.py --owner <owner> --repo <repo>
    
    # With custom templates file
    python setup_game_project.py --templates my-templates.json --owner <owner> --repo <repo>
    
    # Dry run to preview
    python setup_game_project.py --owner <owner> --repo <repo> --dry-run
"""

import os
import sys
import argparse
import time
import re
import json
import requests
from typing import List, Dict, Tuple, Optional
from github import Github, GithubException


# 7 milestone categories for game development
MILESTONES = [
    {'title': 'Programming', 'description': 'Programming and technical implementation'},
    {'title': 'Art', 'description': 'Visual art, graphics, and UI design'},
    {'title': 'Audio', 'description': 'Sound effects and music systems'},
    {'title': 'QA', 'description': 'Quality assurance, testing, and debugging'},
    {'title': 'Documentation', 'description': 'Documentation and technical writing'},
    {'title': 'Marketing', 'description': 'Marketing and promotional activities'},
    {'title': 'Business', 'description': 'Business operations and analytics'},
]

# Kanban workflow columns for the project board (Projects V2)
PROJECT_COLUMNS = [
    {'name': 'Backlog', 'description': "This work hasn't been started", 'color': 'BLUE'},
    {'name': 'On deck', 'description': 'This work is prioritized and ready to be worked on next', 'color': 'YELLOW', 'limit': 5},
    {'name': 'In progress', 'description': 'This work is actively being worked on', 'color': 'GREEN', 'limit': 3},
    {'name': 'Blocked', 'description': 'This work is blocked and cannot finish', 'color': 'RED', 'limit': 5},
    {'name': 'In review', 'description': 'This work is done, and ready for review/QA', 'color': 'PINK', 'limit': 5},
    {'name': 'Done', 'description': 'This work has been completed', 'color': 'PURPLE'},
]

# Standard labels aligned with milestones
STANDARD_LABELS = [
    {'name': 'enhancement', 'color': 'a2eeef', 'description': 'New feature or request'},
    {'name': 'bug', 'color': 'd73a4a', 'description': 'Something isn\'t working'},
    {'name': 'Programming', 'color': '0e8a16', 'description': 'Programming and technical implementation'},
    {'name': 'Art', 'color': 'fbca04', 'description': 'Visual art, graphics, and UI design'},
    {'name': 'Audio', 'color': 'f9d0c4', 'description': 'Sound effects and music'},
    {'name': 'QA', 'color': 'ededed', 'description': 'Quality assurance, testing, and debugging'},
    {'name': 'Documentation', 'color': '0075ca', 'description': 'Documentation and technical writing'},
    {'name': 'Marketing', 'color': 'ff69b4', 'description': 'Marketing and promotion'},
    {'name': 'Business', 'color': 'd4c5f9', 'description': 'Business operations and analytics'},
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


def validate_inputs(templates_file: str, owner: str, repo: str, token: str) -> bool:
    """Validate all required inputs."""
    errors = []
    
    # Check templates file exists
    if not os.path.exists(templates_file):
        errors.append(f"Templates file not found: {templates_file}")
    
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


def load_issue_templates(json_file: str) -> List[UserStory]:
    """Load issue templates from JSON file.
    
    Expected format:
    {
      "categories": {
        "programming": {
          "name": "programming",
          "description": "...",
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
    """
    issues = []
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Generate user story ID counter for each category
    category_counters = {}
    
    # Process each category
    for category_key, category_data in data.get('categories', {}).items():
        category_name = category_data.get('name', category_key)
        templates = category_data.get('templates', [])
        
        # Initialize counter for this category
        if category_name not in category_counters:
            category_counters[category_name] = 1
        
        # Map category name to code for story IDs (case-insensitive)
        category_code_map = {
            'programming': 'PROG',
            'art': 'ART',
            'audio': 'AUDIO',
            'qa': 'QA',
            'documentation': 'DOC',
            'marketing': 'MKT',
            'business': 'BUS',
        }
        category_code = category_code_map.get(category_name.lower(), 'PROG')
        
        # Create UserStory object for each template
        for template in templates:
            story_num = category_counters[category_name]
            story_id = f"US-{category_code}-{story_num:03d}"
            
            title = template.get('title', 'Untitled')
            body = template.get('body', '')
            labels = template.get('labels', [])
            
            # Extract acceptance criteria if present in body (after "Acceptance Criteria:" header)
            acceptance_criteria = []
            description = body
            if 'Acceptance Criteria:' in body:
                parts = body.split('Acceptance Criteria:')
                description = parts[0].strip()
                criteria_text = parts[1].strip()
                # Parse bullet points - first strip, check if starts with -, then remove the -
                for line in criteria_text.split('\n'):
                    line_stripped = line.strip()
                    if line_stripped.startswith('-'):
                        criterion = line_stripped.lstrip('- ').strip()
                        if criterion:
                            acceptance_criteria.append(criterion)
            
            story = UserStory(
                story_id=story_id,
                title=title,
                description=description,
                labels=labels,
                acceptance_criteria=acceptance_criteria,
                milestone=category_name
            )
            issues.append(story)
            
            category_counters[category_name] += 1
    
    return issues


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


def run_graphql_query(token: str, query: str, variables: Dict = None) -> Dict:
    """Execute a GraphQL query against GitHub API."""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    
    response = requests.post(
        'https://api.github.com/graphql',
        headers=headers,
        json=payload
    )
    
    if response.status_code != 200:
        raise Exception(f"GraphQL query failed: {response.status_code} - {response.text}")
    
    result = response.json()
    if 'errors' in result:
        raise Exception(f"GraphQL errors: {json.dumps(result['errors'], indent=2)}")
    
    return result['data']


def setup_project_v2(repo, token: str, owner: str, repo_name: str, dry_run: bool = False):
    """Create or find ProjectV2 board with Kanban workflow columns using GraphQL."""
    print("📊 Step 3: Setting up project board (Projects V2)")
    print("-" * 65)
    
    project_name = f"{repo_name} Project Plan"
    
    if dry_run:
        print(f"  Would create ProjectV2 board: '{project_name}'")
        print(f"  Would use GitHub's default Status field (Todo, In Progress, Done)")
        print()
        return None, None, None
    
    # Get repository node ID and visibility
    query_repo_id = """
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        id
        isPrivate
        owner {
          ... on Organization {
            id
          }
          ... on User {
            id
          }
        }
      }
    }
    """
    
    repo_data = run_graphql_query(token, query_repo_id, {
        'owner': owner,
        'repo': repo_name
    })
    
    repo_id = repo_data['repository']['id']
    owner_id = repo_data['repository']['owner']['id']
    repo_is_private = repo_data['repository']['isPrivate']
    repo_visibility = "private" if repo_is_private else "public"
    
    # Check if project already exists at owner level
    # Create the project (skip checking for existing projects to avoid permission issues)
    # If a project with the same name exists, GitHub will return an error
    project_id = None
    project_number = None
    
    try:
        mutation_create_project = """
        mutation($ownerId: ID!, $title: String!) {
          createProjectV2(input: {ownerId: $ownerId, title: $title}) {
            projectV2 {
              id
              title
              number
            }
          }
        }
        """
        
        create_result = run_graphql_query(token, mutation_create_project, {
            'ownerId': owner_id,
            'title': project_name
        })
        
        project_id = create_result['createProjectV2']['projectV2']['id']
        project_number = create_result['createProjectV2']['projectV2']['number']
        print(f"  ✓ Created ProjectV2: '{project_name}' (#{project_number})")
        
        # Link project to repository
        mutation_link = """
        mutation($projectId: ID!, $repositoryId: ID!) {
          linkProjectV2ToRepository(input: {projectId: $projectId, repositoryId: $repositoryId}) {
            repository {
              id
            }
          }
        }
        """
        
        run_graphql_query(token, mutation_link, {
            'projectId': project_id,
            'repositoryId': repo_id
        })
        print(f"  ✓ Linked project to repository")
        
        # Set project visibility to match repository
        mutation_set_visibility = """
        mutation($projectId: ID!, $isPublic: Boolean!) {
          updateProjectV2(input: {projectId: $projectId, public: $isPublic}) {
            projectV2 {
              id
              public
            }
          }
        }
        """
        
        run_graphql_query(token, mutation_set_visibility, {
            'projectId': project_id,
            'isPublic': not repo_is_private
        })
        print(f"  ✓ Set project visibility to {repo_visibility} (matching repository)")
        
    except Exception as e:
        # If project creation fails, continue with other setup steps
        # Projects can be created manually in GitHub UI if needed
        error_msg = str(e)
        print(f"  ! Warning: Could not create project: {error_msg}")
        print(f"  ! This may be due to:")
        print(f"     - Project with this name already exists")
        print(f"     - Insufficient token permissions (need 'project' scope)")
        print(f"  ! Continuing with labels, milestones, and issues setup...")
    
    # Get existing fields (we need the Status field)
    if project_id:
        query_fields = """
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              fields(first: 20) {
                nodes {
                  ... on ProjectV2SingleSelectField {
                    id
                    name
                    options {
                      id
                      name
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        fields_data = run_graphql_query(token, query_fields, {'projectId': project_id})
        
        # Locate the Status field that GitHub creates by default
        status_field_id = None
        available_options = {}
        
        # Search through fields to find Status
        for field in fields_data['node']['fields']['nodes']:
            if field and field.get('name') == 'Status':
                status_field_id = field['id']
                for opt in field.get('options', []):
                    available_options[opt['name']] = opt['id']
                break
        
        # Map options for use
        option_map = available_options
        
        # Display what was found
        if status_field_id:
            opts_list = list(available_options.keys())
            print(f"  ✓ Found Status field with options: {', '.join(opts_list)}")
            # Warn if Todo option is not available
            if 'Todo' not in available_options:
                print(f"  ⚠️  Warning: 'Todo' status option not found - issues may not be assigned a default status")
        else:
            print(f"  ⚠️  Warning: Status field not found - ensure project was created with default fields enabled")
        
        if not dry_run:
            print(f"  ⚠️  Manual steps: Rename 'View 1', set Board layout, configure swimlanes")
            print()
        else:
            print()
        
        return project_id, status_field_id, option_map
    else:
        # Project creation failed, return None
        print(f"  ! Project board setup skipped")
        print()
        return None, None, {}


def setup_project(repo, milestone_map: Dict, dry_run: bool = False):
    """Create or find project board with Kanban workflow columns."""
    # This function is now deprecated in favor of setup_project_v2
    # Keeping for backwards compatibility
    print("📊 Step 3: Setting up project board")
    print("-" * 65)
    
    project_name = "Game Development Project Plan"
    
    if dry_run:
        print(f"  Would create project board: '{project_name}'")
        print(f"  Visibility would match repository ({'private' if hasattr(repo, 'private') and repo.private else 'public'})")
        print(f"  Would create {len(PROJECT_COLUMNS)} workflow columns:")
        for col_def in PROJECT_COLUMNS:
            print(f"    - {col_def['name']}: {col_def['description']}")
        print()
        return None
    
    # Check if project already exists
    existing_projects = list(repo.get_projects(state='open'))
    project = None
    
    for proj in existing_projects:
        if proj.name == project_name:
            project = proj
            print(f"  ✓ Project already exists: '{project_name}'")
            break
    
    # Create project if it doesn't exist
    if not project:
        project = repo.create_project(
            name=project_name,
            body="Kanban board for game development tasks with workflow stages"
        )
        print(f"  ✓ Created project: '{project_name}'")
    
    # Get existing columns
    existing_columns = {col.name: col for col in project.get_columns()}
    
    # Create workflow columns (in order)
    created_cols = 0
    for col_def in PROJECT_COLUMNS:
        col_name = col_def['name']
        if col_name not in existing_columns:
            # Note: GitHub API doesn't support setting column colors or WIP limits via REST API
            # These need to be set manually in the GitHub UI after creation
            project.create_column(name=col_name)
            print(f"  ✓ Created column: {col_name}")
            created_cols += 1
        else:
            print(f"  ✓ Column exists: {col_name}")
    
    if created_cols > 0:
        print(f"\n  Created {created_cols} new workflow columns")
        print(f"  ⚠️  Note: Column colors and WIP limits must be set manually in GitHub UI:")
        print(f"     - Backlog (blue, no max)")
        print(f"     - On deck (yellow, max 5)")
        print(f"     - In progress (green, max 3)")
        print(f"     - Blocked (red, max 5)")
        print(f"     - In review (pink, max 5)")
        print(f"     - Done (purple, no max)\n")
    else:
        print()
    
    return project



def create_issues_v2(repo, user_stories: List[UserStory], milestone_map: Dict, project_id: str, field_id: str, status_options: Dict, token: str, dry_run: bool = False):
    """Create issues, assign to milestones, add to ProjectV2, set to Todo status."""
    print("📝 Step 4: Creating issues and adding to project")
    print("-" * 65)
    
    successful = 0
    failed = 0
    
    # Get Todo option ID from GitHub's default status options
    default_status_id = status_options.get('Todo') if status_options else None
    
    # Warn if Todo status is not available
    if project_id and not default_status_id and not dry_run:
        print(f"  ⚠️  Warning: 'Todo' status not found in project field options")
        print(f"  ⚠️  Issues will be added to project without initial status set")
        available = list(status_options.keys()) if status_options else []
        if available:
            print(f"  ⚠️  Available options: {', '.join(available)}")
    
    for story in user_stories:
        try:
            if dry_run:
                print(f"  Would create: {story.title}")
                print(f"    Labels: {', '.join(story.labels)}")
                print(f"    Milestone: {story.milestone}")
                print(f"    Project status: Todo")
                print(f"    Criteria: {len(story.acceptance_criteria)} items")
                successful += 1
            else:
                # Get milestone object
                milestone_obj = milestone_map.get(story.milestone)
                
                # Create the issue using REST API
                issue = repo.create_issue(
                    title=story.title,
                    body=story.get_body(),
                    labels=story.labels,
                    milestone=milestone_obj
                )
                print(f"  ✓ Created #{issue.number}: {story.title}")
                
                # Add issue to ProjectV2 using GraphQL
                if project_id and default_status_id:
                    # Get issue node ID
                    query_issue_id = """
                    query($owner: String!, $repo: String!, $number: Int!) {
                      repository(owner: $owner, name: $repo) {
                        issue(number: $number) {
                          id
                        }
                      }
                    }
                    """
                    
                    issue_data = run_graphql_query(token, query_issue_id, {
                        'owner': repo.owner.login,
                        'repo': repo.name,
                        'number': issue.number
                    })
                    
                    issue_node_id = issue_data['repository']['issue']['id']
                    
                    # Add item to project
                    mutation_add_item = """
                    mutation($projectId: ID!, $contentId: ID!) {
                      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
                        item {
                          id
                        }
                      }
                    }
                    """
                    
                    add_result = run_graphql_query(token, mutation_add_item, {
                        'projectId': project_id,
                        'contentId': issue_node_id
                    })
                    
                    newly_added_item_id = add_result['addProjectV2ItemById']['item']['id']
                    
                    # Set the Status field value to Todo for the newly added item
                    if default_status_id and field_id:
                        status_update_mutation = """
                        mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
                          updateProjectV2ItemFieldValue(input: {
                            projectId: $projectId,
                            itemId: $itemId,
                            fieldId: $fieldId,
                            value: {singleSelectOptionId: $optionId}
                          }) {
                            projectV2Item {
                              id
                            }
                          }
                        }
                        """
                        
                        run_graphql_query(token, status_update_mutation, {
                            'projectId': project_id,
                            'itemId': newly_added_item_id,
                            'fieldId': field_id,
                            'optionId': default_status_id
                        })
                        print(f"    → Added to project with Todo status")
                    else:
                        print(f"    → Added to project")
                
                successful += 1
                
                # Rate limiting
                time.sleep(0.5)
        except Exception as e:
            print(f"  ✗ Failed: {story.title} - {str(e)}")
            failed += 1
    
    print(f"\n  Issues: {successful} created, {failed} failed")
    if project_id and not dry_run:
        print(f"  All issues added to ProjectV2 with Todo status\n")
    else:
        print()
    return successful, failed


def create_issues(repo, user_stories: List[UserStory], milestone_map: Dict, project, dry_run: bool = False):
    """Create issues from user stories, assign to milestones, and add to project Backlog."""
    print("📝 Step 4: Creating issues and adding to project")
    print("-" * 65)
    
    successful = 0
    failed = 0
    
    # Get project columns if project exists - find the Backlog column
    backlog_column = None
    if project and not dry_run:
        columns = list(project.get_columns())
        for col in columns:
            if col.name == 'Backlog':
                backlog_column = col
                break
    
    for story in user_stories:
        try:
            if dry_run:
                print(f"  Would create: {story.title}")
                print(f"    Labels: {', '.join(story.labels)}")
                print(f"    Milestone: {story.milestone}")
                print(f"    Project column: Backlog")
                print(f"    Criteria: {len(story.acceptance_criteria)} items")
                successful += 1
            else:
                # Get milestone object
                milestone_obj = milestone_map.get(story.milestone)
                
                # Create the issue
                issue = repo.create_issue(
                    title=story.title,
                    body=story.get_body(),
                    labels=story.labels,
                    milestone=milestone_obj
                )
                print(f"  ✓ Created #{issue.number}: {story.title}")
                
                # Add issue to project board Backlog column
                if backlog_column:
                    backlog_column.create_card(content_id=issue.id, content_type="Issue")
                    print(f"    → Added to Backlog")
                
                successful += 1
                
                # Rate limiting
                time.sleep(0.5)
        except Exception as e:
            print(f"  ✗ Failed: {story.title} - {str(e)}")
            failed += 1
    
    print(f"\n  Issues: {successful} created, {failed} failed")
    if backlog_column and not dry_run:
        print(f"  All issues added to Backlog column\n")
    else:
        print()
    return successful, failed


def main():
    parser = argparse.ArgumentParser(
        description='Setup complete game development project with issues, milestones, and project board'
    )
    parser.add_argument(
        '--templates',
        default='templates/issue-templates.json',
        help='Path to issue templates JSON file (default: templates/issue-templates.json)'
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
    if not validate_inputs(args.templates, args.owner, args.repo, token if not args.dry_run else "dry_run"):
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
    
    # Load issue templates from JSON
    print(f"📄 Loading issue templates from: {args.templates}")
    user_stories = load_issue_templates(args.templates)
    
    if len(user_stories) == 0:
        print("❌ No issue templates found in JSON file.")
        print("\nExpected format:")
        print('{')
        print('  "categories": {')
        print('    "programming": {')
        print('      "templates": [{"title": "...", "body": "...", "labels": [...]}]')
        print('    }')
        print('  }')
        print('}')
        sys.exit(1)
    
    print(f"✓ Loaded {len(user_stories)} issue templates")
    
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
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            sys.exit(0)
        print()
    
    # Execute setup steps
    if not args.dry_run:
        setup_labels(repo, dry_run=False)
        milestone_map = setup_milestones(repo, dry_run=False)
        proj_id, stat_field_id, stat_opts = setup_project_v2(repo, token, args.owner, args.repo, dry_run=False)
        successful, failed = create_issues_v2(repo, user_stories, milestone_map, proj_id, stat_field_id, stat_opts, token, dry_run=False)
    else:
        setup_labels(None, dry_run=True)
        milestone_map = setup_milestones(None, dry_run=True)
        proj_id, stat_field_id, stat_opts = setup_project_v2(None, None, args.owner, args.repo, dry_run=True)
        successful, failed = create_issues_v2(None, user_stories, {}, None, None, None, None, dry_run=True)
    
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
