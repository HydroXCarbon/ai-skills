<!--
  Reference files hold detailed criteria, sub-conditions, or reusable
  data the skill body links to instead of inlining. Keeping these in a
  separate file means the SKILL.md stays scannable while detail-heavy
  content (rubrics, decision tables, lookup data) lives one click away.

  Reference from SKILL.md as:
    For detailed criteria, see [references/<file>.md](references/<file>.md).

  The example below uses a code-review rubric as a worked sample —
  swap categories and items for your skill's domain.
-->

# {Reference Topic Title}

## {Category 1 — listed first if it should be checked first}

- {Item or criterion}: {short prompt or check}
- {Item or criterion}: {short prompt or check}
- {Item or criterion}: {short prompt or check}

## {Category 2}

- {Item or criterion}: {short prompt or check}
- {Item or criterion}: {short prompt or check}

## {Category 3}

- {Item or criterion}: {short prompt or check}

---

## Example — Code Review Criteria

### Security (Check First)

- SQL injection: are user inputs parameterized?
- XSS: is output properly escaped before rendering?
- Auth checks: are protected routes actually protected?
- Secrets: are API keys or credentials hardcoded anywhere?
- Input validation: is validation happening server-side?

### Correctness

- Does the logic match the stated intent?
- Are edge cases handled: empty arrays, null values, zero, negative numbers?
- Are error states surfaced correctly?
- Are async operations awaited properly?

### Readability

- Can a new team member understand this in 5 minutes?
- Are variable and function names descriptive?
- Are functions doing one thing or multiple things?

### Performance

- Are there obvious N+1 query patterns?
- Are expensive operations inside loops that could be outside?

### Tests

- Are there tests for the new behavior?
- Are edge cases tested, not just the happy path?
