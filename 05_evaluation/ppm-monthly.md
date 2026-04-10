# Agent Assessment: ppm-monthly

**Date:** 2026-04-10 10:45 UTC  
**Owner:** Digital department  
**Model:** local LLM

---

## Overall Score: 4.6 / 10

**Status:** 🟡 AMBER — Needs attention and improvements

---

## Score Breakdown

| Section | Score | Status |
|---|---|---|
| Agent Purpose | 10/10 | 🟢 Green |
| Task Assignment | 8/10 | 🟢 Green |
| Context Management | 8/10 | 🟢 Green |
| Data Sensitivity | 3/10 | 🔴 Red |
| Human Oversight | 3/10 | 🔴 Red |
| Error Handling | 0/10 | 🔴 Red |
| Scope Boundaries | 2/10 | 🔴 Red |
| FinOps & Token Usage | 0/10 | 🔴 Red |


---

## Attention Points

- 🔴 **Data Sensitivity** (score: 3/10) — Critical: not sufficient to proceed
- 🔴 **Human Oversight** (score: 3/10) — Critical: not sufficient to proceed
- 🔴 **Error Handling** (score: 0/10) — Critical: not sufficient to proceed
- 🔴 **Scope Boundaries** (score: 2/10) — Critical: not sufficient to proceed
- 🔴 **FinOps & Token Usage** (score: 0/10) — Critical: not sufficient to proceed
- ⚠️ **No token budget defined** — Risk of uncontrolled costs


---

## 1. Agent Purpose

**Purpose:** fill monthly budget file, based on Excel input

**Use case:** monthly budget tracking

**Expected outcome:** all budget lines as filled, for a full month

## 2. Task Assignment

**Tasks:**
  1. read an Excel file (input)
  2. Start from top, represents a developer account
  3. Connect to planisware (account to be defined)
  4. Each developer has a number of BC line (project assignments), and is aligned witht the Excel file. Fill all the hours from Excel in the Planisware. Each day has max 8 hours, and all the hours should be divided over the full month, often 21 or 22 days
  5. After each week is filled in Planisware, 40 hours should be validated and saved.
  6. Repeat this until all accounts (developers) in the Excel sheet are done. Logout from Planisware

**Priority defined:** Yes  
**Dependencies identified:** No

## 3. Context Management

**Context size:** small  
**Input sources:** API  
**Context strategy:** No

## 4. Data Sensitivity

**Sensitivity level:** Internal  
**Data types:** Time registration  
**PII procedures:** No  
**Handling procedures documented:** No  
**Retention policy:** No

## 5. Human Oversight

**Oversight model:** Human-on-the-loop (monitoring with intervention capability)  
**Escalation triggers defined:** No
**Escalation path documented:** No  
**Approval gates:** No

## 6. Error Handling

**Fallback defined:** No
**Retry policy:** No  
**Alerting configured:** No  
**Graceful degradation:** No

## 7. Scope Boundaries

**Agent must NOT:**
  - continue or retrying after 10 contiguous errors

**Allow-list defined:** No  
**Deny-list defined:** No

## 8. FinOps & Token Usage

**Model:** local LLM  
**Token budget per invocation:** Not defined  
**Monthly cost alert:** Not defined  
**Model selection rationale documented:** No  
**Usage tracking plan:** No

---

## Logging Tags (JSON)

Attach these tags to your observability/logging pipeline to enable structured metrics.

```json
{
  "agent_name": "ppm-monthly",
  "agent_purpose": "monthly budget tracking",
  "agent_owner": "Digital department",
  "agent_model": "local LLM",
  "agent_assessment_score": 4.6,
  "agent_assessment_status": "AMBER",
  "agent_data_sensitivity": "Internal",
  "agent_oversight_model": "Human-on-the-loop",
  "agent_context_size": "small",
  "agent_token_budget": "undefined",
  "agent_cost_alert_usd": "undefined",
  "logging_events": {
    "agent_start": "ppm-monthly.start",
    "agent_stop": "ppm-monthly.stop",
    "agent_error": "ppm-monthly.error",
    "agent_escalation": "ppm-monthly.escalation",
    "tokens_used": "ppm-monthly.tokens_used",
    "agent_fallback": "ppm-monthly.fallback",
    "agent_cost": "ppm-monthly.cost"
  },
  "section_scores": {
    "purpose": 10,
    "tasks": 8,
    "context": 8,
    "data_sensitivity": 3,
    "human_oversight": 3,
    "error_handling": 0,
    "scope_boundaries": 2,
    "finops": 0
  }
}
```

### Quick-start: logging integration

Use the `logging_events` keys to instrument your agent code:

```python
import logging, json, time

TAGS = {
    "agent_name": "ppm-monthly",
    "agent_purpose": "monthly budget tracking",
    "agent_owner": "Digital department",
    "agent_model": "local LLM",
    "agent_assessment_score": 4.6,
    "agent_assessment_status": "AMBER",
    "agent_data_sensitivity": "Internal",
    "agent_oversight_model": "Human-on-the-loop",
    "agent_context_size": "small",
    "agent_token_budget": "undefined",
    "agent_cost_alert_usd": "undefined"
}

logger = logging.getLogger("ppm-monthly")

def run_agent():
    logger.info("ppm-monthly.start", extra=TAGS)
    start = time.time()
    try:
        # ... your agent logic here ...
        tokens = 0  # replace with actual token count
        logger.info("ppm-monthly.tokens_used", extra={**TAGS, "tokens": tokens})
    except Exception as e:
        logger.error("ppm-monthly.error", extra={**TAGS, "error": str(e)})
        raise
    finally:
        logger.info("ppm-monthly.stop", extra={**TAGS, "duration_s": time.time() - start})
```

---

_Generated by AI Agent Assessment Tool v1.0_
