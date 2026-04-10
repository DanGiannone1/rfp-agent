---
name: draft-generation
description: Generate proposal sections using RFP requirements and knowledge base sources; use when asked to draft or write sections.
---

# Proposal Section Draft Generation

## Purpose

Generate polished draft content for individual proposal sections by combining knowledge base materials (past proposals, boilerplate, case studies) with new writing tailored to the specific RFP opportunity. Every draft should be submission-ready in tone and structure.

## When to Use

- User asks to "draft", "write", or "generate" a proposal section
- After requirements extraction and response strategy are established, if those artifacts already exist
- When the user provides a section topic (e.g., "draft the technical approach" or "write the past performance section")
- When assembling a complete proposal from individual sections

## Step-by-Step Process

### 1. Understand the Section Scope

Start with the uploaded RFP itself. Do not block on a requirements matrix or strategy brief if the user asked you to draft and the RFP is already available.

Read the RFP directly to determine what this section must cover — don't rely solely on the requirements matrix. Extract:
- Which RFP requirements map to this section (cross-reference the matrix if one exists)
- Evaluation criteria relevant to this section and their relative weights
- Page limits or format constraints
- Any specific instructions from the RFP (e.g., "describe your methodology in no more than 5 pages")

### 2. Search Knowledge Base for Relevant Content

Use `knowledge_base_retrieve` with targeted queries to find:
- **Past proposal language** for similar sections (search by section name + service type)
- **Boilerplate descriptions** of Meridian & Associates LLP capabilities, methodologies, and service lines
- **Case studies** and past performance narratives relevant to the engagement type
- **Personnel bios** and qualifications for key staff
- **Approved technical language** for methodologies, frameworks, and approaches
- **Certifications and accreditations** relevant to the requirements
- **Client testimonials** or metrics from similar engagements

Run multiple searches with different query terms to maximize coverage. For example:
- `"audit methodology approach"` for a technical approach section
- `"[client industry] case study past performance"` for past performance
- `"key personnel partner manager qualifications"` for staffing sections

### 3. Review Working Directory Files

Use `read_full_file` to review:
- Previously drafted sections that should be consistent with this one, if present
- Win themes or strategy brief to align messaging, if present
- RFP-specific requirements that must be addressed
- Uploaded reference documents from the user

Do not create or wait for prerequisite artifacts before drafting. Use existing artifacts when they add value; otherwise draft directly from the RFP plus KB evidence.

### 4. Draft the Section

Compose the section following these principles:
- **Lead with the client's need**, not Meridian's capabilities
- **Incorporate win themes** established in the response strategy
- **Address every mapped requirement** explicitly — use compliance language ("Meridian will...", "Our approach includes...")
- **Cite evidence**: Reference specific past engagements, metrics, and qualifications from KB materials
- **Use active voice** and confident, professional tone
- **Include visuals guidance**: Note where tables, diagrams, or graphics would strengthen the section
- **Respect page limits**: Be concise; every paragraph should earn its space

### 5. Add Source Citations

At the end of the draft, list the KB sources referenced so the user can verify and trace content origin.

### 6. Save Output

Save the completed draft to the working directory as `[section_name]_draft.md` (e.g., `technical_approach_draft.md`, `past_performance_draft.md`) so the user can download it and it appears in the artifacts panel.

### 7. Flag Gaps

Note any areas where:
- KB materials were insufficient and original content was generated
- Specific data points, metrics, or names need to be verified
- Subject matter expert input is recommended
- Graphics or attachments are needed

## Output Format

```markdown
## [Section Title]

[Draft content organized with clear headings, subheadings, and logical flow]

### [Subsection as needed]

[Content incorporating KB materials, tailored to this RFP]

| [Tables where appropriate for clarity] |
|---|
| [Data, timelines, team structures, etc.] |

---

### Source References

The following knowledge base materials were referenced in this draft:
1. [Source document name / description] — used for [what content]
2. [Source document name / description] — used for [what content]

### Content Gaps & Action Items

- [ ] [Gap: specific metric needs verification]
- [ ] [Gap: SME review needed for technical claim]
- [ ] [Gap: graphic/diagram needed for process flow]
- [ ] [Gap: client-specific customization needed in paragraph X]
```

## Tools to Use

- **knowledge_base_retrieve**: Primary tool — search for past proposals, boilerplate, case studies, personnel bios, methodology descriptions, and approved language. Run multiple queries with varied search terms.
- **read_full_file**: Read RFP requirements, previously drafted sections, strategy briefs, and uploaded reference materials end-to-end
