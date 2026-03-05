"""Generate 5 new synthetic PDFs for Meridian & Associates LLP knowledge base."""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# --- Helpers ----------------------------------------------------------------

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
        """Render a simple table with header row and data rows."""
        if col_widths is None:
            n = len(headers)
            col_widths = [190 / n] * n
        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        # Rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in rows:
            self.set_fill_color(240, 244, 248) if fill else self.set_fill_color(255, 255, 255)
            max_h = 7
            for i, cell_text in enumerate(row):
                self.cell(col_widths[i], 7, str(cell_text), border=1, fill=True, align="C")
            self.ln()
            fill = not fill
        self.ln(3)

    def add_wrapped_table(self, headers, rows, col_widths=None):
        """Render a table where cells can wrap text (using multi_cell)."""
        if col_widths is None:
            n = len(headers)
            col_widths = [190 / n] * n
        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        # Rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        fill_toggle = False
        for row in rows:
            if fill_toggle:
                self.set_fill_color(240, 244, 248)
            else:
                self.set_fill_color(255, 255, 255)
            # Calculate row height
            line_heights = []
            for i, cell_text in enumerate(row):
                nb_lines = max(1, len(self.multi_cell(col_widths[i], 5, str(cell_text), split_only=True)))
                line_heights.append(nb_lines * 5.5)
            row_h = max(line_heights)
            row_h = max(row_h, 7)
            # Check page break
            if self.get_y() + row_h > self.h - self.b_margin:
                self.add_page()
                # Reprint header
                self.set_font("Helvetica", "B", 9)
                self.set_fill_color(0, 51, 102)
                self.set_text_color(255, 255, 255)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
                self.ln()
                self.set_font("Helvetica", "", 9)
                self.set_text_color(40, 40, 40)
                if fill_toggle:
                    self.set_fill_color(240, 244, 248)
                else:
                    self.set_fill_color(255, 255, 255)
            x_start = self.get_x()
            y_start = self.get_y()
            for i, cell_text in enumerate(row):
                x = x_start + sum(col_widths[:i])
                self.set_xy(x, y_start)
                self.cell(col_widths[i], row_h, "", border=1, fill=True)
                self.set_xy(x + 1, y_start + 1)
                self.multi_cell(col_widths[i] - 2, 5.5, str(cell_text))
            self.set_xy(x_start, y_start + row_h)
            fill_toggle = not fill_toggle
        self.ln(3)


# =============================================================================
# 1. CASE STUDY: ENERGY SECTOR
# =============================================================================

def generate_case_study_energy():
    pdf = MeridianPDF(
        "Case Study: Energy Sector",
        "Streamlining Regulatory Compliance and Financial Reporting\nfor a Major Upstream Oil & Gas Producer",
        client_confidential=True,
    )
    pdf.cover_page(version="2.1", date="February 2026")

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

    # Key metrics box
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

    # --- Page 4-5: Meridian's Approach ---
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

    # --- Page 6: Team Composition ---
    pdf.add_page()
    pdf.section_heading("5. Team Composition")
    pdf.body_text(
        "Meridian deployed a cross-functional team drawn from three service lines, with deep energy "
        "sector expertise at every level. The team was structured to provide continuous coverage across "
        "the client's six office locations while maintaining centralized quality oversight."
    )

    pdf.add_table(
        ["Role", "Name", "Service Line", "Specialization", "Allocation"],
        [
            ["Lead Engagement Partner", "David Kessler, CPA", "Assurance", "Oil & Gas Audit", "40%"],
            ["Tax Partner", "Lisa Nakamura, JD, CPA", "Tax", "Energy Tax", "30%"],
            ["Advisory Partner", "James Whitfield, CPA", "Advisory", "SOX / Internal Controls", "25%"],
            ["Concurring Partner", "Robert Daniels, CPA", "Assurance", "SEC Reporting", "10%"],
            ["Sr. Manager - Audit", "Karen Okoye, CPA", "Assurance", "E&P Accounting", "80%"],
            ["Sr. Manager - Tax", "Vijay Patel, CPA, MST", "Tax", "Tax Provision", "70%"],
            ["Manager - SOX", "Angela Rivera, CIA", "Advisory", "Process Controls", "100%"],
            ["Manager - Audit", "Thomas Bergman, CPA", "Assurance", "Reserves/ARO", "90%"],
            ["Petroleum Engineer", "Dr. Wei Zhang, PE", "Advisory", "Reserve Estimation", "50%"],
            ["Data Analytics Lead", "Samuel Obi", "Advisory", "MeridianAI Platform", "60%"],
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
    pdf.bullet("4 team members hold petroleum engineering credentials")
    pdf.bullet("6 team members are certified in SAP S/4HANA financial modules")
    pdf.bullet("3 team members hold CISA (Certified Information Systems Auditor) credentials")
    pdf.bullet("2 team members are former SEC Division of Corporation Finance staff")

    # --- Page 7: Outcomes ---
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

    # --- Page 8: Timeline ---
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
# 2. CASE STUDY: RETAIL / CONSUMER
# =============================================================================

def generate_case_study_retail():
    pdf = MeridianPDF(
        "Case Study: Retail & Consumer",
        "Omnichannel Transformation and Revenue Recognition Overhaul\nfor a National Retailer",
        client_confidential=True,
    )
    pdf.cover_page(version="1.4", date="January 2026")

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

    # --- Team Composition ---
    pdf.add_page()
    pdf.section_heading("5. Team Composition")
    pdf.add_table(
        ["Role", "Name", "Specialization", "Allocation"],
        [
            ["Lead Engagement Partner", "Rebecca Hartwell, CPA", "Retail Advisory", "35%"],
            ["Technical Accounting Partner", "David Sokolov, CPA", "ASC 606 / Revenue", "25%"],
            ["Tax Partner", "Patricia Mendez, JD, LLM", "Retail Tax / SALT", "15%"],
            ["Sr. Manager - Revenue", "Chris Takahashi, CPA", "Revenue Recognition", "90%"],
            ["Sr. Manager - Inventory", "Diana Lawson, CPA", "Inventory / SCM", "80%"],
            ["Manager - Analytics", "Priya Sundaram, CFA", "Data Analytics / ML", "100%"],
            ["Manager - Systems", "Eric Johansson", "Oracle Cloud / ERP", "85%"],
            ["Manager - Loyalty", "Natasha Brooks, CPA", "Customer Analytics", "75%"],
            ["Sr. Associate Team (8)", "Various", "Mixed Specializations", "100%"],
            ["Associate Team (12)", "Various", "Audit & Advisory", "100%"],
        ],
        col_widths=[45, 45, 48, 25],
    )
    pdf.body_text(
        "Total engagement hours over the 24-month period were approximately 42,000. The team included "
        "professionals from four Meridian offices (Chicago, New York, Dallas, and Los Angeles) with "
        "regular on-site presence at the client's headquarters and primary distribution center."
    )

    # --- Outcomes ---
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

    pdf.add_page()
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
# 3. FIRM CAPABILITIES OVERVIEW
# =============================================================================

def generate_firm_capabilities():
    pdf = MeridianPDF(
        "Firm Capabilities Overview",
        "Meridian & Associates LLP\nComprehensive Service & Industry Portfolio",
    )
    pdf.cover_page(version="5.0", date="March 2026")

    # --- About Meridian ---
    pdf.add_page()
    pdf.section_heading("1. About Meridian & Associates LLP")
    pdf.body_text(
        "Meridian & Associates LLP is a top-20 professional services firm providing audit, tax, advisory, "
        "and consulting services to organizations ranging from high-growth middle-market companies to "
        "Fortune 500 enterprises. Founded in 1987 by three partners who departed a Big Four firm with a "
        "vision to build a more client-centric, technology-forward professional services organization, "
        "Meridian has grown over 38 years into a global platform with $2.8 billion in annual revenue "
        "and more than 12,000 professionals across 45 offices worldwide."
    )
    pdf.body_text(
        "Our founding principles - technical excellence, client service, innovation, and integrity - "
        "continue to guide every engagement. Meridian has been recognized by the AICPA as a Firm of "
        "the Year (2024), named to Forbes' Best Management Consulting Firms list for seven consecutive "
        "years, and maintains a client retention rate of 94% across all service lines."
    )

    pdf.section_heading("Firm at a Glance", level=2)
    pdf.add_table(
        ["Attribute", "Detail"],
        [
            ["Founded", "1987 (38 years)"],
            ["Headquarters", "New York, NY"],
            ["Annual Revenue", "$2.8 billion (FY 2025)"],
            ["Professionals", "12,400+"],
            ["Partners", "680+"],
            ["Global Offices", "45 (32 US, 13 international)"],
            ["Industries Served", "7 core verticals"],
            ["Service Lines", "4 primary lines"],
            ["Client Retention Rate", "94%"],
            ["PCAOB Registered", "Yes - No Part II quality control criticisms in any PCAOB inspection cycle since registration"],
        ],
        col_widths=[60, 130],
    )

    # --- Service Lines ---
    pdf.add_page()
    pdf.section_heading("2. Service Lines")

    pdf.section_heading("2.1 Audit & Assurance ($1.12B Revenue | 4,200+ Professionals)", level=2)
    pdf.body_text(
        "Meridian's Audit & Assurance practice provides independent financial statement audits, integrated "
        "audits (including SOX Section 404 attestation), reviews, compilations, and attestation services. "
        "We serve over 320 SEC registrants and 1,800 private companies. Our technology-enabled audit "
        "methodology leverages the MeridianAI analytics platform for 100% transaction testing, anomaly "
        "detection, and continuous auditing capabilities."
    )
    pdf.section_heading("Key Capabilities:", level=3)
    pdf.bullet("Financial statement audits (PCAOB and AICPA standards)")
    pdf.bullet("Integrated audits with SOX Section 404 internal controls attestation")
    pdf.bullet("SEC reporting advisory (10-K, 10-Q, 8-K, S-1/S-3 registration statements)")
    pdf.bullet("IFRS reporting and US GAAP to IFRS conversion")
    pdf.bullet("Employee benefit plan audits (401(k), defined benefit, ESOP)")
    pdf.bullet("Service organization audits (SOC 1, SOC 2, SOC 3)")
    pdf.bullet("Agreed-upon procedures and compliance attestation")
    pdf.bullet("IPO readiness and de-SPAC transaction support")

    pdf.section_heading("2.2 Tax Services ($784M Revenue | 3,100+ Professionals)", level=2)
    pdf.body_text(
        "Our Tax Services practice delivers comprehensive tax planning, compliance, and controversy "
        "support across all federal, state, local, and international jurisdictions. We combine deep "
        "technical knowledge with industry specialization to help clients optimize their tax positions "
        "while maintaining full compliance. Our tax technology practice is a recognized leader in "
        "provision automation, transfer pricing documentation, and R&D credit studies."
    )
    pdf.section_heading("Key Capabilities:", level=3)
    pdf.bullet("Federal and state/local tax compliance and planning")
    pdf.bullet("International tax structuring and transfer pricing")
    pdf.bullet("Tax provision preparation and automation (ASC 740)")
    pdf.bullet("R&D tax credit studies (Section 41)")
    pdf.bullet("State and local tax (SALT) advisory and controversy")
    pdf.bullet("M&A tax due diligence and structuring")
    pdf.bullet("Tax controversy and IRS examination support")
    pdf.bullet("Private client services (high-net-worth, family office, estate planning)")
    pdf.bullet("Indirect tax (sales & use tax, VAT, customs)")

    pdf.add_page()
    pdf.section_heading("2.3 Advisory & Consulting ($728M Revenue | 3,800+ Professionals)", level=2)
    pdf.body_text(
        "Meridian's Advisory & Consulting practice helps organizations navigate complex business "
        "challenges across strategy, operations, technology, risk, and transactions. Our consultants "
        "bring a unique combination of deep industry knowledge and functional expertise, supported by "
        "proprietary tools and methodologies. We serve clients across the full lifecycle of business "
        "transformation, from strategy development through implementation and sustained performance "
        "improvement."
    )
    pdf.section_heading("Key Capabilities:", level=3)
    pdf.bullet("Business transformation and operating model design")
    pdf.bullet("Technology advisory (ERP, cloud migration, digital transformation)")
    pdf.bullet("Cybersecurity and data privacy (assessment, implementation, managed services)")
    pdf.bullet("Risk advisory (enterprise risk management, internal audit co-sourcing, compliance)")
    pdf.bullet("Transaction advisory (financial due diligence, valuation, integration)")
    pdf.bullet("Forensic and dispute services (investigations, litigation support, expert testimony)")
    pdf.bullet("Performance improvement (cost optimization, process reengineering)")
    pdf.bullet("Data analytics and artificial intelligence advisory")
    pdf.bullet("Environmental, social, and governance (ESG) advisory and assurance")

    pdf.section_heading("2.4 Managed Services ($168M Revenue | 1,300+ Professionals)", level=2)
    pdf.body_text(
        "Our newest service line, Managed Services, provides ongoing outsourced and co-sourced "
        "professional services on a recurring basis. Launched in 2020, this practice has grown at "
        "a 28% compound annual rate and addresses the increasing demand for flexible, scalable "
        "professional service delivery models."
    )
    pdf.bullet("Finance and accounting outsourcing (FAO)")
    pdf.bullet("Tax compliance co-sourcing")
    pdf.bullet("Internal audit co-sourcing and outsourcing")
    pdf.bullet("Regulatory compliance monitoring")
    pdf.bullet("Continuous controls monitoring")
    pdf.bullet("Cybersecurity managed detection and response")

    # --- Industry Specializations ---
    pdf.add_page()
    pdf.section_heading("3. Industry Specializations")
    pdf.body_text(
        "Meridian organizes its client service delivery around seven core industry verticals, each led "
        "by a dedicated National Industry Leader with a team of specialized partners, directors, and "
        "professionals. This structure ensures that every engagement team brings relevant industry "
        "context, regulatory knowledge, and sector-specific benchmarking capabilities."
    )

    pdf.section_heading("3.1 Financial Services", level=2)
    pdf.key_value("Revenue", "$520M")
    pdf.key_value("Professionals", "2,100+")
    pdf.key_value("Industry Leader", "Sarah Chen, CPA, CISA")
    pdf.body_text(
        "Sub-sectors: Commercial and retail banking, capital markets, insurance (P&C, life, health), "
        "asset and wealth management, fintech, private equity, and real estate investment trusts. "
        "Key regulatory expertise includes Basel III/IV, Dodd-Frank, CECL, LDTI, and state insurance "
        "department requirements."
    )

    pdf.section_heading("3.2 Healthcare & Life Sciences", level=2)
    pdf.key_value("Revenue", "$410M")
    pdf.key_value("Professionals", "1,650+")
    pdf.key_value("Industry Leader", "Michael Torres, CPA, PMP")
    pdf.body_text(
        "Sub-sectors: Health systems and hospitals, physician practices, pharmaceutical manufacturers, "
        "medical device companies, health insurance plans, biotechnology, and digital health. Regulatory "
        "expertise includes Medicare/Medicaid compliance, Stark Law, Anti-Kickback Statute, HIPAA, "
        "FDA compliance, and 340B program requirements."
    )

    pdf.section_heading("3.3 Technology & Media", level=2)
    pdf.key_value("Revenue", "$380M")
    pdf.key_value("Professionals", "1,500+")
    pdf.key_value("Industry Leader", "Jennifer Walsh, CPA")
    pdf.body_text(
        "Sub-sectors: Enterprise software, SaaS, semiconductors, hardware, telecommunications, media "
        "and entertainment, gaming, and digital advertising. Technical expertise includes ASC 606 for "
        "software/SaaS revenue, stock-based compensation, business combinations, and IPO readiness."
    )

    pdf.section_heading("3.4 Energy & Natural Resources", level=2)
    pdf.key_value("Revenue", "$340M")
    pdf.key_value("Professionals", "1,350+")
    pdf.key_value("Industry Leader", "David Kessler, CPA")
    pdf.body_text(
        "Sub-sectors: Upstream oil & gas (E&P), midstream (gathering, processing, transportation), "
        "downstream (refining, marketing), oilfield services, mining and metals, utilities, and "
        "renewable energy. Technical expertise includes successful-efforts and full-cost accounting, "
        "ARO estimation, commodity derivatives, and FERC regulatory accounting."
    )

    pdf.add_page()
    pdf.section_heading("3.5 Manufacturing & Distribution", level=2)
    pdf.key_value("Revenue", "$320M")
    pdf.key_value("Professionals", "1,280+")
    pdf.key_value("Industry Leader", "Paul Krenzer, CPA, CISA")
    pdf.body_text(
        "Sub-sectors: Industrial manufacturing, aerospace and defense, automotive, chemicals, building "
        "products, food and beverage manufacturing, wholesale distribution, and logistics. Key expertise "
        "includes supply chain optimization, cost accounting, contract manufacturing arrangements, and "
        "international trade compliance."
    )

    pdf.section_heading("3.6 Retail & Consumer", level=2)
    pdf.key_value("Revenue", "$290M")
    pdf.key_value("Professionals", "1,160+")
    pdf.key_value("Industry Leader", "Rebecca Hartwell, CPA")
    pdf.body_text(
        "Sub-sectors: Specialty retail, department stores, grocery and convenience, e-commerce, "
        "consumer products (CPG), restaurants and hospitality, and direct-to-consumer brands. Key "
        "expertise includes ASC 606 for complex retail arrangements, loyalty program accounting, "
        "lease accounting (ASC 842) for large store portfolios, and inventory optimization."
    )

    pdf.section_heading("3.7 Public Sector & Not-for-Profit", level=2)
    pdf.key_value("Revenue", "$220M")
    pdf.key_value("Professionals", "960+")
    pdf.key_value("Industry Leader", "Margaret Okonkwo, CPA, CGFM")
    pdf.body_text(
        "Sub-sectors: Federal agencies, state and local governments, higher education, K-12 school "
        "districts, healthcare not-for-profits, foundations, and NGOs. Key expertise includes "
        "Uniform Guidance (2 CFR 200) compliance, GASB reporting, single audits, grant management, "
        "and cost allocation methodologies."
    )

    # --- Technology & Innovation ---
    pdf.add_page()
    pdf.section_heading("4. Technology & Innovation")

    pdf.section_heading("4.1 MeridianAI Platform", level=2)
    pdf.body_text(
        "MeridianAI is Meridian's proprietary artificial intelligence and data analytics platform, "
        "developed in-house by our Technology Innovation Lab (a team of 85 data scientists, engineers, "
        "and product managers). The platform is deployed across all audit and advisory engagements "
        "and includes the following capabilities:"
    )
    pdf.bullet("Full-population journal entry testing and anomaly detection (replacing statistical sampling)")
    pdf.bullet("Continuous auditing with real-time exception monitoring")
    pdf.bullet("Natural language processing for contract analysis and lease abstraction")
    pdf.bullet("Predictive analytics for revenue forecasting and impairment testing")
    pdf.bullet("Automated workpaper generation and cross-referencing")
    pdf.bullet("Client benchmarking across industry peers (anonymized datasets)")
    pdf.body_text(
        "MeridianAI processes over 4.2 billion transactions annually across our client portfolio and "
        "has been independently validated by the PCAOB for use in audit engagements. The platform has "
        "reduced average audit hours by 18% while improving defect detection rates by 35%."
    )

    pdf.section_heading("4.2 Data Analytics Center of Excellence", level=2)
    pdf.body_text(
        "Our Data Analytics Center of Excellence (DACe), headquartered in Chicago with satellite teams "
        "in Bangalore and London, provides specialized analytics services to engagement teams and "
        "directly to clients. DACe maintains expertise in Python, R, SQL, Power BI, Tableau, and "
        "major cloud analytics platforms (Azure Synapse, AWS Redshift, Google BigQuery). The center "
        "supports over 400 engagements annually and has developed 120+ reusable analytics assets "
        "tailored to specific industry and service line needs."
    )

    pdf.section_heading("4.3 Strategic Technology Alliances", level=2)
    pdf.body_text(
        "Meridian maintains strategic alliances with leading technology providers to enhance our service "
        "delivery capabilities and provide integrated solutions to clients:"
    )
    pdf.bold_bullet("Microsoft", "Gold Partner for Azure, Dynamics 365, and Microsoft 365. Over 350 "
                    "certified professionals. Joint solutions for cloud migration, ERP implementation, "
                    "and cybersecurity.")
    pdf.bold_bullet("SAP", "Recognized Partner for S/4HANA implementation and managed services. 180+ "
                    "certified consultants. Specialized capabilities in SAP for financial services, "
                    "manufacturing, and energy.")
    pdf.bold_bullet("ServiceNow", "Elite Partner for GRC, IT service management, and workflow automation. "
                    "120+ certified professionals. Joint solution accelerators for SOX compliance and "
                    "internal audit management.")
    pdf.bold_bullet("AWS", "Advanced Consulting Partner with competencies in financial services, healthcare, "
                    "and data analytics. 95+ certified architects. Specialized in cloud-native financial "
                    "reporting and analytics solutions.")
    pdf.bold_bullet("Oracle", "Platinum Partner for Oracle Cloud ERP and EPM. 140+ certified consultants. "
                    "Deep expertise in Oracle Financial Services applications.")

    # --- Awards & Differentiators ---
    pdf.add_page()
    pdf.section_heading("5. Awards & Recognition")
    pdf.bullet("AICPA Firm of the Year (2024)")
    pdf.bullet("Forbes Best Management Consulting Firms - 7 consecutive years (2020-2026)")
    pdf.bullet("Vault Accounting 50 - Ranked #8 overall, #1 in Culture (2026)")
    pdf.bullet("IDC MarketScape - Major Player in Business Consulting Services (2025)")
    pdf.bullet("Kennedy Vanguard Leader - Financial Services Consulting (2025)")
    pdf.bullet("Modern Healthcare - Top 10 Healthcare Advisory Firm (2022-2025)")
    pdf.bullet("CPA Practice Advisor - Top 10 Technology Innovator (2025)")
    pdf.bullet("Consulting Magazine - Best Firms to Work For - Top 10 (2024, 2025)")
    pdf.bullet("PCAOB Clean Inspection Record - All inspection cycles since registration")

    pdf.section_heading("6. Differentiators")
    pdf.section_heading("6.1 Integrated Delivery Model", level=2)
    pdf.body_text(
        "Unlike firms that operate as siloed practices, Meridian's integrated delivery model brings "
        "together audit, tax, and advisory professionals from the outset of every engagement. Our "
        "engagement leaders are evaluated on cross-service line collaboration, and our compensation "
        "model incentivizes integrated service delivery. This approach reduces redundancy, improves "
        "information sharing, and delivers more holistic solutions to clients."
    )

    pdf.section_heading("6.2 Partner-Led Engagement Model", level=2)
    pdf.body_text(
        "Meridian maintains a partner-to-staff ratio of 1:17, compared to the industry average of 1:25. "
        "This lower ratio ensures that partners are actively involved in day-to-day engagement execution, "
        "not just relationship management. Our engagement quality reviews consistently receive positive "
        "feedback for partner accessibility and senior team involvement."
    )

    pdf.section_heading("6.3 Industry Depth Over Breadth", level=2)
    pdf.body_text(
        "Our professionals are organized first by industry, then by service line. A Meridian energy "
        "audit manager spends 100% of their time on energy engagements, developing deep sector expertise "
        "that generalist firms cannot match. This specialization enables faster ramp-up times, more "
        "relevant insights, and fewer 'learning on your dime' situations for clients."
    )

    pdf.section_heading("6.4 Global Reach with Local Accountability", level=2)
    pdf.body_text(
        "Our 45-office footprint provides national and international coverage, but every engagement "
        "is led by a local partner with P&L accountability for the client relationship. This 'local "
        "partner, global platform' model ensures responsiveness and accountability while providing "
        "access to national and international specialist resources when needed."
    )

    path = os.path.join(OUTPUT_DIR, "firm_capabilities_overview.pdf")
    pdf.output(path)
    print(f"  Generated: {path}")


# =============================================================================
# 4. QA & DELIVERY METHODOLOGY
# =============================================================================

def generate_qa_methodology():
    # QA doc is firm-wide; use a subclass with standardized branding
    class QA_PDF(MeridianPDF):
        """Firm-wide QA doc with standardized header and footer."""
        def header(self):
            if self.page_no() == 1:
                return
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, "Meridian & Associates LLP  |  " + self.doc_title.replace("\n", " "),
                      new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(0, 51, 102)
            self.set_line_width(0.3)
            self.line(10, 13, 200, 13)
            self.ln(4)
            self.set_text_color(0, 0, 0)

        def footer(self):
            self.set_y(-18)
            self.set_draw_color(0, 51, 102)
            self.set_line_width(0.3)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(2)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 5, "CONFIDENTIAL", align="L")
            self.cell(0, 5, f"Page {self.page_no()}", align="R")
            self.set_text_color(0, 0, 0)

        def cover_page(self, version="1.0", date="March 2026"):
            self.add_page()
            # Top bar
            self.set_fill_color(0, 51, 102)
            self.rect(0, 0, 210, 45, "F")
            self.set_y(12)
            self.set_font("Helvetica", "B", 22)
            self.set_text_color(255, 255, 255)
            self.cell(0, 10, "MERIDIAN & ASSOCIATES LLP", align="C")
            self.ln(10)
            self.set_font("Helvetica", "", 10)
            self.cell(0, 6, "MERIDIAN & ASSOCIATES LLP | CONFIDENTIAL", align="C")
            self.ln(30)
            self.set_text_color(0, 51, 102)
            self.set_font("Helvetica", "B", 26)
            self.multi_cell(0, 12, self.doc_title, align="C")
            if self.doc_subtitle:
                self.ln(4)
                self.set_font("Helvetica", "", 14)
                self.set_text_color(80, 80, 80)
                self.multi_cell(0, 8, self.doc_subtitle, align="C")
            self.ln(4)
            # Firm-wide applicability note
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(0, 51, 102)
            self.cell(0, 8, "Firm-Wide Quality Standard -- Applicable to All Service Lines", align="C")
            self.ln(10)
            if self.confidential:
                self.set_font("Helvetica", "B", 12)
                self.set_text_color(180, 0, 0)
                self.cell(0, 8, "CONFIDENTIAL", align="C")
                self.ln(6)
            self.ln(6)
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

    pdf = QA_PDF(
        "Quality Assurance &\nDelivery Methodology",
        "Engagement Lifecycle, Quality Control Framework,\nand Continuous Improvement Standards",
        confidential=True,
    )
    pdf.cover_page(version="4.2", date="January 2026")

    # --- Overview ---
    pdf.add_page()
    pdf.section_heading("1. Overview")
    pdf.body_text(
        "Meridian & Associates LLP is committed to delivering the highest quality professional services "
        "on every engagement. This document describes our comprehensive quality assurance and delivery "
        "methodology, which governs all engagements across our Audit & Assurance, Tax Services, Advisory "
        "& Consulting, and Managed Services practices. Our quality framework is designed to meet or "
        "exceed the requirements of ISQM 1 (International Standard on Quality Management 1), PCAOB "
        "Quality Control standards, and the AICPA's Quality Management standards."
    )
    pdf.body_text(
        "This methodology is maintained by the National Director of Quality & Risk Management, reviewed "
        "annually by the Quality Oversight Committee (a subcommittee of the firm's Management Committee), "
        "and is subject to both internal inspection and external peer review. The most recent AICPA "
        "peer review (completed December 2025) resulted in a pass rating with no findings."
    )

    # --- Engagement Lifecycle ---
    pdf.section_heading("2. Engagement Lifecycle")
    pdf.body_text(
        "Every Meridian engagement follows a structured six-phase lifecycle that ensures consistent "
        "quality, clear communication, and measurable outcomes. While the specific activities within "
        "each phase vary by service line, the framework is universal."
    )

    pdf.section_heading("2.1 Phase 1: Opportunity Assessment & Proposal", level=2)
    pdf.body_text(
        "All new engagement opportunities undergo a structured assessment process before a proposal "
        "is issued. This phase ensures that Meridian has the competence, capacity, and independence "
        "to serve the prospective client."
    )
    pdf.bold_bullet("Client Acceptance / Continuance",
        "Every new client and engagement is subject to our Client Acceptance and Continuance (CAC) "
        "process, which evaluates reputational risk, financial stability, management integrity, "
        "independence requirements, and potential conflicts of interest. CAC decisions require approval "
        "from the engagement partner and the regional managing partner. High-risk clients require "
        "additional approval from the National Risk Management partner.")
    pdf.bold_bullet("Independence Assessment",
        "For attest engagements, our Independence Office performs automated and manual checks against "
        "our global independence tracking system, covering financial relationships, business "
        "relationships, employment relationships, and non-attest service provision. The system "
        "monitors over 48,000 entity relationships in real time.")
    pdf.bold_bullet("Proposal Development",
        "Proposals are developed using our structured proposal methodology, which includes service "
        "scope definition, fee estimation (using our engagement economics model), team composition, "
        "timeline development, and risk assessment. All proposals above $250,000 require review by "
        "the service line leader, and proposals above $1 million require Management Committee approval.")

    pdf.add_page()
    pdf.section_heading("2.2 Phase 2: Planning", level=2)
    pdf.bold_bullet("Engagement Planning Memorandum",
        "Each engagement begins with a comprehensive planning memorandum that documents the engagement "
        "objectives, scope, significant risks, materiality determinations (for audit engagements), "
        "team composition, timeline, and communication plan. The planning memorandum is reviewed and "
        "approved by the engagement partner before fieldwork begins.")
    pdf.bold_bullet("Risk Assessment",
        "We perform a multi-dimensional risk assessment covering financial reporting risks (for audit), "
        "project delivery risks (for advisory), regulatory and compliance risks, and operational risks. "
        "Risk assessments are documented using our proprietary risk scoring framework, which assigns "
        "likelihood and impact ratings to each identified risk and maps mitigation strategies.")
    pdf.bold_bullet("Resource Allocation",
        "Team members are assigned based on industry expertise, technical specialization, experience "
        "level, and availability. Our resource management system (Meridian Resource Hub) provides "
        "real-time visibility into professional availability, utilization, and skill profiles across "
        "all 45 offices. Engagement staffing decisions are approved by the engagement partner and the "
        "resource management director.")
    pdf.bold_bullet("Kick-Off Meeting",
        "Every engagement commences with a structured kick-off meeting attended by the full engagement "
        "team and key client stakeholders. The kick-off covers engagement objectives, timeline, roles "
        "and responsibilities, communication protocols, document request lists, and escalation procedures.")

    pdf.section_heading("2.3 Phase 3: Execution", level=2)
    pdf.bold_bullet("Work Program Execution",
        "Fieldwork is performed in accordance with detailed work programs specific to the engagement "
        "type and industry. Work programs are maintained in our engagement management system (Meridian "
        "Workbench) and are updated annually to reflect changes in professional standards, regulatory "
        "requirements, and firm methodology.")
    pdf.bold_bullet("Milestone Tracking",
        "All engagements are tracked against defined milestones using our project management framework. "
        "Milestone status is reported weekly to the engagement partner and shared with the client "
        "through our client portal. Budget-to-actual hour tracking is performed at the task level, "
        "with variance analysis and reforecasting at each milestone checkpoint.")
    pdf.bold_bullet("Issue Management",
        "Issues identified during fieldwork are logged in a centralized issue tracker, categorized "
        "by severity (critical, high, medium, low), assigned to responsible parties, and tracked to "
        "resolution. Critical and high-severity issues require escalation to the engagement partner "
        "within 24 hours. Unresolved issues are reported to the engagement quality reviewer.")

    pdf.add_page()
    pdf.section_heading("2.4 Phase 4: Reporting & Deliverables", level=2)
    pdf.bold_bullet("Deliverable Preparation",
        "All deliverables are prepared using Meridian-approved templates and undergo a structured "
        "multi-level review process (described in Section 4 below). Deliverables include audit "
        "opinions, tax returns and provisions, advisory reports, management letters, and client "
        "presentations.")
    pdf.bold_bullet("Client Review Process",
        "Draft deliverables are shared with client management for factual review before finalization. "
        "Client comments are documented, evaluated, and addressed through a formal response process. "
        "Final deliverables require engagement partner sign-off.")
    pdf.bold_bullet("Regulatory Filings",
        "For engagements involving regulatory filings (SEC, state regulatory bodies, tax authorities), "
        "we maintain filing calendars, pre-submission checklists, and confirmation procedures to "
        "ensure timely and accurate submission.")

    pdf.section_heading("2.5 Phase 5: Follow-Up & Debrief", level=2)
    pdf.bold_bullet("Post-Engagement Debrief",
        "Within 30 days of engagement completion, the engagement team conducts a structured debrief "
        "covering what worked well, what could be improved, and specific action items for future "
        "engagements. Debrief results are documented and entered into our lessons learned database.")
    pdf.bold_bullet("Client Satisfaction Survey",
        "Every engagement above $50,000 includes a formal client satisfaction survey administered "
        "by our independent Client Experience team. Surveys measure satisfaction across eight "
        "dimensions: technical quality, communication, responsiveness, team expertise, value for "
        "fees, partner involvement, innovation, and overall satisfaction.")

    pdf.section_heading("2.6 Phase 6: Continuous Relationship Management", level=2)
    pdf.body_text(
        "Following engagement completion, the relationship partner maintains ongoing contact through "
        "quarterly business reviews, industry update briefings, and invitations to firm-sponsored "
        "events and thought leadership programs. Our CRM system tracks all client interactions and "
        "triggers automated follow-up reminders based on the client's industry calendar (e.g., "
        "budget season, regulatory filing deadlines)."
    )

    # --- Quality Control Framework ---
    pdf.add_page()
    pdf.section_heading("3. Quality Control Framework")
    pdf.body_text(
        "Meridian's quality control framework is designed in alignment with ISQM 1 and encompasses "
        "governance, ethical requirements, acceptance and continuance, engagement performance, resources, "
        "information and communication, and monitoring and remediation."
    )

    pdf.section_heading("3.1 Governance & Leadership", level=2)
    pdf.body_text(
        "Quality is overseen by a dedicated governance structure:"
    )
    pdf.bold_bullet("Quality Oversight Committee",
        "Chaired by the Vice Chair of Quality, comprising 7 partners representing all service lines "
        "and major industry verticals. Meets monthly to review quality metrics, inspection findings, "
        "and remediation progress.")
    pdf.bold_bullet("National Director of Quality & Risk Management",
        "Full-time role responsible for quality policy development, inspection program management, "
        "and regulatory liaison. Reports directly to the Managing Partner.")
    pdf.bold_bullet("Service Line Quality Leaders",
        "Each service line has a dedicated Quality Leader responsible for methodology updates, "
        "training programs, and engagement-level quality monitoring.")

    pdf.section_heading("3.2 Engagement Quality Reviews (EQR)", level=2)
    pdf.body_text(
        "All public company audit engagements and other high-risk engagements undergo an Engagement "
        "Quality Review performed by a qualified reviewer who is independent of the engagement team. "
        "The EQR reviewer evaluates significant judgments, key audit matters, independence compliance, "
        "and the appropriateness of the audit opinion or other deliverable. EQR completion is required "
        "before any audit opinion is issued."
    )
    pdf.body_text("Criteria for mandatory EQR include:")
    pdf.bullet("All SEC registrant audits")
    pdf.bullet("All engagements with fees exceeding $500,000")
    pdf.bullet("All first-year audit engagements")
    pdf.bullet("Engagements involving restatements or material weaknesses")
    pdf.bullet("Engagements identified as high-risk through the CAC process")
    pdf.bullet("All engagements in industries subject to specialized regulatory oversight")

    pdf.section_heading("3.3 Hot Reviews for High-Risk Engagements", level=2)
    pdf.body_text(
        "In addition to standard EQR, certain engagements are designated for 'hot review' - a real-time "
        "concurrent quality review performed during the engagement rather than at completion. Hot reviews "
        "are triggered by specific risk indicators:"
    )
    pdf.bullet("Going concern uncertainties")
    pdf.bullet("Fraud risk indicators or whistleblower allegations")
    pdf.bullet("Complex business combinations or carve-out transactions")
    pdf.bullet("First-time adoption of major accounting standards")
    pdf.bullet("Engagements subject to active regulatory inquiry or investigation")
    pdf.bullet("Significant management estimates with high estimation uncertainty")

    # --- Project Management ---
    pdf.add_page()
    pdf.section_heading("4. Deliverable Review Process")
    pdf.body_text(
        "Every Meridian deliverable undergoes a structured multi-level review process before issuance "
        "to the client. The review process is designed to ensure technical accuracy, compliance with "
        "professional standards, consistency with firm methodology, and clear communication."
    )

    pdf.section_heading("Review Levels", level=2)
    pdf.add_wrapped_table(
        ["Level", "Reviewer", "Focus Areas", "Turnaround"],
        [
            ["Level 1 - Preparation", "Associate / Sr. Associate", "Data accuracy, completeness, calculation verification", "Same day"],
            ["Level 2 - First Review", "Manager / Sr. Manager", "Technical accuracy, methodology compliance, analytical quality", "1-2 business days"],
            ["Level 3 - Director Review", "Director / Managing Director", "Business relevance, client impact, presentation quality", "1-2 business days"],
            ["Level 4 - Partner Review", "Engagement Partner", "Overall quality, significant judgments, client messaging", "2-3 business days"],
            ["Level 5 - EQR (if required)", "EQ Reviewer (independent)", "Independence, significant judgments, opinion appropriateness", "3-5 business days"],
        ],
        col_widths=[40, 42, 78, 30],
    )

    pdf.section_heading("Review Documentation Requirements", level=2)
    pdf.bullet("All review comments are documented in Meridian Workbench with timestamps and reviewer identification")
    pdf.bullet("Preparer must respond to every review comment with either resolution or explanation")
    pdf.bullet("Unresolved review comments are escalated to the next review level")
    pdf.bullet("Partner sign-off on the review completion checklist is required before client delivery")
    pdf.bullet("Review files are retained for a minimum of 7 years (10 years for SEC engagements)")

    # --- PMO Structure ---
    pdf.section_heading("5. Project Management Standards")
    pdf.section_heading("5.1 PMO Structure", level=2)
    pdf.body_text(
        "Meridian operates a centralized Project Management Office (PMO) that provides standardized "
        "project management methodologies, tools, and support to engagement teams across all service "
        "lines. The PMO employs 45 dedicated project management professionals, of whom 32 hold PMP "
        "certifications. PMO services include:"
    )
    pdf.bullet("Project planning and scheduling (using Microsoft Project and Smartsheet)")
    pdf.bullet("Resource forecasting and capacity planning")
    pdf.bullet("Budget development and financial tracking")
    pdf.bullet("Risk and issue management")
    pdf.bullet("Status reporting and dashboard development")
    pdf.bullet("Change management support")

    pdf.add_page()
    pdf.section_heading("5.2 Resource Allocation", level=2)
    pdf.body_text(
        "Resource allocation is managed through Meridian Resource Hub, our proprietary resource "
        "management platform. The system maintains profiles for all 12,400+ professionals, including "
        "skills, certifications, industry experience, language capabilities, security clearances, "
        "and availability. Key features include:"
    )
    pdf.bullet("Real-time utilization tracking with target utilization bands by level (Partner: 50-60%, "
               "Manager: 70-80%, Senior Associate: 80-85%, Associate: 85-90%)")
    pdf.bullet("Skills-based matching algorithm that recommends optimal team compositions")
    pdf.bullet("Conflict of interest screening integrated with the independence tracking system")
    pdf.bullet("Cross-office staffing for specialized skill requirements")
    pdf.bullet("Pipeline forecasting for proactive resource planning")

    pdf.section_heading("5.3 Milestone Tracking & Reporting", level=2)
    pdf.body_text(
        "All engagements above $100,000 are tracked against defined milestone plans. Milestone "
        "reporting includes:"
    )
    pdf.bullet("Weekly status reports to engagement partner (automated from Meridian Workbench)")
    pdf.bullet("Bi-weekly client status updates (customizable frequency per client preference)")
    pdf.bullet("Monthly portfolio reviews at the service line level")
    pdf.bullet("Quarterly executive dashboards for the Management Committee")
    pdf.bullet("Real-time budget variance alerts (triggered at 10% and 20% thresholds)")

    # --- Client Communication ---
    pdf.section_heading("6. Client Communication Protocols")
    pdf.body_text(
        "Effective client communication is foundational to engagement success. Meridian maintains "
        "structured communication protocols that ensure clients are informed, engaged, and aligned "
        "throughout the engagement lifecycle."
    )

    pdf.add_table(
        ["Communication Type", "Frequency", "Participants", "Format"],
        [
            ["Kick-Off Meeting", "Once (start)", "Full team + client", "In-person / virtual"],
            ["Weekly Status Update", "Weekly", "Manager + client lead", "Email / portal"],
            ["Steering Committee", "Bi-weekly / Monthly", "Partner + C-suite", "In-person / virtual"],
            ["Issue Escalation", "As needed (<24 hrs)", "Partner + client exec", "Phone / in-person"],
            ["Milestone Review", "Per plan", "Sr. team + client team", "In-person presentation"],
            ["Draft Deliverable Review", "Per plan", "Full team + client", "Document + meeting"],
            ["Final Presentation", "Once (end)", "Partner + C-suite", "In-person presentation"],
            ["Post-Engagement Debrief", "Once (30 days post)", "Partner + client exec", "In-person / virtual"],
        ],
        col_widths=[45, 38, 45, 45],
    )

    # --- Technology-Enabled QA ---
    pdf.add_page()
    pdf.section_heading("7. Technology-Enabled Quality Assurance")
    pdf.body_text(
        "Meridian leverages technology extensively to enhance the consistency, efficiency, and "
        "effectiveness of our quality assurance processes."
    )

    pdf.section_heading("7.1 Automated Workpaper Review", level=2)
    pdf.body_text(
        "Our Meridian Workbench platform includes automated quality checks that are performed in "
        "real time as engagement teams prepare workpapers. These checks include:"
    )
    pdf.bullet("Cross-reference validation - ensures all referenced documents exist and are current")
    pdf.bullet("Completeness checks - identifies missing required sections in standard work programs")
    pdf.bullet("Tickmark verification - confirms all items requiring explanation have been documented")
    pdf.bullet("Date consistency - flags date references that are inconsistent with the reporting period")
    pdf.bullet("Materiality threshold compliance - alerts when items exceed defined materiality thresholds")
    pdf.bullet("Template compliance - verifies adherence to current firm templates and formatting standards")

    pdf.section_heading("7.2 AI-Assisted Anomaly Detection", level=2)
    pdf.body_text(
        "MeridianAI's anomaly detection engine is integrated into our audit methodology and provides "
        "the following quality assurance capabilities:"
    )
    pdf.bullet("Journal entry anomaly scoring - machine learning model trained on 8 years of historical "
               "data, identifying entries with characteristics associated with error or fraud")
    pdf.bullet("Trend analysis and outlier detection - automated comparison of client financial data "
               "against industry benchmarks and historical patterns")
    pdf.bullet("Text analytics for contract review - NLP models that identify unusual or non-standard "
               "contract terms requiring additional audit attention")
    pdf.bullet("Predictive risk scoring - real-time risk assessment that updates throughout the "
               "engagement based on accumulated audit evidence")
    pdf.bullet("Automated sampling optimization - risk-based sample selection that maximizes coverage "
               "of high-risk items while maintaining statistical validity")

    pdf.section_heading("7.3 Continuous Monitoring", level=2)
    pdf.body_text(
        "For managed services and ongoing advisory engagements, we deploy continuous monitoring "
        "solutions that provide real-time quality oversight:"
    )
    pdf.bullet("Automated exception reporting for key controls")
    pdf.bullet("Real-time reconciliation monitoring with configurable tolerance thresholds")
    pdf.bullet("Regulatory change tracking and impact assessment")
    pdf.bullet("Dashboard-based oversight with drill-down capability")

    # --- Continuous Improvement ---
    pdf.add_page()
    pdf.section_heading("8. Continuous Improvement Program")

    pdf.section_heading("8.1 Internal Inspection Program", level=2)
    pdf.body_text(
        "Meridian conducts an annual internal inspection program that reviews a risk-weighted sample "
        "of completed engagements across all service lines. The inspection program is designed and "
        "overseen by the National Director of Quality & Risk Management and is staffed by experienced "
        "professionals who are independent of the engagements under review. In the most recent "
        "inspection cycle (2025), 142 engagements were reviewed, representing approximately 12% of "
        "total engagement hours."
    )

    pdf.section_heading("8.2 Lessons Learned Database", level=2)
    pdf.body_text(
        "Post-engagement debrief findings, inspection findings, and client feedback are compiled in "
        "our centralized Lessons Learned Database, which is searchable by industry, service line, "
        "engagement type, and topic. The database contains over 4,800 entries accumulated since 2015 "
        "and is actively referenced during engagement planning to proactively address known risk areas. "
        "The Quality Oversight Committee reviews aggregate lessons learned trends quarterly and "
        "incorporates systemic findings into methodology updates and training programs."
    )

    pdf.section_heading("8.3 Root Cause Analysis", level=2)
    pdf.body_text(
        "Any quality finding rated 'significant' or above triggers a formal root cause analysis (RCA) "
        "performed by the Quality team. RCA follows a structured methodology:"
    )
    pdf.bullet("Problem statement definition and impact assessment")
    pdf.bullet("Data collection (workpaper review, team interviews, process mapping)")
    pdf.bullet("Causal factor identification using fishbone (Ishikawa) analysis")
    pdf.bullet("Root cause determination and validation")
    pdf.bullet("Corrective action development with ownership and timelines")
    pdf.bullet("Effectiveness verification at 90-day and 180-day intervals")
    pdf.body_text(
        "In 2025, 23 formal RCAs were conducted. The most common root causes identified were "
        "insufficient specialist consultation (31%), inadequate engagement planning (26%), and "
        "staff workload/capacity issues (22%). Each finding resulted in specific remediation actions "
        "tracked to completion by the Quality Oversight Committee."
    )

    # --- Metrics & KPIs ---
    pdf.section_heading("9. Quality Metrics & KPIs")
    pdf.body_text(
        "Meridian tracks a comprehensive set of quality metrics and key performance indicators at "
        "the firm, service line, office, and individual engagement levels. These metrics are reported "
        "monthly to firm leadership and are incorporated into partner compensation decisions."
    )

    pdf.add_table(
        ["KPI", "Target", "FY 2025 Actual", "Status"],
        [
            ["Client Satisfaction Score", ">= 4.5 / 5.0", "4.6 / 5.0", "Achieved"],
            ["Engagement Realization Rate", ">= 92%", "94.1%", "Achieved"],
            ["Inspection Pass Rate", ">= 95%", "96.5%", "Achieved"],
            ["EQR Completion (on time)", "100%", "99.7%", "Near-target"],
            ["Staff Utilization (Sr. Assoc)", "80-85%", "82.3%", "Achieved"],
            ["Training Hours per Professional", ">= 40 hrs/yr", "47 hrs/yr", "Achieved"],
            ["Restatement Rate (audit clients)", "< 1%", "0.3%", "Achieved"],
            ["Client Retention Rate", ">= 92%", "94%", "Achieved"],
            ["Employee Satisfaction (quality)", ">= 4.0 / 5.0", "4.2 / 5.0", "Achieved"],
            ["Lessons Learned Entries", ">= 400/yr", "512", "Achieved"],
        ],
        col_widths=[55, 35, 40, 30],
    )

    advisory_dir = os.path.join(os.path.dirname(OUTPUT_DIR), "advisory_consulting")
    path = os.path.join(advisory_dir, "qa_delivery_methodology.pdf")
    pdf.output(path)
    print(f"  Generated: {path}")


# =============================================================================
# 5. RATE CARDS EXPANDED
# =============================================================================

def generate_rate_cards_expanded():
    pdf = MeridianPDF(
        "Rate Cards & Fee Structures",
        "Standard Rates, Industry Adjustments, Specialist Premiums,\nVolume Discounts, and Alternative Fee Arrangements",
        confidential=True,
    )
    pdf.cover_page(version="6.1", date="February 2026")

    # --- Standard Rates ---
    pdf.add_page()
    pdf.section_heading("1. Standard Hourly Rates by Professional Level")
    pdf.body_text(
        "The following standard hourly rates are effective as of January 1, 2026 and apply to all "
        "service lines unless otherwise specified. Rates reflect national averages; specific engagement "
        "rates may vary based on geographic location, industry, complexity, and volume commitments. "
        "All rates are quoted in US dollars and are subject to annual adjustment, typically effective "
        "January 1 of each calendar year."
    )

    pdf.add_table(
        ["Professional Level", "Rate Range", "Typical Rate", "Years Exp."],
        [
            ["Partner / Principal", "$650 - $850/hr", "$750/hr", "20+"],
            ["Managing Director", "$550 - $700/hr", "$625/hr", "15-20"],
            ["Senior Manager / Director", "$425 - $550/hr", "$488/hr", "10-15"],
            ["Manager", "$350 - $450/hr", "$400/hr", "7-10"],
            ["Senior Associate / Senior Consultant", "$250 - $350/hr", "$300/hr", "4-7"],
            ["Associate / Consultant", "$175 - $275/hr", "$225/hr", "2-4"],
            ["Intern / Staff", "$125 - $175/hr", "$150/hr", "0-2"],
        ],
        col_widths=[55, 45, 40, 30],
    )

    pdf.body_text(
        "Notes on rate determination: The specific rate for each professional within the above ranges "
        "is determined by the individual's experience, industry specialization, relevant certifications, "
        "and the nature of the engagement. Partners and Managing Directors typically bill at the higher "
        "end of their range for specialized advisory engagements and at the lower end for recurring "
        "compliance work. Intern/Staff rates apply to professionals in their first two years post-graduation."
    )

    pdf.section_heading("Rate Inclusions", level=2)
    pdf.bullet("All professional time (analysis, meetings, deliverable preparation, review time)")
    pdf.bullet("Standard technology tools (Meridian Workbench, MeridianAI, standard analytics)")
    pdf.bullet("Project management and coordination")
    pdf.bullet("Standard quality assurance reviews")
    pdf.bullet("Engagement administration")
    pdf.ln(2)
    pdf.section_heading("Rate Exclusions", level=2)
    pdf.bullet("Travel and out-of-pocket expenses (billed separately per Section 7)")
    pdf.bullet("Specialist tools or third-party software licenses required for the engagement")
    pdf.bullet("Rush or expedited delivery premiums (see Section 6)")
    pdf.bullet("Expert witness testimony and deposition preparation (billed at 1.5x standard rate)")

    # --- Industry Adjustments ---
    pdf.add_page()
    pdf.section_heading("2. Industry-Specific Rate Adjustments")
    pdf.body_text(
        "Certain industries require specialized knowledge, additional regulatory expertise, or enhanced "
        "quality procedures that are reflected in industry-specific rate adjustments. These adjustments "
        "are applied as a percentage modification to the standard hourly rates and are intended to "
        "reflect the incremental investment in industry specialization, continuing education, and "
        "regulatory compliance required to serve these sectors."
    )

    pdf.add_table(
        ["Industry", "Adjustment", "Rationale"],
        [
            ["Financial Services", "+15%", "Basel/Dodd-Frank expertise, CECL, LDTI, enhanced regulatory risk"],
            ["Healthcare & Life Sciences", "+10%", "HIPAA compliance, clinical operations knowledge, FDA regulations"],
            ["Energy & Natural Resources", "+5%", "Reservoir engineering, commodity accounting, ARO estimation"],
            ["Technology & Media", "+5%", "ASC 606 software/SaaS complexity, stock comp, rapid pace of change"],
            ["Manufacturing & Distribution", "Standard (0%)", "Baseline complexity, well-established standards"],
            ["Retail & Consumer", "Standard (0%)", "Baseline complexity, established retail accounting frameworks"],
            ["Public Sector & Not-for-Profit", "-5%", "Community investment commitment, lower-margin engagement model"],
        ],
        col_widths=[55, 28, 100],
    )

    pdf.body_text(
        "Industry adjustments are applied at the engagement level and are reflected in the engagement "
        "letter. For multi-industry engagements (e.g., a conglomerate with divisions in different "
        "sectors), the adjustment is determined by the primary industry of the reporting entity."
    )

    # --- Specialist Premiums ---
    pdf.section_heading("3. Specialist Premiums")
    pdf.body_text(
        "Engagements requiring scarce or highly specialized expertise may be subject to specialist "
        "premiums, which reflect the limited supply and high demand for professionals with these "
        "specific qualifications. Specialist premiums are applied to the individual specialist's "
        "hourly rate, not to the entire engagement team."
    )

    pdf.add_table(
        ["Specialization", "Premium", "Applicable Roles", "Typical Engagements"],
        [
            ["Forensic Accounting", "+30%", "All levels", "Fraud investigations, litigation support, dispute resolution"],
            ["Cybersecurity", "+25%", "Manager and above", "Penetration testing, incident response, CISO advisory"],
            ["Transfer Pricing", "+20%", "Sr. Manager and above", "TP documentation, APA negotiations, BEPS compliance"],
            ["Data Analytics / AI", "+15%", "All levels", "ML model development, advanced analytics, AI implementation"],
            ["Actuarial Services", "+20%", "All levels", "Insurance reserves, pension valuation, predictive modeling"],
            ["Valuation Services", "+15%", "Manager and above", "Business valuation, purchase price allocation, fairness opinions"],
            ["ESG / Sustainability", "+10%", "Sr. Manager and above", "ESG reporting, CSRD compliance, assurance"],
        ],
        col_widths=[38, 22, 40, 80],
    )

    pdf.body_text(
        "Specialist premiums are cumulative with industry adjustments. For example, a cybersecurity "
        "Senior Manager working on a financial services engagement would be billed at the standard "
        "Senior Manager rate + 15% industry adjustment + 25% specialist premium."
    )

    # --- Volume Discounts ---
    pdf.add_page()
    pdf.section_heading("4. Volume Discount Tiers")
    pdf.body_text(
        "Meridian offers volume-based discounts to clients with significant annual engagement spend. "
        "Discounts are calculated on aggregate annual fees across all service lines and are applied "
        "retroactively at the end of the fee measurement period (typically the client's fiscal year)."
    )

    pdf.add_table(
        ["Tier", "Annual Fee Threshold", "Discount", "Application Method"],
        [
            ["Tier 1", "$250K - $499K", "3%", "Applied to all fees above threshold"],
            ["Tier 2", "$500K - $999K", "5%", "Applied to all fees above threshold"],
            ["Tier 3", "$1.0M - $1.99M", "8%", "Applied to all fees above threshold"],
            ["Tier 4", "$2.0M - $4.99M", "12%", "Applied to all fees above threshold"],
            ["Tier 5", "$5.0M+", "15% (negotiable)", "Custom arrangement"],
        ],
        col_widths=[25, 45, 30, 75],
    )

    pdf.body_text(
        "Volume discounts apply to professional fees only and do not include travel expenses, "
        "third-party costs, or specialist tool licensing. Discounts are non-cumulative (i.e., the "
        "highest applicable tier rate applies to all eligible fees). Multi-year commitments may "
        "qualify for enhanced discount terms - please discuss with your engagement partner."
    )

    pdf.section_heading("Volume Discount Illustration", level=2)
    pdf.body_text(
        "Example: A client with $1.5 million in annual professional fees qualifies for Tier 3 (8% "
        "discount). The annual discount would be $120,000, reducing the effective annual fee to "
        "$1,380,000. If the client commits to a three-year engagement term, an additional 2% loyalty "
        "discount may be available, bringing the effective discount to 10% ($150,000 annual savings)."
    )

    # --- Sample Engagement Cost Models ---
    pdf.section_heading("5. Sample Engagement Cost Models")
    pdf.body_text(
        "The following cost estimates are provided for illustrative purposes based on typical engagement "
        "scopes for mid-market companies ($500M - $5B revenue). Actual fees will vary based on "
        "engagement complexity, company size, industry, geographic distribution, and specific scope "
        "requirements. All estimates assume standard rate structures before volume discounts."
    )

    pdf.add_page()
    pdf.section_heading("5.1 Mid-Market Integrated Audit", level=2)
    pdf.add_table(
        ["Component", "Hours (Est.)", "Fee Range"],
        [
            ["Engagement Planning & Risk Assessment", "400 - 600", "$80K - $130K"],
            ["Internal Controls Testing (SOX 404)", "800 - 1,200", "$160K - $260K"],
            ["Substantive Audit Procedures", "600 - 1,000", "$120K - $220K"],
            ["Review, Reporting & Wrap-up", "200 - 300", "$50K - $75K"],
            ["TOTAL INTEGRATED AUDIT", "2,000 - 3,100", "$350K - $600K"],
        ],
        col_widths=[75, 40, 55],
    )
    pdf.body_text(
        "Assumptions: SEC registrant with 3-5 significant locations, 10-15 significant accounts, "
        "no significant unusual transactions. First-year engagements typically fall at the higher "
        "end of the range due to transition and learning-curve costs."
    )

    pdf.section_heading("5.2 SOX 404 Implementation (New)", level=2)
    pdf.add_table(
        ["Component", "Hours (Est.)", "Fee Range"],
        [
            ["Scoping & Risk Assessment", "300 - 500", "$65K - $110K"],
            ["Control Documentation & Walkthroughs", "500 - 800", "$100K - $175K"],
            ["Remediation Support", "200 - 400", "$45K - $90K"],
            ["Testing & Evaluation", "150 - 300", "$35K - $70K"],
            ["TOTAL SOX IMPLEMENTATION", "1,150 - 2,000", "$200K - $400K"],
        ],
        col_widths=[75, 40, 55],
    )

    pdf.section_heading("5.3 Tax Provision Automation", level=2)
    pdf.add_table(
        ["Component", "Hours (Est.)", "Fee Range"],
        [
            ["Current State Assessment", "150 - 250", "$35K - $60K"],
            ["System Selection & Configuration", "300 - 500", "$65K - $115K"],
            ["Data Migration & Integration", "200 - 350", "$45K - $80K"],
            ["Testing, Training & Go-Live", "100 - 200", "$25K - $50K"],
            ["TOTAL TAX AUTOMATION", "750 - 1,300", "$150K - $300K"],
        ],
        col_widths=[75, 40, 55],
    )

    pdf.add_page()
    pdf.section_heading("5.4 ERP Advisory (Implementation Support)", level=2)
    pdf.add_table(
        ["Component", "Hours (Est.)", "Fee Range"],
        [
            ["Strategy & Vendor Selection", "500 - 800", "$115K - $190K"],
            ["Design & Configuration Oversight", "1,000 - 2,000", "$220K - $475K"],
            ["Data Migration & Testing Advisory", "400 - 800", "$90K - $190K"],
            ["Change Management & Training", "300 - 600", "$65K - $140K"],
            ["Post-Go-Live Stabilization", "200 - 400", "$45K - $95K"],
            ["TOTAL ERP ADVISORY", "2,400 - 4,600", "$500K - $1.5M"],
        ],
        col_widths=[75, 40, 55],
    )
    pdf.body_text(
        "Note: ERP advisory fees reflect Meridian's role as an independent advisor to the client, "
        "not as the system integrator. Fees for system integration are provided by the SI partner "
        "and are not included in these estimates."
    )

    pdf.section_heading("5.5 Additional Common Engagements", level=2)
    pdf.add_table(
        ["Engagement Type", "Typical Duration", "Fee Range"],
        [
            ["Financial Due Diligence (M&A)", "4 - 8 weeks", "$150K - $500K"],
            ["Internal Audit Co-Source (annual)", "Ongoing", "$200K - $600K"],
            ["Cybersecurity Assessment", "6 - 10 weeks", "$125K - $350K"],
            ["ASC 606 Revenue Implementation", "12 - 24 weeks", "$175K - $450K"],
            ["Transfer Pricing Study", "8 - 16 weeks", "$100K - $300K"],
            ["R&D Tax Credit Study", "6 - 12 weeks", "$75K - $200K"],
            ["Forensic Investigation", "Variable", "$200K - $1M+"],
            ["ESG Readiness Assessment", "8 - 12 weeks", "$100K - $250K"],
            ["Business Valuation", "4 - 8 weeks", "$50K - $200K"],
        ],
        col_widths=[60, 45, 55],
    )

    # --- Rush / Expedited ---
    pdf.add_page()
    pdf.section_heading("6. Expedited Delivery and Rush Premiums")
    pdf.body_text(
        "For engagements requiring accelerated timelines, the following premiums apply to professional "
        "fees for the expedited components of the engagement:"
    )
    pdf.add_table(
        ["Timeline Compression", "Premium", "Example"],
        [
            ["10-25% faster than standard", "+10%", "8-week engagement delivered in 6 weeks"],
            ["26-50% faster than standard", "+25%", "12-week engagement delivered in 7 weeks"],
            [">50% faster than standard", "+40% (negotiable)", "Custom - requires partner approval"],
        ],
        col_widths=[55, 30, 95],
    )
    pdf.body_text(
        "Rush premiums are discussed and agreed upon before engagement commencement and are documented "
        "in the engagement letter. They apply only to the portions of work subject to acceleration "
        "and do not apply to travel expenses or third-party costs."
    )

    # --- Travel & Expense ---
    pdf.section_heading("7. Travel & Expense Policy")
    pdf.body_text(
        "Travel and out-of-pocket expenses are billed separately from professional fees at actual "
        "cost without markup, subject to the following guidelines:"
    )
    pdf.section_heading("Air Travel", level=2)
    pdf.bullet("Flights under 3 hours: Economy class")
    pdf.bullet("Flights 3-6 hours: Premium economy or economy (client preference)")
    pdf.bullet("Flights over 6 hours: Business class")
    pdf.bullet("All flights booked at least 14 days in advance when possible to minimize cost")

    pdf.section_heading("Lodging", level=2)
    pdf.bullet("Standard: Up to $275/night in major metropolitan areas, $200/night in other markets")
    pdf.bullet("Extended stay (>4 consecutive weeks): Serviced apartment arrangements at reduced rates")
    pdf.bullet("Preferred hotel programs utilized to maximize client value")

    pdf.section_heading("Ground Transportation", level=2)
    pdf.bullet("Standard rental cars or ride-share services for local travel")
    pdf.bullet("Mileage for personal vehicle use: IRS standard rate ($0.70/mile for 2026)")

    pdf.section_heading("Meals", level=2)
    pdf.bullet("Per diem: $75/day (actual cost or per diem, whichever is lower)")
    pdf.bullet("Client entertainment: Pre-approved by engagement partner, billed at actual cost")

    pdf.section_heading("Expense Cap", level=2)
    pdf.body_text(
        "For ongoing engagements, Meridian will provide monthly expense estimates and will not exceed "
        "the agreed annual travel budget by more than 10% without prior client approval. Virtual/remote "
        "delivery is utilized where possible to minimize travel costs."
    )

    # --- Alternative Fee Arrangements ---
    pdf.add_page()
    pdf.section_heading("8. Alternative Fee Arrangements")
    pdf.body_text(
        "Meridian recognizes that traditional hourly billing does not always align with client "
        "objectives or the value delivered. We offer several alternative fee arrangements designed "
        "to provide cost predictability, align incentives, and reflect the value of our services "
        "rather than simply the time expended."
    )

    pdf.section_heading("8.1 Fixed Fee", level=2)
    pdf.body_text(
        "A predetermined total fee for a defined scope of work, payable in agreed installments "
        "(typically monthly or milestone-based). Fixed fees provide maximum cost certainty and are "
        "most appropriate for well-defined, recurring engagements."
    )
    pdf.bold_bullet("Best Suited For", "Annual audits (after Year 1), tax compliance, SOC reports, "
                    "recurring advisory services")
    pdf.bold_bullet("Scope Change Protocol", "Changes to the agreed scope are documented through a "
                    "formal change order process and priced separately")
    pdf.bold_bullet("Typical Discount vs. Hourly", "3-5% discount to hourly estimate (reflects "
                    "efficiency gains and reduced administrative overhead)")

    pdf.section_heading("8.2 Capped Fee", level=2)
    pdf.body_text(
        "Hourly billing with a contractual maximum (cap) that will not be exceeded regardless of "
        "actual hours incurred. Capped fees provide upside protection for the client while preserving "
        "hourly transparency."
    )
    pdf.bold_bullet("Best Suited For", "First-year audits, complex advisory engagements with "
                    "uncertain scope, M&A due diligence")
    pdf.bold_bullet("Cap Determination", "Typically set at 110-120% of the base fee estimate")
    pdf.bold_bullet("Risk Sharing", "Meridian absorbs overruns above the cap; savings below the "
                    "estimate may be shared 50/50 with the client")

    pdf.section_heading("8.3 Success Fee", level=2)
    pdf.body_text(
        "A fee structure that ties a portion of compensation to achievement of defined outcomes or "
        "results. Success fees combine a reduced base fee with a contingent component linked to "
        "measurable success criteria."
    )
    pdf.bold_bullet("Best Suited For", "R&D tax credit studies, cost reduction initiatives, "
                    "process improvement projects with quantifiable savings")
    pdf.bold_bullet("Structure", "Reduced base fee (typically 50-70% of standard estimate) plus "
                    "success component (typically 15-25% of identified savings/credits)")
    pdf.bold_bullet("Independence Restrictions", "Not available for attest engagements due to "
                    "independence requirements")

    pdf.section_heading("8.4 Retainer / Subscription", level=2)
    pdf.body_text(
        "A fixed monthly or quarterly fee providing access to a defined level of professional "
        "services, similar to a subscription model. Retainers provide predictable costs and "
        "guaranteed resource availability."
    )
    pdf.bold_bullet("Best Suited For", "Ongoing advisory relationships, internal audit co-source, "
                    "regulatory change monitoring, technical accounting hotline")
    pdf.bold_bullet("Structure", "Monthly retainer covering a specified number of hours (e.g., "
                    "40 hours/month at blended rate). Unused hours may roll forward up to one quarter. "
                    "Hours above the retainer are billed at a discounted hourly rate (typically 10% below standard)")
    pdf.bold_bullet("Minimum Term", "Typically 12 months with quarterly renewal option")

    # --- Terms ---
    pdf.add_page()
    pdf.section_heading("9. Payment Terms & Conditions")
    pdf.section_heading("9.1 Standard Payment Terms", level=2)
    pdf.bullet("Invoicing: Monthly, in arrears, by the 10th business day of the following month")
    pdf.bullet("Payment due: Net 30 days from invoice date")
    pdf.bullet("Late payment: 1.5% per month on balances over 30 days past due")
    pdf.bullet("Currency: US dollars (USD), unless otherwise agreed")
    pdf.bullet("Electronic payment preferred (ACH, wire transfer)")

    pdf.section_heading("9.2 Engagement Letter Requirements", level=2)
    pdf.body_text(
        "All fee arrangements, including rates, discounts, premiums, expense policies, and payment "
        "terms, are documented in a signed engagement letter before work commences. The engagement "
        "letter also specifies scope, timeline, team composition, deliverables, confidentiality "
        "obligations, limitation of liability, and dispute resolution procedures."
    )

    pdf.section_heading("9.3 Rate Escalation", level=2)
    pdf.body_text(
        "Standard rates are subject to annual adjustment, typically effective January 1 of each year. "
        "Rate increases are communicated to clients at least 60 days in advance. Historical rate "
        "increases have averaged 3-4% annually, consistent with market trends. Multi-year engagement "
        "agreements may include rate escalation caps (typically CPI + 1-2%) to provide cost predictability."
    )

    pdf.section_heading("10. Contact for Custom Pricing")
    pdf.body_text(
        "The rate cards and fee structures presented in this document represent standard frameworks. "
        "Meridian is committed to developing pricing arrangements that align with each client's unique "
        "needs, budget, and engagement requirements. For custom pricing discussions, please contact:"
    )
    pdf.ln(2)
    pdf.key_value("National Pricing Director", "Jonathan Mercer")
    pdf.key_value("Email", "j.mercer@meridian-llp.com")
    pdf.key_value("Phone", "+1 (212) 555-0198")
    pdf.ln(2)
    pdf.body_text(
        "Alternatively, your engagement partner or relationship manager can facilitate pricing "
        "discussions and connect you with the appropriate specialist for your specific needs."
    )

    path = os.path.join(OUTPUT_DIR, "rate_cards_expanded.pdf")
    pdf.output(path)
    print(f"  Generated: {path}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Generating Meridian & Associates LLP knowledge base documents...\n")
    generate_case_study_energy()
    generate_case_study_retail()
    generate_firm_capabilities()
    generate_qa_methodology()
    generate_rate_cards_expanded()
    print("\nAll 5 documents generated successfully.")
