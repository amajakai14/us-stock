# 2.3 Implementation

**Objective**: Generate working code based on logical design specifications
**Focus**: Domain models, API endpoints, data access, integration components

## Entry Point Requirements
**Can start this phase if:**
- [ ] `user-stories.md` exists from phase 1.1
- [ ] `domain-decomposition.md` exists from phase 1.2
- [ ] Domain design completed for target context (from phase 2.1)
- [ ] Logical design completed for target context (from phase 2.2)
- [ ] Technical specifications and technology choices defined

**Missing Prerequisites Handling:**
- Guide user to complete missing phases first
- Validate logical design completeness before proceeding
- Ensure all technical specifications are defined

## Required Context from Previous Phases

- **From 1.1**: User stories for feature validation from `user-stories.md`
- **From 1.2**: Architecture pattern and integration requirements from `domain-decomposition.md`
- **From 2.1**: Domain model specifications from `domain_design.md`
- **From 2.2**: Technical specifications and technology choices from `logical_design.md`

## Process

- **MANDATORY**: Use the implementation plan template at `.amazonq/templates/planning/implementation-plan-template.md` for systematic implementation
- **MANDATORY**: Map all MVP user stories from phase 1.1 to implementation tasks
- Apply local-first development approach
- Implement MVP scope first, then plan future features
- Ensure testable and runnable components

## User Story Traceability Requirements

### Before Creating Implementation Plan:
1. **Review user-stories.md** from phase 1.1 requirements gathering
2. **Identify MVP user stories** that must be implemented
3. **Map each user story** to specific implementation tasks
4. **Validate completeness** - ensure no MVP stories are missed

### During Implementation:
- **Reference user stories** in each task description
- **Validate acceptance criteria** for each implemented story
- **Test user workflows** end-to-end per story
- **Update story status** as implementation progresses

## Implementation Priority

1. **User Story Driven**: Implement features that complete user stories end-to-end
2. **Local-First**: Implement for local development first (in-memory storage, console logging)
3. **MVP Focus**: Implement only what's needed to satisfy MVP user stories
4. **Feature-Complete**: Each implementation phase should complete specific user stories
5. **Testable**: Ensure each user story can be validated independently

## Phase Transition Validation

Before proceeding to Operation phase (3.1), validate:

- [ ] All MVP user stories from phase 1.1 are implemented
- [ ] Each user story's acceptance criteria are met
- [ ] User workflows are complete and testable
- [ ] Application runs locally without errors
- [ ] All implemented features have been validated
- [ ] **User story traceability** is complete and documented

## Post-MVP Planning

After MVP completion, create implementation plan for future features:
- Review "Future" scope items from logical design (step 2.2)
- Review post-MVP user stories from requirements (step 1.1)
- Prioritize post-MVP features based on business value
- Create implementation roadmap with phases
- Document technical debt and refactoring needs
- Plan integration points for future features
