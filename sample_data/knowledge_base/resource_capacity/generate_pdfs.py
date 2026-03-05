"""Generate 2 synthetic resource capacity PDFs for Meridian & Associates LLP."""

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
# 1. Personnel Skills Database
# ============================================================================

def generate_personnel_skills():
    pdf = MeridianPDF(
        "Personnel Skills &\nCertifications Database",
        "Firm-Wide Capabilities Matrix",
        confidential=True
    )
    pdf.cover_page(version="Q1 2026", date="March 2026")

    pdf.add_page()
    pdf.section_heading("1. Overview")
    pdf.body_text(
        "This document provides a comprehensive summary of Meridian & Associates LLP's professional "
        "workforce capabilities, including certifications, technical specializations, industry expertise, "
        "and language skills. The data is current as of March 1, 2026 and is extracted from Meridian's "
        "internal Talent Management System (Workday HCM)."
    )
    pdf.key_value("Total Professional Staff", "68,420")
    pdf.key_value("Partners and Managing Directors", "2,847")
    pdf.key_value("Senior Managers and Directors", "5,214")
    pdf.key_value("Managers", "8,936")
    pdf.key_value("Senior Associates / Senior Consultants", "14,287")
    pdf.key_value("Associates / Staff / Analysts", "37,136")

    pdf.section_heading("2. Professional Certifications Summary")
    pdf.body_text(
        "Meridian maintains a rigorous professional development program that encourages and supports "
        "staff in obtaining industry-recognized certifications. The following reflects the current "
        "certification holdings across the firm:"
    )

    pdf.section_heading("Accounting and Audit Certifications", level=2)
    pdf.bold_bullet("CPA (Certified Public Accountant)", "12,847 professionals across all 50 US states and 6 international jurisdictions")
    pdf.bold_bullet("CA (Chartered Accountant)", "3,218 professionals (UK, Canada, Australia, India, Singapore)")
    pdf.bold_bullet("CIA (Certified Internal Auditor)", "1,456 professionals")
    pdf.bold_bullet("CISA (Certified Information Systems Auditor)", "987 professionals")
    pdf.bold_bullet("CFE (Certified Fraud Examiner)", "624 professionals")
    pdf.bold_bullet("CGFM (Certified Government Financial Manager)", "312 professionals")
    pdf.bold_bullet("CMA (Certified Management Accountant)", "847 professionals")

    pdf.section_heading("Tax Certifications", level=2)
    pdf.bold_bullet("JD / LLM (Tax)", "428 professionals with law degrees and tax specialization")
    pdf.bold_bullet("Enrolled Agent (EA)", "1,124 professionals authorized to represent taxpayers before the IRS")
    pdf.bold_bullet("AICPA Advanced Tax Certificate", "687 professionals")
    pdf.bold_bullet("Transfer Pricing Specialist", "142 professionals with specialized TP credentials")

    pdf.section_heading("Technology and Advisory Certifications", level=2)
    pdf.bold_bullet("PMP (Project Management Professional)", "2,341 professionals")
    pdf.bold_bullet("CISSP (Certified Information Systems Security Professional)", "412 professionals")
    pdf.bold_bullet("CISM (Certified Information Security Manager)", "287 professionals")
    pdf.bold_bullet("AWS Certified Solutions Architect", "534 professionals (Professional: 189, Associate: 345)")
    pdf.bold_bullet("Azure Solutions Architect Expert", "623 professionals")
    pdf.bold_bullet("Google Cloud Professional Architect", "198 professionals")
    pdf.bold_bullet("TOGAF (Enterprise Architecture)", "324 professionals")
    pdf.bold_bullet("SAP Certified (various modules)", "847 professionals")
    pdf.bold_bullet("Oracle Cloud Certified", "412 professionals")
    pdf.bold_bullet("Workday Certified", "287 professionals")
    pdf.bold_bullet("PROSCI Change Management", "456 professionals")
    pdf.bold_bullet("Lean Six Sigma (Green/Black Belt)", "1,287 professionals (Black Belt: 423, Green Belt: 864)")
    pdf.bold_bullet("CBAP (Certified Business Analysis Professional)", "312 professionals")

    pdf.add_page()
    pdf.section_heading("Healthcare and Life Sciences", level=2)
    pdf.bold_bullet("CPHIMS (Certified Professional in Healthcare Information Management)", "187 professionals")
    pdf.bold_bullet("FHIMSS (Fellow, Healthcare Information Management Systems Society)", "42 professionals")
    pdf.bold_bullet("Epic Certified (various modules)", "234 professionals")
    pdf.bold_bullet("CHFP (Certified Healthcare Financial Professional)", "156 professionals")

    pdf.section_heading("Financial Services", level=2)
    pdf.bold_bullet("CFA (Chartered Financial Analyst)", "287 professionals")
    pdf.bold_bullet("FRM (Financial Risk Manager)", "198 professionals")
    pdf.bold_bullet("Series 7 / Series 63", "142 professionals (through Meridian Capital Advisory LLC)")
    pdf.bold_bullet("CRCM (Certified Regulatory Compliance Manager)", "87 professionals")

    pdf.section_heading("3. Industry Expertise Distribution")
    pdf.body_text(
        "Meridian professionals are organized into industry-aligned practice groups. Many professionals "
        "maintain expertise across multiple industries. The following reflects primary industry alignment:"
    )
    pdf.bold_bullet("Financial Services", "12,480 professionals (banking, capital markets, insurance, wealth management)")
    pdf.bold_bullet("Healthcare & Life Sciences", "9,840 professionals (health systems, pharma, medical devices, payers)")
    pdf.bold_bullet("Technology, Media & Telecom", "8,720 professionals")
    pdf.bold_bullet("Manufacturing & Industrial", "7,340 professionals")
    pdf.bold_bullet("Energy & Utilities", "5,280 professionals")
    pdf.bold_bullet("Government & Public Sector", "6,420 professionals (federal, state/local, higher education)")
    pdf.bold_bullet("Consumer & Retail", "5,640 professionals")
    pdf.bold_bullet("Real Estate & Construction", "3,480 professionals")
    pdf.bold_bullet("Nonprofit & Social Enterprise", "2,120 professionals")
    pdf.bold_bullet("Cross-Industry / Not Aligned", "7,100 professionals")

    pdf.add_page()
    pdf.section_heading("4. Technical Skills Matrix")
    pdf.body_text(
        "The following summarizes key technical skills across the firm's consulting and advisory practices, "
        "based on self-reported skills verified through project experience and assessment."
    )

    pdf.section_heading("Data & Analytics", level=2)
    pdf.bold_bullet("SQL / Database Management", "8,420 professionals (advanced: 3,240)")
    pdf.bold_bullet("Python / R for Data Science", "4,870 professionals")
    pdf.bold_bullet("Tableau / Power BI", "6,340 professionals")
    pdf.bold_bullet("Machine Learning / AI", "2,180 professionals")
    pdf.bold_bullet("Data Engineering (Spark, Databricks, Snowflake)", "1,840 professionals")

    pdf.section_heading("ERP and Enterprise Systems", level=2)
    pdf.bold_bullet("SAP S/4HANA", "3,420 professionals (Functional: 2,180, Technical: 1,240)")
    pdf.bold_bullet("Oracle Cloud (ERP, HCM, SCM)", "2,640 professionals")
    pdf.bold_bullet("Workday (HCM, Financials)", "1,870 professionals")
    pdf.bold_bullet("Microsoft Dynamics 365", "1,240 professionals")
    pdf.bold_bullet("ServiceNow", "980 professionals")

    pdf.section_heading("Cloud & Infrastructure", level=2)
    pdf.bold_bullet("Microsoft Azure", "4,280 professionals")
    pdf.bold_bullet("Amazon Web Services (AWS)", "3,640 professionals")
    pdf.bold_bullet("Google Cloud Platform (GCP)", "1,420 professionals")
    pdf.bold_bullet("Kubernetes / Container Orchestration", "1,840 professionals")
    pdf.bold_bullet("Infrastructure as Code (Terraform, ARM, CDK)", "1,280 professionals")

    pdf.section_heading("Cybersecurity", level=2)
    pdf.bold_bullet("Security Architecture & Engineering", "1,420 professionals")
    pdf.bold_bullet("Penetration Testing / Ethical Hacking", "487 professionals")
    pdf.bold_bullet("Incident Response & Forensics", "342 professionals")
    pdf.bold_bullet("Identity & Access Management", "624 professionals")
    pdf.bold_bullet("Cloud Security", "847 professionals")
    pdf.bold_bullet("GRC (Governance, Risk, Compliance)", "1,640 professionals")

    pdf.add_page()
    pdf.section_heading("5. Language Capabilities")
    pdf.body_text(
        "Meridian's global workforce is highly multilingual, enabling effective service delivery "
        "across jurisdictions and cultures:"
    )
    pdf.bold_bullet("English", "68,420 (100% -- firm working language)")
    pdf.bold_bullet("Mandarin Chinese", "4,280 professionals")
    pdf.bold_bullet("Spanish", "5,840 professionals")
    pdf.bold_bullet("Hindi / Urdu", "8,420 professionals")
    pdf.bold_bullet("Japanese", "1,240 professionals")
    pdf.bold_bullet("German", "2,140 professionals")
    pdf.bold_bullet("French", "3,420 professionals")
    pdf.bold_bullet("Portuguese", "1,640 professionals")
    pdf.bold_bullet("Korean", "840 professionals")
    pdf.bold_bullet("Arabic", "620 professionals")

    pdf.section_heading("6. Geographic Distribution")
    pdf.body_text(
        "Meridian professionals are located across 42 countries, with the following regional distribution:"
    )
    pdf.bold_bullet("Americas", "38,420 professionals (US: 32,840, Canada: 2,840, Latin America: 2,740)")
    pdf.bold_bullet("EMEA", "18,640 professionals (UK: 6,420, Continental Europe: 7,840, Middle East/Africa: 4,380)")
    pdf.bold_bullet("Asia-Pacific", "11,360 professionals (India: 5,240, Greater China: 2,840, ANZ: 1,480, SE Asia: 1,800)")

    pdf.section_heading("7. Data Currency and Maintenance")
    pdf.body_text(
        "This skills database is maintained through Meridian's Talent Management System (Workday HCM) "
        "and is updated continuously as professionals complete certifications, training programs, and "
        "engagement experiences. The data presented in this document represents a point-in-time snapshot "
        "as of March 1, 2026. For the most current data or customized skills queries for a specific "
        "RFP response, contact the Talent Strategy Office at talent@meridian-llp.com."
    )

    pdf.output(os.path.join(OUTPUT_DIR, "personnel_skills_database.pdf"))
    print("  Created: personnel_skills_database.pdf")


# ============================================================================
# 2. Team Capacity Overview
# ============================================================================

def generate_team_capacity():
    pdf = MeridianPDF(
        "Team Capacity &\nUtilization Overview",
        "Q1 2026 Resource Planning Report",
        confidential=True
    )
    pdf.cover_page(version="Q1 2026", date="March 2026")

    pdf.add_page()
    pdf.section_heading("1. Executive Summary")
    pdf.body_text(
        "This report provides a summary of Meridian & Associates LLP's current workforce utilization "
        "rates, available capacity by practice area, and bench strength analysis. The data is intended "
        "to support RFP response teams in accurately representing the firm's ability to staff new "
        "engagements. Data is current as of February 28, 2026."
    )
    pdf.body_text(
        "Overall firm utilization for Q4 FY2025 was 76.8%, within our target range of 75-80%. "
        "The firm has meaningful available capacity across all practice areas, with particular depth "
        "in Advisory/Consulting and Tax Services. Seasonal patterns in audit utilization (busy season "
        "January-April) are reflected in the practice-level data below."
    )

    pdf.section_heading("2. Firm-Wide Utilization Summary (Q4 FY2025)")
    pdf.key_value("Firm-Wide Utilization Rate", "76.8%")
    pdf.key_value("Target Utilization Range", "75% - 80%")
    pdf.key_value("Total Chargeable Hours (Q4)", "18,420,000 hours")
    pdf.key_value("Available Capacity Hours (Q4)", "5,580,000 hours")
    pdf.key_value("Total Headcount", "68,420 professionals")
    pdf.key_value("Net Hiring (Q4)", "+1,240 professionals (1,840 hires, 600 departures)")

    pdf.section_heading("3. Utilization by Practice Area")

    pdf.section_heading("3.1 Audit & Assurance", level=2)
    pdf.key_value("Headcount", "22,140 professionals")
    pdf.key_value("Q4 Utilization", "72.4% (note: off-peak; Q1 utilization typically 88-92%)")
    pdf.key_value("Available Capacity (Q2-Q4 FY2026)", "Moderate -- approximately 4,200 FTEs available for new work")
    pdf.body_text(
        "The Audit & Assurance practice follows a well-established seasonal cycle. January through "
        "April represents peak busy season with utilization rates of 88-92%. Post-busy season "
        "(May through December), utilization typically ranges from 68-75%, creating meaningful "
        "capacity for new engagements, particularly those with summer or fall start dates."
    )
    pdf.section_heading("Capacity by Sub-Practice", level=3)
    pdf.bold_bullet("Financial Statement Audit (SEC Registrants)", "Limited availability Q1; moderate availability Q2-Q4 (est. 1,200 FTEs)")
    pdf.bold_bullet("Financial Statement Audit (Private Companies)", "Moderate availability year-round (est. 800 FTEs)")
    pdf.bold_bullet("Government Audit", "Available -- 420 FTEs with CGFM/Yellow Book qualifications available for new engagements")
    pdf.bold_bullet("Internal Audit & Co-Sourcing", "Available -- 640 FTEs, strong bench for new internal audit mandates")
    pdf.bold_bullet("IT Audit & SOC Reporting", "Available -- 380 FTEs with CISA/CISSP credentials")
    pdf.bold_bullet("Employee Benefit Plan Audit", "Seasonal (peak July-October); available November-June (est. 280 FTEs)")

    pdf.add_page()
    pdf.section_heading("3.2 Tax Services", level=2)
    pdf.key_value("Headcount", "16,840 professionals")
    pdf.key_value("Q4 Utilization", "74.2% (note: between extension season and year-end planning)")
    pdf.key_value("Available Capacity (Q2-Q4 FY2026)", "Significant -- approximately 3,800 FTEs available")
    pdf.body_text(
        "Tax Services experiences two peak periods: the spring filing season (February-April, utilization "
        "85-90%) and the fall extension season (September-October, utilization 82-86%). Between peaks, "
        "meaningful capacity exists for tax planning, compliance onboarding, and advisory projects."
    )
    pdf.section_heading("Capacity by Sub-Practice", level=3)
    pdf.bold_bullet("Corporate Income Tax Compliance", "Moderate availability off-peak (est. 1,400 FTEs)")
    pdf.bold_bullet("International Tax", "Available -- 620 FTEs including transfer pricing specialists")
    pdf.bold_bullet("State & Local Tax (SALT)", "Available -- 840 FTEs across all US regions")
    pdf.bold_bullet("Indirect Tax (Sales/Use, VAT/GST)", "Available -- 480 FTEs")
    pdf.bold_bullet("Tax Technology & Transformation", "Available -- 320 FTEs with tax technology platform experience")
    pdf.bold_bullet("Private Client / High Net Worth", "Limited -- near capacity, selective new client acceptance")

    pdf.section_heading("3.3 Advisory & Consulting", level=2)
    pdf.key_value("Headcount", "24,280 professionals")
    pdf.key_value("Q4 Utilization", "78.6%")
    pdf.key_value("Available Capacity (FY2026)", "Strong -- approximately 5,200 FTEs available for new engagements")
    pdf.body_text(
        "The Advisory & Consulting practice maintains relatively stable utilization throughout the year "
        "without significant seasonal variation. Current pipeline analysis indicates strong demand in "
        "digital transformation, cloud migration, and regulatory compliance, with available capacity "
        "across most sub-practices."
    )
    pdf.section_heading("Capacity by Sub-Practice", level=3)
    pdf.bold_bullet("Strategy & Operations", "Available -- 840 FTEs across all industries")
    pdf.bold_bullet("Technology Consulting", "Available -- 1,420 FTEs (cloud, ERP, data & analytics)")
    pdf.bold_bullet("Risk Advisory", "Available -- 680 FTEs (regulatory, operational, cyber risk)")
    pdf.bold_bullet("Financial Advisory / M&A", "Moderate -- 420 FTEs available, pipeline dependent")
    pdf.bold_bullet("Digital Transformation", "Available -- 780 FTEs (agile, product, UX/UI, DevOps)")
    pdf.bold_bullet("Change Management & Org Design", "Available -- 340 FTEs")
    pdf.bold_bullet("Cybersecurity Services", "Available -- 520 FTEs, growing practice with active hiring")
    pdf.bold_bullet("Supply Chain & Operations", "Available -- 280 FTEs")

    pdf.add_page()
    pdf.section_heading("3.4 Managed Services", level=2)
    pdf.key_value("Headcount", "5,160 professionals")
    pdf.key_value("Q4 Utilization", "84.2% (highest across firm)")
    pdf.key_value("Available Capacity", "Limited -- selective capacity for new managed service contracts")
    pdf.body_text(
        "Managed Services operates at consistently high utilization due to the recurring, contracted "
        "nature of the work. New managed service engagements typically require a 60-90 day ramp-up "
        "period for recruitment and onboarding of dedicated staff."
    )

    pdf.section_heading("4. Bench Strength and Rapid Mobilization")
    pdf.body_text(
        "Meridian maintains a structured approach to bench management and rapid team mobilization "
        "for new engagements:"
    )
    pdf.section_heading("Strategic Bench", level=2)
    pdf.body_text(
        "Approximately 4,800 professionals (7% of total staff) are currently on the strategic bench -- "
        "between engagements and available for immediate deployment. Bench professionals remain "
        "productive through internal projects, training, and proposal support. Average time on bench "
        "is 3.2 weeks."
    )
    pdf.section_heading("Rapid Mobilization Capabilities", level=2)
    pdf.bullet("Small engagements (2-5 FTEs): Team assembled and on-site within 2 weeks")
    pdf.bullet("Medium engagements (6-20 FTEs): Team assembled within 3-4 weeks")
    pdf.bullet("Large engagements (21-50 FTEs): Team assembled within 4-6 weeks")
    pdf.bullet("Major programs (50+ FTEs): Dedicated mobilization team, 6-8 weeks for full staffing")
    pdf.body_text(
        "Mobilization timelines assume standard engagement parameters. Engagements requiring niche "
        "skills, specific certifications, or security clearances may require additional lead time."
    )

    pdf.section_heading("5. Hiring and Growth Plan (FY2026)")
    pdf.body_text(
        "Meridian's FY2026 hiring plan supports both replacement needs and strategic growth investments:"
    )
    pdf.key_value("Total Planned Hires (FY2026)", "8,400 professionals")
    pdf.key_value("Campus / Entry Level", "3,200 (38% of hires)")
    pdf.key_value("Experienced Hires", "4,400 (52% of hires)")
    pdf.key_value("Lateral Partner / MD Hires", "120 (1.5% of hires)")
    pdf.key_value("Contingent / Contract", "680 (8.5% of hires)")
    pdf.ln(2)
    pdf.section_heading("Strategic Growth Areas", level=2)
    pdf.bullet("Cybersecurity Services: +320 net new hires (25% practice growth)")
    pdf.bullet("Cloud & Data Engineering: +280 net new hires (18% practice growth)")
    pdf.bullet("AI/ML Advisory: +180 net new hires (new sub-practice launch)")
    pdf.bullet("ESG Assurance & Advisory: +140 net new hires (regulatory demand driven)")
    pdf.bullet("Healthcare IT Advisory: +120 net new hires (EHR modernization demand)")

    pdf.add_page()
    pdf.section_heading("6. Subcontractor and Alliance Partner Capacity")
    pdf.body_text(
        "In addition to internal resources, Meridian maintains relationships with vetted subcontractor "
        "firms and technology alliance partners that can augment capacity for large or specialized "
        "engagements:"
    )
    pdf.bold_bullet("Preferred Subcontractor Network", "14 pre-qualified firms with master subcontract agreements, providing access to approximately 8,000 additional professionals")
    pdf.bold_bullet("Offshore Delivery Centers", "Meridian-owned centers in Bangalore (2,400 staff), Hyderabad (1,800 staff), and Manila (1,200 staff) provide cost-effective delivery for analytics, testing, and managed services")
    pdf.bold_bullet("Technology Alliance Partners", "Strategic partnerships with Microsoft, AWS, Google Cloud, SAP, Oracle, Workday, ServiceNow, and Salesforce provide access to partner resources and co-delivery capabilities")
    pdf.bold_bullet("Academic Partnerships", "Relationships with 45 universities for specialized research, internship pipelines, and faculty consulting arrangements")

    pdf.section_heading("7. Contact for Resource Inquiries")
    pdf.body_text(
        "For specific resource availability inquiries related to an RFP response or new engagement "
        "opportunity, please contact:"
    )
    pdf.ln(2)
    pdf.body_text(
        "Rachel Morrison\n"
        "Chief Talent Officer\n"
        "Meridian & Associates LLP\n"
        "Email: r.morrison@meridian-llp.com\n"
        "Phone: (212) 555-0234"
    )
    pdf.ln(2)
    pdf.body_text(
        "Resource requests for specific RFP proposals should be submitted through the Pursuit Resource "
        "Request (PRR) system in Meridian WorkStream, with a minimum 10-business-day lead time for "
        "team identification and availability confirmation."
    )

    pdf.output(os.path.join(OUTPUT_DIR, "team_capacity_overview.pdf"))
    print("  Created: team_capacity_overview.pdf")


if __name__ == "__main__":
    generate_personnel_skills()
    generate_team_capacity()
    print("\nAll 2 resource capacity PDFs generated successfully!")
