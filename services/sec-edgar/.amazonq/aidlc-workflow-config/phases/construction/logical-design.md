# 2.2 Logical Design

**Objective**: Transform domain design into technical implementation specifications
**Focus**: Technology stack, API contracts, data persistence, integration patterns

## Entry Point Requirements
**Can start this phase if:**
- [ ] `user-stories.md` exists from phase 1.1
- [ ] `domain-decomposition.md` exists from phase 1.2
- [ ] Domain design completed for target context (from phase 2.1)
- [ ] Domain entities and business rules defined
- [ ] Repository interfaces specified

**Missing Prerequisites Handling:**
- Guide user to complete missing phases first
- Offer to create minimal domain design if missing
- Validate domain model completeness before proceeding

## Required Context from Previous Phases

- **From 1.1**: User stories and non-functional requirements from `user-stories.md`
- **From 1.2**: Architecture decision and bounded context definitions from `domain-decomposition.md`
- **From 2.1**: Domain entities, value objects, and business rules from `domain_design.md`

## CRITICAL SUCCESS CRITERIA

- ✅ Must cover ALL user stories from requirements (step 1.1)
- ✅ Must align with bounded context responsibilities (step 1.2)
- ✅ Must implement domain entities from domain design (step 2.1)
- ✅ Must include BOTH backend AND frontend specifications
- ✅ Must define MVP scope clearly (what's in, what's out)
- ✅ Must be runnable and testable locally first

## Technical Requirements Source Priority

1. **First**: Check `/docs/technical-requirements.md` for technical constraints and decisions
2. **Second**: Check project root `technical-requirements.md`
3. **Third**: If no file found, ask comprehensive questions below

## Process

- If technical-requirements.md exists: Read, analyze, and incorporate solutions into logical design
- **Cross-reference**: Map each user story to technical components (API endpoints, UI screens, data models)
- **Validate completeness**: Ensure all domain entities have corresponding technical specs
- Generate logical design document that aligns with technical requirements
- If technical-requirements.md missing: Ask comprehensive questions to gather technical decisions

## Architecture-Specific Approach

### Microservices - Context Selection and Design

**Context Selection (No Decision File)**:
- **If coming from Domain Design**: Continue with the same context that was just completed
- **If starting fresh**: Ask user directly which bounded context to design
- **Present options** with recommended priority if multiple contexts available
- **Wait for user selection** - User responds with context name or number
- **No formal decision file needed** - This is a simple workflow choice

**File Generation**:
- **Create logical design decision file** for selected bounded context only
- **Create logical design plan file** for selected bounded context
- **Execute logical design** for selected bounded context
- **File naming**: `logical-design-{context-name}.md`
- **Location**: `.aidlc/iterations/iteration-{N}-{feature}/outputs/construction/{context-name}/logical-design.md`

**Context Completion Options**:
After completing one context, ask user:
- **Option A**: Continue with next bounded context (repeat logical design)
- **Option B**: Proceed to Implementation for completed context
- **Option C**: Complete all contexts before implementation

### Monolith Architecture
- **Create single logical design file** covering all bounded contexts
- **File naming**: `logical-design.md`
- **Location**: `.aidlc/iterations/iteration-{N}-{feature}/outputs/construction/logical-design.md`
- **Structure**: Organize by bounded context sections within the single file

## Mandatory Sections in Logical Design Document

### 1. User Story Mapping (NEW)
- Map each user story from step 1.1 to technical components
- Identify which APIs, UI screens, and data models are needed
- Mark MVP vs Future scope

### 2. Backend Design
- API endpoints (all CRUD operations)
- Data models and persistence
- Business logic layer
- Integration patterns

### 3. Frontend Design (MANDATORY - often missed)
- UI components for each user story
- Forms for create/edit operations
- List/detail views
- Navigation and routing
- State management approach

### 4. MVP Task Breakdown (NEW)
- Phase 1: Core domain + basic CRUD (runnable)
- Phase 2: UI for all operations (testable)
- Phase 3: Integration and polish
- Clearly mark what's MVP vs Future

### 5. Completeness Checklist (Architecture-Aware)
- [ ] All user stories have technical specs
- [ ] All domain entities have {microservices: API endpoints | monolith: data models}
- [ ] All operations have UI components
- [ ] Create, Read, Update, Delete all covered
- [ ] Backend + Frontend both specified
- [ ] {microservices: Service boundaries and integration points | monolith: Module boundaries and internal APIs} defined
- [ ] {microservices: Local development approach | monolith: Shared database schema} defined
- [ ] MVP scope clearly defined

## Comprehensive Question Framework

**When to Ask Questions**: Only if technical-requirements.md is missing

Use the comprehensive technical questions framework at `.amazonq/templates/frameworks/technical-questions-framework.md` to gather technical decisions systematically.

**Key Categories**: Architecture, Frontend, Backend, Data, Infrastructure, Integration, Observability, Security, Testing, CI/CD

**Note**: For existing projects, check existing patterns first before asking questions.

## Validation Before Moving to Implementation

Before proceeding to step 2.3 (Implementation), validate the logical design:

### 1. User Story Coverage Check
- Review user-stories.md from step 1.1
- Verify each user story has corresponding technical specs
- Confirm all CRUD operations are specified

### 2. Frontend Completeness Check
- Verify UI components are specified for all user interactions
- Confirm forms exist for create/edit operations
- Ensure list and detail views are defined
- Check navigation and routing are planned

### 3. Backend Completeness Check
- Verify all API endpoints are defined
- Confirm data models match domain entities
- Ensure all business logic is specified

### 4. MVP Scope Validation
- Confirm what's in MVP vs future
- Verify MVP is runnable and testable locally
- Ensure no critical features are missing

### 5. Cross-Reference with Domain Decomposition
- Review domain-decomposition.md from step 1.2
- **Microservices**: Verify bounded context responsibilities are covered and integration points are specified
- **Monolith**: Verify module responsibilities are covered and internal APIs are specified

**If any checks fail, update the logical design before proceeding to implementation.**

**Logical Design Template**: **MANDATORY** - Use the template at `.amazonq/templates/outputs/logical-design-template.md` to ensure complete coverage of all required sections including project structure.
