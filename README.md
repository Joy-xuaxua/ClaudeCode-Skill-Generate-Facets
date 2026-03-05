# Generate Facets - Quick Reference

## Three Ways to Use

### 1. Skill Command (Recommended)
```bash
/generate-facets
```
This invokes the skill directly in Claude Code.

### 2. Python Script
```bash
python ~/.claude/skills/generate-facets/impl.py
```

### 3. Batch File (Windows)
```bash
~/.claude/skills/generate-facets/run.bat
```
Double-click or run from terminal.

## What Happens

1. Checks `~/.claude/usage-data/session-meta/` for new files
2. Skips files that already have facets
3. Analyzes each session for:
   - Goals and outcome
   - Friction points
   - Session type
   - Success indicators
4. Saves to `~/.claude/usage-data/facets/`

## After Running

```bash
/insights
```

View updated report with full analysis.

## File Locations

```
~/.claude/skills/generate-facets/
├── SKILL.md          # Skill definition
├── impl.py           # Python implementation
├── run.bat           # Windows batch launcher
└── README.md         # This file
```

## Customization

Edit `impl.py` to adjust:
- Session type detection rules
- Goal category mapping
- Friction detection thresholds
- Summary generation
