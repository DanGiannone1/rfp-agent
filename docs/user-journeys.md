# RFP Agent — User Journeys

Validated against a live session using `MD_RFP_SUBSET.pdf`. Screenshots taken at each step.

---

## Getting Started: Upload to Chat

1. **User opens the app.** They see a centered card "Upload RFP to Start" with a dashed drop zone. The drop zone immediately shows "Preparing your session... · This usually takes a few seconds." while the backend allocates a session.

2. **Once ready**, the drop zone shows "Drop an RFP file here · or click to choose from your device."

3. **User drops or selects a PDF.** The drop zone changes to:
   > "Converting document... · Processing MD_RFP_SUBSET.pdf · Large documents can take 1–2 minutes to process."

   The user waits. No progress bar — just this message. For the test PDF (47 MB) this took about 60 seconds.

4. **Chat opens automatically.** The full chat interface appears with:
   - Header: "Meridian Platform · Agentic RFP Response System" with session ID badge, idle indicator, file count, and "New chat" button
   - Center: A card with "RFP uploaded. What should we do first? · Pick a starting point or type your own request."
   - Four suggestion buttons in a 2×2 grid:
     - **Compliance matrix** — "Extract mandatory requirements into a compliance matrix."
     - **Bid / no-bid** — "Run a bid/no-bid score across six dimensions."
     - **Executive summary** — "Draft a one-page executive summary with win themes."
     - **Risk analysis** — "List top delivery risks and mitigation actions."
   - Right sidebar: "SOURCE DOCUMENTS · 1" showing the uploaded file with a green ✓ checkmark and "GENERATED ARTIFACTS · 0" with empty state text.
   - Bottom: Input bar with placeholder "Ask for requirements, strategy, compliance, pricing..."

---

## Skill 1: Requirements Extraction

**Trigger:** Click "Compliance matrix" chip, or type "Extract mandatory requirements into a compliance matrix."

**Thinking state:** User sees their message right-aligned, then a "Thinking ···" indicator with three animated dots below the agent avatar.

**Tool badges visible while working:**
- "Read file" passes — agent finds and reads the RFP markdown
- Multiple "Read file" passes — reading different sections
- "Ran command" — agent runs bash to process requirements

**What streams into chat:**
The agent announces it is compiling requirements into a CSV compliance matrix, then saves it. Final message is something like:
> "Compiled the extracted mandatory requirements into a CSV compliance matrix and saving it to the workspace."
> "Saved `compliance_matrix_mandatory.csv` with 29 mandatory requirements extracted from MD_RFP_SUBSET.pdf. Would you like me to add compliance status and response cross-references next?"

**What appears in the panel:**
- `compliance_matrix_mandatory.csv` (≈40 KB) under GENERATED ARTIFACTS
- Canvas auto-opens showing the CSV rendered as a table with columns: Req_ID, Section, Requirement, Mandatory, Compliance

**Correction from original doc:** File is a **CSV**, not a `.md`. Filename is `compliance_matrix_mandatory.csv`, not `compliance-matrix.md`.

---

## Skill 2: Bid/No-Bid Analysis

**Trigger:** Click "Bid / no-bid" chip, or type "Run a bid/no-bid score across six dimensions."

**What streams into chat:**
Agent generates a 6-dimension bid/no-bid scorecard CSV and a summary markdown. Final message example:
> "Saved `bid_no_bid_scorecard.csv` and `bid_no_bid_summary.md` with a total score of 42/100 — No-Bid as primary recommendation. Consider subcontract/IDIQ role. Want me to adjust weights/scores based on inside knowledge of our capability stack or client strategy?"

**What appears in the panel:**
- `bid_no_bid_scorecard.csv` (1.5 KB) — the scored table
- `bid_no_bid_summary.md` (875 B) — narrative summary and recommendation
- Previous artifacts remain listed below

**Correction from original doc:** Produces **two files**, not one. Both a scorecard CSV and a summary markdown.

---

## Skill 3: Executive Summary

**Trigger:** Click "Executive summary" chip, or type "Draft a one-page executive summary with win themes."

**Tool badges visible:**
- "Searching knowledge base" — agent queries KB for firm overview, case studies, approved language
- "Read file" — reads RFP sections
- "Edited file" — writes the summary

**What streams into chat:**
Agent drafts the summary and asks for refinement:
> "I'll draft a one-page executive summary grounded in the RFP and referenced KB sources, then save it as `executive_summary.md`."
> "Saved `executive_summary.md` with win themes and KB-backed rationale. Want me to tailor it to specific evaluation factors (e.g., MBE/SDVOB participation, pricing posture, or a 90-day Transition-In timeline)?"

**What appears in the panel:**
- `executive_summary.md` (43 KB) — auto-opens in canvas, rendered as formatted markdown prose with sections and a key differentiators table

---

## Skill 4: Risk & Gap Analysis

**Trigger:** Click "Risk analysis" chip, or type "List top delivery risks and mitigation actions."

**What streams into chat:**
Agent produces a risk register and offers next steps:
> "Saved `risk_register.csv` with 11 top risks, each with likelihood, impact, severity, owners, and mitigations. Highlights include SLA-related SLAA, MD THINK integration risk, access/security controls, scope creep, and BCDR. Want me to tailor severities to your environment or map each risk to specific contract sections?"

**What appears in the panel:**
- `risk_register.csv` (31 KB) — auto-opens in canvas as a table with columns: risk ID, category, description, likelihood, severity, score, owner, mitigation

**Correction from original doc:** File is a **CSV**, not `.md`. Filename is `risk_register.csv`.

---

## Skill 5: Response Strategy

**Trigger:** Type "Develop a response strategy and win themes."

**Tool badges visible:**
- "Searching knowledge base" — multiple queries for competitive positioning, win themes, client history
- "Read file" — reads RFP evaluation criteria sections
- "Edited file" — saves strategy brief

**What streams into chat:**
> "Drafting a concise response strategy brief with 5 win themes, pricing posture, and capture actions; then saving it as `response_strategy.md` and tagging the file."
> "Saved `response_strategy.md` with strategy, five win themes, pricing posture, and capture actions. Want me to tailor it to specific evaluation criteria (e.g., based goals, MBE goals) or convert the 90-day plan into a timeline?"

**What appears in the panel:**
- `response_strategy.md` (39 KB) — auto-opens in canvas

---

## Skill 6: Draft Generation

**Trigger:** Type "Draft the technical approach section."

**Tool badges visible:**
- "Read file" — reads requirements matrix, strategy brief, and RFP
- "Searching knowledge base" — queries for past technical approaches, methodology language
- "Edited file" — writes the draft

**What streams into chat:**
> "Drafted and saved `technical_approach.md` covering architecture, transition in, integrations, QA/compliance, security. Want me to tailor it to specific subsections to sections or map each subsection to RFP section numbers?"

**What appears in the panel:**
- `technical_approach.md` (45 KB) — largest file generated so far, auto-opens in canvas as formatted markdown

---

## Skill 7: Compliance Review

**Trigger:** Type "Run a compliance review on all drafted sections."

**Tool badges visible:**
- "Finding files" — inventories all workspace files
- "Searching files" — greps for TBD, TODO, placeholder text across all drafts
- "Searching files" — checks terminology consistency
- "Read file" — reads compliance matrix as baseline

**What streams into chat:**
Agent reviews all sections and saves a compliance report.

**What appears in the panel:**
- `compliance_review.md` (20 KB) — auto-opens in canvas

**⚠️ Rate limit warning:** In a long session where all 10 skills are run back-to-back, the agent may hit Azure OpenAI rate limits. When this happens the chat shows:
> "Execution failed: CAPIError: Too Many Requests"

This appears as visible text in the chat. The agent may still produce partial output or a file before this error. **For a demo, allow 30–60 seconds between skills, or run skills across separate sessions.**

---

## Skill 8: Pricing Analysis

**Trigger:** Type "Run a pricing analysis and build a cost model."

**Tool badges visible:**
- "Searching knowledge base" — queries for rate cards, past engagement pricing, margin guidance
- "Read file" — reads RFP scope and pricing requirements
- "Ran command" — builds cost model calculations

**What streams into chat:**
> "Saved `pricing_analysis.md` and `cost_model.csv` with baseline staffing, assumptions, and sensitivity scenarios. Want me to tune the model with actual call volumes/FTEs or add Year 1–3 pricing trajectories and incentive bands?"

**What appears in the panel:**
- `pricing_analysis.md` (18 KB) — narrative pricing strategy
- `cost_model.csv` (878 B) — bottom-up cost table

**⚠️ Rate limit warning:** Same as Skill 7 — may fail with "Too Many Requests" if run immediately after previous skills. If it fails, retrying the same prompt usually succeeds.

---

## Skill 9: Customer Intelligence

**Trigger:** Type "Build a customer intelligence briefing for this client."

**Tool badges visible (this skill runs the most KB searches):**
- "Searching knowledge base · '[client name]'"
- "Searching knowledge base · '[client name] engagement'"
- "Searching knowledge base · '[client name] proposal'"
- "Searching knowledge base · 'case study [industry]'"
- Multiple additional KB queries

**What streams into chat:**
> "Saved `customer_intelligence.md`. Want me to tune the model with actual call volumes or add Year 1–3 pricing trajectories?"

**What appears in the panel:**
- `customer_intelligence.md` (2.2 KB) — client briefing with relationship history, pain points, decision-making insights, and personalization recommendations

---

## Skill 10: Iterative Refinement

**Trigger:** Type "Check consistency across all sections and generate an org chart."

**Tool badges visible:**
- "Finding files" — inventories all generated files (13 at this point)
- "Searching files" — cross-checks terminology, names, dates
- "Read file" — reads multiple section files
- "Edited file" — saves consistency report and org chart

**What streams into chat:**
> "Saved `consistency_check.md` and `org_chart.md` based on cross-section term checks and `cost_model.csv` staffing. Want me to add SIN cross-references to sections or adjust the org chart for alternate staffing scenarios?"

**What appears in the panel:**
- `consistency_check.md` (1.2 KB) — list of consistency issues found across all drafts
- `org_chart.md` (670 B) — text-based team hierarchy
- 13 total generated artifacts now visible in the panel

---

## Accumulated Artifacts After Full Session

After running all 10 skills, the panel shows 13 generated artifacts (newest at top):

| File | Size | Skill |
|------|------|-------|
| `consistency_check.md` | 1.2 KB | 10 |
| `org_chart.md` | 670 B | 10 |
| `cost_model.csv` | 878 B | 8 |
| `customer_intelligence.md` | 2.2 KB | 9 |
| `pricing_analysis.md` | 18 KB | 8 |
| `compliance_review.md` | 20 KB | 7 |
| `technical_approach.md` | 45 KB | 6 |
| `response_strategy.md` | 39 KB | 5 |
| `risk_register.csv` | 31 KB | 4 |
| `executive_summary.md` | 43 KB | 3 |
| `bid_no_bid_scorecard.csv` | 1.5 KB | 2 |
| `bid_no_bid_summary.md` | 875 B | 2 |
| `compliance_matrix_mandatory.csv` | 40 KB | 1 |

---

## New Chat (Starting Over)

User clicks "New chat" in the top-right corner. If messages or files are present, a confirmation appears: "Start a new chat? This will clear current messages and uploaded context." On confirm, the chat history clears, the file panel empties, and the upload screen returns. The agent has no memory of the previous conversation.

---

## Known Issues

| Issue | Impact | Workaround |
|-------|--------|------------|
| Rate limit errors ("Execution failed: CAPIError: Too Many Requests") appear in chat when running many skills back-to-back | Visible error text in chat; skill may produce partial output | Wait 30–60s between skills, or retry the same prompt |
| Session lost on page refresh | User returns to intake screen and must re-upload | Planned fix: session restore from sessionStorage |
| Chat upload (second file) has no progress feedback during 30–60s CU conversion | User sees only a small spinner — no "converting" message | Planned fix: inline assistant message during conversion |
