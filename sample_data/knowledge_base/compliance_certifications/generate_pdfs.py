"""Generate 3 synthetic compliance & certification PDFs for Meridian & Associates LLP."""

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
# 1. SOC 2 Type II Audit Summary
# ============================================================================

def generate_soc2_summary():
    pdf = MeridianPDF(
        "SOC 2 Type II Examination Report",
        "Summary for RFP Response Use",
        confidential=True
    )
    pdf.cover_page(version="2.1", date="January 2026")

    pdf.add_page()
    pdf.section_heading("1. Report Overview")
    pdf.body_text(
        "This document summarizes the results of Meridian & Associates LLP's System and Organization "
        "Controls (SOC 2) Type II examination for the period January 1, 2025 through December 31, 2025. "
        "The examination was conducted by Whitfield & Crane LLP, an independent CPA firm registered with "
        "the AICPA and specializing in SOC examinations."
    )
    pdf.key_value("Examination Period", "January 1, 2025 - December 31, 2025")
    pdf.key_value("Report Date", "February 15, 2026")
    pdf.key_value("Service Auditor", "Whitfield & Crane LLP, New York, NY")
    pdf.key_value("Trust Service Criteria", "Security, Availability, Confidentiality, Processing Integrity")
    pdf.key_value("Opinion", "Unqualified (Clean)")
    pdf.key_value("Exceptions Noted", "Zero (0)")

    pdf.add_page()
    pdf.section_heading("2. Scope of Examination")
    pdf.body_text(
        "The SOC 2 Type II examination covered Meridian's information systems, infrastructure, and "
        "operational processes supporting the delivery of professional services to clients. The scope "
        "encompasses the following systems and environments:"
    )
    pdf.section_heading("In-Scope Systems", level=2)
    pdf.bullet("Meridian Client Portal (MCP) -- secure client document exchange and collaboration platform")
    pdf.bullet("Meridian TaxConnect -- cloud-based global tax compliance management platform")
    pdf.bullet("Meridian Insight -- data analytics and audit automation platform")
    pdf.bullet("Meridian WorkStream -- engagement management and workflow platform")
    pdf.bullet("Enterprise email and collaboration (Microsoft 365 E5 with Advanced Compliance)")
    pdf.bullet("Document management system (iManage Work 10 Cloud)")
    pdf.bullet("Financial reporting and audit workpaper systems (CaseWare Cloud, CCH Engagement)")
    pdf.bullet("Corporate network infrastructure across 42 offices globally")
    pdf.bullet("Azure and AWS cloud environments hosting client-facing applications")
    pdf.bullet("Identity and access management (Okta Identity Cloud, CyberArk Privileged Access)")

    pdf.section_heading("In-Scope Facilities", level=2)
    pdf.bullet("Primary data center: Equinix NY5, Secaucus, NJ (Tier IV)")
    pdf.bullet("Secondary data center: CyrusOne Sterling, VA (Tier III+)")
    pdf.bullet("Azure regions: East US 2, West US 2, West Europe, Southeast Asia")
    pdf.bullet("AWS regions: US-East-1, EU-West-1 (disaster recovery)")
    pdf.bullet("Corporate headquarters: New York, NY (120 Meridian Plaza)")
    pdf.bullet("Regional processing centers: Chicago, IL; London, UK; Singapore")

    pdf.add_page()
    pdf.section_heading("3. Trust Service Criteria and Controls")

    pdf.section_heading("3.1 Security", level=2)
    pdf.body_text(
        "The Security criterion addresses the protection of information and systems against unauthorized "
        "access, both physical and logical. Meridian maintains a comprehensive security program governed "
        "by the Chief Information Security Officer (CISO) and the Information Security Steering Committee."
    )
    pdf.section_heading("Key Controls Tested", level=3)
    pdf.bullet("Multi-factor authentication (MFA) required for all user access to production systems, VPN, and client platforms")
    pdf.bullet("Role-based access control (RBAC) with quarterly access reviews and automated deprovisioning within 24 hours of termination")
    pdf.bullet("Network segmentation with micro-segmentation for client engagement environments")
    pdf.bullet("Endpoint detection and response (EDR) on all managed devices with 24/7 SOC monitoring")
    pdf.bullet("Vulnerability management program with monthly scans and critical patches applied within 72 hours")
    pdf.bullet("Annual penetration testing by independent third party (NCC Group)")
    pdf.bullet("Security awareness training with monthly phishing simulations (98.2% pass rate)")
    pdf.bullet("Encrypted communications (TLS 1.3 for data in transit, AES-256 for data at rest)")

    pdf.section_heading("3.2 Availability", level=2)
    pdf.body_text(
        "The Availability criterion addresses whether systems are available for operation and use as "
        "committed or agreed. Meridian maintains published service-level objectives for all client-facing "
        "platforms."
    )
    pdf.section_heading("Key Controls Tested", level=3)
    pdf.bullet("99.95% uptime SLO for client-facing platforms (actual achieved: 99.98% for 2025)")
    pdf.bullet("Automated failover between primary and secondary data centers with RTO < 4 hours, RPO < 1 hour")
    pdf.bullet("Comprehensive backup strategy: hourly incremental, daily full, with 90-day retention and geographic replication")
    pdf.bullet("Annual disaster recovery testing with documented results (last test: October 2025, full recovery in 2.8 hours)")
    pdf.bullet("Real-time infrastructure monitoring with automated alerting (PagerDuty) and documented escalation procedures")
    pdf.bullet("Capacity planning reviews conducted quarterly with 12-month forecasting")

    pdf.section_heading("3.3 Confidentiality", level=2)
    pdf.body_text(
        "The Confidentiality criterion addresses the protection of information designated as confidential. "
        "Given the nature of professional services, Meridian handles extremely sensitive client data "
        "including financial records, tax returns, strategic plans, and personally identifiable information."
    )
    pdf.section_heading("Key Controls Tested", level=3)
    pdf.bullet("Data classification framework with four tiers: Public, Internal, Confidential, Highly Restricted")
    pdf.bullet("Data loss prevention (DLP) controls on email, cloud storage, and endpoint devices")
    pdf.bullet("Client data isolation through dedicated engagement workspaces with unique encryption keys")
    pdf.bullet("Information barriers (ethical walls) for conflicted engagements with automated enforcement")
    pdf.bullet("Secure data destruction with certificate of destruction for physical and electronic media")
    pdf.bullet("Third-party risk management program with annual assessments of critical vendors")
    pdf.bullet("Client confidentiality acknowledged in engagement letters and reinforced through annual firm-wide training")

    pdf.section_heading("3.4 Processing Integrity", level=2)
    pdf.body_text(
        "The Processing Integrity criterion addresses whether system processing is complete, valid, "
        "accurate, timely, and authorized."
    )
    pdf.section_heading("Key Controls Tested", level=3)
    pdf.bullet("Input validation controls on all client-facing data entry interfaces")
    pdf.bullet("Automated reconciliation processes for financial data with exception reporting")
    pdf.bullet("Change management process requiring peer review, testing, and approval before production deployment")
    pdf.bullet("Segregation of duties between development, testing, and production environments")
    pdf.bullet("Automated quality checks in tax compliance workflow (TaxConnect) with dual-review gates")
    pdf.bullet("Audit trail logging for all data modifications with tamper-evident storage")

    pdf.add_page()
    pdf.section_heading("4. Examination Results")
    pdf.body_text(
        "Whitfield & Crane LLP tested 187 individual controls across the four Trust Service Criteria. "
        "The examination included inspection of documentation, observation of processes, re-performance "
        "of controls, and inquiry of responsible personnel."
    )
    pdf.section_heading("Results Summary", level=2)
    pdf.key_value("Total Controls Tested", "187")
    pdf.key_value("Controls Operating Effectively", "187 (100%)")
    pdf.key_value("Exceptions Identified", "0")
    pdf.key_value("Management Assertions Supported", "Yes, for all criteria")
    pdf.key_value("Opinion Type", "Unqualified (Clean)")
    pdf.ln(4)
    pdf.body_text(
        "The service auditor concluded that Meridian & Associates LLP's controls were suitably designed "
        "and operating effectively throughout the examination period to provide reasonable assurance that "
        "Meridian's service commitments and system requirements were achieved based on the Trust Service "
        "Criteria."
    )

    pdf.section_heading("5. Complementary User Entity Controls (CUECs)", level=1)
    pdf.body_text(
        "The effectiveness of Meridian's controls also depends on certain controls being implemented "
        "and operated by client organizations (user entities). Key CUECs include:"
    )
    pdf.bullet("Clients are responsible for managing user access credentials and promptly notifying Meridian of personnel changes")
    pdf.bullet("Clients should implement MFA for their own users accessing Meridian platforms")
    pdf.bullet("Clients are responsible for the accuracy and completeness of data provided to Meridian")
    pdf.bullet("Clients should maintain their own backup procedures for any data not stored on Meridian platforms")
    pdf.bullet("Clients should promptly report any suspected security incidents to Meridian's Security Operations Center")

    pdf.add_page()
    pdf.section_heading("6. Bridge Letter and Continuous Monitoring")
    pdf.body_text(
        "Meridian maintains a continuous monitoring program between SOC 2 examination periods. Key "
        "elements include monthly security metrics reporting to the CISO, quarterly internal control "
        "self-assessments, and continuous automated monitoring of critical controls through our GRC "
        "platform (ServiceNow GRC)."
    )
    pdf.body_text(
        "A bridge letter covering the period from January 1, 2026 to the date of inquiry is available "
        "upon request. The bridge letter is signed by Meridian's CISO and attests that no material "
        "changes have been made to the control environment and no exceptions have been identified since "
        "the last examination period."
    )
    pdf.body_text(
        "For a complete copy of the SOC 2 Type II report, including the detailed description of the "
        "system, the service auditor's tests of controls, and the results of those tests, please "
        "contact the Meridian & Associates LLP Risk Management Office at soc2@meridian-llp.com. "
        "Distribution requires execution of a non-disclosure agreement."
    )

    pdf.output(os.path.join(OUTPUT_DIR, "soc2_type2_summary.pdf"))
    print("  Created: soc2_type2_summary.pdf")


# ============================================================================
# 2. ISO 27001 Certification Summary
# ============================================================================

def generate_iso27001():
    pdf = MeridianPDF(
        "ISO 27001:2022 Certification",
        "Information Security Management System Summary",
        confidential=True
    )
    pdf.cover_page(version="1.3", date="February 2026")

    pdf.add_page()
    pdf.section_heading("1. Certification Overview")
    pdf.body_text(
        "Meridian & Associates LLP holds ISO/IEC 27001:2022 certification for its Information Security "
        "Management System (ISMS). The certification was originally achieved in 2019 under the 2013 "
        "standard and was successfully transitioned to the 2022 revision in October 2025."
    )
    pdf.key_value("Certificate Number", "IS-2025-MER-04821")
    pdf.key_value("Certification Body", "BSI Group (British Standards Institution)")
    pdf.key_value("Standard", "ISO/IEC 27001:2022")
    pdf.key_value("Initial Certification Date", "March 15, 2019")
    pdf.key_value("Current Certificate Valid From", "October 1, 2025")
    pdf.key_value("Certificate Expiry Date", "September 30, 2028")
    pdf.key_value("Last Surveillance Audit", "November 12-14, 2025")
    pdf.key_value("Surveillance Audit Result", "No nonconformities identified")

    pdf.section_heading("2. Scope of Certification")
    pdf.body_text(
        "The ISMS scope covers the provision of audit, tax, advisory, and consulting services, "
        "including the information systems, infrastructure, personnel, and processes supporting "
        "service delivery across the following locations and functions:"
    )
    pdf.section_heading("Certified Locations", level=2)
    pdf.bullet("Global Headquarters: 120 Meridian Plaza, New York, NY 10004")
    pdf.bullet("Americas Regional Office: 200 South Wacker Drive, Chicago, IL 60606")
    pdf.bullet("West Coast Office: 555 California Street, San Francisco, CA 94104")
    pdf.bullet("EMEA Regional Office: 25 Cannon Street, London EC4M 5TA, United Kingdom")
    pdf.bullet("APAC Regional Office: 1 Raffles Place, Singapore 048616")
    pdf.bullet("Technology Center: 2800 Meridian Parkway, Research Triangle Park, NC 27709")
    pdf.bullet("Data Centers: Equinix NY5 (Secaucus, NJ), CyrusOne Sterling (Sterling, VA)")

    pdf.section_heading("Certified Services", level=2)
    pdf.bullet("Financial statement audit and assurance services")
    pdf.bullet("Tax compliance, planning, and advisory services")
    pdf.bullet("Management consulting and advisory services")
    pdf.bullet("Technology consulting and digital transformation services")
    pdf.bullet("Risk advisory and internal audit services")
    pdf.bullet("Client-facing technology platforms (MCP, TaxConnect, Insight, WorkStream)")

    pdf.add_page()
    pdf.section_heading("3. Statement of Applicability")
    pdf.body_text(
        "Meridian's Statement of Applicability (SoA) addresses all 93 controls in Annex A of "
        "ISO/IEC 27001:2022, organized under 4 themes. The following summarizes the applicability "
        "and implementation status:"
    )

    pdf.section_heading("Organizational Controls (37 controls)", level=2)
    pdf.key_value("Applicable", "37 of 37 (100%)")
    pdf.key_value("Implemented", "37 of 37 (100%)")
    pdf.body_text(
        "All organizational controls are applicable and fully implemented. Key controls include: "
        "information security policies (reviewed annually by CISO and approved by Executive Committee), "
        "segregation of duties, contact with authorities (FBI, CISA, ICO, PDPC), threat intelligence "
        "program, information security in project management, and supplier relationship security."
    )

    pdf.section_heading("People Controls (8 controls)", level=2)
    pdf.key_value("Applicable", "8 of 8 (100%)")
    pdf.key_value("Implemented", "8 of 8 (100%)")
    pdf.body_text(
        "People controls include: pre-employment screening (background checks for all hires), "
        "terms and conditions of employment (information security clauses in all employment contracts), "
        "information security awareness and training (mandatory annual training with quarterly updates), "
        "disciplinary process, post-employment responsibilities, and secure remote working policies."
    )

    pdf.section_heading("Physical Controls (14 controls)", level=2)
    pdf.key_value("Applicable", "14 of 14 (100%)")
    pdf.key_value("Implemented", "14 of 14 (100%)")
    pdf.body_text(
        "Physical controls cover: security perimeters and physical entry controls (badge access with "
        "biometric for sensitive areas), securing offices and facilities, monitoring (CCTV with 90-day "
        "retention), protection against environmental threats (fire suppression, UPS, generator backup), "
        "equipment security, secure disposal, and clear desk/clear screen policies."
    )

    pdf.section_heading("Technological Controls (34 controls)", level=2)
    pdf.key_value("Applicable", "34 of 34 (100%)")
    pdf.key_value("Implemented", "34 of 34 (100%)")
    pdf.body_text(
        "Technological controls include: user endpoint devices (MDM-managed with encryption), "
        "privileged access management (CyberArk), access control (Okta with RBAC and MFA), secure "
        "authentication, capacity management, malware protection (CrowdStrike Falcon), vulnerability "
        "management, configuration management, data deletion, data masking, DLP, monitoring, "
        "network security, web filtering, secure coding practices, and cryptographic controls."
    )

    pdf.add_page()
    pdf.section_heading("4. Risk Management Framework")
    pdf.body_text(
        "Meridian's ISMS risk management process follows ISO 31000 principles and is integrated "
        "with the firm's enterprise risk management (ERM) framework. Key elements include:"
    )
    pdf.bullet("Risk assessments conducted annually and upon significant change (M&A, new service line, major technology change)")
    pdf.bullet("Risk register maintained in ServiceNow GRC with 342 identified risks as of December 2025")
    pdf.bullet("Risk appetite statement approved by the Executive Committee and reviewed annually")
    pdf.bullet("Quantitative risk analysis using FAIR (Factor Analysis of Information Risk) methodology for critical risks")
    pdf.bullet("Risk treatment plans with assigned owners, target dates, and progress tracking")
    pdf.bullet("Monthly risk reporting to CISO and quarterly reporting to Executive Committee and Audit Committee")

    pdf.section_heading("5. Continuous Improvement")
    pdf.body_text(
        "Meridian's ISMS is subject to a continuous improvement cycle that includes:"
    )
    pdf.bullet("Internal audit program: 12 internal audits per year covering all ISMS domains on a rolling basis")
    pdf.bullet("Management reviews: Conducted semi-annually by the Information Security Steering Committee")
    pdf.bullet("Corrective actions: Tracked in ServiceNow with root cause analysis and effectiveness verification")
    pdf.bullet("Security metrics program: 45 key performance indicators (KPIs) and key risk indicators (KRIs) tracked monthly")
    pdf.bullet("Lessons learned: Incorporated from security incidents, near-misses, and industry intelligence")
    pdf.bullet("Benchmarking: Annual comparison against NIST CSF, CIS Controls, and industry peers")

    pdf.section_heading("6. Contact Information")
    pdf.body_text(
        "For questions about Meridian's ISO 27001 certification, to request a copy of the certificate, "
        "or to discuss specific security requirements for a prospective engagement, please contact:"
    )
    pdf.ln(2)
    pdf.body_text(
        "Katherine Park, CISSP, CISM\n"
        "Chief Information Security Officer\n"
        "Meridian & Associates LLP\n"
        "Email: k.park@meridian-llp.com\n"
        "Phone: (212) 555-0456"
    )

    pdf.output(os.path.join(OUTPUT_DIR, "iso27001_certification.pdf"))
    print("  Created: iso27001_certification.pdf")


# ============================================================================
# 3. Industry Certifications Overview
# ============================================================================

def generate_certifications_overview():
    pdf = MeridianPDF(
        "Industry Certifications &\nRegistrations Overview",
        "Comprehensive Listing for RFP Response Use",
        confidential=False
    )
    pdf.cover_page(version="5.0", date="January 2026")

    pdf.add_page()
    pdf.section_heading("1. Public Company Accounting Oversight Board (PCAOB)")
    pdf.key_value("Registration Number", "PCAOB #2847")
    pdf.key_value("Initial Registration", "June 14, 2004")
    pdf.key_value("Status", "Active, in good standing")
    pdf.key_value("Last Inspection", "2024 (cycle: annual for firms auditing 100+ issuers)")
    pdf.key_value("Inspection Results", "No Part I.A findings (deficiencies in issuer audits) for 2024")
    pdf.body_text(
        "Meridian & Associates LLP is registered with the Public Company Accounting Oversight Board "
        "and is authorized to perform audits of issuers (publicly traded companies) and broker-dealers "
        "registered with the Securities and Exchange Commission. Meridian currently serves as the "
        "independent auditor for 143 SEC-registered issuers."
    )
    pdf.body_text(
        "The firm has been subject to annual PCAOB inspections since 2004, given the number of issuer "
        "audit clients. Our most recent inspection report (2024) contained no Part I.A findings -- "
        "deficiencies in portions of specific issuer audits -- and no Part II findings -- criticisms "
        "of the firm's quality control system. This represents the sixth consecutive clean inspection."
    )

    pdf.section_heading("2. AICPA Membership and Peer Review")
    pdf.key_value("AICPA Firm Number", "F-8841-2102")
    pdf.key_value("Membership Status", "Active member, Center for Audit Quality (CAQ)")
    pdf.key_value("AICPA Government Audit Quality Center", "Member since 2005")
    pdf.key_value("AICPA Employee Benefit Plan Audit Quality Center", "Member since 2006")
    pdf.key_value("AICPA Private Companies Practice Section", "Member since 2003")
    pdf.ln(2)
    pdf.section_heading("Peer Review Results", level=2)
    pdf.key_value("Most Recent Peer Review", "Year ended June 30, 2025")
    pdf.key_value("Peer Review Rating", "Pass (highest rating)")
    pdf.key_value("Reviewing Firm", "Hartwell & Associates LLP, Philadelphia, PA")
    pdf.key_value("Consecutive Pass Ratings", "14 (since inception of the program)")
    pdf.body_text(
        "Meridian's peer review encompasses the firm's accounting and auditing practice, including "
        "audits performed under GAAS, Government Auditing Standards, PCAOB standards, and ERISA. "
        "The most recent peer review resulted in a 'Pass' rating with no matters for further consideration "
        "and no deficiency findings."
    )

    pdf.add_page()
    pdf.section_heading("3. State CPA Licenses and Registrations")
    pdf.body_text(
        "Meridian & Associates LLP holds active CPA firm licenses in all 50 US states, the District "
        "of Columbia, Puerto Rico, and the US Virgin Islands. The firm maintains a dedicated licensing "
        "compliance team that monitors renewal requirements, CPE obligations, and regulatory changes "
        "across all jurisdictions."
    )
    pdf.section_heading("Key State Registrations", level=2)
    pdf.bold_bullet("New York", "License #LA-129847, renewed annually, current through December 2026")
    pdf.bold_bullet("Illinois", "License #066-024851, renewed triennially, current through September 2027")
    pdf.bold_bullet("California", "License #COR-12984, renewed biennially, current through June 2027")
    pdf.bold_bullet("Texas", "License #F-08742, renewed annually, current through December 2026")
    pdf.bold_bullet("Florida", "License #AD-0042187, renewed biennially, current through December 2027")
    pdf.body_text(
        "A complete listing of all 53 state and territorial CPA firm licenses is available upon request "
        "from the firm's Office of the General Counsel."
    )

    pdf.section_heading("4. International Registrations")
    pdf.body_text(
        "Meridian & Associates LLP operates internationally through its global network and holds "
        "professional registrations in the following jurisdictions:"
    )
    pdf.bold_bullet("United Kingdom", "Registered with the Financial Reporting Council (FRC) as a Recognised Auditor. FRC Registration #RA-1847. Authorised to conduct statutory audits under the Companies Act 2006.")
    pdf.bold_bullet("European Union", "Registered with relevant audit oversight bodies in Germany (APAS), France (H3C), and the Netherlands (AFM) for the conduct of statutory audits.")
    pdf.bold_bullet("Singapore", "Registered with the Accounting and Corporate Regulatory Authority (ACRA) as a public accounting firm. ACRA Registration #PAF-287.")
    pdf.bold_bullet("Australia", "Registered company auditor with the Australian Securities and Investments Commission (ASIC). Registration #AU-41892.")
    pdf.bold_bullet("Japan", "Registered with the Certified Public Accountants and Auditing Oversight Board (CPAAOB). Member of the Japan Institute of CPAs (JICPA).")
    pdf.bold_bullet("Canada", "Licensed by the Chartered Professional Accountants of Ontario, British Columbia, Alberta, and Quebec. Registered with the Canadian Public Accountability Board (CPAB).")

    pdf.add_page()
    pdf.section_heading("5. Information Security and Privacy Certifications")
    pdf.bold_bullet("ISO/IEC 27001:2022", "Certified by BSI Group. Certificate #IS-2025-MER-04821. Valid through September 30, 2028. Scope: all professional services and supporting IT infrastructure.")
    pdf.bold_bullet("SOC 2 Type II", "Examined annually by Whitfield & Crane LLP. Most recent report period: January-December 2025. Trust Service Criteria: Security, Availability, Confidentiality, Processing Integrity. Opinion: Unqualified.")
    pdf.bold_bullet("SOC 1 Type II (SSAE 18)", "Examined annually for the firm's managed services offerings. Most recent report period: January-December 2025. Opinion: Unqualified.")
    pdf.bold_bullet("ISO 22301:2019", "Business Continuity Management System certification by BSI Group. Certificate #BC-2024-MER-01247. Valid through March 2027.")
    pdf.bold_bullet("CSA STAR Level 2", "Cloud Security Alliance STAR attestation for Meridian cloud-hosted platforms. Achieved Level 2 (third-party assessment) in 2024.")
    pdf.bold_bullet("HITRUST CSF", "HITRUST r2 Certified for systems processing protected health information (PHI). Certificate valid through October 2027.")

    pdf.section_heading("6. Industry-Specific Certifications")
    pdf.bold_bullet("PCAOB", "Registered public accounting firm authorized to audit SEC registrants (see Section 1)")
    pdf.bold_bullet("DCAA Approved", "Pre-approved by the Defense Contract Audit Agency for incurred cost audits of government contractors")
    pdf.bold_bullet("FedRAMP Authorized", "Meridian Client Portal and WorkStream platform authorized at FedRAMP Moderate impact level (ATO granted December 2024)")
    pdf.bold_bullet("FINRA Member", "Meridian Capital Advisory LLC (wholly-owned subsidiary) is a registered broker-dealer and FINRA member firm")
    pdf.bold_bullet("AICPA SOC Practice", "All SOC engagement partners and managers hold the AICPA Advanced SOC for Service Organizations Certificate")

    pdf.section_heading("7. Quality Management System")
    pdf.key_value("Standard", "ISQM 1 (International Standard on Quality Management)")
    pdf.key_value("Effective Date", "December 15, 2022")
    pdf.key_value("Status", "Fully implemented with annual evaluation by Chief Quality Officer")
    pdf.body_text(
        "Meridian implemented ISQM 1 ahead of the required effective date and has conducted three "
        "annual evaluations of its system of quality management. The most recent evaluation (2025) "
        "concluded that the system provides reasonable assurance that the objectives of the system "
        "are being achieved, with no significant deficiencies identified."
    )

    pdf.add_page()
    pdf.section_heading("8. Professional Liability Insurance")
    pdf.body_text(
        "Meridian & Associates LLP maintains comprehensive professional liability (errors and omissions) "
        "insurance coverage appropriate for a firm of its size and scope of services."
    )
    pdf.key_value("Primary Carrier", "[Named insurer available under NDA]")
    pdf.key_value("Policy Type", "Claims-made professional liability")
    pdf.key_value("Coverage Limits", "Per-claim and aggregate limits exceed industry benchmarks for Top 20 firms")
    pdf.key_value("Cyber Liability", "Separate cyber liability policy with dedicated coverage for data breaches, ransomware, and regulatory fines")
    pdf.key_value("Fidelity Bond", "Commercial crime / fidelity bond covering employee dishonesty and fraud")
    pdf.body_text(
        "Specific coverage amounts and policy details are available under non-disclosure agreement "
        "as part of the engagement acceptance process."
    )

    pdf.section_heading("9. Diversity and Inclusion Certifications")
    pdf.bullet("National Minority Supplier Development Council (NMSDC) -- Corporate Member since 2012")
    pdf.bullet("Women's Business Enterprise National Council (WBENC) -- Corporate Member since 2014")
    pdf.bullet("Disability:IN -- Best Places to Work for Disability Inclusion, scored 100% (2024, 2025)")
    pdf.bullet("Human Rights Campaign Corporate Equality Index -- Score: 100 (2024, 2025)")
    pdf.bullet("CEO Action for Diversity and Inclusion -- Signatory since 2018")

    pdf.section_heading("10. Contact for Verification")
    pdf.body_text(
        "All certifications and registrations referenced in this document can be independently verified. "
        "For verification requests or to obtain copies of certificates, please contact:"
    )
    pdf.ln(2)
    pdf.body_text(
        "Office of the General Counsel\n"
        "Meridian & Associates LLP\n"
        "120 Meridian Plaza, New York, NY 10004\n"
        "Email: compliance@meridian-llp.com\n"
        "Phone: (212) 555-0100"
    )

    pdf.output(os.path.join(OUTPUT_DIR, "industry_certifications_overview.pdf"))
    print("  Created: industry_certifications_overview.pdf")


if __name__ == "__main__":
    generate_soc2_summary()
    generate_iso27001()
    generate_certifications_overview()
    print("\nAll 3 compliance certification PDFs generated successfully!")
