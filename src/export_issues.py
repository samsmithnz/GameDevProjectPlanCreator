"""
Export Issues
Export generated issues to JSON or Markdown format.
"""

import json
import argparse
from datetime import datetime
from typing import List, Dict
from generate_issues import IssueGenerator


def export_to_json(issues: List[Dict], output_path: str):
    """Export issues to JSON file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(issues, f, indent=2)
        print(f"Exported {len(issues)} issues to {output_path}")
    except Exception as e:
        raise Exception(f"Failed to export to JSON: {str(e)}")


def export_to_markdown(issues: List[Dict], output_path: str, templates: Dict):
    """Export issues to Markdown file."""
    try:
        markdown = '# Game Development Project Plan\n\n'
        markdown += f"Generated on: {datetime.now().isoformat()}Z\n\n"
        markdown += f"Total Issues: {len(issues)}\n\n"
        markdown += '---\n\n'
        
        # Group by category
        categorized_issues = {}
        for issue in issues:
            # Find which category this issue belongs to
            category_name = 'Other'
            for category_key, category in templates['categories'].items():
                if any(t['title'] == issue['title'] for t in category['templates']):
                    category_name = category['name']
                    break
            
            if category_name not in categorized_issues:
                categorized_issues[category_name] = []
            categorized_issues[category_name].append(issue)
        
        # Write categorized issues
        for category_name, category_issues in categorized_issues.items():
            markdown += f"## {category_name}\n\n"
            for issue in category_issues:
                markdown += f"### {issue['title']}\n\n"
                markdown += f"{issue.get('body', '')}\n\n"
                if issue.get('labels'):
                    markdown += f"**Labels:** {', '.join(issue['labels'])}\n\n"
                markdown += '---\n\n'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"Exported {len(issues)} issues to {output_path}")
    except Exception as e:
        raise Exception(f"Failed to export to Markdown: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description='Export game development issues to JSON or Markdown'
    )
    parser.add_argument(
        'design_doc',
        help='Path to the game design document'
    )
    parser.add_argument(
        '--json',
        metavar='PATH',
        help='Export to JSON file'
    )
    parser.add_argument(
        '--markdown',
        metavar='PATH',
        help='Export to Markdown file'
    )
    
    args = parser.parse_args()
    
    if not args.json and not args.markdown:
        print("Error: At least one export format required (--json or --markdown)")
        parser.print_help()
        return 1
    
    print('🎮 Game Dev Project Plan Creator - Exporter')
    print('============================================\n')
    
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
    print()
    
    # Export to JSON
    if args.json:
        export_to_json(issues, args.json)
        print()
    
    # Export to Markdown
    if args.markdown:
        export_to_markdown(issues, args.markdown, generator.templates)
        print()
    
    print("✅ Done!")


if __name__ == '__main__':
    main()
