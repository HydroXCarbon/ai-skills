<!--
  Spec authoring rules:
  - This is a PLANNING artifact for plan mode, not a design or implementation doc.
  - No code blocks, function signatures, file paths to be created/edited,
    library/framework picks, or other implementation details.
  - Capture intent, behavior, and unknowns. Implementation lives in code.
  - Replace `<feature-name>` in the H1 with a human-readable name.
  - File name: `_specs/<feature-slug>.md` where slug is lowercase-kebab.
  - Delete sections that are genuinely N/A; do not leave empty placeholders.
  - When the brief is sparse, prefer fewer concrete items + more
    items in Open questions over invented detail.
-->

# Spec for <feature-name> branch

## Summary

<!-- 2-4 sentences. State the problem, the affected user, and the intended
     outcome. Avoid restating the title. No "how" — only what and why. -->

## Functional requirements

<!-- Bulleted, user-visible behaviors implied by the brief. Each bullet
     describes WHAT the system does from the user's perspective, not HOW
     it does it. No technology, no APIs, no internal mechanics. -->

-

## Possible edge cases

<!-- Bulleted scenarios that could break the happy path: invalid input,
     concurrent actions, empty/large data, permission boundaries,
     network/timeouts, recovery after failure, etc. State the scenario
     and the expected user-visible behavior. -->

-

## Acceptance criteria

<!-- Bulleted, testable "done when" statements. Each item must be
     verifiable without reading the implementation. Prefer observable
     outcomes ("user sees X", "system rejects Y") over internal state. -->

-

## Open questions

<!-- Bulleted unresolved decisions. For each: state the question and,
     when known, the candidate options. Resolve before implementation.
     Put ambiguity here rather than guessing in other sections. -->

-

## Testing guidelines

<!-- What scenarios validate this spec? Cover the happy path, the edge
     cases above, and any regressions to watch for. Stay at the strategy
     level — name the scenarios, not test files or frameworks. -->

-
