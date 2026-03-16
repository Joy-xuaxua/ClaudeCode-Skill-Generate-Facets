# Generate Facets - Quick Reference

Facets are session summaries required for generating Claude Code's `/insights` report. When running `/insights`, facets are typically generated automatically, and the report relies heavily on them to provide meaningful analysis. However, some users exprience that only several facets are generated while they have lots of sessions. This results in incomplete insights reports that only reflect a small fraction of your actual usage, leading to generic recommendations that echo what you already do rather than providing helpful, deep insights. This skill addresses this issue by systematically generating facets for all sessions, enabling truly comprehensive and insightful reports.

facets may not be consistently created for all sessions. when you have many sessions across various projects.

**Note:** This is a known issue affecting multiple users. See related reports:
- [#24039: insights: facets not generated, most report sections empty](https://github.com/anthropics/claude-code/issues/24039)
- [#28341: /insights: qualitative sections empty — facets generation silently fails](https://github.com/anthropics/claude-code/issues/28341)
- [#23273: /insights command only analyzes 3 sessions out of 2800+](https://github.com/anthropics/claude-code/issues/23273)
- [#23514: insights report only captures a fraction of sessions and projects](https://github.com/anthropics/claude-code/issues/23514)
- [#23361: /insights report samples only ~0.3% of sessions](https://github.com/anthropics/claude-code/issues/23361)

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
