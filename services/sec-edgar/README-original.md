# AI-DLC Workshop

## ⚠️ Important Setup Note
**You must rename or remove this README.md file before proceeding with AI-DLC workflow.**

The AI-DLC process expects to create its own project documentation and this file may interfere with the workflow.

## AI-DLC Development Workflow

### Process Flow
```
🎯 INCEPTION (Business Focus)
Greenfield Projects:
├── 1.1 Requirements Gathering → Transform requirements into user stories
└── 1.2 Domain Decomposition → Define boundaries and choose architecture

Brownfield Projects:
├── 1.0 Reverse Engineering → Analyze existing codebase and create context
├── 1.1 Requirements Gathering → Transform requirements into user stories
└── 1.2 Domain Decomposition → Define boundaries and choose architecture

🔧 CONSTRUCTION (Technical Focus)
├── 2.1 Domain Design → Apply DDD tactical patterns
├── 2.2 Logical Design → Create technical specifications
└── 2.3 Implementation → Generate working code

🚀 OPERATION (Deployment Focus)
└── 3.1 Infrastructure → CI/CD and monitoring
```

### Enhanced Standard Process (Every Phase)
1. **DECISIONS** → Create decision file using mandatory decision-record-template
2. **USER RESOLVES** → User fills in decision answers (AI never auto-fills)
3. **PLAN** → Create execution plan using mandatory plan-template
4. **MANDATORY APPROVAL** → User explicitly approves plan before execution
5. **EXECUTE** → Implement incrementally with phase status tracking

### Key Workflow Enhancements
- **Template Enforcement**: All files use mandatory templates (decisions, plans, outputs)
- **Project Type Detection**: Automatically handles greenfield vs brownfield projects
- **Phase Status Tracking**: Plans updated with [x] checkboxes after each phase completion
- **Comprehensive Decision Coverage**: Enhanced decision frameworks for thorough coverage
- **Strict Approval Gates**: AI stops after plan creation, waits for explicit user approval

### Quick Commands
- `"start AI-DLC"` - Begin new project (detects greenfield vs brownfield)
- `"start AI-DLC greenfield"` - Begin greenfield project (skip reverse engineering)
- `"start AI-DLC brownfield"` - Begin brownfield project (include reverse engineering)
- `"start AI-DLC from domain design"` - Begin from phase 2.1
- `"start AI-DLC from logical design"` - Begin from phase 2.2
- `"start AI-DLC from implementation"` - Begin from phase 2.3
- `"resume AI-DLC"` - Resume paused iteration
- `"proceed"` or `"1"` - Approve and continue

### File Structure Created
```
.aidlc/iterations/iteration-{N}-{feature}/
├── audit.md                           # Mandatory audit trail using audit-template
├── planning/
│   ├── decisions/                     # Decision files using decision-record-template
│   │   ├── 01-requirements-gathering.md
│   │   ├── 02-domain-decomposition.md
│   │   └── 03-{phase}[-{context}].md
│   └── plans/                         # Plan files using plan-template
│       ├── 01-requirements-gathering.md
│       ├── 02-domain-decomposition.md
│       └── 03-{phase}[-{context}].md
└── outputs/                           # All outputs use mandatory templates
    ├── inception/
    │   ├── user-stories.md            # Uses user-stories-template
    │   └── domain-decomposition.md    # Uses domain-decomposition-template
    └── construction/[{context}/]
        ├── domain-design.md           # Uses domain-design-template
        ├── logical-design.md          # Uses logical-design-template
        └── implementation-plan.md
```

### Template System
All artifacts use mandatory templates from `.amazonq/aidlc-workflow-config/templates/`:
- **Planning**: decision-record-template, plan-template
- **Outputs**: user-stories-template, domain-design-template, logical-design-template, etc.
- **Frameworks**: Comprehensive question frameworks for decision coverage

## Getting Started
1. **Rename or remove this README.md file**
2. Use command: `"start AI-DLC"` (will detect project type)
3. Follow the enhanced decision → plan → execute process with mandatory approvals
4. Reference: `#aidlc-workflow` for detailed guidance

## Workflow Guarantees
- ✅ No auto-execution - AI always stops for user approval
- ✅ Template consistency - All files follow mandatory templates
- ✅ Complete audit trail - Phase completion tracking
- ✅ Comprehensive decisions - Enhanced frameworks ensure thorough coverage
- ✅ Project type awareness - Handles greenfield/brownfield appropriately
