"""
Design Document Parser
Extracts features and requirements from game design documents.
"""

import re
from typing import Dict, List, Any


class DesignDocParser:
    """Parses game design documents to extract features and requirements."""
    
    def __init__(self, file_path: str):
        """Initialize parser with design document path."""
        self.file_path = file_path
        self.content = self._load_file()
        self.features = {}
        self.requirements = {}
    
    def _load_file(self) -> str:
        """Load the design document file."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def parse(self) -> Dict[str, Any]:
        """Parse the design document and return extracted data."""
        self.features = self.extract_features()
        self.requirements = self.extract_requirements()
        return {
            'features': self.features,
            'requirements': self.requirements,
            'raw_content': self.content
        }
    
    def extract_features(self) -> Dict[str, Any]:
        """Extract checked features from design doc."""
        features = {
            'must_have': [],
            'nice_to_have': [],
            'multiplayer': False,
            'ai': False,
            'audio': False,
            'graphics': None,
            'progression': []
        }
        
        # Extract must-have features
        must_have_match = re.search(
            r'### Must-Have Features.*?\n([\s\S]*?)(?=###|##|$)',
            self.content
        )
        if must_have_match:
            items = re.findall(r'- \[x\] (.+)', must_have_match.group(1))
            features['must_have'] = [item.strip() for item in items]
        
        # Extract nice-to-have features
        nice_to_have_match = re.search(
            r'### Nice-to-Have Features.*?\n([\s\S]*?)(?=###|##|$)',
            self.content
        )
        if nice_to_have_match:
            items = re.findall(r'- \[x\] (.+)', nice_to_have_match.group(1))
            features['nice_to_have'] = [item.strip() for item in items]
        
        # Check for multiplayer
        features['multiplayer'] = (
            '[x] Local multiplayer' in self.content or
            '[x] Online multiplayer' in self.content
        )
        
        # Check for AI requirements
        features['ai'] = (
            '[x] Enemy AI needed' in self.content or
            '[x] NPC AI needed' in self.content or
            '[x] Pathfinding required' in self.content
        )
        
        # Check for audio
        features['audio'] = (
            '[x] Background music' in self.content or
            '[x] Sound effects' in self.content or
            '[x] Voice acting' in self.content
        )
        
        # Extract progression systems
        progression_match = re.search(
            r'### Player Progression.*?\n([\s\S]*?)(?=###|##|$)',
            self.content
        )
        if progression_match:
            items = re.findall(r'- \[x\] (.+)', progression_match.group(1))
            features['progression'] = [item.strip() for item in items]
        
        return features
    
    def extract_requirements(self) -> Dict[str, str]:
        """Extract technical requirements from design doc."""
        requirements = {
            'engine': self._extract_field('Engine/Framework'),
            'language': self._extract_field('Programming Language'),
            'platform': self._extract_field('Target Platform'),
            'genre': self._extract_field('Genre')
        }
        return requirements
    
    def _extract_field(self, field_name: str) -> str:
        """Extract a specific field value from markdown content."""
        pattern = rf'### {re.escape(field_name)}\s*\n([^\n#]+)'
        match = re.search(pattern, self.content, re.IGNORECASE)
        if match:
            return match.group(1).replace('[', '').replace(']', '').strip()
        return None


if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python parse_design_doc.py <design-doc-path>")
        sys.exit(1)
    
    parser = DesignDocParser(sys.argv[1])
    data = parser.parse()
    
    print("Design Document Parsed Successfully")
    print("=" * 50)
    print(f"Features: {json.dumps(data['features'], indent=2)}")
    print(f"Requirements: {json.dumps(data['requirements'], indent=2)}")
