# AI-DLC Phase Entry Points

## Multi-Entry Point Support

AI-DLC supports starting from any phase after domain decomposition, enabling concurrent team work and flexible project entry.

## Entry Point Commands

### Standard Entry Points
- `"start AI-DLC"` - Begin from requirements gathering (full workflow)
- `"start AI-DLC from domain design"` - Begin from phase 2.1
- `"start AI-DLC from logical design"` - Begin from phase 2.2  
- `"start AI-DLC from implementation"` - Begin from phase 2.3
- `"resume AI-DLC at phase {X.Y}"` - Resume at specific phase

### Context-Specific Entry (Microservices)
- `"start domain design for {context-name}"`
- `"start logical design for {context-name}"`
- `"start implementation for {context-name}"`

## Prerequisite Validation

### Phase 2.1 Domain Design Entry
**Required Artifacts:**
- [ ] `user-stories.md` exists (from phase 1.1)
- [ ] `domain-decomposition.md` exists (from phase 1.2)
- [ ] Architecture decision documented
- [ ] Bounded contexts defined
- [ ] User stories mapped to contexts

**Validation Process:**
1. Check for required files in `.aidlc/iterations/*/outputs/inception/`
2. Validate architecture choice is documented
3. Confirm bounded contexts are defined
4. If missing: Guide user to create minimal versions or complete prerequisites

### Phase 2.2 Logical Design Entry
**Required Artifacts:**
- [ ] All Domain Design prerequisites
- [ ] Domain design completed for target context
- [ ] Domain entities and business rules defined
- [ ] Repository interfaces specified

**Validation Process:**
1. Validate Domain Design prerequisites
2. Check domain design exists for target context
3. Confirm domain models are complete
4. If missing: Guide user to complete domain design first

### Phase 2.3 Implementation Entry
**Required Artifacts:**
- [ ] All Logical Design prerequisites
- [ ] Logical design completed for target context
- [ ] Technical specifications defined
- [ ] API contracts and data models specified

**Validation Process:**
1. Validate Logical Design prerequisites
2. Check logical design exists for target context
3. Confirm technical specifications are complete
4. If missing: Guide user to complete logical design first

## Context Selection (Microservices)

### Context Selection Process
1. **Scan domain decomposition** for available bounded contexts
2. **Ask user to select** which context to work on
3. **Validate context prerequisites** exist
4. **Proceed with context-specific work**

### Context Priority Recommendations
1. **Core Business Context** - Primary value-generating domain
2. **Data-Heavy Contexts** - Complex entity relationships
3. **Integration Contexts** - External system connections
4. **Supporting Contexts** - Utility or administrative domains

## Missing Prerequisites Handling

### When Prerequisites Are Missing
1. **List missing artifacts** clearly
2. **Offer options**:
   - A) Complete missing prerequisites first
   - B) Create minimal versions to proceed
   - C) Use existing artifacts from similar projects
3. **Guide creation** of missing artifacts using templates
4. **Validate completeness** before proceeding

### Minimal Artifact Creation
- **User Stories**: Create basic user stories from requirements
- **Domain Decomposition**: Create simplified bounded context definitions
- **Domain Design**: Create basic entity definitions

## Entry Point Workflow

### Step 1: Entry Point Detection
```
User says: "start AI-DLC from domain design"
↓
AI detects: Phase 2.1 entry point requested
↓
AI validates: Prerequisites for phase 2.1
```

### Step 2: Prerequisite Validation
```
Check required artifacts exist
↓
If missing: Guide user to create or complete
↓
If complete: Proceed to phase entry
```

### Step 3: Context Selection (if Microservices)
```
Scan domain decomposition for contexts
↓
Ask user to select target context
↓
Validate context-specific prerequisites
```

### Step 4: Phase Entry
```
Load phase-specific rules
↓
Create decisions file for selected phase
↓
Follow standard process pattern
```

## Success Criteria

- [ ] User can start from any supported entry point
- [ ] Prerequisites are validated before proceeding
- [ ] Missing artifacts are identified and addressed
- [ ] Context selection works for microservices
- [ ] Standard process pattern continues from entry point
