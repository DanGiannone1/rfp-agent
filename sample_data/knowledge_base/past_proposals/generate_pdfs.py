"""Generate 3 synthetic past proposal PDFs for Meridian & Associates LLP."""

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
        x = self.get_x()
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

    def redacted_text(self, label):
        """Display a redacted value with black bar."""
        self.set_text_color(40, 40, 40)
        self.set_font("Helvetica", "B", 10)
        w = self.get_string_width(label + ": ")
        self.cell(w, 5.5, label + ": ")
        self.set_font("Helvetica", "", 10)
        self.set_fill_color(30, 30, 30)
        self.cell(40, 5.5, "  [REDACTED]  ", fill=True)
        self.set_text_color(40, 40, 40)
        self.ln(7)


# ============================================================================
# 1. Financial Audit Services Proposal (City Government)
# ============================================================================

def generate_financial_audit_proposal():
    pdf = MeridianPDF(
        "Proposal for Financial Audit Services",
        "City of Lakewood, Colorado - RFP #FIN-2025-042",
        client_confidential=True
    )
    pdf.cover_page(version="2.0", date="September 2025")

    # --- Cover Letter ---
    pdf.add_page()
    pdf.section_heading("Cover Letter")
    pdf.body_text("September 8, 2025")
    pdf.ln(2)
    pdf.body_text(
        "Ms. Jennifer Martinez, Finance Director\n"
        "City of Lakewood, Department of Finance\n"
        "480 South Allison Parkway\n"
        "Lakewood, CO 80226"
    )
    pdf.ln(2)
    pdf.body_text("Dear Ms. Martinez,")
    pdf.body_text(
        "Meridian & Associates LLP is pleased to submit this proposal in response to RFP #FIN-2025-042 "
        "for Financial Audit Services for the City of Lakewood. We understand the City seeks a qualified "
        "firm to conduct comprehensive annual financial audits of its general-purpose financial statements, "
        "including the preparation of the Annual Comprehensive Financial Report (ACFR), for a five-year "
        "period commencing with fiscal year ending December 31, 2025."
    )
    pdf.body_text(
        "Meridian brings more than 35 years of experience serving state and local government entities across "
        "the United States. Our Government Services Practice currently serves over 120 municipal clients, "
        "including 18 cities with populations exceeding 100,000. We have consistently delivered audits that "
        "meet or exceed Government Auditing Standards (Yellow Book), the Single Audit Act, and Uniform "
        "Guidance requirements."
    )
    pdf.body_text(
        "Our proposed engagement partner, David Rawlings, CPA, CGFM, has personally led over 75 municipal "
        "financial audits during his 22-year career with Meridian. He will be supported by a dedicated team "
        "of professionals with deep expertise in governmental accounting standards (GASB), public sector "
        "internal controls, and ACFR preparation."
    )
    pdf.body_text(
        "We are committed to delivering timely, high-quality audit services while minimizing disruption to "
        "City staff. Our proven methodology emphasizes early planning, continuous communication, and the "
        "use of advanced data analytics to enhance audit efficiency and coverage."
    )
    pdf.body_text(
        "We welcome the opportunity to discuss our qualifications further. Please do not hesitate to "
        "contact me or David Rawlings at the numbers provided in this proposal."
    )
    pdf.ln(4)
    pdf.body_text("Respectfully submitted,")
    pdf.ln(2)
    pdf.body_text(
        "Margaret L. Foster, CPA\n"
        "Regional Managing Partner, Mountain West\n"
        "Meridian & Associates LLP\n"
        "Phone: (303) 555-0198\n"
        "Email: m.foster@meridian-llp.com"
    )

    # --- Executive Summary ---
    pdf.add_page()
    pdf.section_heading("1. Executive Summary")
    pdf.body_text(
        "Meridian & Associates LLP proposes to serve as the independent external auditor for the City of "
        "Lakewood, providing comprehensive annual financial audit services in full compliance with Generally "
        "Accepted Auditing Standards (GAAS), Government Auditing Standards (GAS/Yellow Book), and the "
        "requirements of the Single Audit Act Amendments and OMB Uniform Guidance (2 CFR Part 200)."
    )
    pdf.body_text(
        "Our engagement will encompass: (1) annual audit of the City's general-purpose financial statements, "
        "(2) preparation and review of the ACFR in accordance with GFOA standards, (3) single audit of "
        "federal award programs, (4) issuance of management letters identifying internal control findings "
        "and recommendations, and (5) presentation of audit results to the City Council and Audit Committee."
    )
    pdf.section_heading("Why Meridian", level=2)
    pdf.bullet("120+ active municipal audit clients nationwide, including 18 cities with populations over 100,000")
    pdf.bullet("97% client retention rate in our Government Services Practice over the past decade")
    pdf.bullet("14 consecutive years of clean peer review reports with no findings")
    pdf.bullet("Proprietary data analytics platform (Meridian Insight) analyzes 100% of transactions versus traditional sampling")
    pdf.bullet("Dedicated GASB technical specialists who monitor and advise on new pronouncements (GASB 87, 96, 100, 101)")
    pdf.bullet("GFOA Certificate of Achievement assistance -- 95% of our ACFR clients receive the Certificate annually")

    # --- Approach & Methodology ---
    pdf.add_page()
    pdf.section_heading("2. Approach and Methodology")
    pdf.section_heading("Phase 1: Planning and Risk Assessment (August - September)", level=2)
    pdf.body_text(
        "Our audit begins with a comprehensive planning phase designed to understand the City's operations, "
        "financial reporting environment, and risk profile. Key activities include:"
    )
    pdf.bullet("Entrance conference with Finance Director, City Manager, and department heads to discuss scope, timing, and expectations")
    pdf.bullet("Assessment of the City's internal control environment using the COSO 2013 framework, including IT general controls")
    pdf.bullet("Identification and evaluation of fraud risk factors in accordance with SAS 99/AU-C 240")
    pdf.bullet("Development of a risk-based audit plan that allocates resources to areas of highest risk and materiality")
    pdf.bullet("Review of prior audit findings, management letter comments, and corrective action plans")
    pdf.bullet("Configuration of Meridian Insight analytics to import and analyze the City's general ledger, payroll, accounts payable, and revenue data")

    pdf.section_heading("Phase 2: Interim Fieldwork (October - November)", level=2)
    pdf.body_text(
        "During interim fieldwork, we perform preliminary testing of internal controls and begin substantive "
        "procedures on transactions occurring through the interim period. This approach allows us to identify "
        "potential issues early and reduces the burden on City staff during year-end."
    )
    pdf.bullet("Testing of key internal controls over financial reporting (revenue recognition, procurement, payroll, cash management)")
    pdf.bullet("Interim substantive testing of high-volume transaction cycles (utility billing, property tax, accounts payable)")
    pdf.bullet("IT general controls testing (access controls, change management, backup and recovery, segregation of duties)")
    pdf.bullet("Review of compliance requirements for major federal programs (Community Development Block Grants, transportation, public safety)")
    pdf.bullet("Progress meeting with Finance Director to discuss preliminary findings and any adjustments to audit plan")

    pdf.section_heading("Phase 3: Year-End Fieldwork (January - February)", level=2)
    pdf.body_text(
        "Year-end fieldwork focuses on completing substantive procedures, confirming account balances, and "
        "evaluating the City's year-end closing process and financial statement preparation."
    )
    pdf.bullet("Confirmation of cash and investment balances with financial institutions and custodians")
    pdf.bullet("Testing of year-end accruals, estimates, and adjustments")
    pdf.bullet("Review of subsequent events through the date of the auditor's report")
    pdf.bullet("Evaluation of the City's component unit relationships and required blending/discrete presentation")
    pdf.bullet("Testing of compliance requirements under Uniform Guidance for each major federal program")
    pdf.bullet("Comprehensive analytics on full-year data using Meridian Insight, including Benford's Law analysis, duplicate payment detection, and vendor relationship mapping")

    pdf.section_heading("Phase 4: Reporting and Delivery (March - April)", level=2)
    pdf.body_text(
        "The final phase encompasses the preparation and delivery of all required reports and communications."
    )
    pdf.bullet("Draft ACFR preparation and review, incorporating GFOA Certificate of Achievement requirements")
    pdf.bullet("Independent auditor's report on the basic financial statements")
    pdf.bullet("Report on internal control over financial reporting and on compliance (Yellow Book)")
    pdf.bullet("Single audit report and schedule of findings and questioned costs (Uniform Guidance)")
    pdf.bullet("Management letter with detailed findings, recommendations, and management responses")
    pdf.bullet("Exit conference and formal presentation to City Council / Audit Committee")

    # --- Team Qualifications ---
    pdf.add_page()
    pdf.section_heading("3. Team Qualifications")
    pdf.section_heading("Engagement Partner: David Rawlings, CPA, CGFM", level=2)
    pdf.body_text(
        "David has 22 years of experience exclusively in governmental auditing. He currently serves as "
        "engagement partner for 14 municipal audit clients, including the City of Aurora (pop. 395,000), "
        "Jefferson County, and the Regional Transportation District. David holds the Certified Government "
        "Financial Manager designation and serves on the AICPA's Government Audit Quality Center Executive "
        "Committee. He personally reviews every audit opinion and management letter issued by his team."
    )
    pdf.section_heading("Engagement Manager: Lisa Nakamura, CPA", level=2)
    pdf.body_text(
        "Lisa brings 15 years of governmental audit experience and will serve as the primary day-to-day "
        "contact for City staff. She specializes in GASB implementation, ACFR preparation, and single "
        "audit compliance. Lisa has managed audits for 9 Colorado municipalities and has a strong track "
        "record of completing engagements on time and within budget."
    )
    pdf.section_heading("Senior Auditor: Marcus Thompson, CPA", level=2)
    pdf.body_text(
        "Marcus has 8 years of experience in public sector auditing, with particular expertise in IT "
        "general controls, data analytics, and federal grant compliance. He leads the on-site fieldwork "
        "team and is responsible for supervising staff auditors and preparing detailed workpapers."
    )
    pdf.section_heading("GASB Technical Specialist: Dr. Rebecca Stein, CPA", level=2)
    pdf.body_text(
        "Rebecca serves as Meridian's national GASB practice leader and will be available as a technical "
        "resource throughout the engagement. She has authored guidance on implementing GASB 87 (Leases), "
        "GASB 96 (IT Subscriptions), and GASB 100/101 (Accounting Changes and Compensated Absences). "
        "She holds a Ph.D. in Accounting from the University of Illinois and previously served on the "
        "GASB's Emerging Issues Task Force."
    )

    # --- Relevant Experience ---
    pdf.add_page()
    pdf.section_heading("4. Relevant Experience")
    pdf.section_heading("City of Aurora, Colorado (Population: 395,000)", level=2)
    pdf.key_value("Engagement Duration", "2018 - Present (8 consecutive years)")
    pdf.key_value("Scope", "ACFR preparation, financial audit, single audit, pension audit")
    pdf.key_value("Team Size", "8-10 professionals during peak fieldwork")
    pdf.body_text(
        "Meridian has served as the City of Aurora's independent auditor since 2018, consistently "
        "delivering the completed ACFR within 120 days of fiscal year-end. The City has received the "
        "GFOA Certificate of Achievement for Excellence in Financial Reporting for all eight years. "
        "We successfully guided the City through implementation of GASB 87 (Leases), identifying over "
        "$45 million in previously unrecognized lease liabilities, and GASB 96 (IT Subscriptions). "
        "Our data analytics program detected $380,000 in duplicate vendor payments during FY2023, "
        "which the City recovered in full."
    )
    pdf.section_heading("Jefferson County, Colorado (Population: 582,000)", level=2)
    pdf.key_value("Engagement Duration", "2020 - Present (6 consecutive years)")
    pdf.key_value("Scope", "Financial audit, single audit, component unit audits (5 entities)")
    pdf.body_text(
        "Jefferson County's complex organizational structure includes five component units requiring "
        "discrete presentation. Meridian coordinates audit procedures across all entities and delivers "
        "a consolidated ACFR that meets both County and component unit reporting requirements. We have "
        "consistently identified opportunities to strengthen internal controls, including recommendations "
        "that led to the County's implementation of a new enterprise procurement system."
    )
    pdf.section_heading("City and County of Denver, Colorado (Population: 715,000)", level=2)
    pdf.key_value("Engagement Duration", "2015 - 2022 (8 years)")
    pdf.key_value("Scope", "Financial audit, single audit, Denver International Airport audit")
    pdf.body_text(
        "Meridian served as Denver's independent auditor for eight years, including the separate audit "
        "of Denver International Airport, a $3.2 billion enterprise fund. Our engagement team included "
        "specialists in aviation revenue accounting, bond covenant compliance, and federal aviation "
        "grant requirements. During our tenure, Denver received the GFOA Certificate of Achievement "
        "every year and was recognized for outstanding financial reporting by the National Council on "
        "Governmental Accounting."
    )

    # --- Pricing ---
    pdf.add_page()
    pdf.section_heading("5. Fee Proposal")
    pdf.body_text(
        "Meridian proposes a fixed annual fee for the comprehensive audit engagement, inclusive of all "
        "professional services described in this proposal. The fee structure reflects our commitment to "
        "providing exceptional value while maintaining the highest quality standards."
    )
    pdf.section_heading("Annual Fee Schedule", level=2)
    pdf.redacted_text("Year 1 (FY2025) - Comprehensive Audit")
    pdf.redacted_text("Year 2 (FY2026) - Comprehensive Audit")
    pdf.redacted_text("Year 3 (FY2027) - Comprehensive Audit")
    pdf.redacted_text("Year 4 (FY2028) - Comprehensive Audit")
    pdf.redacted_text("Year 5 (FY2029) - Comprehensive Audit")
    pdf.ln(2)
    pdf.redacted_text("Total Five-Year Contract Value")
    pdf.ln(4)
    pdf.section_heading("Fee Assumptions and Inclusions", level=2)
    pdf.bullet("All professional fees, including partner, manager, senior, and staff time")
    pdf.bullet("ACFR preparation and review (up to two rounds of revisions)")
    pdf.bullet("Single audit of up to 4 major federal programs per year")
    pdf.bullet("Management letter preparation and presentation")
    pdf.bullet("Up to 40 hours of GASB technical consultation annually at no additional charge")
    pdf.bullet("All travel, technology, and administrative expenses")
    pdf.bullet("Annual fee escalation not to exceed 3% per year for Years 2-5")
    pdf.ln(2)
    pdf.body_text(
        "Note: Pricing for additional services beyond the base scope (e.g., bond offering comfort letters, "
        "agreed-upon procedures, additional component unit audits) will be quoted separately at standard "
        "hourly rates, subject to City approval prior to commencement."
    )

    pdf.output(os.path.join(OUTPUT_DIR, "past_proposal_financial_audit.pdf"))
    print("  Created: past_proposal_financial_audit.pdf")


# ============================================================================
# 2. ERP Implementation Advisory Proposal (Healthcare)
# ============================================================================

def generate_erp_implementation_proposal():
    pdf = MeridianPDF(
        "Proposal for ERP Implementation\nAdvisory Services",
        "Statewide Health System - RFP #IT-2025-118",
        client_confidential=True
    )
    pdf.cover_page(version="1.0", date="July 2025")

    # --- Cover Letter ---
    pdf.add_page()
    pdf.section_heading("Cover Letter")
    pdf.body_text("July 15, 2025")
    pdf.ln(2)
    pdf.body_text(
        "Mr. Robert Patel, Chief Information Officer\n"
        "Statewide Health System\n"
        "1200 Medical Center Drive, Suite 400\n"
        "Columbus, OH 43210"
    )
    pdf.ln(2)
    pdf.body_text("Dear Mr. Patel,")
    pdf.body_text(
        "Meridian & Associates LLP is pleased to present our proposal in response to RFP #IT-2025-118 "
        "for Enterprise Resource Planning (ERP) Implementation Advisory Services. We understand that "
        "Statewide Health System is embarking on a comprehensive ERP modernization initiative to replace "
        "aging financial, supply chain, and human capital management systems across your 12-hospital network "
        "and 85 ambulatory care facilities."
    )
    pdf.body_text(
        "This is precisely the type of complex, mission-critical transformation where Meridian excels. Our "
        "Healthcare Technology Advisory practice has guided 28 health systems through ERP implementations "
        "over the past decade, representing a combined program value exceeding $1.4 billion. We bring "
        "deep expertise in the unique challenges of healthcare ERP -- from clinical-financial integration "
        "to regulatory compliance, from supply chain optimization to workforce management."
    )
    pdf.body_text(
        "Our proposed engagement lead, Michael Torres, CPA, PMP, has personally overseen 9 healthcare ERP "
        "implementations and brings 24 years of healthcare advisory experience. He will be supported by "
        "a multidisciplinary team of ERP specialists, change management consultants, and healthcare "
        "operations experts."
    )
    pdf.body_text(
        "We look forward to the opportunity to serve as Statewide Health System's trusted advisor on this "
        "transformative initiative."
    )
    pdf.ln(4)
    pdf.body_text(
        "Sincerely,\n\n"
        "Michael Torres, CPA, PMP\n"
        "Lead Partner, Healthcare & Life Sciences Practice\n"
        "Meridian & Associates LLP\n"
        "Phone: (312) 555-0287\n"
        "Email: m.torres@meridian-llp.com"
    )

    # --- Executive Summary ---
    pdf.add_page()
    pdf.section_heading("1. Executive Summary")
    pdf.body_text(
        "Statewide Health System's current IT landscape includes a patchwork of legacy systems -- a 15-year-old "
        "financial management system (Lawson), separate supply chain platforms for acute and ambulatory settings, "
        "multiple time-and-attendance systems, and over 200 custom integrations. This fragmentation creates "
        "significant operational inefficiencies, limits real-time visibility, and increases compliance risk."
    )
    pdf.body_text(
        "Meridian proposes to serve as the independent ERP Advisory Partner, providing end-to-end program "
        "oversight from vendor selection through go-live and stabilization. Our role is distinct from and "
        "independent of the ERP implementation vendor, ensuring Statewide Health System has an objective "
        "advocate focused solely on your interests throughout the program."
    )
    pdf.section_heading("Scope of Advisory Services", level=2)
    pdf.bullet("ERP Vendor Evaluation and Selection: Structured evaluation of shortlisted vendors (Oracle Health, Workday, Infor) using weighted scoring methodology")
    pdf.bullet("Program Governance and PMO: Establish governance framework, program management office, and executive reporting cadence")
    pdf.bullet("Business Process Redesign: Facilitate redesign of 140+ business processes across Finance, Supply Chain, HR, and Payroll")
    pdf.bullet("Data Migration Strategy: Develop comprehensive data migration plan, including data cleansing, mapping, validation, and cutover")
    pdf.bullet("Integration Architecture: Design and oversee integration strategy for 45+ interfacing systems (Epic EHR, Kronos, Workday Adaptive, etc.)")
    pdf.bullet("Change Management and Training: Enterprise-wide change management program covering 18,000 end users across 97 locations")
    pdf.bullet("Risk Management: Continuous risk monitoring, issue escalation, and mitigation planning")
    pdf.bullet("Quality Assurance and Testing: Independent testing oversight including UAT, integration testing, performance testing, and parallel processing")
    pdf.bullet("Go-Live Support and Stabilization: On-site support during cutover weekends and 90-day post-go-live stabilization period")

    # --- Approach ---
    pdf.add_page()
    pdf.section_heading("2. Methodology and Approach")
    pdf.section_heading("Phase 1: Discovery and Vendor Selection (Months 1-4)", level=2)
    pdf.body_text(
        "Our discovery phase begins with a comprehensive assessment of Statewide Health System's current "
        "state, including detailed process documentation, pain point analysis, and requirements gathering "
        "across all functional areas. We conduct stakeholder interviews with 80+ department leaders and "
        "super-users to understand both stated and latent requirements."
    )
    pdf.body_text(
        "For vendor selection, we employ Meridian's proprietary Healthcare ERP Evaluation Framework, which "
        "evaluates vendors across 12 dimensions including functional fit, technical architecture, healthcare "
        "regulatory compliance, total cost of ownership, implementation risk, and vendor financial stability. "
        "We facilitate structured vendor demonstrations using scenario-based scripts tailored to Statewide's "
        "operations, and conduct reference checks with comparable health systems."
    )

    pdf.section_heading("Phase 2: Program Planning and Design (Months 5-8)", level=2)
    pdf.body_text(
        "Once a vendor is selected, we establish the program governance structure, detailed project plans, "
        "and begin the business process redesign effort. Our approach to process redesign follows the "
        "'adopt, adapt, enhance' philosophy -- leveraging ERP best practices wherever possible, adapting "
        "to Statewide-specific requirements only where clinically or operationally necessary, and enhancing "
        "processes through automation and workflow optimization."
    )
    pdf.bullet("Establish Program Steering Committee with executive sponsorship from CFO, CIO, CHRO, and CMO")
    pdf.bullet("Create detailed work breakdown structure with 1,200+ activities across 18 workstreams")
    pdf.bullet("Facilitate 40+ business process redesign workshops across Finance, Supply Chain, HR/Payroll")
    pdf.bullet("Develop data migration strategy covering 8 source systems and 15+ years of historical data")
    pdf.bullet("Design integration architecture for bidirectional interfaces with Epic (ADT, charges, clinical documentation)")

    pdf.section_heading("Phase 3: Build and Configure (Months 9-16)", level=2)
    pdf.body_text(
        "During the build phase, Meridian provides independent quality assurance oversight of the "
        "implementation vendor's configuration, development, and testing activities. We conduct weekly "
        "technical reviews, monitor milestone completion, and escalate risks to the Steering Committee."
    )
    pdf.bullet("Weekly QA reviews of configuration decisions against approved business process designs")
    pdf.bullet("Independent code review of custom extensions, reports, and interfaces")
    pdf.bullet("Monthly program health assessments using Meridian's ERP Program Risk Index (PRI)")
    pdf.bullet("Bi-weekly executive status reports with red/amber/green dashboard")
    pdf.bullet("Change management activities: stakeholder engagement, communications, role-based training curriculum design")

    pdf.section_heading("Phase 4: Testing and Validation (Months 17-20)", level=2)
    pdf.body_text(
        "Meridian designs and oversees the comprehensive testing strategy, including system integration "
        "testing (SIT), user acceptance testing (UAT), performance testing, security testing, and parallel "
        "processing. We provide independent test result validation and defect triage support."
    )

    pdf.section_heading("Phase 5: Go-Live and Stabilization (Months 21-24)", level=2)
    pdf.body_text(
        "Our go-live approach employs a phased rollout strategy -- beginning with the corporate office and "
        "two pilot hospitals before expanding to the full 12-hospital network. This approach reduces risk "
        "while allowing the team to incorporate lessons learned from each deployment wave."
    )

    # --- Team ---
    pdf.add_page()
    pdf.section_heading("3. Team Qualifications")
    pdf.section_heading("Engagement Lead: Michael Torres, CPA, PMP", level=2)
    pdf.key_value("Experience", "24 years in healthcare advisory, 9 ERP implementations")
    pdf.key_value("Relevant Clients", "Regional Health Corp (12 hospitals), Pacific Medical Centers (8 hospitals), University Health System")
    pdf.body_text(
        "Michael will serve as the engagement partner and primary executive relationship manager. He will "
        "participate in all Steering Committee meetings and provide strategic guidance throughout the program."
    )

    pdf.section_heading("Program Director: Jennifer Walsh, PMP, CPHIMS", level=2)
    pdf.key_value("Experience", "18 years in healthcare IT advisory, 6 ERP implementations as program director")
    pdf.body_text(
        "Jennifer will serve as the full-time on-site program director, responsible for day-to-day management "
        "of Meridian's advisory team and coordination with the implementation vendor. She recently completed "
        "a 22-month Oracle Health Financials implementation at a 9-hospital system in the Southeast."
    )

    pdf.section_heading("Supply Chain Lead: Marcus Chen, CSCP", level=2)
    pdf.key_value("Experience", "14 years in healthcare supply chain optimization")
    pdf.body_text(
        "Marcus specializes in healthcare supply chain transformation, including item master optimization, "
        "par level management, and clinical preference item standardization. He will lead the supply chain "
        "workstream and integration with clinical systems."
    )

    pdf.section_heading("Change Management Lead: Dr. Amanda Foster, PROSCI", level=2)
    pdf.key_value("Experience", "16 years in organizational change management, 11 in healthcare")
    pdf.body_text(
        "Amanda holds a doctorate in Organizational Psychology and is a certified PROSCI change management "
        "practitioner. She has led change management for 5 healthcare ERP programs, developing training "
        "programs for organizations with up to 25,000 end users."
    )

    # --- Relevant Experience ---
    pdf.add_page()
    pdf.section_heading("4. Relevant Experience")

    pdf.section_heading("Regional Health Corporation (12 Hospitals, 22,000 Employees)", level=2)
    pdf.key_value("Engagement", "ERP Advisory Services for Oracle Cloud Financials and SCM Implementation")
    pdf.key_value("Duration", "26 months (completed March 2025)")
    pdf.key_value("Program Budget", "[REDACTED]")
    pdf.body_text(
        "Meridian served as the independent advisory partner for Regional Health's enterprise-wide Oracle "
        "Cloud implementation. The program encompassed General Ledger, Accounts Payable, Procurement, "
        "Inventory Management, and Fixed Assets across all 12 hospitals and 45 ambulatory locations. "
        "Key outcomes include: on-time go-live for all three deployment waves, 99.7% data migration "
        "accuracy, 22% reduction in purchase order cycle time, and $8.5M in identified cost savings "
        "through supply chain standardization."
    )

    pdf.section_heading("Pacific Medical Centers (8 Hospitals, 15,000 Employees)", level=2)
    pdf.key_value("Engagement", "Workday HCM/Payroll Implementation Advisory")
    pdf.key_value("Duration", "18 months (completed November 2024)")
    pdf.key_value("Program Budget", "[REDACTED]")
    pdf.body_text(
        "Advised Pacific Medical Centers on the implementation of Workday HCM and Payroll, replacing "
        "three legacy HR systems and two payroll platforms. Meridian provided program governance, change "
        "management, and integration oversight for the complex interface between Workday and Kronos "
        "Workforce Dimensions (scheduling and timekeeping). The program achieved first-payroll accuracy "
        "of 99.94% and reduced payroll processing time by 40%."
    )

    pdf.section_heading("University Health System (Academic Medical Center, 8,500 Employees)", level=2)
    pdf.key_value("Engagement", "ERP Vendor Selection and Contract Negotiation")
    pdf.key_value("Duration", "6 months (completed June 2025)")
    pdf.key_value("Negotiated Savings", "[REDACTED]")
    pdf.body_text(
        "Meridian led a structured vendor evaluation process comparing Oracle Health, Workday, and Infor "
        "CloudSuite Healthcare. Our evaluation framework, scenario-based demonstrations, and reference "
        "checks enabled University Health to make a confident selection decision. During contract "
        "negotiation, Meridian's deep knowledge of healthcare ERP pricing models resulted in significant "
        "reductions from the vendor's initial proposal, along with enhanced service-level agreements "
        "and contractual protections."
    )

    # --- Pricing ---
    pdf.add_page()
    pdf.section_heading("5. Investment Summary")
    pdf.body_text(
        "Meridian's advisory fees are structured on a fixed-fee basis by program phase, providing "
        "Statewide Health System with cost certainty and transparency. All fees include travel, "
        "technology, and administrative expenses."
    )
    pdf.section_heading("Fee by Phase", level=2)
    pdf.redacted_text("Phase 1: Discovery and Vendor Selection (4 months)")
    pdf.redacted_text("Phase 2: Program Planning and Design (4 months)")
    pdf.redacted_text("Phase 3: Build and Configure (8 months)")
    pdf.redacted_text("Phase 4: Testing and Validation (4 months)")
    pdf.redacted_text("Phase 5: Go-Live and Stabilization (4 months)")
    pdf.ln(2)
    pdf.redacted_text("Total Advisory Fee (24 months)")
    pdf.ln(4)
    pdf.section_heading("Staffing Summary", level=2)
    pdf.bullet("Engagement Partner: 20% allocation throughout program")
    pdf.bullet("Program Director: 100% on-site allocation throughout program")
    pdf.bullet("Functional Leads (3): 80% allocation during their active phases")
    pdf.bullet("Change Management Lead: 60% allocation Phases 2-5, 100% during go-live")
    pdf.bullet("Staff Consultants (4-6): Variable allocation based on phase requirements")
    pdf.body_text(
        "Note: Staffing levels may be adjusted by mutual agreement based on program needs. "
        "Any material changes to staffing will be communicated and approved through the governance process."
    )

    pdf.output(os.path.join(OUTPUT_DIR, "past_proposal_erp_implementation.pdf"))
    print("  Created: past_proposal_erp_implementation.pdf")


# ============================================================================
# 3. Global Tax Compliance Proposal (Manufacturing)
# ============================================================================

def generate_tax_compliance_proposal():
    pdf = MeridianPDF(
        "Proposal for Global Tax\nCompliance Services",
        "Precision Manufacturing Corp - RFP #TAX-2025-007",
        client_confidential=True
    )
    pdf.cover_page(version="1.0", date="November 2025")

    # --- Cover Letter ---
    pdf.add_page()
    pdf.section_heading("Cover Letter")
    pdf.body_text("November 3, 2025")
    pdf.ln(2)
    pdf.body_text(
        "Ms. Catherine Liu, VP of Tax\n"
        "Precision Manufacturing Corp\n"
        "8900 Industrial Boulevard\n"
        "Milwaukee, WI 53224"
    )
    pdf.ln(2)
    pdf.body_text("Dear Ms. Liu,")
    pdf.body_text(
        "Meridian & Associates LLP is pleased to submit our proposal in response to RFP #TAX-2025-007 "
        "for Global Tax Compliance Services. We understand that Precision Manufacturing Corp seeks a "
        "qualified firm to provide comprehensive income tax compliance, tax provision support, and "
        "transfer pricing documentation services across your operations in 14 countries."
    )
    pdf.body_text(
        "Meridian's International Tax Practice serves over 200 multinational clients, including 35 in "
        "the manufacturing sector. Our integrated global delivery model combines US-based engagement "
        "leadership with local tax professionals in each jurisdiction, ensuring both strategic alignment "
        "and technical accuracy. We leverage our proprietary tax technology platform, Meridian TaxConnect, "
        "to centralize data collection, automate compliance workflows, and provide real-time visibility "
        "into the global compliance calendar."
    )
    pdf.body_text(
        "Our proposed engagement partner, James Worthington, JD, LLM, has 20 years of experience in "
        "international tax compliance for manufacturing companies, including 8 years managing global "
        "compliance programs spanning 20+ jurisdictions."
    )
    pdf.ln(4)
    pdf.body_text(
        "Sincerely,\n\n"
        "James Worthington, JD, LLM\n"
        "Partner, International Tax Practice\n"
        "Meridian & Associates LLP\n"
        "Phone: (414) 555-0331\n"
        "Email: j.worthington@meridian-llp.com"
    )

    # --- Executive Summary ---
    pdf.add_page()
    pdf.section_heading("1. Executive Summary")
    pdf.body_text(
        "Precision Manufacturing Corp operates manufacturing facilities, distribution centers, and sales "
        "offices across 14 countries: United States, Canada, Mexico, Brazil, United Kingdom, Germany, "
        "France, Poland, China, Japan, South Korea, India, Australia, and Singapore. The company's current "
        "tax compliance process involves 6 different local accounting firms, creating coordination challenges, "
        "inconsistent work quality, and limited global visibility."
    )
    pdf.body_text(
        "Meridian proposes a centralized, technology-enabled approach to global tax compliance that will:"
    )
    pdf.bullet("Consolidate all 14 jurisdictions under a single engagement team with unified quality standards")
    pdf.bullet("Reduce compliance preparation time by an estimated 35% through automation and standardized data collection")
    pdf.bullet("Provide real-time dashboard visibility into filing status, deadlines, and risk areas across all jurisdictions")
    pdf.bullet("Ensure consistent transfer pricing documentation that withstands audit scrutiny in all jurisdictions")
    pdf.bullet("Deliver quarterly ASC 740 tax provision support integrated with the compliance process")
    pdf.bullet("Proactively identify tax planning opportunities arising from the compliance work")

    pdf.section_heading("Scope of Services", level=2)
    pdf.bullet("Federal, state, and local income tax compliance for all US entities (parent corporation and 8 domestic subsidiaries)")
    pdf.bullet("International income tax compliance for 13 foreign subsidiaries in 13 jurisdictions")
    pdf.bullet("Transfer pricing documentation: master file, local files for all jurisdictions, and country-by-country reporting (CbCR)")
    pdf.bullet("Quarterly and annual ASC 740 tax provision support, including rate reconciliation and deferred tax analysis")
    pdf.bullet("Sales and use tax compliance for 42 US state/local jurisdictions (estimated 500+ filings annually)")
    pdf.bullet("VAT/GST compliance for 8 non-US jurisdictions")
    pdf.bullet("Tax calendar management and regulatory monitoring across all jurisdictions")

    # --- Approach ---
    pdf.add_page()
    pdf.section_heading("2. Service Delivery Approach")
    pdf.section_heading("Global Coordination Model", level=2)
    pdf.body_text(
        "Meridian employs a hub-and-spoke delivery model centered on a US-based Global Tax Coordination "
        "team. The coordination team manages the overall compliance calendar, standardizes data requests, "
        "performs quality reviews, and serves as Precision's single point of contact. Local compliance "
        "preparation is performed by Meridian professionals in each jurisdiction (or by our vetted "
        "correspondent firms in three jurisdictions: Brazil, South Korea, and Poland), with all work "
        "reviewed by the coordination team before delivery."
    )
    pdf.section_heading("Technology Platform: Meridian TaxConnect", level=2)
    pdf.body_text(
        "TaxConnect is our cloud-based tax compliance management platform that serves as the central "
        "hub for the global engagement. Key features include:"
    )
    pdf.bullet("Centralized Data Portal: Standardized data request templates for each jurisdiction, with automated reminders and progress tracking")
    pdf.bullet("Compliance Calendar: Interactive dashboard showing all filing deadlines, extension dates, estimated payment dates, and completion status")
    pdf.bullet("Document Management: Secure repository for all workpapers, returns, and supporting documentation with version control and audit trail")
    pdf.bullet("Analytics Dashboard: Real-time visibility into effective tax rates, cash tax payments, and transfer pricing margins by jurisdiction")
    pdf.bullet("Provision Integration: Seamless data flow between compliance workpapers and ASC 740 provision calculations")

    pdf.section_heading("Transfer Pricing Documentation", level=2)
    pdf.body_text(
        "Our transfer pricing team prepares OECD-compliant documentation following the three-tiered approach "
        "(master file, local files, and CbCR). We work closely with the compliance team to ensure "
        "consistency between transfer pricing policies and reported results. Our benchmarking analyses "
        "use multiple databases (BvD Orbis, S&P Capital IQ, RoyaltyStat) and are updated annually to "
        "reflect current market conditions."
    )
    pdf.body_text(
        "For Precision's manufacturing operations, we will document intercompany transactions including: "
        "finished goods sales between related entities, raw material procurement through the centralized "
        "purchasing function, management service fees, royalties for licensed manufacturing processes, "
        "and intercompany financing arrangements."
    )

    # --- Team ---
    pdf.add_page()
    pdf.section_heading("3. Team Qualifications")
    pdf.section_heading("Engagement Partner: James Worthington, JD, LLM (Tax)", level=2)
    pdf.key_value("Experience", "20 years in international tax, 8 years managing global compliance programs")
    pdf.key_value("Manufacturing Clients", "12 active manufacturing sector clients spanning 50+ jurisdictions")
    pdf.body_text(
        "James is a recognized authority in international tax compliance for manufacturing companies. "
        "He previously served as VP of Tax at a Fortune 500 manufacturer before joining Meridian, giving "
        "him a unique perspective as both advisor and client. He holds a JD from Georgetown University Law "
        "Center and an LLM in Taxation from New York University School of Law."
    )

    pdf.section_heading("US Tax Director: Sandra Kim, CPA, MST", level=2)
    pdf.key_value("Experience", "16 years in corporate tax compliance")
    pdf.body_text(
        "Sandra oversees all US federal, state, and local income tax compliance. She manages a team of "
        "12 tax professionals and specializes in manufacturing-specific issues including Section 199A "
        "deductions, R&D credits, and IC-DISC structures."
    )

    pdf.section_heading("International Tax Director: Andrew MacPherson, CPA, CA", level=2)
    pdf.key_value("Experience", "18 years in international tax, based in London")
    pdf.body_text(
        "Andrew coordinates international compliance across all 13 foreign jurisdictions. He is dual-qualified "
        "(US CPA and UK Chartered Accountant) and has deep expertise in European tax compliance, BEPS "
        "implementation, and Pillar Two global minimum tax requirements."
    )

    pdf.section_heading("Transfer Pricing Director: Dr. Elena Vasquez, Ph.D.", level=2)
    pdf.key_value("Experience", "15 years in transfer pricing, specializing in manufacturing value chains")
    pdf.body_text(
        "Elena leads the transfer pricing documentation team. She holds a Ph.D. in Economics from MIT "
        "and has successfully defended transfer pricing positions in audits across the US, Germany, China, "
        "and India. She has particular expertise in manufacturing cost-plus structures and intangible "
        "property arrangements."
    )

    # --- Relevant Experience ---
    pdf.add_page()
    pdf.section_heading("4. Relevant Experience")

    pdf.section_heading("Global Industrial Products Company (16 Countries, $4.2B Revenue)", level=2)
    pdf.key_value("Engagement", "Global tax compliance, transfer pricing documentation, tax provision support")
    pdf.key_value("Duration", "2019 - Present (7 consecutive years)")
    pdf.body_text(
        "Meridian provides comprehensive global tax services for this multinational manufacturer of "
        "precision components. We consolidated compliance from 8 prior local firms into a single coordinated "
        "engagement, reducing total compliance costs by 28% while improving quality and timeliness. "
        "Our TaxConnect platform reduced the client's data gathering time by 45%, and our proactive "
        "tax planning identified $12M in cumulative tax savings through supply chain restructuring and "
        "R&D credit optimization."
    )

    pdf.section_heading("Advanced Materials Corporation (11 Countries, $2.8B Revenue)", level=2)
    pdf.key_value("Engagement", "International tax compliance and transfer pricing")
    pdf.key_value("Duration", "2021 - Present (5 consecutive years)")
    pdf.body_text(
        "Meridian manages international compliance and transfer pricing for this specialty materials "
        "manufacturer. Notable achievement: successfully defended the client's transfer pricing methodology "
        "during simultaneous audits in Germany and China, resulting in no adjustments. Our documentation "
        "was cited by the German tax authority as 'thorough and well-supported.'"
    )

    pdf.section_heading("Heritage Automotive Group (9 Countries, $6.1B Revenue)", level=2)
    pdf.key_value("Engagement", "Full-scope global tax compliance transition")
    pdf.key_value("Duration", "2023 - Present (3 years)")
    pdf.body_text(
        "Heritage engaged Meridian to replace their prior Big Four provider, citing dissatisfaction with "
        "responsiveness and partner attention. Meridian completed the transition in 90 days without "
        "missing a single filing deadline. In the first year, we identified $4.2M in overpaid state "
        "income taxes eligible for refund claims, which had been missed by the prior firm."
    )

    # --- Pricing ---
    pdf.add_page()
    pdf.section_heading("5. Fee Proposal")
    pdf.body_text(
        "Meridian proposes a fixed annual fee structure organized by service component, providing "
        "Precision Manufacturing with complete cost transparency and predictability."
    )
    pdf.section_heading("Annual Fee Schedule by Service Component", level=2)
    pdf.redacted_text("US Federal Income Tax Compliance (parent + 8 subsidiaries)")
    pdf.redacted_text("US State and Local Income Tax Compliance (35 state returns)")
    pdf.redacted_text("International Income Tax Compliance (13 jurisdictions)")
    pdf.redacted_text("Transfer Pricing Documentation (master file + 13 local files + CbCR)")
    pdf.redacted_text("ASC 740 Tax Provision Support (quarterly + annual)")
    pdf.redacted_text("Sales and Use Tax Compliance (500+ filings)")
    pdf.redacted_text("International VAT/GST Compliance (8 jurisdictions)")
    pdf.redacted_text("TaxConnect Platform License and Support")
    pdf.ln(2)
    pdf.redacted_text("Total Annual Fee")
    pdf.ln(4)
    pdf.section_heading("Contract Terms", level=2)
    pdf.bullet("Initial term: 3 years with two optional 1-year renewals")
    pdf.bullet("Annual fee escalation: CPI-based, capped at 3%")
    pdf.bullet("Scope adjustments: New jurisdictions or entities added at pre-agreed per-jurisdiction rates")
    pdf.bullet("Out-of-scope services: Tax planning, M&A due diligence, and controversy support billed at standard rates with prior approval")
    pdf.bullet("Service-level commitments: All returns filed a minimum of 5 business days before deadline; provision deliverables within 15 business days of quarter-end")

    pdf.output(os.path.join(OUTPUT_DIR, "past_proposal_tax_compliance.pdf"))
    print("  Created: past_proposal_tax_compliance.pdf")


if __name__ == "__main__":
    generate_financial_audit_proposal()
    generate_erp_implementation_proposal()
    generate_tax_compliance_proposal()
    print("\nAll 3 past proposal PDFs generated successfully!")
