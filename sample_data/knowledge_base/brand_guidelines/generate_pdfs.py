"""Generate 1 synthetic brand/proposal writing guide PDF for Meridian & Associates LLP."""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


class MeridianPDF(FPDF):
    """Base PDF class with firm branding."""

    def __init__(self, title, subtitle="", confidential=False, client_confidential=False):
        super().__init__()
        self.doc_title = title
        self.doc_subtitle = subtitle
        self.confidential = confidential
        self.client_confidential = client_confidential
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "Meridian & Associates LLP", align="L")
        if self.confidential:
            self.set_font("Helvetica", "B", 7)
            self.set_text_color(180, 0, 0)
            self.cell(0, 5, "CONFIDENTIAL", align="R")
        self.ln(8)
        self.set_draw_color(0, 51, 102)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(0, 51, 102)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")

    def cover_page(self, version="1.0", date="March 2026"):
        self.add_page()
        self.alias_nb_pages()
        self.set_fill_color(0, 51, 102)
        self.rect(0, 0, 210, 45, "F")
        self.set_y(12)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "MERIDIAN & ASSOCIATES LLP", align="C")
        self.ln(10)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, "Advisory | Assurance | Tax | Consulting", align="C")
        self.ln(30)
        self.set_text_color(0, 51, 102)
        self.set_font("Helvetica", "B", 26)
        self.multi_cell(0, 12, self.doc_title, align="C")
        if self.doc_subtitle:
            self.ln(4)
            self.set_font("Helvetica", "", 14)
            self.set_text_color(80, 80, 80)
            self.multi_cell(0, 8, self.doc_subtitle, align="C")
        self.ln(15)
        if self.confidential:
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(180, 0, 0)
            self.cell(0, 8, "CONFIDENTIAL", align="C")
            self.ln(6)
        self.ln(10)
        self.set_text_color(100, 100, 100)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, f"Version {version}  |  Effective Date: {date}", align="C")
        self.ln(6)
        self.cell(0, 6, "Meridian & Associates LLP  |  New York | Chicago | San Francisco | London | Singapore", align="C")
        self.ln(20)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(130, 130, 130)
        self.multi_cell(0, 4,
            "This document is the proprietary and confidential property of Meridian & Associates LLP. "
            "It is intended solely for the use of the designated recipient(s). Any unauthorized reproduction, "
            "distribution, or disclosure of this material is strictly prohibited.",
            align="C")

    def section_heading(self, text, level=1):
        if level == 1:
            self.ln(6)
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(0, 51, 102)
            self.cell(0, 8, text)
            self.ln(4)
            self.set_draw_color(0, 51, 102)
            self.line(10, self.get_y(), 120, self.get_y())
            self.ln(6)
        elif level == 2:
            self.ln(4)
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(51, 51, 51)
            self.cell(0, 7, text)
            self.ln(8)
        elif level == 3:
            self.ln(2)
            self.set_font("Helvetica", "BI", 10)
            self.set_text_color(80, 80, 80)
            self.cell(0, 6, text)
            self.ln(7)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.cell(8, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bold_bullet(self, label, text):
        self.set_text_color(40, 40, 40)
        self.set_font("Helvetica", "", 10)
        self.cell(8, 5.5, "-")
        self.set_font("Helvetica", "B", 10)
        w = self.get_string_width(label + ": ")
        self.cell(w, 5.5, label + ": ")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def key_value(self, key, value):
        self.set_text_color(40, 40, 40)
        self.set_font("Helvetica", "B", 10)
        w = self.get_string_width(key + ": ")
        self.cell(w, 5.5, key + ": ")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, value)
        self.ln(1)


# ============================================================================
# 1. Proposal Writing Guide
# ============================================================================

def generate_proposal_writing_guide():
    pdf = MeridianPDF(
        "Proposal Writing Guide",
        "Voice, Tone, Formatting, and Best Practices",
        confidential=True
    )
    pdf.cover_page(version="6.0", date="January 2026")

    # --- Introduction ---
    pdf.add_page()
    pdf.section_heading("1. Introduction and Purpose")
    pdf.body_text(
        "This Proposal Writing Guide establishes the standards for all written proposals, responses "
        "to requests for proposals (RFPs), statements of qualifications (SOQs), and related business "
        "development documents produced by Meridian & Associates LLP. Adherence to these guidelines "
        "ensures consistency, professionalism, and alignment with our brand identity across all markets "
        "and service lines."
    )
    pdf.body_text(
        "Every proposal is an expression of our brand promise. Whether responding to a $50,000 tax "
        "compliance engagement or a $50 million enterprise transformation program, the quality of our "
        "written communication directly influences how clients perceive our capabilities and commitment. "
        "Studies of our win/loss data consistently show that proposal quality -- clarity of writing, "
        "relevance of content, and visual presentation -- is among the top three factors cited by "
        "evaluators in their scoring rationale."
    )
    pdf.body_text(
        "This guide is mandatory for all Meridian professionals involved in proposal development. "
        "The Pursuit Management Office (PMO) reviews all proposals exceeding $500,000 in estimated "
        "fees for compliance with these guidelines before submission."
    )

    # --- Voice & Tone ---
    pdf.add_page()
    pdf.section_heading("2. Voice and Tone")
    pdf.section_heading("2.1 The Meridian Voice", level=2)
    pdf.body_text(
        "The Meridian voice is confident but not arrogant, knowledgeable but not condescending, "
        "and warm but not informal. We write as trusted advisors who genuinely care about our clients' "
        "success -- because we do. Our voice should convey that we have been there before, we understand "
        "the challenges, and we have the expertise and commitment to deliver results."
    )
    pdf.section_heading("Core Voice Attributes", level=3)
    pdf.bold_bullet("Authoritative", "We speak from experience. Use specific metrics, named methodologies, and concrete examples rather than vague claims. Say 'Our team has delivered 28 ERP implementations for health systems' not 'We have extensive ERP experience.'")
    pdf.bold_bullet("Client-Centered", "Every section should answer the client's implicit question: 'Why does this matter to me?' Lead with the client's needs and challenges, then explain how Meridian addresses them. The word 'you/your' should appear more frequently than 'we/our.'")
    pdf.bold_bullet("Forthright", "Be honest about challenges, risks, and trade-offs. Clients value candor. If a timeline is aggressive, say so and explain how we manage the risk. Never promise what we cannot deliver.")
    pdf.bold_bullet("Collaborative", "Use language that positions Meridian as a partner, not a vendor. Phrases like 'working alongside your team,' 'in close collaboration with,' and 'our joint approach' reinforce the partnership model.")
    pdf.bold_bullet("Outcome-Oriented", "Focus on results and value delivered, not just activities performed. Clients buy outcomes, not hours. Quantify impact whenever possible.")

    pdf.section_heading("2.2 Tone Calibration by Audience", level=2)
    pdf.body_text(
        "While the Meridian voice remains consistent, tone should be calibrated to the audience and context:"
    )
    pdf.bold_bullet("C-Suite / Board Level", "More strategic, concise, and business-outcome focused. Minimize technical jargon. Lead with ROI and strategic impact. Use executive summary formats.")
    pdf.bold_bullet("Procurement / Evaluation Committee", "Precise, structured, and directly responsive to evaluation criteria. Mirror the RFP's language and structure. Make it easy to score.")
    pdf.bold_bullet("Technical Evaluators", "Detailed, technically rigorous, and methodology-focused. Demonstrate depth of expertise. Use appropriate technical terminology (but define acronyms).")
    pdf.bold_bullet("Public Sector", "Formal, compliance-oriented, and responsive to stated requirements. Follow the RFP structure exactly. Reference relevant standards, regulations, and experience with similar government entities.")
    pdf.bold_bullet("Private Sector / Commercial", "Slightly more conversational, innovation-focused, and competitive. Emphasize speed, flexibility, and value. Industry-specific language is appropriate.")

    # --- Approved Language ---
    pdf.add_page()
    pdf.section_heading("3. Approved Language and Terminology")

    pdf.section_heading("3.1 Firm Name Usage", level=2)
    pdf.body_text(
        "The firm name should be written consistently throughout all proposals:"
    )
    pdf.bullet("Full name on first reference: 'Meridian & Associates LLP'")
    pdf.bullet("Subsequent references: 'Meridian' (preferred) or 'the firm' (when contextually clear)")
    pdf.bullet("Never abbreviate as 'M&A' (confusion with mergers & acquisitions), 'MAL,' or 'MALLP'")
    pdf.bullet("Never use 'Meridian Associates' (missing ampersand) or 'Meridian and Associates' (ampersand required)")
    pdf.bullet("In legal or contractual sections: always use the full name 'Meridian & Associates LLP'")

    pdf.section_heading("3.2 Service Line Naming", level=2)
    pdf.body_text("Always use the official service line names:")
    pdf.bold_bullet("Correct", "Audit & Assurance (not 'Audit Services' or 'External Audit')")
    pdf.bold_bullet("Correct", "Tax Services (not 'Tax Practice' or 'Tax Division')")
    pdf.bold_bullet("Correct", "Advisory & Consulting (not 'Consulting Services' or 'Management Consulting')")
    pdf.bold_bullet("Correct", "Risk Advisory (not 'Risk Consulting' or 'Risk Management Services')")
    pdf.bold_bullet("Correct", "Financial Advisory (not 'Transaction Services' or 'Deal Advisory')")

    pdf.section_heading("3.3 Phrases to Use", level=2)
    pdf.bullet("'Meridian's approach is designed to...' (positions our methodology as intentional)")
    pdf.bullet("'Based on our experience serving [X] similar organizations...' (demonstrates relevance)")
    pdf.bullet("'We will work in close collaboration with your team to...' (emphasizes partnership)")
    pdf.bullet("'Our proven methodology has delivered measurable results, including...' (outcome-focused)")
    pdf.bullet("'We bring a unique combination of [industry expertise] and [technical capability]...' (differentiator)")
    pdf.bullet("'Meridian is committed to...' (appropriate for quality, timelines, and values statements)")
    pdf.bullet("'Our team includes [X] professionals with [specific credential]...' (concrete capability)")

    pdf.section_heading("3.4 Phrases to Avoid", level=2)
    pdf.bullet("'We are the best/leading/premier firm...' (unsubstantiated superlatives)")
    pdf.bullet("'We are uniquely qualified...' (overused; prove it with facts instead)")
    pdf.bullet("'Best-in-class' (cliche; use specific metrics instead)")
    pdf.bullet("'Synergies' (business jargon; say 'efficiencies,' 'cost savings,' or 'combined benefits')")
    pdf.bullet("'Leverage' as a verb (use 'use,' 'apply,' 'draw on,' or 'build on')")
    pdf.bullet("'Touch base,' 'circle back,' 'deep dive' (informal business slang)")
    pdf.bullet("'Disruptive' or 'game-changing' (tech startup language, not appropriate for professional services)")
    pdf.bullet("'Resources' when referring to people (use 'professionals,' 'team members,' or 'specialists')")
    pdf.bullet("'Low-hanging fruit' (cliche; say 'immediate opportunities' or 'quick wins')")
    pdf.bullet("'Holistic' (overused; say 'comprehensive,' 'integrated,' or 'end-to-end')")

    # --- Formatting Standards ---
    pdf.add_page()
    pdf.section_heading("4. Formatting Standards")

    pdf.section_heading("4.1 Document Structure", level=2)
    pdf.body_text("Every proposal should follow this standard structure, unless the RFP specifies otherwise:")
    pdf.bullet("Cover Page -- branded, with client name, RFP reference, and submission date")
    pdf.bullet("Table of Contents -- auto-generated, with page numbers")
    pdf.bullet("Cover Letter -- personalized, signed by the engagement partner, 1-2 pages maximum")
    pdf.bullet("Executive Summary -- 2-3 pages, readable as a standalone document")
    pdf.bullet("Understanding of Requirements -- demonstrate we have listened and understood the client's needs")
    pdf.bullet("Approach and Methodology -- how we will deliver, with phase descriptions and timelines")
    pdf.bullet("Team Qualifications -- bios of key team members with relevant experience highlighted")
    pdf.bullet("Relevant Experience -- 3-5 case studies directly relevant to the client's situation")
    pdf.bullet("Project Management and Governance -- communication plans, escalation procedures, reporting")
    pdf.bullet("Fee Proposal -- clear pricing with assumptions, inclusions, and exclusions")
    pdf.bullet("Appendices -- resumes, certifications, insurance certificates, references (as requested)")

    pdf.section_heading("4.2 Typography", level=2)
    pdf.bullet("Body text: 10-11pt, Helvetica or Calibri, dark gray (#333333)")
    pdf.bullet("Section headings: 14pt bold, Meridian Blue (#003366)")
    pdf.bullet("Sub-headings: 12pt bold, dark gray (#333333)")
    pdf.bullet("Line spacing: 1.15 - 1.25x for body text")
    pdf.bullet("Margins: 1 inch (25mm) all sides minimum")
    pdf.bullet("Page numbers: bottom center, italicized, 8pt")

    pdf.section_heading("4.3 Visual Elements", level=2)
    pdf.bullet("Use Meridian Blue (#003366) as the primary accent color for headings and rules")
    pdf.bullet("Secondary color: Meridian Gray (#666666) for supporting elements")
    pdf.bullet("Accent color: Meridian Gold (#C5960C) sparingly for highlights and callouts")
    pdf.bullet("Charts and diagrams should use the approved color palette (available in the Brand Toolkit)")
    pdf.bullet("Include the firm logo on the cover page and in the header of subsequent pages")
    pdf.bullet("Photography: use approved firm photography or licensed stock imagery (no generic clip art)")

    pdf.section_heading("4.4 Data Presentation", level=2)
    pdf.bullet("Quantify claims whenever possible: 'served 120+ municipal clients' not 'extensive municipal experience'")
    pdf.bullet("Use tables for comparative information (team qualifications, pricing, timelines)")
    pdf.bullet("Use callout boxes for key differentiators or important statistics")
    pdf.bullet("Present timelines as visual Gantt charts or milestone diagrams, not just text lists")
    pdf.bullet("Round numbers appropriately: use '120+' not '123' for general claims; use exact figures for specific metrics")

    # --- Proposal Structure Best Practices ---
    pdf.add_page()
    pdf.section_heading("5. Section-by-Section Best Practices")

    pdf.section_heading("5.1 Cover Letter", level=2)
    pdf.body_text(
        "The cover letter is often the first substantive text an evaluator reads. It must accomplish "
        "three things in 1-2 pages: (1) demonstrate understanding of the client's situation and needs, "
        "(2) convey why Meridian is the right partner, and (3) express genuine enthusiasm for the opportunity."
    )
    pdf.bullet("Address the letter to the named contact in the RFP, using their correct title")
    pdf.bullet("Open with a reference to the specific RFP number and title")
    pdf.bullet("Mention 1-2 specific aspects of the client's situation that resonate with our experience")
    pdf.bullet("Name the proposed engagement partner and provide a brief credential highlight")
    pdf.bullet("Close with a call to action and direct contact information")
    pdf.bullet("Must be signed (wet signature on original, electronic signature acceptable if specified)")

    pdf.section_heading("5.2 Executive Summary", level=2)
    pdf.body_text(
        "The executive summary must stand alone as a compelling document. Many senior evaluators "
        "read only the executive summary and the pricing section. It should tell a complete story "
        "in 2-3 pages."
    )
    pdf.bullet("Start with the client's challenge, not with Meridian's qualifications")
    pdf.bullet("Present our approach as a clear, logical response to the stated challenge")
    pdf.bullet("Highlight 3-5 key differentiators with supporting evidence")
    pdf.bullet("Include a brief reference to relevant experience (1-2 sentences per case study)")
    pdf.bullet("Close with a value statement: what the client will achieve by selecting Meridian")
    pdf.bullet("Avoid excessive detail -- the executive summary should make the reader want to read more")

    pdf.section_heading("5.3 Approach and Methodology", level=2)
    pdf.body_text(
        "This section is where we demonstrate technical depth and differentiation. It should answer: "
        "'How will Meridian actually do this work, and why is that approach better than alternatives?'"
    )
    pdf.bullet("Organize by phases with clear descriptions of activities, deliverables, and duration")
    pdf.bullet("Explain the 'why' behind our methodology, not just the 'what'")
    pdf.bullet("Reference proprietary tools, frameworks, and accelerators by name (Meridian Insight, TaxConnect, etc.)")
    pdf.bullet("Include a visual timeline or roadmap -- evaluators remember visuals more than text")
    pdf.bullet("Address risk management explicitly: what could go wrong and how we prevent/mitigate it")
    pdf.bullet("Tailor the methodology to the client's specific situation, not a generic boilerplate")

    pdf.section_heading("5.4 Team Qualifications", level=2)
    pdf.body_text(
        "Clients buy people, not firms. The team section is consistently rated as one of the most "
        "important evaluation criteria."
    )
    pdf.bullet("Lead with the engagement partner and describe their personal commitment to the engagement")
    pdf.bullet("For each team member: name, title, years of experience, relevant certifications, and 2-3 directly relevant engagement examples")
    pdf.bullet("Include a team organization chart showing reporting relationships and client interaction points")
    pdf.bullet("Highlight continuity: if the proposed team has worked together before, say so")
    pdf.bullet("Address accessibility: how often will the partner be on-site or available?")
    pdf.bullet("Include professional photos for partner and manager level (per firm photography guidelines)")

    pdf.add_page()
    pdf.section_heading("5.5 Relevant Experience / Case Studies", level=2)
    pdf.body_text(
        "Case studies should be directly relevant to the prospect's industry, size, and challenge. "
        "Generic case studies signal that we have not invested effort in understanding the client."
    )
    pdf.bullet("Select 3-5 case studies that closely mirror the prospect's situation")
    pdf.bullet("Structure each case study as: Challenge > Approach > Results")
    pdf.bullet("Quantify results wherever possible (percentages, dollar amounts, time savings)")
    pdf.bullet("Name the client if permitted; use descriptive industry identifiers if blinded ('a Top-10 US bank')")
    pdf.bullet("Include the engagement partner and duration for credibility")
    pdf.bullet("If offering references, confirm with the reference contact before including their name")

    pdf.section_heading("5.6 Fee Proposal", level=2)
    pdf.body_text(
        "Pricing transparency builds trust. Present fees clearly and anticipate questions about value."
    )
    pdf.bullet("Present fees in the format requested by the RFP (fixed, T&M, blended rates, etc.)")
    pdf.bullet("Clearly state what is included and excluded from the fee")
    pdf.bullet("If offering a fixed fee, state the assumptions upon which it is based")
    pdf.bullet("Present the fee in context of value delivered, not just cost")
    pdf.bullet("Address travel and expense policies explicitly")
    pdf.bullet("If the fee is competitive, say so with market context; if premium, justify with value differentiation")

    # --- Do's and Don'ts ---
    pdf.add_page()
    pdf.section_heading("6. Proposal Do's and Don'ts")

    pdf.section_heading("DO", level=2)
    pdf.bullet("Read the entire RFP before writing a single word -- understand the evaluation criteria and weight them accordingly")
    pdf.bullet("Mirror the RFP's language and structure in your response (if they say 'work plan,' don't call it 'methodology')")
    pdf.bullet("Answer every question asked -- unanswered questions are scored as zero")
    pdf.bullet("Use the client's name throughout -- never submit a proposal with another client's name (our #1 disqualification error)")
    pdf.bullet("Include page numbers, RFP reference number, and firm name on every page")
    pdf.bullet("Have someone outside the engagement team proofread the proposal before submission")
    pdf.bullet("Start writing early -- rushed proposals show, and evaluators notice")
    pdf.bullet("Include a compliance matrix mapping each RFP requirement to the corresponding proposal section")
    pdf.bullet("Use active voice: 'Meridian will conduct...' not 'An analysis will be conducted...'")
    pdf.bullet("Submit early -- at least 24 hours before the deadline for electronic, 48 hours for physical delivery")

    pdf.section_heading("DON'T", level=2)
    pdf.bullet("Don't use boilerplate without customization -- evaluators can tell, and it signals lack of investment")
    pdf.bullet("Don't exceed page limits or formatting requirements (automatic disqualification in many evaluations)")
    pdf.bullet("Don't include irrelevant case studies just to fill space")
    pdf.bullet("Don't use acronyms without defining them on first use")
    pdf.bullet("Don't make claims you cannot substantiate with specific evidence")
    pdf.bullet("Don't disparage competitors by name -- differentiate through our strengths, not their weaknesses")
    pdf.bullet("Don't include team members who are not genuinely available for the engagement")
    pdf.bullet("Don't bury the lead -- put the most important information first in every section")
    pdf.bullet("Don't use passive voice when describing Meridian's actions ('will be delivered' vs 'we will deliver')")
    pdf.bullet("Don't submit without a final quality check using the Proposal Quality Checklist (Appendix A of this guide)")

    # --- Quality Checklist ---
    pdf.add_page()
    pdf.section_heading("7. Pre-Submission Quality Checklist")
    pdf.body_text(
        "Every proposal must pass the following quality checks before submission. For proposals exceeding "
        "$500,000 in estimated fees, the Pursuit Management Office (PMO) conducts this review. For smaller "
        "proposals, the engagement partner is responsible."
    )

    pdf.section_heading("Content Quality", level=2)
    pdf.bullet("All RFP questions and requirements have been addressed")
    pdf.bullet("Client name is correct throughout (search for any prior client names from reused content)")
    pdf.bullet("RFP reference number is correct on cover page, headers, and cover letter")
    pdf.bullet("Executive summary is compelling and can stand alone")
    pdf.bullet("Approach section is tailored to this specific client, not generic")
    pdf.bullet("Case studies are relevant to the client's industry and challenge")
    pdf.bullet("Team members are available and committed for the proposed engagement dates")
    pdf.bullet("Fee proposal is complete, accurate, and internally consistent")
    pdf.bullet("All claims are substantiated with specific evidence")

    pdf.section_heading("Formatting and Presentation", level=2)
    pdf.bullet("Compliant with all RFP formatting requirements (page limits, margins, font size)")
    pdf.bullet("Consistent formatting throughout (headings, fonts, spacing, numbering)")
    pdf.bullet("Table of contents is accurate and page numbers are correct")
    pdf.bullet("All cross-references ('as described in Section 3') are accurate")
    pdf.bullet("Images, charts, and tables are high-resolution and properly labeled")
    pdf.bullet("Firm logo and branding are correctly applied")

    pdf.section_heading("Technical Quality", level=2)
    pdf.bullet("Reviewed by a subject matter expert in the relevant service line")
    pdf.bullet("Pricing reviewed and approved by the engagement partner and practice leader")
    pdf.bullet("Risk assessment completed and documented in the Pursuit Approval System")
    pdf.bullet("Independence and conflict checks completed and cleared")
    pdf.bullet("Engagement letter terms reviewed by Office of the General Counsel (for fees > $1M)")

    pdf.section_heading("Final Delivery", level=2)
    pdf.bullet("Delivery format matches RFP requirements (PDF, hard copy, portal upload, etc.)")
    pdf.bullet("Electronic file size is within any stated limits")
    pdf.bullet("Delivery address and recipient name are confirmed")
    pdf.bullet("Submission deadline is confirmed, including time zone")
    pdf.bullet("Backup delivery plan is in place for physical submissions")

    pdf.section_heading("8. Resources and Support")
    pdf.body_text(
        "The Pursuit Management Office (PMO) provides centralized support for proposal development:"
    )
    pdf.bullet("Proposal writers and editors available for engagements > $1M (request 10+ business days in advance)")
    pdf.bullet("Graphic design support for custom visuals, infographics, and presentation materials")
    pdf.bullet("Content library with pre-approved firm descriptions, case studies, and team bios (Meridian ProposalHub)")
    pdf.bullet("Past proposal archive with win/loss analysis and evaluator feedback")
    pdf.bullet("Proposal coaching and win theme development workshops")
    pdf.bullet("Post-submission debrief facilitation for all pursuits > $500K")
    pdf.ln(4)
    pdf.body_text(
        "Contact the PMO:\n"
        "Email: proposals@meridian-llp.com\n"
        "Phone: (212) 555-0175\n"
        "Meridian ProposalHub: https://proposalhub.meridian-llp.com (internal only)"
    )

    pdf.output(os.path.join(OUTPUT_DIR, "proposal_writing_guide.pdf"))
    print("  Created: proposal_writing_guide.pdf")


if __name__ == "__main__":
    generate_proposal_writing_guide()
    print("\nProposal writing guide PDF generated successfully!")
