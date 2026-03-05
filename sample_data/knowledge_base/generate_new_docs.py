"""Generate new knowledge base documents for Meridian & Associates LLP.

Tasks:
  1. Extended bios (executive, management, execution)
  2. Expanded rate cards
  3. Two new case studies (energy, retail)
  4. Firm capabilities overview
  5. Quality assurance methodology

Run:  uv run python sample_data/knowledge_base/generate_new_docs.py
"""

from fpdf import FPDF
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TALENT_DIR = os.path.join(BASE_DIR, "talent_proof_sources")
ADVISORY_DIR = os.path.join(BASE_DIR, "advisory_consulting")
COMMON_DIR = os.path.join(BASE_DIR, "common_firm_wide")


# ─── Shared PDF Base ─────────────────────────────────────────────────────

class MeridianPDF(FPDF):
    """Base PDF class matching existing firm branding."""

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

    def cover_page(self, version="1.0", date="March 2026", doc_id=None):
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
        meta_line = f"Version {version}  |  Effective Date: {date}"
        if doc_id:
            meta_line += f"  |  Doc ID: {doc_id}"
        self.cell(0, 6, meta_line, align="C")
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

    def table(self, headers, rows, col_widths=None):
        """Render a styled table with navy header row and alternating fill."""
        if col_widths is None:
            col_widths = [190 // len(headers)] * len(headers)
        # Header row
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        # Data rows
        self.set_text_color(40, 40, 40)
        for idx, row in enumerate(rows):
            fill = idx % 2 == 0
            self.set_fill_color(235, 240, 248)
            for j, val in enumerate(row):
                self.set_font("Helvetica", "B" if j == 0 else "", 9)
                self.cell(col_widths[j], 6.5, val, border=1, fill=fill,
                          align="C" if j > 0 else "L")
            self.ln()

    def check_space(self, needed_mm=45):
        if self.get_y() > (297 - 25 - needed_mm):
            self.add_page()


# =========================================================================
# TASK 1a: Executive Bios Extended
# =========================================================================

def generate_executive_bios_extended():
    pdf = MeridianPDF("Executive Leadership Bios", "Extended Partner Profiles", confidential=True)
    pdf.cover_page(version="3.3", date="March 2026", doc_id="MA-BIO-EXEC-EXT-001")

    # --- Patricia Hoffman ---
    pdf.add_page()
    pdf.section_heading("5. Patricia Hoffman, CPA, Six Sigma Black Belt")
    pdf.section_heading("Partner, Energy & Utilities Practice Lead", level=2)
    pdf.key_value("Years of Experience", "25 years")
    pdf.key_value("Office", "Houston, TX")
    pdf.key_value("Direct Line", "+1 (713) 555-0418")
    pdf.key_value("Email", "p.hoffman@meridian-llp.com")
    pdf.ln(2)

    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Patricia Hoffman is the Partner leading Meridian & Associates' Energy & Utilities Practice, "
        "overseeing advisory, technology, and assurance engagements for integrated oil & gas majors, "
        "midstream operators, electric utilities, and renewable energy developers. With 25 years of "
        "experience across the energy value chain, Patricia has directed programs totaling over "
        "$1.9 billion in aggregate project value, with deep expertise in enterprise cloud migration, "
        "operational technology (OT) modernization, digital twin deployment, and ESG/emissions "
        "reporting platforms."
    )
    pdf.body_text(
        "Before joining Meridian in 2009, Patricia spent nine years at a competing Big Four firm "
        "where she rose to Senior Manager in the energy and resources audit practice, serving "
        "upstream, midstream, and downstream clients across the Gulf Coast. She also spent two years "
        "as Director of IT Strategy at a Fortune 50 integrated energy company, giving her a rare "
        "practitioner perspective. Since her promotion to Partner in 2014, Patricia has grown the "
        "Energy Practice from $62 million to over $245 million in annual revenue, establishing "
        "Meridian as a top-three advisor to US energy companies."
    )

    pdf.section_heading("Education", level=3)
    pdf.bullet("MBA, Energy Finance, Rice University, Jones Graduate School of Business (2005)")
    pdf.bullet("BS, Chemical Engineering, Texas A&M University (1999)")

    pdf.section_heading("Certifications & Memberships", level=3)
    pdf.bullet("Certified Public Accountant (CPA), State of Texas")
    pdf.bullet("Six Sigma Black Belt (ASQ Certified)")
    pdf.bullet("Certified Energy Manager (CEM), Association of Energy Engineers")
    pdf.bullet("Board Member, Center for Houston's Future - Energy Transition Committee")
    pdf.bullet("Advisory Board, Stanford Precourt Institute for Energy")
    pdf.bullet("Member, Society of Petroleum Engineers (SPE)")

    pdf.section_heading("Industry Specializations", level=3)
    pdf.bullet("Enterprise cloud migration for energy companies (OT/IT convergence)")
    pdf.bullet("Digital twin and IoT deployment for refining and midstream operations")
    pdf.bullet("ESG data platforms and Scope 1/2/3 emissions reporting (SEC Climate Rule, ISSB)")
    pdf.bullet("SCADA modernization and industrial cybersecurity (IEC 62443, NERC CIP)")
    pdf.bullet("Regulatory compliance (EPA, PHMSA, FERC, state public utility commissions)")
    pdf.bullet("Operational excellence and asset performance management")

    pdf.section_heading("Notable Engagements (Blinded)", level=3)
    pdf.bold_bullet("Top-5 US Integrated Energy Company",
        "Led 24-month enterprise cloud and digital transformation program (110-person team). "
        "Migrated 1,200 corporate IT applications to Azure, deployed edge computing for field "
        "operations, implemented digital twins for refinery optimization across 8 refineries, "
        "and built ESG data platform for real-time emissions monitoring. Achieved 30% IT cost "
        "reduction, 99.97% uptime, and 15% reduction in unplanned downtime. (See Case Study: "
        "Energy & Digital Transformation)")
    pdf.bold_bullet("Major Electric Utility",
        "Directed $85M grid modernization program including AMI 2.0 deployment, ADMS implementation, "
        "and distributed energy resource management system (DERMS). Enabled real-time outage "
        "detection reducing restoration time by 42% and integrated 2.3 GW of distributed solar.")
    pdf.bold_bullet("Midstream Pipeline Operator",
        "Oversaw SCADA and OT security transformation across 12,000 miles of pipeline infrastructure. "
        "Implemented IEC 62443-compliant architecture, deployed centralized SOC for OT monitoring, "
        "and achieved PHMSA compliance ahead of regulatory deadline.")

    pdf.section_heading("Publications & Thought Leadership", level=3)
    pdf.bullet('"The Energy Cloud: Digital Transformation Strategies for Oil & Gas" - Harvard Business Review (2025)')
    pdf.bullet('"Scope 1 & 2 Emissions Monitoring: From Manual Reporting to Real-Time Platforms" - MIT Energy Initiative (2024)')
    pdf.bullet("Keynote Speaker, CERAWeek by S&P Global (2024, 2025)")
    pdf.bullet("Panelist, World Energy Congress - Digital Transformation Track (2025)")

    # --- Robert Adeyemi ---
    pdf.add_page()
    pdf.section_heading("6. Robert Adeyemi, MBA")
    pdf.section_heading("Partner, Retail & Consumer Practice Lead", level=2)
    pdf.key_value("Years of Experience", "22 years")
    pdf.key_value("Office", "New York, NY")
    pdf.key_value("Direct Line", "+1 (212) 555-0531")
    pdf.key_value("Email", "r.adeyemi@meridian-llp.com")
    pdf.ln(2)

    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Robert Adeyemi leads Meridian & Associates' Retail & Consumer Practice, advising national "
        "retailers, consumer brands, quick-service restaurant chains, and e-commerce platforms on "
        "omnichannel transformation, supply chain optimization, and customer experience strategy. "
        "Over his 22-year career, Robert has managed more than 50 large-scale engagements in the "
        "retail and consumer sector, including unified commerce implementations, demand planning "
        "overhauls, loyalty program redesigns, and post-acquisition integrations for retail portfolios."
    )
    pdf.body_text(
        "Prior to joining Meridian in 2010, Robert spent eight years at a top-tier management "
        "consulting firm focused exclusively on retail and consumer clients and two years as "
        "VP of Supply Chain Strategy at a Fortune 200 specialty retailer. His combination of "
        "strategic consulting and in-house operating experience enables him to design solutions "
        "that are both analytically rigorous and operationally pragmatic. Under his leadership, "
        "the Retail & Consumer Practice has grown to $178 million in annual revenue with a "
        "client retention rate of 92%."
    )

    pdf.section_heading("Education", level=3)
    pdf.bullet("MBA, Marketing & Operations, The Wharton School, University of Pennsylvania (2006)")
    pdf.bullet("BA, Economics, magna cum laude, Morehouse College (2002)")

    pdf.section_heading("Certifications & Memberships", level=3)
    pdf.bullet("Certified Supply Chain Professional (CSCP), APICS")
    pdf.bullet("Board Member, National Retail Federation (NRF) - Technology Council")
    pdf.bullet("Advisory Board, Wharton Baker Retailing Center")
    pdf.bullet("Member, Grocery Manufacturers Association (GMA) Digital Commerce Committee")

    pdf.section_heading("Industry Specializations", level=3)
    pdf.bullet("Omnichannel commerce platform implementation (Salesforce, Shopify Plus, commercetools)")
    pdf.bullet("Supply chain visibility and demand forecasting (Manhattan Active, Blue Yonder)")
    pdf.bullet("Customer data platforms and loyalty program design")
    pdf.bullet("Inventory optimization and ship-from-store / BOPIS enablement")
    pdf.bullet("Retail M&A due diligence and post-acquisition integration")
    pdf.bullet("AI-powered merchandising, pricing, and assortment optimization")

    pdf.section_heading("Notable Engagements (Blinded)", level=3)
    pdf.bold_bullet("Top-20 US Specialty Retailer",
        "Led 20-month omnichannel supply chain and customer experience transformation (75-person team). "
        "Implemented unified commerce platform (Salesforce Commerce Cloud + Manhattan Active), real-time "
        "inventory visibility, BOPIS/ship-from-store, AI-powered demand forecasting, and loyalty program "
        "redesign. Achieved 94% inventory accuracy (from 60%), 28% e-commerce growth, 15% increase in "
        "average order value, and $85M inventory reduction. (See Case Study: Retail Omnichannel "
        "Transformation)")
    pdf.bold_bullet("National Quick-Service Restaurant Chain",
        "Directed $42M digital transformation including mobile ordering platform, kitchen display system "
        "modernization, and AI-driven labor scheduling across 3,200 locations. Increased digital order "
        "mix from 18% to 47% and reduced average order fulfillment time by 35%.")
    pdf.bold_bullet("Global Consumer Packaged Goods Company",
        "Oversaw demand sensing and revenue growth management program across 14 product categories "
        "and 28 markets. Deployed Databricks-based ML platform achieving 23% improvement in forecast "
        "accuracy and $120M reduction in excess inventory.")

    pdf.section_heading("Publications & Thought Leadership", level=3)
    pdf.bullet('"The Unified Commerce Imperative: Beyond Omnichannel" - Harvard Business Review (2025)')
    pdf.bullet('"AI-Powered Supply Chains: From Reactive to Predictive Retail" - MIT Sloan Management Review (2024)')
    pdf.bullet("Keynote Speaker, NRF Big Show (2025), Shoptalk (2024)")
    pdf.bullet("Panelist, Consumer Goods Forum - Digital Commerce Summit (2025)")

    pdf.output(os.path.join(TALENT_DIR, "executive_bios_extended.pdf"))
    print("Generated executive_bios_extended.pdf")


# =========================================================================
# TASK 1b: Management Bios Extended
# =========================================================================

def generate_management_bios_extended():
    pdf = MeridianPDF("Management Team Bios", "Extended Senior Manager & Manager Profiles", confidential=True)
    pdf.cover_page(version="2.2", date="March 2026", doc_id="MA-BIO-MGMT-EXT-001")

    # --- Lauren Mitchell ---
    pdf.add_page()
    pdf.section_heading("5. Lauren Mitchell, SHRM-SCP")
    pdf.section_heading("Senior Manager, Organizational Change Management", level=2)
    pdf.key_value("Years of Experience", "12 years")
    pdf.key_value("Office", "Chicago, IL")
    pdf.key_value("Email", "l.mitchell@meridian-llp.com")
    pdf.ln(2)

    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Lauren Mitchell is a Senior Manager in Meridian's Organizational Change Management (OCM) "
        "practice, leading change strategies for large-scale technology implementations, post-merger "
        "integrations, and operational transformation programs. Over her 12-year career, Lauren has "
        "designed and executed change management programs for 25+ enterprise engagements, supporting "
        "more than 200,000 end users through complex transitions. She is recognized for her ability "
        "to quantify change readiness, build executive coalition strategies, and design communications "
        "plans that measurably accelerate user adoption."
    )
    pdf.body_text(
        "Lauren manages a team of 18 change management professionals and is responsible for $8.5 million "
        "in annual engagement revenue. Before joining Meridian in 2018, she spent six years at a global "
        "management consulting firm and two years in corporate HR at a Fortune 100 healthcare company, "
        "where she led the people-side of a company-wide Workday implementation. Her embedded OCM teams "
        "consistently achieve adoption rates exceeding 85% within 90 days of go-live, compared to the "
        "industry average of 65%."
    )

    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Organizational Development, Vanderbilt University Peabody College (2016)")
    pdf.bullet("BA, Psychology, University of Virginia (2012)")

    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Prosci Certified Change Practitioner (Advanced)")
    pdf.bullet("SHRM Senior Certified Professional (SHRM-SCP)")
    pdf.bullet("Certified Professional in Talent Development (CPTD), ATD")
    pdf.bullet("Kotter Change Leadership Certified")
    pdf.bullet("SAFe 5 Agilist (SA)")

    pdf.section_heading("Technical Specializations", level=3)
    pdf.bullet("Enterprise change management for ERP, EHR, and cloud transformations")
    pdf.bullet("Stakeholder analysis and executive coalition building")
    pdf.bullet("Change readiness assessment and adoption metrics design")
    pdf.bullet("Training strategy and curriculum design (instructor-led, e-learning, at-the-elbow)")
    pdf.bullet("Communications planning and employee engagement campaigns")
    pdf.bullet("Post-merger cultural integration and organizational design")

    pdf.section_heading("Project Highlights", level=3)
    pdf.bold_bullet("12-Hospital Health System Merger",
        "Led OCM workstream for 24-month post-merger integration supporting 38,000 employees "
        "and 4,200 physicians through unified Epic EHR deployment. Designed multi-channel communications "
        "strategy, facilitated 220 clinical governance sessions, and achieved 91% end-user proficiency "
        "within 60 days of go-live. (See Healthcare Case Study)")
    pdf.bold_bullet("Fortune 200 Manufacturer",
        "Directed change management for SAP S/4HANA implementation across 8 distribution centers "
        "and 4,500 impacted users. Created role-based training curriculum covering 380 functional "
        "specifications, deployed super-user network of 120 change champions, and achieved 88% "
        "adoption within 30 days of go-live.")
    pdf.bold_bullet("State Government Agency",
        "Managed workforce transition for 1,800-application cloud migration affecting 12,000 "
        "state employees. Designed digital literacy upskilling program, retrained 85 mainframe "
        "developers in cloud technologies, and achieved 94% employee retention through transition.")

    pdf.section_heading("Team Leadership", level=3)
    pdf.body_text(
        "Lauren leads a team of 18 change management professionals including 4 senior consultants "
        "and 14 consultants/analysts. She designed Meridian's internal OCM Methodology Toolkit, now "
        "used across all advisory engagements, and serves as faculty for the firm's Change Leadership "
        "certification program. Lauren is also co-chair of the firm's Women in Leadership employee "
        "resource group and mentors six junior professionals."
    )

    # --- Raj Krishnamurthy ---
    pdf.add_page()
    pdf.section_heading("6. Raj Krishnamurthy, MS, AWS ML Specialty")
    pdf.section_heading("Manager, Data & Analytics", level=2)
    pdf.key_value("Years of Experience", "9 years")
    pdf.key_value("Office", "San Francisco, CA")
    pdf.key_value("Email", "r.krishnamurthy@meridian-llp.com")
    pdf.ln(2)

    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Raj Krishnamurthy is a Manager in Meridian's Data & Analytics practice, specializing in "
        "enterprise data platform architecture, machine learning engineering, and advanced analytics "
        "solutions. Over his 9-year career, Raj has delivered 14 data platform implementations and "
        "ML production deployments across financial services, retail, and energy sectors. He is "
        "recognized for his ability to translate business requirements into scalable data architectures "
        "and to bridge the gap between data science experimentation and production ML operations."
    )
    pdf.body_text(
        "Raj manages a team of 16 data engineers and data scientists, responsible for $7.2 million "
        "in annual engagement revenue. Before joining Meridian in 2020, he spent five years at a "
        "leading technology consulting firm where he built the data engineering practice from the "
        "ground up. His team has deployed 32 production ML models with an average time-to-production "
        "of 8 weeks, compared to the industry benchmark of 16-24 weeks."
    )

    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Data Science, University of California, Berkeley (2019)")
    pdf.bullet("BTech, Computer Science, Indian Institute of Technology Delhi (2015)")

    pdf.section_heading("Certifications", level=3)
    pdf.bullet("AWS Machine Learning Specialty Certification")
    pdf.bullet("Databricks Certified Data Engineer Professional")
    pdf.bullet("Databricks Certified Machine Learning Professional")
    pdf.bullet("Google Professional Machine Learning Engineer")
    pdf.bullet("Snowflake SnowPro Advanced: Data Engineer")

    pdf.section_heading("Technical Specializations", level=3)
    pdf.bullet("Enterprise data platform architecture (Databricks, Snowflake, BigQuery)")
    pdf.bullet("ML engineering and MLOps (MLflow, SageMaker, Vertex AI)")
    pdf.bullet("Real-time data streaming (Kafka, Spark Structured Streaming, Flink)")
    pdf.bullet("Data governance and quality frameworks (Unity Catalog, Great Expectations, Monte Carlo)")
    pdf.bullet("Cloud data services (AWS, Azure, GCP data stacks)")
    pdf.bullet("Generative AI and LLM application development (RAG, fine-tuning, evaluation)")

    pdf.section_heading("Project Highlights", level=3)
    pdf.bold_bullet("Top-20 US Specialty Retailer",
        "Architected Snowflake + Databricks data platform supporting AI-powered demand forecasting "
        "across 800+ stores and 45,000 SKUs. Deployed 8 production ML models achieving 23% improvement "
        "in forecast accuracy and contributing to $85M inventory reduction. (See Retail Case Study)")
    pdf.bold_bullet("Integrated Energy Company",
        "Built ESG data platform on Azure for real-time Scope 1/2 emissions monitoring across "
        "8 refineries and 12,000 miles of pipeline. Integrated 2,400+ IoT sensors with sub-minute "
        "data latency, enabling SEC Climate Rule-compliant reporting. (See Energy Case Study)")
    pdf.bold_bullet("Fortune 500 Financial Services Firm",
        "Designed and deployed enterprise feature store and ML platform on AWS SageMaker supporting "
        "15 production models for fraud detection, credit scoring, and customer churn prediction. "
        "Reduced model deployment time from 6 months to 3 weeks.")

    pdf.section_heading("Team Leadership", level=3)
    pdf.body_text(
        "Raj leads a team of 16 professionals including 5 senior data engineers, 4 ML engineers, "
        "4 data analysts, and 3 junior consultants. He designed Meridian's Data Engineering Academy, "
        "a 16-week upskilling program that has certified 45 consultants in modern data stack technologies "
        "since 2022. Raj also serves as the practice's GenAI innovation lead, running quarterly "
        "hackathons and maintaining an internal catalog of approved LLM patterns."
    )

    # --- Sophia Vasquez ---
    pdf.add_page()
    pdf.section_heading("7. Sophia Vasquez, CPA, CMI")
    pdf.section_heading("Senior Manager, State & Local Tax (SALT)", level=2)
    pdf.key_value("Years of Experience", "14 years")
    pdf.key_value("Office", "New York, NY")
    pdf.key_value("Email", "s.vasquez@meridian-llp.com")
    pdf.ln(2)

    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Sophia Vasquez is a Senior Manager in Meridian's Tax Practice, leading the State & Local Tax "
        "(SALT) service line for the Northeast region. Over her 14-year career, Sophia has advised "
        "clients across technology, financial services, manufacturing, and retail industries on SALT "
        "planning, compliance, controversy, and incentives matters spanning all 50 states. She is "
        "recognized as a leading authority on state income tax nexus, apportionment, and the evolving "
        "post-Wayfair sales and use tax landscape."
    )
    pdf.body_text(
        "Sophia manages a team of 20 SALT professionals and is responsible for $10.8 million in annual "
        "engagement revenue. She has secured over $340 million in cumulative state and local tax savings "
        "for clients through audit defense, voluntary disclosure agreements, credit and incentive "
        "negotiations, and restructuring strategies. Before joining Meridian in 2015, she spent five "
        "years at a Big Four firm in the SALT practice and four years at a state Department of Revenue "
        "as a Senior Tax Auditor, giving her valuable insight into the audit perspective."
    )

    pdf.section_heading("Education", level=3)
    pdf.bullet("JD/LLM, Taxation, Georgetown University Law Center (2014)")
    pdf.bullet("BS, Accounting, summa cum laude, Villanova University (2010)")

    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Certified Public Accountant (CPA), States of New York and New Jersey")
    pdf.bullet("Certified Member of the Institute (CMI), Institute for Professionals in Taxation")
    pdf.bullet("Licensed Attorney, State of New York")
    pdf.bullet("Member, American Bar Association - Tax Section, State & Local Committee")
    pdf.bullet("Member, Tax Executives Institute (TEI) - SALT Committee")

    pdf.section_heading("Technical Specializations", level=3)
    pdf.bullet("State income tax nexus analysis and apportionment planning (post-Wayfair)")
    pdf.bullet("Sales and use tax compliance and automation (Vertex, Avalara, Sovos)")
    pdf.bullet("SALT controversy and audit defense (income tax, sales tax, property tax)")
    pdf.bullet("Credits and incentives negotiation (JDIG, EDGE, BEIP, enterprise zone programs)")
    pdf.bullet("Legal entity restructuring for state tax optimization")
    pdf.bullet("Unclaimed property (escheat) compliance and voluntary disclosure")

    pdf.section_heading("Project Highlights", level=3)
    pdf.bold_bullet("Fortune 100 Technology Company",
        "Led comprehensive SALT restructuring that reduced the client's effective state income tax "
        "rate from 5.8% to 3.2%, generating $28M in annual state tax savings. Designed and implemented "
        "IP holding company structure compliant with state economic substance requirements.")
    pdf.bold_bullet("National Retail Chain (800+ Stores)",
        "Directed post-Wayfair sales tax compliance remediation across 42 states. Implemented Vertex "
        "O Series with automated nexus monitoring, reducing compliance risk exposure by $14M and "
        "cutting monthly compliance processing time by 60%. (Relates to Retail Case Study client)")
    pdf.bold_bullet("Manufacturing Conglomerate",
        "Managed multi-state audit defense covering $85M in assessed state income tax deficiencies "
        "across 8 states. Negotiated settlements totaling 18% of original assessments, saving the "
        "client $69.7M, and established prospective voluntary disclosure agreements in 3 new states.")

    pdf.section_heading("Team Leadership", level=3)
    pdf.body_text(
        "Sophia leads a team of 20 SALT professionals across New York, New Jersey, and Connecticut. "
        "She serves as the SALT practice's knowledge management lead, authoring the firm's SALT Policy "
        "Alert series distributed to 450+ clients, and co-chairs the Tax Practice's annual SALT "
        "symposium. Sophia also mentors 8 junior professionals in the firm's formal mentorship program "
        "and teaches the SALT module in the firm's CPA exam preparation program."
    )

    # --- Thomas Chen ---
    pdf.add_page()
    pdf.section_heading("8. Thomas Chen, CISA, CISSP, CISM")
    pdf.section_heading("Manager, IT Audit & Cybersecurity GRC", level=2)
    pdf.key_value("Years of Experience", "10 years")
    pdf.key_value("Office", "Washington, D.C.")
    pdf.key_value("Email", "t.chen@meridian-llp.com")
    pdf.ln(2)

    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Thomas Chen is a Manager in Meridian's Risk & Compliance Practice, specializing in IT audit, "
        "cybersecurity governance, risk and compliance (GRC), and regulatory frameworks for highly "
        "regulated industries. Over his 10-year career, Thomas has led more than 40 IT audit and "
        "cybersecurity assessment engagements across financial services, healthcare, defense industrial "
        "base, and federal government sectors. He is known for his deep expertise in frameworks "
        "including NIST CSF, NIST 800-53, CMMC, HITRUST, and ISO 27001."
    )
    pdf.body_text(
        "Thomas manages a team of 14 IT audit and GRC professionals and oversees $6.8 million in "
        "annual engagement revenue. Before joining Meridian in 2019, he spent five years at a Big Four "
        "firm in the IT audit practice and one year as an Information Security Analyst at a defense "
        "contractor, where he led CMMC readiness efforts. His dual IT audit and cybersecurity background "
        "enables him to assess both control effectiveness and technical security posture in an integrated "
        "manner that clients find uniquely valuable."
    )

    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Information Security, Johns Hopkins University (2018)")
    pdf.bullet("BS, Management Information Systems, University of Maryland (2014)")

    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Certified Information Systems Auditor (CISA)")
    pdf.bullet("Certified Information Systems Security Professional (CISSP)")
    pdf.bullet("Certified Information Security Manager (CISM)")
    pdf.bullet("GIAC Security Essentials (GSEC)")
    pdf.bullet("HITRUST CSF Practitioner (CCSFP)")
    pdf.bullet("CMMC Registered Practitioner (RP)")

    pdf.section_heading("Technical Specializations", level=3)
    pdf.bullet("IT general controls (ITGC) and application controls testing")
    pdf.bullet("Cybersecurity framework assessments (NIST CSF, NIST 800-53, ISO 27001)")
    pdf.bullet("CMMC readiness and certification support for defense contractors")
    pdf.bullet("HITRUST CSF certification for healthcare organizations")
    pdf.bullet("SOC 1/SOC 2 Type II examinations")
    pdf.bullet("Third-party risk management and vendor security assessments")
    pdf.bullet("GRC platform implementation (ServiceNow GRC, RSA Archer, OneTrust)")

    pdf.section_heading("Project Highlights", level=3)
    pdf.bold_bullet("Defense Contractor (Tier 1 Supplier)",
        "Led CMMC Level 2 readiness assessment and remediation program across 6 facilities. "
        "Identified and remediated 142 control gaps, implemented Splunk SIEM and CrowdStrike EDR, "
        "and achieved CMMC Level 2 certification on first assessment attempt.")
    pdf.bold_bullet("Regional Health System",
        "Directed HITRUST CSF certification for 8-hospital system, managing assessment of 450+ "
        "controls across 19 domains. Achieved r2 certification with zero corrective action plans, "
        "the first health system in the region to achieve this distinction.")
    pdf.bold_bullet("Federal Financial Regulator",
        "Managed annual FISMA assessment covering 22 information systems. Led remediation of 38 "
        "POA&M items, implemented continuous monitoring program using Tenable.io, and achieved "
        "'Effective' rating from OIG for the first time in three years.")

    pdf.section_heading("Team Leadership", level=3)
    pdf.body_text(
        "Thomas leads a team of 14 professionals spanning IT audit, cybersecurity GRC, and third-party "
        "risk management. He developed Meridian's CMMC Practice Accelerator toolkit, which has reduced "
        "CMMC readiness assessment timelines by 35%, and serves as a subject matter expert for the "
        "firm's defense industrial base pursuits. Thomas is also a certified instructor for the firm's "
        "CISA and CISSP exam preparation programs and mentors 5 junior professionals."
    )

    pdf.output(os.path.join(TALENT_DIR, "management_bios_extended.pdf"))
    print("Generated management_bios_extended.pdf")


# =========================================================================
# TASK 1c: Execution Bios Extended
# =========================================================================

def generate_execution_bios_extended():
    pdf = MeridianPDF("Execution Team Bios", "Extended Senior Consultant & Staff Profiles", confidential=True)
    pdf.cover_page(version="1.5", date="March 2026", doc_id="MA-BIO-EXEC-TEAM-EXT-001")

    # --- Olivia Brennan ---
    pdf.add_page()
    pdf.section_heading("5. Olivia Brennan, CBAP")
    pdf.section_heading("Senior Consultant, Business Analyst / Testing Lead", level=2)
    pdf.key_value("Years of Experience", "4 years")
    pdf.key_value("Office", "Chicago, IL")
    pdf.key_value("Email", "o.brennan@meridian-llp.com")
    pdf.ln(2)

    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Olivia Brennan is a Senior Consultant in Meridian's Advisory Practice, serving as a Business "
        "Analyst and Testing Lead on large-scale technology implementation programs. Over her 4-year "
        "career, Olivia has contributed to 7 enterprise engagements spanning ERP implementations, "
        "post-merger integrations, and cloud migration programs. She is recognized for her meticulous "
        "requirements traceability, rigorous test strategy design, and ability to coordinate UAT "
        "efforts involving 100+ business users across multiple workstreams."
    )

    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Information Systems Management, Carnegie Mellon University (2022)")
    pdf.bullet("BS, Industrial Engineering, University of Illinois at Urbana-Champaign (2020)")

    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Certified Business Analysis Professional (CBAP), IIBA")
    pdf.bullet("ISTQB Certified Tester - Advanced Level (Test Analyst)")
    pdf.bullet("SAFe 5 Practitioner")
    pdf.bullet("Jira Administration Certified")

    pdf.section_heading("Technical Skills", level=3)
    pdf.bold_bullet("Business Analysis", "Requirements elicitation, process modeling (BPMN), user stories, acceptance criteria, traceability matrices")
    pdf.bold_bullet("Testing", "Test strategy design, test case development, UAT coordination, defect management, regression testing")
    pdf.bold_bullet("Tools", "Jira, Confluence, Azure DevOps, HP ALM/Quality Center, Zephyr, Selenium (basic), Postman")
    pdf.bold_bullet("Data Analysis", "SQL, Excel/VBA (advanced), Power BI, Python (pandas)")
    pdf.bold_bullet("Methodologies", "Agile (Scrum, SAFe), Waterfall, Hybrid")

    pdf.section_heading("Project Contributions", level=3)
    pdf.bold_bullet("Fortune 200 Manufacturer - SAP S/4HANA",
        "Served as Testing Lead for 16-month SAP greenfield implementation. Designed test strategy "
        "covering 1,200+ test cases across MM, PP, SD, and FI modules. Coordinated 3 UAT cycles "
        "with 120 business users and achieved zero critical defects at go-live. Worked closely with "
        "David Kim's team on cutover planning.")
    pdf.bold_bullet("12-Hospital Health System Merger",
        "Led business analysis for revenue cycle workstream during post-merger integration. Documented "
        "42 AS-IS and TO-BE processes for patient access, coding, and claims management. Facilitated "
        "requirements workshops with 85 stakeholders across both legacy networks.")
    pdf.bold_bullet("State Government Cloud Migration",
        "Managed application portfolio rationalization analysis for 1,800 applications. Assessed each "
        "application against 6R framework (rehost, replatform, refactor, repurchase, retain, retire) "
        "and maintained requirements traceability for 340 applications selected for migration.")

    pdf.section_heading("Training Completed", level=3)
    pdf.bullet("Meridian BA/QA Excellence Program (2023)")
    pdf.bullet("SAP S/4HANA Business Process Integration - Internal Course (2024)")
    pdf.bullet("Meridian Leadership Essentials Program (2025)")

    # --- Kwame Asante ---
    pdf.add_page()
    pdf.section_heading("6. Kwame Asante, SAP S/4HANA Certified")
    pdf.section_heading("Senior Consultant, SAP FICO Functional", level=2)
    pdf.key_value("Years of Experience", "5 years")
    pdf.key_value("Office", "Chicago, IL")
    pdf.key_value("Email", "k.asante@meridian-llp.com")
    pdf.ln(2)

    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Kwame Asante is a Senior Consultant specializing in SAP Finance (FI) and Controlling (CO) "
        "functional configuration for S/4HANA environments. With 5 years of experience, Kwame has "
        "contributed to 6 full-lifecycle SAP implementations and 3 system conversion projects across "
        "manufacturing, energy, and retail industries. He is recognized for his expertise in the "
        "Universal Journal, New Asset Accounting, and SAP Central Finance, as well as his ability "
        "to configure complex intercompany and multi-currency scenarios."
    )

    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Accounting, University of Illinois at Urbana-Champaign (2021)")
    pdf.bullet("BBA, Finance & Information Systems, University of Ghana (2019)")

    pdf.section_heading("Certifications", level=3)
    pdf.bullet("SAP Certified Application Associate - SAP S/4HANA Finance")
    pdf.bullet("SAP Certified Application Associate - SAP S/4HANA Management Accounting")
    pdf.bullet("CPA Candidate (3 of 4 sections passed)")
    pdf.bullet("SAFe 5 Practitioner")

    pdf.section_heading("Technical Skills", level=3)
    pdf.bold_bullet("SAP Modules", "FI (GL, AP, AR, AA, BL), CO (CCA, PCA, IO, PA), Treasury (TRM), Intercompany")
    pdf.bold_bullet("S/4HANA Specific", "Universal Journal, New Asset Accounting, Central Finance, Group Reporting")
    pdf.bold_bullet("Integration", "SAP CPI, IDocs, BAPIs, integration with Concur, Ariba, SuccessFactors")
    pdf.bold_bullet("Reporting", "SAP Analytics Cloud, Embedded Analytics, CDS Views, Fiori apps")
    pdf.bold_bullet("Migration", "SAP LSMW, BODS, Syniti, custom ABAP data migration programs")

    pdf.section_heading("Project Contributions", level=3)
    pdf.bold_bullet("Top-5 US Integrated Energy Company",
        "Led SAP S/4HANA Finance configuration for corporate and refinery operations covering 14 "
        "company codes, 8 currencies, and complex intercompany elimination scenarios. Configured "
        "New Asset Accounting for $18B in fixed assets and designed integration with Azure-based "
        "ESG data platform for emissions cost allocation. (See Energy Case Study)")
    pdf.bold_bullet("Mid-Market Specialty Retailer",
        "Configured SAP FI/CO for 340-store retailer during ECC-to-S/4HANA conversion. Designed "
        "profitability analysis (CO-PA) configuration enabling real-time margin reporting by store, "
        "channel, and product category. Migrated 8 years of financial history with zero reconciliation "
        "differences.")
    pdf.bold_bullet("Aerospace Manufacturer",
        "Configured SAP Treasury and Cash Management for $2.4B revenue defense contractor. Implemented "
        "automated bank statement processing, cash pooling, and multi-currency hedge accounting "
        "compliant with ASC 815 requirements.")

    pdf.section_heading("Training Completed", level=3)
    pdf.bullet("SAP S/4HANA Finance Deep Dive (SAP Official, 2024)")
    pdf.bullet("Meridian SAP Academy - Advanced Track (2023)")
    pdf.bullet("Meridian Consulting Excellence Program (2024)")

    # --- Jessica Huang ---
    pdf.add_page()
    pdf.section_heading("7. Jessica Huang")
    pdf.section_heading("Consultant, Data Engineering", level=2)
    pdf.key_value("Years of Experience", "3 years")
    pdf.key_value("Office", "San Francisco, CA")
    pdf.key_value("Email", "j.huang@meridian-llp.com")
    pdf.ln(2)

    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Jessica Huang is a Consultant in Meridian's Data & Analytics practice, specializing in "
        "data pipeline development, cloud data platform implementation, and data quality engineering. "
        "In her 3 years at the firm, Jessica has contributed to 6 client engagements across energy, "
        "retail, and financial services sectors. She is recognized for her expertise in modern data "
        "stack technologies (dbt, Snowflake, Databricks) and her ability to build production-grade "
        "data pipelines that reliably process terabytes of data with robust testing and monitoring."
    )

    pdf.section_heading("Education", level=3)
    pdf.bullet("MS, Computer Science (Data Systems track), University of Wisconsin-Madison (2023)")
    pdf.bullet("BS, Mathematics & Statistics, UC San Diego (2021)")

    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Microsoft Certified: Azure Data Engineer Associate (DP-203)")
    pdf.bullet("dbt Analytics Engineering Certification")
    pdf.bullet("Databricks Certified Data Engineer Associate")
    pdf.bullet("Snowflake SnowPro Core Certification")

    pdf.section_heading("Technical Skills", level=3)
    pdf.bold_bullet("Data Engineering", "dbt, Apache Spark, Apache Airflow, Dagster, Delta Lake, Apache Iceberg")
    pdf.bold_bullet("Cloud Platforms", "Azure (Data Factory, Synapse, ADLS Gen2, Event Hubs), AWS (Glue, Redshift, S3)")
    pdf.bold_bullet("Data Warehouses", "Snowflake, Databricks Unity Catalog, BigQuery")
    pdf.bold_bullet("Programming", "Python, SQL, Scala, Bash")
    pdf.bold_bullet("Data Quality", "Great Expectations, dbt tests, Monte Carlo, Soda")
    pdf.bold_bullet("Orchestration & CI/CD", "Airflow, Dagster, GitHub Actions, Terraform")

    pdf.section_heading("Project Contributions", level=3)
    pdf.bold_bullet("Integrated Energy Company - ESG Platform",
        "Built data pipelines ingesting real-time IoT sensor data from 2,400+ emissions monitoring "
        "points across 8 refineries into Azure Event Hubs and Delta Lake. Implemented dbt "
        "transformations for SEC Climate Rule-compliant emissions calculations with full data lineage "
        "and audit trail. (See Energy Case Study)")
    pdf.bold_bullet("National Retailer - Demand Forecasting Platform",
        "Developed Snowflake data pipelines processing daily POS transactions from 800+ stores "
        "(2.4M records/day). Built dbt models for demand signal aggregation supporting ML-powered "
        "forecasting models deployed by Raj Krishnamurthy's team. (See Retail Case Study)")
    pdf.bold_bullet("Financial Services - Regulatory Reporting",
        "Built automated data pipeline for CCAR stress testing on AWS, replacing 120 person-hours "
        "of manual data preparation with Airflow-orchestrated ETL processing in under 4 hours. "
        "Implemented Great Expectations data quality checks with 99.98% validation pass rate.")

    pdf.section_heading("Training Completed", level=3)
    pdf.bullet("Meridian Data Engineering Foundations Program (2023)")
    pdf.bullet("Advanced dbt Patterns - Internal Course (2024)")
    pdf.bullet("Meridian Professional Communications Workshop (2024)")
    pdf.bullet("Databricks Certified Data Engineer Professional - In Progress")

    # --- Derek Williams ---
    pdf.add_page()
    pdf.section_heading("8. Derek Williams")
    pdf.section_heading("Staff, Project Coordinator / PMO", level=2)
    pdf.key_value("Years of Experience", "2 years")
    pdf.key_value("Office", "New York, NY")
    pdf.key_value("Email", "d.williams@meridian-llp.com")
    pdf.ln(2)

    pdf.section_heading("Professional Summary", level=3)
    pdf.body_text(
        "Derek Williams is a Staff member in Meridian's Program Management Office (PMO), providing "
        "project coordination and administrative support for large-scale advisory and technology "
        "engagements. Despite being early in his career, Derek has already contributed to 4 major "
        "programs, demonstrating exceptional organizational skills, attention to detail, and the "
        "ability to manage complex project schedules, RAID logs, and stakeholder communications "
        "across multi-workstream programs with 50-120 person teams."
    )

    pdf.section_heading("Education", level=3)
    pdf.bullet("BS, Business Administration (Project Management concentration), Penn State University (2024)")
    pdf.bullet("Minor in Information Sciences and Technology")

    pdf.section_heading("Certifications", level=3)
    pdf.bullet("Certified Associate in Project Management (CAPM), PMI")
    pdf.bullet("Smartsheet Product Certified User")
    pdf.bullet("Smartsheet System Administrator Certification")
    pdf.bullet("Microsoft Project Certified Associate")
    pdf.bullet("SAFe 5 Practitioner - In Progress")

    pdf.section_heading("Technical Skills", level=3)
    pdf.bold_bullet("Project Management", "Schedule management, RAID log maintenance, resource tracking, meeting facilitation, status reporting")
    pdf.bold_bullet("Tools", "Smartsheet, Microsoft Project, Jira, Confluence, Monday.com, SharePoint")
    pdf.bold_bullet("Reporting", "Power BI dashboards, Excel (advanced), PowerPoint executive decks")
    pdf.bold_bullet("Methodologies", "PMI PMBOK, Agile (Scrum), SAFe (basic), Waterfall")
    pdf.bold_bullet("Communication", "Steering committee minutes, weekly status reports, stakeholder RACI matrices")

    pdf.section_heading("Project Contributions", level=3)
    pdf.bold_bullet("National Retailer - Omnichannel Transformation",
        "Served as PMO Coordinator for 20-month, 75-person program. Maintained integrated project "
        "schedule across 6 workstreams in Smartsheet, tracked 280+ deliverables, facilitated weekly "
        "status meetings, and produced executive steering committee decks. Program delivered on-time "
        "and within 4% of budget. (See Retail Case Study)")
    pdf.bold_bullet("Top-5 Energy Company - Digital Transformation",
        "Provided PMO support for 24-month, 110-person cloud migration program. Managed RAID log "
        "with 450+ items, coordinated resource onboarding/offboarding for 180 team members over "
        "program lifecycle, and designed resource utilization dashboard in Power BI. (See Energy "
        "Case Study)")
    pdf.bold_bullet("Fortune 500 Financial Services - Core Banking",
        "Supported PMO for 85-person core banking modernization. Managed defect tracking across "
        "3 parallel testing cycles, maintained change request log, and coordinated bi-weekly "
        "regulatory update meetings with OCC relationship management team.")

    pdf.section_heading("Training Completed", level=3)
    pdf.bullet("Meridian PMO Foundations Program (2024)")
    pdf.bullet("Smartsheet Advanced Administration - Internal Course (2024)")
    pdf.bullet("Meridian Professional Communications Workshop (2025)")
    pdf.bullet("PMP Exam Preparation - In Progress (targeting Q3 2026)")

    pdf.output(os.path.join(TALENT_DIR, "execution_bios_extended.pdf"))
    print("Generated execution_bios_extended.pdf")


# =========================================================================
# TASK 2: Expanded Rate Cards
# =========================================================================

def generate_rate_cards_expanded():
    pdf = MeridianPDF("Professional Services Rate Card",
                      "Standard Hourly Rates, Industry Rates & Sample Engagement Models",
                      confidential=True)
    pdf.cover_page(version="5.0", date="March 2026", doc_id="MA-RC-2026-001")

    # --- Section 1: Onshore rates with 4 industry columns ---
    pdf.add_page()
    pdf.section_heading("1. Standard Hourly Rates by Level and Industry")
    pdf.body_text(
        "The following table presents Meridian & Associates' standard hourly billing rates by professional "
        "level for the 2026 fiscal year across four key industry verticals. Rates are denominated in US "
        "Dollars (USD) and are applicable unless otherwise specified in a client-specific engagement "
        "letter or master services agreement."
    )

    pdf.section_heading("1.1 Onshore Rates (US-Based Professionals)", level=2)
    col_w = [38, 28, 28, 28, 28, 28, 12]
    headers = ["Level", "Standard", "Fin Svcs", "Public Sec", "Healthcare", "Mfg", "Blend"]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows = [
        ["Partner",           "$750-850", "$800-850", "$650-750", "$775-850", "$725-825", "$800"],
        ["Managing Dir",      "$600-700", "$650-700", "$550-625", "$625-700", "$600-675", "$650"],
        ["Senior Mgr",        "$450-525", "$475-525", "$400-475", "$460-525", "$440-510", "$490"],
        ["Manager",           "$350-425", "$375-425", "$325-385", "$360-425", "$345-410", "$390"],
        ["Senior Consultant", "$275-350", "$300-350", "$250-310", "$285-350", "$270-340", "$310"],
        ["Consultant",        "$200-275", "$225-275", "$175-240", "$210-275", "$200-265", "$240"],
        ["Analyst",           "$140-200", "$160-200", "$125-175", "$145-200", "$140-195", "$170"],
    ]
    for i, row in enumerate(rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 8)
            pdf.cell(col_w[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(6)
    pdf.section_heading("1.2 Offshore Rates (India-Based Professionals)", level=2)
    pdf.body_text(
        "Meridian's Global Delivery Center (GDC) in Hyderabad, India, staffed with 850+ professionals, "
        "provides 40-60% savings versus onshore equivalents."
    )
    col_w2 = [48, 38, 38, 38]
    headers2 = ["Level", "Offshore Rate", "Discount vs Onshore", "Blended"]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers2):
        pdf.cell(col_w2[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows2 = [
        ["Senior Manager",    "$220-280/hr", "48%-53%", "$250/hr"],
        ["Manager",           "$165-215/hr", "49%-53%", "$190/hr"],
        ["Senior Consultant", "$120-175/hr", "50%-57%", "$145/hr"],
        ["Consultant",        "$85-135/hr",  "51%-58%", "$110/hr"],
        ["Analyst",           "$60-95/hr",   "53%-57%", "$75/hr"],
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
        "Nearshore centers in Monterrey, Mexico and Bogota, Colombia provide time-zone-aligned support "
        "with 25-35% discount to onshore rates. Fully bilingual (English/Spanish)."
    )
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers2):
        pdf.cell(col_w2[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows3 = [
        ["Senior Manager",    "$310-380/hr", "26%-31%", "$345/hr"],
        ["Manager",           "$250-310/hr", "27%-29%", "$280/hr"],
        ["Senior Consultant", "$195-255/hr", "27%-29%", "$225/hr"],
        ["Consultant",        "$145-200/hr", "27%-28%", "$175/hr"],
        ["Analyst",           "$100-145/hr", "28%-29%", "$120/hr"],
    ]
    for i, row in enumerate(rows3):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w2[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    # --- Section 2: Specialist / Premium Tiers ---
    pdf.add_page()
    pdf.section_heading("2. Specialist & Premium Rate Tiers")
    pdf.body_text(
        "Certain engagement types require professionals with specialized clearances, certifications, "
        "or niche domain expertise. The following premium rate tiers apply in addition to standard rates:"
    )
    col_ws = [58, 38, 38, 56]
    hs = ["Specialist Category", "Premium Range", "Typical Level", "Applicable Engagements"]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(hs):
        pdf.cell(col_ws[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    spec_rows = [
        ["Cybersecurity Incident Response", "$425-650/hr", "Mgr - Partner", "Breach response, forensics, IR retainer"],
        ["CJIS-Cleared Personnel", "$375-550/hr", "Cons - Sr Mgr", "Law enforcement, criminal justice IT"],
        ["Clinical SMEs (MD/RN/PharmD)", "$400-600/hr", "Specialist", "EHR optimization, clinical workflows"],
        ["Data Scientists (PhD/ML Eng)", "$350-500/hr", "Cons - Mgr", "ML model dev, AI strategy, GenAI"],
        ["SAP S/4HANA Architects", "$425-575/hr", "Sr Mgr - MD", "Greenfield, conversion, Central Finance"],
        ["TS/SCI Cleared Consultants", "$400-600/hr", "Cons - Partner", "Defense, intelligence community"],
        ["Actuarial / Quant Specialists", "$375-525/hr", "Mgr - Partner", "Insurance, risk modeling, reserves"],
        ["Epic Certified (Bridges/Caboodle)", "$350-475/hr", "Cons - Sr Mgr", "Epic implementation, optimization"],
    ]
    for i, row in enumerate(spec_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 8)
            pdf.cell(col_ws[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.body_text(
        "Premium rates are applied only when specialist qualifications are contractually required. "
        "Specialist availability is subject to 2-4 week lead time; expedited staffing incurs a 10% "
        "surge premium for commitments under 2 weeks."
    )

    # --- Section 3: Volume Discounts ---
    pdf.ln(2)
    pdf.section_heading("3. Volume Discount Schedule")
    pdf.body_text(
        "Volume-based discounts are applied retroactively upon reaching each tier threshold within the "
        "fiscal year (January 1 - December 31) across all service lines."
    )
    col_w3 = [60, 40, 50]
    headers3 = ["Annual Spend Threshold", "Discount", "Effective Blended Savings"]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers3):
        pdf.cell(col_w3[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows4 = [
        ["$1,000,000 - $4,999,999",  "5%",  "~$50K - $250K savings"],
        ["$5,000,000 - $9,999,999",  "10%", "~$500K - $1M savings"],
        ["$10,000,000 - $24,999,999","15%", "~$1.5M - $3.75M savings"],
        ["$25,000,000+",             "18%", "~$4.5M+ savings"],
    ]
    for i, row in enumerate(rows4):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 9)
            pdf.cell(col_w3[j], 6.5, val, border=1, fill=fill, align="C")
        pdf.ln()

    # --- Section 4: Sample Engagement Cost Models ---
    pdf.add_page()
    pdf.section_heading("4. Sample Engagement Cost Models")
    pdf.body_text(
        "The following representative cost models illustrate typical team composition and total cost "
        "for common engagement types. Actual pricing is tailored based on scope, complexity, client "
        "requirements, and volume discount tier."
    )

    # Model 1: SAP S/4HANA
    pdf.section_heading("4.1 SAP S/4HANA Implementation (Mid-Market, 12 Months)", level=2)
    col_wm = [42, 16, 24, 26, 26, 26, 30]
    hm = ["Role", "FTEs", "Rate/hr", "Hours/FTE", "Onshore %", "Offshore %", "Annual Cost"]
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(hm):
        pdf.cell(col_wm[i], 6.5, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    m1_rows = [
        ["Lead Partner",           "0.2", "$800",  "400",   "100%", "0%",   "$320,000"],
        ["Program Manager (SM)",   "1",   "$490",  "1,920", "100%", "0%",   "$940,800"],
        ["Functional Leads (Mgr)", "3",   "$390",  "1,920", "100%", "0%",   "$2,246,400"],
        ["Sr Consultants",         "6",   "$310",  "1,920", "60%",  "40%",  "$2,591,040"],
        ["Consultants",            "8",   "$240",  "1,920", "40%",  "60%",  "$2,211,840"],
        ["Analysts (Offshore)",    "6",   "$75",   "1,920", "0%",   "100%", "$864,000"],
        ["OCM Lead (Mgr)",         "1",   "$390",  "1,920", "100%", "0%",   "$748,800"],
        ["Testing Lead (SC)",      "1",   "$310",  "1,920", "100%", "0%",   "$595,200"],
    ]
    for i, row in enumerate(m1_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 7.5)
            pdf.cell(col_wm[j], 6, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()
    # Total
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(col_wm[0] + col_wm[1] + col_wm[2] + col_wm[3] + col_wm[4] + col_wm[5], 7,
             "TOTAL (26.2 FTEs, ~50,300 hours)", border=1, fill=True, align="R")
    pdf.cell(col_wm[6], 7, "$10,518,080", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    pdf.ln(2)
    pdf.body_text("T&E estimate: $840K (8% of fees). Total all-in estimate: $11.36M.")

    # Model 2: Cloud Migration
    pdf.section_heading("4.2 Cloud Migration Assessment + Execution (500 Workloads, 6 Months)", level=2)
    m2_rows = [
        ["Lead Partner",           "0.15","$800",  "288",   "100%", "0%",   "$230,400"],
        ["Cloud Architect (SM)",   "1",   "$490",  "960",   "100%", "0%",   "$470,400"],
        ["Migration Leads (Mgr)", "2",    "$390",  "960",   "100%", "0%",   "$748,800"],
        ["Cloud Engineers (SC)",   "4",   "$310",  "960",   "50%",  "50%",  "$873,600"],
        ["DevOps Engineers",       "4",   "$240",  "960",   "30%",  "70%",  "$576,000"],
        ["Analysts (Offshore)",    "6",   "$75",   "960",   "0%",   "100%", "$432,000"],
        ["Security Lead (Mgr)",    "1",   "$425",  "960",   "100%", "0%",   "$408,000"],
    ]
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(hm):
        pdf.cell(col_wm[i], 6.5, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    for i, row in enumerate(m2_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 7.5)
            pdf.cell(col_wm[j], 6, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(sum(col_wm[:6]), 7, "TOTAL (18.15 FTEs, ~17,400 hours)", border=1, fill=True, align="R")
    pdf.cell(col_wm[6], 7, "$3,739,200", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    pdf.ln(2)
    pdf.body_text("T&E estimate: $280K (7.5%). Total all-in estimate: $4.02M.")

    # Model 3: Annual External Audit
    pdf.add_page()
    pdf.section_heading("4.3 Annual External Audit (Mid-Cap SEC Registrant)", level=2)
    col_wa = [48, 16, 26, 26, 26, 26, 22]
    ha = ["Role", "FTEs", "Rate/hr", "Hours/FTE", "Peak Hrs", "Off-Peak", "Total Cost"]
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(ha):
        pdf.cell(col_wa[i], 6.5, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    m3_rows = [
        ["Engagement Partner",      "0.1", "$825",  "200",  "160",  "40",   "$165,000"],
        ["Quality Review Partner",  "0.05","$825",  "80",   "60",   "20",   "$66,000"],
        ["Engagement Manager",      "1",   "$390",  "1,600","1,200","400",  "$624,000"],
        ["Senior Auditors",         "3",   "$310",  "1,600","1,200","400",  "$1,488,000"],
        ["Staff Auditors",          "4",   "$200",  "1,400","1,100","300",  "$1,120,000"],
        ["IT Audit / ITGC",         "1",   "$350",  "400",  "320",  "80",   "$140,000"],
        ["Tax Provision (ASC 740)", "0.5", "$390",  "300",  "240",  "60",   "$117,000"],
    ]
    for i, row in enumerate(m3_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 7.5)
            pdf.cell(col_wa[j], 6, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(sum(col_wa[:6]), 7, "TOTAL (9.65 FTEs, ~5,580 hours)", border=1, fill=True, align="R")
    pdf.cell(col_wa[6], 7, "$3,720,000", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    pdf.ln(2)
    pdf.body_text("Includes integrated audit (financial statements + ICFR per PCAOB AS 2201). "
                  "T&E estimate: $185K. Total all-in: $3.91M.")

    # Model 4: Cybersecurity Risk Assessment
    pdf.section_heading("4.4 Cybersecurity Risk Assessment (8 Weeks)", level=2)
    col_wc = [48, 16, 26, 26, 26, 26, 22]
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(ha):
        pdf.cell(col_wc[i], 6.5, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    m4_rows = [
        ["Engagement Partner",    "0.1", "$800",  "32",  "24",  "8",   "$25,600"],
        ["Cyber Lead (Sr Mgr)",   "1",   "$525",  "320", "280", "40",  "$168,000"],
        ["Security Architect",    "1",   "$425",  "320", "280", "40",  "$136,000"],
        ["Pen Test Lead",         "1",   "$500",  "240", "240", "0",   "$120,000"],
        ["GRC Analyst (Mgr)",     "1",   "$390",  "320", "280", "40",  "$124,800"],
        ["Security Analysts",     "2",   "$275",  "320", "280", "40",  "$176,000"],
    ]
    for i, row in enumerate(m4_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 7.5)
            pdf.cell(col_wc[j], 6, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(sum(col_wc[:6]), 7, "TOTAL (6.1 FTEs, ~1,552 hours)", border=1, fill=True, align="R")
    pdf.cell(col_wc[6], 7, "$750,400", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    pdf.ln(2)
    pdf.body_text("Includes NIST CSF assessment, vulnerability scanning, penetration testing, and "
                  "executive report. T&E: $45K. Total: $795K.")

    # Model 5: Post-Merger Integration
    pdf.check_space(60)
    pdf.section_heading("4.5 Post-Merger Integration Program (18 Months)", level=2)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(hm):
        pdf.cell(col_wm[i], 6.5, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    m5_rows = [
        ["Lead Partner",             "0.25","$825", "600",   "100%", "0%",   "$495,000"],
        ["Integration Director (MD)","1",   "$650", "2,880", "100%", "0%",   "$1,872,000"],
        ["Workstream Leads (SM)",    "4",   "$490", "2,880", "100%", "0%",   "$5,644,800"],
        ["Functional Leads (Mgr)",   "6",   "$390", "2,880", "80%",  "20%",  "$5,391,360"],
        ["Sr Consultants",           "10",  "$310", "2,880", "50%",  "50%",  "$5,558,400"],
        ["Consultants",              "12",  "$240", "2,880", "30%",  "70%",  "$4,423,680"],
        ["Analysts (Offshore)",      "10",  "$75",  "2,880", "0%",   "100%", "$2,160,000"],
        ["OCM Team",                 "6",   "$350", "2,880", "80%",  "20%",  "$4,838,400"],
    ]
    for i, row in enumerate(m5_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 7.5)
            pdf.cell(col_wm[j], 6, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(sum(col_wm[:6]), 7, "TOTAL (49.25 FTEs, ~142,000 hours)", border=1, fill=True, align="R")
    pdf.cell(col_wm[6], 7, "$30,383,640", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    pdf.ln(2)
    pdf.body_text("T&E: $2.4M (8%). Total all-in: $32.78M. Includes IT integration, operational "
                  "synergy capture, org design, and Day 1 readiness.")

    # --- Section 5: Fixed-Fee Deliverables ---
    pdf.add_page()
    pdf.section_heading("5. Fixed-Fee Estimates for Common Deliverables")
    pdf.body_text(
        "The following table provides indicative fixed-fee ranges for frequently requested standalone "
        "deliverables. Fees assume standard scope; complex or expedited engagements may be quoted higher."
    )
    col_wf = [62, 28, 28, 28, 44]
    hf = ["Deliverable", "Low Est.", "Mid Est.", "High Est.", "Typical Duration"]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(hf):
        pdf.cell(col_wf[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    ff_rows = [
        ["SOC 2 Type II Readiness",       "$180K",  "$275K",  "$400K",  "10-14 weeks"],
        ["SOC 2 Type II Examination",      "$120K",  "$200K",  "$325K",  "8-12 weeks"],
        ["Tax Provision Review (ASC 740)", "$85K",   "$150K",  "$250K",  "4-6 weeks"],
        ["Transfer Pricing Study",         "$150K",  "$275K",  "$500K",  "8-16 weeks"],
        ["R&D Tax Credit Study",           "$75K",   "$125K",  "$225K",  "6-10 weeks"],
        ["SALT Nexus Study (50-state)",    "$60K",   "$110K",  "$175K",  "4-8 weeks"],
        ["Cybersecurity Maturity Assess",  "$125K",  "$225K",  "$375K",  "6-8 weeks"],
        ["CMMC Level 2 Readiness",         "$175K",  "$300K",  "$450K",  "10-16 weeks"],
        ["HITRUST CSF Certification",      "$200K",  "$350K",  "$550K",  "12-20 weeks"],
        ["Internal Audit Co-source (ann)", "$250K",  "$500K",  "$900K",  "12 months"],
        ["IT Due Diligence (M&A)",         "$150K",  "$275K",  "$450K",  "4-6 weeks"],
        ["Financial Due Diligence (M&A)",  "$200K",  "$400K",  "$750K",  "4-8 weeks"],
        ["Vendor Selection / RFP Mgmt",    "$75K",   "$150K",  "$250K",  "6-10 weeks"],
        ["Data Governance Assessment",     "$100K",  "$175K",  "$300K",  "6-8 weeks"],
    ]
    for i, row in enumerate(ff_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 8)
            pdf.cell(col_wf[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    # --- Section 6: Policies ---
    pdf.ln(4)
    pdf.section_heading("6. Rate Escalation & Payment Terms")
    pdf.bullet("Annual escalation cap: 3.0% for MSA clients; non-MSA communicated 90 days in advance")
    pdf.bullet("No mid-engagement rate increases for fixed-scope SOWs")
    pdf.bullet("Rate lock available for 24-month commitments exceeding $5M annual spend")
    pdf.bullet("Invoicing: semi-monthly (T&M) or milestone-based (fixed fee)")
    pdf.bullet("Payment due: Net 30 days from invoice date")
    pdf.bullet("Late payment: 1.5% monthly interest on overdue balances (waived first occurrence)")
    pdf.bullet("Retainer deposits: 10% of estimated fees, credited against final invoice")

    pdf.ln(4)
    pdf.section_heading("7. Alternative Fee Arrangements")
    pdf.bold_bullet("Fixed Fee", "Predetermined total cost for agreed scope. 10% contingency buffer included.")
    pdf.bold_bullet("Capped Fee", "T&M with ceiling at 110-120% of estimate. Budget certainty with flexibility.")
    pdf.bold_bullet("Risk/Reward", "Base fee at 70-80% of standard with success bonus on measurable outcomes.")
    pdf.bold_bullet("Retainer", "Monthly fixed fee for ongoing advisory. 10% discount vs. hourly equivalent.")
    pdf.bold_bullet("Managed Services", "Fixed monthly fee per transaction/user/entity with SLA guarantees.")

    pdf.ln(4)
    pdf.section_heading("8. Travel & Expense Policy")
    pdf.bullet("T&E billed at actual cost, no markup. Total T&E capped at 12% of fees unless pre-approved.")
    pdf.bullet("Airfare: Coach <5hrs, premium economy 5-8hrs, business >8hrs. 14-day advance booking.")
    pdf.bullet("Lodging: Actual cost not exceeding GSA per diem. Extended stay rates for 30+ day engagements.")
    pdf.bullet("Ground: Actual cost; mileage at IRS rate ($0.67/mile for 2026).")
    pdf.bullet("Meals: Actual cost up to $75/day/person. Client entertainment >$150/person requires pre-approval.")
    pdf.bullet("Remote engagements: T&E reduced to 3-5% with on-site limited to key milestones.")

    pdf.output(os.path.join(TALENT_DIR, "rate_cards.pdf"))
    print("Generated rate_cards.pdf (expanded)")


# =========================================================================
# TASK 3a: Case Study - Energy
# =========================================================================

def generate_case_study_energy():
    pdf = MeridianPDF(
        "Case Study: Enterprise Cloud\n& Digital Transformation",
        "Major Integrated Energy Company",
        client_confidential=True
    )
    pdf.cover_page(version="1.0", date="February 2026", doc_id="MA-CS-ENERGY-001")

    pdf.add_page()
    pdf.section_heading("1. Engagement Overview")
    items = [
        ("Client:", "Top-5 US integrated energy company (name withheld per confidentiality agreement)"),
        ("Industry:", "Energy & Utilities - Integrated Oil & Gas"),
        ("Revenue:", "$45B+ annual revenue, operations across upstream, midstream, and downstream"),
        ("Engagement Type:", "Enterprise Cloud Migration, Digital Transformation & ESG Platform"),
        ("Duration:", "24 months (January 2024 - December 2025)"),
        ("Team Size:", "110 professionals at peak staffing"),
        ("Total Fees:", "$32.6 million"),
        ("Lead Partner:", "Patricia Hoffman, CPA, Six Sigma Black Belt"),
        ("Meridian Offices:", "Houston (lead), San Francisco, Hyderabad (GDC)"),
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
        "The client, a top-5 US integrated energy company with $45 billion in annual revenue, 8 refineries, "
        "12,000 miles of pipeline infrastructure, and 28,000 employees, faced mounting pressure to modernize "
        "its technology estate while meeting increasingly stringent environmental regulatory requirements. "
        "Despite significant capital investments in operational technology (OT) over decades, the company's "
        "IT and OT environments had evolved independently, creating a fragmented landscape that hindered "
        "operational efficiency, data-driven decision-making, and regulatory compliance."
    )
    pdf.bold_bullet("Aging IT Infrastructure",
        "The corporate IT environment comprised 1,200+ applications running across 6 on-premises data centers, "
        "with an average application age of 12 years. Annual IT operating costs exceeded $180M and were growing "
        "at 9% annually, driven by hardware refresh cycles, legacy licensing models, and specialized "
        "mainframe support costs.")
    pdf.bold_bullet("OT/IT Convergence Gap",
        "Operational technology systems (SCADA, DCS, PLCs) across refineries and pipeline infrastructure "
        "operated in isolation from corporate IT. Field workers relied on paper-based processes and manual "
        "data entry, with an average 48-hour latency between field data capture and corporate system "
        "availability. This gap was identified as a root cause of 23% of unplanned downtime incidents.")
    pdf.bold_bullet("Regulatory Pressure",
        "The EPA, PHMSA, and state regulators were increasing scrutiny of emissions monitoring and pipeline "
        "integrity reporting. The company's existing emissions tracking relied on quarterly manual calculations "
        "with an estimated 15-20% measurement uncertainty. Pending SEC Climate Disclosure Rules required "
        "auditable Scope 1 and Scope 2 emissions data, which the legacy systems could not produce.")
    pdf.bold_bullet("Field Worker Safety",
        "The company recorded 2.4 TRIR (Total Recordable Incident Rate) against an industry target of 1.5. "
        "Analysis showed that 35% of safety incidents were linked to inadequate real-time situational awareness "
        "and delayed communication between field and control room teams.")
    pdf.bold_bullet("Refinery Optimization",
        "Refinery utilization averaged 87% against a theoretical optimum of 94%. The absence of real-time "
        "process optimization analytics resulted in an estimated $120M annually in lost yield and excess "
        "energy consumption.")

    pdf.section_heading("3. Meridian's Solution")
    pdf.body_text(
        "Meridian designed and executed a comprehensive digital transformation program organized into four "
        "integrated workstreams, each with dedicated leadership, measurable milestones, and clear "
        "interdependencies:"
    )
    pdf.section_heading("3.1 Enterprise Cloud Migration (Corporate IT)", level=2)
    pdf.body_text(
        "Meridian led the migration of 1,200 corporate IT applications to Microsoft Azure, using a structured "
        "6R assessment methodology (Rehost, Replatform, Refactor, Repurchase, Retain, Retire). Of the 1,200 "
        "applications, 340 were retired, 520 were rehosted or replatformed, 180 were refactored to cloud-native "
        "architectures, and 160 were repurchased as SaaS. The migration was executed in 6 waves over 18 months "
        "with zero unplanned production outages. Azure Landing Zones were designed with industry-specific "
        "compliance guardrails for NERC CIP and SOX controls."
    )
    pdf.section_heading("3.2 Edge Computing & IoT for Field Operations", level=2)
    pdf.body_text(
        "To bridge the OT/IT gap, Meridian deployed Azure IoT Hub and Azure IoT Edge across 8 refineries "
        "and 42 field compressor stations. Over 2,400 IoT sensors were integrated for real-time monitoring "
        "of emissions, vibration, temperature, pressure, and flow rates. Edge computing devices at each "
        "site enabled sub-second local processing for safety-critical alerts while streaming aggregated "
        "data to the cloud for analytics. Field workers were equipped with ruggedized tablets running "
        "custom Power Apps for digital work permits, safety checklists, and real-time communication "
        "with control rooms."
    )

    pdf.add_page()
    pdf.section_heading("3.3 Digital Twin for Refinery Optimization", level=2)
    pdf.body_text(
        "Meridian implemented Azure Digital Twins across all 8 refineries, creating high-fidelity virtual "
        "replicas of each refinery's process units (CDU, FCC, hydrocracker, reformer). The digital twin "
        "platform integrated real-time process data from DCS systems, lab quality data, and market pricing "
        "feeds to enable continuous optimization of yield, energy consumption, and throughput. Machine "
        "learning models trained on 5 years of historical operating data predicted equipment failures "
        "28 days in advance with 92% accuracy, enabling transition from reactive to predictive maintenance."
    )
    pdf.section_heading("3.4 ESG Data Platform for Emissions Tracking", level=2)
    pdf.body_text(
        "Meridian built a purpose-built ESG data platform on Azure to provide real-time, auditable Scope 1 "
        "and Scope 2 emissions monitoring across all operations. The platform ingested data from 2,400+ IoT "
        "sensors, CEMS (Continuous Emissions Monitoring Systems), fuel purchase records, and electricity "
        "meters. Data pipelines built on Azure Event Hubs and Delta Lake processed over 8 million data "
        "points daily. Emissions calculations followed EPA 40 CFR Part 98 methodologies with full data "
        "lineage and audit trail, meeting SEC Climate Disclosure Rule requirements. The platform also "
        "integrated with the company's SAP S/4HANA instance (configured by Kwame Asante) for emissions "
        "cost allocation to business units."
    )

    pdf.section_heading("4. Delivery Approach & Team Composition")
    pdf.body_text("The 24-month program was structured into three phases:")
    pdf.bold_bullet("Phase 1 - Assessment & Foundation (Months 1-6)",
        "Application portfolio assessment, Azure Landing Zone design, IoT architecture, digital twin pilot "
        "(1 refinery), ESG data platform requirements and architecture")
    pdf.bold_bullet("Phase 2 - Core Execution (Months 7-18)",
        "Cloud migration waves 1-4, IoT deployment across all sites, digital twin rollout to 8 refineries, "
        "ESG platform MVP launch with Scope 1 monitoring")
    pdf.bold_bullet("Phase 3 - Optimization & Scale (Months 19-24)",
        "Cloud migration waves 5-6, advanced analytics and ML models, Scope 2 integration, SEC reporting "
        "readiness, knowledge transfer and steady-state transition")
    pdf.ln(2)
    pdf.body_text("Team composition at peak staffing (110 professionals):")
    pdf.bullet("2 Partners, 5 Senior Managers, 10 Managers, 28 Senior Consultants, 35 Consultants, 30 Analysts")
    pdf.bullet("Onshore (Houston/San Francisco): 55 professionals; Offshore (Hyderabad GDC): 55 professionals")
    pdf.bullet("Dedicated OT/safety specialists: 6 professionals with upstream/downstream operating experience")
    pdf.bullet("Embedded data engineering team of 8 (led by Raj Krishnamurthy, with Jessica Huang)")
    pdf.bullet("PMO coordination by Derek Williams; SAP FICO integration led by Kwame Asante")

    pdf.section_heading("5. Technology Stack")
    pdf.bold_bullet("Cloud Platform", "Microsoft Azure (Azure Government for regulated workloads)")
    pdf.bold_bullet("IoT & Edge", "Azure IoT Hub, Azure IoT Edge, Azure Sphere")
    pdf.bold_bullet("Digital Twins", "Azure Digital Twins, Azure Time Series Insights")
    pdf.bold_bullet("Data Platform", "Azure Event Hubs, Delta Lake, Databricks, Azure Synapse Analytics")
    pdf.bold_bullet("ESG / Emissions", "Custom platform on Azure (dbt, Delta Lake, Power BI)")
    pdf.bold_bullet("ERP Integration", "SAP S/4HANA (FI/CO integration for emissions cost allocation)")
    pdf.bold_bullet("Field Apps", "Microsoft Power Platform (Power Apps, Power Automate)")
    pdf.bold_bullet("Security", "Azure Sentinel, Defender for IoT, IEC 62443-compliant OT segmentation")
    pdf.bold_bullet("DevOps", "Azure DevOps, Terraform, GitHub Enterprise")

    pdf.add_page()
    pdf.section_heading("6. Results & Impact")
    pdf.ln(2)
    col_w = [60, 42, 42, 46]
    headers = ["Metric", "Baseline (Pre)", "Result (Post)", "Improvement"]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows = [
        ["Annual IT Operating Cost",     "$180M",         "$126M",          "30% reduction ($54M)"],
        ["System Uptime",                "99.85%",        "99.97%",         "Near-zero downtime"],
        ["Emissions Monitoring",         "Quarterly/manual","Real-time",    "Continuous across 8 sites"],
        ["Measurement Uncertainty",      "15-20%",        "<3%",            "SEC-audit ready"],
        ["Refinery Utilization",         "87%",           "92.4%",          "+5.4 ppts ($68M/yr)"],
        ["Unplanned Downtime",           "Baseline",      "-15%",           "Predictive maintenance"],
        ["TRIR (Safety Rate)",           "2.4",           "1.6",            "33% improvement"],
        ["Field Data Latency",           "48 hours",      "<1 minute",      "Real-time"],
        ["Application Portfolio",        "1,200 apps",    "860 apps",       "340 retired (28%)"],
    ]
    for i, row in enumerate(rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 8)
            pdf.cell(col_w[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.section_heading("7. Client Testimonial")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6,
        '"Meridian brought a unique combination of energy industry expertise and cutting-edge technology '
        'capabilities that we simply could not find elsewhere. They understood our operational realities '
        '-- from refinery floor to boardroom -- and designed solutions that our engineers and executives '
        'alike embraced. The ESG platform alone has transformed how we think about emissions management, '
        'moving us from a compliance burden to a genuine competitive advantage. The digital twins are '
        'delivering returns we did not expect to see for years."')
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, "-- Chief Information Officer, Client Energy Company")

    pdf.output(os.path.join(TALENT_DIR, "case_study_energy.pdf"))
    print("Generated case_study_energy.pdf")


# =========================================================================
# TASK 3b: Case Study - Retail
# =========================================================================

def generate_case_study_retail():
    pdf = MeridianPDF(
        "Case Study: Omnichannel Supply\nChain & Customer Experience",
        "National Retail Chain",
        client_confidential=True
    )
    pdf.cover_page(version="1.0", date="January 2026", doc_id="MA-CS-RETAIL-001")

    pdf.add_page()
    pdf.section_heading("1. Engagement Overview")
    items = [
        ("Client:", "Top-20 US specialty retailer (name withheld per confidentiality agreement)"),
        ("Industry:", "Retail & Consumer - Specialty Retail"),
        ("Revenue:", "$12B annual revenue, 800+ stores across 48 states"),
        ("Engagement Type:", "Omnichannel Supply Chain & Customer Experience Transformation"),
        ("Duration:", "20 months (March 2024 - October 2025)"),
        ("Team Size:", "75 professionals at peak staffing"),
        ("Total Fees:", "$22.4 million"),
        ("Lead Partner:", "Robert Adeyemi, MBA"),
        ("Meridian Offices:", "New York (lead), Chicago, San Francisco, Hyderabad (GDC)"),
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
        "The client, a top-20 US specialty retailer with $12 billion in annual revenue, 800+ stores, "
        "and a growing e-commerce business, was struggling to deliver a seamless customer experience "
        "across its physical and digital channels. Years of siloed technology investments had created "
        "a fragmented commerce ecosystem that was eroding customer loyalty, limiting growth, and "
        "driving up operational costs."
    )
    pdf.bold_bullet("Inventory Visibility Crisis",
        "Store-level inventory accuracy was only 60%, compared to the industry benchmark of 90%+. "
        "This resulted in $340M in annual lost sales due to out-of-stock items (10% of potential revenue), "
        "$85M in excess inventory across the network, and a 12% order cancellation rate for BOPIS (Buy "
        "Online, Pick Up In Store) orders due to phantom inventory.")
    pdf.bold_bullet("Siloed Commerce Channels",
        "E-commerce and in-store systems operated on separate platforms with no shared customer profile. "
        "The legacy e-commerce platform (custom-built in 2016) could not support modern experiences like "
        "endless aisle, unified cart, or real-time personalization. Customers who shopped both online and "
        "in-store (38% of customer base) spent 2.4x more than single-channel customers, but the company "
        "had no mechanism to identify or nurture these high-value shoppers.")
    pdf.bold_bullet("3PL Dependency and Cost",
        "Fulfillment was heavily dependent on two third-party logistics providers, with no ship-from-store "
        "capability. E-commerce fulfillment costs averaged $11.20 per order compared to $3.40 for in-store "
        "pickup. The 3PL model also created a 4-5 day average delivery time, well below the 2-day "
        "expectation set by major competitors.")
    pdf.bold_bullet("Declining Foot Traffic",
        "Store traffic had declined 18% over three years. The company's loyalty program, launched in 2018, "
        "had stagnated at 4.2M members with a 22% active rate (industry benchmark: 45%). The program "
        "lacked digital engagement capabilities and offered no differentiated benefits for omnichannel behavior.")
    pdf.bold_bullet("Demand Forecasting Gaps",
        "The existing demand planning system (legacy JDA) relied on 8-week-old historical patterns with no "
        "integration of external signals (weather, social media trends, local events). Forecast accuracy was "
        "62% at the store-SKU level, driving $85M in excess inventory and frequent markdowns that eroded "
        "gross margin by an estimated 180 basis points annually.")

    pdf.section_heading("3. Meridian's Solution")
    pdf.body_text(
        "Meridian designed and executed a six-workstream transformation program to create a truly unified "
        "commerce experience, modernize supply chain operations, and build the data foundation for "
        "AI-powered decision-making:"
    )
    pdf.section_heading("3.1 Unified Commerce Platform", level=2)
    pdf.body_text(
        "Meridian implemented Salesforce Commerce Cloud as the unified digital commerce platform, replacing "
        "the legacy custom-built e-commerce system. The implementation included a headless architecture "
        "enabling shared commerce APIs across web, mobile app, and in-store clienteling applications. "
        "A unified customer profile was established by integrating Salesforce CDP with the existing POS "
        "system, enabling real-time personalization and cross-channel recognition of the 38% of customers "
        "who shop both channels."
    )

    pdf.add_page()
    pdf.section_heading("3.2 Real-Time Inventory Visibility", level=2)
    pdf.body_text(
        "Meridian deployed Manhattan Active Warehouse Management and Manhattan Active Inventory across "
        "all 800+ stores and 4 distribution centers. RFID tagging was implemented for all SKUs (45,000 "
        "active SKUs) with weekly cycle counts replacing the previous quarterly physical inventories. "
        "The system provided a single, real-time view of inventory across all locations, enabling accurate "
        "available-to-promise (ATP) for e-commerce orders and eliminating the phantom inventory problem "
        "that had plagued BOPIS execution."
    )
    pdf.section_heading("3.3 BOPIS & Ship-From-Store Enablement", level=2)
    pdf.body_text(
        "With real-time inventory visibility as the foundation, Meridian enabled Buy Online Pick Up In Store "
        "(BOPIS), curbside pickup, and ship-from-store capabilities across all locations. Store associate "
        "workflows were redesigned with dedicated picking zones, priority queuing for online orders, and "
        "custom handheld applications built on the Salesforce platform. The ship-from-store program "
        "effectively converted 800+ stores into micro-fulfillment centers, reducing average delivery "
        "time from 4.8 days to 1.9 days and fulfillment cost from $11.20 to $5.60 per order."
    )
    pdf.section_heading("3.4 AI-Powered Demand Forecasting", level=2)
    pdf.body_text(
        "Meridian's data engineering team (led by Raj Krishnamurthy, with Jessica Huang building the "
        "data pipelines) architected a Snowflake + Databricks data platform to power AI-driven demand "
        "forecasting. The platform ingested POS data from 800+ stores (2.4M records/day), e-commerce "
        "clickstream, weather data, social media trend signals, and local event calendars. Eight "
        "production ML models were deployed for demand sensing at the store-SKU-day level, achieving "
        "85% forecast accuracy (up from 62%), enabling automated replenishment and reducing excess "
        "inventory by $85M across the network."
    )
    pdf.section_heading("3.5 Loyalty Program Redesign", level=2)
    pdf.body_text(
        "Meridian redesigned the loyalty program from a simple points-based model to a tiered, "
        "omnichannel engagement platform. The new program (built on Salesforce Loyalty Management) "
        "rewarded cross-channel behavior, offered personalized promotions powered by the CDP, and "
        "included experiential benefits (early access to new collections, styling consultations). "
        "A mobile-first design with digital wallet integration and QR-based in-store identification "
        "eliminated the friction of the previous card-based system."
    )
    pdf.section_heading("3.6 Sales Tax Compliance Remediation", level=2)
    pdf.body_text(
        "Given the expanded fulfillment footprint (ship-from-store created new nexus in 42 states), "
        "Sophia Vasquez's SALT team implemented Vertex O Series for automated sales tax calculation "
        "and compliance, with real-time nexus monitoring integrated into the Manhattan Active platform. "
        "This proactively addressed $14M in compliance risk exposure."
    )

    pdf.section_heading("4. Delivery Approach & Team Composition")
    pdf.body_text("The 20-month program was organized into three phases:")
    pdf.bold_bullet("Phase 1 - Foundation (Months 1-6)",
        "Platform selection, architecture design, RFID pilot (50 stores), data platform buildout, "
        "loyalty program design")
    pdf.bold_bullet("Phase 2 - Core Rollout (Months 7-14)",
        "Commerce Cloud launch, RFID rollout to all stores, Manhattan Active deployment, demand "
        "forecasting MVP, BOPIS enablement (first 200 stores)")
    pdf.bold_bullet("Phase 3 - Scale & Optimize (Months 15-20)",
        "Ship-from-store rollout, loyalty program launch, advanced ML models, optimization and "
        "knowledge transfer")
    pdf.ln(2)
    pdf.body_text("Team composition at peak staffing (75 professionals):")
    pdf.bullet("2 Partners, 4 Senior Managers, 8 Managers, 18 Senior Consultants, 25 Consultants, 18 Analysts")
    pdf.bullet("Onshore: 42 professionals; Offshore (Hyderabad GDC): 33 professionals")
    pdf.bullet("Dedicated data & analytics team of 12 (Raj Krishnamurthy, Jessica Huang)")
    pdf.bullet("OCM team of 8 (Lauren Mitchell) supporting 12,000 store associates through transition")
    pdf.bullet("PMO coordination by Derek Williams; SALT compliance by Sophia Vasquez")

    pdf.add_page()
    pdf.section_heading("5. Technology Stack")
    pdf.bold_bullet("Commerce", "Salesforce Commerce Cloud (B2C), Salesforce CDP, Salesforce Loyalty Management")
    pdf.bold_bullet("Supply Chain", "Manhattan Active Warehouse Management, Manhattan Active Inventory")
    pdf.bold_bullet("Demand Planning", "Snowflake, Databricks, custom ML models (Python/Spark)")
    pdf.bold_bullet("RFID", "Zebra Technologies RFID readers, Avery Dennison smart labels")
    pdf.bold_bullet("Cloud", "Google Cloud Platform (BigQuery, Vertex AI, Cloud Functions)")
    pdf.bold_bullet("Integration", "MuleSoft Anypoint Platform (API-led connectivity)")
    pdf.bold_bullet("POS Integration", "Custom middleware connecting legacy POS to Salesforce and Manhattan")
    pdf.bold_bullet("Tax Compliance", "Vertex O Series with automated nexus monitoring")
    pdf.bold_bullet("Analytics", "Looker (operational dashboards), Tableau (executive reporting)")
    pdf.bold_bullet("Mobile", "Salesforce Mobile SDK (associate app), React Native (customer app)")

    pdf.section_heading("6. Results & Impact")
    pdf.ln(2)
    col_w = [60, 42, 42, 46]
    headers = ["Metric", "Baseline (Pre)", "Result (Post)", "Improvement"]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    rows = [
        ["Inventory Accuracy",       "60%",          "94%",           "+34 ppts"],
        ["E-Commerce Revenue",       "Baseline",     "+28% YoY",      "$540M incremental"],
        ["Average Order Value",      "Baseline",     "+15%",          "Cross-sell / upsell"],
        ["Excess Inventory",         "$85M",         "Reduced",       "$85M freed capital"],
        ["Forecast Accuracy",        "62%",          "85%",           "+23 ppts (store-SKU)"],
        ["BOPIS Cancel Rate",        "12%",          "2.1%",          "83% reduction"],
        ["Avg Delivery Time",        "4.8 days",     "1.9 days",      "60% faster"],
        ["Fulfillment Cost/Order",   "$11.20",       "$5.60",         "50% reduction"],
        ["Loyalty Active Members",   "4.2M (22%)",   "7.8M (48%)",    "86% member growth"],
        ["Store Traffic",            "-18% trend",   "+6% YoY",       "Trend reversal"],
    ]
    for i, row in enumerate(rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 8)
            pdf.cell(col_w[j], 6.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.section_heading("7. Client Testimonial")
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6,
        '"Meridian transformed how we think about retail. They did not just implement technology -- they '
        'reimagined our entire customer journey from discovery to delivery. The inventory visibility alone '
        'was worth the investment, but the AI-powered demand forecasting and ship-from-store capabilities '
        'have fundamentally changed our cost structure and competitive position. Our store associates love '
        'the new tools, our customers are shopping more frequently, and our investors are seeing the results '
        'in our margin expansion. Robert and his team earned our trust from day one."')
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, "-- Chief Executive Officer, Client Retail Company")

    pdf.output(os.path.join(TALENT_DIR, "case_study_retail.pdf"))
    print("Generated case_study_retail.pdf")


# =========================================================================
# TASK 4: Firm Capabilities Overview
# =========================================================================

def generate_firm_capabilities():
    pdf = MeridianPDF("Firm Capabilities & Overview",
                      "Quick Reference for RFP Response Teams",
                      confidential=True)
    pdf.cover_page(version="1.0", date="March 2026", doc_id="MA-CAP-OVR-001")

    # Page 1: About & Capability Matrix
    pdf.add_page()
    pdf.section_heading("1. About Meridian & Associates LLP")
    pdf.body_text(
        "Founded in 1987, Meridian & Associates LLP is a global professional services firm with $14.2 "
        "billion in annual revenue, 68,000+ professionals across 43 countries, and a 38-year track "
        "record of delivering integrated advisory, assurance, tax, and technology services. The firm "
        "serves approximately 4,200 clients, including 187 Fortune 500 companies."
    )
    pdf.key_value("Global Revenue (FY2025)", "$14.2 billion (8.3% YoY growth)")
    pdf.key_value("Professionals", "68,000+ across 43 countries")
    pdf.key_value("Client Retention", "94% over past 5 years; avg top-100 client tenure: 8.7 years")
    pdf.key_value("Offices", "127 offices across 43 countries; 11 global delivery centers")
    pdf.key_value("Certifications", "ISO 27001, SOC 2 Type II, ISO 22301 across all operations")

    pdf.ln(2)
    pdf.section_heading("2. Capabilities x Industry Matrix")
    pdf.body_text(
        "The following matrix maps Meridian's core service capabilities to the industries where we "
        "maintain deep, specialized expertise (indicated by 'X'):"
    )
    col_cm = [52, 18, 18, 18, 18, 18, 18, 18, 18]
    hcm = ["Capability", "Fin Svcs", "Health", "Tech", "Energy", "Mfg", "Retail", "Gov", "Other"]
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(hcm):
        pdf.cell(col_cm[i], 6.5, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    cap_rows = [
        ["Cloud & Digital Transform",  "X","X","X","X","X","X","X","X"],
        ["ERP / SAP S/4HANA",          "X","X"," ","X","X","X"," "," "],
        ["Cybersecurity & GRC",         "X","X","X","X","X"," ","X"," "],
        ["Data & AI / ML",             "X","X","X","X","X","X","X"," "],
        ["M&A Advisory / PMI",         "X","X","X","X","X","X"," "," "],
        ["Audit & Assurance",          "X","X","X","X","X","X","X"," "],
        ["Tax (Federal & SALT)",       "X","X","X","X","X","X"," "," "],
        ["Transfer Pricing",          "X"," ","X","X","X","X"," "," "],
        ["Supply Chain / Ops",         " "," "," ","X","X","X"," "," "],
        ["Change Management",         "X","X","X","X","X","X","X"," "],
        ["Revenue Cycle (Healthcare)", " ","X"," "," "," "," "," "," "],
        ["Regulatory Compliance",      "X","X"," ","X"," "," ","X"," "],
    ]
    for i, row in enumerate(cap_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 7.5)
            pdf.cell(col_cm[j], 5.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    # Page 2: Practice Areas + Alliances
    pdf.add_page()
    pdf.section_heading("3. Practice Areas at a Glance")
    col_pa = [46, 26, 22, 22, 74]
    hpa = ["Practice Area", "Revenue", "Partners", "Staff", "Key Services"]
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(hpa):
        pdf.cell(col_pa[i], 6.5, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    pa_rows = [
        ["Advisory Services",      "$5.4B","320","16,200","Strategy, M&A, OpEx, org design, OCM"],
        ["Technology & Digital",   "$4.8B","280","14,800","Cloud, ERP, data/AI, cyber, managed svcs"],
        ["Risk & Compliance",      "$2.6B","185","9,400", "Internal audit, reg compliance, forensics"],
        ["Tax & Legal",            "$1.4B","125","5,600", "Intl tax, transfer pricing, SALT, legal"],
        ["Financial Services",     "$3.4B","190","10,200","Banking, insurance, capital markets"],
        ["Healthcare & Life Sci",  "$2.6B","145","8,500", "Payers, providers, pharma, medtech"],
        ["Energy & Utilities",     "$2.0B","110","6,800", "Oil & gas, utilities, renewables"],
        ["Retail & Consumer",      "$1.8B","95", "5,400", "Retail, CPG, QSR, e-commerce"],
        ["Manufacturing",          "$1.6B","85", "4,900", "Discrete, process, A&D, distribution"],
        ["Public Sector",          "$1.4B","80", "4,600", "Federal, state & local, education"],
    ]
    for i, row in enumerate(pa_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 7.5)
            pdf.cell(col_pa[j], 5.5, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.section_heading("4. Technology Alliance Partnerships")
    col_ta = [48, 38, 48, 56]
    hta = ["Partner", "Tier Status", "Certifications", "Key Practices"]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(hta):
        pdf.cell(col_ta[i], 6.5, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    ta_rows = [
        ["Microsoft",     "Azure Expert MSP",     "9,200+ certified",    "Cloud, Dynamics, Power Platform"],
        ["AWS",           "Premier Partner",       "4,800+ certified",    "Migration, data, security"],
        ["SAP",           "Platinum Partner",      "3,200+ certified",    "S/4HANA, BTP, analytics"],
        ["Salesforce",    "Summit Partner",        "2,100+ certified",    "Commerce, Service, MuleSoft"],
        ["ServiceNow",    "Elite Partner",         "1,800+ certified",    "ITSM, GRC, HRSD, CSM"],
        ["Google Cloud",  "Premier Partner",       "2,400+ certified",    "Data, AI/ML, infrastructure"],
        ["Epic",          "Gold Stars Partner",    "180+ certified",      "EHR implementation, Caboodle"],
        ["Oracle",        "Platinum Partner",       "2,600+ certified",    "Cloud ERP, HCM, CX, database"],
        ["Databricks",    "Elite Partner",         "850+ certified",      "Lakehouse, ML, governance"],
    ]
    for i, row in enumerate(ta_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 8)
            pdf.cell(col_ta[j], 6, val, border=1, fill=fill, align="C" if j > 0 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.section_heading("5. Technology Investments & Proprietary Platforms", level=2)
    pdf.body_text(
        "Meridian owns 23 proprietary platforms and accelerators that differentiate our delivery and "
        "accelerate client outcomes. Key investments include:"
    )
    pdf.bullet("MeridianAI -- Enterprise AI orchestration layer powering intelligent document analysis, "
               "knowledge retrieval, and engagement automation across all service lines.")
    pdf.bullet("Prism Analytics -- Data governance and analytics suite used on 80% of advisory engagements.")
    pdf.bullet("Data Analytics Center of Excellence -- 450+ dedicated data scientists and ML engineers "
               "driving innovation in predictive analytics, NLP, and computer vision.")
    pdf.bullet("Annual technology R&D investment: $340M (2.4% of revenue), with 1,200+ technology "
               "professionals in the Global Technology & Innovation group.")

    # Page 3: Awards + GDN + DEI/ESG
    pdf.add_page()
    pdf.section_heading("6. Awards & Industry Recognition")
    pdf.bullet("Ranked #1 in Management Consulting by Vault Professional Services Rankings (2024, 2025)")
    pdf.bullet("Leader, Gartner Magic Quadrant for IT Transformation Services (2025)")
    pdf.bullet("Leader, Gartner Magic Quadrant for Cloud Infrastructure and Platform Services (2025)")
    pdf.bullet("Leader, Forrester Wave: Digital Transformation Services (2025)")
    pdf.bullet("Leader, Forrester Wave: Cybersecurity Consulting Services (2024)")
    pdf.bullet("Leader, IDC MarketScape: SAP Implementation Services (2025)")
    pdf.bullet("Named to Forbes 'World's Best Employers' for 7 consecutive years")
    pdf.bullet("ISO 27001, SOC 2 Type II, ISO 22301 certified across all global operations")
    pdf.bullet("UN Global Compact LEAD designation for sustainability commitments")
    pdf.bullet("Supply Chain Management Review 'Pros to Know' (James O'Sullivan, 2023-2025)")

    pdf.ln(2)
    pdf.section_heading("7. Global Delivery Model")
    pdf.body_text(
        "Meridian operates 11 Global Delivery Centers (GDCs) across 6 countries, providing 24/7 "
        "follow-the-sun coverage with blended rate savings of 30-40% versus onshore-only models. "
        "The GDN supports all service lines including technology, analytics, tax compliance, and "
        "audit support. For detailed delivery center information, see the Global Delivery Network "
        "document (MA-GDN-001)."
    )
    pdf.bullet("India: Hyderabad (850+), Bangalore (620+), Chennai (380+)")
    pdf.bullet("Latin America: Monterrey, Mexico (420+); Bogota, Colombia (280+)")
    pdf.bullet("Europe: Warsaw, Poland (340+); Bucharest, Romania (260+)")
    pdf.bullet("Asia-Pacific: Manila, Philippines (310+); Shanghai, China (280+)")
    pdf.bullet("Additional centers: Dublin, Ireland (220+); Sydney, Australia (180+); Casablanca, Morocco (150+)")

    pdf.ln(2)
    pdf.section_heading("8. Diversity, Equity & Inclusion")
    pdf.body_text(
        "Meridian is committed to fostering an inclusive workplace. Key metrics (FY2025): 44% of new "
        "Partner promotions were women or underrepresented minorities; 52% of global workforce identifies "
        "as female; $28M invested in DEI programs including scholarships, ERGs, and supplier diversity. "
        "For full details, see the DEI Policy document (MA-DEI-001)."
    )

    pdf.ln(2)
    pdf.section_heading("9. ESG & Sustainability")
    pdf.body_text(
        "Meridian achieved carbon neutrality for Scope 1 and 2 emissions in FY2024 and is on track for "
        "Scope 3 net-zero by 2035. The firm has committed to science-based targets validated by SBTi, "
        "reduced business travel emissions by 34% through virtual delivery, and invested $45M in community "
        "impact programs. For full details, see the ESG Report (MA-ESG-001)."
    )

    pdf.output(os.path.join(COMMON_DIR, "firm_capabilities_overview.pdf"))
    print("Generated firm_capabilities_overview.pdf")


# =========================================================================
# TASK 5: Quality Assurance & Delivery Methodology
# =========================================================================

def generate_qa_methodology():
    pdf = MeridianPDF("Quality Assurance &\nDelivery Methodology",
                      "Engagement Quality Framework",
                      confidential=True)
    pdf.cover_page(version="2.0", date="March 2026", doc_id="MA-QA-METH-001")

    # Page 1
    pdf.add_page()
    pdf.section_heading("1. Quality Assurance Framework Overview")
    pdf.body_text(
        "Meridian & Associates maintains a comprehensive Quality Assurance (QA) framework that governs "
        "all client engagements across advisory, assurance, tax, and technology service lines. The "
        "framework is designed to ensure consistent delivery excellence, mitigate engagement risk, "
        "protect client and firm interests, and drive continuous improvement. This framework is "
        "mandatory for all engagements and is enforced by the firm's Office of Quality & Risk "
        "Management (OQRM), which reports directly to the Managing Partner."
    )
    pdf.body_text(
        "The QA framework comprises six integrated components: (1) Peer Review Process, (2) Deliverable "
        "Quality Gates, (3) Risk & Issue Management, (4) Independent Quality Reviews, (5) Client "
        "Satisfaction Measurement, and (6) Continuous Improvement Program. Each component is described "
        "in detail in the sections that follow."
    )

    pdf.section_heading("2. Peer Review Process")
    pdf.section_heading("2.1 Engagement-Level Peer Review", level=2)
    pdf.body_text(
        "Every client engagement is subject to a multi-level peer review process designed to ensure "
        "technical accuracy, methodological rigor, and alignment with professional standards:"
    )
    pdf.bold_bullet("Engagement Quality Control Reviewer (EQCR)",
        "A Partner or Managing Director not involved in the engagement is assigned as EQCR at the "
        "outset of every engagement exceeding $500K in fees or classified as high-risk. The EQCR "
        "reviews the engagement plan, key deliverables, and final reports before client issuance. "
        "For audit engagements, the EQCR role is mandated by PCAOB standards (AS 1220).")
    pdf.bold_bullet("Technical Review",
        "All deliverables undergo technical review by a qualified professional at least one level "
        "above the preparer. For tax opinions and audit reports, a second technical review by a "
        "subject matter specialist is required for complex matters (e.g., ASC 740 provisions "
        "exceeding $10M, transfer pricing studies for >$500M in intercompany transactions).")
    pdf.bold_bullet("Manager Self-Review",
        "Engagement managers complete a self-review checklist covering 42 quality control points "
        "before submitting deliverables for partner review. The checklist covers accuracy, "
        "completeness, formatting, cross-references, and compliance with engagement letter scope.")

    pdf.section_heading("2.2 Firm-Level Quality Reviews", level=2)
    pdf.body_text(
        "The Office of Quality & Risk Management conducts three types of firm-level reviews annually:"
    )
    pdf.bold_bullet("Practice Inspection Program",
        "Annual inspection of a statistically representative sample of completed engagements across "
        "each service line (minimum 5% of engagements per practice). Inspectors are drawn from the "
        "OQRM team and rotating senior Partners. Findings are reported to the Management Committee "
        "and drive remedial training and process improvements.")
    pdf.bold_bullet("Thematic Reviews",
        "Targeted reviews of specific risk areas identified through industry trends, regulatory "
        "changes, or internal incident analysis. Recent themes include AI/ML model governance, "
        "SEC Climate Disclosure readiness, and Pillar Two tax compliance.")
    pdf.bold_bullet("Cross-Service Line Reviews",
        "For multi-service engagements (e.g., audit + tax + advisory), a cross-service review "
        "ensures consistency of findings, appropriate independence safeguards, and seamless "
        "client experience across workstreams.")

    # Page 2
    pdf.add_page()
    pdf.section_heading("3. Deliverable Quality Gates")
    pdf.body_text(
        "All client-facing deliverables progress through a four-stage quality gate process. "
        "Advancement to each subsequent stage requires formal sign-off from the designated reviewer:"
    )
    col_qg = [28, 40, 60, 62]
    hqg = ["Gate", "Stage", "Reviewer", "Exit Criteria"]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(hqg):
        pdf.cell(col_qg[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    qg_rows = [
        ["Gate 1", "Draft", "Preparer + Peer",
         "Content complete, methodology applied, data validated"],
        ["Gate 2", "Internal Review", "Manager + SM/Partner",
         "Technical accuracy, consistency, formatting, risk flags"],
        ["Gate 3", "Client Review", "Client stakeholders",
         "Factual accuracy, alignment with expectations, feedback"],
        ["Gate 4", "Final", "EQCR (if applicable)",
         "All comments resolved, final formatting, archival copy"],
    ]
    for i, row in enumerate(qg_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j < 2 else "", 8)
            pdf.cell(col_qg[j], 6.5, val, border=1, fill=fill, align="C" if j < 2 else "L")
        pdf.ln()

    pdf.ln(4)
    pdf.body_text(
        "Average time through the gate process: 5-8 business days for standard deliverables, "
        "10-15 business days for complex reports. Expedited review is available for time-sensitive "
        "deliverables with Partner approval, with a minimum 48-hour turnaround."
    )

    pdf.section_heading("4. Risk & Issue Management")
    pdf.section_heading("4.1 RAID Log Management", level=2)
    pdf.body_text(
        "Every engagement maintains a RAID (Risks, Assumptions, Issues, Dependencies) log that is "
        "reviewed weekly by the engagement manager and bi-weekly by the engagement partner. The RAID "
        "log template is standardized across the firm and includes the following for each item: unique "
        "identifier, category, description, owner, probability (1-5), impact (1-5), risk score "
        "(P x I), mitigation strategy, target resolution date, and current status."
    )

    pdf.section_heading("4.2 Escalation Matrix", level=2)
    pdf.body_text("Issues are escalated based on the following thresholds:")
    col_esc = [40, 36, 56, 58]
    hesc = ["Severity", "Response Time", "Escalated To", "Examples"]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(hesc):
        pdf.cell(col_esc[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(40, 40, 40)
    esc_rows = [
        ["Critical (P1)", "2 hours", "Engagement Partner + OQRM",
         "Data breach, regulatory finding, safety"],
        ["High (P2)", "8 hours", "Engagement Partner",
         "Scope creep >10%, budget overrun, key staff loss"],
        ["Medium (P3)", "48 hours", "Engagement Manager",
         "Timeline slip <2wks, minor quality issue"],
        ["Low (P4)", "5 business days", "Workstream Lead",
         "Process clarification, resource substitution"],
    ]
    for i, row in enumerate(esc_rows):
        fill = i % 2 == 0
        pdf.set_fill_color(235, 240, 248)
        for j, val in enumerate(row):
            pdf.set_font("Helvetica", "B" if j == 0 else "", 8)
            pdf.cell(col_esc[j], 6.5, val, border=1, fill=fill, align="C" if j < 3 else "L")
        pdf.ln()

    # Page 3
    pdf.add_page()
    pdf.section_heading("5. Independent Quality Reviews (IQR)")
    pdf.body_text(
        "Independent Quality Reviews are mandated for all engagements classified as high-risk. An "
        "engagement is classified as high-risk if it meets any of the following criteria:"
    )
    pdf.bullet("Total fees exceed $5 million")
    pdf.bullet("Client is a SEC registrant (for audit engagements)")
    pdf.bullet("Engagement involves regulatory remediation or consent order compliance")
    pdf.bullet("Multi-service engagement with independence risk (audit + advisory)")
    pdf.bullet("First-year engagement with a new client exceeding $2 million in fees")
    pdf.bullet("Engagement in a sector with elevated regulatory scrutiny (banking, healthcare, defense)")

    pdf.ln(2)
    pdf.body_text(
        "IQRs are conducted at three points during the engagement lifecycle: (1) at engagement "
        "acceptance, (2) at the midpoint or key phase gate, and (3) prior to final deliverable "
        "issuance. The IQR team typically comprises a senior Partner from a different practice area, "
        "a subject matter specialist, and an OQRM representative. Findings are documented in a "
        "formal IQR Report and tracked to resolution."
    )

    pdf.section_heading("6. Client Satisfaction Measurement")
    pdf.body_text(
        "Meridian employs a multi-layered approach to measuring client satisfaction and using feedback "
        "to drive improvement:"
    )
    pdf.bold_bullet("Net Promoter Score (NPS)",
        "Surveyed semi-annually across all active client relationships. Firm-wide NPS: 72 (FY2025), "
        "top quartile among professional services firms. NPS results are reviewed by the Management "
        "Committee and form part of Partner compensation evaluation.")
    pdf.bold_bullet("Pulse Surveys",
        "Short (5-question) surveys deployed at key engagement milestones (kickoff + 30 days, "
        "midpoint, go-live, close-out). Response rate: 78%. Results reviewed weekly by engagement "
        "manager with corrective actions for any score below 4.0/5.0.")
    pdf.bold_bullet("Post-Engagement Reviews (PER)",
        "Formal in-person or virtual review conducted within 30 days of engagement close with "
        "client executive sponsor. Structured around five dimensions: quality of work, team "
        "caliber, communication, value delivered, and likelihood to re-engage. PER summaries "
        "are archived in the firm's CRM and inform future staffing and pursuit decisions.")
    pdf.bold_bullet("Client Advisory Boards",
        "Annual advisory board meetings with top-50 clients to gather strategic feedback on "
        "firm capabilities, emerging needs, and competitive positioning. Advisory board input "
        "directly influences the firm's annual strategic plan and investment priorities.")

    pdf.section_heading("7. Continuous Improvement Program")
    pdf.body_text(
        "Meridian's continuous improvement program ensures that lessons learned, quality findings, "
        "and client feedback are systematically captured and actioned:"
    )
    pdf.bold_bullet("Lessons Learned Repository",
        "All engagements exceeding $1M document lessons learned using a standardized template. "
        "The repository (hosted on the firm's knowledge management platform) contains 3,200+ "
        "entries searchable by industry, service line, technology, and engagement type.")
    pdf.bold_bullet("Quality Scorecard",
        "Each practice area maintains a quarterly quality scorecard tracking 12 KPIs including "
        "on-time delivery rate (target: 95%), budget variance (target: <5%), client NPS, "
        "EQCR finding rate, and employee satisfaction. Scorecards are reviewed by the Management "
        "Committee and drive resource allocation and investment decisions.")
    pdf.bold_bullet("Root Cause Analysis",
        "All P1 and P2 incidents trigger a formal Root Cause Analysis (RCA) using the 5-Why "
        "methodology. RCA findings and corrective actions are tracked in a centralized system "
        "with monthly reporting to the OQRM Director.")
    pdf.bold_bullet("Methodology Updates",
        "The firm's delivery methodologies (Meridian Accelerate, Meridian Audit Methodology, "
        "Meridian Tax Compliance Framework) are updated semi-annually based on quality review "
        "findings, regulatory changes, technology evolution, and client feedback. All methodology "
        "updates are communicated via mandatory e-learning modules with completion tracking.")
    pdf.bold_bullet("Training & Certification",
        "All professionals complete a minimum of 40 hours of continuing professional education "
        "(CPE) annually, including 8 hours of quality and ethics training. The firm invests "
        "$180M annually in learning and development programs, including partnerships with "
        "Harvard Business School, MIT, Stanford, and leading technology vendors.")

    pdf.output(os.path.join(ADVISORY_DIR, "quality_assurance_methodology.pdf"))
    print("Generated quality_assurance_methodology.pdf")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    generate_executive_bios_extended()
    generate_management_bios_extended()
    generate_execution_bios_extended()
    generate_rate_cards_expanded()
    generate_case_study_energy()
    generate_case_study_retail()
    generate_firm_capabilities()
    generate_qa_methodology()
    print("\nAll 8 documents generated successfully!")
