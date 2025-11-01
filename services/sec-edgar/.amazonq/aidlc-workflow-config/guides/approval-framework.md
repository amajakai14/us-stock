# AI-DLC Approval Framework

## Approval Patterns

**Planning**: "I recommend [approach] because [reasoning]. Should I proceed?"  
**Execution**: "The [deliverable] covers [scope]. Ready to proceed to [next phase]?"  
**Phase Transition**: "Completed [phase] with [artifacts]. Ready for [next phase]?"

## Approval Requirements

- **Always wait for explicit approval**: "yes", "proceed", "approved", or "1"
- **Never assume approval**: Even if user seems ready, ask explicitly
- **Provide context**: Always explain what you're asking approval for
- **Be specific**: State exactly what will happen after approval
- **STOP after plan creation**: Never execute plans without approval
- **Ask clearly**: "Should I proceed with this plan?" or "Ready to execute?"

## User Response Patterns

| User Says | Meaning | Action |
|-----------|---------|--------|
| "yes", "proceed", "approved" | Full approval | Continue with planned action |
| "1", "A", "B", "C" | Option selection | Use selected option and proceed |
| "yes but..." | Conditional approval | Address condition first |
| "no", "wait", "stop" | Rejection | Stop and clarify |
| Questions or concerns | Need clarification | Answer questions before proceeding |

## Approval Checkpoints

1. **After creating decision file** - Get decisions resolved
2. **After creating plan file** - Get plan approved  
3. **Before phase transition** - Get deliverables approved
4. **When user provides new requirements** - Confirm understanding
5. **When deviating from plan** - Get approval for changes
