"""
Generate 7 synthetic professional-services PDF documents for Meridian & Associates LLP.
Uses fpdf2 built-in fonts only (Helvetica, Times, Courier).
"""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

class MeridianPDF(FPDF):
    """Reusable PDF subclass with firm branding helpers."""

    doc_title = ""
    doc_subtitle = ""
    version = ""
    effective_date = ""

    def header(self):
        if self.page_no() == 1:
            return  # cover page handled manually
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, "CONFIDENTIAL -- Meridian & Associates LLP", align="L")
        self.cell(0, 5, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.line(10, 15, 200, 15)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(
            0, 5,
            "This document is proprietary and confidential. Unauthorized distribution is prohibited.",
            align="C",
        )

    def cover_page(self, title, subtitle, version, effective_date, doc_id):
        self.add_page()
        # Dark blue banner
        self.set_fill_color(0, 48, 87)
        self.rect(0, 0, 210, 60, "F")
        self.set_y(12)
        self.set_font("Helvetica", "B", 26)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, "MERIDIAN & ASSOCIATES LLP", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 11)
        self.cell(0, 7, "Audit & Assurance Practice", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

        # Title block
        self.set_y(75)
        self.set_text_color(0, 48, 87)
        self.set_font("Helvetica", "B", 22)
        self.multi_cell(0, 10, title, align="C")
        self.ln(3)
        self.set_font("Helvetica", "", 13)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 8, subtitle, align="C")

        # Metadata table
        self.ln(20)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        meta = [
            ("Document ID", doc_id),
            ("Version", version),
            ("Effective Date", effective_date),
            ("Classification", "CONFIDENTIAL"),
            ("Approved By", "National Assurance Quality Board"),
            ("Next Review", "January 2027"),
        ]
        col_w = 60
        val_w = 120
        for label, value in meta:
            self.set_font("Helvetica", "B", 10)
            self.cell(col_w, 7, label + ":", new_x="END")
            self.set_font("Helvetica", "", 10)
            self.cell(val_w, 7, value, new_x="LMARGIN", new_y="NEXT")

        # Confidential stamp
        self.ln(15)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(180, 0, 0)
        self.cell(0, 8, "CONFIDENTIAL", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(120, 120, 120)
        self.multi_cell(
            0, 5,
            "This document contains proprietary methodologies and procedures of Meridian & Associates LLP. "
            "It is intended solely for use by authorized personnel. Distribution outside the firm "
            "requires written approval from the National Managing Partner, Assurance Services.",
            align="C",
        )

    # Convenience writers -----------------------------------------------

    def section_heading(self, number, text):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 48, 87)
        self.cell(0, 9, f"{number}. {text}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 48, 87)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def sub_heading(self, number, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.cell(0, 7, f"{number} {text}", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self.set_font("Times", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, text)
        self.ln(1)

    def bullet(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 48, 87)
        self.cell(4, 5, "-")
        self.set_font("Times", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, "  " + text)
        self.ln(0.5)

    def bullet_list(self, items):
        for item in items:
            self.bullet(item)


# =====================================================================
# Document 1 -- Audit Transition Plan
# =====================================================================

def gen_audit_transition_plan():
    pdf = MeridianPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.cover_page(
        "Audit Engagement\nTransition Plan",
        "90-Day Roadmap for Predecessor Firm Transitions",
        "4.2",
        "March 1, 2026",
        "MA-AA-TP-2026-001",
    )

    # Page 2 -- Purpose & Scope
    pdf.add_page()
    pdf.section_heading("1", "Purpose and Scope")
    pdf.body(
        "This document establishes the standard framework for transitioning audit engagements "
        "from a predecessor firm to Meridian & Associates LLP. It is applicable to all SEC registrant "
        "and non-registrant audit transitions and is designed to ensure compliance with PCAOB AS 2610 "
        "(Initial Audits -- Communications Between Predecessor and Successor Auditors), SEC Rule 2-01 "
        "of Regulation S-X, and the firm's internal quality control standards."
    )
    pdf.body(
        "The 90-day roadmap is structured around four distinct phases, each with defined milestones, "
        "deliverables, responsible parties, and quality checkpoints. All transitions must be overseen "
        "by a National Office-approved engagement partner with a minimum of 15 years of relevant "
        "industry experience."
    )

    pdf.section_heading("2", "Phase I: Pre-Transition (Days 1-15)")
    pdf.sub_heading("2.1", "Predecessor Communications")
    pdf.body(
        "The engagement partner initiates formal communication with the predecessor auditor within "
        "48 hours of engagement acceptance. In accordance with PCAOB AS 2610.05, the successor auditor "
        "must make specific and reasonable inquiries of the predecessor regarding:"
    )
    pdf.bullet_list([
        "Information that might bear on the integrity of management, including fraud or illegal acts.",
        "Disagreements with management about accounting principles, audit procedures, or similarly significant matters.",
        "Communications to those charged with governance regarding fraud, illegal acts, and internal control-related matters.",
        "The predecessor's understanding of the reasons for the change in auditors.",
        "Significant findings or issues arising during the most recent audit, including critical audit matters.",
    ])

    pdf.sub_heading("2.2", "Regulatory Notifications")
    pdf.body(
        "For SEC registrants, the firm ensures timely compliance with the following regulatory requirements:"
    )
    pdf.bullet_list([
        "SEC Form 8-K Item 4.01 filing review: Confirm the registrant files within four business days of the auditor change, disclosing any reportable events or disagreements per Item 304(a) of Regulation S-K.",
        "PCAOB Form AP notification: Prepare engagement-level information for timely reporting once fieldwork commences.",
        "State board of accountancy notifications where required by jurisdiction.",
        "Notification to relevant professional liability insurance carriers regarding the new engagement.",
    ])

    pdf.sub_heading("2.3", "Engagement Acceptance and Risk Assessment")
    pdf.body(
        "Prior to finalizing the transition timeline, the following acceptance procedures are completed "
        "under the supervision of the Regional Assurance Leader and the National Risk Management Partner:"
    )
    pdf.bullet_list([
        "Client background investigation using the firm's proprietary MeridianCheck platform, including litigation history, regulatory sanctions, credit analysis, and media screening.",
        "Independence assessment across all member firms, subsidiaries, and affiliates, covering financial interests, business relationships, and employment of former firm personnel.",
        "Preliminary fee estimate based on risk profile, entity complexity, geographic scope, and specialist resource requirements.",
        "Engagement team conflict-of-interest screening through the Global Independence Compliance System (GICS).",
        "Anti-money laundering (AML) and Know Your Client (KYC) procedures for all engagement entities.",
    ])

    pdf.section_heading("3", "Phase II: Planning (Days 16-45)")
    pdf.sub_heading("3.1", "Risk Assessment and Audit Strategy")
    pdf.body(
        "The engagement team conducts a comprehensive risk assessment in accordance with PCAOB AS 2110 "
        "(Identifying and Assessing Risks of Material Misstatement). This includes obtaining an understanding "
        "of the entity's industry, regulatory environment, business operations, financial reporting "
        "framework, and internal control over financial reporting."
    )
    pdf.body(
        "Materiality thresholds are established in line with the firm's standard methodology: overall "
        "materiality at 5% of pre-tax income (or appropriate benchmark for the entity), performance "
        "materiality at 75% of overall materiality, and a de minimis threshold at 5% of overall "
        "materiality for evaluating identified misstatements."
    )

    pdf.sub_heading("3.2", "Team Mobilization")
    pdf.body(
        "The engagement partner, in consultation with the Regional Resource Manager, assembles the "
        "engagement team based on the following criteria:"
    )
    pdf.bullet_list([
        "Lead engagement partner: Minimum 15 years of experience, relevant industry specialization, prior transition experience required.",
        "Engagement quality reviewer (EQR): Independent partner with SEC registrant experience, appointed by the National Quality Board.",
        "Senior manager(s): Minimum 8 years of experience with at least 3 years in the client's industry vertical.",
        "IT audit specialists: CISA or CISSP certified, experienced with the client's ERP platform.",
        "Valuation, tax, actuarial, and forensic specialists: Assigned based on preliminary risk assessment results.",
    ])

    pdf.sub_heading("3.3", "System Access and Data Migration")
    pdf.body(
        "The IT integration team coordinates secure access to the client's systems and migrates prior-year "
        "audit documentation from the predecessor's working paper platform to MeridianAudit Suite. "
        "All data transfers comply with the firm's Information Security Policy (ISP-2025-003) and "
        "applicable data privacy regulations, including GDPR where relevant."
    )

    pdf.section_heading("4", "Phase III: Execution (Days 46-75)")
    pdf.sub_heading("4.1", "Opening Balance Verification")
    pdf.body(
        "In accordance with PCAOB AS 2610.10-.11 (Initial Audits -- Opening Balances), the engagement "
        "team performs sufficient procedures on opening balances to obtain reasonable assurance that:"
    )
    pdf.bullet_list([
        "Opening balances do not contain misstatements that materially affect the current period's financial statements.",
        "Appropriate accounting policies reflected in the opening balances have been consistently applied in the current period, or changes are properly accounted for and adequately disclosed.",
        "Prior-period closing balances have been correctly brought forward, or, where appropriate, restated.",
    ])

    pdf.sub_heading("4.2", "Interim Testing Procedures")
    pdf.body(
        "The team executes interim substantive and controls testing procedures. Particular emphasis "
        "is placed on areas identified during the risk assessment as higher risk in a first-year "
        "engagement, including revenue recognition (ASC 606), management estimates (ASC 820/ASC 350), "
        "and related party transactions. Journal entry testing covers 100% of entries using "
        "MeridianAI Analyze, as described in the firm's Technology Integration Framework."
    )

    pdf.section_heading("5", "Phase IV: Close-Out (Days 76-90)")
    pdf.sub_heading("5.1", "Management Letter and Communication")
    pdf.body(
        "The engagement partner prepares a comprehensive management letter addressing internal control "
        "observations, including significant deficiencies and material weaknesses identified during "
        "the transition audit. The letter follows the firm's standard template (Form MA-ML-001) and "
        "is reviewed by the EQR prior to issuance."
    )
    pdf.sub_heading("5.2", "Audit Committee Presentation")
    pdf.body(
        "A formal presentation to the audit committee (or those charged with governance) covers: "
        "the transition process summary, significant audit findings, critical audit matters, "
        "independence confirmation, required communications under PCAOB AS 1301, and the planned "
        "approach for the ongoing engagement relationship. The presentation deck follows the firm's "
        "standard template and is reviewed by the National Office prior to delivery."
    )

    pdf.sub_heading("5.3", "GANTT-Style Milestone Summary")
    pdf.body("The following summarizes key milestones and responsible parties across the 90-day plan:")
    milestones = [
        ("Days 1-3", "Engagement letter execution", "Engagement Partner"),
        ("Days 1-5", "Predecessor auditor inquiry letter sent", "Engagement Partner"),
        ("Days 3-10", "Independence clearance completed", "Independence Office"),
        ("Days 5-12", "Predecessor work paper access obtained", "Senior Manager"),
        ("Days 10-15", "SEC/PCAOB notification review", "National Office"),
        ("Days 16-25", "Risk assessment and materiality setting", "Engagement Partner"),
        ("Days 20-30", "Team mobilization and onboarding", "Resource Manager"),
        ("Days 25-40", "System access and data migration", "IT Audit Lead"),
        ("Days 30-45", "Audit strategy memorandum finalized", "Engagement Partner"),
        ("Days 46-55", "Opening balance verification", "Senior Manager"),
        ("Days 50-70", "Interim substantive testing", "Engagement Team"),
        ("Days 55-75", "Controls testing (ICFR)", "IT Audit / Senior Manager"),
        ("Days 76-82", "Management letter drafting", "Engagement Partner"),
        ("Days 80-88", "EQR review completed", "Quality Reviewer"),
        ("Days 85-90", "Audit committee presentation", "Engagement Partner"),
    ]
    # Simple table
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 48, 87)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(30, 6, "Timeline", border=1, fill=True)
    pdf.cell(85, 6, "Milestone", border=1, fill=True)
    pdf.cell(55, 6, "Responsible Party", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(30, 30, 30)
    for i, (timeline, milestone, party) in enumerate(milestones):
        fill = i % 2 == 0
        if fill:
            pdf.set_fill_color(235, 240, 248)
        pdf.cell(30, 5, timeline, border=1, fill=fill)
        pdf.cell(85, 5, milestone, border=1, fill=fill)
        pdf.cell(55, 5, party, border=1, fill=fill, new_x="LMARGIN", new_y="NEXT")

    pdf.output(os.path.join(OUTPUT_DIR, "audit_transition_plan.pdf"))
    print("  Created audit_transition_plan.pdf")


# =====================================================================
# Document 2 -- Risk-Based Audit Methodology
# =====================================================================

def gen_risk_based_methodology():
    pdf = MeridianPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.cover_page(
        "Risk-Based Audit\nMethodology",
        "Standard Approach for Planning and Executing Financial Statement Audits",
        "6.1",
        "January 15, 2026",
        "MA-AA-RM-2026-002",
    )

    pdf.add_page()
    pdf.section_heading("1", "Overview and Authoritative Framework")
    pdf.body(
        "This document codifies Meridian & Associates LLP's risk-based audit methodology for financial "
        "statement audits of both SEC registrants (conducted in accordance with PCAOB standards) and "
        "non-registrant entities (conducted in accordance with AICPA generally accepted auditing "
        "standards, i.e., Clarified Statements on Auditing Standards). The methodology is also aligned "
        "with the International Standards on Auditing (ISAs) issued by the International Auditing and "
        "Assurance Standards Board (IAASB) for engagements subject to those standards."
    )
    pdf.body(
        "The firm's approach is built upon the fundamental principle that audit effort should be "
        "directed toward areas of higher assessed risk of material misstatement. This risk-based "
        "allocation of resources ensures both audit quality and engagement efficiency."
    )

    pdf.section_heading("2", "Understanding the Entity and Its Environment")
    pdf.body(
        "In accordance with PCAOB AS 2110 and ISA 315 (Revised 2019), the engagement team obtains "
        "a thorough understanding of the entity and its environment, including:"
    )
    pdf.bullet_list([
        "Industry, regulatory, and other external factors, including the applicable financial reporting framework (e.g., U.S. GAAP, IFRS).",
        "The nature of the entity: its operations, ownership and governance structures, types of investments and investment activities, the way the entity is structured and financed.",
        "The entity's selection and application of accounting policies, including reasons for changes thereto. Whether the entity's accounting policies are appropriate for its business and consistent with the applicable financial reporting framework and industry practice.",
        "The entity's objectives and strategies, and related business risks that may result in material misstatement of the financial statements.",
        "The measurement and review of the entity's financial performance, including key performance indicators, analyst reports, and peer benchmarking data.",
    ])

    pdf.section_heading("3", "Identifying Significant Accounts and Relevant Assertions")
    pdf.body(
        "The engagement team identifies significant accounts and disclosures and their relevant "
        "assertions. An account or disclosure is considered significant if there is a reasonable "
        "possibility that the account or disclosure could contain a misstatement that, individually "
        "or when aggregated with other misstatements, could have a material effect on the financial "
        "statements. The relevant financial statement assertions are:"
    )
    pdf.bullet_list([
        "Existence or Occurrence: Assets, liabilities, and equity interests exist at the balance sheet date; transactions occurred during the period.",
        "Completeness: All transactions, assets, liabilities, and equity interests that should have been recorded have been recorded; all disclosures that should have been included have been included.",
        "Valuation or Allocation: Assets, liabilities, and equity interests are recorded at appropriate amounts and any resulting valuation or allocation adjustments are appropriately recorded.",
        "Rights and Obligations: The entity holds or controls the rights to assets, and liabilities are obligations of the entity at a given date.",
        "Presentation and Disclosure: Transactions, balances, and disclosures are properly classified, described, and disclosed in conformity with the applicable financial reporting framework.",
        "Accuracy: Amounts and other data relating to recorded transactions and events have been recorded appropriately, and related disclosures have been appropriately measured and described.",
        "Cutoff: Transactions and events have been recorded in the correct accounting period.",
    ])

    pdf.section_heading("4", "Risk Assessment: Inherent Risk and Control Risk")
    pdf.sub_heading("4.1", "Inherent Risk Assessment")
    pdf.body(
        "Inherent risk is assessed at the assertion level for each significant account and disclosure. "
        "The assessment considers the following inherent risk factors as specified in ISA 315 (Revised 2019):"
    )
    pdf.bullet_list([
        "Complexity: The degree of complexity in the underlying transactions, accounting requirements, or processes.",
        "Subjectivity: The degree to which the information required to determine the appropriate accounting treatment, or amounts and disclosures, is subject to management judgment or estimation.",
        "Change: The degree of change in the entity's operations, environment, or applicable financial reporting framework that affects the account or disclosure.",
        "Susceptibility to misstatement due to management bias or fraud: The degree to which the inherent risk factors of complexity, subjectivity, or change provide the conditions for management bias, whether intentional or unintentional, to exist.",
        "Uncertainty: The degree of estimation uncertainty associated with a financial statement line item or disclosure.",
    ])

    pdf.sub_heading("4.2", "Control Risk Assessment")
    pdf.body(
        "Control risk is assessed based on the engagement team's evaluation of the design and "
        "implementation of internal controls relevant to the audit. For integrated audits of SEC "
        "registrants (conducted under PCAOB AS 2201), the team also evaluates the operating "
        "effectiveness of internal control over financial reporting (ICFR) and issues an opinion on ICFR."
    )
    pdf.body(
        "The control risk assessment drives the nature, timing, and extent of further audit procedures. "
        "Where the team intends to rely on controls to reduce substantive testing, tests of controls "
        "are designed to obtain sufficient appropriate evidence about the operating effectiveness of "
        "those controls throughout the period under audit."
    )

    pdf.sub_heading("4.3", "Risk Assessment Matrix")
    pdf.body(
        "The firm utilizes a standardized Risk Assessment Matrix to classify the combined risk of "
        "material misstatement for each significant account-assertion combination. The matrix maps "
        "inherent risk (Low, Moderate, High, Very High) against control risk (Low, Moderate, High) "
        "to yield a combined risk rating that determines the required level of substantive audit evidence:"
    )
    # Risk matrix table
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 48, 87)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(40, 6, "", border=1, fill=True)
    pdf.cell(36, 6, "Control: Low", border=1, fill=True, align="C")
    pdf.cell(36, 6, "Control: Mod", border=1, fill=True, align="C")
    pdf.cell(36, 6, "Control: High", border=1, fill=True, align="C")
    pdf.ln()
    matrix_data = [
        ("Inherent: Low", "Low", "Low", "Moderate"),
        ("Inherent: Mod", "Low", "Moderate", "High"),
        ("Inherent: High", "Moderate", "High", "Very High"),
        ("Inherent: V. High", "High", "Very High", "Very High"),
    ]
    pdf.set_text_color(30, 30, 30)
    for i, (label, c1, c2, c3) in enumerate(matrix_data):
        fill = i % 2 == 0
        if fill:
            pdf.set_fill_color(235, 240, 248)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(40, 6, label, border=1, fill=fill)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(36, 6, c1, border=1, fill=fill, align="C")
        pdf.cell(36, 6, c2, border=1, fill=fill, align="C")
        pdf.cell(36, 6, c3, border=1, fill=fill, align="C")
        pdf.ln()
    pdf.ln(3)

    pdf.section_heading("5", "Materiality Determination")
    pdf.body(
        "Materiality is determined in accordance with PCAOB AS 2105 and ISA 320. The firm's standard "
        "benchmarks and percentages are as follows:"
    )
    pdf.sub_heading("5.1", "Overall Materiality")
    pdf.body(
        "Overall materiality is ordinarily set at 5% of pre-tax income from continuing operations. "
        "Alternative benchmarks may be used when pre-tax income is not a meaningful measure (e.g., "
        "for entities with volatile or near-break-even earnings). Approved alternative benchmarks include:"
    )
    pdf.bullet_list([
        "Revenue: 0.5% to 1% of total revenue (for entities where revenue is the primary performance measure).",
        "Total assets: 0.25% to 0.5% (for asset-intensive industries such as financial institutions or REITs).",
        "Net assets / equity: 1% to 2% (for not-for-profit entities or investment companies).",
        "Blended approach: weighted average of multiple benchmarks (requires National Office approval).",
    ])

    pdf.sub_heading("5.2", "Performance Materiality")
    pdf.body(
        "Performance materiality is set at 75% of overall materiality. This level is calibrated to "
        "reduce to an appropriately low level the probability that the aggregate of uncorrected and "
        "undetected misstatements exceeds overall materiality. For first-year engagements, or where "
        "prior-year audit adjustments or errors indicate elevated risk, performance materiality may "
        "be reduced to 50%-65% of overall materiality at the engagement partner's discretion."
    )

    pdf.sub_heading("5.3", "Clearly Trivial Threshold")
    pdf.body(
        "Misstatements below 5% of overall materiality are considered clearly trivial and need not "
        "be accumulated for purposes of evaluating the effect of uncorrected misstatements. However, "
        "misstatements that are qualitatively significant (e.g., related party transactions, management "
        "compensation, regulatory compliance) are accumulated regardless of amount."
    )

    pdf.section_heading("6", "Designing Audit Procedures")
    pdf.sub_heading("6.1", "Tests of Controls")
    pdf.body(
        "For engagements where a controls reliance strategy is adopted, the engagement team designs "
        "tests of controls to evaluate operating effectiveness. Sample sizes are determined using "
        "the firm's statistical sampling module within MeridianAudit Suite, considering the desired "
        "level of assurance, the expected deviation rate, and the tolerable rate of deviation."
    )

    pdf.sub_heading("6.2", "Substantive Procedures")
    pdf.body(
        "Substantive procedures include both substantive analytical procedures and tests of details. "
        "The nature, timing, and extent of substantive procedures are responsive to the assessed risks "
        "of material misstatement at the assertion level. For all significant accounts with a combined "
        "risk rating of 'High' or 'Very High,' the firm requires tests of details (substantive analytical "
        "procedures alone are not sufficient at those risk levels)."
    )
    pdf.body(
        "The firm's data analytics capabilities (see the Audit Technology Integration Framework, "
        "Document MA-AA-TI-2026-006) enable the engagement team to perform full-population testing "
        "of journal entries and automated three-way matching, supplementing traditional sampling-based "
        "approaches where appropriate."
    )

    pdf.section_heading("7", "Documentation Standards")
    pdf.body(
        "All risk assessments, materiality determinations, and audit strategies are documented in the "
        "firm's MeridianAudit Suite platform. Documentation must be sufficient to enable an experienced "
        "auditor, having no previous connection with the engagement, to understand the nature, timing, "
        "and extent of procedures performed, evidence obtained, and conclusions reached, as required by "
        "PCAOB AS 1215 and ISA 230."
    )

    pdf.output(os.path.join(OUTPUT_DIR, "risk_based_audit_methodology.pdf"))
    print("  Created risk_based_audit_methodology.pdf")


# =====================================================================
# Document 3 -- Independence and Conflict Policy
# =====================================================================

def gen_independence_policy():
    pdf = MeridianPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.cover_page(
        "Independence and\nConflict of Interest Policy",
        "SEC, PCAOB, and AICPA Independence Requirements\nfor Audit and Assurance Engagements",
        "8.0",
        "February 1, 2026",
        "MA-AA-IC-2026-003",
    )

    pdf.add_page()
    pdf.section_heading("1", "Purpose and Applicability")
    pdf.body(
        "This policy establishes the independence and conflict-of-interest requirements applicable to "
        "all partners, principals, and professional staff of Meridian & Associates LLP and its member "
        "firms. Independence is the foundation of the auditing profession and is essential to the "
        "credibility of audit reports. This policy implements the requirements of SEC Rule 2-01 of "
        "Regulation S-X, PCAOB Rule 3520 (Auditor Independence), AICPA Code of Professional Conduct "
        "ET Section 1.200, and the IESBA Code of Ethics."
    )
    pdf.body(
        "All personnel are required to read, understand, and acknowledge this policy annually. Violations "
        "may result in disciplinary action up to and including termination of employment and referral "
        "to regulatory authorities."
    )

    pdf.section_heading("2", "Financial Interest Restrictions")
    pdf.sub_heading("2.1", "Direct Financial Interests")
    pdf.body(
        "No partner, principal, or covered person (as defined below) may hold any direct financial "
        "interest in an audit client or an affiliate of an audit client. A direct financial interest "
        "includes ownership of stock, bonds, notes, or other securities, options, warrants, and similar "
        "instruments. This prohibition applies regardless of materiality."
    )

    pdf.sub_heading("2.2", "Indirect Financial Interests")
    pdf.body(
        "Indirect financial interests (e.g., through mutual funds, blind trusts, retirement plans) "
        "are prohibited when they are material to the covered person. An indirect financial interest "
        "is considered material when its value exceeds 5% of the covered person's total net worth or "
        "when the covered person can exercise control or significant influence over the investment vehicle."
    )

    pdf.sub_heading("2.3", "Covered Persons")
    pdf.body(
        "The term 'covered persons' encompasses the following categories, consistent with SEC Rule 2-01(f)(11):"
    )
    pdf.bullet_list([
        "The audit engagement team members, including the lead engagement partner, engagement quality reviewer, and all staff assigned to the engagement.",
        "The chain of command: any partner or manager in the direct supervisory chain above the engagement partner, up to and including the firm's CEO/Managing Partner.",
        "Any partner in the same office as the lead engagement partner who provides 10 or more hours of non-audit services to the audit client.",
        "Any partner who maintains a direct relationship with the audit client's CEO, CFO, CAO, controller, or equivalent.",
        "The firm itself, including its employee benefit plans, and any entity controlled by the firm or by covered persons.",
    ])

    pdf.section_heading("3", "Prohibited Non-Audit Services")
    pdf.body(
        "In accordance with Section 201 of the Sarbanes-Oxley Act of 2002 and SEC Rule 2-01(c)(4), "
        "the following non-audit services may not be provided to an audit client or an affiliate of "
        "an audit client that is an SEC registrant:"
    )
    pdf.bullet_list([
        "Bookkeeping or other services related to the accounting records or financial statements of the audit client.",
        "Financial information systems design and implementation.",
        "Appraisal or valuation services, fairness opinions, or contribution-in-kind reports.",
        "Actuarial services.",
        "Internal audit outsourcing services.",
        "Management functions or human resources services.",
        "Broker or dealer, investment adviser, or investment banking services.",
        "Legal services and expert services unrelated to the audit.",
        "Any other service that the PCAOB determines by regulation is impermissible.",
    ])
    pdf.body(
        "For non-registrant audit clients, the firm follows the AICPA independence rules, which are "
        "somewhat less restrictive but still prohibit services that place the firm in the position of "
        "auditing its own work or functioning as management of the client."
    )

    pdf.section_heading("4", "Pre-Approval of Permissible Non-Audit Services")
    pdf.body(
        "All non-audit services proposed for an audit client must receive advance written approval "
        "from the audit client's audit committee (or equivalent body) before the services commence. "
        "The firm's National Independence Office reviews each proposed service for compliance before "
        "submission to the client's audit committee. Pre-approval must address:"
    )
    pdf.bullet_list([
        "A description of the proposed service and its scope.",
        "The estimated fee and fee structure (fixed, hourly, or contingent).",
        "An analysis of the impact on independence, including threats and safeguards.",
        "Confirmation that the service does not fall within the prohibited categories listed in Section 3.",
        "Identification of the senior professional responsible for overseeing the non-audit service to ensure independence boundaries are maintained.",
    ])

    pdf.section_heading("5", "Employment and Cooling-Off Periods")
    pdf.body(
        "SEC Rule 2-01(c)(2)(iii)(B) requires a one-year cooling-off period before a member of the "
        "engagement team (or a partner in the chain of command) can accept a Financial Reporting "
        "Oversight Role (FROR) at an audit client. The firm extends this to a two-year cooling-off "
        "period as a matter of firm policy for any of the following positions:"
    )
    pdf.bullet_list([
        "Chief Executive Officer, President, or equivalent.",
        "Chief Financial Officer, Controller, Chief Accounting Officer, or equivalent.",
        "Director of Internal Audit or equivalent.",
        "Any board of directors or audit committee position.",
        "Any position with authority over financial reporting or accounting policies.",
    ])
    pdf.body(
        "Departing personnel must notify the National Independence Office at least 30 days prior to "
        "their intended departure date. The Independence Office assesses whether additional safeguards "
        "are required, including potential removal of the departing professional from the engagement "
        "team immediately upon notification."
    )

    pdf.section_heading("6", "Firm Rotation Requirements")
    pdf.body(
        "For SEC registrant audit clients, the lead engagement partner and the engagement quality "
        "review partner are subject to mandatory rotation after five consecutive years of service "
        "on the engagement, followed by a five-year cooling-off period, in accordance with PCAOB "
        "Rule 3211 and SEC Rule 2-01(c)(6). Additional rotation requirements apply to other "
        "partners providing significant services on the engagement."
    )
    pdf.body(
        "The firm's Partner Rotation Committee, chaired by the Vice Chair of Audit Quality, monitors "
        "all partner tenures and initiates transition planning at least 18 months before a required "
        "rotation event. See the Audit Partner Rotation Policy (Document MA-AA-PR-2026-004) for "
        "detailed procedures."
    )

    pdf.section_heading("7", "Annual Independence Confirmations")
    pdf.body(
        "All partners and professional staff are required to complete an annual independence "
        "confirmation through the Global Independence Compliance System (GICS). The confirmation "
        "requires disclosure of:"
    )
    pdf.bullet_list([
        "All brokerage accounts, investment holdings, and retirement plan investments.",
        "Immediate family members' employment and financial interests.",
        "All outside business relationships, board memberships, and advisory roles.",
        "Loan and borrowing arrangements with financial institution audit clients.",
        "Any known relationships that could create a threat to independence.",
    ])
    pdf.body(
        "Confirmations are due within 30 days of the fiscal year-end (March 31) and must be updated "
        "within 10 business days of any material change in circumstances. The Independence Office "
        "reviews 100% of partner confirmations and a risk-based sample of staff confirmations."
    )

    pdf.section_heading("8", "Partner Compensation Safeguards")
    pdf.body(
        "To ensure that independence is not compromised by financial incentives, the firm's partner "
        "compensation system includes the following safeguards:"
    )
    pdf.bullet_list([
        "Audit quality metrics (including PCAOB inspection results, internal review findings, and restatement history) constitute no less than 25% of the engagement partner's performance evaluation.",
        "Revenue or fee growth metrics may not exceed 15% of the partner's overall compensation determination.",
        "Cross-selling incentives for non-audit services to audit clients are expressly prohibited.",
        "A quality-related clawback provision allows the firm to recoup previously distributed compensation in the event of material audit failures.",
    ])

    pdf.section_heading("9", "Business Relationship Restrictions")
    pdf.body(
        "The firm prohibits business relationships between covered persons and audit clients that "
        "could reasonably be expected to create a mutual financial interest or place the firm in "
        "an advocacy position. Restricted relationships include:"
    )
    pdf.bullet_list([
        "Joint business ventures, partnership interests, or joint investments with audit clients or their officers, directors, or significant shareholders.",
        "Cooperative arrangements with audit clients for marketing, product development, or service delivery.",
        "Reciprocal referral arrangements that create financial interdependence.",
        "Contingent fee arrangements for any service provided to an audit client.",
        "Loans to or from audit clients (except permitted banking relationships under SEC Rule 2-01(c)(1)(ii)).",
    ])

    pdf.output(os.path.join(OUTPUT_DIR, "independence_and_conflict_policy.pdf"))
    print("  Created independence_and_conflict_policy.pdf")


# =====================================================================
# Document 4 -- Audit Partner Rotation Policy
# =====================================================================

def gen_partner_rotation():
    pdf = MeridianPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.cover_page(
        "Audit Partner\nRotation Policy",
        "Mandatory Rotation, Cooling-Off, and Transition Procedures\nfor SEC Registrant Engagements",
        "5.3",
        "January 1, 2026",
        "MA-AA-PR-2026-004",
    )

    pdf.add_page()
    pdf.section_heading("1", "Regulatory Foundation")
    pdf.body(
        "This policy implements the mandatory audit partner rotation requirements established by "
        "Section 203 of the Sarbanes-Oxley Act of 2002, SEC Rule 2-01(c)(6) of Regulation S-X, "
        "and PCAOB Rule 3211 (Auditor Reporting of Certain Audit Participants). These requirements "
        "are designed to safeguard auditor objectivity and independence by limiting the tenure of "
        "key engagement partners on SEC registrant audit engagements."
    )
    pdf.body(
        "The firm also voluntarily applies the rotation principles set forth in the IESBA Code of "
        "Ethics for engagements with non-registrant public interest entities (PIEs) where the firm "
        "deems it appropriate to enhance audit quality and public confidence."
    )

    pdf.section_heading("2", "Rotation Periods and Cooling-Off Requirements")
    pdf.sub_heading("2.1", "Lead Engagement Partner")
    pdf.body(
        "The lead engagement partner (also referred to as the 'engagement partner' or 'signing partner') "
        "must rotate off the engagement after serving in that capacity for five consecutive fiscal years. "
        "Following rotation, the partner is subject to a five-year cooling-off period during which the "
        "partner may not serve in any capacity on the engagement, provide consultation to the engagement "
        "team, or maintain direct contact with the audit client's management or audit committee regarding "
        "audit-related matters."
    )

    pdf.sub_heading("2.2", "Engagement Quality Reviewer")
    pdf.body(
        "The engagement quality reviewer (EQR, also known as the concurring review partner) is subject "
        "to the same five-year rotation and five-year cooling-off requirements as the lead engagement "
        "partner. The EQR's tenure clock runs independently from the lead engagement partner's tenure."
    )

    pdf.sub_heading("2.3", "Other Audit Partners")
    pdf.body(
        "Other audit partners who serve on the engagement in a significant capacity (e.g., partners "
        "responsible for major subsidiaries, divisions, or geographic regions, or partners responsible "
        "for significant accounting or auditing matters) are subject to a seven-year rotation period "
        "followed by a two-year cooling-off period. The engagement partner, in consultation with the "
        "National Quality Board, determines which other partners meet the 'significant capacity' threshold."
    )

    pdf.sub_heading("2.4", "Rotation Period Summary Table")
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 48, 87)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(55, 6, "Role", border=1, fill=True)
    pdf.cell(35, 6, "Max Tenure", border=1, fill=True, align="C")
    pdf.cell(35, 6, "Cooling-Off", border=1, fill=True, align="C")
    pdf.cell(45, 6, "Authority", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(30, 30, 30)
    rows = [
        ("Lead Engagement Partner", "5 years", "5 years", "SOX Sec. 203 / Rule 3211"),
        ("Engagement Quality Reviewer", "5 years", "5 years", "SOX Sec. 203 / Rule 3211"),
        ("Other Significant Partners", "7 years", "2 years", "SEC Rule 2-01(c)(6)"),
        ("Specialty Partners (Tax/IT)", "7 years", "2 years", "Firm Policy"),
    ]
    for i, (role, tenure, cooloff, auth) in enumerate(rows):
        fill = i % 2 == 0
        if fill:
            pdf.set_fill_color(235, 240, 248)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(55, 5, role, border=1, fill=fill)
        pdf.cell(35, 5, tenure, border=1, fill=fill, align="C")
        pdf.cell(35, 5, cooloff, border=1, fill=fill, align="C")
        pdf.cell(45, 5, auth, border=1, fill=fill, align="C")
        pdf.ln()
    pdf.ln(3)

    pdf.section_heading("3", "Transition Planning Procedures")
    pdf.sub_heading("3.1", "18-Month Advance Planning")
    pdf.body(
        "The Partner Rotation Committee identifies all partners approaching mandatory rotation at "
        "least 18 months in advance. The Committee, working with the relevant Regional Assurance "
        "Leader and industry sector leader, develops a succession plan that addresses:"
    )
    pdf.bullet_list([
        "Identification of successor partner candidates based on industry expertise, geographic proximity, available capacity, and client relationship considerations.",
        "Assessment of the successor's current engagement portfolio to ensure adequate bandwidth without compromising quality on existing engagements.",
        "Independence clearance of the proposed successor, including review of financial interests, business relationships, and prior employment.",
        "Client notification strategy and timeline, including coordination with the audit committee chair.",
        "Knowledge transfer plan covering critical audit areas, key judgments, historical issues, and relationship dynamics.",
    ])

    pdf.sub_heading("3.2", "12-Month Transition Period")
    pdf.body(
        "During the final 12 months of the outgoing partner's tenure, the successor partner is "
        "progressively integrated into the engagement. The transition follows a structured handover:"
    )
    pdf.bullet_list([
        "Months 12-9: Successor participates in planning meetings, reviews prior-year work papers for critical areas, and attends key client meetings as an observer.",
        "Months 9-6: Successor takes an active role in the current year's risk assessment, materiality determination, and audit strategy. The outgoing partner provides real-time mentoring and context.",
        "Months 6-3: Successor leads all engagement team interactions and client communications, with the outgoing partner available for consultation. Key client relationships are formally transferred.",
        "Months 3-0: Successor assumes full responsibility. The outgoing partner reviews the final deliverables as a quality safeguard but does not exercise decision-making authority.",
    ])

    pdf.section_heading("4", "Knowledge Transfer Protocols")
    pdf.body(
        "The firm recognizes that loss of institutional knowledge during partner rotation poses a "
        "risk to audit quality. The following protocols are designed to mitigate this risk:"
    )
    pdf.bullet_list([
        "Transition memorandum: The outgoing partner prepares a comprehensive transition memorandum covering entity background, industry-specific risks, historical audit issues and resolutions, key management personnel and communication preferences, prior regulatory findings, and critical accounting estimates and judgments.",
        "Critical judgments briefing: A face-to-face briefing (minimum 4 hours) between the outgoing and incoming partners covering all significant judgments made during the outgoing partner's tenure, including those related to going concern, accounting estimates, and scope of the audit.",
        "Root cause summaries: Documentation of any quality events (restatements, late filings, SEC comment letters, internal inspection findings) and the corrective actions taken.",
        "Relationship mapping: A comprehensive mapping of key client contacts, including communication styles, decision-making processes, and any known sensitivities.",
        "Industry knowledge repository: Updated industry briefings, peer benchmarking data, and regulatory developments maintained in the firm's knowledge management system.",
    ])

    pdf.section_heading("5", "Client Communication Templates")
    pdf.body(
        "The firm provides standardized communication templates for partner rotation events to ensure "
        "consistent, professional messaging to audit clients. The templates include:"
    )
    pdf.bullet_list([
        "Initial notification letter to the audit committee chair (delivered 12 months before rotation, jointly signed by the outgoing partner and the Regional Assurance Leader).",
        "Successor introduction letter (delivered 9 months before rotation, introducing the successor's qualifications, experience, and industry credentials).",
        "Formal transition announcement to the full audit committee (delivered 6 months before rotation, confirming the timeline and transition plan).",
        "Final transition confirmation letter (delivered at the point of rotation, confirming the successor's assumption of responsibilities and contact information).",
    ])

    pdf.section_heading("6", "Succession Planning for Complex Engagements")
    pdf.body(
        "For engagements classified as 'Complex' (defined as Global Systematically Important Banks, "
        "Fortune 100 companies, entities with more than 50 reporting components, or entities in "
        "highly regulated industries such as insurance, banking, and government contracting), "
        "enhanced succession planning requirements apply:"
    )
    pdf.bullet_list([
        "A dedicated Transition Oversight Partner (TOP) is appointed from the National Quality Board to supervise the transition.",
        "The transition period is extended to 24 months (versus the standard 12 months).",
        "A 'dry run' year is required: the successor partner effectively co-leads the engagement alongside the outgoing partner for the final year of tenure.",
        "A post-transition quality review is conducted by the National Office 6 months after the rotation event to assess whether the transition has been effective.",
        "The outgoing partner remains available for a 90-day consultation window following rotation (limited to knowledge transfer; the outgoing partner may not make engagement decisions).",
    ])

    pdf.output(os.path.join(OUTPUT_DIR, "audit_partner_rotation.pdf"))
    print("  Created audit_partner_rotation.pdf")


# =====================================================================
# Document 5 -- Audit Quality and PCAOB Results
# =====================================================================

def gen_audit_quality():
    pdf = MeridianPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.cover_page(
        "Audit Quality and\nPCAOB Inspection Results",
        "Annual Quality Report -- FY2025 Inspection Cycle\nInternal Peer Review and Quality Improvement Initiatives",
        "2.0",
        "February 15, 2026",
        "MA-AA-QR-2026-005",
    )

    pdf.add_page()
    pdf.section_heading("1", "Executive Summary")
    pdf.body(
        "Meridian & Associates LLP is committed to delivering the highest quality audit services. "
        "As a firm that audits more than 300 SEC registrant audit clients (including 18 accelerated filers and "
        "7 large accelerated filers), the firm is subject to annual inspection by the Public Company "
        "Accounting Oversight Board (PCAOB). This report summarizes the results of the most recent "
        "inspection cycle, the firm's internal peer review results, root cause analysis findings, "
        "and the quality improvement initiatives underway."
    )
    pdf.body(
        "Overall, the FY2025 inspection cycle results demonstrate continued improvement in the firm's "
        "audit quality. The number of Part I findings decreased from 4 (in the FY2024 cycle) to 2, "
        "representing a 50% reduction. Both findings were promptly addressed and remediated. No Part II "
        "quality control criticisms were identified."
    )

    pdf.section_heading("2", "PCAOB Inspection Results -- FY2025 Cycle")
    pdf.sub_heading("2.1", "Inspection Scope")
    pdf.body(
        "The PCAOB's FY2025 inspection of Meridian & Associates LLP was conducted between "
        "April 2025 and September 2025. The inspection covered the following:"
    )
    pdf.bullet_list([
        "45 audit engagements selected for review, spanning 14 industry sectors.",
        "Engagements ranged from large accelerated filers (market capitalization exceeding $700 million) to smaller reporting companies and emerging growth companies.",
        "Reviewed engagements included 12 integrated audits (financial statements and ICFR), 28 financial statement-only audits, and 5 broker-dealer audits.",
        "The inspection also included a review of the firm's system of quality control, including independence procedures, partner evaluation and compensation, engagement acceptance, and the firm's monitoring and remediation processes.",
    ])

    pdf.sub_heading("2.2", "Part I Findings -- Audit Deficiencies")
    pdf.body(
        "The PCAOB identified two Part I findings (audit deficiencies) out of 45 engagements reviewed, "
        "representing a 4.4% deficiency rate. The firm's five-year average deficiency rate is 6.2%, "
        "which compares favorably to the industry average of approximately 25% for annually inspected firms."
    )
    pdf.body("The two findings were as follows:")
    pdf.bullet_list([
        "Finding 1 -- Revenue Recognition (Technology Sector): The engagement team did not perform sufficient procedures to test the completeness of identified performance obligations under ASC 606 for a software company with complex multi-element arrangements. Specifically, the team did not adequately evaluate whether certain customization services represented distinct performance obligations. Remediation: The engagement team performed additional procedures and concluded that no misstatement existed. The firm updated its ASC 606 audit guide to include enhanced procedures for identifying embedded performance obligations in software arrangements.",
        "Finding 2 -- Goodwill Impairment (Consumer Products Sector): The engagement team did not sufficiently evaluate the reasonableness of management's cash flow projections used in the quantitative goodwill impairment test under ASC 350 (as simplified by ASU 2017-04, which eliminated the former Step 1/Step 2 framework). The team's sensitivity analysis did not adequately consider downside scenarios. Remediation: The engagement team engaged a Meridian valuation specialist to independently assess the projections and concluded that goodwill was not impaired. The firm issued supplemental guidance on evaluating management's forward-looking assumptions in impairment analyses.",
    ])

    pdf.sub_heading("2.3", "Part II Findings -- Quality Control")
    pdf.body(
        "The PCAOB did not identify any Part II criticisms related to the firm's system of quality "
        "control. The inspection team noted favorably the firm's investment in audit technology, "
        "the comprehensive partner evaluation framework, and the effectiveness of the National "
        "Office consultation process."
    )

    pdf.section_heading("3", "Internal Peer Review Results")
    pdf.body(
        "The firm's triennial peer review, conducted by an independent AICPA-authorized reviewer "
        "in Q4 2025, resulted in a rating of 'Pass' with no deficiencies noted. The peer review "
        "encompassed 30 engagements across the firm's audit, review, compilation, and attestation "
        "practice. The reviewer specifically commended the firm's:"
    )
    pdf.bullet_list([
        "Robust engagement quality review process with demonstrably independent EQR partners.",
        "Effective use of technology to enhance audit evidence, particularly the MeridianAI Analyze platform for journal entry testing.",
        "Comprehensive professional development and industry specialization program for audit professionals.",
        "Thorough documentation practices, particularly for significant judgments and estimates.",
    ])

    pdf.section_heading("4", "Root Cause Analysis Framework")
    pdf.body(
        "The firm employs a structured root cause analysis (RCA) framework for all quality events, "
        "including PCAOB findings, internal inspection deficiencies, restatements, and near-misses. "
        "The RCA framework follows a five-step methodology:"
    )
    pdf.bullet_list([
        "Step 1 -- Identification: Cataloging of the quality event, including the specific engagement, audit area, assertion, and nature of the deficiency.",
        "Step 2 -- Investigation: In-depth analysis of the facts and circumstances, including interviews with engagement team members, review of working papers, and timeline reconstruction.",
        "Step 3 -- Root Cause Determination: Classification of root causes using the firm's taxonomy, which includes categories such as: (a) insufficient professional skepticism, (b) inadequate technical knowledge, (c) resource constraints or excessive workload, (d) insufficient supervision or review, (e) methodology or guidance gaps, (f) technology or tool limitations, and (g) client-related factors.",
        "Step 4 -- Remediation Design: Development of targeted remediation actions linked to each identified root cause, with responsible parties, timelines, and success metrics.",
        "Step 5 -- Monitoring: Ongoing tracking of remediation effectiveness through the firm's Quality Dashboard, with quarterly reporting to the National Assurance Quality Board.",
    ])

    pdf.section_heading("5", "Quality Improvement Initiatives")
    pdf.body(
        "Based on the FY2025 inspection results and the firm's ongoing root cause analysis program, "
        "the following quality improvement initiatives are in progress or planned:"
    )
    pdf.bullet_list([
        "Enhanced ASC 606 Training: A mandatory 16-hour training module for all engagement teams serving clients with complex revenue recognition (effective Q2 2026).",
        "Impairment Assessment Toolkit: Development of standardized templates and independent data sources for evaluating management's assumptions in goodwill, intangible asset, and long-lived asset impairment analyses.",
        "Real-Time Quality Monitoring: Expansion of the MeridianAI platform to provide real-time alerts on potential quality issues during engagement execution, including workload imbalances, delayed milestone completion, and unusual patterns in audit evidence.",
        "Coaching Culture Initiative: A firm-wide program to shift the engagement review process from a 'review and correct' model to a 'coach in real time' model, with senior team members providing guidance during fieldwork rather than post-completion.",
        "Specialist Integration Enhancement: Strengthened protocols for the involvement, supervision, and documentation of work performed by IT audit, valuation, actuarial, tax, and forensic specialists (see Document MA-AA-SF-2026-007).",
    ])

    pdf.section_heading("6", "Audit Quality Indicators (AQIs)")
    pdf.body(
        "The firm tracks and reports the following Audit Quality Indicators on a quarterly basis. "
        "These metrics are reported to the National Assurance Quality Board and are available to "
        "audit committees upon request:"
    )

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 48, 87)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(55, 6, "Indicator", border=1, fill=True)
    pdf.cell(25, 6, "Target", border=1, fill=True, align="C")
    pdf.cell(25, 6, "FY2025", border=1, fill=True, align="C")
    pdf.cell(25, 6, "FY2024", border=1, fill=True, align="C")
    pdf.cell(40, 6, "Trend", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(30, 30, 30)
    aqi_data = [
        ("Partner workload (max hrs)", "1,600", "1,520", "1,580", "Improving"),
        ("Staff leverage ratio", "6:1", "5.9:1", "6.0:1", "Stable"),
        ("Industry specialist hours (%)", ">30%", "34%", "31%", "Improving"),
        ("EQR completion (days pre-sign)", ">5 days", "7.2 days", "5.8 days", "Improving"),
        ("Restatement rate", "<1%", "0.4%", "0.8%", "Improving"),
        ("PCAOB deficiency rate", "<5%", "4.4%", "6.7%", "Improving"),
        ("Staff turnover (audit)", "<18%", "17.5%", "19.1%", "Monitoring"),
        ("CPE hrs (avg per prof.)", ">50 hrs", "62 hrs", "55 hrs", "Improving"),
    ]
    for i, (ind, target, fy25, fy24, trend) in enumerate(aqi_data):
        fill = i % 2 == 0
        if fill:
            pdf.set_fill_color(235, 240, 248)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(55, 5, ind, border=1, fill=fill)
        pdf.cell(25, 5, target, border=1, fill=fill, align="C")
        pdf.cell(25, 5, fy25, border=1, fill=fill, align="C")
        pdf.cell(25, 5, fy24, border=1, fill=fill, align="C")
        pdf.cell(40, 5, trend, border=1, fill=fill, align="C")
        pdf.ln()

    # --- 3-5 Year Part I Findings Trend ---
    pdf.section_heading("7", "Part I Findings -- Five-Year Trend")
    pdf.body(
        "The following table presents the firm's PCAOB Part I inspection findings over the last "
        "five inspection cycles. The data demonstrate a sustained downward trajectory, reflecting "
        "the cumulative impact of the firm's quality improvement investments and root cause "
        "remediation programs."
    )

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 48, 87)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(30, 6, "Cycle", border=1, fill=True, align="C")
    pdf.cell(25, 6, "Engmts", border=1, fill=True, align="C")
    pdf.cell(25, 6, "Part I", border=1, fill=True, align="C")
    pdf.cell(30, 6, "Def. Rate", border=1, fill=True, align="C")
    pdf.cell(65, 6, "Primary Areas", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(30, 30, 30)
    trend_data = [
        ("FY2021", "38", "5", "13.2%", "ICFR testing, Revenue"),
        ("FY2022", "40", "4", "10.0%", "Fair value, Estimates"),
        ("FY2023", "42", "3", "7.1%", "Inventory, ICFR"),
        ("FY2024", "43", "4", "9.3%", "Revenue (ASC 606), Leases"),
        ("FY2025", "45", "2", "4.4%", "Revenue (ASC 606), Goodwill"),
    ]
    for i, (cycle, eng, findings, rate, areas) in enumerate(trend_data):
        fill = i % 2 == 0
        if fill:
            pdf.set_fill_color(235, 240, 248)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(30, 5, cycle, border=1, fill=fill, align="C")
        pdf.cell(25, 5, eng, border=1, fill=fill, align="C")
        pdf.cell(25, 5, findings, border=1, fill=fill, align="C")
        pdf.cell(30, 5, rate, border=1, fill=fill, align="C")
        pdf.cell(65, 5, areas, border=1, fill=fill)
        pdf.ln()

    pdf.body(
        "The FY2024 uptick from 3 to 4 findings reflected the addition of several newly acquired "
        "mid-market engagements that had not yet been fully integrated into Meridian's methodology. "
        "Enhanced onboarding protocols implemented in Q1 2025 contributed to the FY2025 improvement."
    )

    # --- Areas of Continued Focus ---
    pdf.section_heading("8", "Areas of Continued Focus")
    pdf.body(
        "While the overall trajectory is positive, several areas require ongoing attention and "
        "investment. The National Assurance Quality Board has designated the following as priority "
        "focus areas for FY2026:"
    )
    pdf.bullet_list([
        "Revenue Recognition Complexity: ASC 606 continues to generate the most frequent Part I findings across the profession. Meridian's ASC 606 Center of Excellence will deploy enhanced audit programs for software, SaaS, and construction contract revenue in Q2 2026, including mandatory specialist involvement for arrangements exceeding $25M.",
        "Staff Retention and Workload Management: Although staff turnover has improved from 19.1% to 17.5%, the metric remains in 'Monitoring' status. The firm is piloting a workload analytics dashboard that provides real-time visibility into individual utilization and flags teams approaching burnout thresholds. The 18% target remains aspirational in the current labor market, and the Quality Board is evaluating whether an adjusted 19% target is more appropriate.",
        "Emerging Accounting Standards: The adoption of ASU 2023-09 (Income Tax Disclosures) effective for fiscal years beginning after December 15, 2024, will require significant new audit procedures. The firm is developing specialized audit programs and training modules for the expanded rate reconciliation and jurisdictional disclosure requirements.",
        "Audit Data Analytics Adoption: While MeridianAI Analyze is deployed on 100% of SEC registrant engagements, adoption of the full analytics suite (including predictive fraud scoring and automated three-way matching) stands at 68% of eligible engagements. The firm's target is 90% adoption by Q4 2026.",
        "Cryptocurrency and Digital Asset Audits: The firm is building specialized audit methodologies for clients holding or transacting in digital assets, addressing the unique valuation, custody, and disclosure challenges under ASC 350-60 (Crypto Assets).",
    ])

    pdf.section_heading("9", "PCAOB QC 1000 and ISQM 1 Compliance")
    pdf.body(
        "Effective December 15, 2025, PCAOB QC 1000 (A Firm's System of Quality Control) replaced "
        "the prior interim quality control standards and established a risk-based, proactive framework "
        "for quality management at the firm level. Meridian & Associates LLP completed its transition "
        "to QC 1000 in Q4 2025. The firm's quality management system now addresses all eight components "
        "specified in QC 1000: governance and leadership, the firm's risk assessment process, engagement "
        "performance, relevant ethical requirements (including independence), acceptance and continuance, "
        "resources, information and communication, and the monitoring and remediation process."
    )
    pdf.body(
        "The firm's QC 1000 implementation is also aligned with the International Standard on Quality "
        "Management 1 (ISQM 1) issued by the International Auditing and Assurance Standards Board "
        "(IAASB), which took effect on December 15, 2022. Where the firm serves clients subject to "
        "international auditing standards, its quality management system satisfies both QC 1000 and "
        "ISQM 1 requirements. The National Assurance Quality Board maintains a unified quality "
        "objectives and risk register that maps each identified quality risk to both frameworks, "
        "ensuring consistent monitoring and remediation across domestic and international engagements."
    )

    pdf.output(os.path.join(OUTPUT_DIR, "audit_quality_pcaob_results.pdf"))
    print("  Created audit_quality_pcaob_results.pdf")


# =====================================================================
# Document 6 -- Audit Technology Integration
# =====================================================================

def gen_technology_integration():
    pdf = MeridianPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.cover_page(
        "Audit Technology\nIntegration Framework",
        "Proprietary AI, Analytics, and Automation Tools\nfor Financial Statement Audits",
        "3.0",
        "January 30, 2026",
        "MA-AA-TI-2026-006",
    )

    pdf.add_page()
    pdf.section_heading("1", "Introduction and Strategic Vision")
    pdf.body(
        "Meridian & Associates LLP has made a strategic commitment to integrating advanced technology "
        "into every phase of the audit process. The firm has invested over $240 million in its audit "
        "technology platform since 2020, building a suite of proprietary tools designed to enhance "
        "audit quality, improve efficiency, and deliver deeper insights to audit clients and their "
        "stakeholders. This framework document describes the firm's current technology capabilities "
        "and their integration into the standard audit methodology."
    )
    pdf.body(
        "The firm's technology strategy is guided by three core principles: (1) technology should "
        "augment professional judgment, not replace it; (2) full-population testing should be the "
        "default where technically feasible, replacing traditional sampling; and (3) all technology "
        "tools must be validated, documented, and subject to the same quality standards as traditional "
        "audit procedures."
    )
    pdf.body(
        "The firm's technology platform comprises two complementary pillars: MeridianAudit Suite, "
        "the engagement documentation and workflow platform used to manage work papers, review notes, "
        "and sign-offs; and MeridianAI, the analytics and artificial intelligence platform (including "
        "MeridianAI Analyze and MeridianAI Contract Reader) used for data-driven audit procedures "
        "such as journal entry testing, fraud risk scoring, and contract analysis."
    )

    pdf.section_heading("2", "MeridianAI Analyze -- Journal Entry Testing")
    pdf.sub_heading("2.1", "Capabilities")
    pdf.body(
        "MeridianAI Analyze is the firm's flagship AI-powered audit tool for journal entry testing. "
        "Unlike traditional sampling-based approaches (which typically test fewer than 1% of journal "
        "entries), MeridianAI Analyze tests 100% of journal entries recorded during the audit period. "
        "The platform processes entries from any major ERP system (SAP, Oracle, Workday, NetSuite, "
        "Microsoft Dynamics) and uses a multi-layered analysis approach:"
    )
    pdf.bullet_list([
        "Rule-Based Screening: Identifies entries matching predefined risk indicators, including entries posted after business hours, entries by users with unusual posting authority, entries with round-dollar amounts exceeding specified thresholds, entries posted with non-standard or blank descriptions, and entries posted at or near period-end with reversals in the subsequent period.",
        "Machine Learning Anomaly Detection: A supervised learning model trained on the firm's proprietary dataset of over 2.8 billion historical journal entries identifies entries that deviate from expected patterns based on the entity's historical posting behavior. The model considers account combinations, amounts, timing, frequency, and user identity.",
        "Natural Language Processing (NLP): Analyzes the text descriptions of journal entries to identify entries with unusual or inconsistent narratives, entries referencing related parties or key management personnel, and entries with descriptions that are inconsistent with the affected accounts.",
        "Network Analysis: Maps relationships between posting users, accounts, and amounts to identify complex entry chains that may indicate attempts to obscure the true nature of transactions.",
    ])

    pdf.sub_heading("2.2", "Validation and Audit Evidence")
    pdf.body(
        "The firm's Data Science Quality Board has validated MeridianAI Analyze's models using "
        "back-testing against known fraud cases and restatements. The tool's precision rate (correct "
        "identification of unusual entries) exceeds 92%, while the recall rate (identification of all "
        "genuinely unusual entries) exceeds 98%. All model outputs are reviewed by qualified audit "
        "professionals before being used as audit evidence. The tool does not make audit judgments; "
        "it identifies entries for further investigation."
    )

    pdf.section_heading("3", "Predictive Analytics for Fraud Risk Scoring")
    pdf.body(
        "The firm has developed a proprietary fraud risk scoring model that supplements the engagement "
        "team's fraud risk assessment under PCAOB AS 2401 and ISA 240. The model evaluates entity-level "
        "and account-level fraud risk factors using a combination of:"
    )
    pdf.bullet_list([
        "Financial statement analytics: Beneish M-Score, Altman Z-Score, revenue quality indicators, earnings management proxies, and accrual-based measures.",
        "Non-financial indicators: Management turnover, auditor changes, related-party transaction complexity, governance quality scores, litigation and regulatory history, and media sentiment analysis.",
        "Industry benchmarking: Comparison of key financial metrics against industry peer groups using the firm's proprietary database of over 15,000 public company financial profiles.",
        "Temporal analysis: Trend analysis across multiple reporting periods to identify deteriorating patterns that may indicate elevated fraud risk.",
    ])
    pdf.body(
        "The model produces a composite fraud risk score (1-100 scale) for each engagement, with "
        "scores categorized as Low (1-30), Moderate (31-60), High (61-80), and Very High (81-100). "
        "Engagements scoring above 60 require mandatory consultation with the firm's Forensic and "
        "Litigation Services practice."
    )

    pdf.section_heading("4", "Automated Three-Way Matching")
    pdf.body(
        "The firm's automated three-way matching tool digitally matches purchase orders, receiving "
        "reports, and vendor invoices for accounts payable testing. The tool operates on the client's "
        "procurement data (extracted via secure API connections to the client's ERP system) and "
        "performs the following procedures without manual intervention:"
    )
    pdf.bullet_list([
        "Matching of purchase order, goods receipt, and invoice across quantity, price, and amount fields with configurable tolerance thresholds.",
        "Identification of unmatched or partially matched transactions for targeted follow-up.",
        "Analysis of duplicate payments, duplicate vendor records, and payments to vendors not on the approved vendor master file.",
        "Evaluation of purchase order authorization levels and identification of split orders that may indicate circumvention of approval thresholds.",
        "Aging analysis of unmatched receiving reports to identify potential unrecorded liabilities.",
    ])

    pdf.section_heading("5", "Drone and Satellite Imagery for Inventory Observation")
    pdf.body(
        "For engagements involving physically large or geographically dispersed inventory (e.g., "
        "mining, agriculture, energy, real estate), the firm supplements traditional physical "
        "observation procedures with drone and satellite imagery:"
    )
    pdf.bullet_list([
        "Drone-mounted LiDAR (Light Detection and Ranging) sensors create three-dimensional volumetric measurements of bulk inventories such as stockpiles, grain silos, and liquid storage tanks. These measurements are compared to management's recorded quantities with a measurement accuracy of +/- 1.5%.",
        "Commercial satellite imagery (sub-meter resolution) is used to corroborate the existence and scale of large-area inventory, including timber stands, agricultural crops, and solar panel installations. Multi-temporal analysis compares imagery from different dates to assess changes in inventory levels.",
        "All drone and satellite procedures are performed under the supervision of qualified audit professionals. The imagery and volumetric data constitute corroborative audit evidence and are documented in the firm's standard work paper format.",
    ])

    pdf.section_heading("6", "NLP for Contract Analysis")
    pdf.body(
        "The firm's NLP-powered contract analysis tool, MeridianAI Contract Reader, automates the "
        "review of large volumes of contracts for key audit-relevant terms. The tool is used "
        "extensively in the following audit areas:"
    )
    pdf.bullet_list([
        "Revenue recognition (ASC 606): Extraction of performance obligations, variable consideration terms, significant financing components, and contract modification provisions.",
        "Lease accounting (ASC 842): Identification of lease terms, renewal and termination options, variable lease payments, residual value guarantees, and embedded lease arrangements.",
        "Debt and financing (ASC 470/ASC 815): Extraction of covenant terms, interest rate provisions, prepayment penalties, conversion features, and embedded derivatives.",
        "The tool processes contracts in PDF, Word, and scanned image formats (via OCR). It has been trained on over 500,000 contracts across 22 industry sectors and achieves a field-level extraction accuracy exceeding 95%.",
    ])

    pdf.section_heading("7", "RPA for Confirmations Processing")
    pdf.body(
        "The firm has deployed Robotic Process Automation (RPA) to streamline the audit confirmations "
        "process. The RPA solution handles:"
    )
    pdf.bullet_list([
        "Automated generation and distribution of confirmation requests (bank confirmations, accounts receivable confirmations, accounts payable confirmations, and legal confirmations) using data extracted from client systems.",
        "Automated tracking of outstanding confirmations with escalation workflows at 10, 20, and 30 days past the request date.",
        "Digital receipt and reconciliation of returned confirmations, with automatic matching of confirmed balances to the general ledger. Discrepancies exceeding the de minimis threshold are flagged for manual investigation.",
        "Integration with the AICPA Confirmation.com platform for electronic bank and other financial institution confirmations.",
        "Year-over-year response rate analytics to identify clients or third parties with historically low response rates, enabling the team to plan alternative procedures proactively.",
    ])

    pdf.section_heading("8", "Data Lake Architecture and ERP Integration")
    pdf.body(
        "The firm's Audit Data Lake provides a centralized, secure repository for all client data "
        "extracted during the audit process. Key features include:"
    )
    pdf.bullet_list([
        "Pre-built connectors for major ERP systems: SAP (S/4HANA and ECC), Oracle (Cloud ERP and E-Business Suite), Workday, NetSuite, Microsoft Dynamics 365, and Infor.",
        "Automated data extraction, transformation, and loading (ETL) pipelines that standardize client data into the firm's common audit data model, enabling consistent analytics across engagements.",
        "Role-based access controls ensuring that engagement team members only access data for their assigned engagements, with full audit trails of all data access and modifications.",
        "Data retention policies compliant with PCAOB AS 1215 (Audit Documentation) and SEC Rule 2-06 of Regulation S-X (seven-year retention) and applicable data privacy regulations.",
        "Encryption at rest (AES-256) and in transit (TLS 1.3), with data residency options to comply with cross-border data transfer requirements.",
    ])

    pdf.output(os.path.join(OUTPUT_DIR, "audit_technology_integration.pdf"))
    print("  Created audit_technology_integration.pdf")


# =====================================================================
# Document 7 -- Specialist Integration Framework
# =====================================================================

def gen_specialist_framework():
    pdf = MeridianPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.cover_page(
        "Specialist Integration\nFramework",
        "Protocols for Utilizing IT Audit, Valuation, Actuarial,\nForensic, and Tax Specialists in Financial Statement Audits",
        "4.0",
        "February 10, 2026",
        "MA-AA-SF-2026-007",
    )

    pdf.add_page()
    pdf.section_heading("1", "Purpose and Scope")
    pdf.body(
        "This framework establishes the protocols and standards for integrating specialist expertise "
        "into financial statement audits conducted by Meridian & Associates LLP. The use of specialists "
        "is governed by PCAOB AS 1210 (Using the Work of a Specialist), PCAOB AS 1201 (Supervision of "
        "the Audit Engagement), and ISA 620 (Using the Work of an Auditor's Expert). The engagement "
        "partner retains ultimate responsibility for the audit opinion, including all areas in which "
        "specialists are involved."
    )
    pdf.body(
        "The framework applies to all specialist resources, whether drawn from within the firm's "
        "specialist practices or engaged from external third parties. The standards for competency "
        "assessment, supervision, communication, and documentation apply equally in both cases."
    )

    pdf.section_heading("2", "IT Audit Specialists")
    pdf.sub_heading("2.1", "Scope of IT Audit Involvement")
    pdf.body(
        "IT audit specialists are involved on all engagements where the entity's financial reporting "
        "relies on information technology systems. For SEC registrant integrated audits, IT audit "
        "involvement is mandatory. The IT audit scope typically includes:"
    )
    pdf.bullet_list([
        "IT General Controls (ITGCs) Testing: Assessment of controls over program change management, logical access and security, computer operations and job scheduling, and program development/system implementation. ITGCs are evaluated across all in-scope applications and databases that support financial reporting.",
        "SOC Report Evaluation: Review and assessment of Service Organization Controls (SOC 1/SOC 2) reports for third-party service providers used by the audit client. The IT audit specialist evaluates the scope, coverage period, testing methodology, exceptions identified, and complementary user entity controls.",
        "Cybersecurity Assessment: Evaluation of the entity's cybersecurity posture as it relates to financial reporting integrity, including network segmentation, endpoint protection, incident response procedures, and data loss prevention controls. While not a separate cybersecurity audit, these procedures inform the engagement team's assessment of IT-related risks to financial reporting.",
        "Automated Application Controls: Testing of key automated controls within the entity's financial reporting applications, including input validation, processing controls, output reconciliations, and interface controls between systems.",
        "Data Analytics Support: Extraction and validation of data used by the core audit team for substantive analytics, journal entry testing, and other data-driven procedures.",
    ])

    pdf.sub_heading("2.2", "IT Specialist Qualifications")
    pdf.body(
        "All IT audit specialists assigned to engagements must hold at least one of the following "
        "certifications: CISA (Certified Information Systems Auditor), CISSP (Certified Information "
        "Systems Security Professional), or CISM (Certified Information Security Manager). Specialists "
        "assigned to evaluate complex ERP environments must have documented experience with the specific "
        "platform (minimum 3 years for SAP or Oracle environments)."
    )

    pdf.section_heading("3", "Valuation Specialists")
    pdf.sub_heading("3.1", "Scope of Valuation Involvement")
    pdf.body(
        "Valuation specialists are engaged when the audit involves significant fair value measurements, "
        "particularly those classified as Level 3 in the fair value hierarchy under ASC 820 (Fair Value "
        "Measurement). Common areas of valuation specialist involvement include:"
    )
    pdf.bullet_list([
        "Level 3 Fair Value Measurements: Independent assessment of management's valuation models and assumptions for financial instruments, contingent consideration, real estate, and other assets and liabilities measured at fair value using unobservable inputs.",
        "Goodwill and Intangible Asset Impairment (ASC 350/ASC 360): Evaluation of management's discounted cash flow models, market multiples analyses, and other valuation approaches used in goodwill impairment testing, including assessment of discount rates, growth rate assumptions, terminal values, and comparability of guideline companies.",
        "Purchase Price Allocation (ASC 805): Independent assessment of fair values assigned to identifiable assets acquired and liabilities assumed in business combinations, including customer relationships, developed technology, tradenames, in-process research and development, and favorable/unfavorable contract assets.",
        "Share-Based Compensation (ASC 718): Review of valuation models (Black-Scholes, lattice models, Monte Carlo simulations) used to estimate the fair value of stock options, restricted stock units, and performance-based equity awards.",
        "Contingent Consideration and Earnout Provisions: Assessment of probability-weighted scenarios and discount rates used to measure contingent consideration liabilities arising from business combinations.",
    ])

    pdf.sub_heading("3.2", "Valuation Specialist Qualifications")
    pdf.body(
        "Valuation specialists must hold the ASA (American Society of Appraisers) or CFA (Chartered "
        "Financial Analyst) designation. For complex financial instrument valuations, the specialist "
        "must hold the FRM (Financial Risk Manager) designation or demonstrate equivalent expertise "
        "through documented experience."
    )

    pdf.section_heading("4", "Actuarial Specialists")
    pdf.sub_heading("4.1", "Scope of Actuarial Involvement")
    pdf.body(
        "Actuarial specialists are engaged for engagements involving significant actuarially determined "
        "obligations or reserves. Key areas include:"
    )
    pdf.bullet_list([
        "Pension and OPEB Obligations (ASC 715): Independent assessment of the actuarial assumptions used by the plan's actuary, including discount rates, expected return on plan assets, salary escalation rates, mortality tables, turnover rates, and healthcare cost trend rates. The specialist evaluates the reasonableness of assumptions both individually and in the aggregate.",
        "Insurance Reserves (ASC 944): For insurance company audits, evaluation of loss reserves (both case reserves and IBNR -- incurred but not reported), unearned premium reserves, and deferred acquisition cost recoverability. The specialist performs independent reserve analyses using actuarial methods such as chain-ladder, Bornhuetter-Ferguson, and expected loss ratio approaches.",
        "Self-Insurance Liabilities: Assessment of self-insurance accruals for workers' compensation, general liability, professional liability, and healthcare claims, including evaluation of development factors and trend assumptions.",
        "Asset Retirement Obligations (ASC 410): Review of the estimated costs and timing assumptions used to measure asset retirement obligations, including decommissioning, environmental remediation, and lease restoration costs.",
    ])

    pdf.sub_heading("4.2", "Actuarial Specialist Qualifications")
    pdf.body(
        "Actuarial specialists must be credentialed members of the Society of Actuaries (FSA) or the "
        "Casualty Actuarial Society (FCAS). For pension engagements, the specialist must hold the "
        "Enrolled Actuary (EA) designation. All actuarial specialists must comply with the Actuarial "
        "Standards of Practice (ASOPs) issued by the Actuarial Standards Board."
    )

    pdf.section_heading("5", "Forensic Accountants")
    pdf.sub_heading("5.1", "Scope of Forensic Involvement")
    pdf.body(
        "Forensic accounting specialists support the engagement team in addressing fraud risk "
        "assessment and response requirements under PCAOB AS 2401 and ISA 240. Their involvement "
        "includes:"
    )
    pdf.bullet_list([
        "Fraud Risk Assessment: Participation in the engagement team's fraud brainstorming session (required by PCAOB AS 2401.14), contributing forensic expertise on common fraud schemes, industry-specific fraud risks, and indicators of management override of controls.",
        "Fraud Risk Procedures: Design and execution of targeted procedures responsive to identified fraud risks, including data mining and analytics for unusual patterns, Benford's Law analysis, vendor and employee relationship analysis, and lifestyle/behavioral red flag assessment.",
        "Whistleblower Investigations: When the engagement team becomes aware of whistleblower complaints or tips related to financial reporting, the forensic specialist designs and executes investigative procedures, coordinates with the audit client's legal counsel as appropriate, and assesses the impact on the financial statements and audit report.",
        "Management Override Testing: Enhanced testing of management override of controls, including examination of significant or unusual transactions outside the normal course of business, review of accounting estimates for bias, and evaluation of the business rationale for significant unusual transactions.",
        "Anti-Corruption and FCPA: For multinational audit clients, assessment of Foreign Corrupt Practices Act (FCPA) and anti-bribery compliance risks, including review of payments to government officials, agent and consultant agreements, and travel and entertainment expenditures in high-risk jurisdictions.",
    ])

    pdf.sub_heading("5.2", "Forensic Specialist Qualifications")
    pdf.body(
        "Forensic accounting specialists must hold the CFE (Certified Fraud Examiner) designation. "
        "Specialists assigned to FCPA-related procedures must have demonstrated experience with "
        "cross-border corruption investigations and familiarity with the U.S. Department of Justice "
        "and SEC enforcement frameworks."
    )

    pdf.section_heading("6", "Tax Specialists")
    pdf.sub_heading("6.1", "Scope of Tax Involvement")
    pdf.body(
        "Tax specialists are engaged for engagements involving material or complex income tax "
        "positions. Their involvement includes:"
    )
    pdf.bullet_list([
        "Uncertain Tax Positions (ASC 740-10): Evaluation of management's identification and measurement of uncertain tax positions under the two-step recognition and measurement framework (more-likely-than-not recognition threshold and largest amount measurement). The tax specialist assesses the technical merits of each significant position and evaluates whether the entity's reserves are reasonable.",
        "ASC 740 Review: Comprehensive review of the entity's income tax provision, including current and deferred tax calculations, effective tax rate reconciliation, valuation allowance assessment for deferred tax assets, and assessment of unremitted foreign earnings (including the impact of GILTI, BEAT, and FDII provisions under the Tax Cuts and Jobs Act, as amended).",
        "Transfer Pricing: For multinational entities, evaluation of intercompany pricing arrangements and related documentation to assess whether transfer pricing positions could result in material tax adjustments.",
        "Tax Controversy: Assessment of the potential financial statement impact of ongoing tax audits, administrative appeals, and tax litigation.",
        "Tax Legislation Analysis: Evaluation of the impact of new or pending tax legislation on the entity's tax provision and deferred tax balances, including interim period adjustments required by ASC 740-270.",
    ])

    pdf.sub_heading("6.2", "Tax Specialist Qualifications")
    pdf.body(
        "Tax specialists must be licensed CPAs with at least 10 years of relevant tax experience. "
        "Specialists advising on international tax matters must have demonstrated expertise in "
        "cross-border taxation, including bilateral tax treaties, OECD BEPS guidelines, and Pillar Two "
        "global minimum tax rules."
    )

    pdf.section_heading("7", "Engagement Protocols and Supervision")
    pdf.body(
        "The following protocols apply to all specialist engagements:"
    )
    pdf.bullet_list([
        "Scope Definition: The engagement partner, in consultation with the specialist practice leader, defines the scope of the specialist's involvement using the firm's standard Specialist Engagement Memorandum (Form MA-SE-001). The memorandum specifies the audit objective, the relevant assertions, the work to be performed, the timeline, and the expected deliverables.",
        "Competency and Objectivity Assessment: Before utilizing a specialist's work, the engagement team assesses the specialist's professional qualifications, experience, and objectivity. For external specialists, the assessment includes review of credentials, independence, and potential conflicts of interest.",
        "Supervision: The engagement partner and engagement manager are responsible for supervising the specialist's work to the extent necessary to evaluate whether the work constitutes sufficient appropriate audit evidence. This includes reviewing the specialist's assumptions, methods, and conclusions.",
        "Communication: Regular communication between the core audit team and the specialist is required throughout the engagement. A formal handoff meeting is held at the start of the specialist's work, and a findings review meeting is held upon completion.",
        "Disagreements: Any disagreements between the core audit team and a specialist regarding conclusions or findings are escalated to the engagement partner and, if unresolved, to the National Office for consultation.",
    ])

    pdf.section_heading("8", "Documentation Standards")
    pdf.body(
        "The engagement team's work papers must include the following documentation related to "
        "specialist involvement:"
    )
    pdf.bullet_list([
        "The Specialist Engagement Memorandum (Form MA-SE-001) defining scope and responsibilities.",
        "The competency and objectivity assessment of the specialist.",
        "A description of the nature, scope, and objectives of the specialist's work.",
        "The specialist's findings, conclusions, and report (if applicable).",
        "The engagement team's evaluation of the adequacy and appropriateness of the specialist's work as audit evidence, including the team's own assessment of the specialist's assumptions, methods, and conclusions.",
        "Any adjustments to the audit plan or additional procedures performed as a result of the specialist's findings.",
        "Documentation of all communications between the core audit team and the specialist, including disagreements and their resolution.",
    ])
    pdf.body(
        "All specialist work papers are subject to the same retention, access control, and quality "
        "review standards as core audit work papers, in accordance with PCAOB AS 1215 and the firm's "
        "Documentation Policy (MA-QC-DOC-2025-001)."
    )

    pdf.output(os.path.join(OUTPUT_DIR, "specialist_integration_framework.pdf"))
    print("  Created specialist_integration_framework.pdf")


# =====================================================================
# Document 8 -- Group Audit Methodology
# =====================================================================

def gen_group_audit_methodology():
    pdf = MeridianPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.cover_page(
        "Group Audit\nMethodology",
        "Multi-Location Audit Approach Under PCAOB AS 1205 / ISA 600\nComponent Materiality, Direction, and Supervision",
        "3.0",
        "March 1, 2026",
        "MA-AA-GA-2026-008",
    )

    pdf.add_page()
    pdf.section_heading("1", "Purpose and Applicability")
    pdf.body(
        "This document establishes the standard methodology for group audits performed by "
        "Meridian & Associates LLP. A group audit arises when the group financial statements "
        "include the financial information of more than one component -- for example, subsidiaries, "
        "divisions, branches, joint ventures, or investees accounted for under the equity method. "
        "The methodology applies to all engagements where the group engagement team (GET) uses the "
        "work of component auditors, whether those component auditors are other Meridian offices, "
        "Meridian network member firms, or non-network audit firms."
    )
    pdf.body(
        "The framework is designed to comply with PCAOB AS 1205 (Part of the Audit Performed by "
        "Other Independent Auditors), PCAOB AS 2101 (Audit Planning), ISA 600 (Special "
        "Considerations -- Audits of Group Financial Statements), and the firm's internal quality "
        "standards. Where PCAOB and ISA requirements differ, Meridian's policy requires compliance "
        "with the more stringent standard unless the engagement is exclusively subject to one regime."
    )

    pdf.section_heading("2", "Group Engagement Team Responsibilities")
    pdf.sub_heading("2.1", "Acceptance and Continuance")
    pdf.body(
        "Before accepting or continuing a group audit engagement, the group engagement partner "
        "must evaluate the following factors in consultation with the Regional Assurance Leader:"
    )
    pdf.bullet_list([
        "The group structure, including the number, size, and geographic dispersion of components.",
        "The availability and competence of component auditors, including an assessment of their understanding of applicable financial reporting frameworks and auditing standards.",
        "Whether sufficient appropriate audit evidence can reasonably be expected to be obtained for the group audit opinion.",
        "The ability to be sufficiently involved in the work of component auditors, including the ability to perform direction, supervision, and review activities (including site visits where necessary).",
        "Restrictions on access to component management, component auditors, or component information (e.g., due to local regulations or government classification).",
    ])

    pdf.sub_heading("2.2", "Understanding the Group and Its Components")
    pdf.body(
        "The GET must obtain a sufficient understanding of the group, its components, and their "
        "environments to identify and assess risks of material misstatement of the group financial "
        "statements. This understanding encompasses the group's organizational structure, reporting "
        "processes, intercompany transactions and eliminations, and the nature and extent of "
        "consolidation adjustments. The GET must identify components that are individually "
        "financially significant to the group and components that are likely to include significant "
        "risks of material misstatement."
    )

    pdf.sub_heading("2.3", "Scoping and Component Classification")
    pdf.body(
        "Each component is classified into one of three categories that determine the nature and "
        "extent of work to be performed:"
    )
    pdf.bullet_list([
        "Significant Components -- Full Scope: Components that are individually financially significant to the group (typically contributing more than 15% of group revenues, assets, or pre-tax income). A full-scope audit is performed using component materiality.",
        "Significant Components -- Specified Procedures: Components that include significant risks of material misstatement of the group financial statements due to their specific nature or circumstances. Audit procedures are performed on specified account balances, classes of transactions, or disclosures.",
        "Non-Significant Components -- Analytical Procedures: Remaining components where analytical procedures at the group level are sufficient to address the risks of material misstatement. Selected non-significant components are rotated into specified or full-scope procedures on a cyclical basis to provide additional audit coverage.",
    ])
    pdf.body(
        "The scoping decision must achieve coverage of a sufficient portion of the group financial "
        "statements. Meridian's policy requires that significant components receiving full-scope or "
        "specified-scope procedures collectively represent at least 60% of consolidated revenues "
        "and 60% of consolidated total assets. Coverage exceeding 75% on both metrics is "
        "considered best practice."
    )

    pdf.section_heading("3", "Component Materiality")
    pdf.body(
        "Component materiality is set by the GET for each component where audit work will be "
        "performed. Component materiality must be lower than group materiality to reduce the risk "
        "that the aggregate of uncorrected and undetected misstatements across components exceeds "
        "group materiality."
    )
    pdf.body(
        "Meridian's standard approach for determining component materiality is as follows:"
    )
    pdf.bullet_list([
        "Allocation Method: Component materiality is derived by allocating a portion of group materiality to each in-scope component based on relative size (typically using the same benchmark as group materiality -- e.g., pre-tax income, revenue, or total assets).",
        "Cap: Component materiality may not exceed 85% of group materiality for any single component, regardless of the component's relative size.",
        "Floor: Component materiality may not be set below the level at which misstatements would be clearly trivial. As a practical minimum, component materiality is typically no lower than 50% of group performance materiality.",
        "Professional Judgment: The GET exercises professional judgment in adjusting component materiality for qualitative risk factors, such as the component's history of audit adjustments, the quality of the component's internal controls, or the complexity of its transactions.",
    ])
    pdf.body(
        "Component performance materiality and the threshold for accumulating misstatements (SAT -- "
        "Summary of Audit Differences) are similarly derived from group-level thresholds, applying "
        "the same percentage reduction used to determine component materiality from group materiality."
    )

    pdf.section_heading("4", "Direction, Supervision, and Review")
    pdf.sub_heading("4.1", "Group Audit Instructions")
    pdf.body(
        "The GET issues formal Group Audit Instructions (GAIs) to each component auditor. The GAIs "
        "are tailored to the component's scoping classification and include:"
    )
    pdf.bullet_list([
        "Component materiality, performance materiality, and de minimis threshold.",
        "Significant risks identified at the group level and their implications for the component.",
        "Required audit procedures for specified accounts, balances, and disclosures.",
        "Intercompany transaction confirmation and elimination procedures.",
        "Required deliverables and reporting formats (including the use of the firm's standard Component Auditor Reporting Package).",
        "Deadlines for completion of fieldwork, clearance of review notes, and submission of the reporting package.",
        "Requirements for communication of matters arising during the component audit, including fraud, non-compliance with laws and regulations, significant deficiencies, and material weaknesses.",
        "Independence and ethical requirements applicable to the engagement.",
    ])

    pdf.sub_heading("4.2", "Supervision and Monitoring")
    pdf.body(
        "The GET maintains ongoing involvement in the component auditor's work throughout the "
        "engagement. Supervision activities include:"
    )
    pdf.bullet_list([
        "Pre-issuance planning calls with each component auditor to discuss the engagement approach, timing, and risk areas.",
        "Interim status check-ins (at minimum biweekly during active fieldwork) to monitor progress, address emerging issues, and adjust procedures as needed.",
        "Site visits to significant component locations. Meridian requires at least one in-person site visit per triennial cycle for each full-scope significant component, with annual visits for components identified as high-risk.",
        "Review of key working papers prepared by the component auditor, focusing on areas of significant judgment, estimates, and identified risks.",
    ])

    pdf.sub_heading("4.3", "Review of Component Auditor Work")
    pdf.body(
        "The GET reviews the component auditor's reporting package, evaluates the sufficiency "
        "and appropriateness of audit evidence obtained, and assesses whether additional "
        "procedures are required at the group level. The review includes:"
    )
    pdf.bullet_list([
        "Evaluation of the component auditor's summary of unadjusted misstatements and their effect on the group financial statements.",
        "Assessment of significant accounting judgments and estimates at the component level.",
        "Review of the component auditor's communications regarding fraud risks, going concern issues, and significant internal control deficiencies.",
        "Evaluation of the adequacy of the component auditor's response to risks identified in the Group Audit Instructions.",
    ])

    pdf.section_heading("5", "Evaluating Component Auditor Competence")
    pdf.body(
        "Before placing reliance on the work of a component auditor, the GET must evaluate the "
        "component auditor's professional competence and independence. For Meridian network firms, "
        "this evaluation leverages the firm's global quality monitoring program. For non-network "
        "component auditors, the evaluation is more extensive and includes:"
    )
    pdf.bullet_list([
        "Verification of registration with the PCAOB (for audits of SEC registrants) or the relevant national audit oversight body.",
        "Review of the component auditor's most recent PCAOB or equivalent inspection report, including any identified deficiencies and remediation actions.",
        "Assessment of the component auditor's experience with the relevant industry, accounting standards, and applicable regulatory requirements.",
        "Evaluation of the component auditor's quality control system, including peer review results, professional liability insurance coverage, and independence monitoring procedures.",
        "For first-time component auditors, a mandatory pre-engagement site visit or virtual assessment by a member of the GET.",
    ])

    pdf.section_heading("6", "Communication Requirements")
    pdf.sub_heading("6.1", "Communications with Component Auditors")
    pdf.body(
        "Effective two-way communication between the GET and component auditors is essential to "
        "the quality of the group audit. The GET establishes a communication protocol at the outset "
        "of the engagement that defines:"
    )
    pdf.bullet_list([
        "Primary and escalation contacts on both the GET and component auditor sides.",
        "Required communications: matters that must be communicated promptly regardless of timing (e.g., suspected fraud, going concern doubt, material weaknesses, non-compliance with laws or regulations).",
        "Periodic communications: regular updates on fieldwork status, emerging issues, and timing adjustments.",
        "Secure communication channels for the transmission of confidential client information and audit documentation.",
    ])

    pdf.sub_heading("6.2", "Communications with Group and Component Management")
    pdf.body(
        "The group engagement partner communicates with group management on matters affecting the "
        "group audit opinion, including aggregate misstatements, significant accounting policy "
        "inconsistencies across components, and consolidation adjustments. Component auditors "
        "communicate with component management on matters specific to the component audit, with "
        "copies to the GET for significant items."
    )

    pdf.sub_heading("6.3", "Communications with Those Charged with Governance")
    pdf.body(
        "The group engagement partner communicates with the group audit committee on the following "
        "matters specific to the group audit:"
    )
    pdf.bullet_list([
        "An overview of the group audit approach, including the type of work to be performed on significant components.",
        "The identity of component auditors and any concerns about their competence or independence.",
        "Limitations on the GET's access to component information or component auditors.",
        "Instances of fraud, non-compliance, or significant internal control deficiencies identified at the component level.",
        "The group engagement partner's evaluation of the aggregate effect of unadjusted misstatements identified across components.",
    ])

    pdf.section_heading("7", "Consolidation Procedures")
    pdf.body(
        "The GET performs audit procedures on the consolidation process, including:"
    )
    pdf.bullet_list([
        "Evaluating whether the consolidation accounting policies are in accordance with the applicable financial reporting framework (ASC 810 / IFRS 10) and have been applied consistently.",
        "Testing the mathematical accuracy of the consolidation schedule and agreeing individual component trial balances to component auditor reporting packages.",
        "Evaluating the completeness, accuracy, and authorization of intercompany transactions and confirming that all intercompany balances, transactions, profits, and losses have been appropriately eliminated.",
        "Assessing the appropriateness of consolidation adjustments, including those related to business combinations (ASC 805), equity method investments (ASC 323), foreign currency translation (ASC 830), and non-controlling interests.",
        "Evaluating whether the group financial statements include all required disclosures related to the consolidation, including information about non-controlling interests, restrictions on net assets, and variable interest entities.",
    ])

    pdf.section_heading("8", "Documentation Standards")
    pdf.body(
        "The group audit engagement file must include the following documentation, in addition to "
        "the standard engagement file contents required by PCAOB AS 1215:"
    )
    pdf.bullet_list([
        "The component scoping analysis and rationale for the classification of each component.",
        "Component materiality calculations and the basis for any adjustments to the allocation model.",
        "Group Audit Instructions issued to each component auditor.",
        "The evaluation of each component auditor's competence and independence.",
        "A record of the GET's supervision and review activities, including summaries of site visits, planning calls, and review meetings.",
        "Component auditor reporting packages and the GET's evaluation of each package.",
        "The consolidation audit program and results of consolidation procedures.",
        "A summary of all component-level misstatements and their aggregate effect on the group financial statements.",
    ])

    pdf.output(os.path.join(OUTPUT_DIR, "group_audit_methodology.pdf"))
    print("  Created group_audit_methodology.pdf")


# =====================================================================
# Document 9 -- Going Concern Evaluation
# =====================================================================

def gen_going_concern_evaluation():
    pdf = MeridianPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.cover_page(
        "Going Concern\nEvaluation Procedures",
        "Evaluation Framework Under PCAOB AS 2415 / ISA 570\nManagement Assessment, Cash Flow Analysis, and Disclosure",
        "2.0",
        "February 20, 2026",
        "MA-AA-GC-2026-009",
    )

    pdf.add_page()
    pdf.section_heading("1", "Purpose and Regulatory Framework")
    pdf.body(
        "This document establishes the procedures for evaluating whether there is substantial doubt "
        "about an entity's ability to continue as a going concern for a reasonable period of time, "
        "which under U.S. GAAP (ASC 205-40) is defined as one year after the date the financial "
        "statements are issued (or available to be issued). The procedures apply to all audit "
        "engagements performed by Meridian & Associates LLP, regardless of entity size, industry, "
        "or listing status."
    )
    pdf.body(
        "The framework aligns with the following authoritative guidance:"
    )
    pdf.bullet_list([
        "PCAOB AS 2415 -- Consideration of an Entity's Ability to Continue as a Going Concern: Establishes the auditor's responsibility in a PCAOB audit to evaluate conditions and events that raise substantial doubt.",
        "ISA 570 (Revised) -- Going Concern: The international equivalent, applicable to non-SEC engagements, with a broader look-forward period and different reporting requirements.",
        "ASC 205-40 -- Presentation of Financial Statements -- Going Concern: Management's responsibility to evaluate going concern and provide required disclosures under U.S. GAAP.",
        "ASC 205-40-50 -- Disclosure requirements when conditions or events raise substantial doubt about an entity's ability to continue as a going concern, including management's evaluation and plans.",
    ])

    pdf.section_heading("2", "Identifying Conditions and Events")
    pdf.sub_heading("2.1", "Risk Indicators Requiring Evaluation")
    pdf.body(
        "The engagement team evaluates whether conditions or events, considered in the aggregate, "
        "raise substantial doubt about the entity's ability to continue as a going concern. The "
        "following categories of indicators are assessed at planning, during fieldwork, and at the "
        "conclusion of the audit:"
    )
    pdf.bullet_list([
        "Financial Indicators: Negative trends in key financial metrics -- recurring operating losses, working capital deficiencies, negative operating cash flows, adverse key financial ratios (e.g., debt-to-equity, interest coverage, current ratio below covenant thresholds), inability to obtain financing for essential capital expenditures.",
        "Operational Indicators: Loss of a key customer, supplier, or license; uninsured or underinsured catastrophic losses; labor shortages or work stoppages; dependence on the success of a single product or project; material supply chain disruptions.",
        "External Indicators: Legal proceedings, regulatory actions, or tax assessments that could jeopardize continued operations; loss of a key patent or franchise; changes in legislation or governmental policy adversely affecting the entity (e.g., tariffs, sanctions, environmental regulations).",
        "Debt and Covenant Indicators: Default on debt obligations, breach of debt covenants without waiver, denial of usual trade credit by suppliers, renegotiation of debt terms with less favorable provisions, approaching maturity of debt without realistic refinancing prospects.",
    ])

    pdf.sub_heading("2.2", "Information Sources")
    pdf.body(
        "The engagement team draws on the following sources when identifying going concern indicators:"
    )
    pdf.bullet_list([
        "Interim financial information available subsequent to the balance sheet date.",
        "Budgets, forecasts, and cash flow projections prepared by management.",
        "Minutes of board of directors, audit committee, and finance committee meetings.",
        "Publicly available information: analyst reports, credit rating agency actions, SEC filings, regulatory orders, and press coverage.",
        "Inquiry of management, including the CEO, CFO, and legal counsel regarding plans to address adverse conditions.",
        "Inquiry of the entity's legal counsel regarding litigation, claims, and assessments.",
        "Meridian's proprietary fraud risk model (for indicators of financial stress that correlate with going concern risk).",
    ])

    pdf.section_heading("3", "Evaluating Management's Assessment")
    pdf.body(
        "Under ASC 205-40, management is required to evaluate whether there are conditions or "
        "events that raise substantial doubt about the entity's ability to continue as a going "
        "concern. The engagement team evaluates the following aspects of management's assessment:"
    )
    pdf.bullet_list([
        "Completeness: Whether management has identified all relevant conditions and events, including those identified by the audit team that management may not have considered.",
        "Reasonableness of Assumptions: Whether the key assumptions underlying management's cash flow projections and mitigation plans are reasonable and supportable. The team applies professional skepticism to management's estimates of future revenue growth, cost reductions, asset dispositions, and refinancing capabilities.",
        "Feasibility of Management's Plans: Whether management's plans to mitigate the adverse conditions are both feasible and likely to be effectively implemented within the relevant time frame. Plans that depend on actions by third parties (e.g., new financing, waivers from lenders, sales of business units) are evaluated for the probability of execution.",
        "Historical Accuracy: Comparison of management's prior-period forecasts to actual results to assess the reliability of management's projections.",
    ])

    pdf.section_heading("4", "Cash Flow Analysis Procedures")
    pdf.body(
        "Cash flow analysis is the cornerstone of the going concern evaluation. The engagement "
        "team performs the following procedures on management's cash flow projections:"
    )
    pdf.bullet_list([
        "Obtain management's detailed cash flow projections for at least the 12-month period following the expected financial statement issuance date. Projections should be presented on a monthly or weekly basis where liquidity is tight.",
        "Trace key assumptions to supporting evidence: revenue forecasts to signed contracts and backlog reports, cost assumptions to recent actual expenditures, capital expenditure plans to board-approved budgets, and debt service to loan agreements.",
        "Perform sensitivity analysis on key assumptions. As a minimum, the team models a downside scenario using assumptions 15-25% less favorable than management's base case for revenue and 10-15% more unfavorable for costs. If the entity remains viable under reasonable downside scenarios, the going concern risk is reduced.",
        "Evaluate the adequacy of available financing: verify borrowing availability under existing credit facilities (including compliance with borrowing base and financial covenant requirements), assess the probability of refinancing maturing debt, and consider the entity's access to capital markets.",
        "Assess the timing and amount of discretionary cash flows: evaluate management's ability and willingness to defer discretionary expenditures (capital investments, share repurchases, dividends) to preserve liquidity.",
    ])

    pdf.section_heading("5", "Debt Covenant Review")
    pdf.body(
        "Debt covenant compliance is a critical element of the going concern evaluation. The "
        "engagement team performs the following procedures:"
    )
    pdf.bullet_list([
        "Obtain and read all significant debt agreements, including term loans, revolving credit facilities, private placement notes, bond indentures, and capital lease obligations.",
        "Identify all financial and non-financial covenants, including maintenance covenants (tested periodically) and incurrence covenants (tested at the time of specified events).",
        "Recalculate covenant compliance ratios as of the balance sheet date and for each projected measurement date within the look-forward period.",
        "Evaluate projected covenant compliance under both management's base case and the auditor's downside scenario. Identify periods where covenant breaches are projected or reasonably possible.",
        "For existing covenant violations: obtain and review waiver letters from lenders, assessing whether the waiver covers a sufficient period and whether the entity can comply with any modified covenant terms.",
        "Assess cross-default provisions that could accelerate other debt obligations if a covenant is breached on any single agreement.",
    ])

    pdf.section_heading("6", "Subsequent Events Consideration")
    pdf.body(
        "Events occurring after the balance sheet date but before the issuance of the financial "
        "statements may provide evidence relevant to the going concern evaluation. The engagement "
        "team performs the following subsequent events procedures specifically related to going concern:"
    )
    pdf.bullet_list([
        "Review interim financial statements, management accounts, and board meeting minutes for the post-balance-sheet period.",
        "Inquire of management regarding new debt defaults, loss of customers or suppliers, regulatory actions, and significant litigation developments.",
        "Review subsequent financing activity: new credit facilities, debt issuances, equity raises, or asset sales that may alleviate going concern doubt.",
        "Consider subsequent adverse events: bankruptcy filings by significant customers, unfavorable court rulings, loss of a key contract, or macroeconomic developments that worsen the entity's outlook.",
        "Evaluate whether subsequent events represent Type I events (conditions existed at the balance sheet date) or Type II events (conditions arose after the balance sheet date) and their implications for going concern disclosure.",
    ])

    pdf.section_heading("7", "Disclosure Requirements and Audit Reporting")
    pdf.sub_heading("7.1", "Substantial Doubt Exists -- Mitigated by Management's Plans")
    pdf.body(
        "If, after considering management's plans, the auditor concludes that substantial doubt "
        "is alleviated, the entity is required under ASC 205-40-50-12 to disclose: (a) the "
        "conditions or events that raised the doubt, (b) management's evaluation of the "
        "significance of those conditions, and (c) management's plans that alleviated the doubt. "
        "The auditor evaluates the adequacy of these disclosures. No modification to the auditor's "
        "report is required under U.S. GAAS, although the engagement team should consider whether "
        "an emphasis-of-matter paragraph is appropriate."
    )

    pdf.sub_heading("7.2", "Substantial Doubt Exists -- Not Mitigated")
    pdf.body(
        "If substantial doubt remains after considering management's plans, the entity must "
        "disclose the conditions, management's evaluation, and management's plans (ASC 205-40-50-13 "
        "through 50-14). Additionally, the entity must include a statement that there is substantial "
        "doubt about its ability to continue as a going concern within one year. The auditor's "
        "report must include an emphasis-of-matter paragraph under PCAOB AS 2415.12 or a 'Material "
        "Uncertainty Related to Going Concern' section under ISA 570."
    )

    pdf.sub_heading("7.3", "Inadequate Disclosure")
    pdf.body(
        "If the entity fails to include required going concern disclosures, the auditor considers "
        "the impact on the audit opinion. A material omission of required disclosures ordinarily "
        "results in a qualified or adverse opinion."
    )

    pdf.section_heading("8", "Communication with the Audit Committee")
    pdf.body(
        "The engagement partner communicates the following matters to the audit committee in "
        "connection with the going concern evaluation:"
    )
    pdf.bullet_list([
        "The conditions or events identified that raise substantial doubt.",
        "The engagement team's evaluation of management's assessment and plans.",
        "The key assumptions and their sensitivity in management's cash flow projections.",
        "The expected effect on the auditor's report, including any emphasis-of-matter or going concern paragraphs.",
        "Recommendations regarding the adequacy of the entity's going concern disclosures.",
        "Where applicable, the effect of going concern uncertainties on other audit areas, including impairment of long-lived assets (ASC 360), recoverability of deferred tax assets (ASC 740), and fair value measurements (ASC 820).",
    ])
    pdf.body(
        "Communication with the audit committee is documented in the engagement file and referenced "
        "in the firm's AS 1301 communication letter. For SEC registrant audits, the engagement "
        "partner also considers whether the going concern uncertainty represents a Critical Audit "
        "Matter (CAM) requiring disclosure in the auditor's report under PCAOB AS 3101."
    )

    pdf.section_heading("9", "Engagement File Documentation")
    pdf.body(
        "The engagement team documents the going concern evaluation in a standalone memorandum "
        "(Form MA-GC-001) that includes:"
    )
    pdf.bullet_list([
        "A description of the conditions and events identified, including their individual and aggregate significance.",
        "The engagement team's evaluation of management's assessment and the evidence supporting the evaluation.",
        "A summary of the cash flow analysis, including base case and downside scenario results.",
        "The debt covenant compliance analysis and evaluation of waiver adequacy (if applicable).",
        "A description of subsequent events considered and their impact on the evaluation.",
        "The engagement team's conclusion on whether substantial doubt exists and whether it is alleviated by management's plans.",
        "The basis for the engagement team's determination regarding the effect on the auditor's report.",
        "Documentation of communications with the audit committee and management regarding the going concern evaluation.",
    ])

    pdf.output(os.path.join(OUTPUT_DIR, "going_concern_evaluation.pdf"))
    print("  Created going_concern_evaluation.pdf")


# =====================================================================
# Main
# =====================================================================

if __name__ == "__main__":
    print("Generating Meridian & Associates LLP audit documents...")
    gen_audit_transition_plan()
    gen_risk_based_methodology()
    gen_independence_policy()
    gen_partner_rotation()
    gen_audit_quality()
    gen_technology_integration()
    gen_specialist_framework()
    gen_group_audit_methodology()
    gen_going_concern_evaluation()
    print("\nAll 9 documents generated successfully.")
