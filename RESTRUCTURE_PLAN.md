# tinyTUIs Repository Restructuring Plan

## Overview
Transform the current minimal structure into a well-organized monorepo that supports multiple TUI projects and reusable patterns, while keeping it simple and focused.

## Current State
- [`README.md`](README.md) - Well-structured with clear vision
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - Basic guidelines (keeping as-is)
- [`.gitignore`](.gitignore) - Node.js focused, needs Python support
- [`experiments/`](experiments/) - Contains only `.keep` file
- [`site/`](site/) - Basic website structure

## Proposed Changes

### 1. Directory Restructuring
- **Rename** `/experiments/` → `/projects/`
  - Aligns with README.md references
  - Better reflects the purpose of TUI projects
  - Move `.keep` file to maintain directory

### 2. Create Patterns Directory
- **Add** `/patterns/` directory
- **Include** basic README.md explaining purpose:
  ```
  # Patterns
  Shared TUI utilities and reusable code patterns.
  
  This directory will contain:
  - Common keyboard handling utilities
  - Reusable UI components
  - Shared themes and styling
  - General TUI helper functions
  ```

### 3. Enhance .gitignore
**Add Python-specific entries:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

## Implementation Steps

1. **Rename directory**: `git mv experiments projects`
2. **Create patterns directory** with README.md
3. **Update .gitignore** with Python entries
4. **Commit changes** with clear messages

## Final Structure
```
tinytuis/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore (enhanced)
├── projects/
│   └── .keep (temporary)
├── patterns/
│   └── README.md
└── site/
    └── index.html
```

## Success Criteria
- ✅ Directory names align with README references
- ✅ Python development files properly ignored
- ✅ Clear structure for future TUI projects
- ✅ Framework established for pattern extraction
- ✅ Maintains project simplicity and focus

## Next Phase
After structural foundation is complete, validate with a concrete TUI project (e.g., todo-list) to ensure the organization works as intended.