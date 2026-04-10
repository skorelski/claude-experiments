#!/usr/bin/env python3
"""
AI Agent Assessment Tool
========================
Interactive CLI that guides users through defining and evaluating an AI agent
before deployment. Produces a scored markdown report with JSON logging tags.

Scoring:
  7-10  GREEN   — Agent is well-defined; ready to proceed
  4-6   AMBER   — Needs attention and improvements before launch
  1-3   RED     — Insufficient; do not create the agent yet

Usage:
  python assess_agent.py
"""

import json
import os
import sys
import textwrap
from datetime import datetime, timezone

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
SEPARATOR = f"{DIM}{'─' * 60}{RESET}"


def banner():
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════╗
║            AI Agent Assessment Tool  v1.0               ║
║         Define · Score · Tag · Deploy responsibly        ║
╚══════════════════════════════════════════════════════════╝{RESET}
""")


def section_header(number, title, description):
    print(f"\n{SEPARATOR}")
    print(f"{BOLD}{CYAN}  Section {number}: {title}{RESET}")
    print(f"  {DIM}{description}{RESET}")
    print(SEPARATOR)


def ask(prompt, required=True, multiline=False):
    """Prompt for text input. If multiline, collect until empty line."""
    if multiline:
        print(f"\n  {BOLD}{prompt}{RESET}")
        print(f"  {DIM}(Enter each item on a new line. Empty line to finish){RESET}")
        lines = []
        while True:
            line = input("    → ")
            if line.strip() == "":
                if required and not lines:
                    print(f"    {RED}At least one entry is required.{RESET}")
                    continue
                break
            lines.append(line.strip())
        return lines
    else:
        while True:
            answer = input(f"\n  {BOLD}{prompt}{RESET}\n    → ").strip()
            if required and not answer:
                print(f"    {RED}This field is required.{RESET}")
                continue
            return answer


def ask_choice(prompt, options, allow_multiple=False):
    """Present numbered options. Returns selected option(s)."""
    print(f"\n  {BOLD}{prompt}{RESET}")
    for i, opt in enumerate(options, 1):
        print(f"    {CYAN}{i}.{RESET} {opt}")
    if allow_multiple:
        print(f"  {DIM}(Comma-separated numbers, e.g. 1,3){RESET}")
    while True:
        raw = input("    → ").strip()
        try:
            if allow_multiple:
                indices = [int(x.strip()) for x in raw.split(",")]
                if all(1 <= i <= len(options) for i in indices):
                    return [options[i - 1] for i in indices]
            else:
                idx = int(raw)
                if 1 <= idx <= len(options):
                    return options[idx - 1]
        except ValueError:
            pass
        print(f"    {RED}Invalid selection. Try again.{RESET}")


def ask_yes_no(prompt):
    while True:
        answer = input(f"\n  {BOLD}{prompt} (y/n){RESET}\n    → ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print(f"    {RED}Please enter y or n.{RESET}")


def score_badge(score):
    if score >= 7:
        return f"{GREEN}● GREEN{RESET}", "GREEN"
    elif score >= 4:
        return f"{YELLOW}● AMBER{RESET}", "AMBER"
    else:
        return f"{RED}● RED{RESET}", "RED"


def score_badge_md(score):
    if score >= 7:
        return "🟢 GREEN — Ready to proceed"
    elif score >= 4:
        return "🟡 AMBER — Needs attention and improvements"
    else:
        return "🔴 RED — Insufficient; do not create the agent"


# ─────────────────────────────────────────────
# Scoring engine
# ─────────────────────────────────────────────

WEIGHTS = {
    "purpose":          0.15,
    "tasks":            0.15,
    "context":          0.10,
    "data_sensitivity":  0.15,
    "human_oversight":   0.15,
    "error_handling":    0.10,
    "scope_boundaries":  0.10,
    "finops":           0.10,
}


def score_purpose(data):
    s = 0
    purpose = data.get("purpose", "")
    if len(purpose) > 20:
        s += 3
    elif purpose:
        s += 1
    if data.get("owner"):
        s += 2
    if data.get("use_case"):
        s += 2
    expected_outcome = data.get("expected_outcome", "")
    if len(expected_outcome) > 10:
        s += 3
    elif expected_outcome:
        s += 1
    return min(s, 10)


def score_tasks(data):
    tasks = data.get("tasks", [])
    if not tasks:
        return 0
    s = min(len(tasks) * 2, 6)  # up to 6 for having multiple tasks
    if data.get("task_priority"):
        s += 2
    if data.get("task_dependencies_defined"):
        s += 2
    return min(s, 10)


def score_context(data):
    size = data.get("context_size", "unknown")
    s = 5  # baseline
    size_map = {"small": 3, "medium": 2, "large": -1, "very_large": -3}
    s += size_map.get(size, 0)
    if data.get("context_strategy"):
        s += 2
    if data.get("context_chunking"):
        s += 1
    return max(1, min(s, 10))


def score_data_sensitivity(data):
    level = data.get("data_sensitivity_level", "")
    s = 0
    if level:
        s += 3  # classified at all
    if data.get("data_handling_procedures"):
        s += 3
    if data.get("data_retention_policy"):
        s += 2
    if data.get("pii_handling"):
        s += 2
    return min(s, 10)


def score_human_oversight(data):
    s = 0
    if data.get("oversight_model"):
        s += 3
    if data.get("review_triggers"):
        s += 3
    if data.get("escalation_path"):
        s += 2
    if data.get("approval_gates"):
        s += 2
    return min(s, 10)


def score_error_handling(data):
    s = 0
    if data.get("fallback_behavior"):
        s += 3
    if data.get("retry_policy"):
        s += 2
    if data.get("alerting_configured"):
        s += 3
    if data.get("graceful_degradation"):
        s += 2
    return min(s, 10)


def score_scope(data):
    s = 0
    boundaries = data.get("scope_boundaries", [])
    if boundaries:
        s += min(len(boundaries) * 2, 6)
    if data.get("allowed_actions"):
        s += 2
    if data.get("denied_actions"):
        s += 2
    return min(s, 10)


def score_finops(data):
    s = 0
    if data.get("token_budget"):
        s += 3
    if data.get("cost_alert_threshold"):
        s += 2
    if data.get("model_selection_rationale"):
        s += 2
    if data.get("usage_tracking_plan"):
        s += 3
    return min(s, 10)


SCORERS = {
    "purpose":          score_purpose,
    "tasks":            score_tasks,
    "context":          score_context,
    "data_sensitivity":  score_data_sensitivity,
    "human_oversight":   score_human_oversight,
    "error_handling":    score_error_handling,
    "scope_boundaries":  score_scope,
    "finops":           score_finops,
}

SECTION_LABELS = {
    "purpose":          "Agent Purpose",
    "tasks":            "Task Assignment",
    "context":          "Context Management",
    "data_sensitivity":  "Data Sensitivity",
    "human_oversight":   "Human Oversight",
    "error_handling":    "Error Handling",
    "scope_boundaries":  "Scope Boundaries",
    "finops":           "FinOps & Token Usage",
}


# ─────────────────────────────────────────────
# Interactive form sections
# ─────────────────────────────────────────────

def collect_purpose():
    section_header(1, "Agent Purpose", "Define why this agent exists and what outcome it delivers")
    data = {}
    data["agent_name"] = ask("Agent name (used as filename, e.g. 'order-processor'):")
    data["purpose"] = ask("Describe the agent's purpose in one or two sentences:")
    data["owner"] = ask("Who owns this agent? (team or individual):")
    data["use_case"] = ask("Primary use case (e.g. 'customer support triage', 'code review'):")
    data["expected_outcome"] = ask("What is the expected outcome when this agent runs successfully?")
    return data


def collect_tasks():
    section_header(2, "Task Assignment", "List the specific tasks this agent will perform")
    data = {}
    data["tasks"] = ask("List each task the agent should perform:", multiline=True)
    data["task_priority"] = ask_yes_no("Have you defined priority/order for these tasks?")
    data["task_dependencies_defined"] = ask_yes_no("Are dependencies between tasks identified?")
    return data


def collect_context():
    section_header(3, "Context Management", "Assess the input context the agent will work with")
    data = {}
    data["context_size"] = ask_choice(
        "Expected context size per invocation:",
        ["small (< 4K tokens)", "medium (4K–32K tokens)",
         "large (32K–128K tokens)", "very_large (> 128K tokens)"]
    ).split(" ")[0]
    data["context_sources"] = ask("What are the input sources? (e.g. API, database, user prompt, files):")
    data["context_strategy"] = ask_yes_no(
        "Do you have a strategy for managing large contexts? (summarisation, chunking, RAG, etc.)"
    )
    if data["context_strategy"]:
        data["context_strategy_detail"] = ask("Briefly describe your context management strategy:")
        data["context_chunking"] = True
    else:
        data["context_chunking"] = False
    return data


def collect_data_sensitivity():
    section_header(4, "Data Sensitivity", "Classify the data this agent will access and process")
    data = {}
    data["data_sensitivity_level"] = ask_choice(
        "Highest data sensitivity level the agent will handle:",
        ["Public", "Internal", "Confidential", "Restricted / Regulated"]
    )
    data["data_types"] = ask("What types of data will the agent process? (e.g. PII, financial, health):")
    data["pii_handling"] = ask_yes_no("Is there a documented procedure for handling PII?")
    data["data_handling_procedures"] = ask_yes_no(
        "Are data handling procedures documented? (encryption, masking, anonymisation)"
    )
    data["data_retention_policy"] = ask_yes_no("Is there a data retention/deletion policy in place?")
    return data


def collect_human_oversight():
    section_header(5, "Human Oversight", "Define how humans stay in the loop")
    data = {}
    data["oversight_model"] = ask_choice(
        "What oversight model applies to this agent?",
        ["Human-in-the-loop (approval before every action)",
         "Human-on-the-loop (monitoring with intervention capability)",
         "Human-over-the-loop (periodic review only)",
         "Fully autonomous (no routine human oversight)"]
    )
    data["review_triggers"] = ask_yes_no(
        "Are there defined triggers that escalate to a human? (e.g. low confidence, edge cases)"
    )
    if data["review_triggers"]:
        data["review_trigger_details"] = ask("List the key escalation triggers:", multiline=True)
    data["escalation_path"] = ask_yes_no("Is there a documented escalation path?")
    data["approval_gates"] = ask_yes_no(
        "Are there approval gates before critical actions? (e.g. sending emails, modifying data)"
    )
    return data


def collect_error_handling():
    section_header(6, "Error Handling & Fallbacks", "Plan for when things go wrong")
    data = {}
    data["fallback_behavior"] = ask_yes_no(
        "Is there a defined fallback behavior when the agent fails?"
    )
    if data["fallback_behavior"]:
        data["fallback_detail"] = ask("Describe the fallback behavior:")
    data["retry_policy"] = ask_yes_no("Is there a retry policy defined? (max retries, backoff)")
    data["alerting_configured"] = ask_yes_no(
        "Will alerts be sent when the agent encounters errors? (e.g. Slack, PagerDuty, email)"
    )
    data["graceful_degradation"] = ask_yes_no(
        "Can the agent degrade gracefully? (partial results instead of full failure)"
    )
    return data


def collect_scope():
    section_header(7, "Scope Boundaries", "Define explicit limits on what the agent must NOT do")
    data = {}
    data["scope_boundaries"] = ask(
        "List things this agent should explicitly NOT do:", multiline=True
    )
    data["allowed_actions"] = ask_yes_no(
        "Is there a defined allow-list of permitted actions/tools?"
    )
    data["denied_actions"] = ask_yes_no(
        "Is there a defined deny-list of prohibited actions/tools?"
    )
    return data


def collect_finops():
    section_header(8, "FinOps & Token Usage", "Budget and track the cost of running this agent")
    data = {}
    data["model_name"] = ask("Which model(s) will this agent use? (e.g. claude-sonnet-4-6):")
    data["token_budget"] = ask(
        "Max token budget per invocation (leave blank if not yet defined):", required=False
    )
    data["cost_alert_threshold"] = ask(
        "Monthly cost alert threshold in USD (leave blank if not defined):", required=False
    )
    data["model_selection_rationale"] = ask_yes_no(
        "Is the model choice documented with rationale? (cost vs. capability trade-off)"
    )
    data["usage_tracking_plan"] = ask_yes_no(
        "Is there a plan for tracking token usage over time?"
    )
    return data


# ─────────────────────────────────────────────
# Tag generation
# ─────────────────────────────────────────────

def generate_tags(data, scores, overall):
    """Generate JSON logging tags from the assessment data."""
    agent_name = data.get("agent_name", "unnamed-agent")
    safe_name = agent_name.lower().replace(" ", "-")

    tags = {
        "agent_name": safe_name,
        "agent_purpose": data.get("use_case", "undefined"),
        "agent_owner": data.get("owner", "undefined"),
        "agent_model": data.get("model_name", "undefined"),
        "agent_assessment_score": overall,
        "agent_assessment_status": score_badge_md(overall).split(" ")[1],
        "agent_data_sensitivity": data.get("data_sensitivity_level", "undefined"),
        "agent_oversight_model": data.get("oversight_model", "undefined").split("(")[0].strip(),
        "agent_context_size": data.get("context_size", "undefined"),
        "agent_token_budget": data.get("token_budget", "undefined") or "undefined",
        "agent_cost_alert_usd": data.get("cost_alert_threshold", "undefined") or "undefined",
        # Logging event hooks — these are tag keys to attach to log events
        "logging_events": {
            "agent_start": f"{safe_name}.start",
            "agent_stop": f"{safe_name}.stop",
            "agent_error": f"{safe_name}.error",
            "agent_escalation": f"{safe_name}.escalation",
            "tokens_used": f"{safe_name}.tokens_used",
            "agent_fallback": f"{safe_name}.fallback",
            "agent_cost": f"{safe_name}.cost",
        },
        "section_scores": {k: v for k, v in scores.items()},
    }
    return tags


# ─────────────────────────────────────────────
# Markdown report generation
# ─────────────────────────────────────────────

def generate_attention_points(data, scores):
    """Flag areas that need attention."""
    points = []
    for key, score in scores.items():
        if score < 7:
            label = SECTION_LABELS[key]
            if score <= 3:
                points.append(f"🔴 **{label}** (score: {score}/10) — Critical: not sufficient to proceed")
            else:
                points.append(f"🟡 **{label}** (score: {score}/10) — Needs improvement before launch")

    # Extra contextual flags
    if data.get("context_size") in ("large", "very_large"):
        points.append("⚠️ **Large context detected** — Ensure summarisation/chunking strategy is in place")
    if data.get("data_sensitivity_level") in ("Confidential", "Restricted / Regulated"):
        if not data.get("pii_handling"):
            points.append("⚠️ **High-sensitivity data without PII procedures** — Document PII handling before launch")
    if "Fully autonomous" in str(data.get("oversight_model", "")):
        points.append("⚠️ **Fully autonomous agent** — Consider adding at least periodic review checkpoints")
    if not data.get("token_budget"):
        points.append("⚠️ **No token budget defined** — Risk of uncontrolled costs")

    return points


def generate_markdown(data, scores, overall, tags):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    agent_name = data.get("agent_name", "unnamed-agent")
    badge = score_badge_md(overall)
    attention = generate_attention_points(data, scores)

    # Build task list
    tasks_md = ""
    for i, t in enumerate(data.get("tasks", []), 1):
        tasks_md += f"  {i}. {t}\n"

    # Build scope boundaries
    scope_md = ""
    for b in data.get("scope_boundaries", []):
        scope_md += f"  - {b}\n"

    # Build escalation triggers
    triggers_md = ""
    for t in data.get("review_trigger_details", []):
        triggers_md += f"  - {t}\n"

    # Attention points
    attention_md = ""
    if attention:
        for a in attention:
            attention_md += f"- {a}\n"
    else:
        attention_md = "_No attention points — all sections scored 7 or above._\n"

    # Score breakdown table
    score_table = "| Section | Score | Status |\n|---|---|---|\n"
    for key in WEIGHTS:
        s = scores[key]
        label = SECTION_LABELS[key]
        if s >= 7:
            status = "🟢 Green"
        elif s >= 4:
            status = "🟡 Amber"
        else:
            status = "🔴 Red"
        score_table += f"| {label} | {s}/10 | {status} |\n"

    # Build markdown sections as a list and join
    lines = []
    lines.append(f"# Agent Assessment: {agent_name}")
    lines.append("")
    lines.append(f"**Date:** {now}  ")
    lines.append(f"**Owner:** {data.get('owner', '—')}  ")
    lines.append(f"**Model:** {data.get('model_name', '—')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"## Overall Score: {overall:.1f} / 10")
    lines.append("")
    lines.append(f"**Status:** {badge}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Score Breakdown")
    lines.append("")
    lines.append(score_table)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Attention Points")
    lines.append("")
    lines.append(attention_md)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Agent Purpose")
    lines.append("")
    lines.append(f"**Purpose:** {data.get('purpose', '—')}")
    lines.append("")
    lines.append(f"**Use case:** {data.get('use_case', '—')}")
    lines.append("")
    lines.append(f"**Expected outcome:** {data.get('expected_outcome', '—')}")
    lines.append("")
    lines.append("## 2. Task Assignment")
    lines.append("")
    lines.append("**Tasks:**")
    lines.append(tasks_md)
    lines.append(f"**Priority defined:** {'Yes' if data.get('task_priority') else 'No'}  ")
    lines.append(f"**Dependencies identified:** {'Yes' if data.get('task_dependencies_defined') else 'No'}")
    lines.append("")
    lines.append("## 3. Context Management")
    lines.append("")
    lines.append(f"**Context size:** {data.get('context_size', '—')}  ")
    lines.append(f"**Input sources:** {data.get('context_sources', '—')}  ")
    lines.append(f"**Context strategy:** {'Yes' if data.get('context_strategy') else 'No'}")
    if data.get("context_strategy"):
        lines.append(f"**Strategy detail:** {data.get('context_strategy_detail', '—')}")
    lines.append("")
    lines.append("## 4. Data Sensitivity")
    lines.append("")
    lines.append(f"**Sensitivity level:** {data.get('data_sensitivity_level', '—')}  ")
    lines.append(f"**Data types:** {data.get('data_types', '—')}  ")
    lines.append(f"**PII procedures:** {'Yes' if data.get('pii_handling') else 'No'}  ")
    lines.append(f"**Handling procedures documented:** {'Yes' if data.get('data_handling_procedures') else 'No'}  ")
    lines.append(f"**Retention policy:** {'Yes' if data.get('data_retention_policy') else 'No'}")
    lines.append("")
    lines.append("## 5. Human Oversight")
    lines.append("")
    lines.append(f"**Oversight model:** {data.get('oversight_model', '—')}  ")
    lines.append(f"**Escalation triggers defined:** {'Yes' if data.get('review_triggers') else 'No'}")
    if triggers_md:
        lines.append(f"**Triggers:**")
        lines.append(triggers_md.rstrip())
    lines.append(f"**Escalation path documented:** {'Yes' if data.get('escalation_path') else 'No'}  ")
    lines.append(f"**Approval gates:** {'Yes' if data.get('approval_gates') else 'No'}")
    lines.append("")
    lines.append("## 6. Error Handling")
    lines.append("")
    lines.append(f"**Fallback defined:** {'Yes' if data.get('fallback_behavior') else 'No'}")
    if data.get("fallback_behavior"):
        lines.append(f"**Fallback detail:** {data.get('fallback_detail', '—')}")
    lines.append(f"**Retry policy:** {'Yes' if data.get('retry_policy') else 'No'}  ")
    lines.append(f"**Alerting configured:** {'Yes' if data.get('alerting_configured') else 'No'}  ")
    lines.append(f"**Graceful degradation:** {'Yes' if data.get('graceful_degradation') else 'No'}")
    lines.append("")
    lines.append("## 7. Scope Boundaries")
    lines.append("")
    lines.append("**Agent must NOT:**")
    lines.append(scope_md.rstrip())
    lines.append("")
    lines.append(f"**Allow-list defined:** {'Yes' if data.get('allowed_actions') else 'No'}  ")
    lines.append(f"**Deny-list defined:** {'Yes' if data.get('denied_actions') else 'No'}")
    lines.append("")
    lines.append("## 8. FinOps & Token Usage")
    lines.append("")
    lines.append(f"**Model:** {data.get('model_name', '—')}  ")
    lines.append(f"**Token budget per invocation:** {data.get('token_budget') or 'Not defined'}  ")
    cost_alert = f"${data.get('cost_alert_threshold')}" if data.get('cost_alert_threshold') else 'Not defined'
    lines.append(f"**Monthly cost alert:** {cost_alert}  ")
    lines.append(f"**Model selection rationale documented:** {'Yes' if data.get('model_selection_rationale') else 'No'}  ")
    lines.append(f"**Usage tracking plan:** {'Yes' if data.get('usage_tracking_plan') else 'No'}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Logging Tags (JSON)")
    lines.append("")
    lines.append("Attach these tags to your observability/logging pipeline to enable structured metrics.")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(tags, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("### Quick-start: logging integration")
    lines.append("")
    lines.append("Use the `logging_events` keys to instrument your agent code:")
    lines.append("")

    # Build the code sample
    tags_subset = {k: v for k, v in tags.items() if k != "logging_events" and k != "section_scores"}
    agent_id = tags.get("agent_name", "agent")
    code_sample = f'''```python
import logging, json, time

TAGS = {json.dumps(tags_subset, indent=4)}

logger = logging.getLogger("{agent_id}")

def run_agent():
    logger.info("{tags['logging_events']['agent_start']}", extra=TAGS)
    start = time.time()
    try:
        # ... your agent logic here ...
        tokens = 0  # replace with actual token count
        logger.info("{tags['logging_events']['tokens_used']}", extra={{**TAGS, "tokens": tokens}})
    except Exception as e:
        logger.error("{tags['logging_events']['agent_error']}", extra={{**TAGS, "error": str(e)}})
        raise
    finally:
        logger.info("{tags['logging_events']['agent_stop']}", extra={{**TAGS, "duration_s": time.time() - start}})
```'''
    lines.append(code_sample)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("_Generated by AI Agent Assessment Tool v1.0_")

    md = "\n".join(lines) + "\n"

    return md


# ─────────────────────────────────────────────
# Main flow
# ─────────────────────────────────────────────

def main():
    banner()
    print(f"  {DIM}This tool will guide you through 8 sections to assess whether")
    print(f"  your AI agent is well-defined enough for deployment.{RESET}")
    print(f"  {DIM}A scored report with logging tags will be generated at the end.{RESET}\n")

    # Collect all sections
    all_data = {}

    collectors = [
        collect_purpose,
        collect_tasks,
        collect_context,
        collect_data_sensitivity,
        collect_human_oversight,
        collect_error_handling,
        collect_scope,
        collect_finops,
    ]

    for collector in collectors:
        section_data = collector()
        all_data.update(section_data)

    # Score each section
    scores = {}
    for key, scorer in SCORERS.items():
        scores[key] = scorer(all_data)

    # Weighted overall score
    overall = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)

    # Generate tags
    tags = generate_tags(all_data, scores, overall)

    # Generate markdown
    md = generate_markdown(all_data, scores, overall, tags)

    # Determine output filename
    agent_name = all_data.get("agent_name", "unnamed-agent")
    safe_name = agent_name.lower().replace(" ", "-")
    filename = f"{safe_name}.md"
    output_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(output_dir, filename)

    # Write file
    with open(filepath, "w") as f:
        f.write(md)

    # Also write a companion JSON tags file
    tags_filepath = os.path.join(output_dir, f"{safe_name}-tags.json")
    with open(tags_filepath, "w") as f:
        json.dump(tags, f, indent=2)

    # Print summary
    badge_colored, badge_label = score_badge(overall)

    print(f"\n{SEPARATOR}")
    print(f"{BOLD}{CYAN}  Assessment Complete!{RESET}")
    print(SEPARATOR)
    print(f"\n  Agent:   {BOLD}{agent_name}{RESET}")
    print(f"  Score:   {BOLD}{overall:.1f} / 10{RESET}  {badge_colored}")
    print()

    # Print section scores
    for key in WEIGHTS:
        s = scores[key]
        badge_s, _ = score_badge(s)
        label = SECTION_LABELS[key]
        bar = "█" * s + "░" * (10 - s)
        print(f"  {label:<22} {bar}  {s}/10  {badge_s}")

    print()
    attention = generate_attention_points(all_data, scores)
    if attention:
        print(f"  {BOLD}{YELLOW}Attention Points:{RESET}")
        for a in attention:
            # Strip markdown bold for terminal
            clean = a.replace("**", "").replace("🔴", f"{RED}●{RESET}").replace("🟡", f"{YELLOW}●{RESET}").replace("⚠️", f"{YELLOW}⚠{RESET}")
            print(f"    {clean}")
        print()

    print(f"  {GREEN}✓{RESET} Report saved to:  {BOLD}{filepath}{RESET}")
    print(f"  {GREEN}✓{RESET} Tags saved to:    {BOLD}{tags_filepath}{RESET}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Assessment cancelled.{RESET}\n")
        sys.exit(1)
