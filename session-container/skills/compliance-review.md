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

### 6. Tone and Quality Review

Assess the overall proposal for:
- **Professionalism**: Appropriate for a Meridian & Associates LLP submission
- **Client focus**: More "you/your" than "we/our" language
- **Confidence**: Assertive but not arrogant
- **Specificity**: Claims supported by evidence, not vague promises
- **Readability**: Clear, concise, free of jargon where possible
- **Grammar and spelling**: Basic proofreading
- **Active voice**: Preferred over passive constructions

### 7. Generate Compliance Checklist

Compile findings into a structured checklist with pass/fail/warning status.

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

### Tone & Quality Assessment

| Criterion | Rating | Notes |
|---|:---:|---|
| Professional tone | Good / Fair / Poor | [Notes] |
| Client focus | Good / Fair / Poor | [Notes] |
| Specificity of claims | Good / Fair / Poor | [Notes] |
| Grammar/spelling | Good / Fair / Poor | [Notes] |
| Readability | Good / Fair / Poor | [Notes] |

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
- **knowledge_base_retrieve**: Verify claims against actual past performance data, personnel qualifications, and firm credentials
