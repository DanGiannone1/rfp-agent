"""Generate 8 synthetic PDFs for Meridian & Associates LLP."""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Helpers ───────────────────────────────────────────────────────────────

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
            return  # Cover page handled separately
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
        # Top bar
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
        # Title block
        self.set_text_color(0, 51, 102)
        self.set_font("Helvetica", "B", 26)
        self.multi_cell(0, 12, self.doc_title, align="C")
        if self.doc_subtitle:
            self.ln(4)
            self.set_font("Helvetica", "", 14)
            self.set_text_color(80, 80, 80)
            self.multi_cell(0, 8, self.doc_subtitle, align="C")
        self.ln(15)
        # Confidential marking
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
        # Meta
        self.ln(10)
        self.set_text_color(100, 100, 100)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, f"Version {version}  |  Effective Date: {date}", align="C")
        self.ln(6)
        self.cell(0, 6, "Meridian & Associates LLP  |  New York | Chicago | San Francisco | London | Singapore", align="C")
        self.ln(20)
        # Disclaimer
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
        x = self.get_x()
        self.cell(8, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bold_bullet(self, label, text):
        self.set_text_color(40, 40, 40)
        x = self.get_x()
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


# ═══════════════════════════════════════════════════════════════════════════
# 1. EXECUTIVE BIOS
# ═══════════════════════════════════════════════════════════════════════════

def generate_executive_bios():
    pdf = MeridianPDF("Executive Leadership Bios", "Partner & Managing Director Profiles", confidential=True)
    pdf.cover_page(version="3.2", date="January 2026")

    # --- Sarah Chen ---
    pdf.add_page()
    pdf.section_heading("1. Sarah Chen, CPA, CISA")
    pdf.section_heading("Lead Partner, Financial Services Practice", level=2)
    pdf.key_value("Years of Experience", "27 years")
    pdf.key_value("Office", "New York, NY")
    pdf.key_value("Direct Line", "+1 (212) 555-0142")
    pdf.key_value("Email", "s.chen@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Sarah Chen is the Lead Partner for Meridian & Associates' Financial Services Practice, "
        "overseeing a portfolio of engagements spanning commercial banking, capital markets, insurance, "
        "and wealth management. With 27 years of experience advising Fortune 500 financial institutions, "
        "Sarah has led transformative programs totaling over $2.8 billion in aggregate project value. "
        "She is recognized as a leading authority on regulatory compliance, core banking modernization, "
        "and enterprise risk management."
    )
    pdf.body_text(
        "Sarah joined Meridian in 2004 after nine years at a competing Big Four firm, where she served "
        "as a Senior Manager in the banking and capital markets audit practice. Since her promotion to "
        "Partner in 2010, she has grown the Financial Services Practice revenue from $85 million to over "
        "$340 million annually, establishing Meridian as a top-tier advisor to US and European banks."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("MBA, Finance & Strategy, The Wharton School, University of Pennsylvania (2001)")
    pdf.bullet("BS, Accounting, magna cum laude, University of Michigan (1999)")
    pdf.section_heading("Certifications & Memberships", level=3)
    pdf.bullet("Certified Public Accountant (CPA), State of New York")
    pdf.bullet("Certified Information Systems Auditor (CISA)")
    pdf.bullet("Fellow, Institute of Chartered Accountants")
    pdf.bullet("Board Member, Financial Services Roundtable")
    pdf.bullet("Advisory Board, Columbia Business School Center for Financial Innovation")
    pdf.section_heading("Industry Specializations", level=3)
    pdf.bullet("Core banking transformation and cloud migration")
    pdf.bullet("Regulatory compliance (Basel III/IV, Dodd-Frank, SOX 404)")
    pdf.bullet("Enterprise risk management and operational resilience")
    pdf.bullet("Digital payments and open banking architecture")
    pdf.bullet("Post-merger integration for financial institutions")
    pdf.section_heading("Notable Engagements (Blinded)", level=3)
    pdf.bold_bullet("Top-10 US Retail Bank", "Led 18-month core banking modernization program (85-person team). Migrated legacy mainframe to cloud-native architecture, achieving 40% reduction in transaction processing time and $32M annual infrastructure savings.")
    pdf.bold_bullet("Global Investment Bank", "Directed $45M regulatory remediation program across three jurisdictions following consent order. Achieved full regulatory compliance within 14 months, ahead of schedule.")
    pdf.bold_bullet("Major Insurance Carrier", "Oversaw enterprise data governance initiative covering 2.3 petabytes of customer data across 14 legacy platforms. Resulted in 60% improvement in data quality scores.")
    pdf.section_heading("Publications & Thought Leadership", level=3)
    pdf.bullet('"The Future of Core Banking: Cloud-Native Architectures for the Next Decade" - Harvard Business Review (2025)')
    pdf.bullet('"Navigating Regulatory Change in a Post-Basel IV World" - Journal of Financial Regulation (2024)')
    pdf.bullet("Keynote Speaker, Sibos Annual Conference (2024, 2025)")
    pdf.bullet("Panelist, World Economic Forum, Davos - Financial Services Track (2025)")

    # --- Michael Torres ---
    pdf.add_page()
    pdf.section_heading("2. Michael Torres, CPA, PMP")
    pdf.section_heading("Lead Partner, Healthcare & Life Sciences Practice", level=2)
    pdf.key_value("Years of Experience", "24 years")
    pdf.key_value("Office", "Chicago, IL")
    pdf.key_value("Direct Line", "+1 (312) 555-0287")
    pdf.key_value("Email", "m.torres@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Michael Torres leads Meridian's Healthcare & Life Sciences Practice, serving health systems, "
        "pharmaceutical companies, medical device manufacturers, and health insurance plans. Over his "
        "24-year career, Michael has managed more than 60 large-scale engagements in the healthcare sector, "
        "including post-merger integrations, EHR implementations, revenue cycle transformations, and "
        "value-based care program designs. He brings a rare combination of deep clinical operations "
        "understanding and financial acumen that enables him to bridge the gap between C-suite strategy "
        "and frontline clinical delivery."
    )
    pdf.body_text(
        "Before joining Meridian in 2008, Michael spent six years at a global management consulting firm "
        "and five years in hospital administration at a major academic medical center. His operational "
        "background gives him a practitioner's perspective that clients consistently cite as a differentiator. "
        "Under his leadership, the Healthcare Practice has achieved a 94% client retention rate and has been "
        "named a top-tier healthcare advisory practice by Modern Healthcare for four consecutive years."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("MBA, Healthcare Management, Kellogg School of Management, Northwestern University (2006)")
    pdf.bullet("MHA, Master of Health Administration, University of North Carolina at Chapel Hill (2002)")
    pdf.bullet("BS, Biology, Georgetown University (2000)")
    pdf.section_heading("Certifications & Memberships", level=3)
    pdf.bullet("Certified Public Accountant (CPA), State of Illinois")
    pdf.bullet("Project Management Professional (PMP)")
    pdf.bullet("Fellow, American College of Healthcare Executives (FACHE)")
    pdf.bullet("Board of Directors, American Hospital Association - Council on Finance")
    pdf.bullet("Advisory Council Member, HIMSS (Healthcare Information and Management Systems Society)")
    pdf.section_heading("Industry Specializations", level=3)
    pdf.bullet("Post-merger integration for health systems")
    pdf.bullet("Electronic Health Record (EHR) implementation and optimization (Epic, Cerner, MEDITECH)")
    pdf.bullet("Revenue cycle management and claims denial reduction")
    pdf.bullet("Value-based care program design and population health analytics")
    pdf.bullet("Healthcare regulatory compliance (HIPAA, Stark Law, Anti-Kickback)")
    pdf.section_heading("Notable Engagements (Blinded)", level=3)
    pdf.bold_bullet("12-Hospital Regional System", "Led 24-month post-merger integration program (120+ person team). Unified Epic EHR, harmonized clinical workflows, and established shared services center. Realized $52M in synergies, exceeding $45M target.")
    pdf.bold_bullet("Top-5 Health Insurance Plan", "Directed claims processing transformation reducing average adjudication time from 14 days to 3.2 days. Improved clean claims rate from 76% to 94%, generating $28M in annual savings.")
    pdf.bold_bullet("Academic Medical Center", "Oversaw Epic Beaker and Radiant implementation across 3 hospitals and 120 ambulatory sites. Completed on-time and 8% under budget.")
    pdf.section_heading("Publications & Thought Leadership", level=3)
    pdf.bullet('"Realizing Synergies in Health System Mergers: A Framework for Clinical Integration" - New England Journal of Medicine Catalyst (2025)')
    pdf.bullet('"The Revenue Cycle of the Future: AI-Enabled Claims Management" - Healthcare Financial Management Association (2024)')
    pdf.bullet("Keynote Speaker, HIMSS Global Health Conference (2024, 2025)")

    # --- Dr. Priya Ramanathan ---
    pdf.add_page()
    pdf.section_heading("3. Dr. Priya Ramanathan, CISSP, TOGAF")
    pdf.section_heading("Lead Partner, Technology & Digital Advisory Practice", level=2)
    pdf.key_value("Years of Experience", "22 years")
    pdf.key_value("Office", "San Francisco, CA")
    pdf.key_value("Direct Line", "+1 (415) 555-0193")
    pdf.key_value("Email", "p.ramanathan@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Dr. Priya Ramanathan leads Meridian's Technology & Digital Advisory Practice, one of the firm's "
        "fastest-growing service lines with $280 million in annual revenue and a compound annual growth "
        "rate of 22% over the past four years. Priya specializes in enterprise architecture, cloud "
        "transformation, cybersecurity strategy, and AI/ML implementation at scale. Her technical depth, "
        "combined with her ability to translate complex technology concepts into board-level strategic "
        "narratives, has made her a trusted advisor to CTOs and CIOs across the Fortune 500."
    )
    pdf.body_text(
        "Priya holds a Ph.D. in Computer Science from Stanford University with a focus on distributed "
        "systems and machine learning. Prior to joining Meridian in 2011, she spent eight years at a "
        "leading technology consulting firm and two years as VP of Engineering at a Series C fintech "
        "startup. She holds over a dozen patents in distributed computing and has published extensively "
        "in peer-reviewed journals on topics ranging from zero-trust architecture to responsible AI governance."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("Ph.D., Computer Science (Distributed Systems & Machine Learning), Stanford University (2006)")
    pdf.bullet("MS, Computer Science, Stanford University (2003)")
    pdf.bullet("BTech, Computer Science & Engineering, Indian Institute of Technology Bombay (2001)")
    pdf.section_heading("Certifications & Memberships", level=3)
    pdf.bullet("Certified Information Systems Security Professional (CISSP)")
    pdf.bullet("TOGAF 9 Certified Enterprise Architect")
    pdf.bullet("AWS Solutions Architect - Professional")
    pdf.bullet("Google Cloud Professional Cloud Architect")
    pdf.bullet("Board of Advisors, MIT Sloan Center for Information Systems Research (CISR)")
    pdf.bullet("Member, National Academy of Engineering (elected 2024)")
    pdf.section_heading("Industry Specializations", level=3)
    pdf.bullet("Enterprise cloud transformation and multi-cloud architecture")
    pdf.bullet("Cybersecurity strategy, zero-trust architecture, and incident response")
    pdf.bullet("Artificial intelligence and machine learning at enterprise scale")
    pdf.bullet("Digital product development and platform engineering")
    pdf.bullet("Technology due diligence for M&A transactions")
    pdf.section_heading("Notable Engagements (Blinded)", level=3)
    pdf.bold_bullet("Large US State Government Agency", "Led 30-month enterprise cloud migration program (90-person team). Migrated 1,800 applications to Azure Government, achieving FedRAMP High authorization and 35% reduction in IT operating costs.")
    pdf.bold_bullet("Global Retail Conglomerate", "Directed AI/ML center of excellence buildout, deploying 23 production ML models across demand forecasting, pricing optimization, and customer segmentation. Generated $140M in incremental revenue within 18 months.")
    pdf.bold_bullet("Fortune 100 Technology Company", "Oversaw zero-trust security architecture implementation across 180,000 endpoints in 42 countries. Reduced mean time to detect (MTTD) from 72 hours to 4 hours.")
    pdf.section_heading("Publications & Thought Leadership", level=3)
    pdf.bullet('"Zero Trust at Scale: Lessons from 50 Enterprise Implementations" - IEEE Security & Privacy (2025)')
    pdf.bullet('"Responsible AI Governance: A Framework for the Enterprise" - MIT Sloan Management Review (2024)')
    pdf.bullet("12 patents in distributed computing and machine learning systems")
    pdf.bullet("Keynote Speaker, AWS re:Invent (2024), RSA Conference (2025)")

    # --- James O'Sullivan ---
    pdf.add_page()
    pdf.section_heading("4. James O'Sullivan, CPA, Six Sigma Black Belt")
    pdf.section_heading("Lead Partner, Manufacturing & Industrial Practice", level=2)
    pdf.key_value("Years of Experience", "26 years")
    pdf.key_value("Office", "Chicago, IL")
    pdf.key_value("Direct Line", "+1 (312) 555-0356")
    pdf.key_value("Email", "j.osullivan@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "James O'Sullivan leads Meridian's Manufacturing & Industrial Practice, serving clients across "
        "discrete manufacturing, process industries, aerospace & defense, and industrial distribution. "
        "With 26 years of experience, James has guided over 40 major engagements focused on supply chain "
        "transformation, operational excellence, ERP modernization, and sustainability strategy. His "
        "deep understanding of manufacturing operations, combined with his background in financial "
        "advisory, enables him to deliver programs that generate measurable financial returns while "
        "building long-term operational resilience."
    )
    pdf.body_text(
        "Prior to his 18-year tenure at Meridian, James spent eight years at a leading industrial "
        "consulting firm and began his career as a cost accountant at a Fortune 100 automotive manufacturer. "
        "He is widely recognized in the industry for his work on digital supply chain enablement and "
        "has been named one of Supply Chain Management Review's 'Pros to Know' for three consecutive years. "
        "Under his leadership, the Manufacturing Practice has grown to $195 million in annual revenue "
        "with a team of 420 professionals globally."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("MBA, Operations & Supply Chain Management, University of Chicago Booth School of Business (2004)")
    pdf.bullet("BS, Accounting, University of Notre Dame (1998)")
    pdf.section_heading("Certifications & Memberships", level=3)
    pdf.bullet("Certified Public Accountant (CPA), State of Illinois")
    pdf.bullet("Six Sigma Black Belt (ASQ Certified)")
    pdf.bullet("APICS Certified Supply Chain Professional (CSCP)")
    pdf.bullet("Board Member, National Association of Manufacturers - Digital Transformation Council")
    pdf.bullet("Advisory Board, Georgia Tech Supply Chain & Logistics Institute")
    pdf.section_heading("Industry Specializations", level=3)
    pdf.bullet("Supply chain transformation, demand planning, and inventory optimization")
    pdf.bullet("SAP S/4HANA and ERP modernization for manufacturing")
    pdf.bullet("Operational excellence and lean manufacturing (Six Sigma, TPS)")
    pdf.bullet("Sustainability and ESG strategy for industrial companies (Scope 1-3 emissions)")
    pdf.bullet("Industry 4.0, IoT, and smart factory implementation")
    pdf.section_heading("Notable Engagements (Blinded)", level=3)
    pdf.bold_bullet("Fortune 200 Diversified Manufacturer", "Led 16-month supply chain transformation program (65-person team). Implemented SAP IBP, deployed control tower, and launched AI-driven demand sensing. Achieved 28% inventory reduction ($106M freed working capital) and 95% OTIF delivery.")
    pdf.bold_bullet("Global Aerospace OEM", "Directed SAP S/4HANA implementation across 22 manufacturing plants in 8 countries. Consolidated 6 legacy ERP instances into single global template. Delivered $38M in annual process efficiency gains.")
    pdf.bold_bullet("Mid-Market Industrial Distributor", "Oversaw operational turnaround engagement during Chapter 11 restructuring. Reduced operating costs by 24%, renegotiated $120M in supplier contracts, and enabled successful emergence from bankruptcy within 9 months.")
    pdf.section_heading("Publications & Thought Leadership", level=3)
    pdf.bullet('"The Digital Supply Chain: From Visibility to Autonomous Decision-Making" - Harvard Business Review (2025)')
    pdf.bullet('"Scope 3 Emissions in Manufacturing: Measurement, Reduction, and Reporting" - MIT Sloan Management Review (2024)')
    pdf.bullet("Keynote Speaker, Gartner Supply Chain Symposium (2024, 2025)")

    pdf.output(os.path.join(OUTPUT_DIR, "executive_bios.pdf"))
    print("Generated executive_bios.pdf")


# ═══════════════════════════════════════════════════════════════════════════
# 2. MANAGEMENT BIOS
# ═══════════════════════════════════════════════════════════════════════════

def generate_management_bios():
    pdf = MeridianPDF("Management Team Bios", "Senior Manager & Manager Profiles", confidential=True)
    pdf.cover_page(version="2.1", date="February 2026")

    # --- David Kim ---
    pdf.add_page()
    pdf.section_heading("1. David Kim, PMP, SAP Certified")
    pdf.section_heading("Senior Manager, ERP Implementation", level=2)
    pdf.key_value("Years of Experience", "14 years")
    pdf.key_value("Office", "Chicago, IL")
    pdf.key_value("Email", "d.kim@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "David Kim is a Senior Manager in Meridian's Technology Consulting practice, specializing in "
        "large-scale ERP implementations with a focus on SAP S/4HANA. Over his 14-year career, David "
        "has delivered 11 full-lifecycle ERP implementations across manufacturing, retail, and financial "
        "services industries. He is recognized for his expertise in managing complex, multi-workstream "
        "programs involving cross-functional teams of 40-80 consultants and navigating the organizational "
        "change management challenges that frequently derail ERP projects."
    )
    pdf.body_text(
        "David leads a team of 28 consultants and is responsible for $12 million in annual engagement "
        "revenue. His project delivery track record includes a 100% go-live success rate and an average "
        "budget variance of less than 5%. He is a certified SAP S/4HANA Solution Architect and has "
        "completed advanced training in SAP Activate methodology, Agile at Scale (SAFe), and "
        "organizational change management."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Information Systems, Carnegie Mellon University (2014)")
    pdf.bullet("BS, Industrial Engineering, Purdue University (2012)")
    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Project Management Professional (PMP)")
    pdf.bullet("SAP Certified Application Associate - SAP S/4HANA (multiple modules)")
    pdf.bullet("SAFe 5 Agilist (SA)")
    pdf.bullet("ITIL v4 Foundation")
    pdf.bullet("Prosci Certified Change Practitioner")
    pdf.section_heading("Technical Specializations", level=3)
    pdf.bullet("SAP S/4HANA implementation (Finance, MM, PP, SD, WM modules)")
    pdf.bullet("Data migration strategy and execution (SAP LSMW, BODS, Syniti)")
    pdf.bullet("Integration architecture (SAP CPI, MuleSoft, Dell Boomi)")
    pdf.bullet("Cutover planning and hypercare management")
    pdf.bullet("SAP BTP (Business Technology Platform) and Fiori UX design")
    pdf.section_heading("Project Highlights", level=3)
    pdf.bold_bullet("Fortune 200 Manufacturer", "Program Manager for 16-month SAP S/4HANA greenfield implementation across 8 distribution centers. Managed 65-person cross-functional team. Delivered on-time, 3% under budget.")
    pdf.bold_bullet("National Retail Chain", "Led SAP S/4HANA conversion from ECC 6.0 for 340-store retailer. Coordinated data migration of 12M+ material master records and 8 years of transactional history. Zero critical defects at go-live.")
    pdf.bold_bullet("Mid-Market Pharmaceutical Company", "Directed end-to-end SAP implementation covering Finance, Quality Management, and Batch Management. Achieved FDA 21 CFR Part 11 compliance validation on first attempt.")
    pdf.section_heading("Team Leadership", level=3)
    pdf.body_text(
        "David directly manages a team of 28 consultants ranging from Analyst to Manager level. He serves "
        "as the practice's recruiting lead for campus hires from target universities and has designed "
        "the SAP Academy internal training curriculum, which has upskilled over 60 consultants since its "
        "launch in 2022. David also mentors four junior managers in the firm's formal mentorship program."
    )

    # --- Rachel Okonkwo ---
    pdf.add_page()
    pdf.section_heading("2. Rachel Okonkwo, CPA, MST")
    pdf.section_heading("Manager, Tax Provision", level=2)
    pdf.key_value("Years of Experience", "9 years")
    pdf.key_value("Office", "New York, NY")
    pdf.key_value("Email", "r.okonkwo@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Rachel Okonkwo is a Manager in Meridian's Tax Practice, focusing on ASC 740 income tax "
        "provision and compliance for multinational corporations. Over her 9-year career, Rachel has "
        "served clients across technology, financial services, and consumer products industries, "
        "managing tax provision engagements for companies with revenues ranging from $500 million to "
        "$45 billion. She is known for her technical depth in complex areas including uncertain tax "
        "positions (FIN 48), transfer pricing implications for provision, and tax reform impact analysis."
    )
    pdf.body_text(
        "Rachel manages a team of 12 tax professionals and is responsible for the timely delivery of "
        "quarterly and annual tax provisions for 8 key client relationships. She has been instrumental "
        "in the firm's adoption of tax technology tools, leading the implementation of Thomson Reuters "
        "ONESOURCE Tax Provision for three major clients and developing automated workpapers that have "
        "reduced provision cycle time by 35% on average."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Taxation (MST), New York University School of Law (2019)")
    pdf.bullet("BS, Accounting, summa cum laude, Howard University (2017)")
    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Certified Public Accountant (CPA), State of New York")
    pdf.bullet("Certified Tax Technologist (CTT), Thomson Reuters")
    pdf.bullet("Member, American Institute of CPAs (AICPA) - Tax Section")
    pdf.bullet("Member, Tax Executives Institute (TEI)")
    pdf.section_heading("Technical Specializations", level=3)
    pdf.bullet("ASC 740 income tax provision (quarterly and annual)")
    pdf.bullet("Uncertain tax positions (FIN 48/ASC 740-10)")
    pdf.bullet("International tax provision (GILTI, BEAT, FDII, Pillar Two)")
    pdf.bullet("Tax technology implementation (ONESOURCE, Corptax, Longview)")
    pdf.bullet("Tax accounting methods and R&D credit documentation")
    pdf.section_heading("Project Highlights", level=3)
    pdf.bold_bullet("Global Technology Company", "Led ASC 740 provision for $28B revenue multinational with operations in 40+ jurisdictions. Managed complex Pillar Two impact analysis and implemented ONESOURCE Tax Provision, reducing quarterly close cycle from 18 days to 11 days.")
    pdf.bold_bullet("Fortune 500 Financial Services Firm", "Directed tax reform impact analysis (TCJA and subsequent guidance) covering $3.2B in deferred tax assets. Presented findings to Audit Committee and external auditors.")
    pdf.bold_bullet("Consumer Products Conglomerate", "Managed annual and quarterly provisions across 6 domestic and 22 international entities. Identified $14M in previously unrecognized tax benefits through comprehensive FIN 48 review.")
    pdf.section_heading("Team Leadership", level=3)
    pdf.body_text(
        "Rachel leads a team of 12 tax professionals including 3 seniors and 9 staff/associates. She "
        "has been recognized as a top mentor in the firm's New Professional Development program for two "
        "consecutive years and serves on the Tax Practice's Diversity, Equity & Inclusion steering committee. "
        "Rachel is also the lead instructor for the firm's internal ASC 740 training curriculum."
    )

    # --- Alex Petrov ---
    pdf.add_page()
    pdf.section_heading("3. Alex Petrov, CISSP, CISM, CEH")
    pdf.section_heading("Senior Manager, Cybersecurity", level=2)
    pdf.key_value("Years of Experience", "13 years")
    pdf.key_value("Office", "Washington, D.C.")
    pdf.key_value("Email", "a.petrov@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Alex Petrov is a Senior Manager in Meridian's Cybersecurity & Privacy Practice, leading the "
        "firm's offensive security, incident response, and security architecture service lines. With 13 "
        "years of experience spanning the US intelligence community, a leading cybersecurity firm, and "
        "professional services, Alex brings a rare combination of adversarial mindset and enterprise "
        "governance expertise. He has led over 200 penetration testing engagements, managed incident "
        "response for 15 major breaches, and designed security architectures for organizations protecting "
        "critical infrastructure across government and private sectors."
    )
    pdf.body_text(
        "Alex manages a team of 22 cybersecurity professionals and oversees $9.5 million in annual "
        "engagement revenue. His team maintains a 98% client satisfaction rating and has been instrumental "
        "in building Meridian's reputation as a top-tier cybersecurity advisory practice. Alex holds "
        "an active TS/SCI security clearance and regularly advises clients in the defense industrial "
        "base and federal government sectors."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Cybersecurity, Georgia Institute of Technology (2016)")
    pdf.bullet("BS, Computer Science, Virginia Tech (2013)")
    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Certified Information Systems Security Professional (CISSP)")
    pdf.bullet("Certified Information Security Manager (CISM)")
    pdf.bullet("Certified Ethical Hacker (CEH)")
    pdf.bullet("GIAC Certified Incident Handler (GCIH)")
    pdf.bullet("AWS Security Specialty Certification")
    pdf.bullet("Active TS/SCI Security Clearance")
    pdf.section_heading("Technical Specializations", level=3)
    pdf.bullet("Offensive security and penetration testing (network, application, cloud)")
    pdf.bullet("Incident response and digital forensics")
    pdf.bullet("Zero-trust architecture design and implementation")
    pdf.bullet("Cloud security posture management (AWS, Azure, GCP)")
    pdf.bullet("CMMC/NIST SP 800-171 compliance for defense industrial base")
    pdf.bullet("Security operations center (SOC) design and optimization")
    pdf.section_heading("Project Highlights", level=3)
    pdf.bold_bullet("Federal Civilian Agency", "Led FedRAMP High authorization assessment for agency's enterprise cloud migration (1,800 applications on Azure Government). Zero findings on initial assessment. Developed continuous monitoring program.")
    pdf.bold_bullet("Global Financial Institution", "Directed incident response for sophisticated nation-state attack affecting 2.3M customer records. Contained breach within 48 hours, led forensic investigation, and managed regulatory disclosure across 6 jurisdictions.")
    pdf.bold_bullet("Defense Contractor", "Designed and implemented zero-trust architecture across 45,000 endpoints, achieving CMMC Level 3 certification. Reduced attack surface by 72% and MTTD from 96 hours to 6 hours.")
    pdf.section_heading("Team Leadership", level=3)
    pdf.body_text(
        "Alex leads a diverse team of 22 cybersecurity professionals including red team operators, "
        "incident responders, security architects, and GRC analysts. He has established the firm's "
        "Cybersecurity Analyst Development Program (CADP), a 12-month rotational program that has trained "
        "35 entry-level analysts since its inception in 2021. Alex also serves as the firm's internal "
        "CISO advisor, providing guidance on Meridian's own security posture."
    )

    # --- Maria Santos ---
    pdf.add_page()
    pdf.section_heading("4. Maria Santos, CPA, CIA")
    pdf.section_heading("Manager, Audit & Assurance", level=2)
    pdf.key_value("Years of Experience", "8 years")
    pdf.key_value("Office", "San Francisco, CA")
    pdf.key_value("Email", "m.santos@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Maria Santos is a Manager in Meridian's Audit & Assurance Practice, specializing in technology "
        "and life sciences company audits. Over her 8-year career, Maria has served as engagement manager "
        "for audits of public and private companies ranging from pre-IPO startups to $15 billion revenue "
        "technology firms. She has particular expertise in revenue recognition (ASC 606), stock-based "
        "compensation accounting (ASC 718), and business combinations (ASC 805), making her a valuable "
        "resource for high-growth technology companies navigating complex accounting issues."
    )
    pdf.body_text(
        "Maria manages a team of 15 audit professionals and oversees 6 key audit engagements annually. "
        "She has been recognized with Meridian's 'Rising Leader' award in 2024 for her contributions "
        "to practice development, including the design of the firm's technology industry audit methodology "
        "and her leadership of the audit analytics initiative, which integrates data analytics and "
        "continuous auditing techniques into standard audit procedures."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Accountancy, University of Southern California (2018)")
    pdf.bullet("BA, Economics, University of California, Berkeley (2016)")
    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Certified Public Accountant (CPA), State of California")
    pdf.bullet("Certified Internal Auditor (CIA)")
    pdf.bullet("Certified in Risk Management Assurance (CRMA)")
    pdf.bullet("Member, AICPA - Auditing Standards Board Observer Program")
    pdf.section_heading("Technical Specializations", level=3)
    pdf.bullet("Technology and SaaS company audits (public and private)")
    pdf.bullet("Revenue recognition (ASC 606) for complex arrangements")
    pdf.bullet("Stock-based compensation (ASC 718) and equity accounting")
    pdf.bullet("Business combinations and purchase price allocation (ASC 805)")
    pdf.bullet("SOC 1/SOC 2 examination and IT general controls testing")
    pdf.bullet("Audit data analytics and continuous auditing methodologies")
    pdf.section_heading("Project Highlights", level=3)
    pdf.bold_bullet("Pre-IPO SaaS Company", "Managed first-year audit for $2.1B revenue SaaS company preparing for IPO. Navigated complex ASC 606 implementation for multi-element arrangements and stock-based compensation restatement. Achieved clean opinion with no material adjustments.")
    pdf.bold_bullet("Fortune 500 Technology Company", "Led integrated audit (financial statements and ICFR) for $15B revenue technology firm. Managed team of 35 auditors across 4 locations. Identified and resolved 3 significant deficiencies before year-end.")
    pdf.bold_bullet("Biotech Startup Portfolio", "Managed audits for 4 pre-revenue biotechnology companies, addressing complex R&D cost capitalization, in-process R&D valuation, and going concern assessments. All opinions issued within 60 days of year-end.")
    pdf.section_heading("Team Leadership", level=3)
    pdf.body_text(
        "Maria directly supervises a team of 15 audit professionals and serves as counselor to 8 staff "
        "in the firm's performance management system. She is the San Francisco office's campus recruiting "
        "lead for UC Berkeley and Stanford, and she co-chairs the firm's Women in Leadership employee "
        "resource group. Maria has also developed and delivered the firm's internal training module on "
        "ASC 606 revenue recognition, which has been completed by over 200 audit professionals firm-wide."
    )

    pdf.output(os.path.join(OUTPUT_DIR, "management_bios.pdf"))
    print("Generated management_bios.pdf")


# ═══════════════════════════════════════════════════════════════════════════
# 3. EXECUTION BIOS
# ═══════════════════════════════════════════════════════════════════════════

def generate_execution_bios():
    pdf = MeridianPDF("Execution Team Bios", "Senior Consultant & Staff Profiles", confidential=True)
    pdf.cover_page(version="1.4", date="February 2026")

    # --- Jordan Lee ---
    pdf.add_page()
    pdf.section_heading("1. Jordan Lee")
    pdf.section_heading("Senior Consultant, Cloud Engineering", level=2)
    pdf.key_value("Years of Experience", "5 years")
    pdf.key_value("Office", "San Francisco, CA")
    pdf.key_value("Email", "j.lee@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Jordan Lee is a Senior Consultant in Meridian's Cloud Engineering practice, specializing in "
        "designing and implementing enterprise cloud infrastructure on AWS and Azure. Over five years, "
        "Jordan has contributed to 9 cloud migration and modernization engagements, serving clients "
        "in government, financial services, and technology sectors. Jordan is known for deep expertise "
        "in Infrastructure as Code (IaC), containerization, and CI/CD pipeline design, consistently "
        "delivering infrastructure that meets stringent security and compliance requirements including "
        "FedRAMP, SOC 2, and PCI-DSS."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("BS, Computer Science, University of Washington (2021)")
    pdf.bullet("Minor in Mathematics")
    pdf.section_heading("Certifications", level=3)
    pdf.bullet("AWS Solutions Architect - Professional")
    pdf.bullet("AWS DevOps Engineer - Professional")
    pdf.bullet("Microsoft Azure Administrator Associate (AZ-104)")
    pdf.bullet("HashiCorp Certified: Terraform Associate")
    pdf.bullet("Certified Kubernetes Administrator (CKA)")
    pdf.section_heading("Technical Skills", level=3)
    pdf.bold_bullet("Cloud Platforms", "AWS (VPC, ECS, EKS, Lambda, S3, RDS, CloudFront), Azure (AKS, App Service, Functions, ADLS Gen2)")
    pdf.bold_bullet("Infrastructure as Code", "Terraform, AWS CloudFormation, Pulumi, Ansible")
    pdf.bold_bullet("Containers & Orchestration", "Docker, Kubernetes, Helm, ArgoCD, Istio")
    pdf.bold_bullet("CI/CD", "GitHub Actions, Azure DevOps Pipelines, Jenkins, GitLab CI")
    pdf.bold_bullet("Programming", "Python, Go, Bash, TypeScript")
    pdf.bold_bullet("Monitoring & Observability", "Datadog, Prometheus, Grafana, ELK Stack, AWS CloudWatch")
    pdf.section_heading("Project Contributions", level=3)
    pdf.bold_bullet("State Government Cloud Migration", "Designed and implemented landing zone architecture on Azure Government for 1,800-application migration. Built Terraform modules for standardized resource deployment, reducing provisioning time from 3 weeks to 2 hours. Developed automated compliance scanning pipeline achieving FedRAMP High controls coverage.")
    pdf.bold_bullet("Global Bank API Platform", "Architected EKS-based microservices platform supporting 450 API endpoints. Implemented service mesh (Istio) for traffic management and mTLS. Achieved 99.99% platform availability over 12-month measurement period.")
    pdf.bold_bullet("SaaS Startup Infrastructure Buildout", "Built entire cloud infrastructure from scratch for Series B fintech startup on AWS. Designed multi-region active-active architecture supporting 50,000 transactions per second with sub-100ms latency.")
    pdf.section_heading("Training Completed", level=3)
    pdf.bullet("Meridian Cloud Architecture Academy (2023)")
    pdf.bullet("AWS Advanced Networking Specialty - In Progress")
    pdf.bullet("Meridian Leadership Essentials Program (2024)")

    # --- Aisha Patel ---
    pdf.add_page()
    pdf.section_heading("2. Aisha Patel")
    pdf.section_heading("Staff, Data Analytics", level=2)
    pdf.key_value("Years of Experience", "2 years")
    pdf.key_value("Office", "New York, NY")
    pdf.key_value("Email", "a.patel@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Aisha Patel is a Staff member in Meridian's Data Analytics practice, contributing to business "
        "intelligence, data visualization, and advanced analytics engagements. Despite being early in her "
        "career, Aisha has already made significant contributions to 5 client engagements, demonstrating "
        "exceptional proficiency in SQL, Python, and Tableau. She has been recognized for her ability to "
        "translate complex analytical outputs into clear, actionable insights for business stakeholders, "
        "and she received the 'New Professional of the Year' award for the New York office in 2025."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Business Analytics, Columbia University (2024)")
    pdf.bullet("BS, Statistics, University of Michigan (2022)")
    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Tableau Desktop Certified Professional")
    pdf.bullet("Google Professional Data Engineer")
    pdf.bullet("Microsoft Certified: Power BI Data Analyst Associate")
    pdf.bullet("DataCamp Professional Data Scientist Certification")
    pdf.section_heading("Technical Skills", level=3)
    pdf.bold_bullet("Data Analysis", "Python (pandas, NumPy, scikit-learn), R, SQL (T-SQL, PL/SQL, BigQuery)")
    pdf.bold_bullet("Visualization", "Tableau, Power BI, Matplotlib, Plotly, Looker")
    pdf.bold_bullet("Data Engineering", "dbt, Apache Spark, Airflow, Snowflake, Databricks")
    pdf.bold_bullet("Machine Learning", "Regression, classification, clustering, NLP (spaCy, Hugging Face)")
    pdf.bold_bullet("Cloud", "GCP BigQuery, AWS Redshift, Azure Synapse Analytics")
    pdf.section_heading("Project Contributions", level=3)
    pdf.bold_bullet("Healthcare Claims Analytics", "Built predictive model for claims denial risk scoring using XGBoost, achieving 89% accuracy. Model identified $4.2M in at-risk claims per quarter, enabling proactive intervention by revenue cycle team.")
    pdf.bold_bullet("Retail Customer Segmentation", "Developed customer segmentation framework using k-means clustering on 12M+ customer records. Created interactive Tableau dashboard enabling marketing team to design targeted campaigns, contributing to 15% improvement in campaign conversion rates.")
    pdf.bold_bullet("Financial Services Regulatory Reporting", "Automated CCAR stress testing data pipeline using Python and Airflow, reducing manual data preparation from 120 person-hours to 8 person-hours per reporting cycle.")
    pdf.section_heading("Training Completed", level=3)
    pdf.bullet("Meridian Data Analytics Foundations Program (2024)")
    pdf.bullet("Advanced Machine Learning with Python - Internal Course (2025)")
    pdf.bullet("Meridian Professional Communications Workshop (2024)")
    pdf.bullet("Snowflake SnowPro Core Certification - In Progress")

    # --- Marcus Wright ---
    pdf.add_page()
    pdf.section_heading("3. Marcus Wright, SAP Certified")
    pdf.section_heading("Senior Consultant, SAP Functional", level=2)
    pdf.key_value("Years of Experience", "6 years")
    pdf.key_value("Office", "Chicago, IL")
    pdf.key_value("Email", "m.wright@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Marcus Wright is a Senior Consultant specializing in SAP functional configuration and business "
        "process design. With 6 years of experience, Marcus has contributed to 7 SAP implementation and "
        "migration projects across manufacturing, distribution, and consumer products industries. He is "
        "recognized for his deep expertise in SAP Materials Management (MM) and Production Planning (PP) "
        "modules, and his ability to bridge the gap between technical SAP configuration and business "
        "process requirements. Marcus consistently receives outstanding client feedback for his communication "
        "skills, responsiveness, and attention to detail."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("BS, Supply Chain Management, Michigan State University (2020)")
    pdf.bullet("Minor in Information Technology")
    pdf.section_heading("Certifications", level=3)
    pdf.bullet("SAP Certified Application Associate - SAP S/4HANA Sourcing and Procurement")
    pdf.bullet("SAP Certified Application Associate - SAP S/4HANA Manufacturing")
    pdf.bullet("APICS Certified in Production and Inventory Management (CPIM)")
    pdf.bullet("SAFe 5 Practitioner")
    pdf.section_heading("Technical Skills", level=3)
    pdf.bold_bullet("SAP Modules", "MM, PP, PP-PI, WM/EWM, QM, PM (configuration and support)")
    pdf.bold_bullet("SAP Tools", "SAP Activate, LSMW, BODS, Fiori app configuration, BRF+")
    pdf.bold_bullet("Integration", "SAP CPI, IDocs, BAPIs, EDI (850/855/856/810)")
    pdf.bold_bullet("Reporting", "SAP Analytics Cloud, BW/4HANA, CDS Views, Embedded Analytics")
    pdf.bold_bullet("Process Design", "BPMN, Signavio, SAP Solution Manager")
    pdf.section_heading("Project Contributions", level=3)
    pdf.bold_bullet("Fortune 200 Manufacturer", "Led MM and PP functional configuration for SAP S/4HANA greenfield implementation. Designed procurement and production planning processes for 8 distribution centers. Managed 380 functional specifications and coordinated UAT with 120 business users.")
    pdf.bold_bullet("Consumer Products Company", "Configured SAP EWM (Extended Warehouse Management) for 3 distribution centers, enabling real-time inventory visibility and wave-based picking. Reduced warehouse processing time by 22%.")
    pdf.bold_bullet("Chemical Manufacturer", "Designed and configured PP-PI (Process Industry) solution for batch manufacturing. Implemented quality management integration enabling real-time COA (Certificate of Analysis) generation, reducing QA release cycle from 48 hours to 4 hours.")
    pdf.section_heading("Training Completed", level=3)
    pdf.bullet("SAP S/4HANA Manufacturing Deep Dive (SAP Official, 2024)")
    pdf.bullet("Meridian Consulting Excellence Program (2023)")
    pdf.bullet("Advanced Business Process Modeling - Internal Course (2024)")
    pdf.bullet("Meridian Leadership Essentials Program (2025)")

    # --- Emily Nakamura ---
    pdf.add_page()
    pdf.section_heading("4. Emily Nakamura")
    pdf.section_heading("Staff, Risk Advisory", level=2)
    pdf.key_value("Years of Experience", "3 years")
    pdf.key_value("Office", "New York, NY")
    pdf.key_value("Email", "e.nakamura@meridian-llp.com")
    pdf.ln(2)
    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Emily Nakamura is a Staff member in Meridian's Risk Advisory practice, supporting internal audit, "
        "SOX compliance, and enterprise risk management engagements. In her 3 years at the firm, Emily "
        "has contributed to 8 client engagements across financial services, technology, and healthcare "
        "sectors. She is particularly skilled at IT general controls (ITGC) testing, SOX 404 walkthroughs "
        "and testing, and risk assessment documentation. Emily has been recognized for her thoroughness, "
        "strong analytical skills, and ability to work effectively with client personnel at all levels."
    )
    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Accounting (Assurance & Advisory concentration), Boston University (2023)")
    pdf.bullet("BA, Economics, Wellesley College (2021)")
    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Certified Internal Auditor (CIA) - Parts I and II passed, Part III in progress")
    pdf.bullet("Certified Information Systems Auditor (CISA) - Expected Q2 2026")
    pdf.bullet("CompTIA Security+ Certified")
    pdf.bullet("Member, Institute of Internal Auditors (IIA)")
    pdf.section_heading("Technical Skills", level=3)
    pdf.bold_bullet("Audit & Risk", "SOX 404 testing, ITGC evaluation, COSO/ERM frameworks, risk heat mapping")
    pdf.bold_bullet("IT Audit", "Active Directory reviews, change management, database security, segregation of duties (SoD)")
    pdf.bold_bullet("Tools", "AuditBoard, TeamMate+, ACL Analytics, IDEA, ServiceNow GRC")
    pdf.bold_bullet("Data Analysis", "SQL, Python (basic), Excel/VBA (advanced), Power BI")
    pdf.bold_bullet("Frameworks", "COSO 2013, NIST CSF, COBIT 2019, ISO 27001")
    pdf.section_heading("Project Contributions", level=3)
    pdf.bold_bullet("Fortune 500 Financial Services Firm", "Executed SOX 404 testing for 18 key controls across revenue, procurement, and financial reporting cycles. Identified 2 control deficiencies and worked with management to design and implement remediation plans before year-end.")
    pdf.bold_bullet("Technology Company IPO Readiness", "Supported SOX readiness assessment for pre-IPO SaaS company. Documented 42 business processes, identified 65 key controls, and designed testing procedures. Contributed to successful first-year SOX compliance with no material weaknesses.")
    pdf.bold_bullet("Healthcare System Internal Audit", "Conducted HIPAA privacy and security risk assessment across 12-hospital system. Tested 85 controls against NIST CSF framework and prepared findings report for Board Audit Committee presentation.")
    pdf.section_heading("Training Completed", level=3)
    pdf.bullet("Meridian Risk Advisory Foundations Program (2023)")
    pdf.bullet("SOX 404 Testing Methodology - Advanced Course (2024)")
    pdf.bullet("CISA Exam Preparation Course (2025)")
    pdf.bullet("Meridian Professional Communications Workshop (2024)")
    pdf.bullet("Data Analytics for Auditors - Internal Course (2025)")

    pdf.output(os.path.join(OUTPUT_DIR, "execution_bios.pdf"))
    print("Generated execution_bios.pdf")


# ═══════════════════════════════════════════════════════════════════════════
# 4. RATE CARDS
# ═══════════════════════════════════════════════════════════════════════════

def generate_rate_cards():
    pdf = MeridianPDF("Professional Services Rate Card", "Standard Hourly Rates & Pricing Policies", confidential=True)
    pdf.cover_page(version="4.0", date="January 2026")

    pdf.add_page()
    pdf.section_heading("1. Standard Hourly Rates by Level")
    pdf.body_text(
        "The following table presents Meridian & Associates' standard hourly billing rates by professional "
        "level for the 2026 fiscal year. Rates are denominated in US Dollars (USD) and are applicable "
        "to all service lines unless otherwise specified in a client-specific engagement letter or "
        "master services agreement."
    )

    # Table: Onshore rates
    pdf.section_heading("1.1 Onshore Rates (US-Based Professionals)", level=2)
    pdf.set_font("Helvetica", "B", 9)
    col_w = [55, 35, 35, 35, 30]
    headers = ["Professional Level", "Standard Rate", "Financial Svcs", "Public Sector", "Blended"]
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows = [
        ["Partner", "$750 - $850/hr", "$800 - $850/hr", "$650 - $750/hr", "$800/hr"],
        ["Managing Director", "$600 - $700/hr", "$650 - $700/hr", "$550 - $625/hr", "$650/hr"],
        ["Senior Manager", "$450 - $525/hr", "$475 - $525/hr", "$400 - $475/hr", "$490/hr"],
        ["Manager", "$350 - $425/hr", "$375 - $425/hr", "$325 - $385/hr", "$390/hr"],
        ["Senior Consultant", "$275 - $350/hr", "$300 - $350/hr", "$250 - $310/hr", "$310/hr"],
        ["Consultant", "$200 - $275/hr", "$225 - $275/hr", "$175 - $240/hr", "$240/hr"],
        ["Analyst", "$140 - $200/hr", "$160 - $200/hr", "$125 - $175/hr", "$170/hr"],
    ]
    for i, row in enumerate(rows):
        pdf.set_font("Helvetica", "B" if i == 0 else "", 9)
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(6)
    pdf.section_heading("1.2 Offshore Rates (India-Based Professionals)", level=2)
    pdf.body_text(
        "Meridian maintains a Global Delivery Center (GDC) in Hyderabad, India, staffed with 850+ "
        "professionals across technology, analytics, tax compliance, and audit support. Offshore rates "
        "represent a 40-60% discount to onshore equivalents."
    )
    pdf.set_font("Helvetica", "B", 9)
    col_w2 = [55, 40, 40, 40]
    headers2 = ["Professional Level", "Offshore Rate", "Discount vs Onshore", "Blended"]
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers2):
        pdf.cell(col_w2[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows2 = [
        ["Senior Manager", "$220 - $280/hr", "48% - 53%", "$250/hr"],
        ["Manager", "$165 - $215/hr", "49% - 53%", "$190/hr"],
        ["Senior Consultant", "$120 - $175/hr", "50% - 57%", "$145/hr"],
        ["Consultant", "$85 - $135/hr", "51% - 58%", "$110/hr"],
        ["Analyst", "$60 - $95/hr", "53% - 57%", "$75/hr"],
    ]
    for i, row in enumerate(rows2):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w2[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(6)
    pdf.section_heading("1.3 Nearshore Rates (Latin America-Based Professionals)", level=2)
    pdf.body_text(
        "Our nearshore delivery centers in Monterrey, Mexico and Bogota, Colombia provide time-zone-aligned "
        "support with a 25-35% discount to onshore rates. Nearshore professionals operate during US "
        "business hours and are fully bilingual (English/Spanish)."
    )
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers2):
        pdf.cell(col_w2[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows3 = [
        ["Senior Manager", "$310 - $380/hr", "26% - 31%", "$345/hr"],
        ["Manager", "$250 - $310/hr", "27% - 29%", "$280/hr"],
        ["Senior Consultant", "$195 - $255/hr", "27% - 29%", "$225/hr"],
        ["Consultant", "$145 - $200/hr", "27% - 28%", "$175/hr"],
        ["Analyst", "$100 - $145/hr", "28% - 29%", "$120/hr"],
    ]
    for i, row in enumerate(rows3):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w2[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    # Volume discounts
    pdf.add_page()
    pdf.section_heading("2. Volume Discount Schedule")
    pdf.body_text(
        "Meridian offers volume-based discounts to clients with significant annual spend commitments. "
        "Discounts are applied retroactively upon reaching each tier threshold within the fiscal year "
        "(January 1 - December 31) and are calculated on aggregate fees across all Meridian service lines."
    )

    pdf.set_font("Helvetica", "B", 9)
    col_w3 = [60, 40, 50]
    headers3 = ["Annual Spend Threshold", "Discount", "Effective Blended Savings"]
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers3):
        pdf.cell(col_w3[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows4 = [
        ["$1,000,000 - $4,999,999", "5%", "~$50K - $250K savings"],
        ["$5,000,000 - $9,999,999", "10%", "~$500K - $1M savings"],
        ["$10,000,000+", "15%", "~$1.5M+ savings"],
    ]
    for i, row in enumerate(rows4):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w3[j], 6.5, val, border=1, fill=fill, align="C")
        pdf.ln()

    pdf.ln(6)
    pdf.section_heading("3. Rate Escalation Policy")
    pdf.body_text(
        "Standard hourly rates are subject to annual adjustment effective January 1 of each calendar year. "
        "Rate escalation is capped at 3.0% per annum for clients with active multi-year master services "
        "agreements (MSAs). For clients without an MSA, rate adjustments are communicated 90 days in "
        "advance and are based on market conditions, inflation indices, and competitive benchmarking."
    )
    pdf.bullet("Annual escalation cap: 3.0% for MSA clients")
    pdf.bullet("Non-MSA clients: rate adjustments communicated 90 days in advance")
    pdf.bullet("No mid-engagement rate increases for fixed-scope statements of work")
    pdf.bullet("Rate lock available for 24-month commitments exceeding $5M annual spend")

    pdf.ln(4)
    pdf.section_heading("4. Alternative Fee Arrangements")
    pdf.body_text(
        "Meridian offers flexible pricing models tailored to client needs and engagement characteristics. "
        "The following alternative fee arrangements are available upon request:"
    )
    pdf.bold_bullet("Fixed Fee", "Predetermined total engagement cost based on agreed scope. Recommended for well-defined deliverable-based engagements. Includes 10% contingency buffer.")
    pdf.bold_bullet("Capped Fee", "Time and materials billing with a maximum fee ceiling. Provides budget certainty while maintaining flexibility for scope evolution. Cap set at 110-120% of estimated fees.")
    pdf.bold_bullet("Risk/Reward", "Base fee at reduced rate (typically 70-80% of standard) with success bonus tied to measurable outcomes. Available for transformation and cost reduction engagements.")
    pdf.bold_bullet("Retainer", "Monthly fixed fee for ongoing advisory access. Typically includes defined hours per month with rollover provisions. 10% discount vs. hourly equivalent.")
    pdf.bold_bullet("Managed Services", "Fixed monthly fee for ongoing operational services (e.g., managed SOC, tax compliance). Priced per transaction/user/entity with SLA-based performance guarantees.")

    pdf.add_page()
    pdf.section_heading("5. Travel & Expense Policy")
    pdf.body_text(
        "Travel and out-of-pocket expenses are billed at actual cost with no markup, subject to the "
        "following policies and caps. All expenses must comply with Meridian's Travel & Expense Policy "
        "and are subject to client approval for individual expenses exceeding $500."
    )
    pdf.bold_bullet("Airfare", "Coach/economy class for flights under 5 hours; premium economy for flights 5-8 hours; business class for flights exceeding 8 hours. Booking required 14+ days in advance.")
    pdf.bold_bullet("Lodging", "Actual cost, not to exceed GSA per diem rates (or local equivalent) for the engagement location. Extended stay negotiated rates apply for engagements exceeding 30 days.")
    pdf.bold_bullet("Ground Transportation", "Actual cost for rental car, rideshare, or public transit. Mileage reimbursed at IRS standard rate ($0.67/mile for 2026).")
    pdf.bold_bullet("Meals", "Actual cost, not to exceed $75 per day per person. Client entertainment meals require pre-approval for amounts exceeding $150 per person.")
    pdf.bold_bullet("Expense Cap", "Total T&E not to exceed 12% of professional fees unless pre-approved. Monthly expense reports provided with all supporting documentation.")
    pdf.body_text(
        "For primarily remote engagements, Meridian offers a reduced T&E allocation with on-site presence "
        "limited to key milestones (kickoff, workshops, go-live, steering committee meetings). This "
        "typically reduces T&E to 3-5% of professional fees."
    )

    # --- Large Enterprise ---
    pdf.add_page()
    pdf.section_heading("6. Large Enterprise & Transformation Engagements")
    pdf.body_text(
        "The standard rate structures in Sections 1-4 are calibrated for mid-market engagements "
        "($500M - $5B client revenue). Large enterprise and Fortune 500 / Global 2000 engagements "
        "involve additional complexity, regulatory scrutiny, geographic scope, and risk that are reflected "
        "in the following pricing adjustments and sample cost models."
    )

    pdf.section_heading("6.1 Large Enterprise Rate Premiums", level=2)
    pdf.body_text(
        "Engagements for Fortune 500 and Global 2000 clients are subject to a rate premium of 10-15% "
        "above standard rates, reflecting:"
    )
    pdf.bullet("Increased regulatory and compliance complexity (multi-jurisdictional, SEC Large Accelerated Filer requirements)")
    pdf.bullet("Greater coordination overhead (multiple business units, geographies, time zones)")
    pdf.bullet("Enhanced quality assurance requirements (mandatory EQR, concurrence partners, national office consultation)")
    pdf.bullet("Senior staffing requirements (higher ratio of Manager+ level professionals)")
    pdf.bullet("Dedicated account team infrastructure (relationship partner, account coordinator, innovation liaison)")
    pdf.ln(2)

    pdf.section_heading("6.2 Sample Large Enterprise Cost Models", level=2)
    pdf.body_text(
        "The following cost estimates are illustrative for engagements typical of Fortune 500 / Global 2000 "
        "clients. All estimates assume standard rate structures with the 10-15% large enterprise premium "
        "applied, before volume discounts."
    )

    pdf.set_font("Helvetica", "B", 9)
    col_w_le = [80, 35, 40, 35]
    headers_le = ["Engagement Type", "Duration", "Team Size", "Fee Range"]
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers_le):
        pdf.cell(col_w_le[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows_le = [
        ["Large Integrated Audit (Fortune 500)", "Annual", "25-60", "$3M - $8M/year"],
        ["Enterprise-Wide Digital Transformation", "24 months", "80-150+", "$15M - $40M"],
        ["Post-Merger Integration (Multi-Year)", "18-36 months", "40-100", "$10M - $35M"],
        ["Enterprise Cloud Migration (1000+ Apps)", "18-30 months", "50-120", "$20M - $50M"],
    ]
    for i, row in enumerate(rows_le):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w_le[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.section_heading("6.3 Multi-Year Engagement Discount Structure", level=2)
    pdf.body_text(
        "Large enterprise clients frequently engage Meridian across multi-year programs. The following "
        "additional discounts are available for committed multi-year arrangements, applied on top of "
        "standard volume discounts:"
    )

    pdf.set_font("Helvetica", "B", 9)
    col_w_my = [60, 35, 95]
    headers_my = ["Commitment Term", "Additional Discount", "Conditions"]
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers_my):
        pdf.cell(col_w_my[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows_my = [
        ["2-Year MSA", "3%", "Minimum $2M annual spend commitment"],
        ["3-Year MSA", "5%", "Minimum $3M annual spend commitment"],
        ["5-Year Strategic Partnership", "8% (negotiable)", "Minimum $5M annual spend; joint innovation program"],
    ]
    for i, row in enumerate(rows_my):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w_my[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.section_heading("6.4 Dedicated Account Team Pricing Model", level=2)
    pdf.body_text(
        "For clients with $5M+ annual spend, Meridian provides a dedicated account team structure at no "
        "additional charge. The account team includes:"
    )
    pdf.bullet("Relationship Partner -- Senior partner with P&L accountability for the client relationship; monthly strategic reviews")
    pdf.bullet("Account Director -- Full-time client-facing role coordinating across all active engagements and service lines")
    pdf.bullet("Innovation Liaison -- Access to Meridian's R&D and emerging technology practice for quarterly innovation briefings")
    pdf.bullet("Preferred staffing -- Priority access to top-rated professionals and specialists during peak periods")
    pdf.body_text(
        "For clients with $10M+ annual spend, the dedicated account team is supplemented with an on-site "
        "Account Coordinator (partially funded by Meridian) and annual strategic planning workshops with "
        "the Meridian executive leadership team."
    )

    pdf.add_page()
    pdf.section_heading("7. Payment Terms")
    pdf.body_text("Standard payment terms are as follows:")
    pdf.bullet("Invoicing: Semi-monthly (1st and 15th of each month) for time and materials; milestone-based for fixed fee")
    pdf.bullet("Payment due: Net 30 days from invoice date")
    pdf.bullet("Late payment: 1.5% monthly interest on overdue balances (waived for first occurrence)")
    pdf.bullet("Retainer deposits: 10% of estimated engagement fees, credited against final invoice")
    pdf.bullet("Electronic payment: ACH or wire transfer; credit card accepted with 2.5% processing surcharge")

    pdf.output(os.path.join(OUTPUT_DIR, "rate_cards.pdf"))
    print("Generated rate_cards.pdf")


# ═══════════════════════════════════════════════════════════════════════════
# 5. CASE STUDY: FINANCIAL SERVICES
# ═══════════════════════════════════════════════════════════════════════════

def generate_case_study_financial_services():
    pdf = MeridianPDF(
        "Case Study: Core Banking\nSystem Modernization",
        "Major Retail Banking Institution",
        client_confidential=True
    )
    pdf.cover_page(version="2.0", date="December 2025")

    pdf.add_page()
    pdf.section_heading("1. Engagement Overview")
    col = [40, 0]
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

    pdf.section_heading("3. Meridian's Solution", level=1)
    pdf.body_text(
        "Meridian designed and executed a phased migration strategy to replace the legacy mainframe core "
        "with a cloud-native core banking platform while maintaining uninterrupted service to 22 million "
        "accounts. The solution architecture comprised four integrated workstreams:"
    )
    pdf.section_heading("3.1 Core Banking Platform Selection & Implementation", level=2)
    pdf.body_text(
        "After a rigorous 12-week evaluation of Temenos Transact, Thought Machine Vault, and Finacle, "
        "the team selected Thought Machine Vault as the target core banking platform. Key selection "
        "criteria included cloud-native architecture (Kubernetes-based), smart contract-driven product "
        "configuration, and real-time event-driven processing. Meridian led the platform implementation "
        "using an agile delivery methodology with 2-week sprints, deploying the platform on AWS EKS "
        "across three availability zones."
    )
    pdf.section_heading("3.2 API Layer & Integration Architecture", level=2)
    pdf.body_text(
        "Meridian designed and implemented a comprehensive API gateway layer using Kong Enterprise, "
        "exposing 450+ RESTful APIs for internal and external consumption. The API layer served as the "
        "integration backbone, decoupling the core banking platform from downstream channels (mobile, "
        "web, branch, ATM) and enabling fintech partner integration. An event-driven architecture "
        "using Apache Kafka processed over 2.8 million events per hour at peak, providing real-time "
        "data feeds for regulatory reporting, fraud detection, and customer analytics."
    )
    pdf.section_heading("3.3 Data Migration & Parallel Run", level=2)
    pdf.body_text(
        "The data migration workstream addressed 22 million customer accounts, 380 million historical "
        "transactions (7 years), and 14 product configurations. Meridian developed a custom migration "
        "framework using AWS DMS and custom Python ETL pipelines, executing three mock migrations before "
        "the production cutover. A 90-day parallel run period validated data integrity with 99.9997% "
        "accuracy before the legacy system was decommissioned."
    )
    pdf.section_heading("3.4 Real-Time Payments Enablement", level=2)
    pdf.body_text(
        "As part of the modernization, Meridian enabled the bank's connection to the FedNow instant "
        "payments network and upgraded the bank's RTP (Real-Time Payments) connectivity. The new "
        "architecture supported sub-second payment processing compared to the previous 2-4 hour batch "
        "cycle, positioning the bank as a leader in instant payments among top-10 US retail banks."
    )

    pdf.add_page()
    pdf.section_heading("4. Delivery Approach & Team Composition")
    pdf.body_text(
        "The engagement was structured as a multi-phase program with dedicated workstream leads, "
        "an integrated PMO, and a rigorous governance framework. Key delivery elements included:"
    )
    pdf.bullet("Agile delivery with 2-week sprints, PI planning every 10 weeks (SAFe-aligned)")
    pdf.bullet("85-person team at peak: 35 onshore, 50 offshore (Hyderabad GDC)")
    pdf.bullet("Team composition: 2 Partners, 4 Senior Managers, 8 Managers, 22 Senior Consultants, 28 Consultants, 21 Analysts")
    pdf.bullet("Weekly steering committee with C-suite sponsors (CTO, CIO, CFO)")
    pdf.bullet("Bi-weekly regulatory updates to OCC relationship management team")
    pdf.bullet("Independent quality assurance reviews at each phase gate")

    pdf.section_heading("5. Technology Stack")
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

    pdf.section_heading("6. Results & Impact")
    pdf.body_text(
        "The core banking modernization program delivered transformative results across all key "
        "performance dimensions, exceeding original business case projections in several areas:"
    )
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    col_w = [65, 45, 45, 35]
    headers = ["Metric", "Baseline (Pre)", "Result (Post)", "Improvement"]
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows = [
        ["Transaction Processing Time", "4.2 seconds avg", "2.5 seconds avg", "40% reduction"],
        ["Annual Infrastructure Cost", "$78M", "$46M", "$32M savings"],
        ["System Uptime", "99.92%", "99.99%", "Near-zero downtime"],
        ["Customer NPS", "42", "67", "+25 points"],
        ["Regulatory Reporting Latency", "24-48 hours", "Real-time", "Eliminated batch lag"],
        ["API Integration Time", "6-9 months", "2-4 weeks", "90% faster"],
        ["Time to Market (new products)", "9-12 months", "4-6 weeks", "85% faster"],
    ]
    for i, row in enumerate(rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.section_heading("7. Client Testimonial")
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
    print("Generated case_study_financial_services.pdf")


# ═══════════════════════════════════════════════════════════════════════════
# 6. CASE STUDY: HEALTHCARE
# ═══════════════════════════════════════════════════════════════════════════

def generate_case_study_healthcare():
    pdf = MeridianPDF(
        "Case Study: Post-Merger\nIntegration",
        "Regional Hospital System",
        client_confidential=True
    )
    pdf.cover_page(version="1.3", date="November 2025")

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
        ("Meridian Offices:", "Chicago (lead), New York, Hyderabad (GDC)"),
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

    pdf.section_heading("3. Meridian's Solution")
    pdf.body_text(
        "Meridian designed and executed a comprehensive post-merger integration program organized into "
        "four interconnected workstreams, each with dedicated leadership and measurable milestones:"
    )
    pdf.section_heading("3.1 Unified Epic Implementation", level=2)
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
    pdf.section_heading("3.2 Clinical Workflow Harmonization", level=2)
    pdf.body_text(
        "Meridian deployed a clinical integration team of 35 professionals (including 8 clinicians with "
        "direct patient care experience) to harmonize clinical workflows across the merged system. The team "
        "facilitated 220 clinical governance sessions involving 600+ physicians and clinical leaders to "
        "develop unified order sets (reduced from 4,800 to 1,200), a single formulary (consolidated from "
        "two formularies with 62% overlap), and standardized clinical documentation templates for all "
        "major service lines."
    )

    pdf.add_page()
    pdf.section_heading("3.3 Shared Services Center for Revenue Cycle", level=2)
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

    pdf.section_heading("3.4 IT Infrastructure Consolidation", level=2)
    pdf.body_text(
        "The IT consolidation workstream addressed the merger of two independent data centers, network "
        "infrastructure, and end-user computing environments. Key activities included data center "
        "consolidation from 4 facilities to 2 (primary + disaster recovery), network interconnection "
        "via dedicated MPLS circuits, Active Directory forest merge, and unified endpoint management "
        "for 28,000 devices. The team also consolidated 14 redundant clinical applications, reducing "
        "annual application licensing costs by $6.8M."
    )

    pdf.section_heading("4. Delivery Approach & Team Composition")
    pdf.body_text("The 24-month program was structured into three phases:")
    pdf.bold_bullet("Phase 1 - Foundation (Months 1-6)", "Integration planning, governance structure, EHR platform decision, clinical workflow assessment, Day 1 readiness activities")
    pdf.bold_bullet("Phase 2 - Execution (Months 7-18)", "Epic Wave 1 and Wave 2 deployments, shared services center buildout, IT infrastructure consolidation, clinical workflow harmonization")
    pdf.bold_bullet("Phase 3 - Optimization (Months 19-24)", "Performance optimization, benefits realization tracking, knowledge transfer, transition to steady-state operations")
    pdf.ln(2)
    pdf.body_text("Team composition at peak staffing (120+ professionals):")
    pdf.bullet("2 Partners, 6 Senior Managers, 12 Managers, 32 Senior Consultants, 40 Consultants, 28 Analysts")
    pdf.bullet("8 embedded clinicians (3 physicians, 3 RNs, 2 pharmacists) for clinical workflow design")
    pdf.bullet("35,000 end users trained through a blended learning model (e-learning, classroom, at-the-elbow support)")
    pdf.bullet("Dedicated OCM (Organizational Change Management) team of 15 professionals")

    pdf.section_heading("5. Results & Impact")
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    col_w = [65, 40, 40, 45]
    headers = ["Metric", "Baseline", "Result", "Improvement"]
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows = [
        ["Synergies Realized (annual)", "$0 (pre-merger)", "$52M", "116% of $45M target"],
        ["Claims Denial Rate", "12.4%", "9.7%", "22% reduction"],
        ["Patient Record Unification", "Dual systems", "Single EHR", "100% unified"],
        ["Physician Satisfaction", "76%", "82%", "Maintained >80%"],
        ["Days in A/R", "48.2 days", "38.6 days", "20% reduction"],
        ["IT Application Portfolio", "280 applications", "196 applications", "30% consolidation"],
        ["Annual IT Operating Cost", "$62M combined", "$44M unified", "$18M savings"],
    ]
    for i, row in enumerate(rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.section_heading("6. Client Testimonial")
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
    print("Generated case_study_healthcare.pdf")


# ═══════════════════════════════════════════════════════════════════════════
# 7. CASE STUDY: MANUFACTURING
# ═══════════════════════════════════════════════════════════════════════════

def generate_case_study_manufacturing():
    pdf = MeridianPDF(
        "Case Study: Supply Chain\nTransformation",
        "Global Industrial Manufacturer",
        client_confidential=True
    )
    pdf.cover_page(version="1.1", date="October 2025")

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
    pdf.bold_bullet("Delivery Performance Deterioration", "On-Time-In-Full (OTIF) delivery had declined from 91% to 82% over three years, directly impacting customer satisfaction and contributing to $28M in customer penalties and lost contract renewals. The root cause analysis revealed fragmented order promising logic, disconnected transportation planning, and lack of real-time inventory visibility across facilities.")
    pdf.bold_bullet("Logistics Cost Escalation", "Total logistics costs (transportation, warehousing, and distribution) had increased by 34% over three years to $412M annually, driven by expedited shipping to compensate for poor planning, suboptimal carrier utilization, and a distribution network that had not been redesigned since 2015.")
    pdf.bold_bullet("Supply Chain Sustainability Gap", "The company had committed to Science Based Targets (SBTi) for Scope 3 emissions reduction but lacked visibility into supplier emissions data. Only 12 of their top 200 suppliers had provided emissions data, creating a significant ESG reporting and compliance risk.")

    pdf.section_heading("3. Meridian's Solution")
    pdf.body_text(
        "Meridian designed and delivered a holistic supply chain transformation program comprising "
        "four integrated workstreams:"
    )
    pdf.section_heading("3.1 SAP IBP Implementation", level=2)
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
    pdf.section_heading("3.2 Supply Chain Control Tower", level=2)
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

    pdf.section_heading("3.3 Supplier Collaboration Portal", level=2)
    pdf.body_text(
        "To address supplier visibility gaps, Meridian built a cloud-based Supplier Collaboration Portal "
        "using SAP Ariba and custom extensions. The portal enabled real-time purchase order collaboration, "
        "advance ship notice (ASN) exchange, quality certificate submission, and capacity commitment "
        "sharing. Within 6 months of launch, 280 of the top 300 suppliers (93%) were actively using "
        "the portal, reducing purchase order cycle time from 5.2 days to 1.8 days and improving supplier "
        "on-time delivery from 78% to 91%."
    )

    pdf.section_heading("3.4 Sustainability & Scope 3 Emissions Visibility", level=2)
    pdf.body_text(
        "Meridian integrated an ESG data collection module into the Supplier Collaboration Portal, "
        "enabling standardized Scope 3 emissions data collection aligned with the GHG Protocol. The team "
        "developed supplier-specific emissions factors for the top 200 suppliers (representing 82% of "
        "procurement spend) using a combination of primary data collection and industry-average estimation "
        "models. This created the foundation for the client's first comprehensive Scope 3 emissions "
        "baseline, enabling target-setting and progress tracking against SBTi commitments."
    )

    pdf.section_heading("4. Delivery Approach")
    pdf.body_text("The 16-month program was delivered in three phases:")
    pdf.bold_bullet("Phase 1 - Design & Foundation (Months 1-4)", "Current state assessment, solution architecture, IBP system design, control tower requirements, supplier portal MVP design")
    pdf.bold_bullet("Phase 2 - Build & Deploy (Months 5-12)", "IBP configuration and testing, control tower development, supplier onboarding (3 waves), network optimization analysis, change management")
    pdf.bold_bullet("Phase 3 - Optimize & Scale (Months 13-16)", "ML model tuning, advanced analytics deployment, remaining supplier onboarding, benefits realization, knowledge transfer")
    pdf.ln(2)
    pdf.body_text("Team composition at peak (65 professionals):")
    pdf.bullet("1 Partner, 3 Senior Managers, 6 Managers, 18 Senior Consultants, 22 Consultants, 15 Analysts")
    pdf.bullet("45 onshore (Chicago, client sites), 20 offshore (Hyderabad GDC)")
    pdf.bullet("Embedded at 3 client manufacturing sites and 2 distribution centers")

    pdf.section_heading("5. Results & Impact")
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    col_w = [60, 42, 42, 46]
    headers = ["Metric", "Baseline", "Result", "Improvement"]
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows = [
        ["Inventory Level", "$380M (74 DOS)", "$274M (48 DOS)", "28% reduction"],
        ["Working Capital Freed", "-", "$106M", "One-time release"],
        ["OTIF Delivery", "82%", "95%", "+13 points"],
        ["Forecast Accuracy (4-wk)", "52%", "78%", "+26 points"],
        ["Logistics Cost", "$412M/year", "$338M/year", "18% reduction"],
        ["Supplier On-Time Delivery", "78%", "91%", "+13 points"],
        ["Scope 3 Data Coverage", "6% of suppliers", "Top 200 (82% spend)", "Full visibility"],
    ]
    for i, row in enumerate(rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.section_heading("6. Client Testimonial")
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
    print("Generated case_study_manufacturing.pdf")


# ═══════════════════════════════════════════════════════════════════════════
# 8. CASE STUDY: PUBLIC SECTOR
# ═══════════════════════════════════════════════════════════════════════════

def generate_case_study_public_sector():
    pdf = MeridianPDF(
        "Case Study: Enterprise Cloud\nMigration",
        "State Government Agency",
        client_confidential=True
    )
    pdf.cover_page(version="1.0", date="September 2025")

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

    pdf.section_heading("3. Meridian's Solution")
    pdf.body_text(
        "Meridian designed and executed a comprehensive enterprise cloud migration program using a "
        "modified 6R framework (Rehost, Replatform, Refactor, Rearchitect, Retire, Retain) tailored "
        "to the unique requirements of government IT:"
    )

    pdf.section_heading("3.1 Cloud Foundation & Landing Zone", level=2)
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
    pdf.section_heading("3.2 Application Migration (6R Disposition)", level=2)
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

    pdf.section_heading("3.3 DevSecOps Pipeline", level=2)
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

    pdf.section_heading("3.4 Modern Workplace (Microsoft 365 & Teams)", level=2)
    pdf.body_text(
        "As part of the broader modernization initiative, Meridian led the migration of 45,000 users from "
        "on-premises Exchange 2016 and legacy file shares to Microsoft 365 (Exchange Online, SharePoint "
        "Online, OneDrive, Teams). The migration was executed over 12 weekends using a wave-based approach, "
        "with zero data loss and less than 30 minutes of mail delivery delay per user. The deployment "
        "included Microsoft Teams as the unified communications platform, replacing a fragmented mix of "
        "Cisco Jabber, Skype for Business, and ad-hoc Zoom accounts."
    )

    pdf.section_heading("4. Delivery Approach")
    pdf.body_text("The 30-month program was organized into four phases:")
    pdf.bold_bullet("Phase 1 - Foundation (Months 1-6)", "Application discovery and assessment, landing zone design and deployment, security framework, migration factory setup, workforce training program launch")
    pdf.bold_bullet("Phase 2 - Wave 1 Migration (Months 7-14)", "Migration of 600 applications (low-complexity rehost/replatform), M365 migration, DevSecOps platform deployment, first cost savings realization")
    pdf.bold_bullet("Phase 3 - Wave 2 Migration (Months 15-24)", "Migration of 840 applications (medium/high complexity), refactoring of citizen-facing applications, application retirement execution, ongoing workforce development")
    pdf.bold_bullet("Phase 4 - Optimization (Months 25-30)", "Performance tuning, cost optimization, remaining migrations, knowledge transfer, transition to managed operations, benefits realization reporting")
    pdf.ln(2)
    pdf.body_text("Team composition at peak (90 professionals):")
    pdf.bullet("1 Partner, 4 Senior Managers, 8 Managers, 24 Senior Consultants, 32 Consultants, 21 Analysts")
    pdf.bullet("55 onshore (D.C., client data centers), 35 offshore (Hyderabad GDC)")
    pdf.bullet("Dedicated security team of 12 (including 3 FedRAMP-experienced assessors)")
    pdf.bullet("240 agency IT staff trained and certified in Azure fundamentals (AZ-900) and Azure Administrator (AZ-104)")

    pdf.add_page()
    pdf.section_heading("5. Results & Impact")
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    col_w = [60, 42, 42, 46]
    headers = ["Metric", "Baseline", "Result", "Improvement"]
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows = [
        ["Applications Migrated", "0 in cloud", "1,800 migrated", "72% of portfolio"],
        ["IT Operating Costs", "$52M/year", "$34M/year", "35% ($18M savings)"],
        ["System Availability", "99.2% (14 outages/qtr)", "99.95%", "Near-zero outages"],
        ["Security Incidents", "23/year", "0 during migration", "Zero incidents"],
        ["Mean Time to Deploy", "6-8 weeks", "2-4 hours", "99% faster"],
        ["Cloud Certifications", "38 staff", "278 staff", "632% increase"],
        ["Applications Retired", "-", "700 decommissioned", "$4.2M cost avoided"],
    ]
    for i, row in enumerate(rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(3)
    pdf.body_text(
        "The agency was recognized with the state's annual IT Modernization Award and was rated "
        '"Leader" in the National Association of State CIOs (NASCIO) State IT Modernization Index for '
        "the first time in its history. The program's self-funding model, in which early-phase cost "
        "savings funded subsequent phases, has been adopted as a reference model by three other state "
        "agencies planning similar migrations."
    )

    pdf.ln(4)
    pdf.section_heading("6. Client Testimonial")
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
    print("Generated case_study_public_sector.pdf")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    generate_executive_bios()
    generate_management_bios()
    generate_execution_bios()
    generate_rate_cards()
    generate_case_study_financial_services()
    generate_case_study_healthcare()
    generate_case_study_manufacturing()
    generate_case_study_public_sector()
    print("\nAll 8 PDFs generated successfully!")
