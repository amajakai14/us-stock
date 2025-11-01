# 1.2 Domain Decomposition

**Objective**: Group requirements into logical boundaries using DDD Strategic Design and choose architecture pattern
**Focus**: Business capabilities, domain boundaries, architectural organization, and architecture decision

## Required Context from Previous Phases

- **From 1.1**: User stories, business rules, and success criteria from `user-stories.md`
- **From 1.1**: Non-functional requirements (performance, security, scalability needs)

## Common DDD Process

**Sequential Steps to Avoid Circular Dependency:**

1. **Identify Business Capabilities** (architecture-agnostic) → Group user stories by business function
2. **Define Bounded Contexts** (pure domain boundaries) → Identify natural domain boundaries
3. **Analyze Complexity Factors** → Team size, scalability needs, integration complexity
4. **Choose Architecture Pattern** → Microservices or Monolith based on complexity analysis
5. **Organize Contexts** → Structure bounded contexts according to chosen architecture

## Architecture Decision Criteria

### Choose Monolith When:
- Single domain or closely related domains
- Small team (1-5 developers)
- Simple to moderate complexity
- Rapid prototyping or MVP
- Limited operational expertise

### Choose Microservices When:
- Multiple distinct domains with clear boundaries
- Large team (6+ developers) or multiple teams
- High scalability requirements (1000+ concurrent users)
- Complex integration needs
- Strong operational capabilities

## Architecture-Specific Focus

### Microservices
- Context mapping, data ownership, service boundaries, integration patterns

### Monolith
- Module boundaries, shared data models, internal APIs, dependency management

## Key Deliverables

- **Architecture Decision**: Microservices or Monolith with rationale
- **Microservices**: Context map, data ownership matrix, service integration patterns, API contracts
- **Monolith**: Module dependency diagram, shared data specs, internal API definitions, layering rules
- **MANDATORY**: Use `.amazonq/templates/outputs/domain-decomposition-template.md` for consistent structure

## Phase Transition Validation

Before proceeding to Domain Design (2.1), validate:

- [ ] Architecture decision made with clear rationale
- [ ] All bounded contexts have clear responsibilities
- [ ] Data ownership matrix is complete and unambiguous
- [ ] Integration patterns are defined
- [ ] Context relationships are mapped
- [ ] All user stories are assigned to contexts
- [ ] Business rules are identified and assigned
- [ ] User approval obtained on architecture and boundaries

**Validation Questions**:
1. Does each bounded context have a single, clear responsibility?
2. Are data ownership boundaries clear and non-overlapping?
3. Can we implement each context independently?
4. Are integration points well-defined and manageable?

## Phase Restrictions

**Forbidden**: Technology stack, databases, frameworks, implementation details
