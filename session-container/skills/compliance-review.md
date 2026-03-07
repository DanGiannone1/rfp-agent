# Compliance Review

## Purpose

Perform a systematic quality and compliance check on the draft proposal before submission. Verify that every mandatory requirement is addressed, submission instructions are followed, terminology is consistent, no sensitive data is exposed, and the tone is appropriate throughout.

## When to Use

- After all proposal sections have been drafted
- User asks for a "compliance review", "quality check", "submission review", or "final review"
- Before finalizing and submitting the proposal
- When the user wants to verify completeness against RFP requirements

## Step-by-Step Process

### 1. Load the Requirements Matrix

Read the previously generated compliance matrix (if available) or re-extract mandatory requirements from the RFP. This is the primary checklist for the review.

Use `bash` and `glob` to find the requirements matrix and all drafted sections in the working directory.

### 2. Requirement Coverage Check

For each mandatory requirement:
- Search all drafted sections using `grep` to verify the requirement is addressed
- Confirm the response is substantive (not just a passing mention)
- Check that the response uses compliance language ("Meridian will...", "Our approach ensures...")
- Flag any mandatory requirements with no corresponding response content

### 3. Submission Instructions Compliance

Check the RFP's administrative/submission requirements:
- **Format**: Page limits, font size, margin requirements, file format
- **Structure**: Required section order, naming conventions, numbering
- **Required forms**: Certifications, representations, signature pages, attachments
- **Copies**: Number of copies, electronic submission requirements
- **Deadline**: Submission date, time, and method
- **Labeling**: How packages/files should be labeled

### 4. Consistency Check

Review across all sections for:
- **Terminology**: Consistent use of client name, project name, technical terms
- **Team names/titles**: Personnel names and titles match across sections
- **Dates and timelines**: No conflicting dates or schedules
- **Pricing references**: Amounts mentioned in narrative match pricing section
- **Acronyms**: Defined on first use, used consistently thereafter
- **Cross-references**: Internal references point to correct sections
- **Win themes**: Consistently reflected throughout the proposal

### 5. Sensitive Data Review

Scan for content that should not be in a proposal:
- Internal cost data or margin information
- Competitor names (should use "other firms" or similar)
- Draft/placeholder language ("TBD", "INSERT HERE", "TODO", "[PLACEHOLDER]")
- Personal information beyond what's required (SSNs, personal phone numbers)
- Proprietary client information from other engagements
- Internal strategy notes or comments not meant for the client

Use `grep` to search for common markers: "TBD", "TODO", "PLACEHOLDER", "DRAFT", "INSERT", "XXX", "???".

### 6. Branding & Formatting Check

Verify the proposal meets Meridian's presentation standards:
- **Firm name**: "Meridian & Associates LLP" used consistently (not abbreviated or varied)
- **Boilerplate accuracy**: Firm overview, methodology descriptions match approved language from KB
- **Formatting consistency**: Heading hierarchy, numbering scheme, table styles are uniform
- **Visual standards**: Any brand colors, logo placement, or style guidelines are followed
- **Document structure**: Table of contents (if applicable), page numbers, headers/footers, section breaks
- **Page limits**: Total page count and per-section limits comply with RFP requirements

Use `knowledge_base_retrieve` to search for "brand guidelines", "style guide", and "proposal formatting" for approved standards.

### 7. Tone and Quality Review

Assess the overall proposal for:
- **Professionalism**: Appropriate for a Meridian & Associates LLP submission
- **Client focus**: More "you/your" than "we/our" language
- **Confidence**: Assertive but not arrogant
- **Specificity**: Claims supported by evidence, not vague promises
- **Readability**: Clear, concise, free of jargon where possible
- **Grammar and spelling**: Basic proofreading
- **Active voice**: Preferred over passive constructions

### 8. Executive Review Readiness

Prepare a sign-off checklist for leadership review:
- **Strategy alignment**: Does the proposal reflect the agreed win themes and positioning?
- **Pricing approval**: Has the proposed fee been reviewed and approved by the engagement partner?
- **Commitment accuracy**: Are all commitments (timelines, deliverables, staffing) achievable?
- **Legal review**: Have any exceptions to terms, representations, or liability clauses been flagged?
- **Risk acceptance**: Are identified risks acknowledged with appropriate mitigations?

Flag each item as Ready / Needs Review / Blocked and identify the responsible person.

### 9. Generate Compliance Checklist

Compile findings into a structured checklist with pass/fail/warning status.

### 9b. Verify Claims Against Knowledge Base

Before finalizing, use `knowledge_base_retrieve` to spot-check key claims in the drafted proposal:
- Any cited past performance metrics or client outcomes — confirm they appear in KB records
- Personnel qualifications and certifications referenced — verify they match KB personnel files
- Firm credentials, registrations, or accreditations mentioned — confirm they are current per KB compliance docs

Flag any claim that cannot be verified in the KB as needing human confirmation before submission.

### 10. Save Output

Save the compliance review report to the working directory as `compliance_review.md` so the user can download it and it appears in the artifacts panel.

## Output Format

```markdown
## Compliance Review Report

**RFP:** [Title / Number]
**Review Date:** [Date]
**Sections Reviewed:** [List]

### Overall Status: [PASS / PASS WITH WARNINGS / FAIL]

### Requirement Coverage

| Req ID | Requirement | Section Addressed | Status | Notes |
|---|---|---|:---:|---|
| REQ-001 | [Requirement] | Technical Approach, p3 | PASS | Fully addressed |
| REQ-002 | [Requirement] | Key Personnel, p7 | WARN | Partially addressed — missing [detail] |
| REQ-003 | [Requirement] | — | FAIL | Not addressed in any section |

**Coverage Summary:** [X] of [Y] mandatory requirements addressed ([Z]%)

### Submission Instructions Compliance

| Requirement | Status | Notes |
|---|:---:|---|
| Page limit (X pages) | PASS | Current: [N] pages |
| Required sections present | PASS | All [N] required sections included |
| Required forms/attachments | WARN | [Missing form/attachment] |
| File format | PASS | |
| Deadline acknowledged | PASS | [Date/time] |

### Consistency Issues

| Issue | Location | Severity | Suggested Fix |
|---|---|:---:|---|
| [Inconsistent term] | Sections 2, 4 | Medium | Standardize to "[preferred term]" |
| [Date mismatch] | Sections 3, 5 | High | Verify correct date |

### Sensitive Content Findings

| Finding | Location | Severity | Action Required |
|---|---|:---:|---|
| [Placeholder text found] | Section 2, para 3 | High | Replace with final content |
| [Internal note] | Section 4 | High | Remove before submission |

### Branding & Formatting Compliance

| Requirement | Status | Notes |
|---|:---:|---|
| Firm name consistency | PASS/FAIL | |
| Approved boilerplate used | PASS/WARN | [Deviations noted] |
| Heading/numbering consistency | PASS/WARN | |
| Page limits met | PASS/FAIL | [Current: X pages, Limit: Y] |
| Headers/footers/TOC | PASS/WARN | |

### Tone & Quality Assessment

| Criterion | Rating | Notes |
|---|:---:|---|
| Professional tone | Good / Fair / Poor | [Notes] |
| Client focus | Good / Fair / Poor | [Notes] |
| Specificity of claims | Good / Fair / Poor | [Notes] |
| Grammar/spelling | Good / Fair / Poor | [Notes] |
| Readability | Good / Fair / Poor | [Notes] |

### Executive Review Readiness

| Item | Status | Responsible | Notes |
|---|:---:|---|---|
| Strategy alignment | Ready / Needs Review | [Name] | |
| Pricing approval | Ready / Needs Review | [Name] | |
| Commitment review | Ready / Needs Review | [Name] | |
| Legal/terms review | Ready / Needs Review | [Name] | |
| Risk acceptance | Ready / Needs Review | [Name] | |

### Action Items (Priority Order)

1. **[CRITICAL]** [Action needed]
2. **[HIGH]** [Action needed]
3. **[MEDIUM]** [Action needed]
4. **[LOW]** [Action needed]
```

## Tools to Use

- **grep**: Primary tool — search for requirement keywords across all drafted sections; scan for placeholder text, sensitive data markers, and inconsistencies
- **bash / glob**: List and read all proposal files and RFP documents
- **str_replace_editor**: Read specific sections for detailed review
- **knowledge_base_retrieve**: Verify that specific claims in the proposal — past performance metrics, personnel qualifications, certifications, case study outcomes — are accurate and traceable to real KB records. Also check approved brand guidelines and firm language for branding compliance.
