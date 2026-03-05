#!/usr/bin/env python3
"""
Generate 7 synthetic professional-services PDF documents for
Meridian & Associates LLP -- Tax Services practice.

Uses fpdf2 built-in fonts only (Helvetica, Times, Courier).
"""

from fpdf import FPDF
import os
from datetime import date

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Reusable PDF helper
# ---------------------------------------------------------------------------

class FirmPDF(FPDF):
    """Custom FPDF subclass with Meridian & Associates branding."""

    def __init__(self, title: str, subtitle: str, doc_id: str, version: str, effective_date: str):
        super().__init__()
        self.doc_title = title
        self.doc_subtitle = subtitle
        self.doc_id = doc_id
        self.doc_version = version
        self.doc_effective_date = effective_date
        self.set_auto_page_break(auto=True, margin=25)

    # -- header on every page --
    def header(self):
        if self.page_no() == 1:
            return  # cover page handled separately
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "MERIDIAN & ASSOCIATES LLP  |  CONFIDENTIAL", align="L")
        self.cell(0, 5, self.doc_title, align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    # -- footer on every page --
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(130, 130, 130)
        self.cell(0, 5, f"{self.doc_id}  |  Version {self.doc_version}  |  Page {self.page_no()}/{{nb}}", align="C")

    # -- cover page --
    def cover_page(self):
        self.add_page()
        self.ln(30)
        # Firm name
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(0, 51, 102)
        self.cell(0, 14, "Meridian & Associates LLP", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        # Divider line
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.8)
        self.line(40, self.get_y(), 170, self.get_y())
        self.ln(8)
        # Practice line
        self.set_font("Helvetica", "", 14)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, "Tax Services Practice", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)
        # Document title
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(0, 51, 102)
        self.multi_cell(0, 11, self.doc_title, align="C")
        self.ln(4)
        # Subtitle
        self.set_font("Helvetica", "", 13)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 7, self.doc_subtitle, align="C")
        self.ln(20)
        # Metadata box
        self.set_fill_color(240, 243, 248)
        self.set_draw_color(0, 51, 102)
        x = 50
        w = 110
        y_start = self.get_y()
        self.set_x(x)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 51, 102)
        meta = [
            ("Document ID:", self.doc_id),
            ("Version:", self.doc_version),
            ("Effective Date:", self.doc_effective_date),
            ("Classification:", "CONFIDENTIAL"),
            ("Distribution:", "Internal Use Only"),
        ]
        box_h = len(meta) * 7 + 6
        self.rect(x, y_start, w, box_h, style="DF")
        self.ln(3)
        for label, value in meta:
            self.set_x(x + 4)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(0, 51, 102)
            self.cell(32, 7, label)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(50, 50, 50)
            self.cell(0, 7, value, new_x="LMARGIN", new_y="NEXT")
        self.ln(10)
        # Confidentiality notice
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(130, 130, 130)
        self.multi_cell(0, 4,
            "This document is the proprietary and confidential property of Meridian & Associates LLP. "
            "It is intended solely for internal use by authorized personnel of the firm. Unauthorized "
            "reproduction, distribution, or disclosure is strictly prohibited. If you have received this "
            "document in error, please notify the Tax Services Practice Leader immediately.",
            align="C")

    # -- convenience methods for content --
    def section_heading(self, number: str, title: str):
        self.ln(3)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 9, f"{number}  {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 120, self.get_y())
        self.ln(3)

    def subsection_heading(self, number: str, title: str):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.cell(0, 7, f"{number}  {title}", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text: str):
        self.set_font("Times", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet_list(self, items: list[str]):
        self.set_font("Times", "", 10)
        self.set_text_color(30, 30, 30)
        for item in items:
            x = self.get_x()
            self.cell(6, 5, "-")  # bullet character
            self.multi_cell(0, 5, item)
            self.set_x(x)
        self.ln(2)

    def indented_bullet_list(self, items: list[str], indent: float = 12):
        self.set_font("Times", "", 10)
        self.set_text_color(30, 30, 30)
        for item in items:
            self.set_x(self.l_margin + indent)
            self.cell(5, 5, "-")
            self.multi_cell(0, 5, item)
        self.ln(1)

    def key_value_block(self, pairs: list[tuple[str, str]]):
        for key, val in pairs:
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(0, 51, 102)
            self.cell(0, 5, f"{key}  ", new_x="LMARGIN", new_y="NEXT")
            self.set_x(self.l_margin + 6)
            self.set_font("Times", "", 10)
            self.set_text_color(30, 30, 30)
            self.multi_cell(0, 5, val)
            self.ln(1)
        self.ln(1)

    def note_box(self, text: str):
        self.set_fill_color(255, 248, 220)
        self.set_draw_color(200, 170, 80)
        y = self.get_y()
        self.rect(12, y, 186, 14, style="DF")
        self.set_xy(14, y + 2)
        self.set_font("Helvetica", "BI", 9)
        self.set_text_color(120, 80, 0)
        self.multi_cell(182, 5, f"Note: {text}")
        self.ln(4)

    def save(self, filename: str):
        path = os.path.join(OUTPUT_DIR, filename)
        self.alias_nb_pages()
        self.output(path)
        print(f"  -> {path}")


# ===================================================================
# DOCUMENT 1: Global Tax Compliance
# ===================================================================

def build_global_tax_compliance():
    pdf = FirmPDF(
        title="Global Tax Compliance Program",
        subtitle="Managing Corporate Tax Returns Across 80+ Jurisdictions\nMethodology, Quality Controls & Technology Platform",
        doc_id="M&A-TAX-GTC-001",
        version="4.2",
        effective_date="January 1, 2026",
    )
    pdf.cover_page()

    # --- Section 1 ---
    pdf.add_page()
    pdf.section_heading("1.", "Executive Summary")
    pdf.body_text(
        "Meridian & Associates LLP's Global Tax Compliance (GTC) program provides a centralized, "
        "technology-enabled framework for managing corporate income tax return filings across more than "
        "80 jurisdictions worldwide. This program serves as the operational backbone of our international "
        "tax compliance practice, supporting over 1,400 multinational clients with aggregate annual "
        "filings exceeding 22,000 returns. Through rigorous quality controls, standardized processes, "
        "and an integrated technology platform, the GTC program has consistently maintained an amendment "
        "rate below 0.5% -- substantially below the industry average of 1.8%."
    )
    pdf.body_text(
        "The program is designed to address the growing complexity of cross-border tax compliance, "
        "including the implementation of the OECD's Pillar Two Global Anti-Base Erosion (GloBE) rules "
        "establishing a 15% global minimum effective tax rate, expanded Country-by-Country Reporting "
        "(CbCR) requirements under BEPS Action 13, and the proliferation of real-time digital tax "
        "administration mandates across EMEA, APAC, and Latin American jurisdictions."
    )

    # --- Section 2 ---
    pdf.section_heading("2.", "Global Compliance Calendar")
    pdf.body_text(
        "Our standardized global compliance calendar is the cornerstone of the GTC program. The calendar "
        "is maintained in Thomson Reuters ONESOURCE Compliance and is organized into three tiers based on "
        "filing materiality and complexity:"
    )
    pdf.subsection_heading("2.1", "Tier 1 -- Major Jurisdictions (Top 20 by Revenue)")
    pdf.body_text(
        "Tier 1 jurisdictions represent approximately 85% of aggregate taxable income for our typical "
        "multinational client. These include the United States (federal and all material state filings), "
        "United Kingdom, Germany, France, Japan, China (PRC), Canada, Australia, India, Brazil, Mexico, "
        "Singapore, South Korea, the Netherlands, Switzerland, Italy, Spain, Sweden, Ireland, and the UAE. "
        "Each Tier 1 jurisdiction follows a detailed sub-calendar with the following milestones:"
    )
    pdf.bullet_list([
        "T-120 days: Data collection kick-off -- engagement teams issue standardized data request lists to client controllers.",
        "T-90 days: Trial balance and permanent difference analysis -- statutory-to-GAAP reconciliation initiated.",
        "T-60 days: Draft return preparation -- ONESOURCE population and initial computational review.",
        "T-45 days: First-level technical review by senior manager or director.",
        "T-30 days: Signing partner review and approval, including cross-border consistency check.",
        "T-14 days: Client review package distributed -- includes summary of positions, effective tax rate analysis, and filing instructions.",
        "T-7 days: Final quality control checkpoint -- automated diagnostic review and peer comparison.",
        "T-0: Authorized electronic filing or dispatch to local counsel for manual submission.",
    ])

    pdf.subsection_heading("2.2", "Tier 2 -- Secondary Jurisdictions (21-50)")
    pdf.body_text(
        "Tier 2 jurisdictions follow a streamlined calendar with four key milestones: data request, "
        "draft preparation, technical review, and filing. These returns are typically prepared by our "
        "Global Delivery Center (GDC) teams in Hyderabad and Krakow (see common_firm_wide/"
        "global_delivery_network.pdf for GDC operations, capacity, and service-level commitments), "
        "with oversight from in-country Meridian offices. Tier 2 includes jurisdictions such as "
        "Poland, Czech Republic, Thailand, Vietnam, Colombia, Chile, South Africa, Israel, Norway, "
        "and Denmark."
    )

    pdf.subsection_heading("2.3", "Tier 3 -- Ancillary Jurisdictions (51-80+)")
    pdf.body_text(
        "Tier 3 filings are managed through our Correspondent Firm Network (CFN), a curated network of "
        "50+ local tax practices that operate under Meridian quality standards. Engagement oversight is "
        "maintained by the GTC central coordination team. Returns are subject to the same quality control "
        "diagnostics as Tier 1 and 2 filings, with additional translation and local-practice review steps."
    )

    # --- Section 3 ---
    pdf.section_heading("3.", "Three-Tier Review Process")
    pdf.body_text(
        "Every corporate income tax return prepared under the GTC program is subject to our mandatory "
        "three-tier review framework. This process is designed to ensure technical accuracy, consistency "
        "with prior-year positions, and compliance with both local statutory requirements and the client's "
        "global tax strategy."
    )
    pdf.subsection_heading("3.1", "Level 1 -- Preparer Self-Review")
    pdf.body_text(
        "The preparer completes a standardized self-review checklist covering 47 verification points, "
        "including mathematical accuracy, proper sourcing of trial balance data, correct application of "
        "tax rates (including any interim rate changes enacted during the tax year), and consistency "
        "with the Master File and Local File transfer pricing documentation (see M&A-TAX-TPF-002 for "
        "the firm's Transfer Pricing Advisory Framework). The preparer must also run the ONESOURCE "
        "Diagnostic Suite, which performs 200+ automated checks for common errors such as misclassified "
        "deductions, incorrect carryforward amounts, and missing disclosure items."
    )

    pdf.subsection_heading("3.2", "Level 2 -- Technical Reviewer")
    pdf.body_text(
        "An experienced manager, senior manager, or director conducts a substantive technical review "
        "focusing on: (i) proper application of local tax law provisions, including recent legislative "
        "changes; (ii) consistency with transfer pricing benchmarking studies and intercompany agreements; "
        "(iii) correct treatment of permanent and temporary differences; (iv) adequacy of uncertain tax "
        "position disclosures under ASC 740-10 (where the client reports under US GAAP); and (v) "
        "compliance with any Advance Pricing Agreement (APA) or ruling conditions. The reviewer "
        "documents all findings in the electronic workpaper system and must clear all items before "
        "the return advances to Level 3."
    )

    pdf.subsection_heading("3.3", "Level 3 -- Signing Partner")
    pdf.body_text(
        "The signing partner performs a top-level review concentrating on material positions, overall "
        "effective tax rate reasonableness, cross-border consistency (e.g., correlative adjustments, "
        "withholding tax reclaims), and alignment with the client's documented tax risk appetite. The "
        "partner also confirms that the return is consistent with the information reported in the "
        "CbCR Master File and that any Pillar Two top-up tax exposure has been identified and "
        "communicated to the client's tax department."
    )

    # --- Section 4 ---
    pdf.section_heading("4.", "Technology Platform -- ONESOURCE Integration")
    pdf.body_text(
        "The GTC program is built on Thomson Reuters ONESOURCE as the primary compliance technology "
        "platform, supplemented by proprietary Meridian tools and integrations:"
    )
    pdf.bullet_list([
        "ONESOURCE Income Tax (federal and international modules) -- core return preparation engine supporting 70+ country forms.",
        "ONESOURCE DataFlow -- automated data ingestion from client ERP systems (SAP, Oracle, Workday), eliminating manual data entry for 85% of trial balance line items.",
        "ONESOURCE Tax Provision -- integrated provision-to-return reconciliation ensuring consistency between ASC 740 workpapers and filed returns.",
        "Meridian GlobalView Dashboard -- proprietary Power BI analytics layer providing real-time visibility into filing status, reviewer assignments, and approaching deadlines across all jurisdictions.",
        "Meridian DiagnosticAI -- machine learning model trained on 10 years of historical return data to flag anomalous positions, unusual effective tax rate movements, and potential computational errors before human review.",
    ])

    # --- Section 5 ---
    pdf.section_heading("5.", "BEPS Compliance -- CbCR and Pillar Two")
    pdf.subsection_heading("5.1", "Country-by-Country Reporting")
    pdf.body_text(
        "For clients with consolidated group revenue exceeding EUR 750 million (or local currency "
        "equivalent), the GTC program includes preparation and filing of CbCR reports in accordance "
        "with BEPS Action 13 and local implementing legislation. Our CbCR process includes:"
    )
    pdf.bullet_list([
        "Automated data extraction from consolidation systems to populate Table 1 (allocation of income, taxes, and business activities by jurisdiction) and Table 2 (list of constituent entities).",
        "Consistency validation between CbCR data, filed tax returns, and consolidated financial statements -- discrepancies exceeding materiality thresholds trigger mandatory review.",
        "Surrogate filing and notification tracking -- monitoring which jurisdictions require primary vs. surrogate filings, including compliance with exchange-of-information agreements.",
        "Annual CbCR risk assessment identifying jurisdictions where reported data may attract enhanced scrutiny from local tax authorities.",
    ])

    pdf.subsection_heading("5.2", "Pillar Two GloBE Rules -- 15% Minimum Tax")
    pdf.body_text(
        "The Pillar Two GloBE rules require in-scope multinational groups to calculate a jurisdictional "
        "effective tax rate (ETR) and pay a top-up tax where the ETR falls below 15%. The Income "
        "Inclusion Rule (IIR) is effective for fiscal years beginning on or after December 31, 2023; "
        "the Undertaxed Profits Rule (UTPR) is effective for fiscal years beginning on or after "
        "December 31, 2024. The GTC program has been enhanced to include:"
    )
    pdf.bullet_list([
        "Jurisdictional ETR computation using the GloBE Income and Covered Taxes framework, including adjustments for timing differences, stock-based compensation, and excluded dividends.",
        "Substance-based income exclusion (SBIE) calculations -- payroll and tangible asset carve-outs by jurisdiction.",
        "Qualified Domestic Minimum Top-up Tax (QDMTT) analysis for jurisdictions that have adopted domestic top-up mechanisms (e.g., UK, EU member states, South Korea, Japan).",
        "Transitional safe harbor assessments under the CbCR and simplified ETR tests to minimize compliance burden during the initial implementation period.",
        "Integration of top-up tax estimates into quarterly ASC 740 provision calculations for US GAAP reporting clients.",
    ])

    # --- Section 6 ---
    pdf.section_heading("6.", "Quality Control & Performance Metrics")
    pdf.body_text(
        "The GTC program is subject to continuous quality monitoring against the following key "
        "performance indicators (KPIs), reported monthly to the Tax Services Executive Committee:"
    )
    pdf.key_value_block([
        ("Amendment Rate:", "< 0.5% of filed returns requiring amendment (FY2025 actual: 0.37%)"),
        ("On-Time Filing Rate:", "> 99.5% of returns filed by statutory deadline (FY2025 actual: 99.8%)"),
        ("Client Satisfaction:", "> 4.5/5.0 on post-engagement survey (FY2025 actual: 4.7/5.0)"),
        ("Diagnostic Pass Rate:", "> 98% of returns passing all automated checks on first submission (FY2025 actual: 98.4%)"),
        ("Review Cycle Time:", "< 5 business days from draft completion to partner sign-off for Tier 1 returns"),
    ])
    pdf.body_text(
        "Root cause analysis is performed on every amended return, with findings incorporated into "
        "the annual update of preparer training materials and diagnostic rules. The GTC quality "
        "assurance team conducts quarterly cold reviews of a random 5% sample of filed returns, "
        "with results reported to the National Office of Tax Quality."
    )
    pdf.note_box(
        "Effective Q2 2026, all GTC returns will be subject to enhanced Pillar Two consistency "
        "checks as part of the ONESOURCE Diagnostic Suite upgrade (Release 26.1)."
    )

    pdf.save("global_tax_compliance.pdf")


# ===================================================================
# DOCUMENT 2: Transfer Pricing Framework
# ===================================================================

def build_transfer_pricing():
    pdf = FirmPDF(
        title="Transfer Pricing Advisory Framework",
        subtitle="Intercompany Transaction Analysis, Documentation & Dispute Resolution\nBEPS-Aligned Methodology",
        doc_id="M&A-TAX-TPF-002",
        version="3.8",
        effective_date="March 1, 2026",
    )
    pdf.cover_page()

    pdf.add_page()
    pdf.section_heading("1.", "Executive Summary")
    pdf.body_text(
        "Meridian & Associates' Transfer Pricing Advisory Framework establishes the firm's standardized "
        "methodology for analyzing, documenting, and defending intercompany transactions across multinational "
        "group structures. This framework is fully aligned with the OECD Transfer Pricing Guidelines (2022 "
        "revision), the United States Internal Revenue Code Section 482 regulations, and the BEPS Action "
        "8-10 recommendations on aligning transfer pricing outcomes with value creation. In FY2025, the "
        "Transfer Pricing practice served 680+ clients, prepared 2,100+ benchmarking studies, and "
        "successfully resolved 45 bilateral APA negotiations with an average cycle time of 22 months."
    )

    pdf.section_heading("2.", "Functional Analysis Methodology")
    pdf.body_text(
        "The functional analysis is the foundational step in any transfer pricing engagement. Our "
        "methodology follows a structured five-phase approach designed to accurately delineate the "
        "controlled transaction and identify the economically significant activities, assets, and risks "
        "borne by each party:"
    )
    pdf.subsection_heading("2.1", "Phase 1 -- Industry and Business Model Mapping")
    pdf.body_text(
        "We begin with a comprehensive review of the client's industry dynamics, competitive positioning, "
        "and global operating model. This includes analysis of the value chain from raw material sourcing "
        "through end-customer delivery, identification of key value drivers (e.g., proprietary technology, "
        "brand, distribution network, regulatory expertise), and mapping of how profits flow through the "
        "intercompany structure. We leverage Meridian's proprietary Industry Knowledge Database, which "
        "contains functional profiles for over 40 industry verticals based on 15+ years of engagement data."
    )

    pdf.subsection_heading("2.2", "Phase 2 -- Entity-Level Function, Asset & Risk (FAR) Profiling")
    pdf.body_text(
        "Each entity participating in the controlled transaction is profiled using our standardized FAR "
        "template. Functions documented include: R&D and product development, manufacturing and assembly, "
        "supply chain management, marketing and sales, after-sale service, treasury and financing, and "
        "strategic management. Assets catalogued include tangible property, intellectual property (patents, "
        "trade secrets, trademarks, customer relationships), and financial assets. Risk allocation is "
        "assessed under the six-step OECD risk framework: (i) identification, (ii) contractual assumption, "
        "(iii) functional risk management, (iv) financial capacity to assume risk, (v) actual conduct "
        "of the parties, and (vi) allocation of risk consequences."
    )

    pdf.subsection_heading("2.3", "Phase 3 -- Transaction Characterization")
    pdf.body_text(
        "Based on the FAR profiles, each intercompany transaction is characterized by type: tangible goods "
        "transfer, provision of services (routine vs. high-value), licensing of intangible property, "
        "financial transactions (loans, guarantees, cash pooling), or cost contribution arrangements. "
        "The characterization determines the appropriate transfer pricing method and comparability factors."
    )

    # --- Section 3 ---
    pdf.section_heading("3.", "Benchmarking Methodologies")
    pdf.body_text(
        "Meridian applies the following OECD-recognized methods, selecting the most appropriate method "
        "(MAM) based on the functional profile and data availability:"
    )
    pdf.subsection_heading("3.1", "Comparable Uncontrolled Price (CUP) Method")
    pdf.body_text(
        "The CUP method compares the price charged in a controlled transaction to the price charged in a "
        "comparable uncontrolled transaction under comparable circumstances. This method is preferred when "
        "reliable internal or external comparables exist -- particularly for commodity transactions (using "
        "quoted prices per OECD guidance on commodity transactions), royalty arrangements with publicly "
        "available licensing agreements, and intercompany services with market-rate benchmarks. We maintain "
        "proprietary CUP databases covering 12 commodity categories and 8 technology licensing segments."
    )

    pdf.subsection_heading("3.2", "Transactional Net Margin Method (TNMM)")
    pdf.body_text(
        "The TNMM examines the net profit relative to an appropriate base (costs, sales, assets) that a "
        "taxpayer realizes from a controlled transaction. This is the most frequently applied method in "
        "our practice (approximately 65% of benchmarking studies). Our TNMM benchmarking process utilizes "
        "Bureau van Dijk (BvD) databases -- primarily Orbis and TP Catalyst -- to identify independent "
        "comparables. Search strategies are documented in detail, including SIC/NACE code selection, "
        "geographic scope, quantitative screens (revenue thresholds, independence indicators, financial "
        "data availability), and qualitative comparability adjustments."
    )
    pdf.body_text(
        "Profit level indicators (PLIs) are selected based on the tested party's profile: operating "
        "margin for distributors, Berry ratio (gross profit / operating expenses) for service providers, "
        "return on total costs for contract manufacturers, and return on assets for capital-intensive "
        "operations. Interquartile range analysis is performed to establish the arm's length range, with "
        "the median used as the point estimate for planning and provision purposes."
    )

    pdf.subsection_heading("3.3", "Profit Split Method")
    pdf.body_text(
        "The profit split method divides the combined profits from controlled transactions among the "
        "associated enterprises based on the relative value of each party's contributions. We apply "
        "this method when both parties make unique and valuable contributions (e.g., integrated R&D "
        "partnerships, co-branding arrangements, or highly integrated supply chains where one-sided "
        "methods cannot reliably isolate routine returns). Our approach employs both the residual "
        "profit split (allocating routine returns first, then splitting residual based on relative "
        "contributions to value creation) and the contribution analysis."
    )

    # --- Section 4 ---
    pdf.section_heading("4.", "BEPS Action 13 Documentation")
    pdf.subsection_heading("4.1", "Master File")
    pdf.body_text(
        "The Master File provides a high-level overview of the multinational group's global business "
        "operations and transfer pricing policies. Our Master File template covers: (i) organizational "
        "structure -- legal entity chart with ownership percentages and jurisdiction of incorporation; "
        "(ii) description of the group's business -- principal business activities, key product/service "
        "lines, geographic markets, and major supply chain flows; (iii) intangibles -- strategy for "
        "development, ownership, and exploitation, list of important intangibles with legal owners, and "
        "intercompany agreements relating to intangibles including cost contribution and licensing "
        "arrangements; (iv) intercompany financial activities -- description of group financing, including "
        "treasury centers, material financing arrangements, and transfer pricing policies for financial "
        "transactions; and (v) financial and tax positions -- consolidated financial statements and "
        "existing unilateral APAs, bilateral APAs, and rulings."
    )

    pdf.subsection_heading("4.2", "Local File")
    pdf.body_text(
        "The Local File provides detailed transactional transfer pricing documentation for each "
        "jurisdiction. Our Local File template for each material entity includes: detailed description "
        "of the local entity's management structure, organizational chart, and business strategy; "
        "identification of each category of controlled transaction with transaction values; functional "
        "analysis of the local entity and relevant associated enterprises; selection of the most "
        "appropriate transfer pricing method with reasoning; identification of comparables (including "
        "search strategy) and determination of arm's length range; financial data supporting the "
        "arm's length nature of the transactions; and copies of material intercompany agreements."
    )

    # --- Section 5 ---
    pdf.section_heading("5.", "Advance Pricing Agreements (APAs)")
    pdf.body_text(
        "Meridian's APA practice specializes in bilateral and multilateral APA negotiations, providing "
        "certainty over transfer pricing treatment for prospective periods (typically 5 years with "
        "rollback to open years). Our APA process includes:"
    )
    pdf.bullet_list([
        "Pre-filing conference with the IRS APMA program (or foreign equivalent competent authority) to discuss the proposed covered transactions, methodology, and critical assumptions.",
        "Preparation and submission of the formal APA request, including detailed functional analysis, proposed transfer pricing method, economic analysis with arm's length range, and projections.",
        "Negotiation support through the competent authority process, including preparation of position papers, economic modeling of alternative scenarios, and attendance at bilateral meetings.",
        "Post-APA compliance monitoring -- annual reporting obligations, critical assumption testing, and renewal planning beginning 18 months before expiration.",
    ])
    pdf.body_text(
        "In our experience, bilateral APAs between the United States and the following treaty partners "
        "have the highest success rates and most predictable timelines: Japan (average 24 months), "
        "United Kingdom (18 months), Canada (20 months), Germany (26 months), and India (30 months). "
        "We recommend bilateral over unilateral APAs in virtually all cases, as unilateral APAs do not "
        "eliminate double taxation risk."
    )

    # --- Section 6 ---
    pdf.section_heading("6.", "DEMPE Analysis for Intangibles")
    pdf.body_text(
        "Following the BEPS Action 8-10 revisions to the OECD Guidelines, legal ownership of intangible "
        "property alone is insufficient to entitle an entity to intangible-related returns. The DEMPE "
        "framework requires analysis of which entities perform and control the Development, Enhancement, "
        "Maintenance, Protection, and Exploitation of intangibles. Our DEMPE analysis framework includes:"
    )
    pdf.bullet_list([
        "Development -- identify entities performing R&D, design, testing, and regulatory activities; assess whether the legal owner controls and funds development or merely bears title.",
        "Enhancement -- determine which entities improve or update existing intangibles, including software version upgrades, product reformulations, and process improvements.",
        "Maintenance -- assess ongoing activities to preserve intangible value, such as quality control, patent maintenance, trade secret protection protocols, and brand management.",
        "Protection -- identify entities responsible for legal protection (patent prosecution, trademark registration, litigation defense) and practical protection (cybersecurity, confidentiality measures).",
        "Exploitation -- determine which entities commercialize the intangibles through manufacturing, marketing, licensing, or sublicensing activities.",
    ])
    pdf.body_text(
        "Where the DEMPE analysis reveals misalignment between legal ownership and economic substance, "
        "we recommend intercompany arrangements that ensure entities performing significant DEMPE "
        "functions receive appropriate arm's length compensation -- often through cost contribution "
        "arrangements (CCAs) with buy-in payments or performance-based royalties."
    )

    # --- Section 7 ---
    pdf.section_heading("7.", "Financial Transactions Transfer Pricing")
    pdf.body_text(
        "The 2022 OECD guidance on financial transactions (Chapter X) introduced specific rules for "
        "pricing intercompany loans, guarantees, cash pooling, and captive insurance arrangements. "
        "Meridian's approach incorporates:"
    )
    pdf.bullet_list([
        "Accurate delineation of the financial transaction -- confirming the transaction's economic substance (e.g., whether an intercompany loan should be recharacterized as equity based on the borrower's debt capacity).",
        "Credit rating analysis for the borrower entity -- using Moody's CreditEdge, S&P Capital IQ, and our proprietary credit scoring model calibrated to the OECD's guidance on implicit group support.",
        "Arm's length interest rate benchmarking -- utilizing Bloomberg, Refinitiv, and proprietary databases of comparable third-party loan agreements, adjusting for tenor, currency, security, and covenants.",
        "Guarantee fee analysis -- quantifying the benefit to the guaranteed entity (yield approach) and comparing with independent guarantee fee market data.",
        "Cash pooling arrangements -- analysis of the notional pooling or physical pooling structure, allocation of interest benefits, and compensation to the cash pool leader for treasury functions.",
    ])

    # --- Section 8 ---
    pdf.section_heading("8.", "Penalty Protection & Compliance Monitoring")
    pdf.body_text(
        "Proper contemporaneous documentation is the primary mechanism for penalty protection under "
        "Section 6662(e) of the Internal Revenue Code (substantial valuation misstatement) and "
        "corresponding provisions in foreign jurisdictions. Our documentation strategy ensures:"
    )
    pdf.bullet_list([
        "Documentation is completed before the filing deadline for the relevant tax return (including extensions), satisfying the contemporaneous documentation requirement under Treas. Reg. Section 1.6662-6(d).",
        "All economic analyses are performed with reasonable diligence and good faith, meeting the reasonable cause and good faith exception under Section 6664(c).",
        "Annual compliance monitoring compares actual intercompany transaction results against benchmarked ranges, with remediation recommendations (e.g., year-end adjustments, compensating transactions) when results fall outside the interquartile range.",
        "Comprehensive workpaper files are maintained for a minimum of 7 years, supporting defense in the event of examination. All client data is handled in accordance with the firm's data privacy policy (see common_firm_wide/data_privacy_policy.pdf).",
    ])

    pdf.save("transfer_pricing_framework.pdf")


# ===================================================================
# DOCUMENT 3: Tax Provision ASC 740
# ===================================================================

def build_tax_provision():
    pdf = FirmPDF(
        title="Tax Provision Services -- ASC 740",
        subtitle="Standardized Process for Income Tax Accounting,\nQuarterly Forecasting & SOX Control Integration",
        doc_id="M&A-TAX-PRV-003",
        version="5.1",
        effective_date="February 1, 2026",
    )
    pdf.cover_page()

    pdf.add_page()
    pdf.section_heading("1.", "Executive Summary")
    pdf.body_text(
        "Meridian & Associates' Tax Provision Services practice provides comprehensive ASC 740 (Income "
        "Taxes) support to public and private companies, including quarterly and annual worldwide effective "
        "tax rate (ETR) calculations, uncertain tax position analysis, valuation allowance assessments, "
        "and disclosure preparation. Our practice supports over 500 SEC registrants and 300 private "
        "companies, with engagement teams leveraging ONESOURCE Tax Provision, Corptax, and Longview "
        "technology platforms. This document establishes the standardized process to be followed by all "
        "Meridian provision engagement teams to ensure technical accuracy, compliance with ASC 740 "
        "requirements, and integration with clients' SOX 404 internal control frameworks."
    )

    pdf.section_heading("2.", "Worldwide Effective Tax Rate Calculation")
    pdf.subsection_heading("2.1", "Annual ETR Determination")
    pdf.body_text(
        "The worldwide effective tax rate (ETR) is calculated as the ratio of total income tax expense "
        "(current plus deferred) to pre-tax book income from continuing operations. The annual ETR "
        "computation follows these steps:"
    )
    pdf.bullet_list([
        "Step 1: Compile pre-tax book income (loss) by jurisdiction, segregating domestic and foreign components per ASC 740-10-50-6.",
        "Step 2: Apply each jurisdiction's statutory corporate income tax rate to the respective pre-tax income. For jurisdictions with graduated rates or surcharges (e.g., German trade tax), apply the blended effective statutory rate.",
        "Step 3: Identify and quantify permanent differences -- items that affect book income but never affect taxable income (or vice versa). Common permanent differences include: nondeductible executive compensation (IRC Section 162(m)), meals and entertainment (IRC Section 274), tax-exempt municipal bond interest, goodwill impairment (nondeductible book impairment vs. amortizable tax goodwill), and foreign tax credit limitations under IRC Section 904.",
        "Step 4: Compute the net deferred tax provision by analyzing changes in temporary differences (deferred tax assets and liabilities) during the period.",
        "Step 5: Incorporate discrete items -- tax effects recognized entirely in the period they occur, such as enacted rate changes, return-to-provision adjustments, changes in valuation allowance, and resolution of uncertain tax positions.",
        "Step 6: Prepare the rate reconciliation (ASC 740-10-50-12) bridging from the statutory rate to the effective rate, with explanations for each reconciling item exceeding 5% of the statutory amount.",
    ])

    pdf.subsection_heading("2.2", "Quarterly ETR Forecasting (ASC 740-270)")
    pdf.body_text(
        "For interim reporting periods, ASC 740-270 (formerly APB 28 / FIN 18) requires the use of an "
        "estimated annual effective tax rate (EAETR) applied to year-to-date ordinary income. Our "
        "quarterly process includes:"
    )
    pdf.bullet_list([
        "Forecasting full-year pre-tax income by jurisdiction based on the latest internal budget or management projections.",
        "Estimating full-year permanent differences and tax credits expected to be realized ratably over the year.",
        "Computing the EAETR as: (Estimated full-year tax expense on ordinary income) / (Estimated full-year ordinary pre-tax income).",
        "Applying the EAETR to year-to-date ordinary income and subtracting prior quarter cumulative provision to determine the current quarter provision.",
        "Separately accounting for discrete items in the quarter in which they occur, outside the EAETR computation.",
        "Performing a quarterly 'true-up' analysis comparing prior quarter EAETR estimates to updated projections, with documentation of the drivers of any change exceeding 100 basis points.",
    ])
    pdf.note_box(
        "Jurisdictions with year-to-date ordinary losses where the tax benefit cannot be recognized "
        "(e.g., due to valuation allowance) must be excluded from the consolidated EAETR computation "
        "and treated as discrete items (per ASC 740-270-30-36(a))."
    )

    pdf.section_heading("3.", "Uncertain Tax Position Analysis (ASC 740-10)")
    pdf.body_text(
        "The assessment of uncertain tax positions (UTPs) follows the two-step recognition and "
        "measurement framework originally codified in FIN 48 (now ASC 740-10-25):"
    )
    pdf.subsection_heading("3.1", "Step 1 -- Recognition")
    pdf.body_text(
        "A tax position is recognized in the financial statements only if it is 'more likely than not' "
        "(MLTN, defined as a likelihood of greater than 50%) that the position will be sustained upon "
        "examination by the relevant taxing authority, based on the technical merits of the position. "
        "Our analysis framework requires engagement teams to:"
    )
    pdf.bullet_list([
        "Identify all significant tax positions taken or expected to be taken in the tax return, including positions related to the allocation of income between jurisdictions.",
        "Perform a technical merits analysis for each identified position, referencing applicable statutes, regulations, case law, revenue rulings, private letter rulings, and treaty provisions.",
        "Document the MLTN conclusion using Meridian's standardized UTP assessment template, including the basis for the conclusion, relevant authority citations, and any reliance on external opinions.",
        "Assign a probability-weighted outcome matrix for positions with multiple possible outcomes (e.g., audit settlement at 30% of the claimed benefit, full denial, or full sustainment).",
    ])

    pdf.subsection_heading("3.2", "Step 2 -- Measurement")
    pdf.body_text(
        "For positions that satisfy the MLTN recognition threshold, the tax benefit recognized in the "
        "financial statements is measured at the largest amount of benefit that is greater than 50% "
        "likely to be realized upon settlement. This 'cumulative probability' approach requires:"
    )
    pdf.bullet_list([
        "Identification of all possible outcomes and their associated probabilities.",
        "Ranking outcomes from most favorable to least favorable.",
        "Accumulating probabilities from the most favorable outcome until the cumulative probability exceeds 50%.",
        "Recognizing the tax benefit associated with the outcome at which the cumulative probability first exceeds 50%.",
    ])
    pdf.body_text(
        "Unrecognized tax benefits (the 'UTB reserve' or 'FIN 48 liability') are classified as "
        "current or noncurrent liabilities based on the expected timing of settlement. Interest and "
        "penalties, where applicable, are classified consistent with the client's accounting policy "
        "election (as income tax expense or other expense, per ASC 740-10-45-25)."
    )

    pdf.section_heading("4.", "Valuation Allowance Assessment")
    pdf.body_text(
        "A valuation allowance (VA) is recorded against deferred tax assets (DTAs) when it is 'more "
        "likely than not' that some portion or all of the DTA will not be realized. Our framework "
        "evaluates the following sources of evidence, as required by ASC 740-10-30-17 through 30-25:"
    )
    pdf.subsection_heading("4.1", "Positive Evidence (Supporting Realization)")
    pdf.bullet_list([
        "Existing contracts or firm backlog supporting future taxable income.",
        "History of cumulative profitability in the relevant jurisdiction over the most recent 3-year period.",
        "Taxable temporary differences reversing in the same period as deductible temporary differences (i.e., the 'source of income' analysis).",
        "Appreciated asset values (built-in gains) that would generate taxable income upon disposition.",
        "Tax planning strategies -- prudent and feasible actions that management would implement to prevent an operating loss or tax credit carryforward from expiring unused.",
    ])
    pdf.subsection_heading("4.2", "Negative Evidence (Weighing Against Realization)")
    pdf.bullet_list([
        "Cumulative losses in the relevant jurisdiction in recent years (strong negative evidence per ASC 740-10-30-21).",
        "History of operating loss or tax credit carryforwards expiring unused.",
        "Losses expected in early future years (sufficient to offset the positive evidence of profitability in later years).",
        "Unsettled circumstances that could adversely affect future profitability (e.g., pending litigation, regulatory changes, loss of key customer).",
    ])
    pdf.body_text(
        "Negative evidence -- particularly cumulative losses -- is generally considered 'objectively "
        "verifiable' and thus carries more weight than subjective positive evidence such as management "
        "projections of future profitability. A VA release requires sufficient positive evidence to "
        "overcome the negative, with robust documentation and sensitivity analysis."
    )

    pdf.section_heading("5.", "Deferred Tax Asset/Liability Roll-Forward")
    pdf.body_text(
        "Meridian's standardized DTA/DTL roll-forward workpaper tracks the movement in each temporary "
        "difference category from period opening to period close. The roll-forward reconciles:"
    )
    pdf.bullet_list([
        "Opening balance -- prior period ending DTA/DTL by category.",
        "Provision entries -- deferred tax expense (benefit) recorded during the period.",
        "Return-to-provision adjustments -- differences identified between the estimated provision and the filed return.",
        "OCI items -- deferred taxes on unrealized gains/losses, pension adjustments, and hedging instruments recognized in other comprehensive income.",
        "Equity items -- deferred taxes on stock-based compensation windfalls/shortfalls, convertible debt, and other items recorded directly to equity.",
        "Acquisition/disposition entries -- DTAs/DTLs acquired or disposed of in business combinations, including the impact of ASC 805 fair value measurement.",
        "Currency translation -- remeasurement of foreign-denominated DTAs/DTLs at period-end exchange rates.",
        "Closing balance -- period ending DTA/DTL by category, net of valuation allowance.",
    ])

    pdf.section_heading("6.", "SOX Control Integration")
    pdf.body_text(
        "For SEC registrant clients, the tax provision process must be designed to operate within the "
        "company's SOX 404 internal control over financial reporting (ICFR) framework. Key controls "
        "include:"
    )
    pdf.bullet_list([
        "Management Review Control (MRC) -- a qualified tax professional reviews the tax provision workpapers, rate reconciliation, and disclosure schedules before recording journal entries. The MRC must be evidenced by sign-off with documented review points.",
        "Data Input Controls -- validation of trial balance data from the general ledger to the provision model, including automated reconciliation of total pre-tax income.",
        "Completeness Controls -- procedures to ensure all entities, all jurisdictions, and all significant tax positions are captured in the provision calculation.",
        "Spreadsheet Controls -- version management, access restrictions, and formula integrity checks for non-system provision workpapers (particularly relevant for Excel-based provision models).",
        "IT General Controls -- system access, change management, and backup procedures for ONESOURCE Tax Provision, Corptax, or other technology platforms used in the provision process.",
        "Disclosure Checklist -- a standardized disclosure checklist mapping each ASC 740 disclosure requirement (ASC 740-10-50-1 through 50-22) to the source data and preparer/reviewer sign-off.",
    ])

    pdf.section_heading("7.", "Common Pitfalls and Quality Review Checkpoints")
    pdf.body_text(
        "Based on analysis of 2,000+ provision engagements over the past three years, the following "
        "issues represent the most frequent sources of error in ASC 740 computations:"
    )
    pdf.bullet_list([
        "Incorrect treatment of outside basis differences -- failing to record deferred taxes on undistributed foreign earnings after the TCJA transition tax, or incorrectly applying the indefinite reinvestment assertion under ASC 740-30-25-17.",
        "GILTI/Subpart F interaction errors -- double-counting foreign income inclusions or failing to account for Section 250 GILTI deduction limitations when computing the EAETR (see M&A-TAX-INTL-009 for GILTI planning methodology and Section 250 deduction analysis).",
        "State apportionment changes -- not updating state ETRs when the client's apportionment factors shift due to acquisitions, remote-work policies, or market-based sourcing adoption.",
        "Intercompany profit elimination -- omitting the deferred tax effect of unrealized intercompany profits in inventory (ASC 740-10-25-3(e)) or in fixed assets.",
        "Rate change errors -- failing to remeasure DTAs/DTLs using the enacted rate in the period of expected reversal, particularly when multi-year rate phase-ins are enacted.",
        "UTP staleness -- not reassessing uncertain tax positions quarterly for changes in facts, law, or the statute of limitations.",
    ])
    pdf.note_box(
        "All provision workpapers are subject to Meridian's National Office Technical Review (NOTR) "
        "for clients with total assets exceeding $1 billion or income tax expense exceeding $50 million."
    )

    pdf.save("tax_provision_asc740.pdf")


# ===================================================================
# DOCUMENT 4: M&A Tax Due Diligence
# ===================================================================

def build_ma_due_diligence():
    pdf = FirmPDF(
        title="M&A Tax Due Diligence",
        subtitle="Buy-Side and Sell-Side Engagement Methodology\nIdentification of Tax Risks, Opportunities & Structural Considerations",
        doc_id="M&A-TAX-MDD-004",
        version="3.5",
        effective_date="January 15, 2026",
    )
    pdf.cover_page()

    pdf.add_page()
    pdf.section_heading("1.", "Executive Summary")
    pdf.body_text(
        "Meridian & Associates' M&A Tax Due Diligence practice provides comprehensive tax risk "
        "identification and quantification services for both buy-side and sell-side transactions. Our "
        "methodology is designed to enable acquirers, sellers, and their counsel to make informed "
        "decisions regarding transaction structure, purchase price, indemnification provisions, and "
        "post-close integration. In FY2025, the practice supported 320+ transactions ranging from "
        "$25 million to $14 billion in enterprise value, across sectors including technology, "
        "healthcare, financial services, energy, consumer products, and industrials. Our average "
        "engagement identifies $8-15 million in contingent tax exposures per $1 billion of enterprise "
        "value, along with $3-7 million in structuring savings opportunities."
    )

    pdf.section_heading("2.", "Buy-Side Due Diligence Approach")
    pdf.subsection_heading("2.1", "Phase 1 -- Preliminary Tax Assessment")
    pdf.body_text(
        "Upon engagement, the buy-side due diligence team conducts an initial review based on publicly "
        "available information and preliminary data provided by the target or its advisors. This phase "
        "typically occurs in parallel with the financial and legal due diligence workstreams and produces "
        "an Initial Tax Issues Memorandum within 5-7 business days. Key activities include:"
    )
    pdf.bullet_list([
        "Review of the target's organizational chart and legal entity structure, including identification of foreign holding companies, IP holding entities, and pass-through structures.",
        "Analysis of publicly filed tax returns (10-K tax footnote, tax provision disclosures, effective rate reconciliation) to identify potential risk areas.",
        "Preliminary assessment of net operating loss (NOL) carryforwards, tax credit carryforwards, and other tax attributes, including their potential vulnerability to limitation under IRC Section 382.",
        "Identification of historical acquisitions, dispositions, and restructurings that may have created embedded tax issues (e.g., deferred intercompany gains under the consolidated return regulations).",
        "Industry-specific tax risk screening -- e.g., for technology targets: R&D credit substantiation, transfer pricing for IP-intensive operations, state nexus from SaaS sales; for healthcare targets: Section 501(c)(3) UBIT exposures, provider tax assessments, Medicaid rebate accruals.",
    ])

    pdf.subsection_heading("2.2", "Phase 2 -- Detailed Tax Diligence Review")
    pdf.body_text(
        "Following execution of the letter of intent and access to the virtual data room, the team "
        "performs a comprehensive review organized around the following workstreams:"
    )
    pdf.subsection_heading("2.2.1", "Federal Income Tax Review")
    pdf.body_text(
        "The federal income tax workstream includes a detailed review of the target's federal income tax "
        "returns for the most recent 3-5 years (or longer if returns for prior periods remain open under "
        "statute). Specific areas of focus include:"
    )
    pdf.bullet_list([
        "Revenue recognition timing -- comparison of book and tax methods for long-term contracts (Section 460), installment sales (Section 453), and original issue discount (Section 1272).",
        "Deduction analysis -- review of Section 163(j) interest expense limitation calculations, Section 199A qualified business income deduction (for pass-throughs), Section 174 R&E capitalization and amortization (effective for tax years beginning after 2021), and depreciation methods (bonus depreciation phase-down schedule).",
        "Entity classification -- confirmation of entity-level check-the-box elections (Form 8832) for domestic and foreign subsidiaries, with analysis of implications of any election changes.",
        "Accounting method review -- identification of permissible vs. impermissible methods, automatic vs. non-automatic method changes (Forms 3115), and Section 481(a) adjustment computations.",
        "Consolidated return issues -- intercompany transactions, deferred gain/loss, excess loss accounts (ELAs) in subsidiary stock basis, SRLY limitations on loss and credit carryforwards.",
    ])

    pdf.subsection_heading("2.2.2", "State and Local Tax Review")
    pdf.body_text(
        "The state and local tax (SALT) workstream is frequently the area of highest exposure in "
        "diligence, particularly for companies that have expanded geographically through organic growth "
        "or acquisition without updating their state tax compliance. Our SALT review includes:"
    )
    pdf.bullet_list([
        "Nexus analysis -- physical presence, economic nexus (post-Wayfair thresholds), and factor presence standards across all 50 states and the District of Columbia.",
        "Income/franchise tax exposure quantification -- including analysis of apportionment methodology (market-based sourcing vs. cost-of-performance), combined/unitary filing requirements, and state-specific addback statutes (intercompany interest, management fees, intangible expenses).",
        "Sales and use tax compliance -- review of taxability determinations for the target's product/service mix, exemption certificate management, and reverse audit exposure.",
        "Property tax compliance -- real and personal property tax filings, valuation appeals status, and potential exposure from unreported personal property assets.",
        "Unclaimed property -- review of escheatment compliance for uncashed checks, outstanding credits, and dormant accounts.",
    ])

    pdf.subsection_heading("2.2.3", "International Tax Review")
    pdf.body_text(
        "For targets with cross-border operations, the international tax workstream covers:"
    )
    pdf.bullet_list([
        "Controlled Foreign Corporation (CFC) analysis -- Subpart F income, GILTI inclusions, previously taxed income (PTI) tracking, and Section 956 investment in US property.",
        "Transfer pricing review -- evaluation of intercompany pricing policies, documentation adequacy, and exposure to adjustment by foreign tax authorities (see M&A-TAX-TPF-002 for the firm's Transfer Pricing Advisory Framework and BEPS Action 13 documentation standards).",
        "Permanent establishment risk -- analysis of employee and agent activities in foreign jurisdictions that may create unregistered PEs under applicable tax treaties.",
        "Foreign tax credit analysis -- credit vs. deduction elections, foreign tax credit limitation computations, and carryforward/carryback positions.",
        "Treaty benefit analysis -- withholding tax rates applied to cross-border payments (dividends, interest, royalties), limitation on benefits (LOB) provisions, and potential treaty shopping exposure.",
    ])

    pdf.section_heading("3.", "Net Operating Loss & Section 382 Analysis")
    pdf.body_text(
        "A critical component of buy-side diligence for targets with accumulated NOLs is the Section 382 "
        "limitation analysis. Section 382 of the Internal Revenue Code limits the annual use of pre-change "
        "NOLs (and certain other tax attributes) following an 'ownership change' -- defined as a more than "
        "50 percentage point increase in stock ownership by 5-percent shareholders over a 3-year testing "
        "period. Our analysis includes:"
    )
    pdf.bullet_list([
        "Determination of the target's 'testing date' ownership shifts -- analysis of all equity issuances, redemptions, option exercises, and secondary market trading activity that may have triggered prior ownership changes.",
        "Computation of the Section 382 annual limitation amount -- the product of the target's equity value immediately before the ownership change (as adjusted for capital contributions and other modifications) and the applicable long-term tax-exempt rate published monthly by the IRS.",
        "Net unrealized built-in gain/loss (NUBIG/NUBIL) analysis -- determination of whether the target's assets have a net built-in gain or loss as of the testing date, which can increase or decrease the Section 382 limitation for the 5-year recognition period.",
        "Impact on NOL utilization modeling -- projection of post-change NOL absorption rates under the Section 382 limitation, with sensitivity analysis for variations in purchase price (affecting the limitation amount) and future taxable income projections.",
        "Section 383 analysis -- parallel limitation on pre-change tax credit carryforwards (R&D credits, AMT credits, foreign tax credits).",
    ])

    pdf.section_heading("4.", "Purchase Price Allocation Tax Implications")
    pdf.body_text(
        "The structure of the acquisition (asset purchase vs. stock purchase, taxable vs. tax-free "
        "reorganization) has significant implications for the tax basis of acquired assets and the "
        "resulting deferred tax balance sheet. We advise on:"
    )
    pdf.bullet_list([
        "Section 338(h)(10) and 336(e) elections -- converting a stock acquisition into a deemed asset acquisition for tax purposes, enabling a step-up in the tax basis of the target's assets. We model the tax cost of the deemed sale against the present value of future tax depreciation/amortization deductions.",
        "Section 1060 allocation -- allocation of the purchase price among seven asset classes (I through VII), with particular focus on the allocation between amortizable goodwill and going concern value (15-year Section 197 intangibles) and non-amortizable assets.",
        "Deferred tax impact -- computation of deferred tax liabilities arising from book-tax basis differences created by ASC 805 fair value adjustments, including the circular calculation where the DTL itself affects the amount of goodwill.",
        "Contingent consideration -- tax treatment of earnout and milestone payments, including the application of the installment method (Section 453) or open transaction doctrine, and the tax classification of payments (capital gain vs. ordinary income to the seller, purchase price vs. compensation to the buyer).",
    ])

    pdf.section_heading("5.", "Tax Representations, Warranties & Indemnities")
    pdf.body_text(
        "Based on diligence findings, we prepare a Tax Issues Summary Memorandum that supports the "
        "negotiation of tax-specific representations, warranties, and indemnification provisions in "
        "the acquisition agreement. Key elements include:"
    )
    pdf.bullet_list([
        "Specific tax representations -- recommended representations addressing identified exposures (e.g., that the target has not entered into any listed or reportable transactions, that all transfer pricing is at arm's length, that no nexus exists in non-filing states).",
        "Tax indemnification provisions -- recommendations on special tax indemnities for quantified exposures, including survival periods extending beyond the general indemnity basket (typically matching the applicable statute of limitations plus 60 days).",
        "Tax covenants -- recommended covenants restricting pre-close tax elections, amended returns, or settlement of tax audits without buyer consent.",
        "Purchase price adjustment mechanisms -- tax treatment of working capital adjustments, and provisions for allocation of tax refunds and credits related to pre-close periods.",
    ])

    pdf.section_heading("6.", "Post-Close Integration Planning")
    pdf.body_text(
        "Our M&A Tax practice supports post-close integration through the following services, typically "
        "engaged as a separate workstream beginning 60-90 days before anticipated closing:"
    )
    pdf.bullet_list([
        "Day 1 readiness -- ensuring all required entity formations, dissolutions, mergers, and conversions are completed by closing, with corresponding state and federal filings.",
        "Integration of tax compliance -- migration of the target's tax compliance to the acquirer's systems and processes, including alignment of tax accounting methods, fiscal year conformity, and consolidated return group inclusion.",
        "Restructuring planning -- design and implementation of post-close legal entity rationalization, including elimination of redundant holding structures, repatriation of offshore cash, and establishment of tax-efficient supply chain and IP ownership structures.",
        "Synergy tax modeling -- quantification of the tax impact of planned operational synergies (headcount reductions, facility consolidations, system integrations) on the combined entity's effective tax rate.",
        "Section 382 monitoring -- establishment of ongoing ownership change tracking protocols to prevent inadvertent limitation of the combined entity's tax attributes.",
    ])

    pdf.save("ma_tax_due_diligence.pdf")


# ===================================================================
# DOCUMENT 5: Credits and Incentives
# ===================================================================

def build_credits_incentives():
    pdf = FirmPDF(
        title="Tax Credits & Incentives Advisory",
        subtitle="Identification, Quantification & Compliance for Federal,\nState, and International Tax Benefits",
        doc_id="M&A-TAX-TCI-005",
        version="6.0",
        effective_date="January 1, 2026",
    )
    pdf.cover_page()

    pdf.add_page()
    pdf.section_heading("1.", "Executive Summary")
    pdf.body_text(
        "Meridian & Associates' Tax Credits & Incentives (TCI) practice is a dedicated team of 180+ "
        "professionals focused on identifying, quantifying, and sustaining tax credits, deductions, "
        "exemptions, and economic development incentives for corporate clients. In FY2025, the TCI "
        "practice identified total tax savings of $2.1 billion across our client portfolio, spanning "
        "federal R&D credits, state and local incentives, energy credits under the Inflation Reduction "
        "Act, cost segregation studies, export incentives, and economic development grants. Our approach "
        "integrates tax technical expertise with industry-specific knowledge, engineering and scientific "
        "disciplines, and data analytics to deliver defensible, audit-ready benefit computations."
    )
    pdf.body_text(
        "This document describes the methodologies and engagement approaches for each major credit and "
        "incentive category within the TCI practice. All work products are designed to meet the "
        "documentation requirements necessary for penalty protection under IRC Section 6662 and "
        "corresponding state provisions."
    )

    pdf.section_heading("2.", "Research & Development Tax Credit (IRC Section 41)")
    pdf.subsection_heading("2.1", "Four-Part Test Methodology")
    pdf.body_text(
        "The federal R&D tax credit under IRC Section 41 provides a credit for qualified research "
        "expenditures (QREs) incurred in carrying out qualified research activities. Meridian's "
        "R&D credit methodology applies the four-part test established in Treasury Regulation "
        "Section 1.41-4 to each business component (product, process, technique, formula, invention, "
        "or software module) under examination:"
    )
    pdf.bullet_list([
        "Section 174 Test: The research expenditures must be eligible for treatment as research or experimental expenditures under IRC Section 174 (now subject to mandatory 5-year domestic / 15-year foreign amortization for tax years beginning after December 31, 2021, per the Tax Cuts and Jobs Act amendment).",
        "Technological in Nature Test: The activity must rely on principles of physical or biological science, engineering, or computer science. We evaluate whether the activity involves the application of scientific principles, algorithms, or engineering analysis -- as opposed to routine testing, quality control, or market research.",
        "Elimination of Uncertainty Test: The research must be undertaken for the purpose of discovering information to eliminate uncertainty concerning the capability or method for developing or improving a business component, or the appropriateness of the business component's design.",
        "Process of Experimentation Test: Substantially all of the research activities must constitute elements of a process of experimentation -- the systematic evaluation of one or more alternatives through modeling, simulation, testing, or trial-and-error to achieve a result where the capability or method is uncertain.",
    ])

    pdf.subsection_heading("2.2", "Qualified Research Expense Categories")
    pdf.body_text(
        "We quantify QREs in the following categories, applying detailed time-tracking analysis, "
        "project-level documentation review, and employee interviews:"
    )
    pdf.bullet_list([
        "In-house wages -- wages paid to employees performing, directly supervising, or directly supporting qualified research activities. Includes salaries, bonuses, and stock-based compensation (to the extent included in W-2 wages).",
        "Contract research expenses -- 65% of amounts paid to third parties (or 75% for qualified research consortia) for qualified research performed on behalf of the taxpayer.",
        "Supply costs -- cost of tangible personal property (other than land or improvements to land) used in the conduct of qualified research, consumed or destroyed during experimentation.",
        "Cloud computing costs -- following the IRS's evolving guidance and recent court decisions, we analyze whether cloud infrastructure costs incurred in connection with qualified research qualify as supply costs under Section 41(b)(2)(A)(ii).",
    ])

    pdf.subsection_heading("2.3", "ASC 730 Documentation and Credit Computation")
    pdf.body_text(
        "Our R&D credit work product includes a detailed technical memorandum documenting qualifying "
        "activities and business components, a statistical sampling methodology (where applicable) in "
        "accordance with Rev. Proc. 2011-62 and IRS Directive LB&I-04-0117-005, and a credit "
        "computation workbook calculating the credit under both the Regular Credit (RC) and "
        "Alternative Simplified Credit (ASC) methods. We recommend the method that maximizes the "
        "current-year benefit, taking into account base period considerations and Section 280C "
        "election impacts."
    )

    pdf.section_heading("3.", "State and Local Incentives")
    pdf.subsection_heading("3.1", "Job Creation Tax Credits")
    pdf.body_text(
        "Many states offer income tax credits or payroll tax credits for the creation of new jobs, "
        "particularly in targeted industries or geographic zones. Meridian's state incentives team "
        "maintains a proprietary database of 1,200+ active state and local incentive programs across "
        "all 50 states, updated quarterly (see M&A-TAX-SALT-008 for the firm's comprehensive State "
        "and Local Tax methodology, including nexus analysis, apportionment planning, and state "
        "controversy practice). Common programs we evaluate include:"
    )
    pdf.bullet_list([
        "State R&D credits -- over 35 states offer R&D credits (some conforming to the federal methodology, others with state-specific definitions). We prepare state-specific calculations and documentation for each applicable jurisdiction.",
        "Job creation/retention credits -- available in nearly every state, with credit amounts typically ranging from $500 to $9,000 per qualifying job created above a baseline. Key states include Georgia, Ohio, New York, Texas, and California.",
        "Capital investment credits -- credits for investment in real property, machinery, and equipment, often tied to a minimum investment threshold and job creation requirement.",
        "Training and workforce development credits -- reimbursement or credit for qualified training expenditures for new or existing employees.",
        "Enterprise zone / opportunity zone incentives -- enhanced credits, deductions, or exemptions for businesses located in designated zones, including federal Qualified Opportunity Zone (QOZ) benefits under IRC Section 1400Z-2.",
    ])

    pdf.subsection_heading("3.2", "Property Tax Abatements and TIF Districts")
    pdf.body_text(
        "We negotiate property tax abatement agreements with local jurisdictions for qualifying capital "
        "investment projects. Our approach includes: economic impact analysis demonstrating the 'but for' "
        "necessity of the incentive, comparative site analysis showing alternative locations under "
        "consideration, negotiation of abatement terms (typically 50-100% abatement over 5-15 years "
        "with declining schedules), and ongoing compliance monitoring. For projects located within Tax "
        "Increment Financing (TIF) districts, we advise on the interaction between TIF benefits and "
        "other available incentives, ensuring clients capture the full stack of available programs."
    )

    pdf.section_heading("4.", "Federal Energy Credits -- Inflation Reduction Act")
    pdf.subsection_heading("4.1", "Section 45 Production Tax Credit (PTC)")
    pdf.body_text(
        "The Inflation Reduction Act of 2022 (IRA) extended and expanded the Section 45 production tax "
        "credit for electricity produced from qualified energy resources (wind, solar, geothermal, "
        "biomass, hydropower, marine/hydrokinetic). For facilities placed in service after December 31, "
        "2024, the credit transitions to the technology-neutral Section 45Y clean electricity PTC. "
        "Our advisory services cover:"
    )
    pdf.bullet_list([
        "Project structuring -- analysis of direct ownership, partnership flip structures, sale-leaseback arrangements, and inverted lease pass-through structures to optimize credit monetization.",
        "Prevailing wage and apprenticeship requirements -- compliance planning to qualify for the 5x credit multiplier (increasing the base credit from approximately $0.55/kWh to $2.75/kWh for 2025).",
        "Domestic content bonus -- analysis of the manufactured product and mining/extraction components to determine eligibility for the additional 10% credit bonus under Section 45(b)(9).",
        "Energy community bonus -- geographic analysis to determine whether the facility is located in a qualifying energy community (brownfield site, statistical area with fossil fuel employment, or census tract with a retired coal facility), qualifying for an additional 10% credit bonus.",
        "Transferability and direct pay elections -- advising on the Section 6418 credit transfer mechanism (selling credits to unrelated third parties) and Section 6417 direct pay election (available to tax-exempt entities and certain other eligible taxpayers).",
    ])

    pdf.subsection_heading("4.2", "Section 48 Investment Tax Credit (ITC)")
    pdf.body_text(
        "The IRA also enhanced the Section 48 investment tax credit for energy property, with a base "
        "credit rate of 6% (30% with prevailing wage and apprenticeship compliance) for solar, fuel "
        "cell, microgrid, combined heat and power, geothermal, and energy storage property. For "
        "property placed in service after 2024, the technology-neutral Section 48E credit applies. "
        "Our ITC practice addresses project cost certification, placed-in-service date analysis, "
        "recapture risk management (5-year recapture period), and interaction with other federal and "
        "state incentives."
    )

    pdf.section_heading("5.", "Cost Segregation Studies")
    pdf.body_text(
        "Cost segregation studies reclassify building components from 39-year nonresidential real "
        "property (or 27.5-year residential rental property) to shorter-lived personal property "
        "classes (5, 7, or 15-year property) eligible for accelerated depreciation and, where "
        "applicable, bonus depreciation under the TCJA phase-down schedule: 100% (2022), 80% "
        "(2023), 60% (2024), 40% (2025), 20% (2026), and 0% thereafter. For property placed in "
        "service in 2025, the applicable bonus depreciation rate is 40%. Our studies are performed "
        "by multidisciplinary teams of tax professionals and licensed engineers, following the IRS "
        "Audit Technique Guide for Cost Segregation (2022 edition) and the AICPA Practice Guide. "
        "Typical savings range from 3-8% of total construction/acquisition costs, realized as "
        "accelerated deductions in the first 5-7 years of the asset's life."
    )

    pdf.section_heading("6.", "Work Opportunity Tax Credit (WOTC)")
    pdf.body_text(
        "The WOTC under IRC Section 51 provides a credit of up to $2,400-$9,600 per qualifying "
        "new hire from designated target groups (veterans, ex-felons, TANF recipients, SNAP "
        "recipients, designated community residents, summer youth employees, and others). Meridian's "
        "WOTC practice provides end-to-end administration including: new hire screening and Form 8850 "
        "processing (submitted to the State Workforce Agency within 28 days of start date), qualification "
        "verification, credit calculation, and IRS audit support. Our technology platform integrates "
        "with clients' ATS and HRIS systems (Workday, ADP, UKG) to automate screening at the point "
        "of hire, achieving an average certification rate of 15-20% of new hires for retail, "
        "hospitality, and distribution clients."
    )

    pdf.section_heading("7.", "IC-DISC / FDII Export Benefits")
    pdf.body_text(
        "For companies with qualifying export activities, we evaluate two primary export incentive "
        "structures:"
    )
    pdf.bullet_list([
        "Interest Charge Domestic International Sales Corporation (IC-DISC) -- a tax-advantaged entity that earns commission income on export sales, converting ordinary income to qualified dividend income for individual shareholders. Particularly beneficial for closely held C-corporations and S-corporations with export revenue. Our engagements include IC-DISC formation, commission calculations (the greater of 4% of gross receipts or 50% of combined taxable income from qualified export transactions), and compliance filings (Form 1120-IC-DISC).",
        "Foreign-Derived Intangible Income (FDII) -- for tax years beginning after December 31, 2025, the FDII deduction rate has decreased from 37.5% to 21.875% under IRC Section 250(a)(3), resulting in an effective tax rate of 16.406% on FDII (vs. 21% corporate rate). For prior tax years the deduction was 37.5% (effective 13.125% rate). We model the FDII benefit, prepare the Form 8993 computation, and assist with documentation of foreign use of services and property.",
    ])

    pdf.section_heading("8.", "Economic Development Grant Negotiation")
    pdf.body_text(
        "Beyond statutory tax credits, Meridian's TCI practice negotiates discretionary economic "
        "development incentive packages with state and local authorities for major capital investment "
        "and job creation projects. Our negotiation approach includes:"
    )
    pdf.bullet_list([
        "Comprehensive site selection analysis -- evaluating 3-5 finalist locations based on total cost of operations (labor, utilities, logistics, taxes, incentives) using our proprietary Location Optimizer model.",
        "Economic impact modeling -- preparation of fiscal and economic impact analyses (IMPLAN or REMI models) demonstrating the net positive fiscal impact of the project on the jurisdiction.",
        "Incentive term sheet negotiation -- structuring packages that may include cash grants, infrastructure improvements, training funds, property tax abatements, utility rate discounts, and expedited permitting.",
        "Clawback and compliance management -- negotiation of performance thresholds, grace periods, and proportional clawback provisions; ongoing compliance reporting to maintain incentive eligibility.",
    ])
    pdf.body_text(
        "In FY2025, the TCI practice negotiated $340 million in discretionary incentive packages "
        "across 48 projects in 22 states, with an average incentive value of 15-25% of total project "
        "capital expenditure."
    )

    pdf.save("credits_and_incentives.pdf")


# ===================================================================
# DOCUMENT 6: Tax Controversy
# ===================================================================

def build_tax_controversy():
    pdf = FirmPDF(
        title="Tax Controversy & Dispute Resolution",
        subtitle="IRS Examination Defense, Appeals Strategy & Litigation Support\nFederal, State, and International Proceedings",
        doc_id="M&A-TAX-CON-006",
        version="4.0",
        effective_date="February 15, 2026",
    )
    pdf.cover_page()

    pdf.add_page()
    pdf.section_heading("1.", "Executive Summary")
    pdf.body_text(
        "Meridian & Associates' Tax Controversy practice represents taxpayers in disputes with the "
        "Internal Revenue Service, state and local taxing authorities, and foreign tax administrations. "
        "Our team of 140+ controversy professionals -- including former IRS examination agents, Appeals "
        "officers, and Chief Counsel attorneys -- provides end-to-end representation from initial audit "
        "through administrative appeals, judicial proceedings, and competent authority negotiations. In "
        "FY2025, the practice managed 1,100+ active examination and appeals matters, resolved $3.8 "
        "billion in proposed adjustments (achieving an average favorable resolution rate of 72%), and "
        "handled 35 Tax Court cases, 12 refund suits (Court of Federal Claims and district courts), and "
        "8 competent authority proceedings."
    )

    pdf.section_heading("2.", "IRS Examination Defense Framework")
    pdf.subsection_heading("2.1", "Pre-Audit Positioning")
    pdf.body_text(
        "Effective audit defense begins before the first Information Document Request (IDR) is issued. "
        "Our pre-audit positioning services include:"
    )
    pdf.bullet_list([
        "Audit readiness assessment -- review of filed returns and supporting workpapers to identify positions that may attract scrutiny, with remediation recommendations (e.g., amended returns, voluntary disclosures, or protective refund claims filed before the audit commences).",
        "Controversy reserve analysis -- coordination with the tax provision team to ensure uncertain tax positions are accurately reserved under ASC 740-10, providing a reliable financial statement baseline against which audit outcomes can be measured.",
        "Document retention and privilege review -- ensuring the client's document retention policies are adequate and that privileged communications (attorney-client privilege, tax practitioner privilege under Section 7525, and work product doctrine) are properly identified and segregated before production.",
        "Power of Attorney (POA) filing -- preparation and submission of Form 2848 designating Meridian as the taxpayer's authorized representative, with appropriate scope limitations to control information flow.",
    ])

    pdf.subsection_heading("2.2", "IDR Response Protocols")
    pdf.body_text(
        "The Information Document Request is the IRS's primary tool for obtaining information during "
        "an examination. Our IDR response protocol is designed to be responsive and cooperative while "
        "protecting the client's rights:"
    )
    pdf.bullet_list([
        "IDR triage and scoping -- immediate review of each IDR upon receipt to assess the scope, relevance, and privilege implications of each requested item. IDRs that are overbroad or seek privileged materials are addressed through negotiation with the examining agent or, if necessary, escalation to the examination team manager.",
        "Response timeline management -- coordination with the IRS to establish reasonable response deadlines (typically 30-45 days for initial IDRs, 15-30 days for follow-up requests). We track all IDR deadlines in our matter management system with automated escalation alerts.",
        "Centralized production control -- all documents produced in response to IDRs are reviewed by the engagement team, Bates-stamped, logged in a production database, and accompanied by a transmittal letter describing the responsive materials. This prevents inadvertent production of privileged or non-responsive documents.",
        "Narrative responses -- for IDR items requesting explanations of tax positions, we prepare written narratives that articulate the technical basis for the position with supporting authority citations, framing the position favorably without volunteering information beyond the scope of the request.",
    ])

    pdf.section_heading("3.", "30-Day and 90-Day Letter Strategies")
    pdf.subsection_heading("3.1", "30-Day Letter Response")
    pdf.body_text(
        "When the IRS issues a 30-day letter (Revenue Agent Report or RAR) proposing adjustments to "
        "the taxpayer's return, the taxpayer has 30 days to either agree, partially agree, or file a "
        "written protest requesting consideration by the IRS Independent Office of Appeals. Our approach:"
    )
    pdf.bullet_list([
        "Detailed analysis of each proposed adjustment -- determination of the IRS's legal theory, factual basis, and computational accuracy.",
        "Concession analysis -- identification of adjustments that may be meritorious or immaterial, with a recommendation on strategic concession to focus Appeals resources on material disputed issues.",
        "Written protest preparation -- a comprehensive protest document setting forth: (i) a statement of the facts relevant to each disputed issue, (ii) a statement of the applicable law (including statutory provisions, regulations, case law, and IRS guidance), (iii) an argument demonstrating why the taxpayer's position should be sustained, and (iv) a request for a conference with Appeals.",
        "Hazards of litigation assessment -- for each disputed issue, we prepare an internal memorandum assessing the probability of success on the merits, consistent with the hazards-of-litigation framework used by IRS Appeals to evaluate cases.",
    ])

    pdf.subsection_heading("3.2", "90-Day Letter / Statutory Notice of Deficiency")
    pdf.body_text(
        "If the taxpayer does not reach agreement with the IRS at the examination or Appeals level, "
        "the IRS issues a Statutory Notice of Deficiency (90-day letter), which is a prerequisite to "
        "the taxpayer's right to petition the United States Tax Court. Critical considerations include:"
    )
    pdf.bullet_list([
        "Deadline management -- the 90-day filing deadline (150 days for taxpayers outside the United States) is jurisdictional and non-waivable. Failure to file a timely petition results in the deficiency becoming final and assessable. We implement multiple redundant calendar controls to ensure no deadline is missed.",
        "Tax Court petition preparation -- we prepare the petition in compliance with the Tax Court Rules of Practice and Procedure, including the statement of assignments of error and supporting facts.",
        "Forum selection analysis -- evaluation of whether Tax Court is the optimal forum (prepayment forum, but limited discovery and specialized judges) versus filing a refund claim and suit in the Court of Federal Claims or a federal district court (full payment required, but jury trial available in district court and broader discovery rules).",
    ])

    pdf.section_heading("4.", "IRS Appeals Conference")
    pdf.body_text(
        "The IRS Independent Office of Appeals is the administrative forum for resolving tax disputes "
        "without litigation. Our Appeals practice includes:"
    )
    pdf.bullet_list([
        "Pre-conference preparation -- development of a comprehensive Appeals presentation including a legal memorandum, factual exhibits, economic analyses, and expert reports (where applicable).",
        "Hazards-of-litigation negotiation -- engaging with the Appeals Officer on the relative litigation hazards of each issue, leveraging recent case law developments, new factual evidence developed since the examination, and settlement precedents.",
        "Fast Track Settlement -- for cases still in examination, we evaluate whether the IRS Fast Track Settlement (FTS) program or Post-Appeals Mediation (PAM) would be advantageous alternatives to the traditional Appeals process.",
        "Closing agreement negotiation -- when a settlement is reached, we negotiate the terms of the Form 906 closing agreement, ensuring that agreed-upon positions are properly characterized and that the agreement does not create unintended precedent for other tax years or issues.",
    ])

    pdf.section_heading("5.", "Competent Authority Proceedings")
    pdf.body_text(
        "For taxpayers facing double taxation resulting from transfer pricing adjustments or other "
        "cross-border disputes, we represent clients in competent authority proceedings under applicable "
        "income tax treaties. The competent authority process is governed by Article 25 of the OECD "
        "Model Tax Convention (and corresponding bilateral treaty provisions) and Revenue Procedure "
        "2015-40 (for US-initiated requests). Our services include:"
    )
    pdf.bullet_list([
        "Initiation of competent authority request -- preparation and filing of the request with the US Competent Authority (IRS APMA) or the relevant foreign competent authority, within the treaty-prescribed time limits (typically 3 years from the first notification of the action giving rise to double taxation).",
        "Position paper development -- comprehensive analysis demonstrating that the foreign adjustment is inconsistent with the arm's length standard and/or the applicable treaty provisions.",
        "Arbitration provisions -- for treaties containing mandatory binding arbitration provisions (e.g., US-Canada, US-Germany, US-Belgium), advising on the implications of the arbitration clause and preparation for potential arbitration proceedings.",
        "Correlative adjustment implementation -- once agreement is reached, coordinating with both tax authorities to implement the correlative adjustment, including any refunds, additional assessments, and amended return filings.",
    ])

    pdf.section_heading("6.", "Voluntary Disclosure Programs")
    pdf.body_text(
        "Meridian assists taxpayers in making voluntary disclosures to mitigate penalties and potential "
        "criminal exposure for prior non-compliance. Our voluntary disclosure practice covers:"
    )
    pdf.bullet_list([
        "IRS Voluntary Disclosure Practice -- following the updated procedures in IRS Memorandum LB&I-09-1118-014, we prepare preclearance requests and voluntary disclosure submissions for taxpayers with unreported domestic or foreign income, unfiled returns, or other compliance deficiencies.",
        "Streamlined Filing Compliance Procedures -- for taxpayers certifying non-willful failure to report foreign financial accounts or pay tax, the streamlined procedures offer reduced penalties (zero for foreign residents, 5% miscellaneous offshore penalty for domestic filers).",
        "State voluntary disclosure agreements (VDAs) -- negotiation of state VDAs for taxpayers with prior-period income tax, sales tax, or use tax liabilities in states where nexus was established but returns were not filed. VDAs typically provide penalty abatement and a limited lookback period (3-4 years in most states).",
    ])

    pdf.section_heading("7.", "Penalty Abatement Strategies")
    pdf.body_text(
        "We pursue penalty abatement through the following primary arguments:"
    )
    pdf.subsection_heading("7.1", "Reasonable Cause")
    pdf.body_text(
        "Under IRC Section 6664(c), no penalty is imposed under Section 6662 (accuracy-related penalty) "
        "if the taxpayer demonstrates that there was reasonable cause for the underpayment and that the "
        "taxpayer acted in good faith. Factors analyzed include: the nature of the error (computational "
        "vs. interpretive), the taxpayer's compliance history, the complexity of the applicable law, the "
        "taxpayer's reliance on professional advice (satisfying the Neonatology Associates three-prong "
        "test), and the taxpayer's efforts to assess the correct tax liability."
    )
    pdf.subsection_heading("7.2", "Substantial Authority")
    pdf.body_text(
        "For accuracy-related penalties under Section 6662(b)(2) (substantial understatement of income "
        "tax), no penalty applies if the taxpayer had substantial authority for the position. Substantial "
        "authority exists when the weight of authorities supporting the position is substantial in "
        "relation to the contrary authorities, determined by reference to the hierarchy of authority "
        "listed in Treas. Reg. Section 1.6662-4(d)(3)(iii): Internal Revenue Code, regulations, revenue "
        "rulings, revenue procedures, Tax Court and appellate court decisions, legislative history, "
        "private letter rulings, technical advice memoranda, and IRS information releases."
    )
    pdf.subsection_heading("7.3", "Adequate Disclosure")
    pdf.body_text(
        "Alternatively, for non-tax-shelter items, the substantial understatement penalty can be avoided "
        "through adequate disclosure of the position on the tax return (or an attached statement) if "
        "there is a reasonable basis for the position. Disclosure is made on Form 8275 (Disclosure "
        "Statement) or Form 8275-R (for positions contrary to Treasury regulations). We advise clients "
        "on the appropriate use of disclosure as a protective measure for aggressive but defensible "
        "positions."
    )

    pdf.section_heading("8.", "Statute of Limitations Management")
    pdf.body_text(
        "Proper management of the statute of limitations is critical to both the IRS's ability to "
        "assess additional tax and the taxpayer's ability to claim refunds. Key considerations include:"
    )
    pdf.bullet_list([
        "Standard 3-year assessment period (Section 6501(a)) -- beginning on the later of the filing date or the due date of the return.",
        "6-year period for substantial omissions (Section 6501(e)) -- applies when the taxpayer omits more than 25% of gross income from the return. Post-2010 amendments clarify that overstatement of basis can trigger this extended period.",
        "Unlimited period for fraud or failure to file (Section 6501(c)) -- no statute of limitations applies to fraudulent returns or where no return was filed.",
        "Consent to extend (Form 872/872-A) -- we carefully evaluate IRS requests to extend the statute, negotiating restricted consents (limited to specific issues and tax years) and fixed expiration dates rather than open-ended extensions.",
        "Protective refund claims -- filing timely protective refund claims (Form 1120X or informal claim) to preserve the client's right to claim refunds for contingent issues (e.g., pending litigation, Revenue Procedure changes, or Tax Court decisions on appeal).",
    ])

    pdf.save("tax_controversy.pdf")


# ===================================================================
# DOCUMENT 7: Tax Technology & Automation
# ===================================================================

def build_tax_technology():
    pdf = FirmPDF(
        title="Tax Technology & Automation",
        subtitle="Platform Architecture, RPA Implementation & Digital Tax Readiness\nModernizing the Tax Function",
        doc_id="M&A-TAX-TTA-007",
        version="2.5",
        effective_date="March 1, 2026",
    )
    pdf.cover_page()

    pdf.add_page()
    pdf.section_heading("1.", "Executive Summary")
    pdf.body_text(
        "Meridian & Associates' Tax Technology & Automation (TTA) practice helps corporate tax "
        "departments transform their operations through the strategic implementation of tax technology "
        "platforms, robotic process automation (RPA), data analytics, and artificial intelligence. As "
        "tax authorities worldwide accelerate their adoption of digital tax administration -- including "
        "mandatory e-invoicing, real-time reporting, and SAF-T (Standard Audit File for Tax) "
        "requirements -- the imperative for corporate tax functions to modernize has never been greater. "
        "In FY2025, the TTA practice completed 85+ technology implementation engagements, achieving an "
        "average 40% reduction in tax return preparation time and a 55% reduction in manual data entry "
        "for clients adopting our recommended technology stack."
    )
    pdf.body_text(
        "The technology solutions described in this document support and integrate with the firm's "
        "core tax service lines, including global compliance (M&A-TAX-GTC-001), transfer pricing "
        "(M&A-TAX-TPF-002), tax provision (M&A-TAX-PRV-003), M&A due diligence (M&A-TAX-MDD-004), "
        "credits and incentives (M&A-TAX-TCI-005), tax controversy (M&A-TAX-CON-006), SALT "
        "(M&A-TAX-SALT-008), and international tax planning (M&A-TAX-INTL-009)."
    )

    pdf.section_heading("2.", "Core Technology Platform -- Thomson Reuters ONESOURCE")
    pdf.body_text(
        "Thomson Reuters ONESOURCE is the primary compliance and provision technology platform "
        "recommended by Meridian for large multinational tax departments. Our ONESOURCE implementation "
        "practice covers the full platform suite:"
    )
    pdf.subsection_heading("2.1", "ONESOURCE Income Tax")
    pdf.body_text(
        "We implement and optimize ONESOURCE Income Tax for corporate income tax compliance across "
        "US federal, US state and local, and international jurisdictions. Key implementation workstreams "
        "include: chart of accounts mapping and data integration with the client's general ledger and "
        "ERP system, template design and customization, automated workpaper generation, e-filing "
        "configuration, and multi-year migration from legacy platforms (GoSystem, Corptax, CCH Axcess). "
        "Our ONESOURCE Center of Excellence includes 35 certified consultants with an average of 12 "
        "years of implementation experience."
    )
    pdf.subsection_heading("2.2", "ONESOURCE Tax Provision")
    pdf.body_text(
        "ONESOURCE Tax Provision (OTP) automates the ASC 740 quarterly and annual income tax provision "
        "process, including effective tax rate computation, deferred tax roll-forward, return-to-provision "
        "analysis, and financial statement disclosure preparation. We configure OTP to align with the "
        "client's organizational structure (entity-by-entity, consolidated group, or hybrid), establish "
        "automated data feeds from the consolidation system (HFM, OneStream, SAP BPC), and design "
        "custom reports and dashboards for the VP of Tax and CFO. Post-implementation, we provide "
        "annual update and optimization services covering new legislation, rate changes, and M&A "
        "structural changes."
    )
    pdf.subsection_heading("2.3", "ONESOURCE DataFlow")
    pdf.body_text(
        "DataFlow serves as the data integration layer connecting the client's ERP, general ledger, and "
        "other source systems to ONESOURCE Income Tax and Tax Provision. We design and implement "
        "DataFlow extraction, transformation, and loading (ETL) routines that automate the mapping of "
        "GL accounts to tax return line items, reducing manual data entry by 80-90% for clients with "
        "well-structured ERP data. Our implementation methodology includes data quality assessment, "
        "reconciliation checkpoint design, and exception handling workflows."
    )

    pdf.section_heading("3.", "Indirect Tax -- Vertex Tax Engine")
    pdf.body_text(
        "For indirect tax (sales and use tax, VAT, GST) automation, we implement and configure the "
        "Vertex O Series and Vertex Cloud platforms. Our Vertex practice addresses:"
    )
    pdf.bullet_list([
        "Tax determination engine integration -- embedding Vertex's real-time tax calculation engine into the client's order-to-cash and procure-to-pay processes via SAP, Oracle, Salesforce, or custom API integration.",
        "Product taxability mapping -- classification of the client's products and services under Vertex's commodity taxonomy, including analysis of exemptions, reduced rates, and jurisdiction-specific rules.",
        "Exemption certificate management -- implementation of Vertex's exemption certificate module (or integration with CertCapture/Avalara) to automate the collection, validation, and renewal of customer exemption certificates.",
        "Returns automation -- configuration of Vertex Returns for automated preparation and e-filing of sales and use tax returns across all applicable jurisdictions, including reconciliation to GL and Vertex transaction data.",
        "Global indirect tax -- for multinational clients, implementation of Vertex's O Series for global VAT/GST determination, supporting compliance with EU VAT Directive, UK MTD (Making Tax Digital), and other international indirect tax requirements.",
    ])

    pdf.section_heading("4.", "Data Transformation -- Alteryx")
    pdf.body_text(
        "Alteryx Designer and Alteryx Server are deployed as the primary data transformation and "
        "analytics platform for tax data preparation workflows. Common Alteryx use cases in the "
        "tax function include:"
    )
    pdf.bullet_list([
        "Trial balance normalization -- transforming raw GL trial balance exports from multiple ERP instances into a standardized format for import into ONESOURCE or provision workpapers.",
        "Fixed asset analysis -- processing large fixed asset registers (100,000+ assets) for depreciation schedule computation, cost segregation reclassification, and Section 168 bonus depreciation optimization.",
        "R&D credit documentation -- automated extraction and analysis of project time-tracking data, payroll records, and contractor invoices to identify and quantify qualified research expenditures.",
        "State apportionment factor computation -- automated compilation of sales, payroll, and property factors from multiple source systems, including market-based sourcing analysis for service and intangible income.",
        "Transfer pricing benchmarking data preparation -- extraction and cleaning of comparable company data from Orbis/TP Catalyst for TNMM analysis.",
        "M&A due diligence data analysis -- rapid analysis of target company trial balances, fixed asset registers, and intercompany transaction logs during the compressed due diligence timeline.",
    ])
    pdf.body_text(
        "Our Alteryx Center of Excellence maintains a library of 200+ reusable workflow templates "
        "covering common tax data preparation scenarios, reducing implementation time for new client "
        "deployments by 50-60%."
    )

    pdf.section_heading("5.", "Tax Dashboards -- Power BI")
    pdf.body_text(
        "We design and deploy Microsoft Power BI dashboards for tax department performance management "
        "and executive reporting. Standard dashboard packages include:"
    )
    pdf.bullet_list([
        "Global Tax Compliance Dashboard -- real-time visibility into filing status, deadlines, reviewer assignments, and extension tracking across all jurisdictions. Color-coded status indicators (green/yellow/red) with drill-down capability to individual entity and return level.",
        "Effective Tax Rate Dashboard -- visual ETR bridge analysis (waterfall chart from statutory rate to effective rate), trend analysis across quarters, and variance commentary. Enables the VP of Tax to explain ETR movements to the CFO and Audit Committee in real time.",
        "Tax Controversy Tracker -- status of all open audits, appeals cases, and refund claims, including aging analysis, exposure quantification, and reserve adequacy monitoring.",
        "Transfer Pricing Monitoring Dashboard -- comparison of actual intercompany transaction results against benchmarked arm's length ranges, with automated exception alerts when results fall outside the interquartile range.",
        "Tax Credit and Incentive Tracker -- consolidated view of all claimed and available tax credits and incentives, including compliance milestone tracking, expiration dates, and projected cash flow impact.",
    ])

    pdf.section_heading("6.", "Robotic Process Automation (RPA)")
    pdf.subsection_heading("6.1", "RPA for Return Assembly")
    pdf.body_text(
        "Our RPA practice leverages UiPath and Microsoft Power Automate to automate repetitive, "
        "rules-based tasks in the tax compliance process. The flagship use case -- automated return "
        "assembly -- has achieved an average 40% reduction in tax return preparation time across 120+ "
        "client implementations. The return assembly bot performs the following tasks:"
    )
    pdf.bullet_list([
        "Extraction of trial balance data from the ERP system and population into the tax compliance workpapers.",
        "Automated workpaper cross-referencing -- linking supporting schedules to return line items and flagging discrepancies.",
        "PDF assembly -- compiling the final return package including the signed return, supporting schedules, state apportionment worksheets, election statements, and disclosure forms.",
        "Filing checklist automation -- populating filing checklists with return data, generating quality review prompts, and routing for electronic approval.",
        "E-filing submission -- automated submission of completed returns to the IRS Modernized e-File (MeF) system and state e-filing portals.",
    ])

    pdf.subsection_heading("6.2", "Additional RPA Use Cases")
    pdf.body_text("Beyond return assembly, we have implemented RPA solutions for:")
    pdf.bullet_list([
        "Notices and correspondence processing -- automated extraction of data from IRS and state tax authority notices (CP2000, balance due notices, penalty assessments), classification by issue type, and routing to the appropriate engagement team.",
        "Sales tax exemption certificate processing -- automated validation of certificate completeness, expiration date monitoring, and renewal request generation.",
        "Withholding tax reclaim processing -- automated preparation of reclaim forms for excess withholding on cross-border payments (dividends, interest, royalties) under applicable tax treaties.",
        "Estimated tax payment monitoring -- automated tracking of federal and state estimated tax payment deadlines, computation of required installments (Section 6655 safe harbor calculations), and payment initiation through the client's treasury system.",
    ])

    pdf.section_heading("7.", "AI-Assisted Tax Research")
    pdf.body_text(
        "Meridian has developed and deployed AI-powered tax research tools that augment the "
        "capabilities of our tax professionals:"
    )
    pdf.bullet_list([
        "Meridian TaxAI Research Assistant -- a large language model fine-tuned on Meridian's proprietary knowledge base of 50,000+ technical memoranda, tax court decisions, IRS guidance documents, and engagement work products. The assistant provides natural-language responses to complex tax research questions, with citations to primary authority, and is available to all Meridian tax professionals through a secure internal portal.",
        "Automated authority monitoring -- AI-powered scanning of daily tax developments (legislation, regulations, rulings, decisions) with automated classification by topic, jurisdiction, and client impact. High-impact developments trigger automated alerts to relevant engagement teams.",
        "Predictive audit analytics -- machine learning models trained on historical audit data to predict audit selection risk, IRS focus areas, and likely proposed adjustment amounts, enabling proactive audit preparation and reserve optimization.",
        "Document review acceleration -- AI-assisted review of transaction documents (intercompany agreements, M&A purchase agreements, loan documents) to extract key tax terms and flag potential issues, reducing manual review time by 60-70%.",
    ])

    pdf.section_heading("8.", "Digital Tax Administration Readiness")
    pdf.subsection_heading("8.1", "E-Invoicing Mandates")
    pdf.body_text(
        "Governments worldwide are rapidly implementing mandatory electronic invoicing (e-invoicing) "
        "and real-time transaction reporting. As of early 2026, e-invoicing is mandatory in over 50 "
        "jurisdictions including Mexico (CFDI), Brazil (NF-e), Italy (SDI), India (e-Invoice), Saudi "
        "Arabia (ZATCA/Fatoora), and the EU (ViDA -- VAT in the Digital Age, phased implementation "
        "2028-2032). Our e-invoicing readiness assessment covers:"
    )
    pdf.bullet_list([
        "Gap analysis -- comparison of the client's current invoicing process against the technical and format requirements of each applicable mandate (Peppol BIS, UBL 2.1, CII Cross Industry Invoice, country-specific schemas).",
        "Platform selection -- evaluation of e-invoicing platforms (Sovos, Pagero/Thomson Reuters, Avalara, Comarch, SAP Document Compliance) based on geographic coverage, ERP integration capabilities, and scalability.",
        "Implementation roadmap -- phased deployment plan prioritized by mandate effective dates and penalty severity, with integration to the client's ERP and Vertex/ONESOURCE indirect tax engine.",
        "Ongoing compliance monitoring -- continuous monitoring of regulatory changes and platform updates to ensure sustained compliance as mandates evolve.",
    ])

    pdf.subsection_heading("8.2", "ERP Integration Architecture")
    pdf.body_text(
        "The effectiveness of any tax technology solution depends on seamless integration with the "
        "client's enterprise systems. Our integration architecture practice designs and implements "
        "connections between:"
    )
    pdf.bullet_list([
        "ERP to tax compliance -- real-time or batch data flows from SAP S/4HANA, Oracle Cloud, Microsoft Dynamics 365, or Workday Financials to ONESOURCE, Vertex, and other tax engines.",
        "Tax compliance to financial reporting -- automated journal entry generation from tax provision calculations, with posting to the GL and consolidation system.",
        "Tax to treasury -- integration of estimated tax payment schedules, refund tracking, and tax cash flow forecasts into the client's treasury management system (Kyriba, FIS, ION).",
        "Document management -- centralized storage of tax returns, workpapers, election statements, and correspondence in the client's document management system (SharePoint, OpenText, iManage) with appropriate access controls and retention policies.",
    ])
    pdf.body_text(
        "All integrations follow our standardized API-first architecture, leveraging RESTful APIs and "
        "middleware platforms (MuleSoft, Dell Boomi, Microsoft Azure Integration Services) to ensure "
        "scalability, auditability, and maintainability. Each integration includes comprehensive error "
        "handling, reconciliation checkpoints, and automated monitoring with alerting. All tax "
        "technology implementations adhere to the firm's information security standards (see "
        "common_firm_wide/infosec_overview.pdf) and client data handling policies (see "
        "common_firm_wide/data_privacy_policy.pdf)."
    )

    pdf.save("tax_technology_automation.pdf")


# ===================================================================
# DOCUMENT 8: State and Local Tax (SALT) Methodology
# ===================================================================

def build_salt_methodology():
    pdf = FirmPDF(
        title="State and Local Tax Services",
        subtitle="Nexus Analysis, Apportionment Planning, Sales & Use Tax,\nProperty Tax, and State Controversy Practice Guide",
        doc_id="M&A-TAX-SALT-008",
        version="3.0",
        effective_date="March 1, 2026",
    )
    pdf.cover_page()

    # --- Section 1 ---
    pdf.add_page()
    pdf.section_heading("1.", "Executive Summary")
    pdf.body_text(
        "Meridian & Associates LLP's State and Local Tax (SALT) practice assists multistate "
        "businesses in navigating the increasingly complex patchwork of state and local tax "
        "obligations across all 50 states, the District of Columbia, and U.S. territories. The "
        "SALT landscape has undergone a fundamental transformation following the U.S. Supreme "
        "Court's 2018 decision in South Dakota v. Wayfair, Inc. (585 U.S. 162), which eliminated "
        "the physical presence requirement for sales tax nexus and opened the door for states to "
        "assert economic nexus based on sales volume and transaction thresholds."
    )
    pdf.body_text(
        "Our SALT practice encompasses six core service lines: multistate income and franchise "
        "tax, sales and use tax, property tax, unclaimed property, state tax controversy, and "
        "state tax technology. The practice is staffed by 85 professionals, including 12 partners, "
        "and serves over 400 clients ranging from mid-market companies with operations in 5-10 "
        "states to Fortune 100 multinationals with nexus obligations in all 50 states."
    )

    # --- Section 2 ---
    pdf.section_heading("2.", "Multistate Income and Franchise Tax")
    pdf.subsection_heading("2.1", "Nexus Analysis Framework")
    pdf.body_text(
        "Nexus -- the minimum connection a business must have with a state before that state can "
        "impose its tax -- is the threshold question in multistate taxation. Meridian's nexus "
        "analysis evaluates each client's activities against three nexus frameworks:"
    )
    pdf.bullet_list([
        "Physical Presence Nexus: Employees, offices, warehouses, inventory, equipment, or agents located in the state. Even temporary presence (trade shows, installation crews, remote employees) can create nexus in many states.",
        "Economic Nexus (Post-Wayfair): Revenue or transaction thresholds that trigger nexus regardless of physical presence. Thresholds vary by state; common standards include $100,000 in sales or 200 transactions (the Wayfair safe harbor), though several states have adopted lower thresholds or eliminated the transaction count test.",
        "Factor Presence Nexus: Some states (e.g., California, New York, Michigan) apply income tax economic nexus based on a threshold level of property, payroll, or sales in the state, independent of the Wayfair sales tax framework.",
    ])
    pdf.body_text(
        "For businesses engaged in interstate sales of services or intangibles, Meridian evaluates "
        "the applicability of Public Law 86-272 (15 U.S.C. 381-384), which prohibits states from "
        "imposing net income taxes on businesses whose only in-state activity is the solicitation "
        "of orders for sales of tangible personal property. Importantly, P.L. 86-272 does not "
        "protect against franchise taxes, gross receipts taxes, or sales taxes, and the Multistate "
        "Tax Commission's revised interpretation (adopted in 2021) significantly narrows protection "
        "for businesses with internet-based activities, including cookie placement, app-based "
        "interactions, and marketplace facilitation."
    )

    pdf.subsection_heading("2.2", "Apportionment Planning")
    pdf.body_text(
        "Once nexus is established, the next critical question is how much income a state may tax. "
        "Most states use an apportionment formula to allocate a company's total taxable income "
        "among the states where it has nexus. Meridian's apportionment planning services include:"
    )
    pdf.bullet_list([
        "Formula Analysis: Evaluating each state's apportionment formula (single sales factor, three-factor with double-weighted sales, equally weighted three-factor, or cost-of-performance vs. market-based sourcing for services and intangibles).",
        "Sales Factor Optimization: Structuring intercompany transactions, supply chain configurations, and customer billing entities to minimize the sales factor numerator in high-tax states while preserving economic substance.",
        "Throwback and Throwout Rules: Identifying states with throwback rules (which reassign 'nowhere sales' to the state of origin) and evaluating strategies to minimize their impact, including establishing nexus in destination states to avoid throwback.",
        "Alternative Apportionment: Petitioning states for relief under UDITPA Section 18 or state equivalents when the standard formula does not fairly represent the taxpayer's business activity in the state.",
    ])

    pdf.subsection_heading("2.3", "Combined and Unitary Reporting")
    pdf.body_text(
        "Approximately 28 states require or permit combined or unitary reporting, which requires "
        "related entities engaged in a unitary business to file a combined return. Meridian assists "
        "clients with:"
    )
    pdf.bullet_list([
        "Unitary Business Determination: Applying the three-unities test (unity of ownership, operation, and use) and the contribution-dependency test to determine which entities must be included in the combined group.",
        "Water's Edge vs. Worldwide Election: Evaluating whether a water's-edge election (limiting the combined group to domestic entities and certain tax-haven entities) is more beneficial than worldwide combined reporting.",
        "Intercompany Eliminations: Ensuring proper elimination of intercompany transactions within the combined group while preserving the integrity of entity-level apportionment factors.",
        "Joyce vs. Finnigan Rules: Analyzing whether the state applies the Joyce rule (only entities with nexus must include their sales in the apportionment formula) or the Finnigan rule (all entities in the combined group include their sales), which can materially affect the combined sales factor.",
    ])

    # --- Section 3 ---
    pdf.section_heading("3.", "Sales and Use Tax")
    pdf.subsection_heading("3.1", "Compliance Services")
    pdf.body_text(
        "Meridian's sales and use tax compliance practice manages over 12,000 monthly state and "
        "local filings for clients across retail, manufacturing, technology, and financial services "
        "sectors. Our compliance services are supported by Vertex O Series and Avalara AvaTax "
        "technology platforms, with Meridian teams providing oversight, exception management, and "
        "jurisdiction research."
    )
    pdf.bullet_list([
        "Taxability Matrix Maintenance: Maintaining up-to-date taxability determinations for each client's product and service catalog across all jurisdictions. The matrix is reviewed quarterly for legislative changes and updated in real time for audit-driven reclassifications.",
        "Exemption Certificate Management: Centralized collection, validation, storage, and renewal tracking of exemption and resale certificates using Avalara CertCapture or in-house solutions.",
        "Streamlined Sales Tax (SST) Compliance: For clients operating in SST member states, leveraging certified service provider (CSP) arrangements to simplify multi-state compliance.",
        "Marketplace Facilitator Compliance: Advising marketplace sellers and facilitators on evolving state-by-state facilitator obligations, collection responsibilities, and reporting requirements.",
    ])

    pdf.subsection_heading("3.2", "Audit Defense")
    pdf.body_text(
        "Meridian's SALT controversy team represents clients in sales and use tax audits conducted "
        "by state and local taxing authorities. Our audit defense methodology includes:"
    )
    pdf.bullet_list([
        "Pre-Audit Preparation: Conducting an internal pre-audit review (reverse audit) to identify and quantify potential exposures before the state audit commences, including a review of exemption certificate files, taxability determinations, and use tax accrual procedures.",
        "Audit Management: Serving as the primary point of contact with the auditor, managing information requests, reviewing sampling methodologies, negotiating sample periods and populations, and challenging inappropriate extrapolations.",
        "Refund Identification: During the audit process, identifying overpayments and credit opportunities that partially or fully offset assessed deficiencies.",
        "Appeals and Settlement: Representing clients at informal conferences, formal administrative hearings, and state tax tribunal proceedings. Our track record shows an average 45% reduction in assessed deficiencies through the appeals process.",
    ])

    # --- Section 4 ---
    pdf.section_heading("4.", "Property Tax Consulting")
    pdf.body_text(
        "Property tax is the largest source of local government revenue and represents a significant "
        "cost for clients with substantial real estate holdings, manufacturing facilities, and "
        "capital-intensive operations. Meridian's property tax practice provides:"
    )
    pdf.bullet_list([
        "Valuation Review and Appeals: Reviewing assessed valuations of real property, personal property (machinery, equipment, fixtures), and business personal property. We file assessment appeals in jurisdictions where valuations exceed fair market value, achieving an average 12-18% reduction in assessed value for contested properties.",
        "Rendering and Compliance: Preparing and filing annual personal property renditions (declarations) in all jurisdictions with tangible personal property tax obligations. Our rendering process includes asset-by-asset review for obsolescence, reclassification to lower-taxed categories, and identification of assets eligible for exemption.",
        "Tax Abatement and Incentive Negotiation: Negotiating property tax abatements, tax increment financing (TIF), Payment in Lieu of Taxes (PILOT), and enterprise zone benefits for new facilities, expansions, and corporate relocations.",
        "Audit Defense: Representing clients in property tax audits, including defending depreciation schedules, cost basis allocations, and business personal property valuations.",
    ])

    # --- Section 5 ---
    pdf.section_heading("5.", "Unclaimed Property")
    pdf.body_text(
        "Unclaimed property (escheat) compliance is an often-overlooked obligation that carries "
        "significant financial exposure. Most states require holders to report and remit unclaimed "
        "property -- including uncashed checks, dormant bank accounts, unredeemed gift cards, "
        "outstanding credits, and uncashed payroll -- after a specified dormancy period (typically "
        "3-5 years). Meridian's unclaimed property services include:"
    )
    pdf.bullet_list([
        "Compliance Reviews: Evaluating the completeness and accuracy of existing unclaimed property reporting across all 50 states, identifying unreported property types and miscalculated dormancy periods.",
        "Voluntary Disclosure Agreements (VDAs): Negotiating VDAs with state unclaimed property administrators to resolve historical non-compliance. VDAs typically limit the look-back period (often to 10 years vs. an unlimited look-back in audit) and waive interest and penalties.",
        "Audit Defense: Representing clients in unclaimed property examinations conducted by state-contracted auditors (e.g., Kelmar, Verus Financial). Our approach includes challenging estimation methodologies, negotiating scope limitations, and leveraging VDA programs where available.",
        "Policy and Process Design: Implementing internal policies and system configurations to prevent future unclaimed property accumulation, including automatic payment clearing, regular customer outreach, and systematic dormancy monitoring.",
    ])

    # --- Section 6 ---
    pdf.section_heading("6.", "Pass-Through Entity (PTE) Elections")
    pdf.body_text(
        "In response to the $10,000 federal limitation on individual state and local tax (SALT) "
        "deductions imposed by the Tax Cuts and Jobs Act of 2017 (Section 164(b)(6)), more than "
        "35 states have enacted PTE election or PTE tax regimes. These regimes allow partnerships "
        "and S corporations to elect to pay state income tax at the entity level, generating a "
        "federal income tax deduction that effectively circumvents the SALT cap for the entity's "
        "owners."
    )
    pdf.body_text(
        "Meridian assists clients with PTE election analysis, including:"
    )
    pdf.bullet_list([
        "Multi-State Modeling: Modeling the federal and state tax impact of PTE elections across all states where the entity files, considering interactions between states (e.g., credit mechanisms for tax paid to other states), the entity's owner composition (individuals, trusts, corporations, tax-exempt entities), and the effect on estimated tax payments.",
        "Election Mechanics: Navigating the procedural requirements for each state's PTE election, including election timing, irrevocability provisions, estimated payment requirements, and composite return filing obligations.",
        "IRS Notice 2020-75 Compliance: Ensuring PTE tax payments are properly characterized as entity-level deductions for federal income tax purposes in accordance with proposed regulations under Section 164.",
        "Owner-Level Credit Coordination: Assisting individual owners in claiming state tax credits for PTE taxes paid on their behalf, including coordination of credits across multiple states and resolution of credit-stacking issues.",
    ])

    # --- Section 7 ---
    pdf.section_heading("7.", "State Tax Controversy and Voluntary Disclosure")
    pdf.body_text(
        "Meridian's state tax controversy practice handles disputes at every stage of the state "
        "tax lifecycle -- from audit defense through administrative appeals to state court "
        "litigation. Our controversy services include:"
    )
    pdf.bullet_list([
        "Audit Defense and Management: Representing clients in income, franchise, sales/use, and gross receipts tax audits conducted by state departments of revenue.",
        "Administrative Appeals: Preparing and arguing appeals before state administrative hearing bodies, including the California Office of Tax Appeals (OTA), New York Division of Tax Appeals, Texas Comptroller Administrative Hearings, and equivalent bodies in all 50 states.",
        "Voluntary Disclosure Agreements: Negotiating VDAs with state tax authorities for clients with unaddressed nexus obligations. VDAs typically provide a limited look-back period (typically 3-4 years), waiver of penalties, and in some cases reduced interest.",
        "Multistate Tax Commission (MTC) Nexus Program: Utilizing the MTC's National Nexus Program to efficiently negotiate simultaneous VDAs with multiple states through a single process.",
        "Tax Court and State Court Litigation: Engaging experienced state tax litigation counsel (from Meridian's Legal Services network) to pursue judicial remedies when administrative processes are exhausted or constitutional challenges are warranted.",
        "Amnesty Program Monitoring: Tracking and advising clients on state tax amnesty programs, which periodically offer penalty and/or interest abatement for voluntary payment of back taxes.",
    ])

    pdf.save("salt_methodology.pdf")


# ===================================================================
# DOCUMENT 9: International Tax Planning
# ===================================================================

def build_international_tax_planning():
    pdf = FirmPDF(
        title="International Tax Planning Advisory",
        subtitle="Subpart F, GILTI, FTC Optimization, Treaty Planning,\nand Post-TCJA International Structuring",
        doc_id="M&A-TAX-INTL-009",
        version="2.5",
        effective_date="February 15, 2026",
    )
    pdf.cover_page()

    # --- Section 1 ---
    pdf.add_page()
    pdf.section_heading("1.", "Executive Summary")
    pdf.body_text(
        "Meridian & Associates LLP's International Tax practice advises multinational enterprises "
        "on the tax-efficient structuring of global operations in an environment transformed by the "
        "Tax Cuts and Jobs Act (TCJA) of 2017, the OECD's BEPS 2.0 framework (Pillar One and "
        "Pillar Two), and the proliferation of anti-avoidance regimes worldwide. Our international "
        "tax team comprises 120 professionals across 14 offices, including 18 partners with an "
        "average of 22 years of cross-border tax experience."
    )
    pdf.body_text(
        "This document describes our core international tax advisory services, methodologies, and "
        "planning frameworks. All planning recommendations adhere to the firm's Tax Risk Policy, "
        "which requires a 'more likely than not' (MLTN) or higher confidence level for positions "
        "taken on filed returns and a 'should' level of confidence for affirmative planning "
        "recommendations. Aggressive or abusive tax positions are prohibited regardless of client "
        "request."
    )

    # --- Section 2 ---
    pdf.section_heading("2.", "Subpart F and GILTI Planning")
    pdf.subsection_heading("2.1", "Subpart F Income Analysis")
    pdf.body_text(
        "Subpart F (Sections 951-964 of the Internal Revenue Code) requires U.S. shareholders of "
        "controlled foreign corporations (CFCs) to include certain categories of income currently "
        "in their U.S. taxable income, regardless of whether the income is distributed. Meridian's "
        "Subpart F planning encompasses:"
    )
    pdf.bullet_list([
        "Foreign Base Company Income (FBCI) Classification: Analyzing CFC income streams to determine which items constitute foreign base company sales income (Section 954(d)), foreign base company services income (Section 954(e)), or foreign personal holding company income (FPHCI) under Section 954(c). Particular attention is given to the 'same country of incorporation' exceptions that can exclude sales and services income from FBCI.",
        "High-Tax Exception: Evaluating whether CFC income qualifies for the high-tax exception under Section 954(b)(4), which excludes items of income subject to an effective foreign tax rate greater than 90% of the maximum U.S. corporate rate (currently 18.9%). This analysis is performed on an item-by-item basis as required by the regulations.",
        "Active Trade or Business Exception: Structuring CFC operations to maximize qualification for the Section 954(h) active financing exception (for financial services income) and the Section 954(i) active insurance exception.",
        "Same Country Exceptions: Structuring supply chains so that CFC purchases from and sales to related parties involve property manufactured, produced, grown, or extracted in the CFC's country of incorporation, thereby qualifying for the same-country exception to FBCI sales income.",
    ])

    pdf.subsection_heading("2.2", "GILTI Planning")
    pdf.body_text(
        "The Global Intangible Low-Taxed Income (GILTI) regime (Section 951A) imposes current "
        "U.S. taxation on CFC earnings exceeding a deemed return on tangible assets (QBAI). "
        "Meridian's GILTI planning focuses on:"
    )
    pdf.bullet_list([
        "QBAI Maximization: Advising clients on locating tangible depreciable assets in high-return CFCs to increase the QBAI offset, which excludes 10% of QBAI from the GILTI inclusion. This includes evaluating lease-vs.-buy decisions, contract manufacturing arrangements, and capital investment timing.",
        "Tested Income and Tested Loss Netting: Structuring the CFC group to maximize the netting of tested income against tested losses from CFCs with net losses, reducing the aggregate GILTI inclusion. This may involve entity rationalization, check-the-box elections, or merger of high-income and loss-making CFCs.",
        "Section 250 Deduction: Calculating the Section 250 GILTI deduction. For tax years beginning after December 31, 2025, the GILTI deduction rate has decreased from 50% to 37.5% under IRC Section 250(a)(3). The taxable income limitation can further reduce or eliminate the deduction.",
        "GILTI High-Tax Exclusion (HTE): Evaluating whether specific CFCs or tested units qualify for the GILTI HTE under Treasury Regulation 1.951A-2(c)(7), which excludes CFC income items subject to a foreign effective tax rate exceeding 18.9% (90% of the U.S. corporate rate).",
        "Interaction with Pillar Two: Modeling the interaction between GILTI and the OECD Pillar Two GloBE rules to identify jurisdictions where the GILTI inclusion may already satisfy the 15% minimum effective tax rate, and where additional top-up taxes may apply.",
    ])

    # --- Section 3 ---
    pdf.section_heading("3.", "Section 245A Dividends Received Deduction")
    pdf.body_text(
        "Section 245A provides a 100% dividends received deduction (DRD) for the foreign-source "
        "portion of dividends received by domestic corporations from specified 10%-owned foreign "
        "corporations (SFCs). Meridian advises clients on:"
    )
    pdf.bullet_list([
        "Dividend Planning: Timing and structuring repatriation transactions to maximize the Section 245A DRD, including coordination with foreign withholding tax obligations and foreign tax credit considerations.",
        "Hybrid Transaction Rules: Navigating the anti-hybrid provisions of Section 245A(e), which deny the DRD for dividends funded by deductible payments (hybrid dividends). Identification of instruments and arrangements that may trigger hybrid dividend treatment.",
        "Extraordinary Disposition Exception: Evaluating the Section 245A(e)(3) extraordinary disposition rules that can reduce or deny the DRD for gains attributable to CFC property disposed of during a specified period.",
        "Coordination with PTEP: Coordinating Section 245A planning with previously taxed earnings and profits (PTEP) distributions under Section 959, which are excluded from gross income but do not generate the Section 245A DRD.",
    ])

    # --- Section 4 ---
    pdf.section_heading("4.", "Foreign Tax Credit Optimization")
    pdf.subsection_heading("4.1", "Section 904 Basket Analysis")
    pdf.body_text(
        "The foreign tax credit (FTC) limitation under Section 904 restricts the FTC to the U.S. "
        "tax attributable to foreign-source income in each separate limitation category (basket). "
        "Meridian's FTC optimization services include:"
    )
    pdf.bullet_list([
        "Basket Classification: Classifying income and creditable taxes into the applicable Section 904(d) baskets: general category, passive category, GILTI basket, foreign branch basket, and Section 901(j) sanctioned country basket.",
        "Cross-Crediting Analysis: Identifying opportunities for cross-crediting within baskets -- i.e., using excess FTCs from high-tax jurisdictions against FTC capacity from low-tax jurisdictions within the same basket category.",
        "Expense Apportionment: Optimizing the apportionment and allocation of deductions (including interest expense under Section 861 and stewardship expenses) between U.S.-source and foreign-source income to maximize the Section 904 limitation.",
        "FTC Carryback and Carryforward: Tracking FTC carryover positions (one-year carryback and ten-year carryforward under Section 904(c)) and modeling the utilization timeline under various planning scenarios.",
    ])

    pdf.subsection_heading("4.2", "High-Tax Exclusion and Credits")
    pdf.body_text(
        "Meridian evaluates the interaction between the various high-tax exclusion and exception "
        "provisions to determine the optimal treatment of high-taxed foreign income:"
    )
    pdf.bullet_list([
        "Subpart F High-Tax Exception (Section 954(b)(4)): Excludes high-taxed items from Subpart F income, allowing them to be deferred until actual repatriation (but subject to GILTI inclusion).",
        "GILTI High-Tax Exclusion (Reg. 1.951A-2(c)(7)): Excludes high-taxed CFC income from GILTI, which can be beneficial when the foreign effective tax rate exceeds the U.S. effective rate on GILTI inclusions.",
        "Section 960 Deemed Paid Credits: Computing deemed-paid FTCs associated with Subpart F, GILTI, and PTEP distributions, including the 80% haircut on GILTI deemed-paid credits under Section 960(d).",
        "Treaty-Based FTC: Evaluating treaty provisions that may provide enhanced FTC benefits, including specific treaty articles addressing the creditability of foreign taxes.",
    ])

    # --- Section 5 ---
    pdf.section_heading("5.", "Treaty Planning and Holding Company Structures")
    pdf.subsection_heading("5.1", "Treaty Network Optimization")
    pdf.body_text(
        "Meridian advises clients on leveraging the U.S. income tax treaty network (currently "
        "65+ treaties) and foreign treaty networks to reduce withholding taxes on cross-border "
        "payments and resolve double taxation. Our treaty planning services include:"
    )
    pdf.bullet_list([
        "Withholding Tax Reduction: Structuring intercompany dividends, interest, and royalty payments to take advantage of reduced treaty withholding rates. Analysis includes evaluation of Limitation on Benefits (LOB) articles and principal purpose test (PPT) requirements.",
        "Treaty Shopping Prevention: Ensuring that treaty-based structures satisfy substance, LOB, and anti-conduit requirements to withstand challenge by tax authorities. Post-BEPS, we evaluate the impact of the Multilateral Instrument (MLI) on applicable treaties.",
        "Permanent Establishment (PE) Risk Assessment: Evaluating client activities in treaty jurisdictions to determine whether a PE exists under the applicable treaty's PE article, including the impact of Article 12 (Services PE) provisions in certain treaties.",
        "Competent Authority Assistance: Engaging in mutual agreement procedure (MAP) and competent authority proceedings to resolve double taxation arising from transfer pricing adjustments, PE attributions, and treaty interpretation disputes.",
    ])

    pdf.subsection_heading("5.2", "Holding Company Jurisdiction Selection")
    pdf.body_text(
        "The selection of a holding company jurisdiction is a critical structural decision with "
        "implications for withholding taxes, capital gains taxation, CFC status, and Pillar Two "
        "compliance. Meridian evaluates jurisdictions across multiple criteria:"
    )
    pdf.bullet_list([
        "Tax Attributes: Participation exemption for dividends and capital gains, breadth and quality of the treaty network, absence of CFC rules (or favorable CFC exemptions), withholding tax rates on outbound payments, and availability of advance ruling or tax ruling procedures.",
        "Substance Requirements: Post-BEPS requirements for economic substance, including minimum staffing, local decision-making, and adequate operational expenditure in the holding company jurisdiction.",
        "Popular Holding Jurisdictions: Netherlands (participation exemption, extensive treaty network, innovation box), Luxembourg (SOPARFI regime, IP box), Ireland (12.5% rate, extensive treaty network, transitioning to Pillar Two), Singapore (territorial system, broad treaty network, IP development incentives), and Switzerland (reduced cantonal rates, R&D super-deductions).",
        "Pillar Two Considerations: Evaluating the impact of the 15% GloBE minimum tax on the effectiveness of holding company jurisdictions with low effective tax rates, and modeling top-up tax exposure under IIR, UTPR, and QDMTT mechanisms.",
    ])

    # --- Section 6 ---
    pdf.section_heading("6.", "IP Migration and Intangible Property Planning")
    pdf.body_text(
        "Intangible property (IP) -- including patents, trade secrets, software, trademarks, and "
        "know-how -- is the most valuable and mobile asset class for many multinationals. Meridian "
        "advises on the tax-efficient location and transfer of IP, balancing tax benefits against "
        "regulatory, operational, and reputational considerations."
    )
    pdf.bullet_list([
        "Cost Sharing Arrangements (CSAs): Structuring qualified cost sharing arrangements under Section 482 and Treasury Regulation 1.482-7, including platform contribution transaction (PCT) analysis, calculation of buy-in payments, and ongoing cost sharing allocation methodologies.",
        "IP Licensing vs. Transfer: Evaluating the tax consequences of outbound IP transfers (Section 367(d) annual inclusions vs. Section 482 commensurate-with-income adjustments) compared to ongoing licensing arrangements, considering the impact on Subpart F, GILTI, and FDII calculations.",
        "FDII Incentive: Modeling the Foreign-Derived Intangible Income (FDII) deduction under Section 250. For tax years beginning after December 31, 2025, the FDII deduction rate has decreased from 37.5% to 21.875% under IRC Section 250(a)(3). Clients retaining IP in the United States and earning foreign-derived income should evaluate FDII as an alternative to offshore IP migration.",
        "Valuation: Engaging Meridian's Transfer Pricing and Valuation specialists to prepare arm's length valuations of transferred IP using income, market, and cost approaches consistent with Section 482 and OECD Transfer Pricing Guidelines Chapter VI.",
    ])

    # --- Section 7 ---
    pdf.section_heading("7.", "Anti-Inversion Rules and Check-the-Box Planning")
    pdf.subsection_heading("7.1", "Section 7874 Anti-Inversion Rules")
    pdf.body_text(
        "Section 7874 imposes adverse tax consequences on certain corporate transactions (inversions) "
        "in which a U.S. corporation becomes a subsidiary of a foreign corporation, or a foreign "
        "corporation acquires substantially all of the properties of a U.S. corporation or "
        "partnership. Meridian advises clients on:"
    )
    pdf.bullet_list([
        "Ownership Continuity Analysis: Calculating the percentage of stock of the foreign acquiring corporation held by former shareholders/partners of the domestic entity. If this percentage is 80% or more, the foreign corporation is treated as a domestic corporation. If between 60% and 80%, the inversion gain provisions of Section 7874(a) apply.",
        "Substantial Business Activities Test: Evaluating whether the foreign acquiring corporation has substantial business activities in its country of organization (the 25% safe harbor under Treasury Regulation 1.7874-3), which can exempt the transaction from inversion treatment.",
        "Serial Inversions and Anti-Stuffing Rules: Advising on the anti-stuffing rules that prevent taxpayers from artificially inflating the value of the foreign acquiring corporation to reduce the ownership percentage below the 60% or 80% thresholds.",
        "Domestic Entity Acquisitions: Evaluating the Section 7874 implications of cross-border M&A transactions, including mergers, stock acquisitions, and asset acquisitions involving U.S. target companies.",
    ])

    pdf.subsection_heading("7.2", "Check-the-Box Entity Classification")
    pdf.body_text(
        "Entity classification elections under Treasury Regulation 301.7701-3 (the 'check-the-box' "
        "rules) remain one of the most powerful tools in international tax planning. Meridian assists "
        "clients with:"
    )
    pdf.bullet_list([
        "Entity Classification Planning: Evaluating whether foreign entities should be classified as corporations (per se or elective), partnerships, or disregarded entities for U.S. tax purposes. The classification affects CFC status, Subpart F inclusions, GILTI calculations, and FTC computations.",
        "Hybrid Entity Planning: Utilizing check-the-box elections to create hybrid entities (treated as transparent for U.S. tax purposes but as separate entities for foreign tax purposes) or reverse hybrids. Post-TCJA and post-ATAD, hybrid arrangements face increased scrutiny under Section 267A (anti-hybrid) and similar foreign anti-hybrid rules.",
        "Timing and Retroactivity: Advising on the timing of entity classification elections, including the ability to file retroactive elections (effective up to 75 days before the filing date under the regulatory relief provisions) and the consequences of late elections.",
        "Interaction with Pillar Two: Analyzing how entity classification elections affect the jurisdictional blending and effective tax rate calculations under the GloBE rules, including the treatment of tax transparent entities and reverse hybrid entities.",
    ])

    # --- Section 8 ---
    pdf.section_heading("8.", "Pillar Two Interaction and Compliance")
    pdf.body_text(
        "The OECD/G20 Inclusive Framework's Pillar Two (Global Anti-Base Erosion, or GloBE) rules "
        "are fundamentally reshaping international tax planning. With over 50 jurisdictions "
        "enacting or announcing GloBE implementation legislation, Meridian helps clients navigate "
        "the compliance obligations and planning implications."
    )
    pdf.bullet_list([
        "Impact Assessment: Modeling the GloBE effective tax rate for each jurisdiction where the client operates, identifying jurisdictions where top-up tax exposure exists (ETR below 15%) and quantifying the additional tax cost under IIR (Income Inclusion Rule), UTPR (Undertaxed Profits Rule), and QDMTT (Qualified Domestic Minimum Top-Up Tax) mechanisms.",
        "Safe Harbor Analysis: Evaluating qualification for the GloBE transitional safe harbors (CbCR safe harbor, de minimis test, and routine profits test) to reduce compliance burden during the initial years of implementation.",
        "Data Readiness: Assessing the client's ability to produce the detailed financial data required for GloBE calculations, including jurisdictional top-up tax computations, deferred tax adjustments, and substance-based income exclusion (SBIE) calculations.",
        "U.S. Interaction: Analyzing the interaction between the U.S. international tax regime (GILTI, Subpart F, BEAT, FDII) and Pillar Two, including whether GILTI satisfies the requirements of a qualified IIR and the potential for double taxation.",
        "Structural Optimization: Advising on structural changes (entity rationalization, IP relocation, substance augmentation) to minimize top-up tax exposure while maintaining compliance with the GloBE anti-abuse rules.",
    ])

    # --- Section 9 ---
    pdf.section_heading("9.", "Post-TCJA Structuring Considerations")
    pdf.body_text(
        "The TCJA fundamentally altered the U.S. international tax landscape. Meridian continuously "
        "monitors legislative and regulatory developments and advises clients on optimization within "
        "the post-TCJA framework, including:"
    )
    pdf.bullet_list([
        "TCJA Sunset Provisions: Key provisions including the Section 250 FDII/GILTI deduction rates (which decreased effective for tax years beginning after December 31, 2025, from 37.5%/50% to 21.875%/37.5% respectively), Section 163(j) interest limitation (30% of EBITDA reverting to EBIT), Section 174 R&D capitalization requirement, and the bonus depreciation phase-down (40% for 2025, 20% for 2026). Modeling the impact of remaining sunset scenarios and advising on planning actions.",
        "Base Erosion and Anti-Abuse Tax (BEAT): Evaluating whether clients are applicable taxpayers under Section 59A (average annual gross receipts exceeding $500 million and base erosion percentage exceeding 3%) and modeling the BEAT liability under various payment restructuring scenarios.",
        "Section 163(j) International Implications: Analyzing the interaction between the Section 163(j) interest limitation and CFC-level interest deductions, including the allocation of interest expense for Section 904 FTC limitation purposes.",
        "Outbound and Inbound Restructuring: Advising on the tax consequences of expatriating operations (Section 367, Section 1248), repatriating operations, and restructuring existing holding company chains in light of TCJA, Pillar Two, and evolving bilateral treaty provisions.",
    ])

    pdf.save("international_tax_planning.pdf")


# ===================================================================
# MAIN
# ===================================================================

def main():
    print("Generating Meridian & Associates LLP -- Tax Services PDFs...")
    build_global_tax_compliance()
    build_transfer_pricing()
    build_tax_provision()
    build_ma_due_diligence()
    build_credits_incentives()
    build_tax_controversy()
    build_tax_technology()
    build_salt_methodology()
    build_international_tax_planning()
    print("\nDone. All 9 PDFs generated.")


if __name__ == "__main__":
    main()
