---
inclusion: always
---

# AI-DLC Development Workflow

## 🎯 Essential Rules
- **DECISIONS → PLAN → EXECUTE** (Always create decisions first)
- **NEVER skip decisions** (Always create decision file with options)
- **STOP after creating plan** (Wait for approval - NEVER auto-execute)
- **NEVER fill decision answers** (User decides)
- **MANDATORY APPROVAL** (Plans require explicit user approval before execution)
- **Update plans incrementally** (Every 3-5 tasks)
- **Use .aidlc folder structure** (All artifacts)
- **Apply Domain-Driven Design** (Throughout process)

## 🚨 Critical Behaviors

### Decision Process
- Always create decisions first before any planning
- Never skip the decision step - every phase starts with decisions file
- **MANDATORY**: Use decision-record-template.md format for all decision files
- Never fill in decision answers - leave all decision fields blank for user input
- Present options clearly with rationale, but don't make decisions
- Wait for user to resolve decisions before creating plan

### Plan Process
- Always plan before executing - generate detailed plans and get approval
- **MANDATORY**: Use plan-template.md format for all plan files
- Never proceed without explicit user approval ("yes", "proceed", "approved")
- Strict two-step process: Generate plan file ONLY → Get approval → Then execute
- NEVER combine planning and execution - always stop after creating plan file
- Ask clearly: "Should I proceed with this plan?"
- **CRITICAL**: If you create a plan, you MUST stop and wait for user approval
- **VIOLATION**: Auto-executing after plan creation breaks the AI-DLC workflow

### Execution Process
- **Update plan status** after completing each phase/task with [x] checkboxes
- Complete success criteria - mark [x] before next phase
- Include backend AND frontend in logical design
- Validate before implementation using checklists
- **MANDATORY**: Use output templates for all deliverables (user-stories, domain-design, etc.)
- Always maintain audit trail - update audit.md using audit-template at each phase completion

## 📁 File Structure

### Required Structure
```
.aidlc/iterations/iteration-{N}-{feature}/
├── audit.md                           # MANDATORY: Use audit template
├── planning/
│   ├── decisions/
│   │   ├── 01-requirements-gathering.md
│   │   ├── 02-domain-decomposition.md
│   │   ├── 03-domain-design[-{context}].md
│   │   ├── 04-logical-design[-{context}].md
│   │   └── 05-implementation[-{context}].md
│   └── plans/
│       ├── 01-requirements-gathering.md
│       ├── 02-domain-decomposition.md
│       ├── 03-domain-design[-{context}].md
│       ├── 04-logical-design[-{context}].md
│       └── 05-implementation[-{context}].md
└── outputs/
    ├── inception/
    │   ├── user-stories.md
    │   └── domain-decomposition.md
    └── construction/[{context}/]
        ├── domain-design.md
        ├── logical-design.md
        └── implementation-plan.md
```

### Naming Conventions
- **Iterations**: `iteration-{number}-{feature-name}` (e.g., `iteration-1-unicorn-store`)
- **Decision/Plan Files**: `{phase-number}-{phase-name}.md` (e.g., `01-requirements-gathering.md`)
- **Context Files**: Add `-{context-name}` for microservices (e.g., `03-domain-design-catalog.md`)
- **Architecture-Specific**: Microservices use `{context}/` folders, Monolith uses single folder

## 🔄 Standard Process (Every Phase)

### Step-by-Step Flow
1. **DECISIONS** → Create decision file with options and recommendations
2. **USER RESOLVES** → User fills in decision answers
3. **PLAN** → Create execution plan based on resolved decisions
4. **USER APPROVES** → User approves the plan
5. **EXECUTE** → Implement the approved plan incrementally

### Phase Setup Process
1. Verify .aidlc structure exists (create if missing)
2. Create iteration folder using proper naming convention
3. Create required subfolders (planning/decisions/, planning/plans/, outputs/)
4. Create audit.md using audit template in iteration folder

### Phase Execution Process
1. **Load phase instructions** - Load the content of aidlc-workflow-config/phases/{phase-name}.md into context and follow its guidance
2. **Load reverse engineering context** - If .aidlc/context/ files exist, load product.md, tech.md, and structure.md into context
3. Create decision file using numbered naming in planning/decisions/
4. Wait for user to resolve decisions (never skip this step)
5. Create plan file using same number in planning/plans/
6. Get plan approval (wait for explicit approval)
7. Execute and create outputs using proper folder structure
8. Update audit.md to track phase completion

### Phase Instruction Files (Load When Entering Each Phase)
- **Requirements Gathering**: aidlc-workflow-config/phases/inception/requirements-gathering.md
- **Domain Decomposition**: aidlc-workflow-config/phases/inception/domain-decomposition.md  
- **Domain Design**: aidlc-workflow-config/phases/construction/domain-design.md
- **Logical Design**: aidlc-workflow-config/phases/construction/logical-design.md
- **Implementation**: aidlc-workflow-config/phases/construction/implementation.md

## 📊 Workflow Phases

### Inception (Business Focus)
**Greenfield Projects:**
- **1.1 Requirements Gathering** → Transform requirements into user stories
- **1.2 Domain Decomposition** → Define boundaries and choose architecture

**Brownfield Projects:**
- **1.0 Reverse Engineering** → Analyze existing codebase and create context
- **1.1 Requirements Gathering** → Transform requirements into user stories
- **1.2 Domain Decomposition** → Define boundaries and choose architecture

### Construction (Technical Focus)
- **2.1 Domain Design** → Apply DDD tactical patterns
- **2.2 Logical Design** → Create technical specifications
- **2.3 Implementation** → Generate working code

### Operation (Deployment)
- **3.1 Infrastructure** → CI/CD and monitoring

## 🏗️ Architecture Patterns

### Microservices Workflow
- **Context Selection**: Ask user directly which bounded context to work on
- **Priority Order**: Core Business → Data-Heavy → Integration → Supporting
- **File Structure**: Separate files per context (`domain-design-{context}.md`)
- **Output Organization**: Use `{context}/` folders under `outputs/construction/`

### Monolith Workflow
- **File Structure**: Single files with context sections (`domain-design.md`)
- **Output Organization**: Single `outputs/construction/` folder

## ⚡ Quick Commands
- `"start AI-DLC"` - Begin new project (detects greenfield vs brownfield)
- `"start AI-DLC greenfield"` - Begin greenfield project (skip reverse engineering)
- `"start AI-DLC brownfield"` - Begin brownfield project (include reverse engineering)
- `"start AI-DLC from domain design"` - Begin from phase 2.1
- `"start AI-DLC from logical design"` - Begin from phase 2.2
- `"start AI-DLC from implementation"` - Begin from phase 2.3
- `"resume AI-DLC"` - Resume paused iteration
- `"proceed"` or `"1"` - Approve and continue

## 🎯 Core Philosophy

### Development Approach
- **Local-First**: In-memory storage, console logging for MVP
- **MVP Focus**: Implement only what's needed to run and test
- **Testable**: Ensure each component can be tested independently

### Process Approach
- **Decision-Driven**: ADR format, cover functional and non-functional requirements
- **Incremental**: Update plans during work, not at end
- **Quality Gates**: Validate completeness before next phase

## 📚 References

### Templates
- [Decision Record](../aidlc-workflow-config/templates/planning/decision-record-template.md) - ADR format for decisions
- [Plan Template](../aidlc-workflow-config/templates/planning/plan-template.md) - Structured planning format
- [Implementation Plan](../aidlc-workflow-config/templates/planning/implementation-plan-template.md) - Technical implementation guidance
- [Output Templates](../aidlc-workflow-config/templates/outputs/) - **MANDATORY for all deliverables:**
  - user-stories-template.md
  - domain-decomposition-template.md
  - domain-design-template.md
  - logical-design-template.md
  - audit-template.md

### Guides
- [Approval Framework](../aidlc-workflow-config/guides/approval-framework.md) - How to get user approval
- [Recommendations](../aidlc-workflow-config/guides/recommendations.md) - Decision framework and templates
- [Resume Command](../aidlc-workflow-config/guides/resume-command.md) - How to resume AI-DLC sessions
- [Phase Entry](../aidlc-workflow-config/guides/phase-entry.md) - Multi-entry point support for concurrent teams

### Phase Details
- [Reverse Engineering](../aidlc-workflow-config/phases/inception/reverse-engineering.md) - Determine greenfield vs brownfield, analyze existing code
- [Requirements Gathering](../aidlc-workflow-config/phases/inception/requirements-gathering.md) - Transform requirements into user stories
- [Domain Decomposition](../aidlc-workflow-config/phases/inception/domain-decomposition.md) - Define boundaries and choose architecture
- [Domain Design](../aidlc-workflow-config/phases/construction/domain-design.md) - Apply DDD tactical patterns
- [Logical Design](../aidlc-workflow-config/phases/construction/logical-design.md) - Create technical specifications
- [Implementation](../aidlc-workflow-config/phases/construction/implementation.md) - Generate working code
- [Deployment](../aidlc-workflow-config/phases/operation/deployment.md) - Deploy to target platform

## Usage
Reference this workflow using: `#aidlc-workflow`
