## Description

<!-- What does this PR change and why? Be concise but complete. -->

## Type of change

<!-- Check all that apply -->

- [ ] `fix/` — Bug fix (incorrect score, broken output, invalid STL geometry)
- [ ] `feat/` — New feature or new assessment section
- [ ] `docs/` — Documentation only (README, CONTRIBUTING, Code of Conduct, etc.)
- [ ] `stl/` — 3D model file change
- [ ] `refactor/` — Code restructuring with no behaviour change

---

## Governance check

<!-- Required for ALL pull requests. Answer honestly. -->

Does this PR touch any governance-sensitive areas?

- [ ] Scoring weights (`WEIGHTS` in `assess_agent.py`)
- [ ] Verdict thresholds (GREEN ≥ 7 / AMBER 4–6 / RED ≤ 3)
- [ ] Mandatory assessment sections
- [ ] Code of Conduct or SECURITY policy

**If any box above is checked**, this PR requires sign-off from an independent reviewer (not the author) before it can be merged. Include your written rationale below explaining how this change improves governance outcomes.

> _Rationale (required if governance-sensitive):_

---

## Changes to `assess_agent.py`

<!-- Complete this section if the assessment tool was modified. Delete if not applicable. -->

| Section scorer changed | Before (example score) | After (example score) |
|---|---|---|
| | | |

What inputs now score differently, and why is that more accurate?

---

## Changes to STL files

<!-- Complete this section if any file in `agent_assessment_3d/` was modified. Delete if not applicable. -->

- [ ] Model is watertight (verified with `trimesh`)
- [ ] Prints without supports (draft angles ≥ 3°)
- [ ] Generator script updated alongside the STL binary
- Printer used for validation:
- Slicer and settings:

---

## Testing

<!-- How did you verify this change works correctly? -->

- [ ] Ran `assess_agent.py` end-to-end and reviewed output
- [ ] Checked generated `.md` report and `-tags.json` for correctness
- [ ] Verified STL files load in Blender / slicer without errors
- [ ] Reviewed documentation changes for accuracy

---

## Related issues

<!-- Link any related issues: "Closes #123" or "Related to #456" -->

---

## Checklist

- [ ] Branch name follows conventions (`fix/`, `feat/`, `docs/`, `stl/`, `refactor/`)
- [ ] Commit messages are written in the imperative mood
- [ ] No secrets, credentials, or API keys are included
- [ ] `CONTRIBUTING.md` guidelines have been followed
