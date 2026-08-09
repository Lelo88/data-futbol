# Contributing

This project is currently under active development.

Contributions should follow the current phase of the project and keep the documentation aligned with the actual work completed.

## Phase execution

Every phase must follow a clear execution lifecycle:

Pending → In Progress → Completed

A phase may only transition to Completed after:

1. The planned work has been completed.
2. Required validation or review has been performed.
3. Phase-specific documentation has been completed.
4. The documentation synchronization review has been performed.
5. Required documentation updates have been included in the phase branch and PR.

Changes outside the defined phase scope require explicit justification. If an additional file must be modified because of a consistency or dependency discovered during the phase, the reason must be documented rather than silently expanding the scope.

## Documentation synchronization

Every completed phase must include a documentation synchronization review before the phase can be considered complete.

The synchronization step determines which project documentation needs to be updated based on the actual changes produced by the phase. It does not imply that every documentation file must be modified for every phase.

### Always review

The following files must be reviewed at the end of every completed phase:

- docs/project-status.md
- CHANGELOG.md
- README.md
- Documentation directly related to the completed phase

### Update when applicable

The following files must only be modified when the phase actually requires it:

- docs/decision-log.md
- CONTRIBUTING.md
- ARCHITECTURE.md
- Other project documentation affected by the phase

Do not modify a file merely to create a documentation change.

### project-status.md

docs/project-status.md must be updated whenever a phase changes its project status.
The status must accurately represent the actual state of the project.
Future phases must not be marked as started or completed unless work on them has actually begun.
A phase cannot be considered fully completed until its status is synchronized.

### CHANGELOG.md

CHANGELOG.md must be reviewed at the end of every phase.
It must be updated when the phase introduces a meaningful project change, such as new functionality, significant documentation, architecture changes, important project decisions, or changes that materially affect project behavior or scope.
Trivial internal changes do not require a changelog entry.
Changelog entries must describe changes that actually exist in the completed phase.
Do not document planned or future work as completed changes.

### README.md

README.md must be reviewed at the end of every phase.
It must only be modified when information becomes outdated or incomplete as a consequence of the completed phase.
Do not add progress information to the README if the existing README does not use that concept.
Avoid duplicating detailed project status or phase documentation in the README.

### docs/decision-log.md

docs/decision-log.md must only be updated when the phase produces an actual project decision.
Research, implementation, or documentation work does not automatically constitute a decision.
Decisions must be recorded only when they are meaningful enough to affect project scope, architecture, technology, data strategy, product behavior, or another documented project constraint.
Do not create artificial decision-log entries merely because a phase was completed.

### Phase-specific documentation

Every phase must maintain the documentation directly associated with that phase.
Phase-specific documentation should answer the questions and define the requirements belonging to that phase.
A phase must not modify documentation belonging to future phases unless required to maintain consistency.

## Documentation consistency review

At the end of every phase, verify consistency among:

- README.md
- CHANGELOG.md
- docs/project-status.md
- docs/decision-log.md when applicable
- phase-specific documentation
- any other affected project documentation

Check specifically that:

- completed phases are represented consistently;
- future phases remain pending;
- terminology is consistent;
- no document claims that a provider, architecture, feature, or decision has been finalized when it has not;
- no planned work is presented as completed;
- documentation does not contradict the current project state.

## Phase lifecycle

The standard phase lifecycle is:

Pending → In Progress → Completed

## Phase execution prompts

Every future phase execution prompt should explicitly define:

- Phase objective
- Scope
- Files to create
- Files to modify
- Files that must not be modified
- Validation requirements
- Documentation synchronization requirements
- Expected status after completion
- Next phase

Every future phase prompt must include the documentation synchronization review described above.

## Commit and PR relationship

Documentation changes required to complete a phase should normally be included in the same phase branch and PR.

Avoid creating unrelated documentation commits on separate branches unless there is a clear reason to do so.

## Final phase checklist

Use this checklist before merging a completed phase:

- [ ] Phase work completed
- [ ] Tests or validation completed when applicable
- [ ] Phase-specific documentation updated
- [ ] docs/project-status.md reviewed and updated if required
- [ ] CHANGELOG.md reviewed and updated if required
- [ ] README.md reviewed and updated if required
- [ ] docs/decision-log.md reviewed and updated if a real decision was made
- [ ] Other affected documentation reviewed
- [ ] Documentation consistency verified
- [ ] Future phases remain correctly marked
- [ ] PR scope matches the phase

Contribution guidelines will be published after the MVP.