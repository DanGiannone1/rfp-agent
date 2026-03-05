"""Generate 2 synthetic pricing framework PDFs for Meridian & Associates LLP."""

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
# 1. Cost Model Framework
# ============================================================================

def generate_cost_model():
    pdf = MeridianPDF(
        "Cost Modeling Framework",
        "Standard Pricing Methodology for Professional Services",
        confidential=True
    )
    pdf.cover_page(version="4.1", date="January 2026")

    pdf.add_page()
    pdf.section_heading("1. Purpose and Scope")
    pdf.body_text(
        "This document establishes Meridian & Associates LLP's standard cost modeling framework for "
        "pricing professional services engagements. It provides guidance on labor cost calculation, "
        "overhead allocation, margin targets, and fee presentation methods. All engagement partners "
        "and pricing managers are required to use this framework when developing fee proposals."
    )
    pdf.body_text(
        "The framework applies to all service lines -- Audit & Assurance, Tax Services, Advisory & "
        "Consulting, Risk Advisory, and Financial Advisory -- with service-line-specific adjustments "
        "noted where applicable. Pricing for managed services and recurring engagements follows "
        "supplementary guidelines in the Managed Services Pricing Addendum."
    )

    pdf.section_heading("2. Labor Categories and Standard Rates")
    pdf.body_text(
        "Meridian defines seven standard labor categories across all service lines. Each category has "
        "a standard billing rate (used for time-and-materials engagements) and a standard cost rate "
        "(used for internal cost modeling and fixed-fee estimation). Rates are updated annually "
        "effective January 1."
    )

    pdf.section_heading("FY2026 Standard Billing Rates (US Market)", level=2)
    pdf.bold_bullet("Partner / Managing Director", "$750 - $950 per hour (varies by service line and specialization)")
    pdf.bold_bullet("Senior Manager / Director", "$550 - $725 per hour")
    pdf.bold_bullet("Manager", "$425 - $575 per hour")
    pdf.bold_bullet("Senior Associate / Senior Consultant", "$325 - $450 per hour")
    pdf.bold_bullet("Associate / Staff", "$225 - $325 per hour")
    pdf.bold_bullet("Analyst / Junior Staff", "$175 - $250 per hour")
    pdf.bold_bullet("Administrative / Paraprofessional", "$125 - $175 per hour")

    pdf.section_heading("Rate Adjustments by Market", level=3)
    pdf.body_text(
        "Standard billing rates are adjusted based on the market in which services are delivered:"
    )
    pdf.bold_bullet("Tier 1 Markets (NYC, SF, London, Singapore)", "Standard rates as listed above")
    pdf.bold_bullet("Tier 2 Markets (Chicago, LA, DC, Boston, Frankfurt)", "95% of standard rates")
    pdf.bold_bullet("Tier 3 Markets (Denver, Dallas, Atlanta, other US metros)", "88% of standard rates")
    pdf.bold_bullet("Tier 4 Markets (smaller US metros, nearshore locations)", "80% of standard rates")
    pdf.bold_bullet("Offshore Delivery Centers (India, Philippines)", "45-55% of standard rates")

    pdf.section_heading("Rate Adjustments by Service Line", level=3)
    pdf.body_text("Within each labor category, rates vary by service line reflecting market positioning:")
    pdf.bold_bullet("Financial Advisory / M&A", "110-120% of base rate (premium for transaction advisory)")
    pdf.bold_bullet("Technology Consulting", "105-115% of base rate (premium for specialized skills)")
    pdf.bold_bullet("Cybersecurity Services", "110-125% of base rate (market scarcity premium)")
    pdf.bold_bullet("Tax Compliance", "90-95% of base rate (competitive market pressure)")
    pdf.bold_bullet("Government Audit", "85-90% of base rate (public sector pricing constraints)")

    pdf.add_page()
    pdf.section_heading("3. Cost Rate Calculation")
    pdf.body_text(
        "The internal cost rate represents the fully loaded cost of a professional hour, used for "
        "margin analysis and fixed-fee estimation. It includes direct compensation, benefits, and "
        "allocated overhead."
    )

    pdf.section_heading("Cost Rate Components", level=2)
    pdf.bold_bullet("Direct Compensation", "Base salary + performance bonus (target), annualized and divided by standard available hours (1,800 hours for US professionals)")
    pdf.bold_bullet("Benefits Load", "32% of direct compensation (health insurance, retirement contributions, payroll taxes, disability, life insurance)")
    pdf.bold_bullet("Facilities Allocation", "Per-capita allocation of office space, technology infrastructure, and utilities. FY2026: $18,400 per professional (Tier 1), $14,200 (Tier 2), $11,800 (Tier 3/4)")
    pdf.bold_bullet("Technology Allocation", "Per-capita allocation of software licenses, equipment, and IT support. FY2026: $8,400 per professional")
    pdf.bold_bullet("Training and Development", "Per-capita allocation of CPE, training programs, and professional development. FY2026: $4,200 per professional")
    pdf.bold_bullet("Insurance Allocation", "Professional liability insurance allocated per chargeable hour. FY2026: $12.50 per hour")
    pdf.bold_bullet("General and Administrative", "Corporate overhead (executive management, finance, HR, marketing, legal) allocated as 15% of direct compensation + benefits")

    pdf.section_heading("FY2026 Standard Cost Rates (US Tier 1 Market)", level=2)
    pdf.bold_bullet("Partner / Managing Director", "$385 - $480 per hour (fully loaded cost)")
    pdf.bold_bullet("Senior Manager / Director", "$265 - $345 per hour")
    pdf.bold_bullet("Manager", "$195 - $265 per hour")
    pdf.bold_bullet("Senior Associate / Senior Consultant", "$145 - $205 per hour")
    pdf.bold_bullet("Associate / Staff", "$105 - $155 per hour")
    pdf.bold_bullet("Analyst / Junior Staff", "$80 - $120 per hour")
    pdf.bold_bullet("Administrative / Paraprofessional", "$60 - $85 per hour")

    pdf.section_heading("Implied Standard Margins", level=3)
    pdf.body_text(
        "At standard billing rates and standard cost rates, the implied gross margin by labor category "
        "ranges from approximately 45% (Partner level) to 55% (Staff level). Blended engagement margins "
        "depend on the labor mix (pyramid) and typically fall in the 42-52% range at standard rates."
    )

    pdf.add_page()
    pdf.section_heading("4. Fixed-Fee Estimation Methodology")
    pdf.body_text(
        "For fixed-fee engagements, the cost model follows a bottom-up estimation approach:"
    )

    pdf.section_heading("Step 1: Scope Definition and Work Breakdown", level=2)
    pdf.body_text(
        "Define the engagement scope in sufficient detail to estimate effort. Break the scope into "
        "phases, workstreams, and activities. For each activity, identify the labor categories required "
        "and the estimated hours. Use historical data from comparable engagements (available in the "
        "Pricing Analytics Dashboard) to calibrate estimates."
    )

    pdf.section_heading("Step 2: Effort Estimation", level=2)
    pdf.body_text(
        "Estimate hours by labor category for each activity using one of three methods:"
    )
    pdf.bold_bullet("Analogous Estimation", "Based on actual hours from comparable prior engagements, adjusted for scope differences. Preferred method when good comparables exist.")
    pdf.bold_bullet("Parametric Estimation", "Based on productivity metrics (e.g., hours per entity audited, hours per tax return, hours per process redesigned). The Pricing Analytics Dashboard maintains productivity benchmarks by service line.")
    pdf.bold_bullet("Expert Judgment", "Senior practitioner estimates based on experience. Used for novel or highly customized engagements. Should include a contingency buffer of 10-15%.")

    pdf.section_heading("Step 3: Cost Calculation", level=2)
    pdf.body_text(
        "Multiply estimated hours by the applicable cost rate for each labor category. Add direct "
        "engagement expenses (travel, technology licenses, subcontractor costs). The result is the "
        "total estimated cost."
    )

    pdf.section_heading("Step 4: Margin Application", level=2)
    pdf.body_text(
        "Apply the target margin for the service line and engagement type (see Section 5). The fee "
        "is calculated as: Fee = Total Estimated Cost / (1 - Target Margin %)."
    )

    pdf.section_heading("Step 5: Competitive and Value Adjustment", level=2)
    pdf.body_text(
        "Adjust the calculated fee based on competitive intelligence, strategic value of the client, "
        "and the client's price sensitivity. This adjustment requires practice leader approval if it "
        "results in a margin below the floor (see Section 5)."
    )

    pdf.section_heading("Step 6: Risk Contingency", level=2)
    pdf.body_text(
        "For fixed-fee engagements, add an appropriate risk contingency to protect against scope creep "
        "and estimation uncertainty:"
    )
    pdf.bold_bullet("Low Risk", "5% contingency -- well-defined scope, strong comparable data, experienced team, repeat engagement")
    pdf.bold_bullet("Medium Risk", "10% contingency -- standard scope with some customization, reasonable comparable data")
    pdf.bold_bullet("High Risk", "15-20% contingency -- novel scope, limited comparable data, new client, complex dependencies")

    pdf.add_page()
    pdf.section_heading("5. Target Margins by Service Line")
    pdf.body_text(
        "The following target and floor margins apply to all new engagement pricing. Floor margins "
        "represent the absolute minimum acceptable margin and require Regional Managing Partner "
        "approval. Margins are calculated on a gross basis (fee less direct costs, before G&A allocation)."
    )

    pdf.section_heading("Audit & Assurance", level=2)
    pdf.bold_bullet("Target Margin", "40-45%")
    pdf.bold_bullet("Floor Margin", "32%")
    pdf.body_text("Note: Government and not-for-profit audit margins typically fall at the lower end of the range due to competitive pricing pressures and procurement constraints.")

    pdf.section_heading("Tax Services", level=2)
    pdf.bold_bullet("Target Margin (Compliance)", "35-42%")
    pdf.bold_bullet("Target Margin (Advisory/Planning)", "45-52%")
    pdf.bold_bullet("Floor Margin", "28%")
    pdf.body_text("Note: Tax compliance margins are typically lower due to competitive pressure and volume-based pricing. Tax advisory and planning engagements command premium margins due to specialized expertise and value delivered.")

    pdf.section_heading("Advisory & Consulting", level=2)
    pdf.bold_bullet("Target Margin (Strategy/Operations)", "48-55%")
    pdf.bold_bullet("Target Margin (Technology Consulting)", "45-52%")
    pdf.bold_bullet("Target Margin (Change Management)", "42-48%")
    pdf.bold_bullet("Floor Margin", "35%")
    pdf.body_text("Note: Advisory margins are the highest across the firm, reflecting the value-based nature of the work and the seniority of the labor mix.")

    pdf.section_heading("Risk Advisory", level=2)
    pdf.bold_bullet("Target Margin", "42-48%")
    pdf.bold_bullet("Floor Margin", "33%")

    pdf.section_heading("Financial Advisory / M&A", level=2)
    pdf.bold_bullet("Target Margin (Retainer/Hourly)", "50-58%")
    pdf.bold_bullet("Target Margin (Success Fee Component)", "65-75% (net of retainer credits)")
    pdf.bold_bullet("Floor Margin (Retainer/Hourly)", "38%")
    pdf.body_text("Note: Financial advisory engagements often include success fee components tied to transaction close. The blended margin including success fees is typically 55-65%.")

    pdf.add_page()
    pdf.section_heading("6. Expense Policy for Fee Proposals")
    pdf.body_text(
        "Engagement expenses should be handled consistently in all fee proposals:"
    )

    pdf.section_heading("Travel and Living Expenses", level=2)
    pdf.bullet("Fixed-fee engagements: Travel should be included in the fixed fee whenever possible, using estimated travel frequency and per-diem costs. This eliminates client surprise and simplifies billing.")
    pdf.bullet("T&M engagements: Travel billed at actual cost with no markup, subject to the firm's travel policy (economy air for flights under 5 hours, premium economy for longer flights, business class for international with partner approval)")
    pdf.bullet("Per-diem rates: Use GSA per-diem rates for US travel, OANDA for international travel")
    pdf.bullet("Remote delivery: Where possible, propose a blended on-site/remote model to reduce travel costs and demonstrate efficiency")

    pdf.section_heading("Technology and Tools", level=2)
    pdf.bullet("Firm-standard tools (Meridian Insight, TaxConnect, WorkStream) are included in the fee -- never charge separately")
    pdf.bullet("Third-party software licenses required for a specific engagement (e.g., specialized analytics tools, RPA licenses) should be included in the fee with client approval")
    pdf.bullet("Technology infrastructure (laptops, connectivity) is included in overhead -- never charge separately")

    pdf.section_heading("Subcontractor Costs", level=2)
    pdf.bullet("Subcontractor costs should be estimated and included in the total fee")
    pdf.bullet("Standard markup on subcontractor costs: 15-20%")
    pdf.bullet("For pass-through arrangements (client-directed subcontractors): no markup, bill at cost")

    pdf.section_heading("7. Fee Presentation Formats")
    pdf.body_text(
        "Fees should be presented in the format most appropriate for the client and engagement type:"
    )
    pdf.bold_bullet("Fixed Fee by Phase", "Preferred for project-based advisory work. Present a total fixed fee broken down by project phase. Provides client with clear cost and Meridian with scope management tool.")
    pdf.bold_bullet("Annual Fixed Fee", "Standard for recurring engagements (audit, tax compliance, managed services). Present as an annual fee with assumptions and scope definition.")
    pdf.bold_bullet("Time-and-Materials with Cap", "Appropriate when scope is uncertain. Present blended or category-specific rates with a not-to-exceed cap. Provides client with cost protection.")
    pdf.bold_bullet("Blended Rate", "Present a single blended hourly rate that incorporates all labor categories. Simplifies pricing but reduces transparency. Most appropriate for staff augmentation.")
    pdf.bold_bullet("Value-Based / Success Fee", "For engagements with clearly measurable outcomes (cost reduction, revenue improvement, transaction close). Present a base fee plus success fee tied to achieved results.")

    pdf.section_heading("8. Pricing Approval Requirements")
    pdf.body_text("All fee proposals require the following approvals before submission:")
    pdf.bold_bullet("Under $250K", "Engagement Partner approval")
    pdf.bold_bullet("$250K - $1M", "Engagement Partner + Practice Leader approval")
    pdf.bold_bullet("$1M - $5M", "Engagement Partner + Practice Leader + Regional Managing Partner approval")
    pdf.bold_bullet("Over $5M", "Engagement Partner + Practice Leader + Regional Managing Partner + Chief Operating Officer approval")
    pdf.bold_bullet("Below Floor Margin", "All of the above + CEO or Vice Chairman approval")
    pdf.body_text(
        "Pricing approval requests should be submitted through the Pursuit Approval System (PAS) in "
        "Meridian WorkStream at least 5 business days before the proposal submission deadline."
    )

    pdf.output(os.path.join(OUTPUT_DIR, "cost_model_framework.pdf"))
    print("  Created: cost_model_framework.pdf")


# ============================================================================
# 2. Discount and Margin Guidance
# ============================================================================

def generate_discount_guidance():
    pdf = MeridianPDF(
        "Discount Authority &\nMargin Guidance",
        "Competitive Pricing Decision Framework",
        confidential=True
    )
    pdf.cover_page(version="3.0", date="January 2026")

    pdf.add_page()
    pdf.section_heading("1. Purpose")
    pdf.body_text(
        "This document provides guidance on discount authority levels, competitive pricing strategies, "
        "and margin management for engagement pricing decisions. It complements the Cost Modeling "
        "Framework (see separate document) and is intended for use by engagement partners, practice "
        "leaders, and pricing managers."
    )
    pdf.body_text(
        "Meridian's pricing philosophy balances three objectives: (1) delivering fair value to clients, "
        "(2) maintaining margins that fund reinvestment in our people and capabilities, and (3) winning "
        "strategically important engagements. This framework provides structured decision-making tools "
        "to balance these objectives in competitive pursuit situations."
    )

    pdf.section_heading("2. Discount Authority Levels")
    pdf.body_text(
        "Discounts from standard billing rates or standard fixed-fee calculations are authorized "
        "at the following levels. All discounts must be documented in the Pursuit Approval System (PAS) "
        "with a business justification."
    )

    pdf.section_heading("2.1 Engagement Partner Authority", level=2)
    pdf.key_value("Maximum Discount from Standard Rates", "Up to 10%")
    pdf.key_value("Minimum Resulting Margin", "Must remain above service line floor margin")
    pdf.body_text("Conditions for Engagement Partner-level discounting:")
    pdf.bullet("Repeat client with demonstrated loyalty and growth potential")
    pdf.bullet("Multi-service relationship where cross-selling offsets the discount on a specific engagement")
    pdf.bullet("Competitive situation where intelligence indicates pricing is a key evaluation factor")
    pdf.bullet("Volume-based discount for large-scope engagements (50,000+ hours annually)")

    pdf.section_heading("2.2 Practice Leader Authority", level=2)
    pdf.key_value("Maximum Discount from Standard Rates", "Up to 20%")
    pdf.key_value("Minimum Resulting Margin", "Must remain above service line floor margin")
    pdf.body_text("Conditions requiring Practice Leader approval:")
    pdf.bullet("Discount exceeds 10% from standard rates")
    pdf.bullet("New client acquisition where penetration pricing is strategically justified")
    pdf.bullet("Competitive displacement of incumbent firm where pricing is decisive")
    pdf.bullet("Public sector engagements where rate schedules are subject to negotiation")

    pdf.section_heading("2.3 Regional Managing Partner Authority", level=2)
    pdf.key_value("Maximum Discount from Standard Rates", "Up to 30%")
    pdf.key_value("Minimum Resulting Margin", "May go to floor margin but not below")
    pdf.body_text("Conditions requiring Regional Managing Partner approval:")
    pdf.bullet("Discount exceeds 20% from standard rates")
    pdf.bullet("Strategic account pursuit designated by the Growth Office")
    pdf.bullet("Market entry pricing for new geography or industry vertical")
    pdf.bullet("Response to competitive pressure from Big Four or major boutique firms")

    pdf.add_page()
    pdf.section_heading("2.4 CEO / Vice Chairman Authority", level=2)
    pdf.key_value("Maximum Discount from Standard Rates", "Unlimited (subject to business case)")
    pdf.key_value("Minimum Resulting Margin", "May go below floor margin with documented justification")
    pdf.body_text("Conditions requiring CEO/Vice Chairman approval:")
    pdf.bullet("Pricing below the service line floor margin for any reason")
    pdf.bullet("Pro bono or significantly discounted work for nonprofit organizations")
    pdf.bullet("Loss-leader pricing for strategically critical accounts (requires 3-year profitability plan)")
    pdf.bullet("Government contracts with prescribed rate ceilings below standard rates")

    pdf.section_heading("3. Strategic Pricing Scenarios")
    pdf.body_text(
        "The following guidance addresses common competitive pricing scenarios and provides a framework "
        "for decision-making:"
    )

    pdf.section_heading("3.1 Incumbent Defense", level=2)
    pdf.body_text(
        "When defending an existing client relationship against competitive threat:"
    )
    pdf.bullet("Assess the true competitive threat: Is the client genuinely considering alternatives, or is this a negotiating tactic?")
    pdf.bullet("Lead with value reinforcement before offering rate concessions. Document the cumulative value delivered over the relationship.")
    pdf.bullet("If pricing adjustment is necessary, prefer volume-based or multi-year commitment discounts over straight rate reductions")
    pdf.bullet("Consider offering additional services at no incremental cost rather than reducing rates (protects rate integrity)")
    pdf.bullet("Authorized discount range: up to 15% with Practice Leader approval, documented in PAS")
    pdf.bullet("Critical rule: Never reduce rates below the point where quality or staffing would be compromised")

    pdf.section_heading("3.2 New Client Acquisition", level=2)
    pdf.body_text(
        "When pursuing a new client where pricing is a significant evaluation factor:"
    )
    pdf.bullet("Understand the client's budget range before finalizing pricing (ask during the pre-proposal meeting)")
    pdf.bullet("Consider a phased pricing approach: Year 1 at a penetration rate, with rate normalization in Years 2-3")
    pdf.bullet("Multi-year commitments justify lower Year 1 pricing -- ensure the total contract value meets margin targets")
    pdf.bullet("For strategic accounts, a below-target-margin Year 1 may be justified if cross-selling opportunities are identified and documented")
    pdf.bullet("Authorized discount range: up to 25% in Year 1 with Regional Managing Partner approval")
    pdf.bullet("Requirement: 3-year account profitability model demonstrating path to target margins")

    pdf.section_heading("3.3 Competitive Displacement", level=2)
    pdf.body_text(
        "When attempting to displace a competitor (typically Big Four or major regional firm):"
    )
    pdf.bullet("Price at or slightly below the incumbent's estimated fees (use market intelligence from the Growth Office)")
    pdf.bullet("Differentiate on value, team quality, and service model rather than price alone")
    pdf.bullet("Offer a transition guarantee: If defined transition milestones are not met, Meridian will credit a portion of transition fees")
    pdf.bullet("Consider 'risk-sharing' pricing models (e.g., base fee + performance bonus) that demonstrate confidence in outcomes")
    pdf.bullet("Authorized discount range: up to 20% with Practice Leader approval; up to 30% with Regional Managing Partner for strategic accounts")

    pdf.add_page()
    pdf.section_heading("3.4 Public Sector Pricing", level=2)
    pdf.body_text(
        "Public sector engagements have unique pricing considerations:"
    )
    pdf.bullet("Many public entities publish rate schedules or require rates within GSA Schedule ranges")
    pdf.bullet("Price evaluation often represents 30-40% of total evaluation score (vs. 15-25% for commercial clients)")
    pdf.bullet("Government rates should be developed as a separate rate card, not as discounts from commercial rates")
    pdf.bullet("Meridian's standard government rates are 85-90% of Tier 3 commercial rates")
    pdf.bullet("For federal contracts, ensure compliance with FAR cost accounting standards and Cost Accounting Standards (CAS)")
    pdf.bullet("For state and local contracts, review specific procurement regulations for rate disclosure requirements")

    pdf.section_heading("3.5 Multi-Service Bundle Pricing", level=2)
    pdf.body_text(
        "When proposing multiple service lines to a single client:"
    )
    pdf.bullet("Bundle discounts of 8-12% from the aggregate standard pricing are pre-authorized at the Engagement Partner level")
    pdf.bullet("Larger bundle discounts (up to 18%) are authorized at the Practice Leader level")
    pdf.bullet("The discount should be presented as a 'relationship benefit' rather than individual service line reductions")
    pdf.bullet("Each service line within the bundle must maintain its own floor margin")
    pdf.bullet("Cross-service synergies (shared understanding of client, reduced onboarding) genuinely reduce cost and can fund a portion of the discount")

    pdf.section_heading("4. Margin Protection Strategies")
    pdf.body_text(
        "When pricing pressure threatens target margins, consider these strategies before reducing fees:"
    )

    pdf.section_heading("4.1 Scope Optimization", level=2)
    pdf.bullet("Reduce scope to fit budget rather than reducing rates: 'We can deliver the full program at $X, or a focused Phase 1 at $Y'")
    pdf.bullet("Offer a tiered proposal with 'good/better/best' options at different price points")
    pdf.bullet("Shift lower-value activities to the client (e.g., data gathering, scheduling, document collection)")

    pdf.section_heading("4.2 Delivery Model Optimization", level=2)
    pdf.bullet("Increase offshore/nearshore delivery ratio to reduce blended cost (without reducing client-facing quality)")
    pdf.bullet("Use junior staff for appropriate tasks under senior supervision (steeper pyramid)")
    pdf.bullet("Implement automation and accelerators to reduce total hours while maintaining quality")
    pdf.bullet("Propose a blended on-site/remote model (e.g., 3 days on-site, 2 remote) to reduce travel costs")

    pdf.section_heading("4.3 Fee Structure Innovation", level=2)
    pdf.bullet("Propose outcome-based pricing: lower base fee with upside tied to achieved results")
    pdf.bullet("Offer gainsharing arrangements for cost reduction engagements (Meridian shares in the savings)")
    pdf.bullet("Use milestone-based payments to improve cash flow and reduce client risk perception")
    pdf.bullet("Multi-year contracts with early payment discounts (e.g., 2% discount for payment within 15 days)")

    pdf.add_page()
    pdf.section_heading("5. Competitive Intelligence Guidelines")
    pdf.body_text(
        "Effective pricing requires understanding the competitive landscape. The Growth Office maintains "
        "competitive intelligence on market rates and pricing trends:"
    )
    pdf.section_heading("Available Resources", level=2)
    pdf.bullet("Annual Rate Benchmarking Study: Comprehensive analysis of billing rates across the Top 20 professional services firms (updated February of each year)")
    pdf.bullet("Win/Loss Pricing Analysis: Database of pricing outcomes from all pursuits > $250K, including evaluator feedback on price competitiveness")
    pdf.bullet("Competitive Rate Cards: Estimated rate ranges for major competitors by service line and market tier")
    pdf.bullet("Public Sector Pricing Database: Rates from publicly available government contracts and GSA Schedules for major competitors")
    pdf.bullet("Industry Pricing Surveys: Third-party surveys from Source Global Research, ALM Intelligence, and Kennedy Consulting Research")

    pdf.section_heading("Intelligence Ethics", level=2)
    pdf.body_text(
        "All competitive intelligence must be gathered through ethical and legal means. The following "
        "are strictly prohibited:"
    )
    pdf.bullet("Soliciting specific pricing information from competitor employees or former competitor employees")
    pdf.bullet("Using client-provided competitor proposals for pricing intelligence (unless the client has explicitly authorized sharing)")
    pdf.bullet("Misrepresenting identity or affiliation to gather competitor information")
    pdf.bullet("Using proprietary competitor information obtained through any unauthorized means")

    pdf.section_heading("6. Annual Rate Review Process")
    pdf.body_text(
        "Standard billing rates and cost rates are reviewed and updated annually through the following process:"
    )
    pdf.bullet("September: Compensation Committee sets preliminary compensation ranges for the upcoming fiscal year")
    pdf.bullet("October: Finance calculates updated cost rates based on new compensation, benefits, and overhead projections")
    pdf.bullet("November: Growth Office conducts competitive rate benchmarking analysis")
    pdf.bullet("December: Pricing Committee (COO, practice leaders, CFO) sets standard billing rates for the upcoming year")
    pdf.bullet("January 1: New rates take effect for all new engagement letters and T&M billing")
    pdf.bullet("Existing fixed-fee contracts: Rate changes apply only at renewal or extension")

    pdf.section_heading("7. Contact and Support")
    pdf.body_text(
        "For pricing strategy support, competitive intelligence, or assistance with complex pricing "
        "scenarios, contact:"
    )
    pdf.ln(2)
    pdf.body_text(
        "Victoria Chen\n"
        "Chief Pricing Officer\n"
        "Meridian & Associates LLP\n"
        "Email: v.chen@meridian-llp.com\n"
        "Phone: (212) 555-0312"
    )
    pdf.ln(2)
    pdf.body_text(
        "Andrew Foster\n"
        "VP, Growth Office\n"
        "Meridian & Associates LLP\n"
        "Email: a.foster@meridian-llp.com\n"
        "Phone: (212) 555-0289"
    )

    pdf.output(os.path.join(OUTPUT_DIR, "discount_and_margin_guidance.pdf"))
    print("  Created: discount_and_margin_guidance.pdf")


if __name__ == "__main__":
    generate_cost_model()
    generate_discount_guidance()
    print("\nAll 2 pricing framework PDFs generated successfully!")
