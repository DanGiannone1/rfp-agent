"""Generate 3 synthetic client profile PDFs for Meridian & Associates LLP."""

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
            self.cell(0, 5, "CLIENT CONFIDENTIAL", align="R")
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
            self.cell(0, 8, "CLIENT CONFIDENTIAL", align="C")
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
# 1. ACME Manufacturing Client Profile
# ============================================================================

def generate_acme_manufacturing():
    pdf = MeridianPDF(
        "Client Relationship Profile",
        "ACME Manufacturing Corporation",
        confidential=True
    )
    pdf.cover_page(version="2.4", date="February 2026")

    pdf.add_page()
    pdf.section_heading("1. Client Overview")
    pdf.key_value("Client Name", "ACME Manufacturing Corporation")
    pdf.key_value("Industry", "Diversified Manufacturing (Industrial Equipment, Aerospace Components, Automotive Parts)")
    pdf.key_value("Headquarters", "Detroit, MI")
    pdf.key_value("Annual Revenue", "$4.8 billion (FY2025)")
    pdf.key_value("Employees", "18,500 globally")
    pdf.key_value("Publicly Traded", "Yes -- NYSE: ACMM")
    pdf.key_value("Global Operations", "Manufacturing facilities in US (6), Mexico (2), Germany (1), China (1), India (1)")
    pdf.key_value("Fiscal Year End", "December 31")
    pdf.key_value("Relationship Partner", "Sarah Chen, CPA, CISA")
    pdf.key_value("Relationship Start Date", "October 2017")
    pdf.key_value("Relationship Tenure", "8+ years")

    pdf.section_heading("2. Relationship History")
    pdf.body_text(
        "Meridian & Associates LLP has served ACME Manufacturing Corporation since October 2017, "
        "beginning with an internal audit co-sourcing engagement. The relationship has expanded "
        "significantly over time, and ACME is now one of Meridian's Top 50 clients by revenue, "
        "with annual fees exceeding $8.2 million across multiple service lines."
    )

    pdf.section_heading("Timeline of Engagements", level=2)
    pdf.bold_bullet("2017 (Q4)", "Internal Audit Co-Sourcing -- engaged to supplement ACME's internal audit function with 6 dedicated professionals. Scope included SOX 404 testing, operational audits, and compliance reviews.")
    pdf.bold_bullet("2018 (Q2)", "IT Risk Assessment -- comprehensive assessment of cybersecurity posture across 11 manufacturing facilities. Identified 47 critical vulnerabilities and developed remediation roadmap.")
    pdf.bold_bullet("2019 (Q1)", "ERP Advisory -- selected as independent advisor for ACME's $85M SAP S/4HANA implementation. Provided program governance, change management, and quality assurance over 24 months.")
    pdf.bold_bullet("2020 (Q3)", "Transfer Pricing Study -- documented intercompany pricing for cross-border transactions between US, Mexico, Germany, China, and India operations.")
    pdf.bold_bullet("2021 (Q1)", "Post-Merger Integration -- advised on integration of Vertex Precision Components ($420M acquisition), including Day 1 readiness, synergy tracking, and cultural integration.")
    pdf.bold_bullet("2022 (Q2)", "Tax Compliance Transition -- assumed global tax compliance from prior provider. Consolidated 8 local firms into coordinated Meridian delivery.")
    pdf.bold_bullet("2023 (Q1)", "Supply Chain Resilience Study -- developed multi-tier supply chain risk model following pandemic disruptions. Identified alternative sourcing strategies for 340 critical components.")
    pdf.bold_bullet("2024 (Q2)", "ESG Reporting Advisory -- assisted with first voluntary CSRD-aligned sustainability report and limited assurance engagement.")
    pdf.bold_bullet("2025 (Q1)", "Cybersecurity Maturity Assessment -- reassessment and NIST CSF 2.0 alignment across all operations. Supported preparation for SEC cybersecurity disclosure requirements.")
    pdf.bold_bullet("2025 (Q4)", "R&D Tax Credit Study -- identified $14.2M in previously unclaimed federal and state R&D tax credits for FY2022-2024.")

    pdf.add_page()
    pdf.section_heading("3. Current Active Engagements")

    pdf.section_heading("Internal Audit Co-Sourcing (Ongoing)", level=2)
    pdf.key_value("Annual Fee", "$1.8M")
    pdf.key_value("Meridian Team Size", "8 dedicated professionals (1 Director, 2 Managers, 5 Staff)")
    pdf.key_value("Scope", "SOX 404 testing (65 key controls), operational audits (12 per year), compliance reviews, fraud risk assessments")
    pdf.key_value("Engagement Partner", "Sarah Chen")
    pdf.key_value("Client Contact", "VP of Internal Audit, Thomas Nakamura")

    pdf.section_heading("Global Tax Compliance (Ongoing)", level=2)
    pdf.key_value("Annual Fee", "$3.4M")
    pdf.key_value("Scope", "US federal, state (28 states), and international compliance (5 jurisdictions). Transfer pricing documentation. Quarterly ASC 740 provision support.")
    pdf.key_value("Engagement Partner", "James Worthington")
    pdf.key_value("Client Contact", "VP of Tax, Maria Rodriguez")

    pdf.section_heading("ESG Assurance (Annual)", level=2)
    pdf.key_value("Annual Fee", "$420K")
    pdf.key_value("Scope", "Limited assurance on selected ESG metrics per ISAE 3000/3410. Advisory on CSRD readiness.")
    pdf.key_value("Engagement Partner", "Sarah Chen")
    pdf.key_value("Client Contact", "Chief Sustainability Officer, Karen Park")

    pdf.section_heading("Cybersecurity Managed Services (Ongoing)", level=2)
    pdf.key_value("Annual Fee", "$2.6M")
    pdf.key_value("Scope", "Continuous vulnerability management, penetration testing (quarterly), incident response retainer, security awareness training program")
    pdf.key_value("Engagement Partner", "David Kim")
    pdf.key_value("Client Contact", "CISO, Robert Zhang")

    pdf.add_page()
    pdf.section_heading("4. Key Outcomes and Value Delivered")
    pdf.body_text(
        "Over the course of our 8+ year relationship, Meridian has delivered measurable value to ACME "
        "Manufacturing across multiple dimensions:"
    )
    pdf.bold_bullet("Tax Savings", "$14.2M in R&D tax credits identified (FY2022-2024); $2.8M in transfer pricing optimization savings annually")
    pdf.bold_bullet("Audit Efficiency", "Reduced SOX testing cycle from 16 weeks to 11 weeks through continuous auditing techniques and data analytics")
    pdf.bold_bullet("ERP Implementation", "SAP S/4HANA delivered on-time and within 3% of budget ($85M program). Achieved 99.4% data migration accuracy. Reduced month-end close from 12 days to 5 days.")
    pdf.bold_bullet("Cybersecurity", "Reduced critical vulnerabilities by 87% (from 47 to 6) over 2-year remediation program. Achieved NIST CSF maturity score of 3.8/5.0, up from 2.1.")
    pdf.bold_bullet("Post-Merger Integration", "Vertex Precision integration completed in 9 months (3 months ahead of plan). Achieved $18M in Year 1 synergies against $15M target.")
    pdf.bold_bullet("Supply Chain", "Identified alternative sourcing for 340 critical components, reducing single-source dependency from 42% to 14%")

    pdf.section_heading("5. Client Satisfaction")
    pdf.key_value("Most Recent CSAT Score", "4.7 / 5.0 (December 2025 annual survey)")
    pdf.key_value("Net Promoter Score", "+72 (Promoter category)")
    pdf.key_value("Relationship Health Rating", "Green -- strong and growing")
    pdf.body_text(
        "ACME has participated in Meridian's annual client satisfaction survey every year since 2018. "
        "Scores have consistently exceeded 4.5/5.0. Key themes from qualitative feedback include:"
    )
    pdf.bullet("'Meridian professionals feel like an extension of our team, not outside consultants'")
    pdf.bullet("'The partner-level attention we receive is exceptional -- Sarah is always accessible'")
    pdf.bullet("'Meridian proactively identifies issues and opportunities; they don't wait to be asked'")
    pdf.bullet("'The quality of deliverables is consistently high across all service lines'")
    pdf.bullet("'Pricing is fair and transparent -- no surprises'")

    pdf.section_heading("6. Growth Opportunities")
    pdf.body_text("The following opportunities have been identified for relationship expansion:")
    pdf.bold_bullet("External Audit (FY2027)", "ACME's current external auditor contract expires December 2026. Management has indicated interest in considering Meridian. Requires independence planning if pursued.")
    pdf.bold_bullet("AI/ML Advisory", "ACME is evaluating AI applications for predictive maintenance and quality control. Meridian's new AI Advisory practice is well-positioned.")
    pdf.bold_bullet("International Expansion Advisory", "ACME is considering a manufacturing facility in Vietnam. Meridian can provide site selection, tax structuring, and regulatory compliance advisory.")

    pdf.section_heading("7. Key Contacts at ACME")
    pdf.bold_bullet("CEO", "Richard Hawthorne (relationship: moderate -- annual executive dinner)")
    pdf.bold_bullet("CFO", "Patricia Williams (relationship: strong -- quarterly meetings with Sarah Chen)")
    pdf.bold_bullet("VP of Internal Audit", "Thomas Nakamura (relationship: strong -- daily interaction)")
    pdf.bold_bullet("VP of Tax", "Maria Rodriguez (relationship: strong -- bi-weekly calls)")
    pdf.bold_bullet("CISO", "Robert Zhang (relationship: strong -- monthly security briefings)")
    pdf.bold_bullet("Chief Sustainability Officer", "Karen Park (relationship: developing)")
    pdf.bold_bullet("General Counsel", "Margaret O'Brien (relationship: moderate)")

    pdf.output(os.path.join(OUTPUT_DIR, "client_profile_acme_manufacturing.pdf"))
    print("  Created: client_profile_acme_manufacturing.pdf")


# ============================================================================
# 2. Statewide Health Client Profile
# ============================================================================

def generate_statewide_health():
    pdf = MeridianPDF(
        "Client Relationship Profile",
        "Statewide Health System",
        confidential=True
    )
    pdf.cover_page(version="1.8", date="February 2026")

    pdf.add_page()
    pdf.section_heading("1. Client Overview")
    pdf.key_value("Client Name", "Statewide Health System")
    pdf.key_value("Industry", "Healthcare (Integrated Health System)")
    pdf.key_value("Headquarters", "Columbus, OH")
    pdf.key_value("Annual Revenue", "$7.2 billion (FY2025)")
    pdf.key_value("Employees", "42,000")
    pdf.key_value("Organization Type", "Not-for-profit 501(c)(3)")
    pdf.key_value("Facilities", "12 hospitals, 85 ambulatory care sites, 3 post-acute facilities, 2 research centers")
    pdf.key_value("Service Area", "Central and Southern Ohio (3.2 million covered lives)")
    pdf.key_value("Fiscal Year End", "June 30")
    pdf.key_value("Relationship Partner", "Michael Torres, CPA, PMP")
    pdf.key_value("Relationship Start Date", "March 2019")
    pdf.key_value("Relationship Tenure", "7 years")

    pdf.section_heading("2. Relationship History")
    pdf.body_text(
        "Meridian's relationship with Statewide Health System began in 2019 when we were selected through "
        "a competitive RFP process to provide revenue cycle optimization consulting. The engagement was "
        "highly successful, leading to significant relationship expansion. Statewide is now Meridian's "
        "largest healthcare client and a flagship reference account for the Healthcare & Life Sciences "
        "Practice. Total relationship revenue has grown from $1.2M in Year 1 to $11.4M in FY2025."
    )

    pdf.section_heading("Timeline of Engagements", level=2)
    pdf.bold_bullet("2019 (Q1)", "Revenue Cycle Optimization -- 14-month engagement to redesign patient access, charge capture, coding, and denial management processes across all 12 hospitals. Achieved $48M annual revenue improvement.")
    pdf.bold_bullet("2020 (Q2)", "COVID-19 Financial Response -- emergency engagement to model financial impact, optimize CARES Act funding, and restructure operating budgets. Secured $124M in CARES/ARPA funding.")
    pdf.bold_bullet("2020 (Q4)", "Telehealth Strategy -- developed enterprise telehealth strategy and implementation roadmap. Scaled from 200 to 15,000 monthly virtual visits within 6 months.")
    pdf.bold_bullet("2021 (Q2)", "Clinical Workforce Planning -- comprehensive workforce analysis addressing post-pandemic nursing shortages. Developed retention strategies, compensation benchmarking, and flexible staffing models.")
    pdf.bold_bullet("2022 (Q1)", "ERP Advisory Services -- selected as independent advisor for Oracle Cloud implementation (see separate proposal file). 24-month program currently in Phase 3.")
    pdf.bold_bullet("2023 (Q1)", "Value-Based Care Program Design -- designed bundled payment programs for orthopedics, cardiology, and maternity services. Negotiated contracts with 4 major payers.")
    pdf.bold_bullet("2024 (Q2)", "Cybersecurity Assessment -- HITRUST readiness assessment and remediation planning across all clinical and business systems. Achieved HITRUST r2 certification in 10 months.")
    pdf.bold_bullet("2025 (Q1)", "Financial Sustainability Initiative -- comprehensive margin improvement program targeting $85M in annual savings through operational efficiency, supply chain optimization, and revenue enhancement.")

    pdf.add_page()
    pdf.section_heading("3. Current Active Engagements")

    pdf.section_heading("ERP Advisory Services (Multi-Year)", level=2)
    pdf.key_value("Total Contract Value", "$4.8M (24-month program)")
    pdf.key_value("Current Phase", "Phase 3: Build and Configure (Month 14 of 24)")
    pdf.key_value("Meridian Team Size", "12 professionals on-site (1 Program Director, 3 Functional Leads, 2 Change Management, 6 Analysts)")
    pdf.key_value("Status", "On track -- green on all major milestones")
    pdf.key_value("Engagement Partner", "Michael Torres")
    pdf.key_value("Client Contact", "CIO, Robert Patel; CFO, Angela Morrison")

    pdf.section_heading("Financial Sustainability Initiative (In Progress)", level=2)
    pdf.key_value("Contract Value", "$3.2M (18-month program)")
    pdf.key_value("Current Phase", "Phase 2: Implementation (Month 8 of 18)")
    pdf.key_value("Target Savings", "$85M annual run-rate by completion")
    pdf.key_value("Savings Achieved to Date", "$42M identified, $28M implemented")
    pdf.key_value("Engagement Partner", "Michael Torres")
    pdf.key_value("Client Contact", "CFO, Angela Morrison; COO, Dr. James Patterson")

    pdf.section_heading("Cybersecurity Managed Services (Ongoing)", level=2)
    pdf.key_value("Annual Fee", "$1.8M")
    pdf.key_value("Scope", "Continuous monitoring, vulnerability management, incident response, HITRUST maintenance, security awareness training for 42,000 employees")
    pdf.key_value("Engagement Partner", "David Kim")
    pdf.key_value("Client Contact", "CISO, Michelle Chang")

    pdf.section_heading("Tax-Exempt Bond Compliance (Annual)", level=2)
    pdf.key_value("Annual Fee", "$380K")
    pdf.key_value("Scope", "Post-issuance compliance monitoring for $1.4B in outstanding tax-exempt bonds. Private use analysis, arbitrage rebate calculations.")
    pdf.key_value("Engagement Partner", "James Worthington")
    pdf.key_value("Client Contact", "Treasurer, William Foster")

    pdf.add_page()
    pdf.section_heading("4. Key Outcomes and Value Delivered")
    pdf.bold_bullet("Revenue Cycle", "$48M annual revenue improvement through denial rate reduction (from 12.4% to 6.8%), coding accuracy improvement (95.2% to 98.7%), and patient access redesign")
    pdf.bold_bullet("COVID-19 Response", "$124M in CARES/ARPA funding secured. Financial model guided Board through decisions on service line prioritization and capital expenditure deferrals.")
    pdf.bold_bullet("Telehealth", "Scaled from 200 to 15,000 monthly virtual visits. Telehealth now accounts for 8% of total ambulatory visits with patient satisfaction scores averaging 4.6/5.0")
    pdf.bold_bullet("Value-Based Care", "Bundled payment programs generating $12M in shared savings in Year 1. Quality metrics improved across all three service lines.")
    pdf.bold_bullet("Cybersecurity", "Achieved HITRUST r2 certification in 10 months (industry average: 14 months). Reduced critical vulnerabilities by 91%.")
    pdf.bold_bullet("Financial Sustainability", "$42M in savings opportunities identified in first 8 months against $85M 18-month target. Ahead of pace.")
    pdf.bold_bullet("Workforce", "Nursing turnover reduced from 24% to 16% through retention strategies. Saved an estimated $18M in annual agency staffing costs.")

    pdf.section_heading("5. Client Satisfaction")
    pdf.key_value("Most Recent CSAT Score", "4.8 / 5.0 (November 2025 annual survey)")
    pdf.key_value("Net Promoter Score", "+82 (Promoter category -- highest among healthcare clients)")
    pdf.key_value("Relationship Health Rating", "Green -- flagship account")
    pdf.body_text("Selected verbatim feedback from the CEO:")
    pdf.bullet("'Meridian is a true strategic partner. They understand the unique challenges of running a not-for-profit health system and bring insights from across their client base that we simply cannot get elsewhere.'")
    pdf.bullet("'Michael Torres and his team operate with an ownership mentality. They care about our outcomes as much as we do.'")
    pdf.bullet("'The breadth of capabilities -- from ERP to cybersecurity to financial strategy -- under one roof has been transformational for us.'")

    pdf.section_heading("6. Growth Opportunities")
    pdf.bold_bullet("External Financial Audit", "Current auditor contract expires June 2027. Board Audit Committee chair has expressed interest in exploring alternatives. Requires independence review.")
    pdf.bold_bullet("Clinical AI Advisory", "Statewide is evaluating AI-assisted clinical decision support, ambient documentation, and predictive analytics. RFP expected Q3 2026.")
    pdf.bold_bullet("Ambulatory Growth Strategy", "Planning 8 new ambulatory sites over 3 years. Opportunity for market analysis, site selection, and financial pro forma development.")
    pdf.bold_bullet("Post-Acute Care Expansion", "Exploring home health and hospice service lines. Advisory opportunity for market entry strategy and regulatory compliance.")

    pdf.section_heading("7. Key Contacts at Statewide Health")
    pdf.bold_bullet("CEO", "Dr. Catherine Reynolds (relationship: strong -- quarterly executive meetings)")
    pdf.bold_bullet("CFO", "Angela Morrison (relationship: very strong -- weekly interaction)")
    pdf.bold_bullet("CIO", "Robert Patel (relationship: strong -- daily interaction during ERP program)")
    pdf.bold_bullet("COO", "Dr. James Patterson (relationship: strong -- financial sustainability program)")
    pdf.bold_bullet("CISO", "Michelle Chang (relationship: strong)")
    pdf.bold_bullet("CMO", "Dr. Elizabeth Warren (relationship: developing)")
    pdf.bold_bullet("Board Audit Committee Chair", "Harold Richardson (relationship: moderate -- annual presentation)")

    pdf.output(os.path.join(OUTPUT_DIR, "client_profile_statewide_health.pdf"))
    print("  Created: client_profile_statewide_health.pdf")


# ============================================================================
# 3. Metro Transit Authority Client Profile
# ============================================================================

def generate_metro_transit():
    pdf = MeridianPDF(
        "Client Relationship Profile",
        "Metro Transit Authority",
        confidential=True
    )
    pdf.cover_page(version="1.5", date="February 2026")

    pdf.add_page()
    pdf.section_heading("1. Client Overview")
    pdf.key_value("Client Name", "Metro Transit Authority (MTA)")
    pdf.key_value("Industry", "Public Sector -- Transportation")
    pdf.key_value("Headquarters", "Portland, OR")
    pdf.key_value("Annual Operating Budget", "$1.8 billion (FY2025)")
    pdf.key_value("Employees", "8,200")
    pdf.key_value("Organization Type", "Regional government authority, established by state statute")
    pdf.key_value("Service Area", "Portland metropolitan area, covering 3 counties and 1,400 square miles")
    pdf.key_value("Ridership", "98 million annual trips (FY2025)")
    pdf.key_value("Modes of Service", "Light rail (5 lines, 97 stations), bus (82 routes), commuter rail (1 line), paratransit, bike-share")
    pdf.key_value("Fiscal Year End", "June 30")
    pdf.key_value("Relationship Partner", "David Rawlings, CPA, CGFM")
    pdf.key_value("Relationship Start Date", "July 2020")
    pdf.key_value("Relationship Tenure", "6 years")

    pdf.section_heading("2. Relationship History")
    pdf.body_text(
        "Meridian's engagement with Metro Transit Authority began in 2020 when MTA selected Meridian "
        "through a competitive procurement process to serve as its independent external auditor. The "
        "initial contract was for a 3-year term with two 1-year renewal options. Both renewal options "
        "have been exercised, and MTA has indicated intent to issue a new 5-year RFP in early 2026 "
        "(a significant re-compete opportunity). Total relationship revenue has grown from $680K in "
        "Year 1 to $2.4M in FY2025 as additional service lines have been added."
    )

    pdf.section_heading("Timeline of Engagements", level=2)
    pdf.bold_bullet("2020 (Q3)", "External Financial Audit -- selected as independent auditor for MTA's ACFR and single audit. Scope includes the Authority and 3 component units.")
    pdf.bold_bullet("2021 (Q1)", "Federal Grant Compliance Review -- comprehensive review of $340M in FTA formula and discretionary grants. Identified compliance gaps in procurement documentation and grant period tracking.")
    pdf.bold_bullet("2021 (Q4)", "Internal Controls Assessment -- COSO-based assessment of internal controls over financial reporting. Identified 12 significant deficiencies and developed remediation roadmap.")
    pdf.bold_bullet("2022 (Q2)", "Fare Revenue Integrity Study -- analysis of fare evasion rates, revenue leakage, and technology options for next-generation fare collection system.")
    pdf.bold_bullet("2023 (Q1)", "Cybersecurity Assessment -- assessment of operational technology (OT) security across rail signaling, SCADA systems, and transit management systems. Developed incident response playbook.")
    pdf.bold_bullet("2023 (Q3)", "Capital Program Audit -- performance audit of $2.1B capital program (light rail expansion). Assessed project management practices, cost controls, and contractor oversight.")
    pdf.bold_bullet("2024 (Q2)", "Zero-Emission Bus Transition Study -- financial and operational analysis of transitioning 420-bus fleet to battery-electric. Modeled TCO, infrastructure requirements, and phased deployment scenarios.")
    pdf.bold_bullet("2025 (Q1)", "Enterprise Risk Management -- designed and implemented ERM framework per ISO 31000. Facilitated risk workshops with Board and executive leadership.")

    pdf.add_page()
    pdf.section_heading("3. Current Active Engagements")

    pdf.section_heading("Annual Financial Audit (Ongoing)", level=2)
    pdf.key_value("Annual Fee", "$890K")
    pdf.key_value("Scope", "ACFR preparation and audit, single audit (6 major federal programs), 3 component unit audits, management letter")
    pdf.key_value("Team Size", "10 professionals during peak fieldwork (September-November)")
    pdf.key_value("Engagement Partner", "David Rawlings")
    pdf.key_value("Client Contact", "CFO, Diana Kowalski; Controller, Mark Tanaka")

    pdf.section_heading("Cybersecurity Monitoring (Ongoing)", level=2)
    pdf.key_value("Annual Fee", "$640K")
    pdf.key_value("Scope", "Quarterly vulnerability assessments of IT and OT environments, annual penetration testing, incident response retainer, security awareness training")
    pdf.key_value("Engagement Partner", "David Kim")
    pdf.key_value("Client Contact", "CIO, Steven Hernandez")

    pdf.section_heading("Capital Program Oversight (Ongoing)", level=2)
    pdf.key_value("Annual Fee", "$870K")
    pdf.key_value("Scope", "Independent oversight of $2.1B light rail expansion program. Quarterly progress audits, cost-to-complete analysis, change order review, contractor performance assessment.")
    pdf.key_value("Engagement Partner", "David Rawlings")
    pdf.key_value("Client Contact", "VP Capital Programs, Jennifer Lawson")

    pdf.add_page()
    pdf.section_heading("4. Key Outcomes and Value Delivered")
    pdf.bold_bullet("ACFR Quality", "MTA has received the GFOA Certificate of Achievement for Excellence in Financial Reporting for all 5 years of Meridian's tenure as auditor. Prior auditor: 2 of 5 years.")
    pdf.bold_bullet("Federal Compliance", "Identified $2.4M in questioned costs during single audit, all resolved through corrective action without FTA enforcement. Prevented potential debarment risk.")
    pdf.bold_bullet("Internal Controls", "12 significant deficiencies identified in 2021 reduced to 2 by 2024 through systematic remediation. No material weaknesses in any year.")
    pdf.bold_bullet("Fare Revenue", "Fare integrity study identified $8.2M in annual revenue leakage. Recommendations informed MTA's decision to procure next-generation open-payment fare system.")
    pdf.bold_bullet("Cybersecurity", "OT security assessment identified critical vulnerabilities in rail signaling systems. Remediation completed within 6 months. MTA was the only peer agency not impacted by the 2024 ransomware wave affecting transit systems.")
    pdf.bold_bullet("Capital Program", "Identified $14.8M in potential cost overruns early enough for corrective action. Capital program currently 2.3% under budget.")
    pdf.bold_bullet("Zero-Emission Transition", "TCO analysis demonstrated battery-electric buses achieve cost parity at Year 8, with $180M in lifecycle savings over 12-year fleet life. Analysis secured Board approval and $340M in FTA Low-No grants.")

    pdf.section_heading("5. Client Satisfaction")
    pdf.key_value("Most Recent CSAT Score", "4.6 / 5.0 (October 2025 annual survey)")
    pdf.key_value("Net Promoter Score", "+68 (Promoter category)")
    pdf.key_value("Relationship Health Rating", "Green -- strong with upcoming re-compete")
    pdf.body_text("Selected feedback from MTA Board Chair:")
    pdf.bullet("'Meridian has brought a level of rigor and professionalism to our financial oversight that the Board deeply values.'")
    pdf.bullet("'The capital program oversight work has given us confidence that taxpayer dollars are being spent responsibly.'")
    pdf.bullet("'David Rawlings and his team understand the unique governance and accountability requirements of a public transit agency.'")

    pdf.section_heading("6. Key Risks and Considerations")
    pdf.bold_bullet("Re-Compete Risk", "Current audit contract expires June 2026. MTA procurement rules require competitive RFP for contracts exceeding $500K. Strong incumbent position but must demonstrate continued value and competitive pricing.")
    pdf.bold_bullet("Independence Considerations", "Growing advisory relationship creates independence monitoring requirements. Current non-audit fees ($1.51M) exceed audit fees ($890K). Independence Committee reviewing annually.")
    pdf.bold_bullet("Political Environment", "MTA Board is politically appointed. Board composition changed significantly after November 2024 elections. New members may prefer different advisory relationships.")
    pdf.bold_bullet("Budget Pressure", "MTA facing structural budget deficit due to post-pandemic ridership recovery (82% of pre-pandemic levels). May pressure professional services spending.")

    pdf.add_page()
    pdf.section_heading("7. Growth Opportunities")
    pdf.bold_bullet("Audit Re-Compete (FY2026-2031)", "Highest priority. 5-year contract worth approximately $4.5M-$5M total. Proposal team being assembled now.")
    pdf.bold_bullet("ERP Modernization", "MTA's 20-year-old PeopleSoft financial system approaching end-of-life. CIO has requested informal briefing on Meridian's ERP advisory capabilities.")
    pdf.bold_bullet("Workforce Planning", "MTA facing significant retirement wave (28% of workforce eligible to retire within 5 years). Workforce planning and succession consulting opportunity.")
    pdf.bold_bullet("Climate Resilience", "Board resolution requires climate vulnerability assessment of all transit infrastructure. Opportunity for risk assessment and adaptation planning engagement.")

    pdf.section_heading("8. Key Contacts at MTA")
    pdf.bold_bullet("General Manager / CEO", "Anthony Reeves (relationship: moderate -- quarterly Board presentations)")
    pdf.bold_bullet("CFO", "Diana Kowalski (relationship: very strong -- weekly interaction during audit season)")
    pdf.bold_bullet("Controller", "Mark Tanaka (relationship: very strong -- daily interaction)")
    pdf.bold_bullet("CIO", "Steven Hernandez (relationship: strong)")
    pdf.bold_bullet("VP Capital Programs", "Jennifer Lawson (relationship: strong)")
    pdf.bold_bullet("Board Chair", "Commissioner Patricia Kim (relationship: moderate)")
    pdf.bold_bullet("Board Audit Committee Chair", "Commissioner David Washington (relationship: strong -- quarterly presentations)")
    pdf.bold_bullet("General Counsel", "Rebecca Santos (relationship: developing)")

    pdf.output(os.path.join(OUTPUT_DIR, "client_profile_metro_transit.pdf"))
    print("  Created: client_profile_metro_transit.pdf")


if __name__ == "__main__":
    generate_acme_manufacturing()
    generate_statewide_health()
    generate_metro_transit()
    print("\nAll 3 client profile PDFs generated successfully!")
