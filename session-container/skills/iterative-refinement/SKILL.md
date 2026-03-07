---
name: iterative-refinement
description: Guide iterative refinement, consistency checks, and collateral generation; use when asked to refine or polish.
---

# Iterative Refinement

## Purpose

Guide the collaborative editing cycle between the agent and human reviewers. Ensures cross-section consistency, helps generate supporting collateral (resumes, org charts, pricing tables), and tracks what has been reviewed vs. what still needs attention. This is the human-in-the-loop workflow that turns a first draft into a submission-ready proposal.

## When to Use

- After initial draft sections have been generated
- User asks to "refine", "polish", "review sections", "check consistency", or "improve" the proposal
- When assembling attachments and supporting materials
- When multiple sections need to be harmonized after separate drafting passes
- User asks for "collateral", "resumes", "org chart", or "pricing table"

## Step-by-Step Process

### 1. Assess Current State

Use `bash` and `glob` to inventory all files in the working directory:
- Which sections are drafted?
- Which sections are still missing or incomplete?
- Are there reviewer comments or feedback files?
- What attachments/collateral have been generated vs. still needed?

Present a status summary to the user showing what's done, what's in progress, and what's outstanding.

### 2. Cross-Section Consistency Check

Read all drafted sections and verify consistency across the full proposal:

**Terminology and naming:**
- Client name spelled identically everywhere
- Project/engagement name consistent
- Meridian & Associates LLP used correctly (not abbreviated inconsistently)
- Technical terms and acronyms used consistently

**Personnel references:**
- Names and titles match across all sections (executive summary, key personnel, staffing plan, org chart)
- Role descriptions are consistent
- No one is referenced in the narrative but absent from the team section

**Dates and timelines:**
- Start dates, milestones, and end dates align across narrative, schedule, and pricing
- No conflicting timeline references

**Pricing alignment:**
- Fee amounts in the executive summary match the pricing section
- Hours and rates are consistent between staffing plan and cost summary
- Any phased pricing references are consistent

**Win theme threading:**
- Verify that established win themes appear in every major section
- Check that the executive summary reflects themes from the technical approach
- Ensure the management approach reinforces capability claims

Use `grep` to search for key terms, personnel names, dates, and dollar amounts across all files.

### 3. Section-Level Refinement

For each section the user wants to improve:
- Read the current draft
- Identify weaknesses: vague claims, missing evidence, poor flow, passive voice, generic language
- Search `knowledge_base_retrieve` for additional supporting evidence, case studies, or approved language
- Propose specific improvements with tracked changes (use `str_replace_editor`)
- Flag items that need human decision (e.g., "Should we include the XYZ case study here?")

### 4. Collateral Generation

Generate supporting documents and attachments as needed:

**Personnel materials:**
- Key personnel resumes/bios (search KB for personnel records)
- Team organizational chart (text-based hierarchy)
- Staffing plan with roles, hours, and availability

**Project planning:**
- Project schedule / milestone timeline (markdown table)
- Work breakdown structure
- Deliverables list with dates

**Pricing materials:**
- Fee summary table
- Rate schedule
- Cost breakdown by phase or task

**Administrative:**
- Required forms checklist (extracted from RFP submission instructions)
- Certifications and representations list
- Reference list with contact information

For each collateral item, search the KB first for templates and existing content, then generate tailored output.

### 5. Track Review Status

Maintain a review tracker showing the status of each section and collateral item:

```markdown
| Section / Item | Status | Reviewer | Notes |
|---|:---:|---|---|
| Executive Summary | Draft Complete | — | Awaiting review |
| Technical Approach | Under Review | [User] | User editing Section 2.3 |
| Management Approach | Approved | [User] | Final |
| Key Personnel | Draft Complete | — | Need to confirm [name] availability |
| Pricing | In Progress | — | Waiting on subcontractor quote |
| Org Chart | Not Started | — | Depends on final team roster |
```

Update this tracker as the user provides feedback and approves sections.

### 6. Incorporate Feedback

When the user provides edits or feedback:
- Apply requested changes using `str_replace_editor`
- Verify that changes don't create inconsistencies with other sections
- Re-check cross-references and terminology after edits
- Confirm changes with the user before moving to the next section

## Output Format

```markdown
## Refinement Status Report

**RFP:** [Title / Number]
**Last Updated:** [Date/Time]

### Proposal Completeness

| Section | Status | Consistency Check | Notes |
|---|:---:|:---:|---|
| Executive Summary | Complete | PASS | Win themes reflected |
| Technical Approach | In Review | WARN | Timeline mismatch with Section 4 |
| Management Approach | Draft | PASS | |
| Key Personnel | Complete | PASS | |
| Past Performance | Draft | FAIL | References client name inconsistently |
| Pricing | In Progress | — | Not yet reviewed |

**Overall Progress:** [X] of [Y] sections complete ([Z]%)

### Consistency Issues Found

1. **[HIGH]** [Description] — Found in [locations]
   - **Fix:** [Proposed resolution]
2. **[MEDIUM]** [Description] — Found in [locations]
   - **Fix:** [Proposed resolution]

### Collateral Status

| Item | Status | Source | Notes |
|---|:---:|---|---|
| Team resumes (N) | [X] of [Y] complete | KB personnel records | Missing [name] |
| Org chart | Complete | Generated | |
| Project schedule | Draft | Generated | Needs milestone dates |
| Pricing table | Not started | — | Awaiting final rates |
| Required forms | Checklist ready | RFP Section [X] | [N] forms needed |

### Recommended Next Steps

1. [Highest-priority action]
2. [Next action]
3. [Next action]
```

### 7. Save Output

Save the refinement status report to the working directory as `refinement_status.md` so the user can track progress and it appears in the artifacts panel. Update this file each time the user provides feedback or sections are approved.

## Tools to Use

- **grep**: Search across all proposal files for terminology, names, dates, amounts, and win theme keywords to verify consistency
- **bash / glob**: Inventory all files, check word counts, identify missing sections
- **str_replace_editor**: Read and edit specific sections to apply refinements
- **knowledge_base_retrieve**: Search for additional evidence, personnel records, case studies, and approved language to strengthen weak sections
