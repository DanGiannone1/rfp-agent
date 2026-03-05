#!/usr/bin/env python3
"""Generate 10 synthetic PDF documents for Meridian & Associates LLP knowledge base."""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base", "common_firm_wide")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FIRM = "Meridian & Associates LLP"
CONFIDENTIAL = "CONFIDENTIAL - For Internal Use and Authorized RFP Response Only"


class FirmPDF(FPDF):
    """Base PDF class with firm branding and helper methods."""

    def __init__(self, title: str, version: str = "3.1", effective: str = "January 2026"):
        super().__init__()
        self.doc_title = title
        self.version = version
        self.effective = effective
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() == 1:
            return  # Cover page has its own layout
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, f"{FIRM}  |  {self.doc_title}", align="L")
        self.ln(3)
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-20)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5, CONFIDENTIAL, align="C")
        self.ln(3)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")

    def cover_page(self):
        self.add_page()
        self.alias_nb_pages()
        # Top bar
        self.set_fill_color(0, 51, 102)
        self.rect(0, 0, 210, 45, "F")
        self.set_y(12)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, FIRM, align="C")
        self.ln(12)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 5, "Global Professional Services", align="C")
        # Title block
        self.set_y(65)
        self.set_text_color(0, 51, 102)
        self.set_font("Helvetica", "B", 24)
        self.multi_cell(0, 11, self.doc_title, align="C")
        # Metadata
        self.ln(15)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(80, 80, 80)
        lines = [
            f"Version {self.version}",
            f"Effective Date: {self.effective}",
            f"Classification: Confidential",
            "",
            "Prepared by the Office of Strategic Communications",
            FIRM,
        ]
        for line in lines:
            self.cell(0, 7, line, align="C")
            self.ln(7)
        # Confidential box
        self.ln(20)
        self.set_draw_color(180, 0, 0)
        self.set_line_width(0.4)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(180, 0, 0)
        x = 30
        self.rect(x, self.get_y(), 150, 18)
        self.set_xy(x, self.get_y() + 3)
        self.cell(150, 5, "CONFIDENTIAL", align="C")
        self.ln(5)
        self.set_font("Helvetica", "", 8)
        self.set_xy(x, self.get_y())
        self.cell(150, 5, "This document contains proprietary information. Do not distribute", align="C")
        self.ln(4)
        self.set_xy(x, self.get_y())
        self.cell(150, 5, "outside of authorized RFP response teams without written consent.", align="C")

    def section_heading(self, number, title):
        # Ensure at least 40mm of space for heading + some body text
        self.check_page_space(40)
        self.ln(6)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 8, f"{number}. {title}")
        self.ln(9)
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 120, self.get_y())
        self.ln(4)

    def sub_heading(self, number, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.cell(0, 7, f"{number} {title}")
        self.ln(8)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet_list(self, items):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        for item in items:
            x = self.get_x()
            self.cell(8, 5.5, "-")
            self.multi_cell(0, 5.5, item)
            self.set_x(x)
        self.ln(2)

    def toc_entry(self, number, title, indent=0):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        x_start = 10 + indent
        self.set_x(x_start)
        self.cell(12, 6, str(number))
        self.cell(0, 6, title)
        self.ln(6)

    def add_toc(self, entries):
        self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "Table of Contents")
        self.ln(12)
        self.set_draw_color(0, 51, 102)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(6)
        for num, title in entries:
            indent = 10 if "." in str(num) else 0
            self.toc_entry(num, title, indent)

    def check_page_space(self, needed_mm=45):
        """Add a page break only if less than needed_mm of space remains."""
        if self.get_y() > (297 - 25 - needed_mm):
            self.add_page()

    def save(self, filename):
        path = os.path.join(OUTPUT_DIR, filename)
        self.output(path)
        print(f"  Created: {filename}")


# ---------------------------------------------------------------------------
# Document 1: Executive Summary Boilerplate
# ---------------------------------------------------------------------------
def gen_executive_summary():
    pdf = FirmPDF("Executive Summary Boilerplate", "4.2", "January 2026")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "Firm Overview and Heritage"),
        ("2", "Mission, Vision, and Values"),
        ("3", "Service Lines"),
        ("4", "Key Differentiators"),
        ("5", "Financial Highlights"),
        ("6", "Client Portfolio"),
        ("7", "Leadership Team"),
        ("8", "Technology Alliances"),
        ("9", "Partnership Governance"),
        ("10", "Awards and Recognition"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "Firm Overview and Heritage")
    pdf.body_text(
        "Meridian & Associates LLP was founded in 1987 by former partners of a leading global consultancy "
        "who recognized the need for a more integrated, client-centric approach to professional services. "
        "What began as a boutique advisory firm in Chicago, Illinois, has grown into one of the world's "
        "preeminent professional services organizations, with a presence in over 40 countries and a workforce "
        "of more than 68,000 professionals. Over nearly four decades, Meridian has maintained an unwavering "
        "commitment to quality, integrity, and innovation -- values that continue to define our culture and "
        "guide our service delivery."
    )
    pdf.body_text(
        "From our founding engagement -- advising a Fortune 100 manufacturer on a $2.3 billion post-merger "
        "integration -- Meridian demonstrated an ability to combine strategic insight with operational rigor. "
        "This combination has been the hallmark of every engagement since. In 1994, the firm expanded into "
        "Europe with offices in London and Frankfurt. By 2002, Meridian had established a significant "
        "presence across the Asia-Pacific region, including major delivery centers in Bangalore, Shanghai, "
        "and Sydney. The 2010s saw the build-out of our digital and technology consulting practice, which "
        "today represents 34% of global revenue."
    )

    pdf.section_heading("2", "Mission, Vision, and Values")
    pdf.sub_heading("2.1", "Mission Statement")
    pdf.body_text(
        "To empower organizations to navigate complexity, seize opportunity, and achieve sustainable growth "
        "through world-class advisory, technology, and assurance services delivered with integrity and purpose."
    )
    pdf.sub_heading("2.2", "Vision")
    pdf.body_text(
        "To be the most trusted professional services partner for organizations shaping the future of "
        "industries and communities worldwide."
    )
    pdf.sub_heading("2.3", "Core Values")
    pdf.bullet_list([
        "Integrity Above All -- We uphold the highest ethical standards in every interaction.",
        "Client Centricity -- Our clients' success is the measure of our own.",
        "Innovation with Purpose -- We invest in emerging capabilities that create tangible value.",
        "Inclusive Excellence -- Diverse perspectives drive better outcomes.",
        "Stewardship -- We develop our people, protect our communities, and sustain our planet.",
    ])

    pdf.section_heading("3", "Service Lines")
    pdf.body_text(
        "Meridian operates through four integrated service lines, each supported by deep industry expertise "
        "and a global delivery network:"
    )
    pdf.bullet_list([
        "Advisory Services (38% of revenue) -- Strategy, M&A advisory, operational transformation, "
        "organizational design, and change management. Over 2,400 engagements completed in FY2025.",
        "Technology & Digital (34% of revenue) -- Cloud migration, enterprise platform implementation "
        "(SAP S/4HANA, Salesforce, ServiceNow, Workday), data and AI/ML, cybersecurity, and managed "
        "services. 9,200+ certified cloud architects across AWS, Azure, and GCP.",
        "Risk & Compliance (18% of revenue) -- Internal audit, regulatory compliance, financial crime "
        "prevention, third-party risk management, and forensic investigations. Serving 14 of the 20 "
        "largest global financial institutions.",
        "Tax & Legal (10% of revenue) -- International tax structuring, transfer pricing, indirect tax, "
        "trade and customs, and legal entity rationalization across 35 jurisdictions.",
    ])

    pdf.section_heading("4", "Key Differentiators")
    pdf.bullet_list([
        "Integrated Delivery Model -- Unlike firms that operate in silos, Meridian's service lines share a "
        "common methodology framework (Meridian Accelerate) and staffing model, enabling seamless "
        "cross-functional teams.",
        "Global Delivery Network -- Our 11 delivery centers across 6 countries provide 24/7 follow-the-sun "
        "coverage with blended rate savings of 30-40% versus onshore-only models.",
        "Industry Depth -- Over 60% of our professionals specialize in no more than two industries, ensuring "
        "genuine domain expertise rather than generalist advice.",
        "Proprietary Technology Assets -- Meridian owns 23 proprietary platforms and accelerators, including "
        "MeridianAI (our enterprise AI orchestration layer) and Prism Analytics (our data governance suite).",
        "Client Retention -- 94% client retention rate over the past five years; average tenure with top 100 "
        "clients exceeds 8.7 years.",
    ])

    pdf.section_heading("5", "Financial Highlights")
    pdf.body_text("Fiscal Year 2025 (ended June 30, 2025):")
    pdf.bullet_list([
        "Global Revenue: $14.2 billion (8.3% YoY growth)",
        "Revenue per Professional: $208,800",
        "Operating Margin: 22.4%",
        "Capital Investment in Technology and Innovation: $620 million",
        "Average Revenue per Partner: $4.9 million",
    ])
    pdf.body_text(
        "Meridian has achieved 14 consecutive years of revenue growth, including through the COVID-19 "
        "pandemic, when our rapid pivot to virtual delivery and digital transformation services allowed us "
        "to sustain momentum while supporting clients through unprecedented disruption."
    )

    pdf.section_heading("6", "Client Portfolio")
    pdf.body_text(
        "Meridian serves approximately 4,200 clients globally, including 187 Fortune 500 companies and "
        "62 of the Financial Times Europe 500. Our client base spans every major industry:"
    )
    pdf.bullet_list([
        "Financial Services -- 24% of revenue (banking, insurance, capital markets, fintech)",
        "Healthcare & Life Sciences -- 18% of revenue (payers, providers, pharma, medtech)",
        "Technology, Media & Telecommunications -- 16% of revenue",
        "Energy, Resources & Industrials -- 14% of revenue",
        "Consumer & Retail -- 12% of revenue",
        "Government & Public Sector -- 10% of revenue (civilian, defense, state & local)",
        "Other (education, non-profit, real estate) -- 6% of revenue",
    ])

    pdf.section_heading("7", "Leadership Team")
    pdf.body_text(
        "Meridian's leadership team combines deep industry expertise with proven operational and "
        "technology leadership:"
    )
    pdf.bullet_list([
        "Global Managing Partner: Jonathan R. Whitfield -- 28 years with the firm; former head of "
        "Advisory Services. Appointed 2021. Oversees firm strategy, partner governance, and client "
        "relationships. MBA, Harvard Business School; CPA.",
        "Chief Operating Officer (COO): Dr. Priya Mehta -- Joined 2016 from a Fortune 50 technology "
        "company. Responsible for global operations, delivery network, real estate, and shared services. "
        "PhD in Industrial Engineering, Georgia Tech.",
        "Chief Information Security Officer (CISO): Marcus T. Chen -- 22 years in cybersecurity; former "
        "CISO at a top-10 global bank. Leads the firm's 340-person security organization. CISSP, CISM, "
        "CRISC certified.",
        "Chief Data Officer (CDO): Dr. Amara Osei -- Leads the firm's data strategy, AI/ML governance, "
        "analytics platforms, and data privacy engineering. Former Chief Analytics Officer at a major "
        "healthcare system. PhD in Statistics, Stanford.",
        "Chief Technology Officer (CTO): Raj Krishnamurthy -- Oversees the firm's technology platform "
        "strategy, cloud infrastructure, and proprietary technology assets (MeridianAI, Prism Analytics). "
        "Former VP of Engineering at a hyperscale cloud provider. 18 years in enterprise technology.",
    ])

    pdf.section_heading("8", "Technology Alliances")
    pdf.body_text(
        "Meridian maintains strategic technology alliances with leading platform providers, ensuring our "
        "teams have access to the deepest technical enablement and co-innovation opportunities:"
    )
    pdf.bullet_list([
        "Microsoft -- Global Solutions Partner (highest tier). Azure Expert MSP. Over 5,200 Microsoft "
        "certifications across Azure, Dynamics 365, Power Platform, and Microsoft 365. Joint go-to-market "
        "programs in AI (Azure OpenAI Service) and security (Microsoft Sentinel, Defender).",
        "Amazon Web Services (AWS) -- Premier Consulting Partner. AWS Managed Service Provider. 2,800+ "
        "AWS certifications. Migration Competency, DevOps Competency, and Data Analytics Competency "
        "designations.",
        "SAP -- Global Strategic Services Partner. Over 1,400 SAP-certified consultants. S/4HANA, "
        "SuccessFactors, Ariba, and BTP capabilities. Recognized SAP Pinnacle Award winner (2024, 2025).",
        "Salesforce -- Summit (Platinum) Consulting Partner. 1,100+ Salesforce certifications. "
        "Multi-Cloud Practice (Sales, Service, Marketing, Commerce, MuleSoft, Tableau).",
        "ServiceNow -- Elite Partner. 800+ ServiceNow-certified professionals. IT Service Management, "
        "IT Operations Management, Security Operations, and HR Service Delivery certified.",
    ])

    pdf.section_heading("9", "Partnership Governance")
    pdf.body_text(
        "Meridian & Associates LLP is structured as a global limited liability partnership, governed by "
        "its partners and managed through a well-defined governance framework:"
    )
    pdf.bullet_list([
        "Equity partners: 2,890 as of January 2026, across all service lines, industries, and geographies.",
        "Board of Partners: 24-member elected board providing strategic oversight, fiduciary governance, "
        "and partner accountability. Elected for three-year terms with staggered rotation.",
        "Executive Committee: 12-member committee responsible for day-to-day firm management, chaired by "
        "the Global Managing Partner. Includes the COO, CFO, General Counsel, CHRO, CIO, and service "
        "line leaders.",
        "Partner admission: Annual cycle with rigorous evaluation including client impact, leadership "
        "contribution, business development, and adherence to firm values. FY2025: 186 new partners "
        "admitted (6.4% admission rate from eligible candidates).",
        "Partner compensation: Lockstep-modified system with performance differentiation. Transparent "
        "compensation principles published internally. 15% of variable compensation tied to DEI, ESG, "
        "and people development metrics.",
    ])

    pdf.section_heading("10", "Awards and Recognition")
    pdf.bullet_list([
        "Ranked #1 in Management Consulting by Vault Professional Services Rankings (2024, 2025)",
        "Leader in Gartner Magic Quadrant for IT Transformation Services (2025)",
        "Named to Forbes 'World's Best Employers' list for 7 consecutive years",
        "ISO 27001, SOC 2 Type II, and ISO 22301 certified across all global operations",
        "Received the UN Global Compact LEAD designation for sustainability commitments",
    ])

    pdf.save("executive_summary_boilerplate.pdf")


# ---------------------------------------------------------------------------
# Document 2: Global Footprint and Scale
# ---------------------------------------------------------------------------
def gen_global_footprint():
    pdf = FirmPDF("Global Footprint and Scale", "2.8", "February 2026")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "Global Presence Overview"),
        ("2", "Americas Region"),
        ("3", "Europe, Middle East & Africa (EMEA)"),
        ("4", "Asia-Pacific (APAC)"),
        ("5", "Revenue by Region"),
        ("6", "Headcount by Region"),
        ("7", "Recent Expansion and Emerging Markets"),
        ("8", "Language and Cultural Capabilities"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "Global Presence Overview")
    pdf.body_text(
        "Meridian & Associates LLP operates from 127 offices in 43 countries, supported by 11 global "
        "delivery centers and 3 innovation labs. Our geographic footprint enables us to serve multinational "
        "clients with local expertise and global consistency, while our delivery network provides scalable "
        "capacity and cost-effective resourcing options."
    )
    pdf.body_text(
        "The firm's international expansion has been deliberate and organic, supplemented by strategic "
        "acquisitions. Since 2018, Meridian has completed 14 acquisitions to strengthen capabilities in "
        "high-growth markets and emerging technology domains, including the 2023 acquisition of Helm Digital "
        "(a 900-person digital engineering firm based in Berlin) and the 2024 acquisition of Nuvance "
        "Analytics (a 450-person AI/ML consultancy headquartered in Toronto)."
    )

    pdf.section_heading("2", "Americas Region")
    pdf.body_text(
        "The Americas region is Meridian's largest, contributing 45% of global revenue ($6.39 billion in "
        "FY2025). The region comprises 38 offices across the United States, Canada, Mexico, Brazil, "
        "Argentina, Colombia, and Costa Rica, with approximately 28,500 professionals."
    )
    pdf.sub_heading("2.1", "Key Office Locations")
    pdf.bullet_list([
        "United States: Chicago (global HQ, 4,200 staff), New York (3,800), San Francisco (2,100), "
        "Washington D.C. (1,900), Dallas (1,400), Atlanta (1,200), Boston (950), Seattle (800), "
        "Miami (650), Denver (500), plus 12 additional locations",
        "Canada: Toronto (1,100), Montreal (450), Vancouver (350), Calgary (200)",
        "Latin America: Sao Paulo (850), Mexico City (600), Buenos Aires (350), Bogota (300)",
        "Nearshore Delivery Center: San Jose, Costa Rica (1,400 professionals)",
    ])

    pdf.section_heading("3", "Europe, Middle East & Africa (EMEA)")
    pdf.body_text(
        "EMEA accounts for 32% of global revenue ($4.54 billion in FY2025) with 52 offices across "
        "28 countries and approximately 21,800 professionals. The region has seen strong growth driven "
        "by regulatory compliance demand (GDPR, DORA, AI Act) and digital transformation."
    )
    pdf.sub_heading("3.1", "Key Office Locations")
    pdf.bullet_list([
        "United Kingdom: London (EMEA HQ, 3,200), Edinburgh (450), Birmingham (300), Manchester (250)",
        "Continental Europe: Frankfurt (1,100), Paris (950), Amsterdam (700), Zurich (550), Madrid (400), "
        "Milan (350), Stockholm (300), Dublin (250), Brussels (200), Vienna (180), Copenhagen (150)",
        "Middle East: Dubai (650), Riyadh (400), Abu Dhabi (200), Doha (150)",
        "Africa: Johannesburg (350), Nairobi (200), Lagos (150), Cairo (120)",
        "Nearshore Delivery Centers: Warsaw, Poland (1,800); Bucharest, Romania (1,200)",
    ])

    pdf.section_heading("4", "Asia-Pacific (APAC)")
    pdf.body_text(
        "APAC contributes 23% of global revenue ($3.27 billion in FY2025) and is the fastest-growing "
        "region with 14% YoY revenue growth. The region employs approximately 17,700 professionals across "
        "37 offices in 12 countries."
    )
    pdf.sub_heading("4.1", "Key Office Locations")
    pdf.bullet_list([
        "India: Mumbai (APAC advisory HQ, 1,200), Delhi NCR (800), Bangalore (offshore delivery, 3,400), "
        "Hyderabad (offshore delivery, 2,200), Chennai (offshore delivery, 1,800), Pune (600)",
        "Greater China: Shanghai (800), Beijing (550), Hong Kong (450), Shenzhen (200), Guangzhou (200)",
        "Japan: Tokyo (750), Osaka (200)",
        "Southeast Asia: Singapore (regional HQ, 650), Manila (offshore delivery, 1,600), "
        "Jakarta (350), Bangkok (250), Kuala Lumpur (200)",
        "Oceania: Sydney (800), Melbourne (500), Auckland (150)",
    ])

    pdf.section_heading("5", "Revenue by Region")
    pdf.body_text("Global Revenue Distribution -- FY2025 ($14.2 billion total):")
    pdf.bullet_list([
        "Americas: $6.39B (45%) -- 6.2% YoY growth",
        "EMEA: $4.54B (32%) -- 7.8% YoY growth",
        "APAC: $3.27B (23%) -- 14.1% YoY growth",
    ])

    pdf.section_heading("6", "Headcount by Region")
    pdf.body_text("Global Headcount -- As of December 31, 2025 (68,000+ total):")
    pdf.bullet_list([
        "Americas: 28,500 (42%) -- including 1,400 in Costa Rica nearshore center",
        "EMEA: 21,800 (32%) -- including 3,000 in Poland and Romania delivery centers",
        "APAC: 17,700 (26%) -- including 9,000 in India and Philippines offshore centers",
    ])

    pdf.section_heading("7", "Recent Expansion and Emerging Markets")
    pdf.body_text(
        "Meridian has made significant investments in emerging markets over the past three years, "
        "reflecting our commitment to serving clients where growth is accelerating:"
    )
    pdf.bullet_list([
        "Saudi Arabia (Vision 2030) -- Expanded Riyadh office from 120 to 400 professionals since 2023; "
        "secured advisory mandates with three Saudi giga-projects.",
        "Vietnam -- Opened Ho Chi Minh City office in Q3 2025 (initial team of 80) to support "
        "manufacturing clients diversifying supply chains from China.",
        "East Africa -- Established Nairobi hub in 2024 to serve the rapidly digitizing financial services "
        "sector across Kenya, Tanzania, Uganda, and Ethiopia.",
        "Poland -- Doubled Warsaw delivery center capacity to 1,800 professionals, adding specialized "
        "capabilities in cloud engineering and data science.",
    ])

    pdf.section_heading("8", "Language and Cultural Capabilities")
    pdf.body_text(
        "Our global workforce delivers services in 32 languages. The firm maintains a Cultural Fluency "
        "program that ensures engagement teams are equipped to work effectively across cultural contexts. "
        "Key language capabilities include English, Spanish, Portuguese, French, German, Mandarin, Japanese, "
        "Korean, Arabic, Hindi, Bahasa, Thai, Dutch, Italian, Swedish, Polish, Romanian, and Turkish."
    )

    pdf.save("global_footprint_and_scale.pdf")


# ---------------------------------------------------------------------------
# Document 3: DEI Policy
# ---------------------------------------------------------------------------
def gen_dei_policy():
    pdf = FirmPDF("Diversity, Equity & Inclusion Policy", "5.0", "January 2026")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "Policy Statement and Leadership Commitment"),
        ("2", "Representation Goals and Current Metrics"),
        ("3", "Talent Acquisition and Pipeline Programs"),
        ("4", "Employee Resource Groups (ERGs)"),
        ("5", "Pay Equity and Transparency"),
        ("6", "Supplier Diversity"),
        ("7", "Inclusive Client Service"),
        ("8", "Accountability and Governance"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "Policy Statement and Leadership Commitment")
    pdf.body_text(
        "Meridian & Associates LLP is committed to building and sustaining a workforce that reflects the "
        "diversity of the communities and clients we serve. We believe that inclusive teams produce superior "
        "outcomes, and that equity in opportunity is both a moral imperative and a business advantage. This "
        "policy applies to all 68,000+ professionals across every office, service line, and level."
    )
    pdf.body_text(
        "Our Global Managing Partner, the Executive Committee, and the Board of Partners have endorsed this "
        "policy and are personally accountable for its implementation. DEI metrics are embedded in leadership "
        "performance evaluations and directly influence partner compensation. In FY2025, 15% of partner "
        "variable compensation was tied to DEI outcomes."
    )

    pdf.section_heading("2", "Representation Goals and Current Metrics")
    pdf.sub_heading("2.1", "Gender Representation")
    pdf.bullet_list([
        "Women in total workforce: 46% (current) / 48% (2027 target)",
        "Women in management (Manager through Senior Manager): 42% (current) / 45% (2027 target)",
        "Women in senior leadership (Director and above): 34% (current) / 38% (2027 target)",
        "Women in partnership: 27% (current) / 32% (2028 target)",
    ])
    pdf.sub_heading("2.2", "Racial and Ethnic Representation (U.S. Operations)")
    pdf.bullet_list([
        "Underrepresented minorities in total U.S. workforce: 38% (current) / 40% (2027 target)",
        "Underrepresented minorities in senior roles (Director+): 28% (current, up from 21% in 2022) / "
        "32% (2026 target)",
        "Black/African American professionals in management+: 12% (current) / 15% (2027 target)",
        "Hispanic/Latino professionals in management+: 11% (current) / 14% (2027 target)",
    ])
    pdf.sub_heading("2.3", "Other Dimensions")
    pdf.bullet_list([
        "LGBTQ+ self-identification rate: 8.2% of workforce (voluntary disclosure)",
        "Professionals with disabilities: 4.1% self-identification rate",
        "Veterans: 3.8% of U.S. workforce",
    ])

    pdf.section_heading("3", "Talent Acquisition and Pipeline Programs")
    pdf.body_text(
        "Meridian invests over $28 million annually in DEI-related talent programs. Key initiatives include:"
    )
    pdf.bullet_list([
        "University Partnerships -- Recruiting relationships with 45 HBCUs, 22 Hispanic-Serving "
        "Institutions, and 15 tribal colleges. In FY2025, 32% of U.S. campus hires came from these "
        "partnerships.",
        "Meridian Scholars Program -- Full-ride scholarships and guaranteed internships for 200 "
        "underrepresented students annually in accounting, technology, and business disciplines.",
        "Return-to-Work Program -- Structured re-entry pathway for professionals who have taken career "
        "breaks of 2+ years. 340 participants since 2021, with 78% conversion to full-time roles.",
        "Diverse Slate Policy -- All roles at the Manager level and above require a diverse candidate "
        "slate (minimum two candidates from underrepresented groups) before an offer can be extended.",
        "Blind Resume Screening -- Implemented across all entry-level and campus hiring since 2023.",
    ])

    pdf.section_heading("4", "Employee Resource Groups (ERGs)")
    pdf.body_text(
        "Meridian supports 11 firm-sponsored ERGs, each with an executive sponsor from the Executive "
        "Committee and an annual operating budget. Total ERG investment: $4.2 million in FY2025."
    )
    pdf.bullet_list([
        "M-BOLD (Black Organization for Leadership and Development) -- 4,800 members",
        "Adelante (Hispanic/Latino professionals) -- 3,200 members",
        "APEX (Asian Pacific professionals) -- 3,600 members",
        "Pride@Meridian (LGBTQ+ and allies) -- 5,100 members",
        "Women@Meridian -- 12,400 members",
        "MeridianVets (military veterans and families) -- 1,900 members",
        "AccessAbility (professionals with disabilities) -- 1,400 members",
        "Indigenous Circle -- 600 members",
        "Working Parents Network -- 8,200 members",
        "Interfaith Alliance -- 2,100 members",
        "NextGen (early-career professionals) -- 9,800 members",
    ])

    pdf.section_heading("5", "Pay Equity and Transparency")
    pdf.body_text(
        "Meridian conducts comprehensive pay equity audits annually, performed by an independent third-party "
        "firm. The most recent audit (completed September 2025) found:"
    )
    pdf.bullet_list([
        "Gender pay gap (adjusted for role, level, tenure, and geography): 0.7% -- within the statistical "
        "noise threshold. Remediation adjustments applied where gaps exceeded 1%.",
        "Racial/ethnic pay gap (adjusted, U.S. operations): 0.9% -- remediation adjustments applied.",
        "The firm publishes a public Pay Equity Report annually, available on meridianllp.com.",
        "All compensation bands are disclosed internally by level and geography.",
    ])

    pdf.section_heading("6", "Supplier Diversity")
    pdf.body_text(
        "In FY2025, Meridian directed $180 million in procurement spend to certified diverse suppliers, "
        "representing 14.2% of addressable procurement. Categories of diverse suppliers include:"
    )
    pdf.bullet_list([
        "Minority-owned business enterprises (MBEs): $72M",
        "Women-owned business enterprises (WBEs): $54M",
        "Veteran-owned businesses (VOBs): $22M",
        "LGBTQ+-owned businesses: $14M",
        "Disability-owned businesses: $10M",
        "Small and disadvantaged businesses: $8M",
    ])
    pdf.body_text("The firm's target is to reach $220 million (17% of addressable spend) by FY2027.")

    pdf.section_heading("7", "Inclusive Client Service")
    pdf.body_text(
        "We are committed to ensuring our client-facing teams reflect the diversity of the populations our "
        "clients serve. Engagement staffing reviews include diversity composition as a mandatory criterion "
        "for all proposals and project plans. Our Inclusive Service Delivery training is mandatory for all "
        "professionals at the Senior Consultant level and above."
    )

    pdf.section_heading("8", "Accountability and Governance")
    pdf.bullet_list([
        "Global DEI Council -- Chaired by the Chief Diversity Officer, reports directly to the Global "
        "Managing Partner. Meets monthly.",
        "Regional DEI Leads -- Dedicated leaders in Americas, EMEA, and APAC with dotted-line reporting "
        "to the CDO.",
        "Annual DEI Scorecard -- Published internally with progress against all targets.",
        "External Reporting -- Meridian publishes its EEO-1 data (U.S.) and UK Gender Pay Gap Report "
        "annually.",
    ])

    pdf.save("dei_policy.pdf")


# ---------------------------------------------------------------------------
# Document 4: ESG Report
# ---------------------------------------------------------------------------
def gen_esg_report():
    pdf = FirmPDF("Environmental, Social & Governance Report", "4.0", "December 2025")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "Message from the Global Managing Partner"),
        ("2", "Climate Commitments and Net-Zero Pathway"),
        ("3", "Emissions Data (Scope 1, 2, and 3)"),
        ("3.1", "Year-over-Year Emissions Trend"),
        ("4", "Scope 3 Supplier Engagement"),
        ("5", "TCFD Climate Risk Scenario Analysis"),
        ("6", "Water Consumption and Waste Diversion"),
        ("7", "Energy and Office Operations"),
        ("8", "Third-Party Assurance"),
        ("9", "Human Rights and Modern Slavery Compliance"),
        ("10", "Employee Wellbeing, Health and Safety"),
        ("11", "Community Investment and Social Impact"),
        ("12", "Sustainable Procurement"),
        ("13", "CSRD, ISSB, and ESRS Readiness"),
        ("14", "Governance and Reporting Frameworks"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "Message from the Global Managing Partner")
    pdf.body_text(
        "Sustainability is not a peripheral initiative at Meridian -- it is central to how we operate, "
        "advise our clients, and invest in the future. In FY2025, we accelerated our commitments across "
        "every dimension of ESG, from reducing our operational carbon footprint to deepening our community "
        "investment. This report provides a transparent account of our progress, grounded in data and "
        "aligned to the frameworks our stakeholders expect."
    )
    pdf.body_text(
        "I am particularly proud that we achieved our interim 2025 emissions reduction target one year "
        "ahead of schedule, and that our community investment exceeded $45 million for the first time. "
        "As we look toward our net-zero by 2040 commitment, we recognize that the hardest work lies ahead "
        "-- particularly in addressing Scope 3 emissions across our value chain. We are committed to this "
        "journey with the same rigor we bring to our client engagements."
    )
    pdf.body_text(
        "This year we have also taken important steps to strengthen our reporting: our Scope 1, 2, and 3 "
        "emissions data has received limited assurance from Whitfield & Crane LLP for the first time, our TCFD "
        "disclosures now include quantitative scenario analysis, and we have begun formal readiness "
        "assessments for the EU Corporate Sustainability Reporting Directive (CSRD) and ISSB standards. "
        "I invite you to review this report as evidence of our commitment to accountability."
    )

    pdf.section_heading("2", "Climate Commitments and Net-Zero Pathway")
    pdf.body_text("Meridian's climate strategy is anchored in Science-Based Targets initiative (SBTi) "
                   "validated goals:")
    pdf.bullet_list([
        "Net-Zero by 2040 -- Full value chain (Scopes 1, 2, and 3), 10 years ahead of the Paris "
        "Agreement timeline.",
        "Interim Target (2030) -- 50% absolute reduction in Scope 1 and 2 emissions from a 2019 "
        "baseline; 30% reduction in Scope 3 emissions intensity per dollar of revenue.",
        "FY2025 Progress -- Scope 1 and 2 emissions reduced by 42% from 2019 baseline (on track for "
        "50% by 2030). Scope 3 intensity reduced by 19%.",
        "Carbon Removal -- Committed to investing $15 million in permanent carbon removal technologies "
        "(direct air capture, enhanced weathering) between 2025 and 2030.",
        "Internal Carbon Price -- $85/tCO2e shadow price applied to all capital investment decisions "
        "exceeding $1 million since January 2025.",
    ])

    pdf.section_heading("3", "Emissions Data (Scope 1, 2, and 3)")
    pdf.sub_heading("3.1", "Scope 1 -- Direct Emissions")
    pdf.body_text("Total Scope 1 emissions in FY2025: 8,400 tCO2e (down from 14,200 tCO2e in 2019).")
    pdf.bullet_list([
        "Natural gas for heating: 4,100 tCO2e",
        "Company-owned/leased vehicles: 2,800 tCO2e",
        "Diesel generators (backup power): 900 tCO2e",
        "Refrigerants: 600 tCO2e",
    ])
    pdf.sub_heading("3.2", "Scope 2 -- Purchased Energy (Market-Based)")
    pdf.body_text("Total Scope 2 emissions in FY2025: 18,600 tCO2e (down from 38,900 tCO2e in 2019).")
    pdf.bullet_list([
        "78% of global offices now run on certified renewable electricity (via PPAs, green tariffs, "
        "and unbundled RECs).",
        "100% renewable electricity achieved in all Americas and EMEA offices.",
        "APAC transitioning: 52% renewable, with full conversion targeted by 2028.",
    ])
    pdf.sub_heading("3.3", "Scope 3 -- Value Chain Emissions")
    pdf.body_text("Total Scope 3 emissions in FY2025: 312,000 tCO2e. Major categories:")
    pdf.bullet_list([
        "Business travel (Category 6): 148,000 tCO2e (47% of Scope 3) -- reduced 28% from 2019 via "
        "virtual-first engagement model and sustainable travel policy.",
        "Purchased goods and services (Category 1): 89,000 tCO2e (29%)",
        "Employee commuting (Category 7): 42,000 tCO2e (13%)",
        "Capital goods (Category 2): 18,000 tCO2e (6%)",
        "Other categories: 15,000 tCO2e (5%)",
    ])
    pdf.sub_heading("3.4", "Year-over-Year Emissions Trend (tCO2e)")
    pdf.body_text(
        "The following table summarizes emissions across all scopes from the 2019 baseline through FY2025, "
        "demonstrating consistent year-over-year reductions:"
    )
    pdf.bullet_list([
        "FY2019 (Baseline): Scope 1: 14,200 | Scope 2: 38,900 | Scope 3: 410,000 | Total: 463,100",
        "FY2020: Scope 1: 12,800 | Scope 2: 35,200 | Scope 3: 348,000 | Total: 396,000 (-14.5%)",
        "FY2021: Scope 1: 11,600 | Scope 2: 31,100 | Scope 3: 355,000 | Total: 397,700 (+0.4%)",
        "FY2022: Scope 1: 10,500 | Scope 2: 27,400 | Scope 3: 340,000 | Total: 377,900 (-5.0%)",
        "FY2023: Scope 1: 9,600 | Scope 2: 23,800 | Scope 3: 328,000 | Total: 361,400 (-4.4%)",
        "FY2024: Scope 1: 9,000 | Scope 2: 21,100 | Scope 3: 320,000 | Total: 350,100 (-3.1%)",
        "FY2025: Scope 1: 8,400 | Scope 2: 18,600 | Scope 3: 312,000 | Total: 339,000 (-3.2%)",
    ])
    pdf.body_text(
        "Cumulative reduction from baseline: Scope 1 and 2 combined down 49.1%; Scope 3 down 23.9%; "
        "total emissions down 26.8%. The firm is on track to meet or exceed all 2030 interim targets."
    )

    pdf.section_heading("4", "Scope 3 Supplier Engagement")
    pdf.body_text(
        "Addressing Scope 3 emissions -- which represent 92% of our total footprint -- requires deep "
        "engagement with our supply chain. Meridian's Supplier Climate Program sets aggressive targets "
        "for tier-1 supplier decarbonization:"
    )
    pdf.bullet_list([
        "80% of tier-1 suppliers by spend committed to SBTi-validated targets by 2028 (currently 62%).",
        "100% of tier-1 suppliers by spend required to disclose Scope 1 and 2 emissions annually by 2027 "
        "(currently 86%).",
        "50% of tier-1 suppliers by spend required to disclose material Scope 3 categories by 2029.",
        "Quarterly supplier scorecards track emissions intensity, renewable energy adoption, and SBTi "
        "commitment status.",
        "Supplier Climate Academy -- Free training program launched in 2024 to help SME suppliers develop "
        "carbon accounting capabilities; 340 suppliers enrolled to date.",
        "Contractual levers: New and renewed contracts above $500K include a climate commitment clause "
        "requiring SBTi commitment within 24 months or demonstration of equivalent decarbonization plan.",
        "Collaborative reduction pilots: Joint decarbonization initiatives with top 20 suppliers by spend, "
        "targeting 15% average emissions reduction in shared value chain activities by 2027.",
    ])

    pdf.section_heading("5", "TCFD Climate Risk Scenario Analysis")
    pdf.body_text(
        "In alignment with the Task Force on Climate-related Financial Disclosures (TCFD) recommendations, "
        "Meridian conducted its first quantitative climate risk scenario analysis in FY2025, examining "
        "both physical and transition risks under three scenarios drawn from the Network for Greening the "
        "Financial System (NGFS) framework."
    )
    pdf.sub_heading("5.1", "Physical Risks")
    pdf.body_text(
        "Physical risk assessment covered all 127 office locations and 11 delivery centers. "
        "Key findings under a high-warming scenario (NGFS Current Policies, ~3 degrees C by 2100):"
    )
    pdf.bullet_list([
        "Acute risks: 18 offices in high-exposure zones for flooding (coastal or riverine), including "
        "Mumbai, Manila, Houston, and Jakarta. Estimated incremental annual property damage and business "
        "interruption cost: $4.2-$6.8 million by 2040.",
        "Chronic risks: 22 offices exposed to extreme heat stress (>35 degrees C wet-bulb days >20/year "
        "by 2050), affecting outdoor commuting and data center cooling costs. Estimated incremental "
        "annual cooling costs: $1.8-$3.1 million by 2040.",
        "Adaptation measures: Flood resilience upgrades at high-risk locations (completed for Mumbai and "
        "Manila); geographic diversification of delivery centers; enhanced BCDR triggers for climate events.",
    ])
    pdf.sub_heading("5.2", "Transition Risks")
    pdf.body_text(
        "Transition risk assessment focused on regulatory, market, and reputational factors under an "
        "orderly transition scenario (NGFS Net Zero 2050):"
    )
    pdf.bullet_list([
        "Regulatory: Carbon pricing in key jurisdictions (EU CBAM, potential U.S. carbon fee) could "
        "increase travel and procurement costs by $8-$14 million annually by 2030.",
        "Market: Client demand shift toward low-carbon advisory services; estimated $200-$400 million "
        "revenue opportunity in climate transition advisory, sustainable finance, and ESG assurance by 2028.",
        "Reputational: Increasing client RFP requirements for verified emissions data; failure to meet "
        "stated targets could result in exclusion from procurement shortlists for 15-20% of pipeline.",
        "Technology: Transition to electric fleet and sustainable business travel estimated at $12 million "
        "capital investment through 2030, with $3 million annual operating savings from 2031.",
    ])

    pdf.section_heading("6", "Water Consumption and Waste Diversion")
    pdf.sub_heading("6.1", "Water Stewardship")
    pdf.body_text(
        "While Meridian's operations are not water-intensive, we recognize our responsibility to minimize "
        "consumption and manage water risk across our facility portfolio:"
    )
    pdf.bullet_list([
        "Total water consumption FY2025: 485,000 cubic meters across all global offices and data centers.",
        "Water intensity: 7.1 cubic meters per employee per year (down 12% from FY2022 baseline of "
        "8.1 cubic meters).",
        "Data center water usage effectiveness (WUE): 1.3 L/kWh (industry benchmark: 1.8 L/kWh). "
        "Achieved through free-air cooling in Chicago and London data centers.",
        "Water-stressed locations: 14 offices identified in high or extremely high water-stress areas "
        "(per WRI Aqueduct). These offices have implemented rainwater harvesting, greywater recycling, "
        "and low-flow fixtures, reducing consumption by 28% on average.",
        "Target: 20% reduction in water intensity per employee by 2028 from FY2022 baseline.",
    ])
    pdf.sub_heading("6.2", "Waste Diversion")
    pdf.body_text("Meridian is committed to zero waste to landfill across all major offices by 2030:")
    pdf.bullet_list([
        "Total waste generated FY2025: 2,840 metric tons (down from 4,100 metric tons in FY2019).",
        "Landfill diversion rate: 78% (target: 90% by 2028, 100% by 2030).",
        "E-waste: 100% of IT hardware processed through certified R2/e-Stewards recyclers. 14,200 "
        "devices responsibly recycled in FY2025.",
        "Construction waste: All office fit-outs require minimum 85% waste diversion per Meridian's "
        "Sustainable Fitout Standard.",
        "Single-use plastics: Eliminated from all offices and firm-sponsored events since 2023.",
        "Paper consumption: 42 metric tons in FY2025, down 71% from 2019 baseline through "
        "digital-first policies and default duplex printing.",
    ])

    pdf.section_heading("7", "Energy and Office Operations")
    pdf.bullet_list([
        "78% of offices certified renewable electricity; target 100% by 2028.",
        "LEED/BREEAM certified office space: 62% of global square footage.",
        "Smart building systems deployed in 34 major offices, reducing HVAC energy by 22%.",
        "Total energy consumption FY2025: 142,000 MWh (down 18% from FY2019 baseline of 173,000 MWh).",
        "Energy intensity: 2.09 MWh per employee (down from 2.50 MWh in FY2019).",
        "On-site solar installations at 8 offices generating 3,200 MWh annually.",
        "LED lighting retrofit: 94% of global office space converted; remaining 6% scheduled for FY2026.",
    ])

    pdf.section_heading("8", "Third-Party Assurance")
    pdf.body_text(
        "Meridian believes that credible ESG reporting requires independent verification. Beginning with "
        "FY2025 data, we have engaged Whitfield & Crane LLP (acting independently of any advisory relationship) "
        "to provide external assurance over our emissions disclosures:"
    )
    pdf.bullet_list([
        "Scope 1 and 2 emissions: Limited assurance engagement in accordance with ISAE 3410 "
        "(Assurance Engagements on Greenhouse Gas Statements). Opinion: Unqualified.",
        "Scope 3 emissions (Categories 1, 6, and 7, representing 90% of Scope 3): Limited assurance "
        "in accordance with ISAE 3000 (Revised). Opinion: Unqualified.",
        "The assurance report is published as an appendix to the full ESG Report on meridianllp.com.",
        "Roadmap to reasonable assurance: Meridian plans to transition from limited to reasonable "
        "assurance for Scope 1 and 2 emissions by FY2027, and for material Scope 3 categories by FY2029, "
        "in anticipation of mandatory assurance requirements under the EU CSRD.",
        "Internal controls: The ESG data collection process is integrated into the firm's SOX-equivalent "
        "internal control framework, with documented data flows, control owners, and quarterly reviews.",
    ])

    pdf.section_heading("9", "Human Rights and Modern Slavery Compliance")
    pdf.body_text(
        "Meridian is committed to respecting human rights across our operations and value chain, consistent "
        "with the UN Guiding Principles on Business and Human Rights (UNGPs) and the OECD Guidelines for "
        "Multinational Enterprises."
    )
    pdf.sub_heading("9.1", "Human Rights Due Diligence")
    pdf.bullet_list([
        "Human Rights Impact Assessment (HRIA) conducted biennially; most recent assessment completed "
        "September 2025 covering all operations and tier-1 supply chain.",
        "Salient human rights issues identified: labor rights in extended supply chain (facilities "
        "management, IT hardware manufacturing), data privacy and surveillance risk in technology "
        "deployments, and working conditions in offshore delivery centers.",
        "Remediation: All identified risks have documented mitigation plans with assigned owners and "
        "quarterly progress tracking. Zero substantiated human rights grievances in FY2025.",
        "Grievance mechanism: Accessible to all workers and affected communities via the Ethics Hotline "
        "(24/7, 18 languages) and a dedicated human rights inbox (humanrights@meridianllp.com).",
    ])
    pdf.sub_heading("9.2", "Modern Slavery Statement")
    pdf.bullet_list([
        "Annual Modern Slavery Statement published in compliance with the UK Modern Slavery Act 2015 "
        "(Section 54) and the Australian Modern Slavery Act 2018.",
        "Supply chain risk assessment: All suppliers in high-risk geographies and sectors undergo enhanced "
        "due diligence, including on-site audits for facilities management and hardware suppliers.",
        "Training: 100% of procurement staff (240 professionals) completed modern slavery awareness "
        "training in FY2025. Mandatory annual refresher.",
        "Contractual provisions: All supplier contracts include anti-slavery and anti-trafficking clauses "
        "with right-to-audit provisions and immediate termination for non-compliance.",
        "FY2025 outcomes: 12 enhanced audits conducted; 2 suppliers placed on remediation plans; zero "
        "instances of forced labor or human trafficking identified.",
    ])

    pdf.section_heading("10", "Employee Wellbeing, Health and Safety")
    pdf.body_text(
        "The health, safety, and wellbeing of our 68,000+ professionals is a fundamental responsibility. "
        "Meridian's Global Wellbeing Program encompasses physical safety, mental health, and holistic "
        "employee support."
    )
    pdf.sub_heading("10.1", "Health and Safety Data")
    pdf.bullet_list([
        "Lost-Time Injury Rate (LTIR): 0.04 per 200,000 hours worked (industry average for professional "
        "services: 0.10). Zero work-related fatalities since firm inception.",
        "Total Recordable Incident Rate (TRIR): 0.12 per 200,000 hours worked.",
        "Near-miss reports: 342 submitted in FY2025 (up 28% YoY, reflecting improved reporting culture). "
        "92% resulted in preventive actions within 30 days.",
        "Ergonomic assessments: Completed for 100% of office-based and remote workers. 4,200 workstation "
        "modifications made in FY2025.",
        "Travel safety: 24/7 global travel risk management through International SOS; real-time alerts "
        "and evacuation support for all traveling professionals.",
    ])
    pdf.sub_heading("10.2", "Mental Health and Wellbeing Programs")
    pdf.bullet_list([
        "Employee Assistance Program (EAP): Free, confidential counseling available 24/7 in 18 languages. "
        "Utilization rate: 14.2% in FY2025 (up from 9.8% in FY2023, reflecting reduced stigma).",
        "Mental Health First Aiders: 1,200 trained volunteers across all offices (target: 1 per 50 "
        "employees by 2027).",
        "Burnout prevention: Mandatory project-end downtime of 5 business days for engagements exceeding "
        "12 weeks. Average annual utilization rate monitored at service line level.",
        "Wellbeing days: Four additional paid wellbeing days per year (beyond standard PTO) introduced "
        "in FY2024. 89% utilization in FY2025.",
        "Digital wellbeing: Firm-wide license for Headspace and access to virtual therapy via Spring "
        "Health. 38% active monthly users.",
        "Manager training: Mandatory 'Leading with Wellbeing' module for all people managers. 96% "
        "completion rate in FY2025.",
        "Annual Wellbeing Survey: 82% participation rate; overall wellbeing score: 7.4/10 (up from "
        "6.9/10 in FY2023).",
    ])

    pdf.section_heading("11", "Community Investment and Social Impact")
    pdf.body_text(
        "In FY2025, Meridian invested $45.2 million in community initiatives, comprising $28.1 million in "
        "direct grants and sponsorships, $9.4 million in pro bono professional services (representing "
        "142,000 hours), and $7.7 million in employee volunteer time (98,000 hours)."
    )
    pdf.bullet_list([
        "Meridian Foundation -- Awarded 340 grants totaling $18.5 million to nonprofit organizations "
        "focused on education, economic mobility, and environmental justice.",
        "Skills for Tomorrow -- Free digital skills training delivered to 28,000 individuals in "
        "underserved communities across 15 countries.",
        "Disaster Response -- Deployed rapid-response advisory teams to support recovery from 6 natural "
        "disasters, contributing $3.2 million in cash and services.",
        "Pro Bono Program -- 2,400 professionals contributed 142,000 hours of pro bono work to 280 "
        "nonprofit and social enterprise clients.",
    ])

    pdf.section_heading("12", "Sustainable Procurement")
    pdf.body_text(
        "Meridian's Sustainable Procurement Policy requires all suppliers with contracts exceeding $500,000 "
        "annually to complete a sustainability assessment, disclose Scope 1 and 2 emissions, and commit to "
        "science-based reduction targets within two years of engagement. In FY2025:"
    )
    pdf.bullet_list([
        "86% of tier-1 suppliers (by spend) completed sustainability assessments.",
        "62% of tier-1 suppliers have committed to or achieved SBTi validation.",
        "Introduced a Sustainable Supplier Preferred List, with 5% procurement price preference for "
        "verified sustainable suppliers.",
        "Sustainable procurement spend: $285 million (22.5% of addressable procurement), exceeding our "
        "FY2025 target of 20%.",
    ])

    pdf.section_heading("13", "CSRD, ISSB, and ESRS Readiness")
    pdf.body_text(
        "With the EU Corporate Sustainability Reporting Directive (CSRD) requiring compliance from FY2026 "
        "for large undertakings, and the International Sustainability Standards Board (ISSB) standards "
        "(IFRS S1 and S2) being adopted by multiple jurisdictions, Meridian has launched a comprehensive "
        "readiness program to ensure our own reporting meets evolving requirements and to build advisory "
        "capacity for our EMEA clients."
    )
    pdf.bullet_list([
        "CSRD scope: Meridian's EU entities (covering 8,400 professionals across 16 countries) fall within "
        "scope. A dedicated CSRD Program Office was established in Q1 2025, led by the Chief Sustainability "
        "Officer.",
        "Double materiality assessment: Completed in Q3 2025 in accordance with EFRAG guidance. "
        "14 material topics identified across environmental, social, and governance dimensions.",
        "ESRS mapping: Gap analysis completed against all applicable European Sustainability Reporting "
        "Standards (ESRS). Data collection processes being enhanced for ESRS E1 (Climate), S1 (Own "
        "Workforce), and G1 (Business Conduct) -- the three highest-priority standards.",
        "ISSB alignment: Voluntary early adoption of IFRS S2 (Climate-related Disclosures) in our "
        "FY2026 reporting cycle. Scenario analysis (Section 5) already meets IFRS S2 requirements.",
        "Data infrastructure: Invested $8.5 million in ESG data management platform (Workiva) to "
        "automate data collection, audit trails, and reporting across CSRD, ISSB, GRI, and CDP frameworks.",
        "Advisory capability: 320 professionals across Risk & Compliance and Advisory service lines "
        "trained and certified in CSRD/ESRS advisory. Over 45 CSRD readiness engagements delivered to "
        "EMEA clients in FY2025.",
    ])

    pdf.section_heading("14", "Governance and Reporting Frameworks")
    pdf.bullet_list([
        "Task Force on Climate-related Financial Disclosures (TCFD) -- Fully aligned since 2023; "
        "quantitative scenario analysis added in FY2025 (see Section 5).",
        "Global Reporting Initiative (GRI) Standards -- Report prepared in accordance with GRI 2021.",
        "UN Sustainable Development Goals -- Mapped initiatives to SDGs 4, 5, 8, 10, 12, 13, and 17.",
        "CDP Climate Change -- Scored A- in 2025 disclosure (up from B in 2023).",
        "SASB Standards -- Professional & Commercial Services industry standard disclosures included.",
        "UN Global Compact -- Advanced-level participant; Communication on Progress submitted annually.",
        "ESG Committee of the Board of Partners -- Meets quarterly; chaired by the Chief Sustainability "
        "Officer with direct reporting to the Global Managing Partner.",
        "Executive compensation linkage: 15% of partner variable compensation tied to DEI, ESG, and "
        "people development metrics, of which ESG performance accounts for approximately one-third.",
    ])

    pdf.save("esg_report.pdf")


# ---------------------------------------------------------------------------
# Document 5: Information Security Overview
# ---------------------------------------------------------------------------
def gen_infosec_overview():
    pdf = FirmPDF("Information Security Overview", "6.1", "January 2026")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "Security Governance and Organization"),
        ("2", "Certifications and Compliance"),
        ("3", "Data Encryption Standards"),
        ("4", "Network and Infrastructure Security"),
        ("5", "Endpoint Protection"),
        ("6", "Security Operations Center (SOC)"),
        ("7", "Vulnerability Management"),
        ("8", "Zero Trust Architecture"),
        ("9", "Third-Party Security Management"),
        ("10", "Security Awareness and Training"),
        ("11", "Data Loss Prevention (DLP)"),
        ("12", "Incident Response Lifecycle"),
        ("13", "AI/ML Security Controls"),
        ("14", "Physical Security"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "Security Governance and Organization")
    pdf.body_text(
        "Information security at Meridian & Associates LLP is governed by the Global Chief Information "
        "Security Officer (CISO), who reports directly to the Chief Operating Officer and has a standing "
        "quarterly briefing with the Board of Partners. The CISO leads a team of 340 security professionals "
        "organized across six functions: Security Architecture, Security Operations, Identity and Access "
        "Management, Governance Risk and Compliance, Application Security, and Incident Response."
    )
    pdf.body_text(
        "The Information Security Steering Committee, comprising the CISO, CIO, CTO, General Counsel, and "
        "Chief Risk Officer, meets monthly to review the security posture, approve policy changes, and "
        "allocate resources. The firm's annual information security budget exceeds $120 million."
    )

    pdf.section_heading("2", "Certifications and Compliance")
    pdf.body_text(
        "Meridian maintains a comprehensive set of security certifications and undergoes rigorous "
        "independent audits annually:"
    )
    pdf.bullet_list([
        "SOC 2 Type II -- Certified across all service delivery environments. Annual audit performed by "
        "an independent Big 4 firm; most recent report issued October 2025 with zero exceptions.",
        "ISO 27001:2022 -- Certified for all global operations. Certification body: BSI Group. Last "
        "recertification: March 2025.",
        "ISO 27017 -- Cloud security controls certification for our managed services environments.",
        "ISO 27018 -- Protection of personally identifiable information in public clouds.",
        "ISO 22301 -- Business continuity management system certification.",
        "PCI DSS v4.0 -- Level 1 Service Provider for engagements handling cardholder data.",
        "FedRAMP Moderate -- Authorized for U.S. federal government engagements.",
        "HITRUST CSF v11 -- Certified for healthcare client engagements.",
    ])

    pdf.section_heading("3", "Data Encryption Standards")
    pdf.sub_heading("3.1", "Data at Rest")
    pdf.bullet_list([
        "AES-256 encryption for all data at rest across all storage systems.",
        "Full-disk encryption (BitLocker/FileVault) mandatory on all endpoints.",
        "Database-level Transparent Data Encryption (TDE) for all production databases.",
        "Hardware Security Modules (HSMs) for cryptographic key management, FIPS 140-2 Level 3 certified.",
    ])
    pdf.sub_heading("3.2", "Data in Transit")
    pdf.bullet_list([
        "TLS 1.3 enforced for all external communications; TLS 1.2 minimum for legacy integrations "
        "(with documented exception and remediation timeline).",
        "Mutual TLS (mTLS) for all inter-service communications within the internal network.",
        "IPSec VPN with AES-256-GCM for site-to-site connectivity.",
        "Certificate management via automated PKI with 90-day rotation for all server certificates.",
    ])

    pdf.section_heading("4", "Network and Infrastructure Security")
    pdf.bullet_list([
        "Micro-segmented network architecture with software-defined perimeters.",
        "Next-generation firewalls (Palo Alto Networks) at all network boundaries.",
        "Distributed Denial of Service (DDoS) mitigation via Cloudflare Enterprise.",
        "DNS security with DNSSEC validation and DNS-over-HTTPS for all endpoints.",
        "Web Application Firewall (WAF) protecting all internet-facing applications.",
        "Network Detection and Response (NDR) deployed across all segments.",
    ])

    pdf.section_heading("5", "Endpoint Protection")
    pdf.bullet_list([
        "CrowdStrike Falcon deployed on 100% of managed endpoints (72,000+ devices).",
        "Endpoint Detection and Response (EDR) with 24/7 managed threat hunting.",
        "Mobile Device Management (MDM) via Microsoft Intune for all firm-issued and BYOD devices.",
        "Application allowlisting on all critical infrastructure servers.",
        "USB and removable media controls -- disabled by default, exception-based approval process.",
        "Automated patch deployment within 72 hours for critical vulnerabilities, 14 days for high.",
    ])

    pdf.section_heading("6", "Security Operations Center (SOC)")
    pdf.body_text(
        "Meridian operates a 24/7/365 Security Operations Center with primary facilities in Chicago and "
        "London, and a tertiary facility in Bangalore for follow-the-sun coverage. The SOC processes an "
        "average of 4.2 billion security events per day."
    )
    pdf.bullet_list([
        "SIEM Platform: Splunk Enterprise Security with custom correlation rules and ML-based anomaly "
        "detection.",
        "SOAR Platform: Palo Alto XSOAR for automated incident triage and response playbooks.",
        "Mean Time to Detect (MTTD): < 15 minutes for critical threats.",
        "Mean Time to Respond (MTTR): < 1 hour for critical incidents.",
        "Threat Intelligence: Integration with 12 commercial and open-source threat intelligence feeds, "
        "plus a dedicated in-house threat intelligence team of 18 analysts.",
        "Purple Team Exercises: Conducted quarterly with external red team partners.",
    ])

    pdf.section_heading("7", "Vulnerability Management")
    pdf.bullet_list([
        "Continuous vulnerability scanning across all environments using Qualys and Tenable.",
        "Critical vulnerabilities: Remediation within 24 hours.",
        "High vulnerabilities: Remediation within 7 days.",
        "Medium vulnerabilities: Remediation within 30 days.",
        "Annual penetration testing by two independent firms (rotating annually).",
        "Bug bounty program via HackerOne for internet-facing applications.",
        "Static Application Security Testing (SAST) and Dynamic Application Security Testing (DAST) "
        "integrated into all CI/CD pipelines.",
    ])

    pdf.section_heading("8", "Zero Trust Architecture")
    pdf.body_text(
        "Meridian has implemented a comprehensive Zero Trust security model based on NIST SP 800-207 "
        "principles:"
    )
    pdf.bullet_list([
        "Identity-Centric Access -- All access decisions based on verified identity, device health, and "
        "contextual risk signals. No implicit trust based on network location.",
        "Continuous Verification -- Session-based re-authentication every 8 hours; step-up MFA for "
        "sensitive operations.",
        "Least Privilege -- Role-based access control (RBAC) with quarterly access reviews and automated "
        "deprovisioning for role changes.",
        "Micro-Segmentation -- East-west traffic controlled by identity-aware policies; lateral "
        "movement restricted by default.",
        "Multi-Factor Authentication -- Enforced for all users via hardware security keys (FIDO2) or "
        "Microsoft Authenticator. SMS-based MFA prohibited.",
    ])

    pdf.section_heading("9", "Third-Party Security Management")
    pdf.body_text(
        "All third-party vendors and subcontractors undergo a tiered security assessment based on data "
        "access and criticality:"
    )
    pdf.bullet_list([
        "Tier 1 (Critical -- access to client data): Full security assessment, SOC 2 Type II or equivalent "
        "required, annual on-site audit, continuous monitoring.",
        "Tier 2 (Important -- access to internal systems): Security questionnaire (SIG Lite), evidence of "
        "penetration testing, annual reassessment.",
        "Tier 3 (Standard -- no data access): Self-attestation, periodic spot checks.",
        "Contractual Requirements: All vendors must agree to Meridian's Data Protection Addendum, which "
        "includes breach notification within 24 hours, right to audit, and data destruction upon "
        "termination.",
    ])

    pdf.section_heading("10", "Security Awareness and Training")
    pdf.bullet_list([
        "Mandatory annual security awareness training for all 68,000+ professionals (98.7% completion "
        "rate in FY2025).",
        "Monthly phishing simulations with targeted remediation training for repeat clickers.",
        "Role-based training for developers (OWASP Top 10, secure coding), administrators (hardening "
        "guidelines), and executives (business email compromise awareness).",
        "Security Champion program: 450+ trained security champions embedded in project teams.",
    ])

    pdf.section_heading("11", "Data Loss Prevention (DLP)")
    pdf.body_text(
        "Meridian operates a comprehensive Data Loss Prevention program to detect and prevent unauthorized "
        "exfiltration of sensitive data across all channels:"
    )
    pdf.bullet_list([
        "Endpoint DLP: Microsoft Purview DLP agents deployed on 100% of managed endpoints. Policies "
        "enforce blocking or encryption for files containing PII, client confidential data, and "
        "financial data leaving the corporate environment.",
        "Email DLP: All outbound email scanned in real-time for sensitive data patterns (SSN, credit "
        "card numbers, client code names, MNPI indicators). Policy violations trigger automatic "
        "encryption, quarantine, or block depending on severity.",
        "Cloud DLP: Cloud Access Security Broker (CASB) integration with Microsoft 365, Salesforce, "
        "and all sanctioned SaaS applications. Policies prevent upload of classified data to unsanctioned "
        "cloud services.",
        "Network DLP: Deep content inspection at all network egress points. SSL/TLS inspection for "
        "encrypted traffic (with documented exceptions for banking and healthcare endpoints).",
        "Data classification: Four-tier classification scheme (Public, Internal, Confidential, "
        "Restricted). Automated classification applied at creation using Microsoft Purview Information "
        "Protection. Manual override requires justification and manager approval.",
        "DLP incident metrics FY2025: 14,200 policy violations detected; 98% automatically remediated; "
        "42 escalated to the Insider Threat team for investigation; zero confirmed data exfiltration events.",
    ])

    pdf.section_heading("12", "Incident Response Lifecycle")
    pdf.body_text(
        "Meridian's Incident Response (IR) program follows the NIST SP 800-61 framework, structured "
        "across five phases:"
    )
    pdf.sub_heading("12.1", "Detection and Analysis")
    pdf.bullet_list([
        "24/7 SOC monitoring with automated alert triage via SOAR playbooks.",
        "Threat intelligence correlation across 12 commercial and open-source feeds.",
        "ML-based anomaly detection for user behavior (UEBA) and network traffic.",
        "Mean Time to Detect (MTTD) for critical threats: < 15 minutes.",
        "Severity classification (P1-P4) within 30 minutes of detection.",
    ])
    pdf.sub_heading("12.2", "Containment")
    pdf.bullet_list([
        "Automated containment actions for P1 incidents: endpoint isolation, account suspension, "
        "network segment quarantine.",
        "Containment decision authority: SOC Shift Lead for P3/P4; IR Manager for P2; CISO for P1.",
        "Evidence preservation procedures activated in parallel (forensic imaging, log snapshots).",
    ])
    pdf.sub_heading("12.3", "Eradication")
    pdf.bullet_list([
        "Root cause analysis initiated within 4 hours of containment.",
        "Malware removal, compromised credential rotation, vulnerable system patching.",
        "Threat hunting across the full environment to identify lateral movement or persistence.",
    ])
    pdf.sub_heading("12.4", "Recovery")
    pdf.bullet_list([
        "System restoration from verified clean backups (immutable backups for ransomware scenarios).",
        "Phased recovery with enhanced monitoring: Tier 1 systems restored first within RTO targets.",
        "Client notification per contractual SLAs (typically within 24 hours for data-impacting incidents).",
        "Mean Time to Recover (MTTR) for P1 incidents: < 4 hours.",
    ])
    pdf.sub_heading("12.5", "Lessons Learned")
    pdf.bullet_list([
        "Post-incident review (PIR) completed within 10 business days of incident closure.",
        "PIR report distributed to CISO, CIO, affected business unit leaders, and relevant clients.",
        "Remediation actions tracked to completion with executive-level accountability.",
        "Annual Incident Response Report published internally with trend analysis and improvement plan.",
        "FY2025 summary: 847 security incidents investigated; 12 classified as P1/P2; zero resulted in "
        "confirmed client data breach; average MTTR for P1: 2 hours 48 minutes.",
    ])

    pdf.section_heading("13", "AI/ML Security Controls")
    pdf.body_text(
        "As AI/ML technologies become integral to client engagements and internal operations, Meridian "
        "has implemented security controls specifically designed for AI/ML risks:"
    )
    pdf.bullet_list([
        "Prompt injection defense: All client-facing and internal LLM deployments include input "
        "sanitization, output filtering, and system prompt protection. Validated through quarterly "
        "red-team exercises by the Application Security team.",
        "Model supply chain security: All AI/ML models (proprietary and third-party) are tracked in a "
        "Model Registry with provenance documentation, integrity checksums (SHA-256), and version "
        "control. Third-party model artifacts scanned for known vulnerabilities before deployment.",
        "LLM guardrails: MeridianAI (the firm's enterprise AI orchestration layer) enforces configurable "
        "guardrails including: content filtering for harmful/inappropriate outputs, PII detection and "
        "redaction in prompts and responses, hallucination detection scores, and usage rate limiting.",
        "Data isolation: AI/ML systems operate in dedicated, network-segmented environments. Client data "
        "used for inference is not persisted beyond the session and is never used for model training.",
        "AI-specific penetration testing: Annual specialized penetration testing of all AI/ML systems "
        "covering OWASP Top 10 for LLM Applications (2025), including prompt injection, training data "
        "poisoning, model theft, and excessive agency.",
        "Access controls: All AI/ML model endpoints protected by the same Zero Trust policies as other "
        "firm systems. API keys rotated every 90 days. Usage logged and auditable.",
        "Vendor AI assessments: Third-party AI tools undergo security review covering model architecture, "
        "data handling, training practices, and compliance certifications before approval for use.",
    ])

    pdf.section_heading("14", "Physical Security")
    pdf.body_text(
        "Meridian implements physical security controls across all 127 offices, 11 delivery centers, "
        "and 4 data center facilities to protect personnel, assets, and information:"
    )
    pdf.bullet_list([
        "Badge access: All offices require proximity card (HID iCLASS) or biometric access. Badge "
        "access rights reviewed quarterly and revoked within 4 hours of termination or role change.",
        "Visitor management: All visitors must present government-issued ID, sign a visitor log, and "
        "be escorted by a badged employee at all times. Visitor badges are visually distinct and "
        "expire at end of business day.",
        "CCTV: Video surveillance at all entry/exit points, server rooms, and common areas. 90-day "
        "retention for standard footage; 1-year retention for security-sensitive areas. Monitored by "
        "the Global Security Operations Center.",
        "Clean rooms: Designated secure workspaces for engagements requiring enhanced physical security "
        "(defense, intelligence community, financial services M&A). Clean rooms feature: Faraday "
        "shielding, no-device policies, separate network segments, and restricted badge access limited "
        "to named individuals.",
        "Data center physical security: Tier IV facilities with multi-layer physical controls including "
        "mantrap entry, biometric + PIN access, 24/7 on-site guards, vehicle barriers, and seismic "
        "bracing. Access restricted to pre-approved personnel with background checks.",
        "Mail and package screening: All incoming mail and packages at major offices screened through "
        "X-ray scanners.",
    ])

    pdf.save("infosec_overview.pdf")


# ---------------------------------------------------------------------------
# Document 6: Data Privacy Policy
# ---------------------------------------------------------------------------
def gen_data_privacy():
    pdf = FirmPDF("Data Privacy Policy", "4.3", "January 2026")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "Policy Purpose and Scope"),
        ("2", "GDPR Compliance Framework"),
        ("3", "U.S. Privacy Compliance (CCPA/CPRA)"),
        ("4", "HIPAA Compliance"),
        ("5", "China PIPL Compliance"),
        ("6", "Cross-Border Data Transfers"),
        ("7", "Data Subject Rights"),
        ("8", "Privacy Impact Assessments"),
        ("9", "Data Retention and Disposal"),
        ("10", "Data Protection Officer"),
        ("11", "Breach Notification Procedures"),
        ("12", "AI and Data Processing"),
        ("13", "Privacy by Design"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "Policy Purpose and Scope")
    pdf.body_text(
        "This Data Privacy Policy establishes the principles, standards, and procedures by which Meridian "
        "& Associates LLP collects, processes, stores, and disposes of personal data in all jurisdictions "
        "where we operate. The policy applies to all personal data processed by the firm, whether relating "
        "to clients, employees, contractors, job applicants, website visitors, or any other data subjects."
    )
    pdf.body_text(
        "Meridian recognizes that privacy is a fundamental right and a cornerstone of trust. Our approach "
        "is to apply the highest applicable standard globally -- where local law imposes stricter "
        "requirements, those requirements take precedence; where local law is less prescriptive, the GDPR "
        "standard applies as our baseline."
    )

    pdf.section_heading("2", "GDPR Compliance Framework")
    pdf.body_text(
        "As a firm with significant operations in the European Economic Area and processing substantial "
        "volumes of EU personal data, GDPR compliance is a foundational element of our privacy program."
    )
    pdf.sub_heading("2.1", "Lawful Bases for Processing")
    pdf.bullet_list([
        "Client engagement data: Legitimate interest (delivery of contracted services) and contractual "
        "necessity.",
        "Employee data: Contractual necessity, legal obligation, and legitimate interest.",
        "Marketing data: Consent (explicit opt-in for electronic marketing).",
        "Special category data: Explicit consent or substantial public interest (where applicable).",
    ])
    pdf.sub_heading("2.2", "Records of Processing Activities (ROPA)")
    pdf.body_text(
        "Meridian maintains a comprehensive ROPA covering all processing activities across all entities, "
        "updated quarterly. The ROPA includes: purpose of processing, categories of data subjects, data "
        "categories, recipients, transfer mechanisms, retention periods, and security measures. The ROPA "
        "is managed centrally via OneTrust and is available to supervisory authorities upon request."
    )
    pdf.sub_heading("2.3", "Data Protection Impact Assessments")
    pdf.body_text(
        "DPIAs are mandatory for any processing that is likely to result in a high risk to data subjects, "
        "including: large-scale profiling, systematic monitoring, processing of special categories at scale, "
        "and new technology deployments involving personal data. In FY2025, 89 DPIAs were completed."
    )

    pdf.section_heading("3", "U.S. Privacy Compliance (CCPA/CPRA)")
    pdf.body_text(
        "Meridian complies with the California Consumer Privacy Act (as amended by the California Privacy "
        "Rights Act) and monitors emerging state privacy laws across all 50 states. Current compliance "
        "covers:"
    )
    pdf.bullet_list([
        "California (CCPA/CPRA) -- Full compliance including data minimization, purpose limitation, and "
        "automated decision-making opt-out.",
        "Virginia (VCDPA), Colorado (CPA), Connecticut (CTDPA), Utah (UCPA), Texas (TDPSA), Oregon "
        "(OCPA) -- Compliant with all enacted state privacy laws as of January 2026.",
        "Do Not Sell/Share -- Meridian does not sell personal information. We honor Global Privacy Control "
        "(GPC) signals as opt-out requests.",
        "Service Provider Agreements -- All U.S. vendor contracts include CCPA-compliant service provider "
        "terms with restrictions on use, retention, and disclosure.",
    ])

    pdf.section_heading("4", "HIPAA Compliance")
    pdf.body_text(
        "Healthcare & Life Sciences represents 18% of Meridian's global revenue, making HIPAA compliance "
        "a critical component of our privacy program. Meridian acts as a Business Associate under HIPAA "
        "for engagements involving protected health information (PHI)."
    )
    pdf.bullet_list([
        "Business Associate Agreements (BAAs): Executed with all healthcare clients before any PHI "
        "is accessed or processed. BAA template aligned with 45 CFR 164.504(e).",
        "HIPAA Security Rule: Administrative, physical, and technical safeguards implemented across all "
        "systems handling PHI, including AES-256 encryption, role-based access controls, automatic "
        "session timeout, and audit logging with 7-year retention.",
        "HIPAA Privacy Rule: Minimum necessary standard enforced for all PHI access. Workforce members "
        "access only the PHI required for their specific engagement role.",
        "HITRUST CSF v11 certification: Maintained across all healthcare delivery environments, providing "
        "a comprehensive control framework that incorporates HIPAA, NIST, and ISO 27001 requirements.",
        "Dedicated healthcare privacy team: 8 privacy professionals specializing in healthcare data "
        "regulations, including HIPAA, HITECH, 42 CFR Part 2 (substance use disorder records), and "
        "state-specific health privacy laws.",
        "PHI breach history: Zero reportable PHI breaches in the past 5 fiscal years.",
        "Training: HIPAA-specific training mandatory for all professionals assigned to healthcare "
        "engagements. Annual refresher with 100% completion rate in FY2025.",
    ])

    pdf.section_heading("5", "China PIPL Compliance")
    pdf.body_text(
        "Meridian operates five offices in Greater China (Shanghai, Beijing, Hong Kong, Shenzhen, and Guangzhou) "
        "with approximately 2,200 professionals. Compliance with China's Personal Information Protection "
        "Law (PIPL), effective November 2021, is managed through a dedicated China Privacy Program."
    )
    pdf.bullet_list([
        "Local data residency: All personal information of Chinese data subjects is stored on servers "
        "located within mainland China (hosted on Alibaba Cloud, Beijing region) in compliance with PIPL "
        "Article 40 and the Cyberspace Administration of China (CAC) data localization requirements.",
        "Cross-border transfers: Where personal information must be transferred outside China (e.g., "
        "for global HR processes or cross-border engagements), Meridian has completed the CAC-mandated "
        "Standard Contract filing and Security Assessment as required by the Measures on Standard "
        "Contracts for Cross-Border Transfers of Personal Information.",
        "Consent management: Separate, informed consent obtained for all personal information processing "
        "in China, in compliance with PIPL Articles 13-14. Enhanced consent procedures for sensitive "
        "personal information (biometric, financial, location data).",
        "Personal Information Protection Impact Assessments (PIPIAs): Conducted for all processing "
        "activities involving Chinese personal information that meet PIPL Article 55 thresholds. "
        "12 PIPIAs completed in FY2025.",
        "DPO equivalent: A dedicated Personal Information Protection Officer has been appointed for "
        "Meridian's China operations, as required by PIPL Article 52.",
        "Regulatory engagement: Active participation in CAC and Ministry of Industry and Information "
        "Technology (MIIT) consultation processes on implementing regulations.",
    ])

    pdf.section_heading("6", "Cross-Border Data Transfers")
    pdf.body_text(
        "Given our global operations, cross-border data transfers are inherent to our business. Meridian "
        "employs the following mechanisms to ensure lawful transfers:"
    )
    pdf.bullet_list([
        "Standard Contractual Clauses (SCCs) -- EU-approved SCCs (June 2021 version) are incorporated "
        "into all inter-company and vendor agreements involving transfers from the EEA.",
        "Binding Corporate Rules (BCRs) -- Meridian's BCRs were approved by the Irish Data Protection "
        "Commission (as lead authority) in 2024 and are recognized across all EEA member states.",
        "Transfer Impact Assessments (TIAs) -- Conducted for all transfers to countries without an "
        "adequacy decision. TIAs evaluate the legal framework of the recipient country, supplementary "
        "measures applied, and residual risk.",
        "UK International Data Transfer Agreement (IDTA) -- Used for transfers from the UK post-Brexit.",
        "APEC Cross-Border Privacy Rules (CBPR) -- Certified for transfers within the APEC framework.",
        "Supplementary Measures -- Including encryption in transit and at rest, pseudonymization, and "
        "contractual prohibitions on government access disclosure.",
    ])

    pdf.section_heading("7", "Data Subject Rights")
    pdf.body_text(
        "Meridian has established a centralized Data Subject Rights portal (privacy.meridianllp.com) "
        "that enables individuals to exercise the following rights:"
    )
    pdf.bullet_list([
        "Right of Access -- Response within 30 days (GDPR) / 45 days (CCPA).",
        "Right to Rectification -- Inaccurate data corrected within 10 business days.",
        "Right to Erasure (Right to be Forgotten) -- Processed within 30 days, subject to legal holds "
        "and regulatory retention requirements.",
        "Right to Restriction of Processing -- Implemented within 5 business days.",
        "Right to Data Portability -- Machine-readable export provided within 30 days.",
        "Right to Object -- Objections to processing assessed within 15 business days.",
        "Rights Related to Automated Decision-Making -- Human review available upon request for any "
        "decision made solely by automated means.",
    ])
    pdf.body_text(
        "In FY2025, Meridian processed 2,340 data subject requests with an average response time of "
        "18 days and a 100% on-time completion rate."
    )

    pdf.section_heading("8", "Privacy Impact Assessments")
    pdf.body_text(
        "Privacy Impact Assessments (PIAs) are integrated into the firm's project lifecycle methodology. "
        "A PIA is required before the launch of any new system, application, or process that involves "
        "personal data. The PIA process includes: data mapping, risk identification, controls assessment, "
        "and sign-off by the DPO. High-risk PIAs require review by the Privacy Steering Committee."
    )

    pdf.section_heading("9", "Data Retention and Disposal")
    pdf.body_text("Meridian's data retention schedule is based on the principle of data minimization:")
    pdf.bullet_list([
        "Active client engagement data: Duration of engagement + 7 years (regulatory minimum).",
        "Client proposals and RFP responses: 3 years from submission.",
        "Employee records: Duration of employment + 7 years (or longer if required by local law).",
        "Job applicant data: 2 years from decision date (or 6 months in jurisdictions requiring shorter "
        "retention).",
        "Marketing consent records: Duration of consent + 3 years.",
        "System logs and audit trails: 13 months (standard) / 7 years (for regulated engagements).",
    ])
    pdf.body_text(
        "Data disposal follows NIST SP 800-88 guidelines. Electronic media is sanitized via cryptographic "
        "erasure or physical destruction. Paper records are cross-cut shredded. Disposal certificates are "
        "retained for audit purposes."
    )

    pdf.section_heading("10", "Data Protection Officer")
    pdf.body_text(
        "Meridian has appointed a Global Data Protection Officer (DPO) as required by Article 37 of the "
        "GDPR. The DPO operates independently and reports directly to the Board of Partners on all privacy "
        "matters."
    )
    pdf.bullet_list([
        "Global DPO: Dr. Helena Voss, CIPP/E, CIPM, FIP",
        "Contact: dpo@meridianllp.com",
        "EU Representative (Art. 27): Meridian EU Privacy Office, Dublin, Ireland",
        "UK Representative: Meridian UK Privacy Office, London, United Kingdom",
    ])
    pdf.body_text(
        "Regional Privacy Officers are appointed in each major jurisdiction and serve as the first point "
        "of contact for local regulatory authorities. The DPO is supported by a team of 24 privacy "
        "professionals."
    )

    pdf.section_heading("11", "Breach Notification Procedures")
    pdf.bullet_list([
        "All suspected or confirmed data breaches must be reported to the Privacy Incident Response Team "
        "(PIRT) within 1 hour of discovery via the internal hotline or email.",
        "The PIRT conducts a preliminary assessment within 4 hours to determine scope, severity, and "
        "notification obligations.",
        "GDPR notification: Supervisory authority notified within 72 hours where required. Data subjects "
        "notified without undue delay for high-risk breaches.",
        "CCPA notification: Affected California residents notified in the most expedient time possible.",
        "Contractual notification: Affected clients notified within 24 hours per standard DPA terms.",
        "Post-incident review completed within 30 days with remediation plan and lessons learned.",
    ])

    pdf.section_heading("12", "AI and Data Processing")
    pdf.body_text(
        "As Meridian expands its use of artificial intelligence and machine learning across client "
        "engagements and internal operations, the firm enforces strict controls to ensure personal data "
        "is excluded from AI/ML model training and that all AI-driven processing of personal data "
        "complies with applicable privacy regulations."
    )
    pdf.bullet_list([
        "No personal data in model training: Client personal data and employee personal data are never "
        "used to train, fine-tune, or improve AI/ML models -- whether proprietary (MeridianAI) or "
        "third-party. This prohibition is enforced through technical controls (data classification "
        "tagging, automated PII detection, and training pipeline guardrails) and contractual obligations "
        "with all AI/ML vendors.",
        "AI processing lawful basis: Any processing of personal data by AI systems (e.g., document "
        "analysis, anomaly detection in audit, HR analytics) must have a documented lawful basis under "
        "GDPR Article 6 (and equivalent provisions under CCPA, PIPL, etc.), recorded in the ROPA.",
        "Automated decision-making: Where AI systems produce outputs that could materially affect data "
        "subjects (e.g., candidate screening, risk scoring), Meridian ensures meaningful human review "
        "before any decision is finalized, in compliance with GDPR Article 22.",
        "Data minimization in AI: Only the minimum necessary personal data fields are provided to AI "
        "systems. Pseudonymization and anonymization are applied wherever technically feasible.",
        "Third-party AI vendor assessments: All AI/ML vendors undergo privacy-specific due diligence "
        "including review of data processing terms, sub-processor disclosures, data residency, and "
        "model training practices. Vendors that train models on client-provided data are not approved.",
        "Opt-in policy: Clients must provide explicit written consent before any personal data from "
        "their engagement is processed by AI/ML systems beyond standard document search and retrieval.",
    ])

    pdf.section_heading("13", "Privacy by Design")
    pdf.body_text(
        "Meridian embeds privacy by design and by default into all systems, processes, and services. This "
        "includes: data minimization at collection, purpose limitation enforced via technical controls, "
        "privacy-preserving default settings, and automated data lifecycle management. All new technology "
        "deployments undergo a Privacy Architecture Review before production deployment."
    )

    pdf.save("data_privacy_policy.pdf")


# ---------------------------------------------------------------------------
# Document 7: BCDR Plan
# ---------------------------------------------------------------------------
def gen_bcdr_plan():
    pdf = FirmPDF("Business Continuity and Disaster Recovery Plan", "5.2", "January 2026")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "Purpose and Scope"),
        ("2", "Governance and Organizational Structure"),
        ("3", "Business Impact Analysis"),
        ("4", "Recovery Objectives"),
        ("5", "Data Center and Infrastructure Redundancy"),
        ("6", "Backup and Replication Strategy"),
        ("7", "Pandemic and Workforce Disruption"),
        ("8", "Communication and Escalation"),
        ("9", "Testing and Exercise Program"),
        ("10", "Third-Party Dependency Management"),
        ("11", "Cyber Incident and Ransomware Recovery"),
        ("12", "Client-Specific BCDR Customization"),
        ("13", "Vendor Dependency Matrix"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "Purpose and Scope")
    pdf.body_text(
        "This Business Continuity and Disaster Recovery (BCDR) Plan establishes the framework, procedures, "
        "and responsibilities for maintaining critical business operations and recovering technology "
        "infrastructure in the event of a disruption. The plan covers all Meridian & Associates LLP "
        "operations globally, including client-facing service delivery, internal business functions, and "
        "supporting technology infrastructure."
    )
    pdf.body_text(
        "The plan is designed to address a range of disruption scenarios including: natural disasters "
        "(earthquake, flood, hurricane, wildfire), technology failures (data center outage, network failure, "
        "ransomware attack), pandemic or health emergencies, civil unrest or geopolitical events, and "
        "critical supplier failures. The plan is reviewed and updated at least semi-annually, with ad hoc "
        "updates triggered by significant organizational changes, lessons learned from exercises, or "
        "emerging threats."
    )

    pdf.section_heading("2", "Governance and Organizational Structure")
    pdf.bullet_list([
        "Executive Sponsor: Chief Operating Officer (COO)",
        "BCDR Program Director: VP of Enterprise Resilience, reporting to the COO",
        "Crisis Management Team (CMT): COO, CISO, General Counsel, Chief People Officer, Head of "
        "Communications, Regional Managing Partners",
        "Business Continuity Coordinators: Designated in each service line and major office (142 total)",
        "DR Engineering Team: 28 dedicated infrastructure engineers responsible for DR environment "
        "maintenance and failover execution",
    ])

    pdf.section_heading("3", "Business Impact Analysis")
    pdf.body_text(
        "Meridian conducts a comprehensive Business Impact Analysis (BIA) annually to classify all business "
        "processes and technology systems by criticality. Systems are classified into four tiers:"
    )
    pdf.bullet_list([
        "Tier 1 -- Mission Critical: Revenue-generating client delivery systems, email and collaboration, "
        "identity and access management, financial systems. Downtime tolerance: < 4 hours.",
        "Tier 2 -- Business Critical: CRM, project management, time and expense, knowledge management. "
        "Downtime tolerance: < 12 hours.",
        "Tier 3 -- Business Important: Learning management, internal portals, analytics dashboards. "
        "Downtime tolerance: < 48 hours.",
        "Tier 4 -- Non-Critical: Archive systems, development/test environments. Downtime tolerance: "
        "< 5 business days.",
    ])

    pdf.section_heading("4", "Recovery Objectives")
    pdf.body_text("Recovery objectives are defined by system tier:")
    pdf.bullet_list([
        "Tier 1 -- RPO: 1 hour, RTO: 4 hours. Synchronous replication to secondary data center. "
        "Automated failover with manual confirmation.",
        "Tier 2 -- RPO: 4 hours, RTO: 12 hours. Asynchronous replication with 4-hour snapshots.",
        "Tier 3 -- RPO: 24 hours, RTO: 48 hours. Daily backup replication.",
        "Tier 4 -- RPO: 48 hours, RTO: 5 business days. Weekly backup replication.",
    ])
    pdf.body_text(
        "These objectives have been validated through testing and are contractually committed to clients "
        "whose SLAs reference our BCDR capabilities."
    )

    pdf.section_heading("5", "Data Center and Infrastructure Redundancy")
    pdf.sub_heading("5.1", "Primary and Secondary Data Centers")
    pdf.bullet_list([
        "Primary Data Center: Equinix CH3, Chicago, Illinois -- Tier IV design, 99.995% uptime SLA. "
        "2,400 sq ft dedicated cage, N+1 power and cooling redundancy.",
        "Secondary Data Center: CyrusOne Sterling, Virginia -- Geographically separated by 580 miles. "
        "Active-passive configuration with automated failover capability.",
        "European Data Center: Equinix LD8, London -- Serves EMEA operations with data sovereignty "
        "controls ensuring EU data remains within the EEA.",
        "APAC Data Center: Equinix SG3, Singapore -- Serves APAC operations.",
    ])
    pdf.sub_heading("5.2", "Cloud Infrastructure")
    pdf.bullet_list([
        "Primary cloud provider: Microsoft Azure (multi-region, paired regions for DR).",
        "Secondary cloud provider: AWS (used for specific workloads and as tertiary DR option).",
        "All cloud workloads deployed across minimum two availability zones.",
        "Cross-region replication for all Tier 1 and Tier 2 cloud services.",
    ])

    pdf.section_heading("6", "Backup and Replication Strategy")
    pdf.bullet_list([
        "Tier 1 systems: Synchronous replication (zero data loss) between primary and secondary sites. "
        "Additional daily backups retained for 90 days.",
        "Tier 2 systems: Asynchronous replication every 4 hours. Daily backups retained for 60 days.",
        "Tier 3/4 systems: Daily incremental backups, weekly full backups. Retained for 30 days.",
        "All backups encrypted (AES-256) and integrity-verified via automated checksums.",
        "Annual backup restoration testing: 100% of Tier 1 systems, 50% of Tier 2 systems tested "
        "annually.",
        "Immutable backup copies maintained in air-gapped storage for ransomware resilience.",
    ])

    pdf.section_heading("7", "Pandemic and Workforce Disruption")
    pdf.body_text(
        "Meridian's pandemic response protocol was extensively refined during COVID-19 and has been "
        "maintained in a state of readiness. Key elements:"
    )
    pdf.bullet_list([
        "100% remote work capability -- All 68,000+ professionals can operate fully remotely within 24 "
        "hours of activation. VPN and virtual desktop infrastructure scaled to support concurrent full "
        "workforce access.",
        "Split-team operations -- Critical functions operate with geographically dispersed A/B teams to "
        "prevent single-site workforce loss.",
        "Supply chain for hardware -- Pre-positioned inventory of 5,000 laptops and peripherals for "
        "rapid deployment.",
        "Mental health and wellbeing support -- Expanded EAP services, manager training on remote team "
        "wellbeing, and flexible work arrangements during extended disruptions.",
        "Trigger thresholds: Monitoring tier activated when WHO raises alert level; full protocol "
        "activated upon pandemic declaration or when >5% of any office reports illness.",
    ])

    pdf.section_heading("8", "Communication and Escalation")
    pdf.sub_heading("8.1", "Communication Cascade")
    pdf.bullet_list([
        "T+0 minutes: Incident detected and reported to BCDR Program Director and on-call CMT member.",
        "T+15 minutes: CMT convened (virtual war room). Initial assessment of scope and severity.",
        "T+30 minutes: Crisis communication drafted for internal distribution.",
        "T+1 hour: Employee notification via Everbridge mass notification system (SMS, email, push "
        "notification, voice call).",
        "T+2 hours: Client notification for affected engagements (via Engagement Partners).",
        "T+4 hours: External stakeholder communication (regulators, insurers) if required.",
    ])
    pdf.sub_heading("8.2", "Communication Channels")
    pdf.bullet_list([
        "Primary: Everbridge Mass Notification Platform",
        "Secondary: Microsoft Teams (dedicated Crisis Channel)",
        "Tertiary: Satellite phone network (12 units distributed to CMT members and regional leads)",
        "Backup: Personal mobile phones via pre-registered contact tree",
    ])

    pdf.section_heading("9", "Testing and Exercise Program")
    pdf.body_text(
        "Meridian conducts a rigorous annual testing program to validate BCDR capabilities:"
    )
    pdf.bullet_list([
        "Full DR Failover Test -- Conducted annually (most recent: September 2025). Full failover of "
        "all Tier 1 systems to secondary data center. RTO achieved: 3 hours 12 minutes (within 4-hour "
        "target). RPO achieved: 47 minutes (within 1-hour target).",
        "Tabletop Exercises -- Two per year with CMT participation. Scenarios include ransomware attack, "
        "multi-site natural disaster, and critical vendor failure.",
        "Departmental BCP Tests -- Each service line conducts at least one business continuity exercise "
        "annually.",
        "Communication Cascade Tests -- Quarterly Everbridge tests with >95% acknowledgment rate target. "
        "FY2025 average: 97.2% within 30 minutes.",
        "Third-Party DR Validation -- Annual review of critical vendor DR capabilities and contractual "
        "SLAs.",
    ])

    pdf.section_heading("10", "Third-Party Dependency Management")
    pdf.body_text(
        "Meridian identifies and manages third-party dependencies that could impact business continuity:"
    )
    pdf.bullet_list([
        "Critical Vendor Registry: 47 vendors classified as critical (single point of failure or "
        "essential to Tier 1 processes).",
        "Contractual Requirements: All critical vendors must demonstrate BCDR capabilities with RTOs "
        "equal to or better than Meridian's requirements.",
        "Annual DR Evidence Collection: SOC 2 reports, DR test results, and BCP documentation reviewed "
        "annually for all critical vendors.",
        "Diversification Policy: No single vendor may represent more than 30% of spend in any critical "
        "service category. Alternative vendors pre-qualified for top 20 critical services.",
        "Escrow Agreements: Source code escrow for all critical bespoke software vendors.",
    ])

    pdf.section_heading("11", "Cyber Incident and Ransomware Recovery")
    pdf.body_text(
        "Ransomware and destructive cyber attacks represent one of the highest-probability, "
        "highest-impact disruption scenarios. Meridian maintains a dedicated Cyber Incident Recovery "
        "Plan that supplements the general BCDR framework:"
    )
    pdf.sub_heading("11.1", "Ransomware-Specific Controls")
    pdf.bullet_list([
        "Immutable backups: All Tier 1 and Tier 2 system backups are stored in air-gapped, immutable "
        "storage (write-once, read-many). Backup integrity verified daily via automated checksums.",
        "Network segmentation: Microsegmentation limits lateral movement. Delivery center networks are "
        "isolated from corporate networks and from each other.",
        "Endpoint isolation: CrowdStrike Falcon real-time response enables one-click isolation of "
        "compromised endpoints within seconds of detection.",
        "Ransomware-specific playbooks: Pre-approved response playbooks for 6 ransomware scenarios, "
        "tested quarterly in tabletop exercises with the Crisis Management Team.",
        "Decryption capability: Relationship with law enforcement (FBI, NCA, Europol) and ransomware "
        "decryptor databases (No More Ransom) for recovery without payment.",
    ])
    pdf.sub_heading("11.2", "Recovery Procedures")
    pdf.bullet_list([
        "Containment: Immediate network isolation of affected segments. Kill switch for all outbound "
        "internet connectivity if active data exfiltration detected.",
        "Forensic investigation: Retained incident response firm (CrowdStrike Services) on standby "
        "with guaranteed 2-hour response SLA. Forensic investigation runs in parallel with recovery.",
        "Clean recovery: Systems rebuilt from verified clean images and immutable backups. No data "
        "restored from potentially compromised backup snapshots.",
        "Identity reset: Full credential rotation for all administrative accounts. MFA re-enrollment "
        "for affected users.",
        "Ransom payment policy: Meridian's policy is not to pay ransoms. This position is endorsed by "
        "the Board of Partners and communicated to insurers. Exception requires unanimous CMT approval "
        "and legal counsel sign-off.",
        "Recovery time target: Full Tier 1 recovery from ransomware scenario within 8 hours. "
        "Most recent test (September 2025): achieved in 6 hours 22 minutes.",
    ])

    pdf.section_heading("12", "Client-Specific BCDR Customization")
    pdf.body_text(
        "Meridian recognizes that many clients -- particularly in financial services, healthcare, and "
        "government -- have BCDR requirements that exceed the firm's standard framework. The firm offers "
        "client-specific BCDR customization through the following mechanisms:"
    )
    pdf.bullet_list([
        "Client BCDR questionnaire: Completed during engagement onboarding to identify enhanced "
        "requirements (e.g., tighter RTOs, dedicated recovery environments, regulatory-specific "
        "notifications).",
        "Dedicated recovery environments: For Tier 1 clients (annual fees >$10M), Meridian can provision "
        "dedicated DR environments with client-specified configurations, tested semi-annually.",
        "Client-specific tabletop exercises: Annual joint tabletop exercises with the client's BC team "
        "to validate end-to-end recovery across both organizations. Offered to all clients with "
        "managed services contracts.",
        "Regulatory alignment: BCDR plans tailored to sector-specific regulations including DORA "
        "(EU financial services), OCC Heightened Standards (U.S. banking), and CPS 230 (APRA, Australia).",
        "Client notification SLAs: Default notification within 24 hours of a material incident. "
        "Accelerated notification (4-hour or 1-hour) available contractually for critical engagements.",
        "Client audit rights: All managed services clients have contractual rights to audit Meridian's "
        "BCDR capabilities annually, including observation of DR failover tests.",
    ])

    pdf.section_heading("13", "Vendor Dependency Matrix")
    pdf.body_text(
        "The following summarizes Meridian's critical vendor dependencies, diversification status, "
        "and contractual BCDR commitments for the firm's most essential third-party services:"
    )
    pdf.bullet_list([
        "Cloud Infrastructure (Microsoft Azure, primary): RTO contractual SLA 4 hours. Multi-region "
        "deployment across paired regions. Secondary provider: AWS (active for specific workloads). "
        "Diversification: Yes.",
        "Cloud Infrastructure (AWS, secondary): Used for 20% of workloads. Cross-region replication "
        "configured. Provides tertiary DR option for Azure-primary services. Diversification: Yes.",
        "Collaboration Platform (Microsoft 365): RTO contractual SLA 4 hours. Geo-redundant deployment. "
        "Offline access capability via cached Outlook/Teams. Alternative: Satellite phone network and "
        "backup email system. Diversification: Partial.",
        "SIEM/Security (Splunk Enterprise): RTO 2 hours. Deployed in active-active across two data "
        "centers. Alternative: Azure Sentinel as warm standby. Diversification: Yes.",
        "Endpoint Security (CrowdStrike Falcon): Cloud-native, multi-region. RTO < 1 hour. "
        "No single-vendor alternative but compensating controls (Windows Defender ATP) available. "
        "Diversification: Partial.",
        "Data Center Facilities (Equinix): Three facilities (Chicago, London, Singapore). Each site has "
        "independent contracts with separate power and cooling infrastructure. Geographic separation "
        "provides inherent diversification. Diversification: Yes.",
        "Telecommunications (multiple carriers): Primary: AT&T (Americas), BT (EMEA), Singtel (APAC). "
        "Secondary carriers in each region. SD-WAN overlay enables automated failover. "
        "Diversification: Yes.",
        "HR/Payroll (Workday): RTO 12 hours. Multi-tenant cloud with Workday-managed DR. Manual "
        "payroll processing procedures documented as fallback. Diversification: No (single vendor, "
        "assessed acceptable risk).",
    ])

    pdf.save("bcdr_plan.pdf")


# ---------------------------------------------------------------------------
# Document 8: Code of Conduct
# ---------------------------------------------------------------------------
def gen_code_of_conduct():
    pdf = FirmPDF("Code of Conduct and Business Ethics", "7.0", "January 2026")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "A Message from Our Global Managing Partner"),
        ("2", "Anti-Bribery and Anti-Corruption"),
        ("3", "Gifts, Entertainment, and Hospitality"),
        ("4", "Conflicts of Interest"),
        ("5", "Confidentiality and Information Barriers"),
        ("6", "Whistleblower Protection and Reporting"),
        ("7", "Fair Competition and Antitrust"),
        ("8", "Social Media and Public Statements"),
        ("9", "Workplace Conduct and Anti-Harassment"),
        ("10", "Responsible AI and Technology Ethics"),
        ("11", "Personal Data Handling Responsibilities"),
        ("12", "Insider Trading and MNPI"),
        ("13", "Modern Slavery Awareness"),
        ("14", "Disciplinary Framework"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "A Message from Our Global Managing Partner")
    pdf.body_text(
        "Our reputation is our most valuable asset. Every interaction, every engagement, every decision made "
        "by any Meridian professional reflects on the entire firm. This Code of Conduct is not merely a "
        "compliance document -- it is a statement of who we are and how we choose to operate. It applies to "
        "every partner, employee, contractor, and anyone acting on behalf of Meridian & Associates LLP."
    )
    pdf.body_text(
        "I expect every professional to read this Code thoroughly, to complete the annual certification, "
        "and -- most importantly -- to live these principles every day. When in doubt, ask. When you see "
        "something that does not align with our values, speak up. Our culture depends on it."
    )

    pdf.section_heading("2", "Anti-Bribery and Anti-Corruption")
    pdf.body_text(
        "Meridian maintains a zero-tolerance policy toward bribery and corruption in all forms. We comply "
        "with the U.S. Foreign Corrupt Practices Act (FCPA), the UK Bribery Act 2010, and all applicable "
        "local anti-corruption laws in every jurisdiction where we operate."
    )
    pdf.bullet_list([
        "No Meridian professional may offer, promise, authorize, or pay any bribe, kickback, or improper "
        "payment to any person -- including government officials, clients, or private parties.",
        "Facilitating payments ('grease payments') are prohibited without exception, regardless of local "
        "custom or practice.",
        "All third-party agents, intermediaries, and joint venture partners must undergo anti-corruption "
        "due diligence and agree to Meridian's Anti-Corruption Compliance Addendum.",
        "Political contributions on behalf of the firm are prohibited. Personal political contributions "
        "are permitted but must be disclosed if they involve officials connected to firm clients.",
        "Annual FCPA/anti-corruption training is mandatory for all professionals. Completion rate "
        "in FY2025: 99.4%.",
    ])

    pdf.section_heading("3", "Gifts, Entertainment, and Hospitality")
    pdf.body_text(
        "Meridian recognizes that modest gifts and business hospitality are a normal part of professional "
        "relationships. However, they must never create an actual or perceived obligation or conflict."
    )
    pdf.bullet_list([
        "Receiving Gifts: Maximum value of $150 per item; $500 aggregate per source per calendar year. "
        "Cash and cash equivalents (gift cards, vouchers) are never permitted.",
        "Giving Gifts: Maximum value of $250 per item. Must be appropriate to the business context and "
        "compliant with the recipient's own policies.",
        "Entertainment: Business meals and events up to $300 per person are pre-approved. Events "
        "exceeding $300 per person require Ethics Office approval.",
        "Government Officials: Any gift or hospitality involving a government official or public sector "
        "client requires prior written approval from the Ethics Office regardless of value.",
        "Reporting: All gifts and entertainment exceeding $75 must be logged in the firm's Gift and "
        "Entertainment Registry within 5 business days.",
    ])

    pdf.section_heading("4", "Conflicts of Interest")
    pdf.body_text(
        "All Meridian professionals have a duty to avoid situations where personal interests could "
        "conflict, or appear to conflict, with the interests of the firm or our clients."
    )
    pdf.bullet_list([
        "Independence: Professionals on assurance engagements must comply with all applicable "
        "independence rules (AICPA, IESBA, SEC where applicable).",
        "Financial Interests: Professionals may not hold material financial interests in clients they "
        "serve or that the firm audits. All investment holdings are subject to annual disclosure and "
        "screening via the firm's Independence Compliance System.",
        "Outside Employment: Any outside employment, board membership, or advisory role requires "
        "prior written approval from the professional's service line leader and the Ethics Office.",
        "Personal Relationships: Professionals must disclose any close personal relationship with a "
        "client employee who is in a position to influence the engagement.",
        "Annual Disclosure: All professionals at the Senior Consultant level and above must complete "
        "an annual Conflict of Interest Disclosure questionnaire.",
    ])

    pdf.section_heading("5", "Confidentiality and Information Barriers")
    pdf.body_text(
        "Protecting client and firm confidential information is a fundamental obligation of every "
        "Meridian professional."
    )
    pdf.bullet_list([
        "Client information may only be used for the purpose for which it was provided and may not be "
        "shared with other clients, engagement teams, or external parties without explicit authorization.",
        "Information barriers ('ethical walls') are established when the firm serves clients with "
        "competing interests or when regulatory requirements mandate separation. Barrier compliance "
        "is monitored by the Conflicts Office.",
        "Clean desk and clear screen policies apply in all offices. Confidential documents must be "
        "secured when unattended.",
        "Use of client information in proposals, case studies, or marketing materials requires prior "
        "written consent from the client.",
        "Non-disclosure obligations survive engagement termination indefinitely unless a shorter period "
        "is specified in the engagement agreement.",
    ])

    pdf.section_heading("6", "Whistleblower Protection and Reporting")
    pdf.body_text(
        "Meridian encourages all professionals and external stakeholders to report concerns about "
        "unethical or illegal conduct without fear of retaliation."
    )
    pdf.bullet_list([
        "Ethics Hotline: Available 24/7 in 18 languages via phone (1-800-555-ETHX) and web "
        "(ethics.meridianllp.com). Operated by an independent third party (NAVEX Global).",
        "Anonymous Reporting: Reports may be made anonymously. The firm will investigate all credible "
        "reports regardless of whether the reporter identifies themselves.",
        "Non-Retaliation: Meridian strictly prohibits retaliation against anyone who reports a concern "
        "in good faith. Retaliation is itself a terminable offense.",
        "Investigation Process: All reports are reviewed by the Ethics & Compliance team within 48 "
        "hours. Investigations are conducted by trained investigators independent of the business unit "
        "involved. Findings are reported to the Ethics Committee.",
        "In FY2025, the Ethics Hotline received 312 reports. 100% were investigated; 67% were "
        "substantiated and resulted in remedial action.",
    ])

    pdf.section_heading("7", "Fair Competition and Antitrust")
    pdf.bullet_list([
        "Meridian competes vigorously but fairly in all markets. Agreements or understandings with "
        "competitors regarding pricing, market allocation, or bid rigging are strictly prohibited.",
        "Professionals must not exchange competitively sensitive information with competitors, whether "
        "in formal settings or informal conversations (e.g., industry conferences, social events).",
        "All professional association memberships and competitor interactions must be conducted in "
        "accordance with the firm's Antitrust Compliance Guidelines.",
    ])

    pdf.section_heading("8", "Social Media and Public Statements")
    pdf.bullet_list([
        "Only authorized spokespersons may make statements on behalf of Meridian to the media, "
        "analysts, or at public events.",
        "Personal social media use must not disclose confidential firm or client information, express "
        "views that could be attributed to the firm, or disparage clients, competitors, or colleagues.",
        "Professionals are encouraged to build their professional brand on platforms like LinkedIn but "
        "must identify views as their own and not those of Meridian.",
        "All thought leadership content (articles, blog posts, white papers) must be reviewed by the "
        "Communications team before publication.",
    ])

    pdf.section_heading("9", "Workplace Conduct and Anti-Harassment")
    pdf.body_text(
        "Meridian is committed to providing a workplace free from harassment, discrimination, and "
        "bullying of any kind. This applies to all interactions -- in-office, virtual, at client sites, "
        "and at firm-sponsored events."
    )
    pdf.bullet_list([
        "Zero tolerance for harassment based on race, color, religion, sex, sexual orientation, gender "
        "identity, national origin, disability, age, veteran status, or any other protected characteristic.",
        "All complaints are investigated promptly and thoroughly. Substantiated harassment results in "
        "disciplinary action up to and including termination.",
        "Mandatory anti-harassment training annually for all professionals; enhanced training for "
        "managers and partners.",
    ])

    pdf.section_heading("10", "Responsible AI and Technology Ethics")
    pdf.body_text(
        "As Meridian increasingly deploys artificial intelligence and generative AI (GenAI) tools in client "
        "engagements and internal operations, every professional must understand their responsibilities "
        "regarding the ethical use of these technologies."
    )
    pdf.bullet_list([
        "Permitted uses of GenAI: Research assistance, first-draft document generation, code development "
        "support, data analysis acceleration, and internal knowledge retrieval -- provided outputs are "
        "reviewed by a qualified human before delivery to clients or use in decision-making.",
        "Prohibited uses of GenAI: Inputting client confidential data into unapproved AI tools; using AI "
        "outputs as final work product without human review; relying on AI for audit opinions, legal "
        "advice, or regulatory filings without expert validation; using AI to generate misleading or "
        "fabricated content.",
        "Approved tools only: Professionals may only use AI tools that have been vetted and approved by "
        "the AI Governance Board (see the Approved AI Tools Registry on the firm intranet). Use of "
        "personal AI accounts (e.g., personal ChatGPT, Gemini, Claude accounts) for firm or client "
        "work is strictly prohibited.",
        "Transparency: When AI tools contribute materially to a client deliverable, this must be disclosed "
        "to the engagement partner and documented in the engagement file. Client consent is required "
        "where engagement terms mandate it.",
        "Bias awareness: All professionals using AI-assisted analytics or decision-support tools must "
        "complete the firm's Responsible AI Foundations training (mandatory annually) and must critically "
        "evaluate AI outputs for potential bias, hallucination, or error.",
    ])

    pdf.section_heading("11", "Personal Data Handling Responsibilities")
    pdf.body_text(
        "Every Meridian professional handles personal data in the course of their work -- whether client "
        "data, employee data, or third-party data. The following obligations apply to all staff regardless "
        "of role or seniority:"
    )
    pdf.bullet_list([
        "Need-to-know access: Only access personal data that is necessary for your specific role and "
        "current engagement. Do not browse, copy, or retain personal data beyond what is required.",
        "Secure handling: Personal data must be stored only in approved firm systems (never on personal "
        "devices, personal cloud storage, or USB drives). Encryption is mandatory for any transfer.",
        "Incident reporting: Any suspected or actual loss, theft, unauthorized access, or accidental "
        "disclosure of personal data must be reported to the Privacy Incident Response Team (PIRT) "
        "within 1 hour of discovery. Failure to report is itself a disciplinary matter.",
        "Retention and disposal: Follow the firm's Data Retention Schedule. Do not retain personal data "
        "beyond the approved period. Use approved disposal methods (cryptographic erasure, cross-cut "
        "shredding).",
        "Cross-border awareness: Before transferring personal data across national borders, confirm that "
        "an approved transfer mechanism is in place (SCCs, BCRs, adequacy decision). Contact the Privacy "
        "Office if uncertain.",
        "Training: Annual Data Privacy and Protection training is mandatory for all staff. Role-specific "
        "modules apply to HR, recruitment, and client-facing data analysts.",
    ])

    pdf.section_heading("12", "Insider Trading and MNPI")
    pdf.body_text(
        "In the course of serving clients, Meridian professionals may become aware of material nonpublic "
        "information (MNPI) -- information that, if made public, could affect the price of a client's "
        "securities. The misuse of MNPI is a serious criminal offense."
    )
    pdf.bullet_list([
        "Trading prohibition: No Meridian professional may trade in the securities of any company while in "
        "possession of MNPI about that company, regardless of how the information was obtained.",
        "Tipping prohibition: Passing MNPI to any other person -- including family members, friends, or "
        "colleagues not authorized to receive it -- is strictly prohibited (known as 'tipping').",
        "Restricted list: The Conflicts Office maintains a Restricted Securities List. Professionals must "
        "check this list and obtain pre-clearance before executing any personal securities trade.",
        "Information barriers: When the firm is engaged on transactions involving publicly traded "
        "securities (M&A, IPO advisory, due diligence), strict information barriers are established and "
        "monitored. Unauthorized disclosure across barriers is a terminable offense.",
        "Monitoring: The firm conducts automated surveillance of employee trading activity via its "
        "Independence Compliance System and reports anomalies to the Ethics Office.",
        "Training: Annual Insider Trading and MNPI training is mandatory for all professionals at the "
        "Consultant level and above. Enhanced training for professionals in M&A advisory, due diligence, "
        "and financial services engagements.",
    ])

    pdf.section_heading("13", "Modern Slavery Awareness")
    pdf.body_text(
        "Meridian is committed to preventing modern slavery and human trafficking in all its forms across "
        "our operations and supply chain, in accordance with the UK Modern Slavery Act 2015 and the "
        "Australian Modern Slavery Act 2018."
    )
    pdf.bullet_list([
        "Awareness obligation: Every professional must be alert to indicators of forced labor, debt "
        "bondage, human trafficking, and exploitative working conditions -- whether encountered in our "
        "supply chain, at client sites, or in the communities where we operate.",
        "Reporting: Any suspicion of modern slavery must be reported immediately via the Ethics Hotline "
        "or directly to the General Counsel's office. Reports may be made anonymously.",
        "Supply chain vigilance: Professionals involved in procurement decisions must ensure that the "
        "firm's Supplier Code of Conduct (which includes anti-slavery provisions) is incorporated into "
        "all new contracts and renewals above $100,000.",
        "Training: All professionals in procurement, HR, and facilities management roles must complete "
        "annual Modern Slavery Awareness training. General awareness is included in the annual Code of "
        "Conduct certification for all staff.",
        "Annual statement: Meridian publishes a Modern Slavery Statement annually, signed by the Global "
        "Managing Partner, detailing the steps taken to assess and mitigate modern slavery risks.",
    ])

    pdf.section_heading("14", "Disciplinary Framework")
    pdf.body_text(
        "Violations of this Code are taken seriously and addressed through a graduated disciplinary "
        "framework:"
    )
    pdf.bullet_list([
        "Level 1 -- Coaching and Counseling: For minor or first-time infractions. Documented in "
        "personnel file.",
        "Level 2 -- Formal Written Warning: For repeated minor infractions or moderate violations. "
        "May impact performance rating and compensation.",
        "Level 3 -- Suspension and Investigation: For serious violations. Professional placed on "
        "administrative leave pending investigation.",
        "Level 4 -- Termination: For egregious violations including fraud, bribery, sexual harassment, "
        "data breach caused by willful misconduct, or patterns of repeated violations.",
        "All disciplinary actions are reviewed by the Ethics Committee for consistency and fairness.",
    ])

    pdf.save("code_of_conduct.pdf")


# ---------------------------------------------------------------------------
# Document 9: Commercials and Legal Terms
# ---------------------------------------------------------------------------
def gen_commercials():
    pdf = FirmPDF("Commercial Terms and Legal Framework", "3.5", "February 2026")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "Master Services Agreement Overview"),
        ("2", "Fee Structures and Rate Cards"),
        ("3", "Liability and Indemnification"),
        ("4", "Intellectual Property"),
        ("5", "Insurance Coverage"),
        ("6", "Payment Terms"),
        ("7", "Term, Termination, and Transition"),
        ("8", "Dispute Resolution"),
        ("9", "Regulatory and Compliance Provisions"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "Master Services Agreement Overview")
    pdf.body_text(
        "Meridian & Associates LLP engages clients under a Master Services Agreement (MSA) supplemented "
        "by project-specific Statements of Work (SOWs). The MSA establishes the overarching legal and "
        "commercial framework, while each SOW defines scope, deliverables, timeline, team composition, "
        "and fees for individual engagements."
    )
    pdf.body_text(
        "This document summarizes the standard commercial and legal terms included in Meridian's MSA "
        "template (version 12.4, effective January 2026). Terms are subject to negotiation on a "
        "case-by-case basis, with deviations from standard terms requiring approval from the Office of "
        "General Counsel."
    )
    pdf.bullet_list([
        "MSA term: 3 years with automatic 1-year renewals unless either party provides 90 days' written "
        "notice of non-renewal.",
        "SOW execution: Each SOW must reference the MSA and be signed by authorized representatives "
        "of both parties.",
        "Change orders: Scope changes processed through a formal Change Order process with mutual "
        "written agreement on adjusted fees and timelines.",
        "Governing law: Specified per engagement (typically the jurisdiction where the majority of "
        "services are performed).",
    ])

    pdf.section_heading("2", "Fee Structures and Rate Cards")
    pdf.body_text(
        "Meridian offers flexible fee arrangements tailored to the nature and risk profile of each "
        "engagement:"
    )
    pdf.sub_heading("2.1", "Time and Materials")
    pdf.body_text(
        "Standard hourly rates by level (U.S. market, FY2026). Rates are adjusted by geography and "
        "service line. Offshore and nearshore delivery rates are 30-40% below onshore rates."
    )
    pdf.bullet_list([
        "Partner / Managing Director: $750 - $1,100 per hour",
        "Senior Director / Director: $550 - $750 per hour",
        "Senior Manager: $400 - $550 per hour",
        "Manager: $300 - $400 per hour",
        "Senior Consultant: $225 - $300 per hour",
        "Consultant: $175 - $225 per hour",
        "Analyst: $125 - $175 per hour",
    ])
    pdf.sub_heading("2.2", "Alternative Fee Arrangements")
    pdf.bullet_list([
        "Fixed Fee -- Agreed upon for well-defined scopes. Invoiced on a milestone basis.",
        "Capped Fee -- Time and materials with an agreed maximum. Provides cost certainty with "
        "flexibility for scope variation.",
        "Risk/Reward -- Base fee plus performance-based component tied to agreed KPIs or outcomes. "
        "Typically used for transformation engagements.",
        "Retainer -- Monthly or quarterly retainer for ongoing advisory relationships. Includes a "
        "specified number of hours/days with overage billed at agreed rates.",
        "Blended Rates -- Single blended rate for mixed-seniority teams. Commonly used for delivery "
        "center-based engagements.",
    ])
    pdf.sub_heading("2.3", "Rate Escalation")
    pdf.body_text(
        "Standard rate escalation is capped at 3% per annum, applied at each MSA anniversary. "
        "Multi-year fixed-fee engagements include escalation provisions in the SOW. Rate changes are "
        "communicated 60 days in advance."
    )

    pdf.section_heading("3", "Liability and Indemnification")
    pdf.sub_heading("3.1", "Limitation of Liability")
    pdf.bullet_list([
        "Aggregate Liability Cap: 2x the annual fees paid or payable under the applicable SOW in the "
        "12 months preceding the claim.",
        "Per-Incident Cap: 1x annual fees under the applicable SOW.",
        "Exclusions from Cap: Fraud, willful misconduct, gross negligence, breaches of "
        "confidentiality, IP infringement indemnity, and data breach indemnity are carved out from "
        "the liability cap.",
        "Consequential Damages: Neither party is liable for indirect, incidental, consequential, "
        "special, or punitive damages, except in cases of fraud, willful misconduct, or breach of "
        "confidentiality.",
    ])
    pdf.sub_heading("3.2", "Indemnification")
    pdf.bullet_list([
        "Meridian indemnifies the client against third-party claims arising from: (a) IP infringement "
        "by Meridian deliverables, (b) Meridian's negligent acts or omissions, (c) breach of applicable "
        "data protection laws attributable to Meridian.",
        "Client indemnifies Meridian against third-party claims arising from: (a) client-provided "
        "materials, data, or instructions, (b) client's use of deliverables outside the agreed scope.",
        "Indemnification Procedures: Prompt written notice, sole control of defense by indemnifying "
        "party, reasonable cooperation by indemnified party.",
    ])

    pdf.section_heading("4", "Intellectual Property")
    pdf.bullet_list([
        "Client Deliverables: Upon full payment, the client receives ownership of all bespoke "
        "deliverables created specifically for the engagement (work product).",
        "Pre-Existing IP: Meridian retains ownership of all pre-existing intellectual property, "
        "methodologies, tools, frameworks, and software (collectively, 'Meridian IP'). Client receives "
        "a non-exclusive, royalty-free license to use embedded Meridian IP solely as part of the "
        "delivered work product.",
        "Knowledge and Expertise: Meridian retains the right to use general knowledge, skills, "
        "experience, techniques, and ideas gained during the engagement.",
        "Open Source: Any open source components included in deliverables are disclosed in a Bill of "
        "Materials with applicable licenses identified.",
    ])

    pdf.section_heading("5", "Insurance Coverage")
    pdf.body_text(
        "Meridian maintains comprehensive insurance coverage through a program placed with A-rated (AM "
        "Best) carriers:"
    )
    pdf.bullet_list([
        "Professional Liability (Errors & Omissions): $100 million per occurrence / $200 million "
        "aggregate. Covers professional negligence, errors, or omissions in service delivery.",
        "Cyber Liability and Technology E&O: $50 million per occurrence / $100 million aggregate. "
        "Covers data breaches, cyber incidents, technology failures, and regulatory defense costs.",
        "Commercial General Liability: $25 million per occurrence / $50 million aggregate. Covers "
        "bodily injury, property damage, and personal/advertising injury.",
        "Workers' Compensation: Statutory limits in all jurisdictions.",
        "Employment Practices Liability: $25 million per occurrence / $50 million aggregate.",
        "Directors & Officers Liability: $50 million per occurrence.",
        "Crime / Fidelity: $10 million per occurrence.",
        "Umbrella / Excess: $100 million aggregate over primary layers.",
    ])
    pdf.body_text(
        "Certificates of Insurance are provided upon request. Additional insured status and waiver of "
        "subrogation are available for specific clients as endorsements."
    )

    pdf.section_heading("6", "Payment Terms")
    pdf.bullet_list([
        "Standard Payment Terms: Net 30 days from invoice date.",
        "Invoicing Frequency: Monthly in arrears for T&M engagements. Milestone-based for fixed-fee "
        "engagements.",
        "Late Payment: Interest at 1.5% per month (or the maximum permitted by law, whichever is "
        "lower) on overdue balances.",
        "Expenses: Reasonable travel and out-of-pocket expenses invoiced at cost, subject to the "
        "firm's travel policy and agreed expense caps.",
        "Currency: Invoiced in the local currency of the primary engagement location unless otherwise "
        "agreed. Multi-currency arrangements available for global programs.",
        "Electronic Invoicing: Meridian supports all major e-invoicing formats (Ariba, Coupa, Tungsten, "
        "Taulia, EDI 810) and can onboard to client-specific procurement platforms.",
    ])

    pdf.section_heading("7", "Term, Termination, and Transition")
    pdf.bullet_list([
        "Termination for Convenience: Either party may terminate an SOW with 30 days' written notice. "
        "Client pays for work completed and non-cancellable expenses incurred through the termination "
        "date.",
        "Termination for Cause: Either party may terminate immediately upon material breach that "
        "remains uncured for 30 days after written notice.",
        "Transition Assistance: Upon termination, Meridian will provide up to 90 days of transition "
        "assistance at agreed rates to ensure orderly handover of work product, knowledge transfer, "
        "and data migration.",
        "Data Return/Destruction: Within 30 days of engagement completion or termination, all client "
        "data will be returned or destroyed per the client's instruction, with a certification of "
        "destruction provided.",
    ])

    pdf.section_heading("8", "Dispute Resolution")
    pdf.bullet_list([
        "Step 1 -- Executive Escalation: Disputes escalated to senior leadership (Engagement Partner "
        "and client executive sponsor) for good-faith resolution within 15 business days.",
        "Step 2 -- Mediation: If unresolved, parties agree to mediation administered by JAMS under its "
        "mediation rules. Costs shared equally.",
        "Step 3 -- Arbitration: If mediation fails within 45 days, disputes are resolved by binding "
        "arbitration administered by JAMS under its Comprehensive Arbitration Rules. Single arbitrator "
        "for claims under $5M; three-arbitrator panel for claims $5M and above.",
        "Injunctive Relief: Either party may seek injunctive relief from a court of competent "
        "jurisdiction for breaches of confidentiality or IP provisions.",
    ])

    pdf.section_heading("9", "Regulatory and Compliance Provisions")
    pdf.bullet_list([
        "Anti-Corruption: Both parties warrant compliance with the FCPA, UK Bribery Act, and "
        "applicable local anti-corruption laws.",
        "Sanctions: Meridian complies with all applicable economic sanctions and export control laws "
        "(OFAC, EU, UN). Screening performed for all new clients and engagements.",
        "Modern Slavery: Meridian's Modern Slavery Statement is published annually in accordance with "
        "the UK Modern Slavery Act 2015 and Australian Modern Slavery Act 2018.",
        "Right to Audit: Client has the right to audit Meridian's compliance with the terms of the "
        "MSA upon 30 days' written notice, no more than once per calendar year, during business hours.",
    ])

    pdf.save("commercials_and_legal_terms.pdf")


# ---------------------------------------------------------------------------
# Document 10: Global Delivery Network
# ---------------------------------------------------------------------------
def gen_delivery_network():
    pdf = FirmPDF("Global Delivery Network", "2.5", "January 2026")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "Delivery Network Overview"),
        ("2", "Nearshore Delivery Centers"),
        ("3", "Offshore Delivery Centers"),
        ("4", "Blended Rate Model and Cost Savings"),
        ("5", "Quality Assurance Framework"),
        ("6", "Follow-the-Sun Operating Model"),
        ("7", "Data Sovereignty and Regulatory Controls"),
        ("8", "Talent and Capability Profile"),
        ("9", "Scalability and Surge Capacity"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "Delivery Network Overview")
    pdf.body_text(
        "Meridian's Global Delivery Network (GDN) comprises 11 delivery centers across 6 countries, "
        "employing over 14,000 professionals who provide scalable, cost-effective, and high-quality "
        "service delivery to clients worldwide. The GDN is a core strategic asset that enables Meridian "
        "to offer blended delivery models combining onshore expertise with nearshore and offshore "
        "capacity, delivering savings of 30-40% compared to fully onshore delivery without compromising "
        "quality or security."
    )
    pdf.body_text(
        "The GDN operates as an integrated extension of our onshore teams, sharing the same "
        "methodologies, quality standards, security protocols, and career development frameworks. Every "
        "delivery center is ISO 27001 certified and operates under Meridian's global Information "
        "Security Policy and Data Privacy Policy."
    )

    pdf.section_heading("2", "Nearshore Delivery Centers")
    pdf.body_text(
        "Nearshore centers provide time-zone-aligned delivery for Americas and European clients, "
        "combining cost efficiency with real-time collaboration capabilities."
    )
    pdf.sub_heading("2.1", "San Jose, Costa Rica")
    pdf.bullet_list([
        "Established: 2016. Headcount: 1,400 professionals.",
        "Time zone: CST (UTC-6) -- aligned with U.S. Eastern and Central time zones.",
        "Capabilities: Application development, cloud engineering, data analytics, cybersecurity "
        "operations, service desk (English and Spanish bilingual).",
        "Certifications: ISO 27001, SOC 2 Type II, CMMI Level 5.",
        "Key advantage: 1-2 hour time zone overlap with all U.S. time zones; strong bilingual "
        "talent pool; stable business environment ranked #1 in Latin America for ease of doing business.",
    ])
    pdf.sub_heading("2.2", "Warsaw, Poland")
    pdf.bullet_list([
        "Established: 2018 (expanded 2024). Headcount: 1,800 professionals.",
        "Time zone: CET (UTC+1) -- aligned with Western European clients.",
        "Capabilities: Cloud migration (AWS, Azure, GCP), data engineering, SAP, ServiceNow, "
        "RPA/intelligent automation, cybersecurity, financial advisory support.",
        "Certifications: ISO 27001, SOC 2 Type II, ISO 22301.",
        "Key advantage: EU data residency compliance; access to deep STEM talent pool from 20+ Polish "
        "technical universities; multilingual (Polish, English, German, French common).",
    ])
    pdf.sub_heading("2.3", "Bucharest, Romania")
    pdf.bullet_list([
        "Established: 2020. Headcount: 1,200 professionals.",
        "Time zone: EET (UTC+2) -- serves both Western and Eastern European clients.",
        "Capabilities: Software engineering, QA/testing, data science and ML engineering, DevOps, "
        "technical documentation.",
        "Certifications: ISO 27001, SOC 2 Type II.",
        "Key advantage: Competitive cost structure (20-25% below Warsaw); strong engineering talent; "
        "EU membership ensuring data sovereignty compliance.",
    ])

    pdf.sub_heading("2.4", "Cluj-Napoca, Romania")
    pdf.bullet_list([
        "Established: 2023. Headcount: 150 professionals.",
        "Time zone: EET (UTC+2) -- complements Bucharest operations.",
        "Capabilities: Software engineering, automated testing, DevSecOps, data pipeline development.",
        "Certifications: ISO 27001, SOC 2 Type II.",
        "Key advantage: Access to strong technical university talent pool (Babes-Bolyai University, "
        "Technical University of Cluj-Napoca); supplements Bucharest capacity for EU-compliant delivery.",
    ])
    pdf.sub_heading("2.5", "Guadalajara, Mexico")
    pdf.bullet_list([
        "Established: 2024. Headcount: 100 professionals.",
        "Time zone: CST (UTC-6) -- aligned with U.S. Central and Mountain time zones.",
        "Capabilities: Application development, cloud engineering, data analytics, bilingual service desk "
        "(English and Spanish).",
        "Certifications: ISO 27001 (in progress; expected Q2 2026).",
        "Key advantage: Strong STEM talent from Universidad de Guadalajara and ITESO; nearshore "
        "alternative to Costa Rica with competitive cost structure; supports growing Latin American client base.",
    ])

    pdf.section_heading("3", "Offshore Delivery Centers")
    pdf.body_text(
        "Offshore centers provide maximum cost efficiency and access to deep talent pools for large-scale "
        "delivery programs."
    )
    pdf.sub_heading("3.1", "India -- Bangalore")
    pdf.bullet_list([
        "Established: 2008. Headcount: 3,400 professionals (largest delivery center).",
        "Capabilities: Full-stack development, enterprise platform implementation (SAP, Salesforce, "
        "Workday, Oracle), data engineering, AI/ML, cloud infrastructure, testing/QA.",
        "Certifications: ISO 27001, SOC 2 Type II, CMMI Level 5, ISO 20000.",
        "Specializations: Center of Excellence for SAP S/4HANA and Data & AI.",
    ])
    pdf.sub_heading("3.2", "India -- Hyderabad")
    pdf.bullet_list([
        "Established: 2012. Headcount: 2,200 professionals.",
        "Capabilities: Cybersecurity operations (managed SOC), infrastructure managed services, "
        "application support, ERP managed services, cloud operations.",
        "Certifications: ISO 27001, SOC 2 Type II, ISO 20000, PCI DSS.",
        "Specializations: Center of Excellence for Managed Security Services and Cloud Operations.",
    ])
    pdf.sub_heading("3.3", "India -- Chennai")
    pdf.bullet_list([
        "Established: 2014. Headcount: 1,800 professionals.",
        "Capabilities: Finance and accounting operations, regulatory technology, risk analytics, "
        "internal audit support, testing and quality assurance.",
        "Certifications: ISO 27001, SOC 2 Type II.",
        "Specializations: Center of Excellence for Financial Services delivery and RegTech.",
    ])
    pdf.sub_heading("3.4", "Philippines -- Manila")
    pdf.bullet_list([
        "Established: 2017. Headcount: 1,600 professionals.",
        "Capabilities: Business process operations, customer experience, content management, "
        "healthcare revenue cycle, finance and accounting, HR operations.",
        "Certifications: ISO 27001, SOC 2 Type II, HITRUST (healthcare operations).",
        "Key advantage: Native English proficiency; strong cultural alignment with U.S. and "
        "Australian clients; competitive cost (35-40% below onshore).",
    ])
    pdf.sub_heading("3.5", "India -- Pune")
    pdf.bullet_list([
        "Established: 2022. Headcount: 200 professionals.",
        "Capabilities: Cloud-native application development, microservices architecture, API engineering, "
        "and mobile development.",
        "Certifications: ISO 27001, SOC 2 Type II.",
        "Specializations: Emerging technology incubator for cloud-native and edge computing solutions; "
        "supplements Bangalore capacity for high-demand technology engagements.",
    ])
    pdf.sub_heading("3.6", "Philippines -- Cebu")
    pdf.bullet_list([
        "Established: 2023. Headcount: 150 professionals.",
        "Capabilities: Business process operations, document processing, data entry and validation, "
        "quality assurance, customer support operations.",
        "Certifications: ISO 27001 (in progress; expected Q3 2026).",
        "Key advantage: Lower cost structure than Manila (10-15% savings); strong English proficiency; "
        "growing IT talent pool from University of San Carlos and Cebu Institute of Technology.",
    ])

    pdf.section_heading("4", "Blended Rate Model and Cost Savings")
    pdf.body_text(
        "Meridian's blended delivery model combines onshore engagement leadership and client-facing "
        "expertise with nearshore and offshore delivery capacity. Typical blended ratios and savings:"
    )
    pdf.bullet_list([
        "Standard Blend (Advisory): 50% onshore / 20% nearshore / 30% offshore. Savings: 20-25% vs "
        "fully onshore.",
        "Optimized Blend (Technology Delivery): 25% onshore / 25% nearshore / 50% offshore. Savings: "
        "30-35% vs fully onshore.",
        "Maximum Efficiency Blend (Managed Services): 15% onshore / 15% nearshore / 70% offshore. "
        "Savings: 35-40% vs fully onshore.",
        "Nearshore Premium: Nearshore rates are typically 15-20% above offshore rates but 25-30% below "
        "onshore rates, offering a balanced value proposition.",
    ])
    pdf.body_text(
        "Blended rates are calculated transparently based on the team composition defined in each SOW. "
        "Clients receive visibility into the onshore/nearshore/offshore mix and can adjust the blend "
        "within agreed parameters to optimize for cost, time zone, or capability requirements."
    )

    pdf.section_heading("5", "Quality Assurance Framework")
    pdf.body_text(
        "All delivery centers operate under Meridian's unified Quality Assurance Framework (QAF), which "
        "ensures consistent delivery quality regardless of location:"
    )
    pdf.bullet_list([
        "Meridian Delivery Methodology -- Standardized delivery lifecycle (Initiate, Design, Build, "
        "Test, Deploy, Operate) with mandatory quality gates at each phase transition.",
        "Peer Reviews -- All deliverables undergo peer review by a qualified reviewer not on the "
        "engagement team. Code reviews are mandatory for all software deliverables.",
        "Quality Metrics -- Tracked monthly: defect density, on-time delivery rate (target: >95%), "
        "client satisfaction score (target: >4.5/5.0), rework rate (target: <5%).",
        "Independent Quality Audits -- Meridian's Quality Assurance team conducts random audits of "
        "10% of active engagements per quarter. Findings are reported to the Quality Steering Committee.",
        "Client Feedback -- Structured feedback collected at project milestones and engagement "
        "completion. Net Promoter Score (NPS) tracked quarterly (current: +62).",
        "Continuous Improvement -- Monthly quality review boards at each delivery center. Root cause "
        "analysis for all engagements scoring below 4.0/5.0 on client satisfaction.",
    ])

    pdf.section_heading("6", "Follow-the-Sun Operating Model")
    pdf.body_text(
        "Meridian's follow-the-sun model leverages the geographic distribution of our delivery centers "
        "to provide extended or continuous coverage:"
    )
    pdf.bullet_list([
        "Zone 1 -- Americas (Costa Rica, Mexico, onshore U.S./Canada): UTC-8 to UTC-5. Coverage: 7 AM - 8 PM ET.",
        "Zone 2 -- EMEA (Poland, Romania, onshore UK/Europe): UTC+0 to UTC+2. Coverage: 8 AM - 7 PM CET.",
        "Zone 3 -- APAC (India, Philippines, onshore Australia): UTC+5:30 to UTC+11. Coverage: "
        "8 AM - 8 PM IST.",
        "Combined coverage: Near-continuous 20+ hour operational window for development, support, and "
        "managed service engagements.",
        "Handoff Protocols: Standardized shift handoff procedures with documented work-in-progress "
        "status, blocking issues, and next actions. Average handoff time: 15 minutes.",
        "For 24/7 operations (managed SOC, critical production support): Full round-the-clock staffing "
        "with rotating shifts across all three zones.",
    ])

    pdf.section_heading("7", "Data Sovereignty and Regulatory Controls")
    pdf.body_text(
        "Meridian implements robust data sovereignty controls to ensure compliance with client and "
        "regulatory requirements:"
    )
    pdf.bullet_list([
        "Data Residency Guarantees -- Client data can be restricted to specific geographic regions. "
        "EU-only delivery available through Poland and Romania centers for GDPR-sensitive engagements.",
        "Network Segmentation -- Each client environment is logically isolated with dedicated virtual "
        "networks, access controls, and audit logging.",
        "Access Restrictions -- Geofencing capabilities restrict data access to approved delivery "
        "center locations. VPN with multi-factor authentication required for all remote access.",
        "Background Checks -- All delivery center staff undergo comprehensive background checks "
        "including criminal history, education verification, and employment history verification. "
        "Enhanced vetting (including credit and government clearance) for regulated industry clients.",
        "Regulatory Compliance -- Individual centers maintain additional certifications as required: "
        "HIPAA (for U.S. healthcare), PCI DSS (for payment card data), FedRAMP (for U.S. government), "
        "IRAP (for Australian government).",
    ])

    pdf.section_heading("8", "Talent and Capability Profile")
    pdf.body_text(
        "The GDN workforce comprises highly skilled professionals with strong technical and domain "
        "expertise:"
    )
    pdf.bullet_list([
        "Average experience: 6.8 years across the GDN.",
        "Advanced degrees: 42% hold master's degrees or above.",
        "Cloud certifications: 4,200+ across AWS, Azure, and GCP (including 380 Professional/Expert "
        "level).",
        "Agile certifications: 2,800+ (CSM, PSM, SAFe).",
        "Annual training investment: Average 120 hours per professional per year.",
        "Attrition rate: 11.2% (well below the industry average of 18-22% in delivery center markets).",
        "Internal mobility: 15% of GDN staff rotate to onshore client sites annually for knowledge "
        "transfer and career development.",
    ])

    pdf.section_heading("9", "Scalability and Surge Capacity")
    pdf.body_text(
        "The GDN is designed to scale rapidly in response to client demand:"
    )
    pdf.bullet_list([
        "Standard ramp-up: 50-100 additional professionals within 4-6 weeks for established capability "
        "areas.",
        "Rapid ramp-up: Up to 200 professionals within 8 weeks using pre-qualified bench resources "
        "and strategic staffing partnerships.",
        "Bench capacity: Approximately 800 professionals (6% of GDN headcount) are maintained on "
        "bench at any time, pre-trained in high-demand skill areas.",
        "Strategic staffing partners: Pre-qualified relationships with 8 staffing firms across India, "
        "Philippines, Poland, and Romania for surge capacity beyond bench.",
        "Facility headroom: All delivery centers operate at 70-80% physical capacity, with expansion "
        "space available for 20-30% growth without new facility buildout.",
        "Maximum demonstrated ramp: 350 professionals onboarded in 10 weeks for a global financial "
        "services client's cloud migration program (2024).",
    ])

    pdf.save("global_delivery_network.pdf")


# ---------------------------------------------------------------------------
# Document 11: AI Governance & Responsible Technology Policy
# ---------------------------------------------------------------------------
def gen_ai_governance():
    pdf = FirmPDF("AI Governance & Responsible Technology Policy", "1.0", "February 2026")
    pdf.cover_page()
    pdf.add_toc([
        ("1", "AI Ethics Framework and Principles"),
        ("2", "Generative AI Acceptable Use Policy"),
        ("3", "Client Data Protection in AI Systems"),
        ("4", "Model Risk Management Framework"),
        ("5", "Algorithmic Bias Monitoring and Fairness"),
        ("6", "AI Output Review Requirements"),
        ("7", "Third-Party AI Tool Vetting"),
        ("8", "AI-Specific Incident Response"),
        ("9", "Governance Structure"),
        ("10", "Training Requirements"),
    ])

    pdf.add_page()
    pdf.section_heading("1", "AI Ethics Framework and Principles")
    pdf.body_text(
        "Meridian & Associates LLP recognizes that artificial intelligence and machine learning technologies "
        "present both transformative opportunities and significant risks. This policy establishes the firm's "
        "framework for the responsible development, deployment, and use of AI systems across all service "
        "lines, internal operations, and client engagements. It applies to all partners, employees, "
        "contractors, and third parties acting on behalf of Meridian."
    )
    pdf.body_text(
        "Meridian's Responsible AI Principles guide all AI-related activities:"
    )
    pdf.bullet_list([
        "Beneficence -- AI systems must be designed and deployed to create genuine value for clients, "
        "employees, and society. AI should augment human capabilities, not replace human judgment in "
        "contexts requiring ethical reasoning, empathy, or professional skepticism.",
        "Transparency -- Clients, regulators, and affected individuals must be able to understand how "
        "AI systems influence decisions that affect them. Meridian discloses AI use in client "
        "deliverables where material.",
        "Fairness -- AI systems must not discriminate against individuals or groups based on protected "
        "characteristics. Outputs must be regularly tested for disparate impact.",
        "Accountability -- Every AI system deployed at Meridian must have a designated human owner "
        "who is accountable for its outputs, performance, and compliance.",
        "Privacy -- AI systems must respect data protection rights. Personal data is never used for "
        "model training without explicit consent and lawful basis.",
        "Safety and Reliability -- AI systems must be tested rigorously before deployment. Failure modes "
        "must be understood, documented, and mitigated.",
        "Security -- AI systems must be protected against adversarial attacks, data poisoning, prompt "
        "injection, and model theft.",
    ])

    pdf.section_heading("2", "Generative AI Acceptable Use Policy")
    pdf.body_text(
        "The following guidelines govern the use of generative AI (GenAI) tools -- including large language "
        "models, image generators, and code generation systems -- by all Meridian professionals:"
    )
    pdf.sub_heading("2.1", "Permitted Uses")
    pdf.bullet_list([
        "Internal research, brainstorming, and ideation support using approved tools only.",
        "First-draft generation for internal documents, proposals, and communications (subject to human "
        "review before distribution).",
        "Code development assistance (code completion, refactoring suggestions, test generation) using "
        "approved IDE-integrated tools.",
        "Data analysis acceleration (summarization, pattern identification, visualization) on non-"
        "confidential or appropriately classified data.",
        "Translation and language assistance for internal and client communications.",
        "Knowledge retrieval from Meridian's proprietary knowledge bases via MeridianAI.",
    ])
    pdf.sub_heading("2.2", "Prohibited Uses")
    pdf.bullet_list([
        "Inputting client confidential, restricted, or personal data into any AI tool not on the "
        "Approved AI Tools Registry -- including personal accounts for ChatGPT, Gemini, Claude, "
        "Copilot, or any other public GenAI service.",
        "Using AI-generated outputs as final work product delivered to clients without qualified "
        "human review and validation.",
        "Relying on AI for audit opinions, legal advice, tax computations, regulatory filings, or any "
        "deliverable requiring professional certification or sign-off.",
        "Using AI to generate content intended to deceive, mislead, or fabricate information.",
        "Using AI to circumvent security controls, access restrictions, or compliance policies.",
        "Using AI to make or materially influence employment, promotion, or compensation decisions "
        "without meaningful human oversight.",
        "Using AI-generated code in production environments without security review and testing.",
    ])

    pdf.section_heading("3", "Client Data Protection in AI Systems")
    pdf.body_text(
        "Protecting client data is paramount in all AI deployments. The following controls are mandatory:"
    )
    pdf.bullet_list([
        "No client data in training: Client data is never used to train, fine-tune, or improve any "
        "AI/ML model -- whether proprietary or third-party. This is an absolute prohibition enforced "
        "through technical controls (data classification enforcement, training pipeline isolation) and "
        "contractual terms with all AI vendors.",
        "Opt-in policy: Clients must provide explicit written consent before their engagement data is "
        "processed by any AI system beyond basic search and retrieval. Consent is documented in the "
        "engagement letter or a supplemental AI processing addendum.",
        "Data minimization: Only the minimum data necessary for the specific AI task is provided to the "
        "system. PII is redacted or pseudonymized wherever technically feasible.",
        "Ephemeral processing: Client data processed by AI systems for inference is not persisted "
        "beyond the active session. No client data is retained in AI system logs, caches, or "
        "vector stores beyond 24 hours.",
        "Data residency: AI processing of client data respects all data residency requirements specified "
        "in the engagement agreement. Regional AI deployment options available for EU, UK, APAC, and "
        "U.S.-only processing.",
        "Vendor contractual controls: All AI vendor contracts include explicit prohibitions on using "
        "client data for model training, improvement, or any purpose beyond the contracted inference "
        "service. Verified annually through vendor audit or SOC 2 review.",
    ])

    pdf.section_heading("4", "Model Risk Management Framework")
    pdf.body_text(
        "Meridian applies a risk-based approach to AI/ML model governance, aligned with the principles of "
        "SR 11-7 (OCC/Fed model risk management guidance) and adapted for professional services context:"
    )
    pdf.sub_heading("4.1", "Model Classification")
    pdf.bullet_list([
        "Tier 1 -- High Risk: Models whose outputs directly influence client deliverables, financial "
        "decisions, regulatory outcomes, or hiring/promotion decisions. Subject to full validation "
        "cycle, independent review, and annual re-validation.",
        "Tier 2 -- Medium Risk: Models used for internal analytics, resource planning, or quality "
        "assurance. Subject to initial validation and biennial review.",
        "Tier 3 -- Low Risk: Models used for productivity assistance (summarization, translation, "
        "code completion). Subject to initial assessment and periodic spot checks.",
    ])
    pdf.sub_heading("4.2", "Model Lifecycle Controls")
    pdf.bullet_list([
        "Model Registry: All AI/ML models in use across the firm are cataloged in a central Model "
        "Registry with metadata including: purpose, owner, data inputs, known limitations, risk tier, "
        "validation status, and deployment environment.",
        "Development standards: All proprietary models developed using Meridian's ML Engineering "
        "Standards, which mandate version control, reproducibility, documentation, and peer review.",
        "Validation: Independent validation by the AI Risk team (separate from the model development "
        "team) for all Tier 1 and Tier 2 models. Validation covers: conceptual soundness, data quality, "
        "performance metrics, limitations analysis, and ongoing monitoring plan.",
        "Monitoring: Production models monitored for data drift, performance degradation, and anomalous "
        "outputs. Automated alerts trigger review when metrics exceed defined thresholds.",
        "Retirement: Documented decommissioning process including stakeholder notification, archival of "
        "model artifacts, and transition plan for dependent processes.",
    ])

    pdf.section_heading("5", "Algorithmic Bias Monitoring and Fairness")
    pdf.body_text(
        "Meridian is committed to ensuring that AI systems do not perpetuate or amplify unfair bias. "
        "The following requirements apply to all AI systems that produce outputs affecting individuals:"
    )
    pdf.bullet_list([
        "Pre-deployment testing: All Tier 1 models undergo fairness testing before deployment, analyzing "
        "outputs across protected characteristics (race, gender, age, disability, etc.) where applicable. "
        "Fairness metrics include demographic parity, equalized odds, and calibration across subgroups.",
        "Ongoing monitoring: Production models with human-impacting outputs are monitored quarterly for "
        "disparate impact. Results reported to the AI Ethics Board.",
        "Training data audits: Data used to train or fine-tune proprietary models is audited for "
        "representational balance and potential sources of historical bias.",
        "Remediation: Models found to exhibit statistically significant bias are flagged for immediate "
        "review. Remediation options include: retraining with balanced data, algorithmic debiasing "
        "techniques, output adjustment, or model retirement.",
        "Client transparency: For client engagements where AI-assisted analytics or decision-support "
        "systems are delivered, fairness testing methodology and results are included in the deliverable "
        "documentation upon client request.",
        "External audit: Annual independent audit of the firm's highest-risk AI systems by a qualified "
        "external assessor. Results reported to the Board of Partners.",
    ])

    pdf.section_heading("6", "AI Output Review Requirements")
    pdf.body_text(
        "Meridian mandates human-in-the-loop review for all AI-generated or AI-assisted outputs that are "
        "delivered to clients or used in consequential decision-making:"
    )
    pdf.bullet_list([
        "Client deliverables: All AI-generated or AI-assisted content included in client deliverables "
        "must be reviewed and validated by a qualified professional before delivery. The reviewer must "
        "be competent in the subject matter and must attest that the output is accurate, appropriate, "
        "and free from hallucination or material error.",
        "Audit and assurance: AI tools may assist with data analysis, anomaly detection, and sampling in "
        "audit engagements, but all audit conclusions, opinions, and findings must be determined by "
        "qualified auditors exercising professional judgment. AI outputs in audit are treated as "
        "evidence to be evaluated, not as conclusions.",
        "Legal and regulatory: AI-generated legal analysis, regulatory interpretations, or tax "
        "computations must be reviewed by a licensed professional before use.",
        "Code and technology: AI-generated code must pass the same code review, security scanning "
        "(SAST/DAST), and testing standards as human-written code before production deployment.",
        "Internal decisions: AI-assisted recommendations for hiring, promotion, performance evaluation, "
        "or resource allocation must be reviewed by the responsible human decision-maker, who retains "
        "full authority to accept, modify, or reject the AI recommendation.",
        "Documentation: The use of AI in producing any deliverable must be documented in the engagement "
        "file, including the tools used, the nature of AI assistance, and the reviewer who validated "
        "the output.",
    ])

    pdf.section_heading("7", "Third-Party AI Tool Vetting")
    pdf.body_text(
        "All AI/ML tools and services from external vendors must undergo a formal assessment before "
        "approval for use within Meridian:"
    )
    pdf.bullet_list([
        "Assessment process: Requests for new AI tools are submitted to the AI Governance Board via the "
        "Technology Procurement Portal. Assessment includes: security review (InfoSec team), privacy "
        "review (Privacy Office), legal review (General Counsel), and ethical risk assessment (AI "
        "Ethics Board).",
        "Security requirements: SOC 2 Type II certification (or equivalent). Penetration test results "
        "within the last 12 months. Vulnerability disclosure policy. No training on customer data "
        "without explicit opt-in.",
        "Privacy requirements: GDPR/CCPA-compliant data processing terms. Clear disclosure of data "
        "flows, sub-processors, and retention policies. Data residency options compatible with "
        "Meridian's client requirements.",
        "Contractual requirements: Explicit prohibition on using Meridian or client data for model "
        "training. Right to audit. Breach notification within 24 hours. Data deletion upon termination.",
        "Ongoing monitoring: Approved tools are reassessed annually. Material changes to vendor terms "
        "of service, data practices, or security posture trigger interim review.",
        "Approved AI Tools Registry: Maintained on the firm intranet with current list of 34 approved "
        "AI tools and services, categorized by use case and data classification level.",
    ])

    pdf.section_heading("8", "AI-Specific Incident Response")
    pdf.body_text(
        "AI-related incidents require specialized response procedures in addition to the firm's general "
        "Incident Response framework:"
    )
    pdf.bullet_list([
        "Scope: AI-specific incidents include: AI-generated output that is materially incorrect and "
        "has been delivered to a client; discovery of bias in a deployed model; unauthorized data "
        "exposure through an AI system; prompt injection or adversarial manipulation; unintended "
        "disclosure of confidential information via AI-generated output.",
        "Reporting: AI incidents must be reported to both the IT Service Desk (for general tracking) "
        "and the AI Ethics Board (ai-ethics@meridianllp.com) within 2 hours of discovery.",
        "Containment: For AI output errors affecting client deliverables, the engagement partner is "
        "notified immediately. Affected outputs are recalled or corrected. Client notification per "
        "engagement terms.",
        "Investigation: Root cause analysis conducted by the AI Risk team in collaboration with "
        "the development/deployment team. Focus areas: data quality, model behavior, prompt "
        "engineering, human oversight adequacy.",
        "Remediation: Corrective actions may include: model retraining, guardrail adjustment, "
        "additional human review requirements, tool restriction, or vendor escalation.",
        "Tracking: All AI incidents logged in the firm's incident management system with dedicated "
        "AI incident category. Quarterly trend reports provided to the AI Ethics Board and CISO.",
        "FY2025 summary: 28 AI-related incidents reported; 23 classified as low severity (output "
        "quality); 5 classified as medium (data handling); zero classified as high; average "
        "resolution time: 3.2 business days.",
    ])

    pdf.section_heading("9", "Governance Structure")
    pdf.body_text(
        "Meridian's AI governance is led by dedicated leadership and oversight bodies:"
    )
    pdf.sub_heading("9.1", "Chief AI Officer")
    pdf.body_text(
        "Dr. Amara Osei serves as Meridian's Chief AI Officer (a dual role with Chief Data Officer), "
        "reporting to the CTO with a dotted line to the Global Managing Partner. The Chief AI Officer "
        "is responsible for AI strategy, governance policy, risk oversight, and the firm's AI research "
        "and innovation agenda."
    )
    pdf.sub_heading("9.2", "AI Ethics Board")
    pdf.bullet_list([
        "Composition: 12 members including the Chief AI Officer (Chair), CISO, General Counsel, Chief "
        "Risk Officer, DPO, representatives from each service line, and two external advisors (a "
        "computer science professor and a civil liberties attorney).",
        "Mandate: Approve the AI Governance Policy and material updates; review and approve Tier 1 AI "
        "use cases; adjudicate escalated ethical concerns; oversee fairness testing program; commission "
        "external AI audits.",
        "Meeting cadence: Monthly, with ad hoc sessions for urgent matters.",
        "Authority: The AI Ethics Board has the authority to suspend or prohibit any AI use case, tool, "
        "or vendor that does not comply with this policy, regardless of commercial impact.",
    ])
    pdf.sub_heading("9.3", "AI Risk Team")
    pdf.bullet_list([
        "18 dedicated professionals within Risk & Compliance responsible for: model validation, bias "
        "testing, AI incident investigation, and regulatory monitoring.",
        "Independent from AI development teams to ensure objectivity in validation and review.",
        "Reports to the Chief Risk Officer with functional reporting to the Chief AI Officer.",
    ])

    pdf.section_heading("10", "Training Requirements")
    pdf.body_text(
        "Meridian invests in comprehensive AI literacy and responsible AI training for all professionals:"
    )
    pdf.bullet_list([
        "Responsible AI Foundations (mandatory, all staff): Annual 2-hour module covering AI ethics "
        "principles, acceptable use policy, data protection in AI, and incident reporting. "
        "FY2025 completion rate: 96.8%.",
        "GenAI for Professionals (mandatory, all client-facing staff): 4-hour module on effective and "
        "responsible use of generative AI tools in client engagements. Includes hands-on exercises "
        "with approved tools and case studies on AI risks.",
        "AI Risk Management (mandatory, AI Risk team and model developers): 16-hour certification "
        "program covering model risk management, validation methodology, fairness testing, and "
        "regulatory landscape.",
        "AI for Leaders (mandatory, Director level and above): 3-hour executive module on AI strategy, "
        "governance obligations, and leadership accountability for AI decisions.",
        "Specialized modules: Available for specific roles including AI/ML engineering, prompt "
        "engineering, AI in audit, AI in legal services, and AI vendor management.",
        "Continuous learning: Monthly 'AI at Meridian' webinar series featuring internal practitioners, "
        "client case studies, and external guest speakers. Average attendance: 4,200 per session.",
    ])

    pdf.save("ai_governance_policy.pdf")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def _run_subdirectory_generators():
    """Run generate_pdfs.py in each knowledge_base subdirectory."""
    import subprocess
    import sys

    kb_dir = os.path.join(os.path.dirname(__file__), "knowledge_base")
    for subdir in sorted(os.listdir(kb_dir)):
        script = os.path.join(kb_dir, subdir, "generate_pdfs.py")
        if os.path.isfile(script):
            print(f"\n--- {subdir} ---")
            subprocess.run([sys.executable, script], cwd=os.path.dirname(script), check=True)


if __name__ == "__main__":
    print("Generating Meridian & Associates LLP knowledge base documents...")
    print("\n=== Common / Firm-Wide ===")
    gen_executive_summary()
    gen_global_footprint()
    gen_dei_policy()
    gen_esg_report()
    gen_infosec_overview()
    gen_data_privacy()
    gen_bcdr_plan()
    gen_code_of_conduct()
    gen_commercials()
    gen_delivery_network()
    gen_ai_governance()
    print("\n=== Subdirectory Generators ===")
    _run_subdirectory_generators()
    print("\nDone! All knowledge base documents generated.")
