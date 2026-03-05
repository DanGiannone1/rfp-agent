#!/usr/bin/env python3
"""
Generate Meridian & Associates LLP summary PDF reports:
  1. bid_performance_summary.pdf
  2. engagement_performance_summary.pdf

Uses fpdf2 with Helvetica font only. Navy header branding (RGB 0,51,102).
"""

from fpdf import FPDF
import os
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Branding constants ──────────────────────────────────────────────────────
NAVY = (0, 51, 102)
WHITE = (255, 255, 255)
LIGHT_GRAY = (240, 240, 240)
MID_GRAY = (200, 200, 200)
DARK_GRAY = (80, 80, 80)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_RED = (160, 0, 0)
ACCENT_BLUE = (0, 90, 156)
ROW_ALT = (245, 248, 252)  # very light blue for alternating rows


class MeridianPDF(FPDF):
    """Custom PDF class with Meridian & Associates LLP branding."""

    def __init__(self, title_text="Report", **kwargs):
        super().__init__(**kwargs)
        self.title_text = title_text
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        # Navy banner
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 18, "F")
        # Firm name
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*WHITE)
        self.set_xy(10, 3)
        self.cell(0, 6, "MERIDIAN & ASSOCIATES LLP", ln=False)
        # Report title right-aligned
        self.set_font("Helvetica", "", 8)
        self.set_xy(10, 9)
        self.cell(190, 6, self.title_text, align="R")
        # Reset
        self.set_text_color(*BLACK)
        self.set_y(22)

    def footer(self):
        self.set_y(-20)
        # Thin navy line
        self.set_draw_color(*NAVY)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        # CONFIDENTIAL left, page right
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*DARK_RED)
        self.cell(0, 4, "CONFIDENTIAL", ln=True)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*DARK_GRAY)
        self.cell(95, 4, "Meridian & Associates LLP  |  Internal Use Only")
        self.cell(95, 4, f"Page {self.page_no()}/{{nb}}", align="R")

    # ── Utility methods ──────────────────────────────────────────────────

    def add_cover_page(self, title, subtitle, date_str, classification="CONFIDENTIAL"):
        self.add_page()
        # Override header for cover — large navy block
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 110, "F")
        # Firm name
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*WHITE)
        self.set_xy(20, 30)
        self.cell(0, 12, "MERIDIAN & ASSOCIATES LLP", ln=True)
        # Thin white line
        self.set_draw_color(*WHITE)
        self.set_line_width(0.5)
        self.line(20, 48, 190, 48)
        # Title
        self.set_font("Helvetica", "B", 18)
        self.set_xy(20, 55)
        self.multi_cell(170, 10, title)
        # Subtitle
        self.set_font("Helvetica", "", 12)
        self.set_xy(20, 85)
        self.cell(0, 8, subtitle, ln=True)

        # Below navy block
        self.set_text_color(*BLACK)
        self.set_xy(20, 120)
        self.set_font("Helvetica", "", 11)
        self.cell(0, 8, f"Prepared: {date_str}", ln=True)
        self.set_x(20)
        self.cell(0, 8, "Prepared By: Business Development & Quality Assurance", ln=True)
        self.set_x(20)
        self.cell(0, 8, "Distribution: Partners, Managing Directors, BD Leadership", ln=True)

        # Classification box
        self.ln(10)
        self.set_x(20)
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(255, 235, 235)
        self.set_draw_color(*DARK_RED)
        self.set_line_width(0.4)
        self.set_text_color(*DARK_RED)
        self.cell(170, 10, f"CLASSIFICATION: {classification}", border=1,
                  align="C", fill=True, ln=True)
        self.set_text_color(*BLACK)

    def section_title(self, text, numbering=""):
        """Navy section header with optional numbering."""
        self.ln(4)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*NAVY)
        full = f"{numbering}  {text}" if numbering else text
        self.cell(0, 8, full, ln=True)
        # underline
        self.set_draw_color(*NAVY)
        self.set_line_width(0.6)
        y = self.get_y()
        self.line(10, y, 200, y)
        self.ln(4)
        self.set_text_color(*BLACK)

    def sub_section(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*ACCENT_BLUE)
        self.cell(0, 7, text, ln=True)
        self.set_text_color(*BLACK)
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*DARK_GRAY)
        self.multi_cell(0, 5, text)
        self.set_text_color(*BLACK)
        self.ln(1)

    def styled_table(self, headers, data, col_widths=None, align_cols=None,
                     highlight_col=None):
        """
        Render a professional table with navy header row and alternating rows.
        headers: list of str
        data: list of lists of str
        col_widths: list of float (must sum to ~190)
        align_cols: list of str ('L','C','R') per column
        highlight_col: index of column to bold
        """
        n = len(headers)
        if col_widths is None:
            col_widths = [190 / n] * n
        if align_cols is None:
            align_cols = ["L"] + ["C"] * (n - 1)

        # Check if table fits on page; if not, add page
        needed = 8 + len(data) * 6.5 + 4
        if self.get_y() + needed > 270:
            self.add_page()

        # Header row
        self.set_font("Helvetica", "B", 8.5)
        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, border=0, align="C", fill=True)
        self.ln()

        # Data rows
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*BLACK)
        for row_idx, row in enumerate(data):
            if row_idx % 2 == 1:
                self.set_fill_color(*ROW_ALT)
                fill = True
            else:
                self.set_fill_color(*WHITE)
                fill = True
            for i, val in enumerate(row):
                if highlight_col is not None and i == highlight_col:
                    self.set_font("Helvetica", "B", 8.5)
                else:
                    self.set_font("Helvetica", "", 8.5)
                self.cell(col_widths[i], 6.5, str(val), border=0,
                          align=align_cols[i], fill=fill)
            self.ln()

        # Bottom border
        self.set_draw_color(*MID_GRAY)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 10 + sum(col_widths), self.get_y())
        self.ln(3)

    def kpi_row(self, items):
        """
        Render a row of KPI boxes.
        items: list of (label, value, trend_arrow_or_None)
        """
        box_w = 190 / len(items)
        start_x = 10
        y = self.get_y()
        box_h = 20
        if y + box_h + 5 > 270:
            self.add_page()
            y = self.get_y()

        for i, (label, value, trend) in enumerate(items):
            x = start_x + i * box_w
            # Box background
            self.set_fill_color(*LIGHT_GRAY)
            self.set_draw_color(*MID_GRAY)
            self.set_line_width(0.3)
            self.rect(x, y, box_w - 2, box_h, "DF")
            # Value
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(*NAVY)
            self.set_xy(x + 2, y + 2)
            val_text = str(value)
            if trend:
                val_text += f"  {trend}"
            self.cell(box_w - 6, 10, val_text, align="C")
            # Label
            self.set_font("Helvetica", "", 7.5)
            self.set_text_color(*DARK_GRAY)
            self.set_xy(x + 2, y + 12)
            self.cell(box_w - 6, 6, label, align="C")

        self.set_text_color(*BLACK)
        self.set_y(y + box_h + 4)

    def bar_chart_table(self, title, items, max_val=None, bar_width=80):
        """
        Render a horizontal bar chart using table cells.
        items: list of (label, value, display_text)
        """
        if max_val is None:
            max_val = max(v for _, v, _ in items) if items else 1

        self.sub_section(title)
        label_w = 55
        bar_cell_w = bar_width
        val_w = 190 - label_w - bar_cell_w

        if self.get_y() + len(items) * 8 + 10 > 270:
            self.add_page()

        for i, (label, value, display) in enumerate(items):
            if i % 2 == 1:
                self.set_fill_color(*ROW_ALT)
            else:
                self.set_fill_color(*WHITE)
            fill = True
            y = self.get_y()
            # Label
            self.set_font("Helvetica", "", 8.5)
            self.set_text_color(*DARK_GRAY)
            self.cell(label_w, 7, label, align="L", fill=fill)
            # Bar
            bar_len = (value / max_val) * (bar_cell_w - 4) if max_val > 0 else 0
            x_bar = self.get_x() + 2
            self.set_fill_color(*NAVY)
            self.rect(x_bar, y + 1.5, bar_len, 4, "F")
            # Reset fill for row
            if i % 2 == 1:
                self.set_fill_color(*ROW_ALT)
            else:
                self.set_fill_color(*WHITE)
            self.cell(bar_cell_w, 7, "", fill=False)
            # Value
            self.set_font("Helvetica", "B", 8.5)
            self.set_text_color(*NAVY)
            self.cell(val_w, 7, display, align="R", fill=fill)
            self.ln()
            self.set_text_color(*BLACK)
        self.ln(3)

    def bullet_list(self, items, indent=15):
        """Render a bulleted list."""
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GRAY)
        for item in items:
            x = self.get_x()
            self.set_x(indent)
            if self.get_y() > 265:
                self.add_page()
            # bullet character
            self.cell(5, 5, "-", ln=False)
            self.multi_cell(170, 5, item)
            self.ln(0.5)
        self.set_text_color(*BLACK)
        self.ln(2)

    def numbered_list(self, items, indent=15):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK_GRAY)
        for i, item in enumerate(items, 1):
            self.set_x(indent)
            if self.get_y() > 265:
                self.add_page()
            self.cell(8, 5, f"{i}.", ln=False)
            self.multi_cell(167, 5, item)
            self.ln(0.5)
        self.set_text_color(*BLACK)
        self.ln(2)

    def callout_box(self, title, text, color=NAVY):
        """Colored left-border callout box."""
        if self.get_y() + 25 > 265:
            self.add_page()
        y = self.get_y()
        # Left border
        self.set_fill_color(*color)
        self.rect(12, y, 2.5, 20, "F")
        # Background
        self.set_fill_color(245, 248, 252)
        self.rect(14.5, y, 183, 20, "F")
        # Title
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*color)
        self.set_xy(17, y + 2)
        self.cell(0, 5, title)
        # Text
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(*DARK_GRAY)
        self.set_xy(17, y + 8)
        self.multi_cell(178, 4.5, text)
        self.set_y(y + 23)
        self.set_text_color(*BLACK)


# ═══════════════════════════════════════════════════════════════════════════
# DOCUMENT 1: BID PERFORMANCE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

def generate_bid_performance():
    pdf = MeridianPDF(title_text="Bid Performance Summary  |  FY2022-FY2025",
                      orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()

    # ── Cover Page ────────────────────────────────────────────────────────
    pdf.add_cover_page(
        title="Bid & Pursuit Performance Summary",
        subtitle="Fiscal Years 2022 - 2025  |  Year-to-Date FY2026",
        date_str="March 5, 2026",
    )

    # ── Page 2: Executive Summary ─────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Executive Summary", "1.")

    pdf.body_text(
        "This report presents a comprehensive analysis of Meridian & Associates LLP's "
        "bid and pursuit activity spanning fiscal years 2022 through 2025, with year-to-date "
        "figures for FY2026. Over this period, the firm evaluated 347 bid opportunities, "
        "pursued 278 (80%), and achieved a 60% win rate on pursued engagements. The data "
        "reflects a consistent upward trajectory in win rates, deal size, and pursuit "
        "efficiency, while highlighting areas requiring strategic investment."
    )

    pdf.kpi_row([
        ("Total Bids Evaluated", "347", None),
        ("Pursued (Go Decisions)", "278", None),
        ("Won", "167", None),
        ("Overall Win Rate", "60%", None),
    ])

    pdf.ln(2)
    pdf.kpi_row([
        ("No-Bid Decisions", "69 (20%)", None),
        ("Losses", "98 (35%)", None),
        ("Withdrawn", "13 (5%)", None),
        ("Avg Deal Size (FY25)", "$2.4M", None),
    ])

    pdf.ln(4)
    pdf.sub_section("Year-Over-Year Bid Volume")
    pdf.styled_table(
        headers=["Fiscal Year", "Evaluated", "Pursued", "Won", "Lost",
                 "Withdrawn", "No-Bid", "Win Rate"],
        data=[
            ["FY2022", "72", "58", "32", "22", "4", "14", "56%"],
            ["FY2023", "81", "65", "39", "22", "4", "16", "60%"],
            ["FY2024", "89", "72", "46", "24", "2", "17", "64%"],
            ["FY2025", "92", "73", "46", "25", "2", "19", "63%"],
            ["FY2026 YTD", "13", "10", "4", "5", "1", "3", "40%*"],
        ],
        col_widths=[24, 22, 22, 22, 22, 24, 22, 22],
        align_cols=["L", "C", "C", "C", "C", "C", "C", "C"],
    )
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*DARK_GRAY)
    pdf.cell(0, 4, "* FY2026 YTD reflects Q1 only; win rate expected to normalize as pipeline matures.", ln=True)
    pdf.set_text_color(*BLACK)

    pdf.callout_box(
        "KEY INSIGHT",
        "Win rate has improved from 56% in FY2022 to 63% in FY2025, driven by stronger bid/no-bid "
        "discipline, industry specialization investments, and the multi-service bundling strategy.",
    )

    # ── Page 3: Win Rate by Industry & Service Line ───────────────────────
    pdf.add_page()
    pdf.section_title("Win Rate Analysis", "2.")

    pdf.sub_section("2.1  Win Rate by Industry Vertical")
    pdf.body_text(
        "Industry-specific win rates reveal the firm's competitive strengths and "
        "gaps. Financial Services and Energy lead at 66%, while Public Sector trails "
        "at 52%, reflecting a need for investment in cleared personnel and "
        "government-specific compliance frameworks."
    )

    pdf.bar_chart_table(
        "Industry Win Rates",
        [
            ("Financial Services", 66, "82 bids  |  54 won  |  66%"),
            ("Energy", 66, "38 bids  |  25 won  |  66%"),
            ("Manufacturing", 65, "48 bids  |  31 won  |  65%"),
            ("Healthcare", 64, "61 bids  |  39 won  |  64%"),
            ("Technology", 58, "45 bids  |  26 won  |  58%"),
            ("Retail", 55, "31 bids  |  17 won  |  55%"),
            ("Public Sector", 52, "42 bids  |  22 won  |  52%"),
        ],
        max_val=80,
    )

    pdf.ln(2)
    pdf.sub_section("2.2  Win Rate by Service Line")

    pdf.styled_table(
        headers=["Service Line", "Bids", "Won", "Win Rate", "Avg Deal Value"],
        data=[
            ["Multi-Service", "23", "18", "78%", "$4.1M"],
            ["Audit & Assurance", "98", "65", "66%", "$2.8M"],
            ["Tax Services", "72", "47", "65%", "$1.6M"],
            ["Advisory & Consulting", "85", "48", "56%", "$2.9M"],
        ],
        col_widths=[48, 28, 28, 30, 32],
        align_cols=["L", "C", "C", "C", "R"],
        highlight_col=3,
    )

    pdf.callout_box(
        "MULTI-SERVICE ADVANTAGE",
        "Multi-service (bundled) engagements achieve a 78% win rate -- the highest across all "
        "service lines -- and are growing 22% year-over-year. The firm should continue expanding "
        "cross-service pursuit teams.",
    )

    # ── Page 4: Loss Reason Analysis ──────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Loss Reason Analysis", "3.")

    pdf.body_text(
        "Of the 98 competitive losses recorded from FY2022 to FY2025, a structured "
        "loss debrief was conducted for 91 (93%). The following analysis categorizes "
        "root causes and identifies actionable improvement areas."
    )

    pdf.bar_chart_table(
        "Primary Loss Reasons (n = 98)",
        [
            ("Price Competitiveness", 42, "42%  (41 losses)  |  Avg gap: 18% above winner"),
            ("Incumbent Advantage", 23, "23%  (23 losses)  |  Mostly audit rotation retained"),
            ("Capability Gap", 15, "15%  (15 losses)  |  Niche ERP, cleared personnel"),
            ("Relationship / Politics", 12, "12%  (12 losses)  |  Pre-wired RFPs, board ties"),
            ("Compliance / Geographic", 8, "8%  (7 losses)  |  Local presence, certifications"),
        ],
        max_val=50,
        bar_width=55,
    )

    pdf.ln(2)
    pdf.sub_section("3.1  Price Competitiveness Detail")
    pdf.body_text(
        "Price was cited as the primary loss reason in 42% of defeats. Detailed analysis shows "
        "the average pricing gap was 18% above the winning bidder. However, 60% of price-driven "
        "losses occurred in Advisory & Consulting, where blended rates are under the most competitive "
        "pressure. The GDC cost model has partially addressed this -- pursuit teams that leveraged "
        "the Global Delivery Center achieved a 69% win rate versus 52% without."
    )

    pdf.sub_section("3.2  Strategic Recommendations from Loss Analysis")
    pdf.numbered_list([
        "Expand GDC utilization in Advisory proposals to improve rate competitiveness",
        "Invest in FedRAMP / cleared personnel pipeline to address public sector capability gaps",
        "Develop formal incumbent displacement playbook with 18-month relationship-building lead time",
        "Implement competitive intelligence process to identify pre-wired RFPs earlier in the cycle",
        "Establish regional alliance partnerships to address geographic coverage gaps",
    ])

    # ── Page 5: Pursuit Economics ─────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Pursuit Cost & Economics", "4.")

    pdf.body_text(
        "The firm invests approximately $10.6 million annually in pursuit activities. "
        "Effective bid/no-bid discipline and rising win rates have improved pursuit ROI "
        "significantly over the reporting period."
    )

    pdf.kpi_row([
        ("Avg Pursuit Cost", "$38K", None),
        ("Cost as % of Deal", "1.4%", None),
        ("Annual Investment", "$10.6M", None),
        ("Pursuit ROI", "14.2x", None),
    ])

    pdf.ln(4)
    pdf.sub_section("4.1  Pursuit Cost by Engagement Size")
    pdf.styled_table(
        headers=["Deal Size Tier", "Avg Pursuit Cost", "Range", "Win Rate", "ROI"],
        data=[
            ["< $500K", "$8K", "$3K - $15K", "68%", "22.1x"],
            ["$500K - $2M", "$28K", "$12K - $55K", "62%", "16.8x"],
            ["$2M - $5M", "$62K", "$30K - $95K", "58%", "13.4x"],
            ["$5M - $10M", "$95K", "$50K - $140K", "55%", "11.2x"],
            ["> $10M", "$148K", "$80K - $180K", "51%", "9.8x"],
        ],
        col_widths=[38, 34, 38, 28, 28],
        align_cols=["L", "R", "C", "C", "R"],
    )

    pdf.ln(2)
    pdf.sub_section("4.2  Annual Pursuit Investment Trend")
    pdf.styled_table(
        headers=["Fiscal Year", "Total Investment", "Bids Pursued", "Cost/Bid",
                 "Won Revenue", "ROI"],
        data=[
            ["FY2022", "$8.7M", "58", "$150K", "$57.6M", "6.6x"],
            ["FY2023", "$9.8M", "65", "$151K", "$101.4M", "10.3x"],
            ["FY2024", "$10.8M", "72", "$150K", "$147.2M", "13.6x"],
            ["FY2025", "$11.0M", "73", "$151K", "$156.4M", "14.2x"],
        ],
        col_widths=[26, 32, 28, 28, 34, 22],
        align_cols=["L", "R", "C", "R", "R", "R"],
    )

    pdf.callout_box(
        "EFFICIENCY GAINS",
        "Pursuit ROI has more than doubled from 6.6x in FY2022 to 14.2x in FY2025, "
        "driven by stronger bid/no-bid discipline (20% no-bid rate) and larger average deal sizes.",
    )

    # ── Page 6: Win Theme Effectiveness ───────────────────────────────────
    pdf.add_page()
    pdf.section_title("Win Theme Effectiveness", "5.")

    pdf.body_text(
        "Analysis of winning proposals identifies five recurring themes most strongly "
        "correlated with positive outcomes. Proposals incorporating three or more of these "
        "themes achieved a combined 76% win rate."
    )

    pdf.bar_chart_table(
        "Win Rate When Theme Is Present in Proposal",
        [
            ("Multi-service integration", 78, "78%  |  Used in 23 bids"),
            ("Industry specialization / named SMEs", 73, "73%  |  Used in 142 bids"),
            ("Past performance / case studies", 71, "71%  |  Used in 189 bids"),
            ("GDC cost model / blended rates", 69, "69%  |  Used in 96 bids"),
            ("Proprietary technology (MeridianAI)", 67, "67%  |  Used in 78 bids"),
        ],
        max_val=85,
    )

    pdf.ln(2)
    pdf.sub_section("5.1  Theme Combination Analysis")
    pdf.styled_table(
        headers=["Themes in Proposal", "Bids", "Won", "Win Rate"],
        data=[
            ["0-1 themes", "52", "24", "46%"],
            ["2 themes", "89", "51", "57%"],
            ["3 themes", "78", "53", "68%"],
            ["4+ themes", "59", "45", "76%"],
        ],
        col_widths=[50, 40, 40, 40],
        align_cols=["L", "C", "C", "C"],
        highlight_col=3,
    )

    pdf.callout_box(
        "RECOMMENDATION",
        "All pursuit teams should target inclusion of at least three win themes per proposal. "
        "BD leadership should gate proposal submissions on theme checklist completion.",
    )

    # ── Page 7: Competitive Landscape ─────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Competitive Win/Loss Analysis", "6.")

    pdf.body_text(
        "Head-to-head competitive data is tracked for five primary competitors. The firm "
        "performs strongest against RSK International (68% win rate) and weakest against "
        "Whitfield & Crane (40%), the latter being the firm's most frequent competitor."
    )

    pdf.styled_table(
        headers=["Competitor", "Head-to-Head", "We Won", "We Lost",
                 "Win Rate", "Primary Threat"],
        data=[
            ["RSK International", "22", "15", "7", "68%", "Global reach"],
            ["Hensley Pratt", "31", "19", "12", "61%", "Tax specialization"],
            ["Calloway Donovan", "38", "22", "16", "58%", "Technology practice"],
            ["Novak Bishop Group", "28", "16", "12", "57%", "Regional depth"],
            ["Whitfield & Crane", "45", "18", "27", "40%", "Price, incumbency"],
        ],
        col_widths=[36, 26, 22, 22, 22, 42],
        align_cols=["L", "C", "C", "C", "C", "L"],
        highlight_col=4,
    )

    pdf.ln(2)
    pdf.sub_section("6.1  Whitfield & Crane Deep-Dive")
    pdf.body_text(
        "As the firm's most formidable competitor (45 head-to-head encounters, 40% win rate), "
        "Whitfield & Crane warrants dedicated counter-strategy. Key competitive disadvantages "
        "observed include:"
    )
    pdf.bullet_list([
        "Consistently 10-15% lower fee structure due to larger offshore delivery capacity",
        "Stronger incumbent retention in audit rotations (they retain 72% of defenses vs. our 58%)",
        "Deeper bench in financial services regulatory advisory",
        "More aggressive pursuit investment (estimated 2.1% of deal value vs. our 1.4%)",
    ])

    pdf.sub_section("6.2  Recommended Counter-Strategies")
    pdf.numbered_list([
        "Develop W&C-specific competitive battle cards with differentiated messaging",
        "Pre-position relationships 18+ months ahead of known rotation cycles",
        "Lead with MeridianAI differentiation where W&C relies on manual processes",
        "Pursue joint-bid opportunities in sectors where we are complementary",
    ])

    # ── Page 8: Trends & Outlook ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Trends & Strategic Outlook", "7.")

    pdf.sub_section("7.1  Key Performance Trends (FY2022 to FY2025)")
    pdf.styled_table(
        headers=["Metric", "FY2022", "FY2023", "FY2024", "FY2025", "Trend"],
        data=[
            ["Win rate (pursued)", "56%", "60%", "64%", "63%", "Improving"],
            ["Average deal size", "$1.8M", "$2.0M", "$2.2M", "$2.4M", "Growing"],
            ["Multi-svc % of bids", "5%", "7%", "9%", "12%", "Growing 22% YoY"],
            ["Public sector win rate", "58%", "55%", "52%", "48%", "Declining"],
            ["No-bid rate", "19%", "20%", "19%", "21%", "Stable"],
            ["Pursuit ROI", "6.6x", "10.3x", "13.6x", "14.2x", "Strong growth"],
        ],
        col_widths=[38, 24, 24, 24, 24, 36],
        align_cols=["L", "C", "C", "C", "C", "L"],
    )

    pdf.ln(3)
    pdf.sub_section("7.2  FY2026 Strategic Priorities")
    pdf.numbered_list([
        "Achieve 65% overall win rate by expanding theme-based proposal methodology",
        "Grow multi-service pursuits to 15% of total bids (from 12%)",
        "Reverse public sector win rate decline through cleared personnel hiring initiative",
        "Reduce price-driven losses by 20% through expanded GDC utilization in Advisory",
        "Launch competitive intelligence program targeting Whitfield & Crane displacement",
        "Implement formal pursuit cost tracking at engagement level for ROI optimization",
    ])

    pdf.ln(2)
    pdf.sub_section("7.3  Pipeline Outlook (FY2026)")
    pdf.body_text(
        "The current qualified pipeline contains 42 active opportunities with an estimated "
        "total contract value of $138M. Based on current win rates and pipeline stage "
        "weighting, the firm projects $78M-$92M in new wins for FY2026, representing "
        "12-18% growth over FY2025."
    )

    pdf.callout_box(
        "OUTLOOK",
        "The firm is well-positioned for continued growth, with improving win rates, larger "
        "deal sizes, and a robust pipeline. Key risks include public sector capability gaps "
        "and pricing pressure from Whitfield & Crane in the financial services vertical.",
    )

    # ── Save ──────────────────────────────────────────────────────────────
    path = os.path.join(OUTPUT_DIR, "bid_performance_summary.pdf")
    pdf.output(path)
    print(f"Generated: {path}  ({pdf.page_no()} pages)")
    return path


# ═══════════════════════════════════════════════════════════════════════════
# DOCUMENT 2: ENGAGEMENT PERFORMANCE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

def generate_engagement_performance():
    pdf = MeridianPDF(
        title_text="Engagement Performance Summary  |  FY2022-FY2025",
        orientation="P", unit="mm", format="A4",
    )
    pdf.alias_nb_pages()

    # ── Cover Page ────────────────────────────────────────────────────────
    pdf.add_cover_page(
        title="Engagement Delivery Performance Summary",
        subtitle="Fiscal Years 2022 - 2025  |  Comprehensive Review",
        date_str="March 5, 2026",
    )

    # ── Page 2: Executive Summary ─────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Executive Summary", "1.")

    pdf.body_text(
        "This report provides a comprehensive review of Meridian & Associates LLP's engagement "
        "delivery performance across fiscal years 2022 through 2025. The firm has completed 1,089 "
        "engagements totaling $3.2 billion in tracked revenue during this period, with marked "
        "improvement across all key delivery metrics including margin realization, on-time "
        "delivery, client satisfaction, and quality indicators."
    )

    pdf.kpi_row([
        ("Total Engagements", "1,247", None),
        ("Completed", "1,089", None),
        ("Revenue Delivered", "$3.2B", None),
        ("Avg Engagement Value", "$2.6M", None),
    ])

    pdf.ln(2)
    pdf.kpi_row([
        ("FY25 Actual Margin", "29.1%", None),
        ("FY25 Realization", "0.92", None),
        ("FY25 Client NPS", "71", None),
        ("Client Retention", "94%", None),
    ])

    pdf.ln(4)
    pdf.body_text(
        "Key highlights from the four-year review period include: actual margins reaching and "
        "exceeding the 29% target in FY2025; realization rate improving from 0.87 to 0.92; "
        "client NPS climbing 13 points from 58 to 71; and rework incidents declining by 53%. "
        "The firm's investment in delivery methodology, project management tooling, and quality "
        "assurance processes has yielded measurable returns."
    )

    pdf.callout_box(
        "KEY ACHIEVEMENT",
        "FY2025 marks the first year actual margins (29.1%) exceeded the firm's target margin (29%), "
        "driven by improved realization rates and a 45% reduction in write-offs since FY2022.",
    )

    # ── Page 3: Financial Performance ─────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Financial Performance", "2.")

    pdf.sub_section("2.1  Margin & Realization Trends")
    pdf.styled_table(
        headers=["Metric", "FY2022", "FY2023", "FY2024", "FY2025", "4-Year Trend"],
        data=[
            ["Target Margin", "28.0%", "28.0%", "29.0%", "29.0%", "Stable"],
            ["Actual Margin", "26.4%", "27.1%", "28.3%", "29.1%", "Improving"],
            ["Margin Gap", "-1.6%", "-0.9%", "-0.7%", "+0.1%", "Closed"],
            ["Realization Rate", "0.87", "0.89", "0.91", "0.92", "Improving"],
            ["Write-offs ($M)", "$18.4", "$15.2", "$12.8", "$10.1", "Declining"],
            ["Collections (Days)", "42", "39", "37", "35", "Improving"],
        ],
        col_widths=[34, 24, 24, 24, 24, 34],
        align_cols=["L", "C", "C", "C", "C", "L"],
    )

    pdf.ln(2)
    pdf.sub_section("2.2  Write-Off Reduction Analysis")
    pdf.body_text(
        "Total write-offs declined 45% from $18.4M in FY2022 to $10.1M in FY2025. This $8.3M "
        "improvement is attributable to three primary factors: (1) tighter scope definition at "
        "engagement inception, (2) automated budget tracking and early warning alerts via the "
        "MeridianPM platform, and (3) mandatory quarterly engagement health reviews for all "
        "engagements exceeding $1M in value."
    )

    pdf.bar_chart_table(
        "Write-Offs by Service Line (FY2025)",
        [
            ("Advisory & Consulting", 5.2, "$5.2M  |  51% of total"),
            ("Audit & Assurance", 2.4, "$2.4M  |  24% of total"),
            ("Multi-Service", 1.5, "$1.5M  |  15% of total"),
            ("Tax Services", 1.0, "$1.0M  |  10% of total"),
        ],
        max_val=6,
    )

    pdf.ln(2)
    pdf.sub_section("2.3  Collections Performance")
    pdf.body_text(
        "Days Sales Outstanding (DSO) improved from 42 days to 35 days over the period. "
        "The firm now collects 91% of invoiced amounts within 45 days, up from 78% in FY2022. "
        "Automated invoicing, milestone-based billing, and dedicated collections support for "
        "engagements over $2M have driven this improvement."
    )

    # ── Page 4: Delivery Quality ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Delivery Quality Metrics", "3.")

    pdf.sub_section("3.1  On-Time & On-Budget Performance")
    pdf.styled_table(
        headers=["Metric", "FY2022", "FY2023", "FY2024", "FY2025", "Improvement"],
        data=[
            ["On-Time Delivery", "71%", "74%", "78%", "82%", "+11 pts"],
            ["On-Budget Delivery", "65%", "68%", "72%", "76%", "+11 pts"],
            ["Both On-Time & On-Budget", "52%", "56%", "62%", "68%", "+16 pts"],
            ["Client NPS (Average)", "58", "62", "67", "71", "+13 pts"],
            ["Rework Incidents", "47", "38", "29", "22", "-53%"],
            ["Engagement Terminations", "8", "5", "4", "2", "-75%"],
        ],
        col_widths=[40, 24, 24, 24, 24, 30],
        align_cols=["L", "C", "C", "C", "C", "C"],
    )

    pdf.ln(3)
    pdf.sub_section("3.2  Client NPS Trend by Service Line")
    pdf.styled_table(
        headers=["Service Line", "FY2022", "FY2023", "FY2024", "FY2025", "Trend"],
        data=[
            ["Multi-Service", "65", "69", "72", "74", "+9"],
            ["Tax Services", "64", "68", "71", "72", "+8"],
            ["Audit & Assurance", "56", "60", "65", "68", "+12"],
            ["Advisory & Consulting", "52", "57", "62", "65", "+13"],
        ],
        col_widths=[40, 26, 26, 26, 26, 26],
        align_cols=["L", "C", "C", "C", "C", "C"],
    )

    pdf.ln(2)
    pdf.sub_section("3.3  Rework Incident Analysis")
    pdf.body_text(
        "Rework incidents -- defined as deliverable revisions requiring more than 40 hours of "
        "unplanned effort -- declined from 47 in FY2022 to 22 in FY2025. Advisory & Consulting "
        "accounted for 59% of all rework incidents, followed by Multi-Service at 23%. "
        "Root causes include scope ambiguity (41%), data quality issues (28%), and staff "
        "capability mismatches (18%)."
    )

    pdf.callout_box(
        "QUALITY MILESTONE",
        "FY2025 engagement terminations dropped to just 2 (from 8 in FY2022), reflecting "
        "the impact of proactive engagement health monitoring and early partner intervention.",
    )

    # ── Page 5: Performance by Service Line ───────────────────────────────
    pdf.add_page()
    pdf.section_title("Performance by Service Line", "4.")

    pdf.styled_table(
        headers=["Service Line", "Avg Margin", "On-Time", "On-Budget",
                 "NPS", "Realization"],
        data=[
            ["Tax Services", "33.8%", "88%", "82%", "72", "0.95"],
            ["Audit & Assurance", "31.2%", "85%", "78%", "68", "0.94"],
            ["Multi-Service", "27.3%", "74%", "69%", "74", "0.90"],
            ["Advisory & Consulting", "24.6%", "71%", "65%", "65", "0.88"],
        ],
        col_widths=[40, 28, 26, 26, 24, 28],
        align_cols=["L", "C", "C", "C", "C", "C"],
        highlight_col=1,
    )

    pdf.ln(3)
    pdf.sub_section("4.1  Audit & Assurance")
    pdf.body_text(
        "The Audit & Assurance practice delivers the second-highest margins (31.2%) with "
        "strong delivery predictability (85% on-time). Key success factors include well-defined "
        "regulatory frameworks that constrain scope, mature staffing models, and recurring "
        "engagement patterns. The primary risk is first-year audit transitions, which "
        "consistently require 18 months rather than the contracted 12 for complex financial "
        "institutions."
    )

    pdf.sub_section("4.2  Tax Services")
    pdf.body_text(
        "Tax Services leads all practice areas in margin (33.8%), on-time delivery (88%), "
        "and realization (0.95). The practice benefits from well-defined deliverables, strong "
        "repeatability, and high client dependency. Seasonal concentration in Q3/Q4 creates "
        "resource pressure but also drives scheduling discipline."
    )

    pdf.sub_section("4.3  Advisory & Consulting")
    pdf.body_text(
        "Advisory & Consulting, while the largest revenue contributor, has the lowest margins "
        "(24.6%) and delivery metrics. This reflects inherent project complexity, scope evolution, "
        "and competitive rate pressure. Improvement initiatives include mandatory scope gates "
        "at 25%/50%/75% completion, expanded use of the Global Delivery Center for commodity "
        "workstreams, and structured change order processes."
    )

    pdf.sub_section("4.4  Multi-Service Engagements")
    pdf.body_text(
        "Multi-service engagements -- bundling audit, tax, and/or advisory services -- generate "
        "the highest NPS (74) but face coordination challenges reflected in lower on-time (74%) "
        "and on-budget (69%) scores. The mandatory single program director model, implemented "
        "in Q2 FY2025, is expected to improve these metrics significantly."
    )

    # ── Page 6: Risk Events & Mitigation ──────────────────────────────────
    pdf.add_page()
    pdf.section_title("Risk Events & Mitigation", "5.")

    pdf.sub_section("5.1  Top Recurring Risk Patterns")
    pdf.body_text(
        "Analysis of engagement post-mortems and quarterly health reviews identifies five "
        "recurring risk patterns that account for 78% of budget overruns and delivery delays."
    )

    pdf.styled_table(
        headers=["Risk Pattern", "Frequency", "Avg Budget Impact",
                 "Avg Schedule Impact", "Service Lines Affected"],
        data=[
            ["Scope creep (advisory)", "38% of overruns", "+22%", "+6 weeks",
             "Advisory, Multi-Svc"],
            ["Data migration gaps", "24% of overruns", "+35%", "+8 weeks",
             "Advisory (ERP)"],
            ["Client resource delays", "18% of overruns", "+12%", "+4 weeks",
             "Healthcare, Pub Sector"],
            ["Staff attrition mid-project", "12% of overruns", "+15%", "+3 weeks",
             "All service lines"],
            ["Regulatory changes", "8% of overruns", "+18%", "+5 weeks",
             "Audit, Tax"],
        ],
        col_widths=[38, 28, 30, 30, 42],
        align_cols=["L", "C", "C", "C", "L"],
    )

    pdf.ln(3)
    pdf.sub_section("5.2  Mitigation Actions Implemented")
    pdf.numbered_list([
        "Scope creep: Mandatory scope gates at 25%/50%/75% with formal change order for any expansion",
        "Data migration: 30% contingency buffer now required for legacy systems older than 10 years",
        "Client resources: Contractual client resource commitments with penalty clauses for delays",
        "Staff attrition: Engagement-level retention bonuses for critical roles on 12+ month projects",
        "Regulatory changes: Quarterly regulatory scanning with methodology pivot protocols",
    ])

    pdf.sub_section("5.3  Staff Attrition Impact")
    pdf.body_text(
        "Average annual turnover on active engagements is 8%, with peak attrition in the "
        "24-36 month experience band. Advisory & Consulting is most affected (11% attrition) "
        "due to project-based staffing and competitive poaching. The firm has implemented "
        "engagement-level retention incentives and structured knowledge transfer protocols "
        "to mitigate continuity risk."
    )

    # ── Page 7: Client Retention & Follow-On ──────────────────────────────
    pdf.add_page()
    pdf.section_title("Client Retention & Follow-On Revenue", "6.")

    pdf.kpi_row([
        ("Client Retention Rate", "94%", None),
        ("Follow-On Rate", "62%", None),
        ("LTV Multiplier", "3.2x", None),
        ("Top 20 Revenue Share", "34%", None),
    ])

    pdf.ln(4)
    pdf.sub_section("6.1  Retention & Follow-On Trends")
    pdf.styled_table(
        headers=["Metric", "FY2022", "FY2023", "FY2024", "FY2025"],
        data=[
            ["Client retention rate", "91%", "92%", "93%", "94%"],
            ["Engagements with follow-on", "54%", "57%", "60%", "62%"],
            ["LTV multiplier (avg)", "2.6x", "2.8x", "3.0x", "3.2x"],
            ["Cross-sell rate", "18%", "22%", "26%", "31%"],
            ["Upsell rate (within engagement)", "28%", "31%", "35%", "38%"],
        ],
        col_widths=[48, 32, 32, 32, 32],
        align_cols=["L", "C", "C", "C", "C"],
    )

    pdf.ln(3)
    pdf.sub_section("6.2  Revenue Concentration Analysis")
    pdf.body_text(
        "The top 20 clients account for 34% of tracked engagement revenue ($1.09B of $3.2B). "
        "While this concentration provides revenue stability, it also represents a risk factor. "
        "The firm has established a key account program with dedicated relationship partners "
        "and annual strategic reviews for the top 50 clients."
    )

    pdf.styled_table(
        headers=["Client Tier", "# Clients", "% of Revenue", "Avg LTV",
                 "Retention Rate"],
        data=[
            ["Tier 1 (Top 20)", "20", "34%", "$54.5M", "98%"],
            ["Tier 2 (21-50)", "30", "24%", "$25.6M", "96%"],
            ["Tier 3 (51-100)", "50", "22%", "$14.1M", "94%"],
            ["Tier 4 (101+)", "347", "20%", "$1.8M", "89%"],
        ],
        col_widths=[38, 28, 30, 32, 32],
        align_cols=["L", "C", "C", "R", "C"],
    )

    pdf.callout_box(
        "GROWTH OPPORTUNITY",
        "Cross-sell rate has grown from 18% to 31% over four years. The firm targets 40% "
        "by FY2027 through structured account planning and multi-service pursuit incentives.",
    )

    # ── Page 8: Lessons Learned & Outlook ─────────────────────────────────
    pdf.add_page()
    pdf.section_title("Lessons Learned & Strategic Outlook", "7.")

    pdf.sub_section("7.1  Key Lessons from Engagement Close-Outs")
    pdf.body_text(
        "The following lessons are distilled from 1,089 engagement close-out reviews conducted "
        "over FY2022-FY2025. Each has been incorporated into the firm's engagement methodology "
        "and proposal scoping guidelines."
    )

    pdf.numbered_list([
        "Healthcare engagements: Include clinical/domain SME from day 1. Engagements that "
        "embedded a clinical subject matter expert from inception had 34% fewer rework "
        "incidents and 18% higher NPS scores.",
        "SAP/ERP data migration: Require 30% contingency for legacy systems older than 10 "
        "years. Historical data shows actual migration effort exceeds estimates by 25-40% "
        "for legacy environments.",
        "Public sector procurement: Budget 6-week delay buffer beyond contracted start date. "
        "Average actual procurement delay is 6.2 weeks, with some engagements delayed "
        "up to 14 weeks.",
        "Multi-service engagements: Mandate a single program director rather than per-service-line "
        "leads. Engagements with unified program leadership score 12 points higher on NPS and "
        "are 22% more likely to deliver on budget.",
        "First-year audit transitions: Plan for 18 months, not 12, for complex financial "
        "institutions. Accelerated transitions (12 months) have a 62% probability of budget "
        "overrun exceeding 15%.",
    ])

    pdf.ln(2)
    pdf.sub_section("7.2  FY2026 Delivery Priorities")
    pdf.numbered_list([
        "Achieve 85% on-time delivery rate across all service lines",
        "Reduce Advisory & Consulting rework incidents by 30% through scope gate enforcement",
        "Improve overall realization rate to 0.94 through better estimate calibration",
        "Expand MeridianPM platform adoption to 100% of engagements over $500K",
        "Reduce DSO to 33 days through milestone-based billing automation",
        "Achieve 96% client retention through proactive key account management",
    ])

    pdf.ln(2)
    pdf.sub_section("7.3  Performance Outlook")
    pdf.body_text(
        "The firm's delivery performance trajectory is strongly positive across all dimensions. "
        "Margins have reached target levels, quality metrics are improving consistently, and "
        "client satisfaction is at its highest recorded level. The primary areas requiring "
        "continued attention are Advisory & Consulting delivery predictability, multi-service "
        "coordination, and staff retention on long-duration engagements. With the methodology "
        "enhancements and tooling investments underway, the firm is well-positioned to achieve "
        "its FY2026 delivery targets."
    )

    pdf.callout_box(
        "STRATEGIC OUTLOOK",
        "Engagement delivery performance has improved materially across every tracked metric over "
        "four years. Continued investment in project management tooling, quality gates, and "
        "staff retention will sustain this trajectory and support the firm's growth ambitions.",
    )

    # ── Save ──────────────────────────────────────────────────────────────
    path = os.path.join(OUTPUT_DIR, "engagement_performance_summary.pdf")
    pdf.output(path)
    print(f"Generated: {path}  ({pdf.page_no()} pages)")
    return path


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 60)
    print("Meridian & Associates LLP — PDF Report Generator")
    print("=" * 60)
    print()
    generate_bid_performance()
    print()
    generate_engagement_performance()
    print()
    print("Done. Both reports generated successfully.")
