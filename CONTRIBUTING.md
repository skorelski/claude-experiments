# Contributing to the AI Agent Assessment Project

Thank you for your interest in contributing. This project exists to make AI agent governance practical, collaborative, and honest. Every improvement — whether to the assessment logic, the 3D print files, the documentation, or the scoring model — helps teams make better decisions about AI deployment.

---

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Branch and Commit Conventions](#branch-and-commit-conventions)
- [What Can Be Changed and What Cannot](#what-can-be-changed-and-what-cannot)
- [Contribution Types](#contribution-types)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Reporting Issues](#reporting-issues)
- [Recognition](#recognition)

---

## Ways to Contribute

You do not need to write code to contribute. The project welcomes contributions across several areas:

- **Assessment logic** — improvements to section scorers, weighting, or attention point detection in `assess_agent.py`
- **3D print files** — refined STL geometry, new pieces, or fixes for printability issues
- **Documentation** — clearer descriptions, better examples, translations
- **Governance documents** — suggestions for the Code of Conduct, this file, or the SECURITY policy
- **New assessment sections** — proposals for additional governance areas not yet covered
- **Bug reports** — anything that produces incorrect scores, broken output, or invalid STL geometry

---

## Getting Started

1. **Fork the repository** and clone your fork locally.

2. **Set up the Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install trimesh manifold3d shapely pillow --break-system-packages
   ```

3. **Install Node dependencies** (only needed if modifying `.docx` generation):
   ```bash
   npm install docx
   ```

4. **Run the assessment tool** to confirm everything works before making changes:
   ```bash
   cd 05_evaluation
   python assess_agent.py
   ```

5. **Create a branch** for your change (see conventions below).

---

## Branch and Commit Conventions

Use short, descriptive branch names prefixed by type:

| Prefix | Use for |
|---|---|
| `fix/` | Bug fixes |
| `feat/` | New features or sections |
| `docs/` | Documentation-only changes |
| `stl/` | 3D model file changes |
| `refactor/` | Code restructuring with no behaviour change |

**Examples:**
```
fix/scope-scorer-zero-boundary
feat/add-compliance-section
docs/clarify-finops-guidance
stl/improve-tile-rim-geometry
```

Commit messages should be concise and written in the imperative mood. Lead with the what, follow with the why if it is not obvious:

```
Fix context scorer returning 0 for medium-sized agents

The size_map lookup was missing the 'medium' key after a refactor,
causing all medium-context agents to receive a score of 5 with no
adjustment, regardless of whether a context strategy was defined.
```

---

## What Can Be Changed and What Cannot

Some parts of this project are considered **governance-sensitive** and require additional scrutiny before being changed.

### Requires explicit reviewer sign-off

- The scoring weights in `WEIGHTS` (in `assess_agent.py`)
- The verdict thresholds (GREEN ≥ 7, AMBER 4–6, RED ≤ 3)
- The set of mandatory assessment sections
- The Code of Conduct
- The SECURITY policy

Changes to these elements affect deployment decisions for real AI agents. Any pull request touching them must include a written rationale explaining why the change improves governance outcomes, not just code quality.

### Open for improvement

- Individual section scorer functions (`score_purpose`, `score_tasks`, etc.)
- Attention point detection logic
- Output formatting and report structure
- STL geometry and print quality
- Documentation wording and examples
- README and setup instructions

---

## Contribution Types

### Improving the Assessment Tool (`assess_agent.py`)

When modifying a scorer, include in your pull request:

- A description of what the current behaviour misses or gets wrong
- The specific inputs that now score differently and why that is more accurate
- A brief test showing the score before and after your change

### Adding a New Assessment Section

New sections are welcome but must clear a higher bar. Open an issue first to discuss the proposal before writing code. A new section should:

- Address a governance gap not already covered by existing sections
- Have clear, objective scoring criteria (not just subjective judgement)
- Include a corresponding physical tile concept (symbol, colour suggestion)
- Update the `WEIGHTS` dictionary so all weights still sum to 1.0

### Modifying STL Files

If you improve any of the 3D models in `05_evaluation/agent_assessment_3d/`:

- Verify the model is watertight using `trimesh` before submitting
- Confirm it prints without supports (draft angles ≥ 3°)
- Include the updated generator script alongside the STL, not just the binary file
- Note the printer and slicer settings you used to validate it

### Documentation Changes

For documentation-only changes you do not need to open an issue first. Just submit a pull request with a clear description of what was unclear and how your version improves it.

---

## Pull Request Process

1. **Open an issue first** for any non-trivial change, so the approach can be agreed before you invest time writing code.
2. **Keep pull requests focused** — one logical change per PR. Avoid combining unrelated fixes.
3. **Fill out the PR description** — explain what changed, why, and how you tested it.
4. **All governance-sensitive changes** require at least one reviewer who is not the author.
5. **Non-governance changes** require at least one passing review before merge.
6. **Squash commits** before merging if your branch has more than three commits, to keep the history readable.

---

## Code Style

The project uses plain Python with no formatter enforced, but please follow these conventions:

- **PEP 8** for naming and spacing
- **Descriptive variable names** — `score_context` not `sc`
- **Comments on scoring logic** — if a scoring decision is not obvious, explain it in a comment
- **No external dependencies** beyond those already in `requirements.txt` without prior discussion
- **No hard-coded paths** — use `os.path` relative to the script location

For JavaScript (docx generation), follow the existing style in `code_of_conduct.js` — constants at the top, helper functions grouped by purpose.

---

## Reporting Issues

Open a GitHub issue with the following information:

- **For scoring bugs:** the input values that produce the wrong score, the expected score, and the actual score
- **For STL issues:** the printer model, slicer, and settings used, plus a description of the print failure
- **For documentation issues:** the section that is unclear and what you understood it to mean
- **For security issues:** do not open a public issue — follow the process in [SECURITY.md](SECURITY.md)

---

## Recognition

All contributors are recognised in the project's release notes. Significant contributions — new sections, major scorer improvements, validated STL redesigns — are highlighted specifically. If you contributed and are not credited, please open an issue.

---

*Last updated: April 2026*
