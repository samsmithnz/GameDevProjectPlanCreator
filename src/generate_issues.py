"""
Issue Generator
Generates GitHub issues based on design document and templates.
"""

import json
import os
from typing import List, Dict, Any
from parse_design_doc import DesignDocParser


class IssueGenerator:
    """Generates issues from templates based on design document features."""
    
    def __init__(self, templates_path: str = None):
        """Initialize with path to templates file."""
        if templates_path is None:
            templates_path = os.path.join(
                os.path.dirname(__file__),
                '../templates/issue-templates.json'
            )
        self.templates = self._load_templates(templates_path)
        self.design_data = None
    
    def _load_templates(self, path: str) -> Dict:
        """Load issue templates from JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def set_design_doc(self, design_doc_path: str):
        """Parse and set the design document."""
        parser = DesignDocParser(design_doc_path)
        self.design_data = parser.parse()
    
    def generate_issues(self) -> List[Dict[str, Any]]:
        """Generate issues based on design doc and templates."""
        if not self.design_data:
            raise ValueError("No design document set. Call set_design_doc() first.")
        
        issues = []
        features = self.design_data['features']
        
        # Always include programming - core mechanics are fundamental
        issues.extend(self.templates['categories']['programming']['templates'])
        
        # Always add art - UI/UX and graphics are essential
        issues.extend(self.templates['categories']['art']['templates'])
        
        # Add audio if needed
        if features.get('audio'):
            issues.extend(self.templates['categories']['audio']['templates'])
        
        # Always add QA - testing is essential
        issues.extend(self.templates['categories']['qa']['templates'])
        
        # Always add documentation
        issues.extend(self.templates['categories']['documentation']['templates'])
        
        # Always add marketing - launch preparation is important
        issues.extend(self.templates['categories']['marketing']['templates'])
        
        # Always add business - project management is essential
        issues.extend(self.templates['categories']['business']['templates'])
        
        return issues
    
    def generate_report(self, issues: List[Dict]) -> Dict[str, Any]:
        """Generate a summary report of the project plan."""
        report = {
            'total_issues': len(issues),
            'by_category': {},
            'by_label': {}
        }
        
        # Count by category
        for category_key, category in self.templates['categories'].items():
            category_issues = [
                issue for issue in issues
                if any(t['title'] == issue['title'] for t in category['templates'])
            ]
            if category_issues:
                report['by_category'][category['name']] = len(category_issues)
        
        # Count by label
        for issue in issues:
            if 'labels' in issue:
                for label in issue['labels']:
                    report['by_label'][label] = report['by_label'].get(label, 0) + 1
        
        return report


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generate_issues.py <design-doc-path>")
        sys.exit(1)
    
    generator = IssueGenerator()
    generator.set_design_doc(sys.argv[1])
    issues = generator.generate_issues()
    report = generator.generate_report(issues)
    
    print(f"\nGenerated {len(issues)} issues")
    print("\nBy Category:")
    for category, count in report['by_category'].items():
        print(f"  - {category}: {count}")
    print("\nBy Label:")
    for label, count in report['by_label'].items():
        print(f"  - {label}: {count}")
