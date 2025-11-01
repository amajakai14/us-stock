# Resume AI-DLC Command

When user says **"resume AI-DLC"** or requests specific phase entry, follow this process:

## 1. Auto-Detection Phase
- **Scan for iterations**: Check `.aidlc/iterations/` for existing iterations
- **Find latest iteration**: Identify most recent `iteration-{N}-{feature}/` folder
- **Read audit.md**: Extract current state information from "Current State" section
- **Detect entry point**: Determine if resuming or starting from specific phase

## 2. Context Restoration
- **Current Phase**: Report where user left off (e.g., "2.2 Logical Design")
- **Current Step**: Specific step within phase (e.g., "Awaiting user approval on plan")
- **Last Activity**: When work was last done
- **Progress Summary**: Brief overview of what's been completed
- **Available Contexts**: List bounded contexts and their completion status

## 3. State Analysis
- **Check plan files**: Scan for status indicators (🔄 🚀 ⏸️ ✅ ❌)
- **Check decision files**: Review resolved and outstanding decisions
- **Review deliverables**: Check outputs/inception/ and outputs/construction/ folder outputs
- **Identify blockers**: Look for outstanding questions or issues
- **Review decisions**: Summarize key decisions made so far
- **Assess completeness**: What's done vs what's remaining
- **Validate prerequisites**: For entry point requests, check required artifacts

## 4. Entry Point Validation (New)
**For specific phase entry requests:**
- **Validate prerequisites**: Check required artifacts exist
- **Context selection**: For microservices, identify available contexts
- **Missing artifacts**: List what needs to be created
- **Offer options**: Complete prerequisites, create minimal versions, or use existing

## 5. Resume Recommendations
- **Immediate next steps**: What to do right now
- **Context questions**: Ask user to confirm current understanding
- **Blocker resolution**: Address any outstanding issues
- **Approval status**: Check if any approvals are pending
- **Entry point guidance**: For new phase entry, explain prerequisites

## 6. Resume Response Format
```
## AI-DLC Resume Summary

**Iteration**: {iteration-name}
**Current Phase**: {phase} - {status}
**Last Activity**: {timestamp}
**Progress**: {completed-phases}/{total-phases} phases completed

### What's Been Completed ✅
- {list-of-completed-phases}

### Current Status 🔄
- **Phase**: {current-phase}
- **Step**: {current-step}
- **Next Action**: {what-to-do-next}

### Available Contexts (Microservices)
- **{Context 1}**: {completion-status}
- **{Context 2}**: {completion-status}

### Outstanding Items ⚠️
- {list-of-pending-items}

### Resume Options
A) Continue from where you left off
B) Review and update current phase plan
C) Skip to different phase
D) Start new iteration
E) Work on different context (if microservices)

**Recommendation**: {recommended-option} because {reasoning}

Ready to proceed with {recommended-action}?
```

## 7. Entry Point Response Format (New)
```
## AI-DLC Phase Entry: {Requested Phase}

### Prerequisite Check
- [✅/❌] User stories defined
- [✅/❌] Domain decomposition complete
- [✅/❌] Architecture decision made
- [✅/❌] {Phase-specific prerequisites}

### Available Contexts (Microservices)
- **{Context 1}**: Ready for {requested-phase}
- **{Context 2}**: Missing {prerequisites}

### Entry Options
A) Proceed with {context-name} (prerequisites met)
B) Complete missing prerequisites first
C) Create minimal artifacts to proceed
D) Select different context

**Recommendation**: {recommended-option}

Ready to {action}?
```

## 8. Error Handling
- **No iterations found**: Guide user to start new AI-DLC project
- **Corrupted state**: Ask user to clarify current status
- **Multiple active iterations**: Ask user to choose which to resume
- **Missing audit.md**: Reconstruct state from available plan files
- **Missing prerequisites**: Guide user through prerequisite creation
- **Invalid entry point**: Explain valid entry points and requirements
