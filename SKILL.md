# Generate Facets from Session-Meta

Generate analysis facets from Claude Code session-meta files.

## Usage

```bash
/generate-facets
```

## What This Does

1. **Counts** session-meta files vs existing facets
2. **Reads** session-meta files in batches
3. **Analyzes** each session to extract:
   - `underlying_goal`: The user's core objective
   - `goal_categories`: Type of work (development/troubleshooting/learning/etc)
   - `outcome`: Session result (achieved/mostly_achieved/interrupted/etc)
   - `user_satisfaction_counts`: Satisfaction levels
   - `claude_helpfulness`: How helpful Claude was
   - `session_type`: Category (debugging/refactoring/learning/etc)
   - `friction_counts`: Tool errors by type
   - `friction_detail`: Description of issues
   - `primary_success`: What was accomplished
   - `brief_summary`: Session description
4. **Writes** facet JSON files to `~/.claude/usage-data/facets/`

## Output

- Facets saved to: `C:\Users\zliu71\.claude\usage-data\facets\`
- Progress updates shown during processing
- Final summary with statistics

## After Running

Run `/insights` to see updated report with full analysis.
