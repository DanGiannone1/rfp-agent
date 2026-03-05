"""Fix all 6 case study PDFs: rewrite energy/retail teams, expand 4 shorter ones."""

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
        elif self.client_confidential:
            self.set_font("Helvetica", "B", 7)
            self.set_text_color(180, 0, 0)
            self.cell(0, 5, "CLIENT CONFIDENTIAL - BLINDED", align="R")
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
        if self.client_confidential:
            self.set_font("Helvetica", "B", 12)
            self.set_text_color(180, 0, 0)
            self.cell(0, 8, "CLIENT CONFIDENTIAL - BLINDED", align="C")
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
            "distribution, or disclosure of this material is strictly prohibited. The information contained "
            "herein is provided for informational purposes only and does not constitute a binding offer or agreement.",
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

    def add_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            n = len(headers)
            col_widths = [190 / n] * n
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(240, 244, 248)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell_text in enumerate(row):
                self.cell(col_widths[i], 7, str(cell_text), border=1, fill=True, align="C")
            self.ln()
            fill = not fill
        self.ln(3)

    def results_table(self, headers, rows, col_widths=None):
        """Render results table matching original case study style."""
        if col_widths is None:
            col_widths = [60, 42, 42, 46]
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(40, 40, 40)
        for i, row in enumerate(rows):
            fill = i % 2 == 0
            self.set_fill_color(235, 240, 248)
            for j, val in enumerate(row):
                self.set_font("Helvetica", "B" if j == 0 else "", 9)
                self.cell(col_widths[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
            self.ln()
        self.ln(4)


# =============================================================================
# 1. ENERGY CASE STUDY (full rewrite of team composition)
# =============================================================================

def generate_case_study_energy():
    pdf = MeridianPDF(
        "Case Study: Energy Sector",
        "Streamlining Regulatory Compliance and Financial Reporting\nfor a Major Upstream Oil & Gas Producer",
        client_confidential=True,
    )
    pdf.cover_page(version="2.2", date="March 2026")

    # --- Page 2: Executive Summary ---
    pdf.add_page()
    pdf.section_heading("1. Executive Summary")
    pdf.body_text(
        "Meridian & Associates LLP was engaged by a Fortune 500 exploration and production (E&P) company "
        "to deliver an integrated suite of assurance, tax, and advisory services spanning a three-year "
        "engagement period. The client, one of the largest independent upstream oil and gas producers in "
        "North America, operates across multiple prolific basins including the Permian, Eagle Ford, "
        "Bakken, and DJ Basin, with approximately $18 billion in annual revenue and over 8,500 employees."
    )
    pdf.body_text(
        "The engagement encompassed an integrated financial statement audit, SOX Section 404 internal "
        "controls assessment, SEC reporting advisory, and a comprehensive tax provision automation "
        "initiative. Meridian deployed a cross-functional team of 47 professionals representing our "
        "Assurance, Tax, and Advisory service lines, working in close coordination with the client's "
        "finance, accounting, tax, and IT departments across six office locations."
    )
    pdf.body_text(
        "This case study provides a detailed overview of the engagement challenges, Meridian's phased "
        "approach, specialist team composition, and the quantifiable business outcomes delivered to the "
        "client over the course of the relationship."
    )

    pdf.ln(2)
    pdf.section_heading("Engagement at a Glance", level=2)
    pdf.add_table(
        ["Metric", "Detail"],
        [
            ["Client Revenue", "$18.2B (FY 2025)"],
            ["Industry", "Oil & Gas - Upstream E&P"],
            ["Engagement Duration", "36 months (2023-2026)"],
            ["Team Size", "47 professionals (peak)"],
            ["Service Lines", "Audit, Tax, Advisory"],
            ["Total Engagement Value", "$6.8M (cumulative)"],
            ["Client Satisfaction", "4.8 / 5.0 (annual survey)"],
        ],
        col_widths=[60, 130],
    )

    # --- Page 3: Client Background & Challenges ---
    pdf.add_page()
    pdf.section_heading("2. Client Background")
    pdf.body_text(
        "The client is a publicly traded independent E&P company headquartered in Houston, Texas, with "
        "operations spanning the continental United States and select international assets in Canada and "
        "Colombia. The company's asset portfolio includes approximately 2.1 million net acres across "
        "four major basins, with proved reserves of 1.8 billion barrels of oil equivalent (BOE). Daily "
        "production averages approximately 485,000 BOE/day, split roughly 62% oil and condensate, 23% "
        "natural gas, and 15% natural gas liquids (NGLs)."
    )
    pdf.body_text(
        "The company completed two significant acquisitions in the 18 months preceding the engagement "
        "- a $3.2 billion bolt-on acquisition in the Permian Basin and a $1.1 billion entry into the "
        "DJ Basin - which added complexity to the financial reporting environment. Additionally, the "
        "company had recently transitioned its accounting methodology from the full-cost method to the "
        "successful-efforts method, a change that required extensive retrospective adjustments and "
        "ongoing judgment-intensive accounting determinations."
    )

    pdf.section_heading("3. Key Challenges")
    pdf.section_heading("3.1 Commodity Price Volatility and Financial Reporting", level=2)
    pdf.body_text(
        "The client's financial results are highly sensitive to commodity price fluctuations. WTI crude "
        "oil prices ranged from $62 to $93 per barrel during the engagement period, while Henry Hub "
        "natural gas prices varied between $1.80 and $5.40 per MMBtu. This volatility created significant "
        "challenges in several areas:"
    )
    pdf.bullet("Impairment testing of long-lived assets under ASC 360, requiring quarterly assessment of "
               "proved and unproved properties across four basins with differing economic profiles")
    pdf.bullet("Derivative financial instrument accounting under ASC 815, with the client maintaining a "
               "hedging program covering approximately 65% of near-term production using a mix of swaps, "
               "collars, and three-way collars")
    pdf.bullet("Revenue recognition under ASC 606 for complex marketing and transportation arrangements, "
               "including take-or-pay contracts, index-based pricing with quality differentials, and "
               "intercompany elimination of midstream revenues")
    pdf.bullet("Going-concern and liquidity assessments during periods of depressed commodity prices, "
               "particularly given the company's $4.5 billion revolving credit facility with borrowing "
               "base redetermination provisions")

    pdf.section_heading("3.2 Asset Retirement Obligation (ARO) Estimation", level=2)
    pdf.body_text(
        "The client operates approximately 12,400 producing wells across its portfolio, each requiring "
        "individual ARO estimation under ASC 410-20. The complexity of ARO estimation was compounded by "
        "several factors:"
    )
    pdf.bullet("Multi-jurisdictional regulatory requirements spanning Texas, New Mexico, North Dakota, "
               "Colorado, Wyoming, and two Canadian provinces, each with distinct plugging and abandonment standards")
    pdf.bullet("Wide variation in estimated settlement costs ranging from $35,000 per well for shallow "
               "vertical wells to $850,000 for deep horizontal wells with multi-stage completions")
    pdf.bullet("Discount rate determination challenges in a rising interest rate environment, requiring "
               "regular reassessment of credit-adjusted risk-free rates")
    pdf.bullet("Legacy liabilities from the two recent acquisitions, where historical ARO records were "
               "incomplete or based on outdated cost assumptions")

    pdf.section_heading("3.3 Full-Cost to Successful-Efforts Transition", level=2)
    pdf.body_text(
        "The client's recent transition from the full-cost method to the successful-efforts method of "
        "accounting for oil and gas properties under ASC 932 introduced pervasive complexity. Under the "
        "full-cost method, all exploration costs had been capitalized in a single cost center. The "
        "transition required the client to retrospectively identify and expense exploration costs for "
        "dry holes and geological/geophysical expenditures that did not result in proved reserves, "
        "spanning a 15-year historical period encompassing over 4,200 individual well files."
    )
    pdf.body_text(
        "This transition also required recalculation of depletion under the unit-of-production method "
        "at a property-by-property level rather than the full-cost pool level, necessitating detailed "
        "reserve allocation and cost assignment for each of the client's approximately 340 distinct "
        "producing properties."
    )

    # --- Meridian's Approach ---
    pdf.add_page()
    pdf.section_heading("4. Meridian's Approach")
    pdf.body_text(
        "Meridian structured the engagement as a three-phase program, with overlapping workstreams to "
        "maximize efficiency and minimize disruption to the client's operations. Our approach leveraged "
        "deep industry expertise, purpose-built analytical tools, and a collaborative delivery model "
        "that embedded our professionals alongside the client's teams."
    )

    pdf.section_heading("4.1 Phase 1: Assessment & Stabilization (Months 1-6)", level=2)
    pdf.body_text(
        "The initial phase focused on gaining a comprehensive understanding of the client's financial "
        "reporting environment, identifying control deficiencies, and establishing a remediation roadmap."
    )
    pdf.bold_bullet("Financial Reporting Diagnostic",
        "Conducted a 6-week diagnostic assessment of the client's close process, identifying 23 "
        "bottlenecks that contributed to a 22-business-day close cycle. Key findings included manual "
        "journal entry processes for intercompany eliminations, lack of automated reconciliation for "
        "revenue accruals, and inconsistent application of the successful-efforts method across basins.")
    pdf.bold_bullet("SOX 404 Scoping & Risk Assessment",
        "Performed top-down risk assessment identifying 14 significant accounts and 8 relevant assertions. "
        "Identified 187 key controls across 12 business processes, with 34 controls requiring "
        "remediation or redesign. Highest-risk areas included production revenue, derivative accounting, "
        "and property cost capitalization.")
    pdf.bold_bullet("Tax Provision Gap Analysis",
        "Evaluated the client's tax provision process, which relied on a combination of spreadsheets, "
        "legacy Corptax modules, and manual calculations. Identified $2.8 million in potential tax "
        "overpayments related to incorrectly classified intangible drilling costs (IDCs) and suboptimal "
        "utilization of percentage depletion allowances.")
    pdf.bold_bullet("Technology Assessment",
        "Mapped the client's financial reporting technology stack, including SAP S/4HANA (core ERP), "
        "Quorum (production accounting), Allegro (commodity trading/risk management), and BlackLine "
        "(account reconciliation). Identified integration gaps and data quality issues that contributed "
        "to manual workarounds.")

    pdf.section_heading("4.2 Phase 2: Execution & Remediation (Months 7-24)", level=2)
    pdf.body_text(
        "The execution phase represented the core of the engagement, with concurrent workstreams "
        "addressing audit, controls remediation, and tax automation."
    )
    pdf.bold_bullet("Integrated Audit Execution",
        "Delivered integrated financial statement audits for FY 2023 and FY 2024, with a combined "
        "team of 28 assurance professionals including 4 partners and 6 managers. Deployed our "
        "proprietary MeridianAI analytics platform to analyze 100% of journal entries (approximately "
        "1.2 million annually) for anomaly detection, replacing the prior auditor's sample-based approach.")
    pdf.bold_bullet("SOX Remediation Program",
        "Worked with the client to remediate 34 identified control deficiencies, including 6 material "
        "weaknesses and 11 significant deficiencies. Designed and implemented automated controls for "
        "revenue recognition, lease accounting, and intercompany transactions. Conducted walkthroughs "
        "and operating effectiveness testing for all 187 key controls across four quarterly testing cycles.")
    pdf.bold_bullet("ARO Revaluation Initiative",
        "Assembled a specialist team including petroleum engineers and environmental specialists to "
        "revalue ARO obligations for all 12,400 wells. Developed a proprietary statistical model that "
        "incorporated basin-specific cost data, regulatory requirements, and historical plugging and "
        "abandonment costs from state databases. The revaluation resulted in a net adjustment of $142 "
        "million to the ARO liability, with corresponding adjustments to asset carrying values and "
        "accretion expense.")
    pdf.bold_bullet("Tax Provision Automation",
        "Implemented OneSource Tax Provision integrated with SAP S/4HANA, replacing the legacy "
        "spreadsheet-based process. Configured the system for 42 tax jurisdictions (federal, 38 states, "
        "3 Canadian provinces), including automated calculation of percentage depletion, IDC deductions, "
        "and enhanced oil recovery credits. Developed automated book-to-tax difference tracking for over "
        "200 temporary differences.")

    pdf.add_page()
    pdf.section_heading("4.3 Phase 3: Optimization & Transition (Months 25-36)", level=2)
    pdf.body_text(
        "The final phase focused on sustaining improvements, optimizing processes, and transitioning "
        "knowledge to the client's internal teams."
    )
    pdf.bold_bullet("Close Cycle Optimization",
        "Implemented a structured close calendar with automated task tracking, eliminating 14 of the 23 "
        "identified bottlenecks. Introduced parallel processing for basin-level close activities and "
        "automated the consolidation of intercompany transactions across 28 legal entities.")
    pdf.bold_bullet("SEC Reporting Enhancement",
        "Redesigned the client's SEC reporting process for Forms 10-K, 10-Q, and 8-K, including "
        "implementation of Workiva (formerly Wdesk) for collaborative document preparation and XBRL "
        "tagging. Reduced the SEC filing preparation timeline from 18 days to 11 days.")
    pdf.bold_bullet("Knowledge Transfer & Training",
        "Conducted 32 hours of structured training sessions covering successful-efforts accounting, "
        "derivative instrument accounting, and ARO estimation methodology. Delivered comprehensive "
        "process documentation including 47 updated accounting policies and 23 procedure manuals.")
    pdf.bold_bullet("Continuous Monitoring Framework",
        "Established a continuous monitoring program for key financial reporting controls, leveraging "
        "automated exception reporting and dashboard-based oversight. Transitioned monitoring "
        "responsibility to the client's internal audit team with ongoing advisory support.")

    # --- Team Composition (REWRITTEN with bio'd professionals) ---
    pdf.add_page()
    pdf.section_heading("5. Team Composition")
    pdf.body_text(
        "Meridian deployed a cross-functional team drawn from three service lines, with deep energy "
        "sector expertise at every level. The team was structured to provide continuous coverage across "
        "the client's six office locations while maintaining centralized quality oversight. The senior "
        "team drew on Meridian's deepest bench of industry specialists, led by our Energy & Utilities "
        "Practice Lead Patricia Hoffman."
    )

    pdf.add_table(
        ["Role", "Name", "Service Line", "Specialization", "Allocation"],
        [
            ["Lead Engagement Partner", "Patricia Hoffman, CPA", "Energy & Utilities", "E&P Audit / SOX", "40%"],
            ["Advisory Partner", "James O'Sullivan, CPA", "Manufacturing & SCM", "Operations / Controls", "25%"],
            ["Sr. Manager - Tax", "Rachel Okonkwo, CPA, MST", "Tax", "Tax Provision", "70%"],
            ["Sr. Manager - SALT", "Sophia Vasquez, CPA, JD", "Tax", "SALT / Multi-State", "50%"],
            ["Sr. Manager - Technology", "David Kim, PMP, SAP", "Advisory", "ERP / SAP S/4HANA", "60%"],
            ["Manager - Risk", "Maria Santos, CPA, CIA", "Advisory", "Internal Controls", "80%"],
            ["Sr. Consultant - SAP", "Marcus Wright", "Consulting", "SAP FICO", "100%"],
            ["Sr. Consultant - SAP", "Kwame Asante", "Consulting", "SAP S/4HANA FICO", "100%"],
            ["Consultant - Data Eng.", "Jessica Huang", "Consulting", "Data Engineering", "90%"],
            ["Staff - PMO", "Derek Williams", "Advisory", "PMO Coordination", "100%"],
        ],
        col_widths=[38, 38, 28, 42, 22],
    )
    pdf.body_text(
        "In addition to the senior team listed above, the engagement was supported by 12 senior "
        "associates, 18 associates, and 7 staff-level professionals. Total engagement hours over the "
        "36-month period were approximately 68,000, with peak staffing of 47 professionals during "
        "year-end audit execution periods."
    )

    pdf.section_heading("Team Qualifications", level=2)
    pdf.bullet("100% of partners and senior managers hold active CPA licenses")
    pdf.bullet("Average of 16 years of energy sector experience among partners and managers")
    pdf.bullet("Patricia Hoffman brings CEM (Certified Energy Manager) credentials and Six Sigma Black Belt certification with deep upstream E&P expertise")
    pdf.bullet("James O'Sullivan provides operational excellence perspective from 26 years in manufacturing and supply chain, with direct relevance to field operations optimization")
    pdf.bullet("Rachel Okonkwo and Sophia Vasquez bring complementary tax expertise spanning federal provision and multi-state SALT, critical for the client's 42-jurisdiction tax footprint")
    pdf.bullet("David Kim's 11 full-lifecycle SAP S/4HANA implementations ensured seamless ERP integration for the tax provision automation workstream")
    pdf.bullet("Marcus Wright and Kwame Asante provided dedicated SAP FICO configuration support, with Kwame holding SAP S/4HANA certification")
    pdf.bullet("Jessica Huang built the data pipelines connecting Quorum, Allegro, and SAP for the MeridianAI analytics platform")

    # --- Outcomes ---
    pdf.add_page()
    pdf.section_heading("6. Quantifiable Outcomes")
    pdf.body_text(
        "The engagement delivered measurable, sustained improvements across the client's financial "
        "reporting, compliance, and tax functions. The following outcomes were validated through "
        "independent measurement and client confirmation."
    )

    pdf.section_heading("6.1 Financial Close & Reporting", level=2)
    pdf.add_table(
        ["Metric", "Before Meridian", "After Meridian", "Improvement"],
        [
            ["Close Cycle (business days)", "22 days", "14 days", "35% reduction"],
            ["SEC Filing Prep Time", "18 days", "11 days", "39% reduction"],
            ["Manual Journal Entries", "2,340 / quarter", "890 / quarter", "62% reduction"],
            ["Restatement Risk Items", "14 identified", "0 remaining", "100% resolved"],
            ["Audit Adjustments (Year 1 vs 3)", "23 proposed", "4 proposed", "83% reduction"],
        ],
        col_widths=[50, 45, 45, 40],
    )

    pdf.section_heading("6.2 SOX 404 Compliance", level=2)
    pdf.add_table(
        ["Metric", "Before Meridian", "After Meridian", "Improvement"],
        [
            ["Material Weaknesses", "6", "0", "100% remediated"],
            ["Significant Deficiencies", "11", "1", "91% remediated"],
            ["Control Deficiencies", "34 total", "3 remaining", "91% resolved"],
            ["Automated Controls (%)", "28%", "67%", "+39 pct points"],
            ["Testing Exceptions", "42 / cycle", "7 / cycle", "83% reduction"],
        ],
        col_widths=[50, 45, 45, 40],
    )

    pdf.section_heading("6.3 Tax & Cost Savings", level=2)
    pdf.add_table(
        ["Category", "Amount", "Description"],
        [
            ["R&D Tax Credits Identified", "$4.2M", "Previously unclaimed credits for drilling technology innovation"],
            ["IDC Reclassification Benefit", "$2.8M", "Corrected classification of intangible drilling costs"],
            ["Percentage Depletion Recovery", "$1.4M", "Optimized depletion method elections across properties"],
            ["Tax Provision Efficiency", "$380K/yr", "Annual cost savings from automated tax provision process"],
            ["Audit Fee Reduction (Year 3)", "$420K", "Efficiency gains shared with client through reduced fees"],
        ],
        col_widths=[55, 25, 100],
    )

    # --- Timeline ---
    pdf.add_page()
    pdf.section_heading("7. Engagement Timeline")
    pdf.add_table(
        ["Phase", "Period", "Key Milestones"],
        [
            ["Phase 1", "Jan - Jun 2023", "Diagnostic complete, SOX scoping, tax gap analysis"],
            ["Audit Y1", "Jul - Dec 2023", "FY 2023 integrated audit, initial SOX testing"],
            ["Phase 2a", "Jan - Jun 2024", "SOX remediation, tax automation implementation"],
            ["Audit Y2", "Jul - Dec 2024", "FY 2024 audit, ARO revaluation, controls retesting"],
            ["Phase 2b", "Jan - Jun 2025", "SEC reporting redesign, close optimization"],
            ["Audit Y3", "Jul - Dec 2025", "FY 2025 audit, clean SOX opinion achieved"],
            ["Phase 3", "Jan - Mar 2026", "Knowledge transfer, continuous monitoring handoff"],
        ],
        col_widths=[25, 40, 115],
    )

    pdf.section_heading("8. Client Testimonial")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6,
        '"Meridian\'s team brought a level of energy-sector expertise that we had not experienced with '
        'our prior auditors. Their ability to integrate audit, tax, and advisory services into a '
        'cohesive program saved us significant time and resources. The identification of $4.2 million '
        'in R&D credits alone justified the engagement economics, and the improvement in our close cycle '
        'has fundamentally changed how our finance organization operates."')
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, "- Chief Financial Officer, [Client Name Redacted]")
    pdf.ln(8)

    pdf.section_heading("9. Lessons Learned & Transferable Insights")
    pdf.bold_bullet("Early Integration Pays Dividends",
        "Co-locating audit, tax, and advisory teams from Day 1 reduced information asymmetry and "
        "eliminated an estimated 2,400 hours of duplicative data requests over the engagement.")
    pdf.bold_bullet("Technology-Enabled Audit Is Transformative",
        "Deploying MeridianAI for 100% journal entry testing replaced statistical sampling and "
        "identified 14 anomalous transactions in Year 1 that the prior sample-based approach had missed.")
    pdf.bold_bullet("Specialist Resources Drive Value",
        "The inclusion of petroleum engineers and environmental specialists on the ARO workstream "
        "produced a $142M revaluation that a generalist team would not have identified.")
    pdf.bold_bullet("Automation Requires Change Management",
        "The tax provision automation initiative required more change management effort than initially "
        "scoped. We added dedicated training resources in Phase 2, increasing the original training "
        "budget by 40% to ensure sustainable adoption.")

    path = os.path.join(OUTPUT_DIR, "case_study_energy.pdf")
    pdf.output(path)
    print(f"  Generated: {path}")


# =============================================================================
# 2. RETAIL CASE STUDY (full rewrite of team composition)
# =============================================================================

def generate_case_study_retail():
    pdf = MeridianPDF(
        "Case Study: Retail & Consumer",
        "Omnichannel Transformation and Revenue Recognition Overhaul\nfor a National Retailer",
        client_confidential=True,
    )
    pdf.cover_page(version="1.5", date="March 2026")

    # --- Executive Summary ---
    pdf.add_page()
    pdf.section_heading("1. Executive Summary")
    pdf.body_text(
        "Meridian & Associates LLP was engaged by a leading national specialty retailer to provide "
        "comprehensive advisory and assurance services related to the company's omnichannel transformation "
        "and the implementation of ASC 606 (Revenue from Contracts with Customers). The client operates "
        "over 450 retail locations across 42 states, a rapidly growing e-commerce platform (representing "
        "28% of total revenue and growing at 35% year-over-year), and a wholesale channel serving "
        "approximately 1,200 independent retail partners."
    )
    pdf.body_text(
        "With $3.2 billion in annual revenue, the client faced a complex set of revenue recognition "
        "challenges arising from multiple performance obligations, customer loyalty programs, gift card "
        "programs, sales return reserves, and promotional pricing structures. Concurrently, the company "
        "was undergoing a major technology transformation, migrating from a legacy point-of-sale system "
        "to a unified commerce platform, which created both opportunities and risks in the financial "
        "reporting environment."
    )
    pdf.body_text(
        "Meridian assembled a 32-person team combining retail industry specialists, technical accounting "
        "experts, data analytics professionals, and inventory management advisors. The engagement spanned "
        "24 months and delivered transformational improvements in revenue recognition accuracy, working "
        "capital management, and financial reporting efficiency."
    )

    pdf.section_heading("Engagement at a Glance", level=2)
    pdf.add_table(
        ["Metric", "Detail"],
        [
            ["Client Revenue", "$3.2B (FY 2025)"],
            ["Industry", "Specialty Retail (Omnichannel)"],
            ["Engagement Duration", "24 months (2024-2025)"],
            ["Team Size", "32 professionals (peak)"],
            ["Service Lines", "Advisory, Assurance, Tax"],
            ["Total Engagement Value", "$4.1M (cumulative)"],
            ["Client Satisfaction", "4.9 / 5.0 (annual survey)"],
        ],
        col_widths=[60, 130],
    )

    # --- Client Background ---
    pdf.add_page()
    pdf.section_heading("2. Client Background")
    pdf.body_text(
        "The client is a publicly traded specialty retailer headquartered in the Midwest, operating under "
        "three distinct retail banners across the value, mid-market, and premium segments. The company's "
        "product mix spans apparel (52%), home goods (28%), and beauty/wellness (20%), with a private-label "
        "portfolio representing approximately 40% of total sales. The company employs roughly 24,000 "
        "associates across its retail operations, distribution centers, and corporate headquarters."
    )
    pdf.body_text(
        "Key business characteristics relevant to the engagement included:"
    )
    pdf.bullet("A multi-banner loyalty program ('Meridian Rewards' - name changed) with approximately 18 million "
               "active members, representing 72% of total retail sales")
    pdf.bullet("Gift card programs across all three banners with approximately $145 million in outstanding "
               "gift card liabilities at any given time")
    pdf.bullet("A buy-online-pickup-in-store (BOPIS) program representing 12% of e-commerce orders, creating "
               "complex allocation questions for revenue by channel and location")
    pdf.bullet("A recently launched marketplace platform allowing third-party sellers, introducing "
               "principal-versus-agent revenue recognition considerations")
    pdf.bullet("Complex promotional structures including percentage-off coupons, buy-one-get-one (BOGO) "
               "promotions, tiered loyalty discounts, and employee discount programs")

    # --- Challenges ---
    pdf.section_heading("3. Key Challenges")
    pdf.section_heading("3.1 ASC 606 Revenue Recognition Complexity", level=2)
    pdf.body_text(
        "The client's revenue streams created a web of interrelated accounting challenges under ASC 606. "
        "The prior accounting treatment had been developed incrementally over 15 years and had not been "
        "comprehensively reassessed since the initial ASC 606 adoption in 2018. Specific issues included:"
    )
    pdf.bold_bullet("Loyalty Program (ASC 606-10-55-41 through 55-45)",
        "The loyalty program offered points redeemable for discounts, free products, and exclusive experiences. "
        "The existing accounting model allocated consideration to loyalty points using a residual approach, "
        "which did not comply with the relative standalone selling price method required by ASC 606. An "
        "estimated 23% of loyalty points expired unused (breakage), but the client had not developed a "
        "statistically robust breakage estimation model.")
    pdf.bold_bullet("Gift Card Breakage (ASC 606-10-55-46 through 55-49)",
        "The client recognized gift card breakage revenue only upon legal escheatment to state authorities, "
        "rather than proportionally as redemptions occur. This resulted in an estimated $12.4 million in "
        "deferred revenue that should have been recognized over prior periods under the proportional method.")
    pdf.bold_bullet("Returns Reserve Estimation",
        "The client's return rate varied significantly by channel (in-store: 8%, e-commerce: 22%, "
        "wholesale: 3%) and by product category. The existing returns reserve methodology used a blended "
        "rate that did not capture channel-specific or seasonal patterns, resulting in material "
        "quarter-to-quarter fluctuations in gross margin.")

    pdf.add_page()
    pdf.section_heading("3.2 Omnichannel Revenue Allocation", level=2)
    pdf.body_text(
        "The convergence of physical and digital retail created novel revenue allocation challenges:"
    )
    pdf.bullet("BOPIS orders: Revenue allocated between e-commerce and store channels for internal "
               "reporting, with inventory transfer and fulfillment cost implications")
    pdf.bullet("Ship-from-store orders: Store inventory used to fulfill e-commerce orders, requiring "
               "real-time inventory adjustment and revenue channel attribution")
    pdf.bullet("Marketplace transactions: Determination of principal versus agent status for approximately "
               "$180 million in gross merchandise value (GMV) flowing through the third-party marketplace")
    pdf.bullet("Bundled promotions: Cross-banner promotional offers requiring allocation of transaction "
               "price across multiple performance obligations and legal entities")
    pdf.bullet("Subscription box program: Monthly curated product boxes creating distinct performance "
               "obligations for product delivery and styling services")

    pdf.section_heading("3.3 Inventory and Working Capital Challenges", level=2)
    pdf.body_text(
        "The client's inventory management practices were contributing to significant working capital "
        "inefficiency. Inventory turns had declined from 4.8x to 3.9x over three years, and markdown "
        "rates had increased from 28% to 34% of gross revenue. Excess and obsolete inventory reserves "
        "had grown to $87 million, representing 11% of total inventory. The client's aging distribution "
        "center technology and manual allocation processes were unable to support the real-time inventory "
        "visibility required for effective omnichannel operations."
    )

    # --- Approach ---
    pdf.add_page()
    pdf.section_heading("4. Meridian's Approach")

    pdf.section_heading("4.1 Phase 1: Data-Driven Assessment (Months 1-4)", level=2)
    pdf.body_text(
        "Meridian's approach began with a comprehensive data-driven assessment designed to quantify the "
        "magnitude of revenue recognition issues and inventory inefficiencies before proposing solutions."
    )
    pdf.bold_bullet("Transaction-Level Revenue Analysis",
        "Analyzed 142 million individual point-of-sale transactions from the prior 36 months, "
        "encompassing all channels, banners, and product categories. Used MeridianAI's pattern "
        "recognition capabilities to identify 47 distinct revenue stream archetypes requiring unique "
        "ASC 606 treatment.")
    pdf.bold_bullet("Loyalty Program Deep Dive",
        "Performed actuarial-grade analysis of loyalty program data, including issuance patterns, "
        "redemption curves, breakage history, and member lifetime value segmentation. Developed a "
        "stochastic breakage estimation model with 95% confidence intervals that improved upon the "
        "client's deterministic approach.")
    pdf.bold_bullet("Gift Card Liability Reconstruction",
        "Reconstructed gift card liability from individual card-level transaction data spanning 7 years. "
        "Applied jurisdiction-specific escheatment rules for all 42 operating states and developed a "
        "proportional recognition model based on observed redemption patterns stratified by card type "
        "(physical, digital, promotional).")
    pdf.bold_bullet("Inventory Health Assessment",
        "Conducted SKU-level analysis of 84,000 active SKUs across all locations, assessing sell-through "
        "rates, aging profiles, markdown trajectories, and seasonal demand patterns. Identified $23 "
        "million in excess inventory that could be liquidated through targeted markdown strategies.")

    pdf.section_heading("4.2 Phase 2: System Integration & Implementation (Months 5-16)", level=2)
    pdf.body_text(
        "The implementation phase ran concurrently with the client's unified commerce platform migration, "
        "allowing Meridian to influence system configuration decisions that would impact financial reporting."
    )
    pdf.bold_bullet("Revenue Recognition Engine Configuration",
        "Designed and configured a revenue recognition subledger within the client's new Oracle Cloud "
        "ERP, implementing automated allocation of transaction price across identified performance "
        "obligations. The engine processes approximately 450,000 transactions daily with same-day "
        "revenue recognition classification.")
    pdf.bold_bullet("Loyalty Accounting Redesign",
        "Implemented a standalone selling price (SSP) allocation model for loyalty points, utilizing "
        "the adjusted market assessment approach. Integrated the model with the POS system to calculate "
        "and record the loyalty obligation at the point of sale in real time.")
    pdf.bold_bullet("Returns Reserve Automation",
        "Developed a machine-learning-based returns prediction model incorporating channel, product "
        "category, price point, seasonality, and promotional intensity as features. The model reduced "
        "returns reserve estimation error from +/- 18% to +/- 4% on a quarterly basis.")
    pdf.bold_bullet("Inventory Optimization Advisory",
        "Implemented demand-sensing analytics for the client's top 2,000 SKUs (representing 65% of "
        "revenue), enabling dynamic allocation of inventory across channels and locations. Redesigned "
        "the markdown optimization framework using price elasticity modeling.")

    pdf.add_page()
    pdf.section_heading("4.3 Phase 3: Validation & Sustainability (Months 17-24)", level=2)
    pdf.bold_bullet("Financial Statement Impact Assessment",
        "Quantified the cumulative effect of all revenue recognition corrections, including catch-up "
        "adjustments for gift card breakage, loyalty program reallocation, and returns reserve "
        "refinement. Worked with the client's legal counsel and SEC reporting team to determine "
        "appropriate disclosure treatment, concluding that a 'big bath' restatement was not required "
        "and the corrections could be recorded as a change in accounting estimate.")
    pdf.bold_bullet("Audit Support & Documentation",
        "Prepared comprehensive technical accounting memoranda supporting all significant judgments and "
        "estimates, facilitating a smooth year-end audit process. The client's external auditor (not "
        "Meridian, as we served in an advisory capacity) reported a 45% reduction in audit hours "
        "related to revenue recognition testing.")
    pdf.bold_bullet("Training & Change Management",
        "Delivered a structured training program covering 84 finance and accounting professionals across "
        "headquarters and field operations. Topics included ASC 606 principles, new system workflows, "
        "and ongoing monitoring procedures. Achieved a 92% post-training assessment pass rate.")
    pdf.bold_bullet("Ongoing Monitoring Dashboard",
        "Deployed a real-time monitoring dashboard tracking key revenue recognition metrics, including "
        "SSP allocation variances, loyalty breakage actuals versus estimates, gift card liability aging, "
        "and returns rates by channel. Configured automated alerts for deviations exceeding defined "
        "materiality thresholds.")

    # --- Team Composition (REWRITTEN with bio'd professionals) ---
    pdf.add_page()
    pdf.section_heading("5. Team Composition")
    pdf.body_text(
        "Meridian assembled a cross-functional team led by Robert Adeyemi, our Retail & Consumer Practice "
        "Lead, combining deep retail industry expertise with specialized technical accounting, tax, change "
        "management, and data analytics capabilities. The team was structured to address the engagement's "
        "dual focus on revenue recognition compliance and operational transformation."
    )
    pdf.add_table(
        ["Role", "Name", "Specialization", "Allocation"],
        [
            ["Lead Engagement Partner", "Robert Adeyemi, MBA", "Retail & Consumer", "35%"],
            ["Technical Accounting Partner", "Sarah Chen, CPA, CISA", "ASC 606 / Fin. Svcs.", "25%"],
            ["Sr. Manager - SALT Tax", "Sophia Vasquez, CPA, JD", "SALT / Multi-State", "50%"],
            ["Manager - Tax Provision", "Rachel Okonkwo, CPA, MST", "Tax Provision", "60%"],
            ["Sr. Manager - OCM", "Lauren Mitchell, SHRM-SCP", "Change Management", "80%"],
            ["Manager - Data/Analytics", "Raj Krishnamurthy", "Data Analytics / ML", "100%"],
            ["Staff - Data Analytics", "Aisha Patel", "Data Analytics", "100%"],
            ["Sr. Consultant - BA", "Olivia Brennan, CBAP", "BA / Testing", "90%"],
            ["Consultant - Data Eng.", "Jessica Huang", "Data Engineering", "85%"],
            ["Staff - PMO", "Derek Williams", "PMO Coordination", "100%"],
        ],
        col_widths=[45, 45, 48, 25],
    )
    pdf.body_text(
        "Total engagement hours over the 24-month period were approximately 42,000. The team included "
        "professionals from four Meridian offices (New York, Chicago, Atlanta, and Seattle) with "
        "regular on-site presence at the client's headquarters and primary distribution center."
    )

    pdf.section_heading("Team Qualifications", level=2)
    pdf.bullet("Robert Adeyemi brings MBA (Wharton) credentials and CSCP certification with deep consumer/retail expertise spanning omnichannel strategy, merchandising analytics, and supply chain optimization")
    pdf.bullet("Sarah Chen's 27 years of financial services experience and CISA credential provided essential technical accounting rigor for the ASC 606 revenue recognition redesign, including complex multi-element arrangements")
    pdf.bullet("Sophia Vasquez and Rachel Okonkwo provided complementary tax capabilities: Sophia's JD and SALT specialization addressed the 42-state nexus complexity, while Rachel automated the federal and state tax provision workflow")
    pdf.bullet("Lauren Mitchell's SHRM-SCP and Prosci certifications enabled an enterprise-grade change management program that achieved 92% training pass rates across 84 finance professionals")
    pdf.bullet("Raj Krishnamurthy's AWS ML and Databricks expertise powered the machine-learning returns prediction model and demand-sensing analytics for inventory optimization")
    pdf.bullet("Aisha Patel built the real-time monitoring dashboards and performed the 142-million-transaction revenue analysis that identified 47 distinct revenue archetypes")
    pdf.bullet("Olivia Brennan's CBAP credential supported rigorous requirements definition and UAT planning for the Oracle Cloud revenue recognition engine")

    # --- Outcomes ---
    pdf.add_page()
    pdf.section_heading("6. Quantifiable Outcomes")
    pdf.section_heading("6.1 Revenue Recognition Improvements", level=2)
    pdf.add_table(
        ["Metric", "Before", "After", "Improvement"],
        [
            ["Revenue Recognition Errors", "14 per quarter", "1 per quarter", "93% reduction"],
            ["Loyalty Breakage Accuracy", "+/- 35% variance", "+/- 6% variance", "83% improvement"],
            ["Gift Card Revenue Timing", "Escheatment only", "Proportional model", "ASC 606 compliant"],
            ["Returns Reserve Accuracy", "+/- 18%", "+/- 4%", "78% improvement"],
            ["Restatement Risk Items", "8 identified", "0 remaining", "100% resolved"],
        ],
        col_widths=[48, 42, 42, 40],
    )

    pdf.section_heading("6.2 Working Capital & Inventory", level=2)
    pdf.add_table(
        ["Metric", "Before", "After", "Improvement"],
        [
            ["Inventory Turns", "3.9x", "4.7x", "+0.8x improvement"],
            ["Markdown Rate (% of rev)", "34%", "29%", "-5 pct points"],
            ["Excess & Obsolete Reserve", "$87M", "$64M", "$23M reduction"],
            ["Working Capital Freed", "-", "$8.0M", "Net improvement"],
            ["Stockout Rate", "7.2%", "4.1%", "43% reduction"],
        ],
        col_widths=[48, 42, 42, 40],
    )

    pdf.section_heading("6.3 Operational Efficiency", level=2)
    pdf.add_table(
        ["Metric", "Before", "After", "Improvement"],
        [
            ["Monthly Close (days)", "12", "7", "42% reduction"],
            ["Manual Rev Rec Entries", "680 / month", "120 / month", "82% reduction"],
            ["Channel Attribution Time", "48 hrs", "Real-time", "Eliminated lag"],
            ["Audit Hours (Rev Rec)", "4,200 hrs", "2,310 hrs", "45% reduction"],
        ],
        col_widths=[48, 42, 42, 40],
    )

    pdf.section_heading("7. Client Testimonial")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6,
        '"Meridian didn\'t just fix our revenue recognition issues - they fundamentally transformed how '
        'we think about financial data across our omnichannel business. The combination of deep technical '
        'accounting knowledge and practical retail operating experience is something we hadn\'t found at '
        'other firms. The $8 million in working capital improvement exceeded our expectations and funded '
        'our next phase of digital investment."')
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, "- Chief Accounting Officer, [Client Name Redacted]")
    pdf.ln(8)

    pdf.section_heading("8. Lessons Learned")
    pdf.bold_bullet("Data Quality Is the Foundation",
        "Investing four months in transaction-level data analysis before proposing solutions ensured "
        "that our recommendations were grounded in empirical evidence rather than assumptions. The "
        "client's leadership team cited this data-driven approach as a key differentiator.")
    pdf.bold_bullet("System Migration Creates Opportunity",
        "Aligning revenue recognition redesign with the client's commerce platform migration allowed "
        "us to embed controls and automation into the new system from inception, rather than retrofitting.")
    pdf.bold_bullet("Cross-Functional Collaboration Is Essential",
        "Revenue recognition in retail touches merchandising, marketing, store operations, e-commerce, "
        "and finance. Our team's ability to engage stakeholders across all functions was critical to "
        "achieving buy-in and sustainable adoption.")

    path = os.path.join(OUTPUT_DIR, "case_study_retail.pdf")
    pdf.output(path)
    print(f"  Generated: {path}")


# =============================================================================
# 3. FINANCIAL SERVICES CASE STUDY (expanded with team table)
# =============================================================================

def generate_case_study_financial_services():
    pdf = MeridianPDF(
        "Case Study: Core Banking\nSystem Modernization",
        "Major Retail Banking Institution",
        client_confidential=True
    )
    pdf.cover_page(version="2.1", date="March 2026")

    pdf.add_page()
    pdf.section_heading("1. Engagement Overview")
    items = [
        ("Client:", "Top-10 US retail bank (name withheld per confidentiality agreement)"),
        ("Industry:", "Financial Services - Retail Banking"),
        ("Engagement Type:", "Technology Transformation - Core Banking Modernization"),
        ("Duration:", "18 months (January 2024 - June 2025)"),
        ("Team Size:", "85 professionals at peak staffing"),
        ("Total Fees:", "$24.8 million"),
        ("Lead Partner:", "Sarah Chen, CPA, CISA"),
        ("Meridian Offices:", "New York (lead), Chicago, Hyderabad (GDC)"),
    ]
    for label, val in items:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(40, 40, 40)
        w = pdf.get_string_width(label) + 4
        pdf.cell(w, 6, label)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, val)
        pdf.ln(1)

    pdf.ln(3)
    pdf.section_heading("2. Client Situation & Challenge")
    pdf.body_text(
        "The client, a top-10 US retail bank with $285 billion in assets and 22 million consumer accounts, "
        "faced an urgent imperative to modernize its core banking infrastructure. The bank's transaction "
        "processing backbone had operated on an IBM zSeries mainframe platform for over 30 years, running "
        "custom COBOL applications that had been progressively layered and patched over three decades. "
        "While the system remained functionally stable, it presented escalating strategic and operational risks:"
    )
    pdf.bold_bullet("Technology Obsolescence", "The mainframe workforce was aging rapidly, with 40% of core COBOL developers expected to retire within 5 years. Recruiting replacements was increasingly difficult and expensive, with annual contractor rates exceeding $280/hour for specialized mainframe skills.")
    pdf.bold_bullet("Regulatory Pressure", "The OCC had issued a Matter Requiring Attention (MRA) citing the bank's inability to produce real-time transaction data for regulatory reporting. The existing batch-processing architecture introduced 24-48 hour latency in critical reporting feeds.")
    pdf.bold_bullet("Customer Experience Gaps", "The bank's Net Promoter Score (NPS) had declined from 58 to 42 over three years, driven primarily by slow transaction processing, limited digital banking features, and an inability to offer real-time payments. Competitor banks with modern core systems were capturing market share in the 25-40 demographic.")
    pdf.bold_bullet("Cost Structure", "Annual mainframe operating costs exceeded $78 million, growing at 8-12% annually due to MIPS-based licensing models and specialized hardware maintenance. The bank estimated a 5-year total cost of ownership (TCO) of $450 million to maintain the status quo.")
    pdf.bold_bullet("Integration Constraints", "The monolithic mainframe architecture required custom point-to-point integrations for each new channel or partner, with average integration timelines of 6-9 months. This severely limited the bank's ability to partner with fintechs or launch new digital products.")

    # --- Expanded: Regulatory & Compliance Context ---
    pdf.add_page()
    pdf.section_heading("3. Regulatory & Compliance Context")
    pdf.body_text(
        "The engagement operated within a demanding regulatory environment that shaped every technical "
        "and architectural decision. The bank is supervised by the OCC, the Federal Reserve, and the FDIC, "
        "with additional oversight from the CFPB for consumer-facing products. Key regulatory considerations "
        "included:"
    )
    pdf.bold_bullet("OCC MRA Resolution",
        "The MRA required the bank to demonstrate real-time transaction reporting capability within 18 months. "
        "Failure to resolve the MRA could result in a formal enforcement action, potentially including "
        "a cease-and-desist order restricting new product launches. Meridian worked with the bank's "
        "regulatory affairs team to develop a remediation plan accepted by the OCC examination team "
        "within 60 days of engagement kickoff.")
    pdf.bold_bullet("BSA/AML Real-Time Monitoring",
        "The legacy batch architecture prevented the bank from implementing real-time transaction monitoring "
        "for Bank Secrecy Act (BSA) and Anti-Money Laundering (AML) compliance. The modernized platform "
        "needed to support real-time event-driven alerting, with transaction data flowing to the AML "
        "monitoring system within seconds rather than the existing 24-48 hour batch cycle.")
    pdf.bold_bullet("Data Residency and Privacy",
        "The bank operates in all 50 states plus international correspondent banking relationships, "
        "requiring compliance with state-specific data privacy laws, including the California Consumer "
        "Privacy Act (CCPA) and the New York SHIELD Act. The cloud architecture design incorporated "
        "data residency controls ensuring all customer PII remained within US-based AWS regions.")
    pdf.bold_bullet("Third-Party Risk Management",
        "The adoption of Thought Machine Vault as a third-party core banking platform triggered OCC "
        "guidance on third-party risk management (OCC 2023-17). Meridian conducted a comprehensive "
        "vendor due diligence assessment covering technology resilience, financial viability, information "
        "security controls, and business continuity capabilities.")

    pdf.section_heading("4. Meridian's Solution", level=1)
    pdf.body_text(
        "Meridian designed and executed a phased migration strategy to replace the legacy mainframe core "
        "with a cloud-native core banking platform while maintaining uninterrupted service to 22 million "
        "accounts. The solution architecture comprised four integrated workstreams:"
    )
    pdf.section_heading("4.1 Core Banking Platform Selection & Implementation", level=2)
    pdf.body_text(
        "After a rigorous 12-week evaluation of Temenos Transact, Thought Machine Vault, and Finacle, "
        "the team selected Thought Machine Vault as the target core banking platform. Key selection "
        "criteria included cloud-native architecture (Kubernetes-based), smart contract-driven product "
        "configuration, and real-time event-driven processing. Meridian led the platform implementation "
        "using an agile delivery methodology with 2-week sprints, deploying the platform on AWS EKS "
        "across three availability zones."
    )
    pdf.section_heading("4.2 API Layer & Integration Architecture", level=2)
    pdf.body_text(
        "Meridian designed and implemented a comprehensive API gateway layer using Kong Enterprise, "
        "exposing 450+ RESTful APIs for internal and external consumption. The API layer served as the "
        "integration backbone, decoupling the core banking platform from downstream channels (mobile, "
        "web, branch, ATM) and enabling fintech partner integration. An event-driven architecture "
        "using Apache Kafka processed over 2.8 million events per hour at peak, providing real-time "
        "data feeds for regulatory reporting, fraud detection, and customer analytics."
    )

    pdf.add_page()
    pdf.section_heading("4.3 Data Migration & Parallel Run", level=2)
    pdf.body_text(
        "The data migration workstream addressed 22 million customer accounts, 380 million historical "
        "transactions (7 years), and 14 product configurations. Meridian developed a custom migration "
        "framework using AWS DMS and custom Python ETL pipelines, executing three mock migrations before "
        "the production cutover. A 90-day parallel run period validated data integrity with 99.9997% "
        "accuracy before the legacy system was decommissioned."
    )
    pdf.body_text(
        "The migration framework incorporated comprehensive data validation at every stage. Automated "
        "reconciliation scripts compared account balances, transaction histories, and product attributes "
        "between source and target systems, with any discrepancy flagged for manual review. The team "
        "processed over 2.4 billion individual data points during the three mock migrations, achieving "
        "progressively higher accuracy rates (99.992%, 99.998%, and 99.9997%) as data quality issues "
        "were identified and remediated."
    )
    pdf.section_heading("4.4 Real-Time Payments Enablement", level=2)
    pdf.body_text(
        "As part of the modernization, Meridian enabled the bank's connection to the FedNow instant "
        "payments network and upgraded the bank's RTP (Real-Time Payments) connectivity. The new "
        "architecture supported sub-second payment processing compared to the previous 2-4 hour batch "
        "cycle, positioning the bank as a leader in instant payments among top-10 US retail banks."
    )
    pdf.body_text(
        "The payments integration required careful coordination with The Clearing House (TCH) for RTP "
        "and the Federal Reserve for FedNow, including certification testing, message format validation "
        "(ISO 20022), and fraud control configuration. The team implemented velocity limits, device "
        "binding, and behavioral analytics to mitigate fraud risk in the real-time payments channel, "
        "achieving a fraud rate of 0.003% in the first six months of production operation."
    )

    # --- Expanded: Security Architecture ---
    pdf.section_heading("4.5 Security Architecture & Zero-Trust Design", level=2)
    pdf.body_text(
        "Given the sensitivity of core banking operations, Meridian implemented a comprehensive security "
        "architecture aligned with zero-trust principles. Alex Petrov, Senior Manager for Cybersecurity, "
        "led the security design and implementation:"
    )
    pdf.bullet("Zero-trust network segmentation using AWS VPC service endpoints and PrivateLink, eliminating public internet exposure for all core banking APIs")
    pdf.bullet("mTLS (mutual TLS) authentication between all microservices, with certificate rotation automated via HashiCorp Vault")
    pdf.bullet("Runtime application self-protection (RASP) integrated into the Kubernetes pod security context")
    pdf.bullet("Comprehensive audit logging with tamper-evident storage in AWS CloudTrail and S3 Object Lock, meeting OCC examination requirements")
    pdf.bullet("Penetration testing conducted by Meridian's red team across three engagement phases, with all critical findings remediated within SLA")

    # --- Team Composition (NEW section with named team members) ---
    pdf.add_page()
    pdf.section_heading("5. Team Composition")
    pdf.body_text(
        "The engagement was led by Sarah Chen, Meridian's Financial Services Practice Lead, with a "
        "senior team drawing on deep expertise in cybersecurity, IT audit, cloud infrastructure, and "
        "data analytics. The team combined industry-specific banking knowledge with technical depth "
        "across the modernization workstreams."
    )
    pdf.add_table(
        ["Role", "Name", "Specialization", "Allocation"],
        [
            ["Lead Partner", "Sarah Chen, CPA, CISA", "Financial Services", "40%"],
            ["Sr. Mgr - Cybersecurity", "Alex Petrov, CISSP, CISM", "Security Architecture", "80%"],
            ["Mgr - IT Audit / GRC", "Thomas Chen, CISA, CISSP", "IT Audit & Controls", "70%"],
            ["Sr. Mgr - Technology", "David Kim, PMP, SAP", "ERP / Platform Integ.", "60%"],
            ["Sr. Consultant - Cloud", "Jordan Lee", "Cloud Infrastructure", "100%"],
            ["Staff - Data Analytics", "Aisha Patel", "Data Analytics", "100%"],
            ["Staff - Risk Advisory", "Emily Nakamura", "Risk Advisory", "90%"],
        ],
        col_widths=[45, 45, 48, 25],
    )
    pdf.body_text(
        "Beyond the senior team, the engagement was supported by 4 additional Senior Managers, "
        "8 Managers, 22 Senior Consultants, 28 Consultants, and 21 Analysts, with 35 onshore and "
        "50 offshore (Hyderabad GDC) at peak staffing."
    )
    pdf.section_heading("Key Team Contributions", level=2)
    pdf.bullet("Alex Petrov designed the zero-trust security architecture and led three rounds of penetration testing, ensuring the platform met OCC and FFIEC cybersecurity examination standards")
    pdf.bullet("Thomas Chen conducted the IT general controls assessment and SOX 404 impact analysis for the core banking migration, identifying 28 control changes requiring remediation before go-live")
    pdf.bullet("David Kim managed the integration architecture between the new Thought Machine Vault core and the bank's existing SAP ERP for general ledger, subledger, and regulatory reporting feeds")
    pdf.bullet("Jordan Lee led the AWS EKS infrastructure build-out across three availability zones, implementing infrastructure-as-code using Terraform and GitOps deployment via ArgoCD")
    pdf.bullet("Aisha Patel built the data migration validation framework, performing automated reconciliation across 2.4 billion data points during mock migrations")
    pdf.bullet("Emily Nakamura supported the vendor risk assessment of Thought Machine per OCC 2023-17 guidance and developed the ongoing third-party monitoring framework")

    pdf.ln(2)
    pdf.body_text("Delivery governance included:")
    pdf.bullet("Agile delivery with 2-week sprints, PI planning every 10 weeks (SAFe-aligned)")
    pdf.bullet("Weekly steering committee with C-suite sponsors (CTO, CIO, CFO)")
    pdf.bullet("Bi-weekly regulatory updates to OCC relationship management team")
    pdf.bullet("Independent quality assurance reviews at each phase gate")

    # --- Technology Stack ---
    pdf.add_page()
    pdf.section_heading("6. Technology Stack")
    pdf.body_text("The following technologies were deployed as part of the solution:")
    pdf.bold_bullet("Core Banking", "Thought Machine Vault (cloud-native, smart contract-based)")
    pdf.bold_bullet("Cloud Infrastructure", "AWS (EKS, RDS Aurora, S3, CloudFront, Route 53)")
    pdf.bold_bullet("Containerization", "Docker, Kubernetes (EKS), Helm, ArgoCD")
    pdf.bold_bullet("Event Streaming", "Apache Kafka (MSK), Schema Registry, Kafka Connect")
    pdf.bold_bullet("API Management", "Kong Enterprise Gateway, OpenAPI 3.0 specifications")
    pdf.bold_bullet("Data Migration", "AWS DMS, Custom Python ETL, Apache Spark")
    pdf.bold_bullet("Monitoring", "Datadog (APM, infrastructure, logs), PagerDuty")
    pdf.bold_bullet("Security", "HashiCorp Vault (secrets), AWS KMS, WAF, GuardDuty")
    pdf.bold_bullet("CI/CD", "GitHub Enterprise, GitHub Actions, SonarQube, Artifactory")

    # --- Expanded: Delivery Phases ---
    pdf.section_heading("7. Delivery Phases")
    pdf.section_heading("7.1 Phase 1: Discovery & Architecture (Months 1-3)", level=2)
    pdf.body_text(
        "The initial phase encompassed application portfolio analysis, target architecture design, "
        "vendor selection, and migration planning. Key activities included stakeholder interviews with "
        "120+ business and technology leaders, current-state architecture documentation, TCO modeling "
        "for three platform alternatives, and development of the phased migration roadmap. The phase "
        "concluded with Architecture Review Board approval and OCC remediation plan acceptance."
    )
    pdf.section_heading("7.2 Phase 2: Platform Build & Mock Migration (Months 4-9)", level=2)
    pdf.body_text(
        "This phase focused on core platform deployment, API layer construction, security architecture "
        "implementation, and three iterative mock migrations. The team configured 14 product templates "
        "in Thought Machine Vault's smart contract framework, built and tested 450+ APIs, and executed "
        "mock migrations with progressively larger datasets. The phase also included comprehensive "
        "performance testing simulating 5x peak transaction volumes to validate system scalability."
    )
    pdf.section_heading("7.3 Phase 3: Parallel Run & Cutover (Months 10-15)", level=2)
    pdf.body_text(
        "The 90-day parallel run period operated both legacy and modern systems simultaneously, with "
        "real-time transaction comparison validating functional equivalence. The team monitored "
        "approximately 8.5 million daily transactions across both systems, with automated alerting "
        "for any discrepancy exceeding $0.01. The production cutover was executed over a holiday weekend "
        "with a 72-hour change freeze, completing the migration with zero customer-visible impact."
    )
    pdf.section_heading("7.4 Phase 4: Stabilization & Optimization (Months 16-18)", level=2)
    pdf.body_text(
        "The final phase focused on production stabilization, performance optimization, FedNow "
        "certification, legacy system decommissioning, and knowledge transfer to the bank's internal "
        "technology teams. The team conducted 48 hours of structured training sessions and delivered "
        "comprehensive runbooks for all operational procedures."
    )

    # --- Results ---
    pdf.add_page()
    pdf.section_heading("8. Results & Impact")
    pdf.body_text(
        "The core banking modernization program delivered transformative results across all key "
        "performance dimensions, exceeding original business case projections in several areas:"
    )
    pdf.ln(2)
    pdf.results_table(
        ["Metric", "Baseline (Pre)", "Result (Post)", "Improvement"],
        [
            ["Transaction Processing Time", "4.2 seconds avg", "2.5 seconds avg", "40% reduction"],
            ["Annual Infrastructure Cost", "$78M", "$46M", "$32M savings"],
            ["System Uptime", "99.92%", "99.99%", "Near-zero downtime"],
            ["Customer NPS", "42", "67", "+25 points"],
            ["Regulatory Reporting Latency", "24-48 hours", "Real-time", "Eliminated batch lag"],
            ["API Integration Time", "6-9 months", "2-4 weeks", "90% faster"],
            ["Time to Market (new products)", "9-12 months", "4-6 weeks", "85% faster"],
        ],
        col_widths=[65, 45, 45, 35],
    )

    pdf.section_heading("9. Client Testimonial")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6,
        '"Meridian\'s team brought an exceptional combination of deep banking domain expertise and '
        'cutting-edge technology skills. They didn\'t just migrate our core -- they fundamentally '
        'reimagined our technology architecture. The results speak for themselves: our operating costs '
        'are down, our customers are happier, and we\'re now launching new products in weeks instead '
        'of months. I would not hesitate to engage Meridian again for our next strategic initiative."')
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, "-- Chief Technology Officer, Client Institution")

    pdf.output(os.path.join(OUTPUT_DIR, "case_study_financial_services.pdf"))
    print("  Generated: case_study_financial_services.pdf")


# =============================================================================
# 4. HEALTHCARE CASE STUDY (expanded with team table)
# =============================================================================

def generate_case_study_healthcare():
    pdf = MeridianPDF(
        "Case Study: Post-Merger\nIntegration",
        "Regional Hospital System",
        client_confidential=True
    )
    pdf.cover_page(version="1.4", date="March 2026")

    pdf.add_page()
    pdf.section_heading("1. Engagement Overview")
    items = [
        ("Client:", "12-hospital regional system formed from merger of two health networks (name withheld)"),
        ("Industry:", "Healthcare - Hospital Systems"),
        ("Engagement Type:", "Post-Merger Integration - Clinical & Operational"),
        ("Duration:", "24 months (July 2023 - June 2025)"),
        ("Team Size:", "120+ professionals at peak staffing"),
        ("Total Fees:", "$38.4 million"),
        ("Lead Partner:", "Michael Torres, CPA, PMP, FACHE"),
        ("Meridian Offices:", "Chicago (lead), New York, Atlanta, Hyderabad (GDC)"),
    ]
    for label, val in items:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(40, 40, 40)
        w = pdf.get_string_width(label) + 4
        pdf.cell(w, 6, label)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, val)
        pdf.ln(1)

    pdf.ln(3)
    pdf.section_heading("2. Client Situation & Challenge")
    pdf.body_text(
        "The client was formed through the merger of two established regional health networks, creating "
        "a combined system of 12 hospitals, 185 ambulatory care sites, 4,200 physicians, and 38,000 "
        "employees serving a metropolitan area of 3.2 million residents. The merger, valued at $4.8 billion, "
        "was driven by the need to achieve scale, improve clinical outcomes, and realize significant "
        "cost synergies in an increasingly competitive and value-based healthcare market."
    )
    pdf.body_text("The newly formed system faced several critical integration challenges:")
    pdf.bold_bullet("Duplicate EHR Systems", "Network A operated on Epic (since 2016, fully integrated across 7 hospitals) while Network B used Cerner Millennium (deployed in 2014 across 5 hospitals). Maintaining two EHR platforms was projected to cost $28M annually in redundant licensing, support, and interface maintenance, and created patient safety risks at cross-network referral points where records were not accessible.")
    pdf.bold_bullet("Clinical Workflow Variation", "The two networks had independently developed clinical protocols, order sets, formularies, and documentation standards over decades. Initial assessment identified 2,400+ clinical workflow variations across 180 clinical departments, with 340 classified as high-priority due to patient safety implications.")
    pdf.bold_bullet("Synergy Target Pressure", "The merger business case committed to $45M in annual run-rate synergies within 30 months, including $18M from IT consolidation, $15M from supply chain standardization, and $12M from revenue cycle optimization. The Board and investor community were closely monitoring progress against these targets.")
    pdf.bold_bullet("Workforce Integration", "Cultural differences between the two networks were significant. Network A was an academic-affiliated system with a research-oriented culture, while Network B was a community-based system focused on operational efficiency. Physician alignment and retention were critical risks, particularly among high-revenue surgical specialties.")
    pdf.bold_bullet("Regulatory Requirements", "The merged entity needed to file updated Medicare and Medicaid provider enrollment, consolidate compliance programs, and ensure HIPAA-compliant data sharing across the newly unified system, all while maintaining CMS Conditions of Participation at every facility.")

    # --- Expanded: Clinical Quality & Patient Safety ---
    pdf.add_page()
    pdf.section_heading("3. Clinical Quality & Patient Safety Considerations")
    pdf.body_text(
        "Beyond the operational and financial aspects of the merger, maintaining and improving clinical "
        "quality during the integration was a paramount concern. The two networks entered the merger with "
        "different quality profiles and measurement frameworks:"
    )
    pdf.bold_bullet("Quality Metric Harmonization",
        "Network A tracked 142 clinical quality metrics aligned with the National Quality Forum (NQF) "
        "measure set, while Network B used a proprietary set of 89 metrics with only 54% overlap. "
        "Meridian's team worked with clinical leadership to develop a unified quality dashboard of 168 "
        "metrics covering CMS Hospital Compare measures, Leapfrog Safety Grades, and system-specific "
        "indicators. The dashboard provided real-time visibility into quality performance across all "
        "12 facilities from Day 1 of clinical integration.")
    pdf.bold_bullet("Medication Safety During Formulary Consolidation",
        "The consolidation of two independent formularies into a single system-wide formulary required "
        "careful management of 3,400 medication entries. Meridian embedded two pharmacist consultants in "
        "the integration team to conduct medication equivalency mapping, identify therapeutic substitution "
        "opportunities, and design clinical decision support alerts for high-risk medications during the "
        "transition period. The team processed 847 formulary change orders with zero medication safety "
        "events directly attributable to the consolidation.")
    pdf.bold_bullet("Credentialing & Privileging",
        "The merger required re-credentialing and re-privileging 4,200 physicians and advanced practice "
        "providers across the unified medical staff structure. Meridian implemented a centralized "
        "credentialing verification organization (CVO) using MD-Staff, reducing the average credentialing "
        "cycle from 120 days to 45 days and ensuring continuous compliance with Joint Commission standards.")

    pdf.section_heading("4. Meridian's Solution")
    pdf.body_text(
        "Meridian designed and executed a comprehensive post-merger integration program organized into "
        "four interconnected workstreams, each with dedicated leadership and measurable milestones:"
    )
    pdf.section_heading("4.1 Unified Epic Implementation", level=2)
    pdf.body_text(
        "After a thorough evaluation, the steering committee selected Epic as the unified EHR platform, "
        "leveraging Network A's mature Epic environment as the foundation. Meridian led the extension of "
        "Epic to Network B's 5 hospitals and 85 ambulatory sites through a phased rollout: three community "
        "hospitals in Wave 1, followed by two specialty hospitals in Wave 2. The implementation included "
        "Epic Beaker (laboratory), Radiant (imaging), Willow (pharmacy), and Cadence (scheduling), "
        "achieving a single patient record across all 12 facilities."
    )
    pdf.body_text(
        "A dedicated data migration team converted 4.2 million patient records and 12 years of clinical "
        "history from Cerner to Epic, using a custom migration toolkit developed by Meridian's GDC team. "
        "The migration achieved 99.98% data integrity as validated by an independent clinical data audit."
    )

    pdf.add_page()
    pdf.section_heading("4.2 Clinical Workflow Harmonization", level=2)
    pdf.body_text(
        "Meridian deployed a clinical integration team of 35 professionals (including 8 clinicians with "
        "direct patient care experience) to harmonize clinical workflows across the merged system. The team "
        "facilitated 220 clinical governance sessions involving 600+ physicians and clinical leaders to "
        "develop unified order sets (reduced from 4,800 to 1,200), a single formulary (consolidated from "
        "two formularies with 62% overlap), and standardized clinical documentation templates for all "
        "major service lines."
    )

    pdf.section_heading("4.3 Shared Services Center for Revenue Cycle", level=2)
    pdf.body_text(
        "Meridian designed and stood up a centralized Revenue Cycle Management (RCM) shared services "
        "center serving all 12 hospitals. The center consolidated previously distributed functions including "
        "patient access/registration, coding, billing, claims submission, denial management, and collections. "
        "Key improvements included:"
    )
    pdf.bullet("Centralized coding pool with CAC (Computer-Assisted Coding) technology, improving coding accuracy from 88% to 96%")
    pdf.bullet("Automated claims scrubbing engine reducing clean claims rejection rate from 18% to 4%")
    pdf.bullet("Dedicated denial management unit with root cause analytics, reducing denial rate from 12.4% to 9.7%")
    pdf.bullet("Single patient financial services model with unified pricing transparency and financial counseling")
    pdf.bullet("Standardized charge capture process reducing revenue leakage by an estimated $8.2M annually")

    pdf.section_heading("4.4 IT Infrastructure Consolidation", level=2)
    pdf.body_text(
        "The IT consolidation workstream addressed the merger of two independent data centers, network "
        "infrastructure, and end-user computing environments. Key activities included data center "
        "consolidation from 4 facilities to 2 (primary + disaster recovery), network interconnection "
        "via dedicated MPLS circuits, Active Directory forest merge, and unified endpoint management "
        "for 28,000 devices. The team also consolidated 14 redundant clinical applications, reducing "
        "annual application licensing costs by $6.8M."
    )

    # --- Expanded: Change Management Deep Dive ---
    pdf.add_page()
    pdf.section_heading("5. Organizational Change Management")
    pdf.body_text(
        "The scale of organizational change in a health system merger of this magnitude required a "
        "dedicated and sophisticated change management program. Lauren Mitchell, Meridian's Senior "
        "Manager for Organizational Change Management, led a team of 15 change management professionals "
        "embedded across all four workstreams."
    )
    pdf.section_heading("5.1 Physician Engagement Strategy", level=2)
    pdf.body_text(
        "Physician alignment was identified early as the highest-risk element of the integration. The "
        "team implemented a multi-layered engagement approach: (1) a Physician Integration Advisory Council "
        "of 24 physician leaders meeting biweekly, (2) specialty-specific working groups for the 12 "
        "highest-revenue service lines, (3) one-on-one engagement sessions with 180 department chairs "
        "and division chiefs, and (4) monthly town halls with the CMO and integration leadership. "
        "This approach maintained physician satisfaction above 80% throughout the integration, a metric "
        "that comparable mergers typically see decline by 15-20 points."
    )
    pdf.section_heading("5.2 End-User Training Program", level=2)
    pdf.body_text(
        "The EHR migration required training 35,000 end users across diverse roles and skill levels. "
        "The training program used a blended model combining self-paced e-learning modules (average "
        "4 hours per role), instructor-led classroom sessions (8-16 hours depending on role complexity), "
        "and at-the-elbow support during go-live weeks. Meridian deployed 120 super-users and 45 floor "
        "support specialists during Wave 1, scaling to 85 super-users for Wave 2 as the organization "
        "built internal capability. Post-training competency assessments showed 94% of users met or "
        "exceeded proficiency targets within 30 days of go-live."
    )
    pdf.section_heading("5.3 Communication Framework", level=2)
    pdf.body_text(
        "The OCM team implemented a structured communication cadence: weekly integration newsletters "
        "to all 38,000 employees, biweekly leadership briefings for 450 director-level leaders, monthly "
        "patient advisory council updates, and real-time status dashboards accessible via the intranet. "
        "Sentiment surveys conducted quarterly showed stakeholder confidence in the integration increasing "
        "from 42% (Month 1) to 78% (Month 24)."
    )

    # --- Team Composition (NEW section with named team members) ---
    pdf.add_page()
    pdf.section_heading("6. Team Composition")
    pdf.body_text(
        "The engagement was led by Michael Torres, Meridian's Healthcare & Life Sciences Practice Lead, "
        "with a senior team combining healthcare operations expertise, change management capabilities, "
        "risk advisory, tax, and quality assurance specializations."
    )
    pdf.add_table(
        ["Role", "Name", "Specialization", "Allocation"],
        [
            ["Lead Partner", "Michael Torres, CPA, PMP", "Healthcare / PMI", "50%"],
            ["Sr. Mgr - OCM", "Lauren Mitchell, SHRM-SCP", "Change Management", "100%"],
            ["Mgr - Risk Advisory", "Maria Santos, CPA, CIA", "Risk & Compliance", "80%"],
            ["Mgr - Tax Provision", "Rachel Okonkwo, CPA, MST", "Healthcare Tax", "60%"],
            ["Sr. Consultant - BA", "Olivia Brennan, CBAP", "BA / Testing", "100%"],
            ["Staff - PMO", "Derek Williams", "PMO Coordination", "100%"],
            ["Staff - Data Analytics", "Aisha Patel", "Data Analytics", "90%"],
        ],
        col_widths=[45, 45, 48, 25],
    )
    pdf.body_text(
        "Beyond the senior team, the program included 4 additional Senior Managers, 12 Managers, "
        "32 Senior Consultants, 40 Consultants, and 28 Analysts. The team also included 8 embedded "
        "clinicians (3 physicians, 3 RNs, 2 pharmacists) for clinical workflow design."
    )
    pdf.section_heading("Key Team Contributions", level=2)
    pdf.bullet("Lauren Mitchell led the 15-person OCM team, designing the physician engagement strategy that maintained satisfaction above 80% and the blended training program for 35,000 end users")
    pdf.bullet("Maria Santos conducted the enterprise risk assessment for the merged entity, identifying 42 integration-specific risks and designing mitigation controls for each, with particular focus on HIPAA compliance during data migration")
    pdf.bullet("Rachel Okonkwo managed the tax implications of the merger, including provider enrollment consolidation, tax-exempt status re-certification across 14 entities, and the tax provision for the combined system's first unified fiscal year")
    pdf.bullet("Olivia Brennan led requirements definition and user acceptance testing for the Epic extension to Network B, managing 2,400 test cases across clinical and revenue cycle workflows with a 98.7% first-pass rate")
    pdf.bullet("Derek Williams coordinated the integrated PMO, managing 1,200+ project tasks across four workstreams with weekly status reporting to the Board Integration Committee")
    pdf.bullet("Aisha Patel built the unified quality dashboard consolidating metrics from both networks and developed the analytics models for denial management root cause analysis")

    pdf.ln(2)
    pdf.body_text("The 24-month program was structured into three phases:")
    pdf.bold_bullet("Phase 1 - Foundation (Months 1-6)", "Integration planning, governance structure, EHR platform decision, clinical workflow assessment, Day 1 readiness activities")
    pdf.bold_bullet("Phase 2 - Execution (Months 7-18)", "Epic Wave 1 and Wave 2 deployments, shared services center buildout, IT infrastructure consolidation, clinical workflow harmonization")
    pdf.bold_bullet("Phase 3 - Optimization (Months 19-24)", "Performance optimization, benefits realization tracking, knowledge transfer, transition to steady-state operations")

    # --- Results ---
    pdf.add_page()
    pdf.section_heading("7. Results & Impact")
    pdf.ln(2)
    pdf.results_table(
        ["Metric", "Baseline", "Result", "Improvement"],
        [
            ["Synergies Realized (annual)", "$0 (pre-merger)", "$52M", "116% of $45M target"],
            ["Claims Denial Rate", "12.4%", "9.7%", "22% reduction"],
            ["Patient Record Unification", "Dual systems", "Single EHR", "100% unified"],
            ["Physician Satisfaction", "76%", "82%", "Maintained >80%"],
            ["Days in A/R", "48.2 days", "38.6 days", "20% reduction"],
            ["IT Application Portfolio", "280 applications", "196 applications", "30% consolidation"],
            ["Annual IT Operating Cost", "$62M combined", "$44M unified", "$18M savings"],
        ],
        col_widths=[65, 40, 40, 45],
    )

    # --- Expanded: Additional Outcomes ---
    pdf.section_heading("7.1 Clinical Quality Outcomes", level=2)
    pdf.body_text(
        "Importantly, the integration achieved its operational targets without compromising clinical quality. "
        "Key quality outcomes during and after the integration included:"
    )
    pdf.bullet("Hospital-acquired infection rates remained stable or improved across all 12 facilities, with CLABSI rates declining 12% system-wide")
    pdf.bullet("30-day readmission rates decreased from 14.8% (blended pre-merger) to 13.2% post-integration, attributed to improved care coordination via the unified EHR")
    pdf.bullet("Patient experience scores (HCAHPS) improved from the 62nd percentile to the 71st percentile nationally, driven by reduced wait times from streamlined scheduling")
    pdf.bullet("Zero sentinel events attributed to the integration, validating the team's patient-safety-first approach to clinical workflow harmonization")

    # --- Expanded: Synergy Realization Detail ---
    pdf.add_page()
    pdf.section_heading("7.2 Synergy Realization Breakdown", level=2)
    pdf.body_text(
        "The $52M in realized annual synergies exceeded the Board's $45M target by 16%. The following "
        "table provides a detailed breakdown by category:"
    )
    pdf.add_table(
        ["Synergy Category", "Target", "Realized", "Variance"],
        [
            ["IT Consolidation", "$18M", "$21.2M", "+$3.2M (18%)"],
            ["Supply Chain Standardization", "$15M", "$16.8M", "+$1.8M (12%)"],
            ["Revenue Cycle Optimization", "$12M", "$14.0M", "+$2.0M (17%)"],
        ],
        col_widths=[55, 40, 40, 50],
    )
    pdf.body_text(
        "IT consolidation synergies exceeded target primarily through aggressive application retirement "
        "(280 to 196 applications) and favorable renegotiation of enterprise license agreements under "
        "the combined system's increased purchasing leverage. Supply chain savings were driven by GPO "
        "contract consolidation across medical/surgical supplies, pharmaceuticals, and capital equipment. "
        "Revenue cycle improvements reflected the impact of centralized coding, automated claims scrubbing, "
        "and the denial management unit."
    )

    pdf.section_heading("8. Lessons Learned & Transferable Insights")
    pdf.bold_bullet("Clinical Quality Must Be Non-Negotiable",
        "Establishing a unified quality dashboard on Day 1, before any operational changes, created "
        "an objective baseline and accountability framework that prevented quality degradation during "
        "the integration. This approach is now a standard element of Meridian's PMI methodology.")
    pdf.bold_bullet("Physician Engagement Requires Investment",
        "The multi-layered physician engagement strategy consumed approximately 15% of the total "
        "program budget but was essential to maintaining satisfaction and preventing attrition of "
        "high-revenue specialists. Programs that underinvest in physician alignment typically experience "
        "18-24 months of productivity decline post-merger.")
    pdf.bold_bullet("EHR Migration Is a Clinical Event, Not Just IT",
        "Treating the Cerner-to-Epic migration as a clinical transformation rather than a technology "
        "project ensured that patient safety considerations drove every design and deployment decision. "
        "The embedded clinician model (8 clinicians on the integration team) was critical to achieving "
        "this mindset.")
    pdf.bold_bullet("Change Management Cannot Be an Afterthought",
        "The dedicated 15-person OCM team, led by Lauren Mitchell, was embedded from Day 1 rather than "
        "added mid-stream. Organizations that treat change management as an add-on to PMI programs "
        "consistently underperform on synergy realization and workforce retention metrics.")

    pdf.section_heading("9. Client Testimonial")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6,
        '"The Meridian team understood from day one that this was not just a technology project -- it was '
        'a clinical transformation. Their ability to engage our physicians and nursing staff in the design '
        'process, combined with their operational rigor in managing a program of this complexity, was '
        'exceptional. We exceeded our synergy targets while maintaining clinical quality and physician '
        'satisfaction, which is the true measure of a successful integration."')
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, "-- Chief Executive Officer, Client Health System")

    pdf.output(os.path.join(OUTPUT_DIR, "case_study_healthcare.pdf"))
    print("  Generated: case_study_healthcare.pdf")


# =============================================================================
# 5. MANUFACTURING CASE STUDY (expanded with team table)
# =============================================================================

def generate_case_study_manufacturing():
    pdf = MeridianPDF(
        "Case Study: Supply Chain\nTransformation",
        "Global Industrial Manufacturer",
        client_confidential=True
    )
    pdf.cover_page(version="1.2", date="March 2026")

    pdf.add_page()
    pdf.section_heading("1. Engagement Overview")
    items = [
        ("Client:", "Fortune 200 diversified industrial manufacturer (name withheld)"),
        ("Industry:", "Manufacturing - Diversified Industrials"),
        ("Engagement Type:", "Supply Chain Transformation"),
        ("Duration:", "16 months (March 2024 - June 2025)"),
        ("Team Size:", "65 professionals at peak staffing"),
        ("Total Fees:", "$18.2 million"),
        ("Lead Partner:", "James O'Sullivan, CPA, Six Sigma Black Belt"),
        ("Meridian Offices:", "Chicago (lead), San Francisco, Hyderabad (GDC)"),
    ]
    for label, val in items:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(40, 40, 40)
        w = pdf.get_string_width(label) + 4
        pdf.cell(w, 6, label)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, val)
        pdf.ln(1)

    pdf.ln(3)
    pdf.section_heading("2. Client Situation & Challenge")
    pdf.body_text(
        "The client, a Fortune 200 diversified industrial manufacturer with $18.6 billion in annual "
        "revenue, operated a global supply chain spanning 14 countries, 22 manufacturing plants, 8 "
        "distribution centers, and a network of 3,400 direct material suppliers. Despite significant "
        "investments in manufacturing technology and capacity, the company's supply chain performance "
        "had deteriorated significantly over the preceding three years, driven by:"
    )
    pdf.bold_bullet("Excess Inventory", "Finished goods and work-in-progress inventory had ballooned to $380M, representing 74 days of supply versus an industry benchmark of 45-50 days. Carrying costs alone exceeded $45M annually. The excess was concentrated in slow-moving SKUs and safety stock buffers inflated during the COVID-era supply disruptions but never rationalized.")
    pdf.bold_bullet("Poor Demand Visibility", "The company used a fragmented collection of spreadsheet-based forecasting processes across its 5 business units, with no integrated demand planning platform. Forecast accuracy at the SKU-location level averaged 52%, well below the 70-75% industry benchmark, resulting in simultaneous overstock and stockout conditions across the distribution network.")
    pdf.bold_bullet("Delivery Performance Deterioration", "On-Time-In-Full (OTIF) delivery had declined from 91% to 82% over three years, directly impacting customer satisfaction and contributing to $28M in customer penalties and lost contract renewals.")
    pdf.bold_bullet("Logistics Cost Escalation", "Total logistics costs (transportation, warehousing, and distribution) had increased by 34% over three years to $412M annually, driven by expedited shipping to compensate for poor planning, suboptimal carrier utilization, and a distribution network that had not been redesigned since 2015.")
    pdf.bold_bullet("Supply Chain Sustainability Gap", "The company had committed to Science Based Targets (SBTi) for Scope 3 emissions reduction but lacked visibility into supplier emissions data. Only 12 of their top 200 suppliers had provided emissions data, creating a significant ESG reporting and compliance risk.")

    # --- Expanded: Root Cause Analysis ---
    pdf.add_page()
    pdf.section_heading("3. Root Cause Analysis")
    pdf.body_text(
        "Before designing the transformation program, Meridian conducted a 6-week diagnostic to identify "
        "the structural root causes behind the client's supply chain deterioration. The analysis revealed "
        "interconnected systemic issues rather than isolated functional failures:"
    )
    pdf.section_heading("3.1 Organizational Fragmentation", level=2)
    pdf.body_text(
        "The company's five business units operated with high autonomy, each maintaining independent "
        "demand planning processes, supplier relationships, and logistics arrangements. This siloed "
        "structure prevented cross-BU demand aggregation, eliminated opportunities for consolidated "
        "purchasing leverage, and created competing priorities for shared manufacturing capacity. "
        "There was no enterprise-level S&OP process to balance demand, supply, and financial targets "
        "across the portfolio."
    )
    pdf.section_heading("3.2 Technology Fragmentation", level=2)
    pdf.body_text(
        "The supply chain technology landscape consisted of 23 discrete systems across planning, "
        "execution, and analytics functions, with limited integration. The core ERP (SAP ECC 6.0) "
        "had not been upgraded to S/4HANA, and the planning stack relied on a mix of SAP APO "
        "(partially decommissioned), Kinaxis RapidResponse (used by 2 BUs), and Excel-based models. "
        "Data latency between systems averaged 24-48 hours, making real-time decision-making impossible."
    )
    pdf.section_heading("3.3 Post-Pandemic Overcorrection", level=2)
    pdf.body_text(
        "During the 2020-2022 supply chain crisis, the company had aggressively built safety stock "
        "buffers and dual-sourced critical components to mitigate shortage risk. While appropriate "
        "during the crisis, these measures were never unwound as conditions normalized. Safety stock "
        "parameters remained at crisis-level settings, dual-sourcing arrangements continued even where "
        "supply had stabilized, and expedited shipping remained a default rather than exception. The "
        "result was $380M in excess inventory and inflated logistics costs that eroded margins."
    )

    pdf.section_heading("4. Meridian's Solution")
    pdf.body_text(
        "Meridian designed and delivered a holistic supply chain transformation program comprising "
        "four integrated workstreams:"
    )
    pdf.section_heading("4.1 SAP IBP Implementation", level=2)
    pdf.body_text(
        "Meridian implemented SAP Integrated Business Planning (IBP) as the unified demand and supply "
        "planning platform across all 5 business units. The implementation covered Demand Planning, "
        "Supply Planning, Inventory Optimization, and Sales & Operations Planning (S&OP) modules. "
        "The team configured statistical forecasting models calibrated to the client's product hierarchy "
        "(15,000 active SKUs), integrated point-of-sale data from 8 key retail customers, and designed "
        "a monthly S&OP process connecting commercial demand signals to manufacturing capacity planning."
    )
    pdf.body_text(
        "A critical innovation was the integration of external demand signals, including commodity price "
        "indices, weather patterns, and macroeconomic indicators, into the IBP demand sensing engine. "
        "This AI-augmented approach improved short-term (4-week) forecast accuracy from 52% to 78%, "
        "significantly reducing the need for safety stock buffers."
    )

    pdf.add_page()
    pdf.section_heading("4.2 Supply Chain Control Tower", level=2)
    pdf.body_text(
        "Meridian designed and deployed a digital Supply Chain Control Tower providing real-time "
        "end-to-end visibility from supplier shipments through manufacturing to customer delivery. "
        "Built on a combination of SAP Digital Supply Chain and custom analytics layers, the control "
        "tower integrated data from 14 source systems including ERP, TMS, WMS, and supplier portals. "
        "Key capabilities included:"
    )
    pdf.bullet("Real-time inventory visibility across all 22 plants and 8 distribution centers (updated every 15 minutes)")
    pdf.bullet("Automated exception management with ML-based anomaly detection (identifying potential disruptions 5-7 days in advance)")
    pdf.bullet("Dynamic order promising engine incorporating real-time ATP (Available-to-Promise) across the network")
    pdf.bullet("Transportation visibility with GPS tracking integration for 85% of shipment volume")
    pdf.bullet("Executive dashboards with drill-down capability from enterprise KPIs to individual shipment level")

    pdf.section_heading("4.3 Supplier Collaboration Portal", level=2)
    pdf.body_text(
        "To address supplier visibility gaps, Meridian built a cloud-based Supplier Collaboration Portal "
        "using SAP Ariba and custom extensions. The portal enabled real-time purchase order collaboration, "
        "advance ship notice (ASN) exchange, quality certificate submission, and capacity commitment "
        "sharing. Within 6 months of launch, 280 of the top 300 suppliers (93%) were actively using "
        "the portal, reducing purchase order cycle time from 5.2 days to 1.8 days and improving supplier "
        "on-time delivery from 78% to 91%."
    )

    pdf.section_heading("4.4 Sustainability & Scope 3 Emissions Visibility", level=2)
    pdf.body_text(
        "Meridian integrated an ESG data collection module into the Supplier Collaboration Portal, "
        "enabling standardized Scope 3 emissions data collection aligned with the GHG Protocol. The team "
        "developed supplier-specific emissions factors for the top 200 suppliers (representing 82% of "
        "procurement spend) using a combination of primary data collection and industry-average estimation "
        "models. This created the foundation for the client's first comprehensive Scope 3 emissions "
        "baseline, enabling target-setting and progress tracking against SBTi commitments."
    )

    # --- Team Composition (NEW section with named team members) ---
    pdf.add_page()
    pdf.section_heading("5. Team Composition")
    pdf.body_text(
        "The engagement was led by James O'Sullivan, Meridian's Manufacturing & Industrial Practice Lead, "
        "with a senior team combining deep SAP/ERP expertise, data analytics capabilities, and supply "
        "chain domain knowledge."
    )
    pdf.add_table(
        ["Role", "Name", "Specialization", "Allocation"],
        [
            ["Lead Partner", "James O'Sullivan, CPA", "Mfg. & Supply Chain", "35%"],
            ["Sr. Mgr - Technology", "David Kim, PMP, SAP", "SAP IBP / ERP", "80%"],
            ["Mgr - Data/Analytics", "Raj Krishnamurthy", "Data Analytics / ML", "100%"],
            ["Sr. Consultant - SAP", "Marcus Wright", "SAP FICO", "100%"],
            ["Sr. Consultant - SAP", "Kwame Asante", "SAP S/4HANA FICO", "100%"],
            ["Consultant - Data Eng.", "Jessica Huang", "Data Engineering", "90%"],
            ["Staff - Risk Advisory", "Emily Nakamura", "Risk Advisory", "80%"],
        ],
        col_widths=[45, 45, 48, 25],
    )
    pdf.body_text(
        "Beyond the senior team, the program included 2 additional Senior Managers, 6 Managers, "
        "18 Senior Consultants, 22 Consultants, and 15 Analysts. At peak, 45 professionals were onshore "
        "(Chicago and client sites) with 20 offshore (Hyderabad GDC)."
    )
    pdf.section_heading("Key Team Contributions", level=2)
    pdf.bullet("David Kim led the SAP IBP implementation as overall technical architect, leveraging his experience from 11 prior full-lifecycle ERP implementations to design the integrated planning platform configuration")
    pdf.bullet("Raj Krishnamurthy built the AI-augmented demand sensing engine, integrating external signals (commodity prices, weather, macroeconomic indicators) with historical demand data using AWS SageMaker and Databricks")
    pdf.bullet("Marcus Wright configured the SAP FICO financial integration between IBP and the core ERP, ensuring inventory valuation, cost allocation, and financial reporting alignment across all 5 business units")
    pdf.bullet("Kwame Asante led the SAP S/4HANA FICO workstream for the Supplier Collaboration Portal, configuring accounts payable automation, purchase order matching, and supplier payment optimization")
    pdf.bullet("Jessica Huang designed and built the data integration pipelines connecting 14 source systems to the Control Tower, processing over 2 million data events daily with sub-minute latency")
    pdf.bullet("Emily Nakamura conducted the supply chain risk assessment and designed the continuous monitoring framework for supplier financial health, geopolitical risk, and concentration risk across the 3,400-supplier network")

    # --- Delivery Approach ---
    pdf.section_heading("6. Delivery Approach")
    pdf.body_text("The 16-month program was delivered in three phases:")
    pdf.bold_bullet("Phase 1 - Design & Foundation (Months 1-4)", "Current state assessment, root cause analysis, solution architecture, IBP system design, control tower requirements, supplier portal MVP design")
    pdf.bold_bullet("Phase 2 - Build & Deploy (Months 5-12)", "IBP configuration and testing, control tower development, supplier onboarding (3 waves), network optimization analysis, change management")
    pdf.bold_bullet("Phase 3 - Optimize & Scale (Months 13-16)", "ML model tuning, advanced analytics deployment, remaining supplier onboarding, benefits realization, knowledge transfer")

    # --- Results ---
    pdf.add_page()
    pdf.section_heading("7. Results & Impact")
    pdf.ln(2)
    pdf.results_table(
        ["Metric", "Baseline", "Result", "Improvement"],
        [
            ["Inventory Level", "$380M (74 DOS)", "$274M (48 DOS)", "28% reduction"],
            ["Working Capital Freed", "-", "$106M", "One-time release"],
            ["OTIF Delivery", "82%", "95%", "+13 points"],
            ["Forecast Accuracy (4-wk)", "52%", "78%", "+26 points"],
            ["Logistics Cost", "$412M/year", "$338M/year", "18% reduction"],
            ["Supplier On-Time Delivery", "78%", "91%", "+13 points"],
            ["Scope 3 Data Coverage", "6% of suppliers", "Top 200 (82% spend)", "Full visibility"],
        ],
        col_widths=[60, 42, 42, 46],
    )

    # --- Expanded: Lessons Learned ---
    pdf.section_heading("8. Lessons Learned & Transferable Insights")
    pdf.bold_bullet("Enterprise S&OP Is the Foundation",
        "The single most impactful element of the transformation was the establishment of a monthly "
        "enterprise S&OP process that forced cross-BU demand aggregation and capacity balancing. "
        "Technology enablement (SAP IBP) was necessary but insufficient without the governance and "
        "organizational alignment that the S&OP cadence provided.")
    pdf.bold_bullet("Post-Crisis Parameter Reset Is Critical",
        "Organizations that built supply chain buffers during the 2020-2022 disruptions must "
        "systematically review and right-size those parameters. The client's $380M inventory position "
        "was not the result of a single decision but the cumulative effect of hundreds of crisis-era "
        "parameter changes that were never revisited.")
    pdf.bold_bullet("Supplier Collaboration Requires Mutual Value",
        "The Supplier Collaboration Portal achieved 93% adoption among top suppliers because it was "
        "designed to deliver value to suppliers (faster payment terms, demand visibility) rather than "
        "simply extracting data from them. Portals designed solely for buyer benefit typically achieve "
        "adoption rates below 40%.")
    pdf.bold_bullet("Data Engineering Is the Unsung Hero",
        "Jessica Huang's data integration work, connecting 14 source systems with sub-minute latency, "
        "was the technical foundation that enabled every other capability. Organizations that "
        "underinvest in data engineering infrastructure consistently struggle to realize the value of "
        "analytics and planning tools.")

    pdf.ln(4)
    pdf.section_heading("9. Client Testimonial")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6,
        '"Meridian transformed our supply chain from a cost center and constant source of frustration '
        'into a genuine competitive advantage. The $106 million in freed working capital alone more '
        'than justified the investment, but the real game-changer has been the visibility -- for the '
        'first time, we can see our entire supply chain in real time and make decisions proactively '
        'rather than reactively. Our customers have noticed the difference."')
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, "-- Chief Supply Chain Officer, Client Organization")

    pdf.output(os.path.join(OUTPUT_DIR, "case_study_manufacturing.pdf"))
    print("  Generated: case_study_manufacturing.pdf")


# =============================================================================
# 6. PUBLIC SECTOR CASE STUDY (expanded with team table)
# =============================================================================

def generate_case_study_public_sector():
    pdf = MeridianPDF(
        "Case Study: Enterprise Cloud\nMigration",
        "State Government Agency",
        client_confidential=True
    )
    pdf.cover_page(version="1.1", date="March 2026")

    pdf.add_page()
    pdf.section_heading("1. Engagement Overview")
    items = [
        ("Client:", "Large US state government agency (name withheld per contract)"),
        ("Industry:", "Public Sector - State Government"),
        ("Engagement Type:", "Enterprise Cloud Migration & Modernization"),
        ("Duration:", "30 months (January 2023 - June 2025)"),
        ("Team Size:", "90 professionals at peak staffing"),
        ("Total Fees:", "$32.6 million"),
        ("Lead Partner:", "Dr. Priya Ramanathan, CISSP, TOGAF"),
        ("Meridian Offices:", "Washington, D.C. (lead), San Francisco, Hyderabad (GDC)"),
    ]
    for label, val in items:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(40, 40, 40)
        w = pdf.get_string_width(label) + 4
        pdf.cell(w, 6, label)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, val)
        pdf.ln(1)

    pdf.ln(3)
    pdf.section_heading("2. Client Situation & Challenge")
    pdf.body_text(
        "The client, one of the largest US state government agencies by IT budget, supported over "
        "45,000 state employees and delivered critical services to 12 million residents. The agency's "
        "IT infrastructure had accumulated significant technical debt over two decades, with the majority "
        "of systems hosted in two aging state-owned data centers. The Governor's office had mandated "
        "an enterprise cloud migration as a cornerstone of the state's Digital Government initiative, "
        "targeting measurable improvements in service delivery, security, and cost efficiency."
    )
    pdf.body_text("The agency faced a complex set of interrelated challenges:")
    pdf.bold_bullet("Aging Infrastructure", "60% of on-premises infrastructure was past manufacturer end-of-life, including 340 physical servers running Windows Server 2012 (end of extended support), 85 storage arrays averaging 8 years old, and network switches with known security vulnerabilities. The agency experienced an average of 14 unplanned outages per quarter, directly impacting citizen services.")
    pdf.bold_bullet("Security & Compliance", "The state had experienced a significant ransomware incident in 2021 affecting a neighboring agency, prompting executive-level urgency around security modernization. The target environment required FedRAMP High authorization equivalent (StateRAMP), CJIS compliance for law enforcement data, and IRS Publication 1075 compliance for tax systems.")
    pdf.bold_bullet("Application Portfolio Complexity", "The agency operated 2,500+ applications ranging from modern web applications to 25-year-old COBOL/CICS mainframe programs. An initial assessment revealed that 35% of applications had no documented architecture, 22% had no identified technical owner, and 18% were running on unsupported operating systems or middleware.")
    pdf.bold_bullet("Workforce Readiness", "The agency's IT workforce of 1,200 had limited cloud skills, with fewer than 40 staff holding cloud certifications. Additionally, the agency operated under state civil service rules that constrained hiring timelines and salary competitiveness, making external recruitment of cloud talent extremely challenging.")
    pdf.bold_bullet("Budget Constraints", "The migration needed to be funded within existing IT operating budgets, requiring the program to generate sufficient cost savings in early phases to self-fund subsequent phases. The legislature had approved a $15M one-time modernization appropriation to seed the program.")

    # --- Expanded: Governance & Procurement Context ---
    pdf.add_page()
    pdf.section_heading("3. Governance & Procurement Context")
    pdf.body_text(
        "Government IT modernization operates within a unique set of constraints that fundamentally "
        "shape program design and execution. Understanding these constraints was critical to Meridian's "
        "approach:"
    )
    pdf.section_heading("3.1 Legislative Oversight", level=2)
    pdf.body_text(
        "The program operated under direct oversight from the state legislature's Joint Committee on "
        "Technology, which required quarterly progress reports and retained approval authority for "
        "expenditures exceeding $5M. Meridian's team prepared 10 quarterly legislative briefings over "
        "the engagement period, translating technical migration progress into business outcome metrics "
        "that resonated with non-technical legislative stakeholders. The team also supported three "
        "formal legislative hearings where program leadership testified on progress, challenges, and "
        "cost savings achieved."
    )
    pdf.section_heading("3.2 Procurement Compliance", level=2)
    pdf.body_text(
        "All technology procurements within the program were subject to the state's competitive "
        "procurement requirements, including formal RFP processes for engagements exceeding $250K "
        "and sole-source justification requirements for specialized services. Meridian worked within "
        "these constraints by front-loading procurement activities during the foundation phase, "
        "establishing master service agreements with pre-approved cloud service providers, and "
        "developing procurement templates that reduced the average procurement cycle from 120 days "
        "to 45 days while maintaining full compliance with state procurement law."
    )
    pdf.section_heading("3.3 Labor Relations", level=2)
    pdf.body_text(
        "The migration raised concerns among the state employee union regarding potential workforce "
        "displacement. Meridian worked with agency leadership and union representatives to develop a "
        "workforce transition plan that committed to no involuntary reductions in force, funded cloud "
        "training for all 1,200 IT staff, and created new cloud operations roles that offered career "
        "advancement opportunities. This proactive engagement secured union support for the program "
        "and avoided any labor actions that could have disrupted the migration timeline."
    )

    pdf.section_heading("4. Meridian's Solution")
    pdf.body_text(
        "Meridian designed and executed a comprehensive enterprise cloud migration program using a "
        "modified 6R framework (Rehost, Replatform, Refactor, Rearchitect, Retire, Retain) tailored "
        "to the unique requirements of government IT:"
    )

    pdf.section_heading("4.1 Cloud Foundation & Landing Zone", level=2)
    pdf.body_text(
        "Meridian designed and deployed a secure Azure Government landing zone aligned with the Microsoft "
        "Cloud Adoption Framework and customized for state government compliance requirements. The landing "
        "zone included:"
    )
    pdf.bullet("Hub-and-spoke network topology with centralized firewall (Azure Firewall Premium) and DDoS protection")
    pdf.bullet("Identity integration with the agency's on-premises Active Directory via Azure AD Connect with staged rollover")
    pdf.bullet("Azure Policy guardrails enforcing StateRAMP, CJIS, and IRS 1075 controls at the subscription level")
    pdf.bullet("Centralized logging and SIEM integration (Microsoft Sentinel) for security monitoring")
    pdf.bullet("Automated Infrastructure as Code (IaC) deployment using Terraform modules, enabling standardized, repeatable provisioning")
    pdf.bullet("Cost management framework with automated budget alerts, reserved instance optimization, and chargeback reporting by agency division")

    pdf.add_page()
    pdf.section_heading("4.2 Application Migration (6R Disposition)", level=2)
    pdf.body_text(
        "Meridian conducted a comprehensive assessment of all 2,500 applications and developed a "
        "disposition recommendation for each based on business criticality, technical complexity, "
        "compliance requirements, and total cost of ownership. The disposition breakdown was:"
    )
    pdf.bold_bullet("Rehost (Lift & Shift)", "680 applications (27%) migrated to Azure IaaS with minimal modification. Targeted applications with modern-ish architecture but no immediate business case for refactoring.")
    pdf.bold_bullet("Replatform", "420 applications (17%) migrated with targeted optimizations, such as moving databases from self-managed SQL Server to Azure SQL Managed Instance, or shifting web workloads to Azure App Service.")
    pdf.bold_bullet("Refactor / Rearchitect", "340 applications (14%) redesigned as cloud-native services using Azure Kubernetes Service (AKS), Azure Functions, and managed PaaS services. Focused on high-value, citizen-facing applications.")
    pdf.bold_bullet("Retire", "700 applications (28%) identified for decommissioning based on redundancy analysis, zero/low usage, or availability of SaaS replacements. Retirement of these applications eliminated $4.2M in annual licensing and maintenance costs.")
    pdf.bold_bullet("Retain (On-Premises)", "360 applications (14%) retained on-premises due to mainframe dependencies, specialized hardware requirements, or compliance constraints. These will be addressed in a future modernization phase.")

    pdf.section_heading("4.3 DevSecOps Pipeline", level=2)
    pdf.body_text(
        "Meridian established an enterprise DevSecOps platform to standardize application deployment, "
        "security scanning, and change management across the migrated portfolio. Built on Azure DevOps "
        "with integrated security tooling, the pipeline included:"
    )
    pdf.bullet("Automated CI/CD pipelines with mandatory stages: build, SAST (SonarQube), DAST (OWASP ZAP), container scanning (Trivy), infrastructure validation (Terraform plan), and deployment")
    pdf.bullet("Pre-configured pipeline templates for common application archetypes (web app, API, batch job, data pipeline)")
    pdf.bullet("Integrated change management workflow aligned with the agency's ITIL-based CAB process")
    pdf.bullet("Secrets management via Azure Key Vault with automated rotation")
    pdf.bullet("Compliance-as-Code validation ensuring every deployment meets StateRAMP controls")

    pdf.add_page()
    pdf.section_heading("4.4 Modern Workplace (Microsoft 365 & Teams)", level=2)
    pdf.body_text(
        "As part of the broader modernization initiative, Meridian led the migration of 45,000 users from "
        "on-premises Exchange 2016 and legacy file shares to Microsoft 365 (Exchange Online, SharePoint "
        "Online, OneDrive, Teams). The migration was executed over 12 weekends using a wave-based approach, "
        "with zero data loss and less than 30 minutes of mail delivery delay per user. The deployment "
        "included Microsoft Teams as the unified communications platform, replacing a fragmented mix of "
        "Cisco Jabber, Skype for Business, and ad-hoc Zoom accounts."
    )

    # --- Team Composition (NEW section with named team members) ---
    pdf.section_heading("5. Team Composition")
    pdf.body_text(
        "The engagement was led by Dr. Priya Ramanathan, Meridian's Technology & Digital Advisory Practice "
        "Lead, with a senior team combining deep cybersecurity expertise, IT audit and GRC capabilities, "
        "cloud infrastructure skills, and public sector program management experience."
    )
    pdf.add_table(
        ["Role", "Name", "Specialization", "Allocation"],
        [
            ["Lead Partner", "Dr. Priya Ramanathan, CISSP", "Technology & Public Sector", "30%"],
            ["Sr. Mgr - Cybersecurity", "Alex Petrov, CISSP, CISM", "Security Architecture", "80%"],
            ["Mgr - IT Audit / GRC", "Thomas Chen, CISA, CISSP", "IT Audit & Compliance", "90%"],
            ["Sr. Consultant - Cloud", "Jordan Lee", "Cloud Infrastructure", "100%"],
            ["Staff - PMO", "Derek Williams", "PMO Coordination", "100%"],
            ["Sr. Consultant - BA", "Olivia Brennan, CBAP", "BA / Testing", "90%"],
            ["Sr. Mgr - OCM", "Lauren Mitchell, SHRM-SCP", "Change Management", "70%"],
        ],
        col_widths=[45, 45, 48, 25],
    )
    pdf.body_text(
        "Beyond the senior team, the program included 3 additional Senior Managers, 8 Managers, "
        "24 Senior Consultants, 32 Consultants, and 21 Analysts. At peak, 55 professionals were onshore "
        "(D.C. and client data centers) with 35 offshore (Hyderabad GDC). A dedicated security team of "
        "12 included 3 FedRAMP-experienced assessors."
    )
    pdf.section_heading("Key Team Contributions", level=2)
    pdf.bullet("Alex Petrov designed the Azure Government security architecture, implementing zero-trust controls, CJIS-compliant network segmentation, and IRS 1075 data handling procedures, achieving StateRAMP High authorization on first assessment")
    pdf.bullet("Thomas Chen led the IT controls assessment for the migration, ensuring SOC 2 Type II readiness for the cloud environment and developing the compliance-as-code framework that automated control validation across all deployed workloads")
    pdf.bullet("Jordan Lee served as lead cloud architect, designing the Azure landing zone, configuring hub-and-spoke networking, and building the Terraform IaC modules that enabled standardized deployment of 1,800 applications")
    pdf.bullet("Derek Williams managed the integrated PMO across four phases, coordinating migration waves, legislative reporting, and vendor management with weekly dashboards tracking 400+ active work items")
    pdf.bullet("Olivia Brennan led requirements and testing for the 340 refactored citizen-facing applications, managing 4,800 test cases and user acceptance testing with agency subject matter experts across 22 divisions")
    pdf.bullet("Lauren Mitchell designed the workforce transition and training program, achieving 240 Azure certifications among agency IT staff and securing union support through proactive engagement and career path development")

    # --- Delivery Phases ---
    pdf.add_page()
    pdf.section_heading("6. Delivery Phases")
    pdf.section_heading("6.1 Phase 1 - Foundation (Months 1-6)", level=2)
    pdf.body_text(
        "Application discovery and assessment (2,500 applications), landing zone design and deployment, "
        "security framework development, migration factory setup, workforce training program launch. "
        "This phase also included the legislative briefing cadence establishment and procurement of "
        "Azure Government Reserved Instances to optimize first-year cloud spend. The phase concluded "
        "with the first legislative hearing, where the CIO presented the program roadmap and "
        "self-funding model."
    )
    pdf.section_heading("6.2 Phase 2 - Wave 1 Migration (Months 7-14)", level=2)
    pdf.body_text(
        "Migration of 600 applications (low-complexity rehost/replatform), M365 migration for 45,000 "
        "users, DevSecOps platform deployment, first cost savings realization. The wave targeted "
        "applications with well-documented architectures and clear technical owners, building migration "
        "factory momentum and organizational confidence. Cost savings from Wave 1 ($8.2M annualized) "
        "exceeded the threshold required to self-fund Phase 3, validating the program's financial model."
    )
    pdf.section_heading("6.3 Phase 3 - Wave 2 Migration (Months 15-24)", level=2)
    pdf.body_text(
        "Migration of 840 applications (medium/high complexity), refactoring of 340 citizen-facing "
        "applications to cloud-native architecture, application retirement execution (700 applications "
        "decommissioned), ongoing workforce development. This phase required significantly more technical "
        "depth per application, with average migration complexity scoring 3.2x higher than Wave 1. The "
        "refactored citizen-facing applications included the state's online tax filing system (1.8 million "
        "annual filings), benefits enrollment portal (420,000 users), and professional licensing system "
        "(890,000 active licenses)."
    )
    pdf.section_heading("6.4 Phase 4 - Optimization (Months 25-30)", level=2)
    pdf.body_text(
        "Performance tuning, cost optimization (right-sizing VMs, reserved instance optimization, storage "
        "tier management), remaining migrations, knowledge transfer, transition to managed operations, "
        "and benefits realization reporting. The team conducted a comprehensive cost optimization review "
        "that identified $3.8M in additional annual savings through right-sizing, auto-scaling, and "
        "storage lifecycle management."
    )

    # --- Results ---
    pdf.add_page()
    pdf.section_heading("7. Results & Impact")
    pdf.ln(2)
    pdf.results_table(
        ["Metric", "Baseline", "Result", "Improvement"],
        [
            ["Applications Migrated", "0 in cloud", "1,800 migrated", "72% of portfolio"],
            ["IT Operating Costs", "$52M/year", "$34M/year", "35% ($18M savings)"],
            ["System Availability", "99.2% (14 outages/qtr)", "99.95%", "Near-zero outages"],
            ["Security Incidents", "23/year", "0 during migration", "Zero incidents"],
            ["Mean Time to Deploy", "6-8 weeks", "2-4 hours", "99% faster"],
            ["Cloud Certifications", "38 staff", "278 staff", "632% increase"],
            ["Applications Retired", "-", "700 decommissioned", "$4.2M cost avoided"],
        ],
        col_widths=[60, 42, 42, 46],
    )

    pdf.body_text(
        "The agency was recognized with the state's annual IT Modernization Award and was rated "
        '"Leader" in the National Association of State CIOs (NASCIO) State IT Modernization Index for '
        "the first time in its history. The program's self-funding model, in which early-phase cost "
        "savings funded subsequent phases, has been adopted as a reference model by three other state "
        "agencies planning similar migrations."
    )

    # --- Expanded: Lessons Learned ---
    pdf.section_heading("8. Lessons Learned & Transferable Insights")
    pdf.bold_bullet("Self-Funding Models Unlock Government Modernization",
        "The program's most innovative element was its self-funding financial model, where Wave 1 "
        "cost savings funded subsequent phases. This approach eliminated the need for large upfront "
        "legislative appropriations and created a sustainable funding mechanism. Other state agencies "
        "have since adopted this model, and Meridian has incorporated it as a standard element of "
        "our public sector cloud migration methodology.")
    pdf.bold_bullet("Security Is the Enabler, Not the Blocker",
        "By front-loading security architecture design and embedding compliance-as-code from Day 1, "
        "Alex Petrov's team ensured that security accelerated rather than impeded the migration. "
        "The StateRAMP High first-pass authorization demonstrated that cloud environments can meet "
        "or exceed the security posture of on-premises data centers when properly architected.")
    pdf.bold_bullet("Workforce Development Is a Strategic Investment",
        "The 240 Azure certifications achieved by agency staff transformed the IT organization from "
        "cloud-resistant to cloud-proficient. Lauren Mitchell's workforce transition program, "
        "including union engagement and career path development, ensured that modernization was "
        "viewed as an opportunity rather than a threat by the existing workforce.")

    pdf.ln(4)
    pdf.section_heading("9. Client Testimonial")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6,
        '"This was the most complex technology program our agency has ever undertaken, and Meridian '
        'was the right partner at every step. They brought deep Azure Government expertise, an '
        'unwavering focus on security, and a pragmatic approach to managing our unique government '
        'constraints -- from procurement rules to workforce development. The fact that we migrated '
        '1,800 applications with zero security incidents is a testament to their methodology and '
        'the quality of their team."')
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, "-- Chief Information Officer, Client Agency")

    pdf.output(os.path.join(OUTPUT_DIR, "case_study_public_sector.pdf"))
    print("  Generated: case_study_public_sector.pdf")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Generating fixed case study PDFs...")
    generate_case_study_energy()
    generate_case_study_retail()
    generate_case_study_financial_services()
    generate_case_study_healthcare()
    generate_case_study_manufacturing()
    generate_case_study_public_sector()
    print("\nAll 6 case study PDFs generated successfully!")
