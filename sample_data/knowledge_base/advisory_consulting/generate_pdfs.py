#!/usr/bin/env python3
"""Generate 7 synthetic professional-services PDF documents for Meridian & Associates LLP."""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Helper PDF class
# ---------------------------------------------------------------------------

class MeridianPDF(FPDF):
    """Custom PDF with Meridian & Associates branding."""

    def __init__(self, title: str, version: str = "3.1", date: str = "January 2026"):
        super().__init__()
        self.doc_title = title
        self.doc_version = version
        self.doc_date = date
        self.set_auto_page_break(auto=True, margin=25)

    # -- cover page --------------------------------------------------------

    def cover_page(self):
        self.add_page()
        # Top bar
        self.set_fill_color(0, 51, 102)
        self.rect(0, 0, 210, 45, "F")
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(255, 255, 255)
        self.set_y(12)
        self.cell(0, 10, "MERIDIAN & ASSOCIATES LLP", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 11)
        self.cell(0, 7, "Advisory | Consulting | Technology | Risk", align="C", new_x="LMARGIN", new_y="NEXT")

        # Title block
        self.set_text_color(0, 0, 0)
        self.ln(35)
        self.set_font("Helvetica", "B", 22)
        self.multi_cell(0, 11, self.doc_title, align="C")
        self.ln(8)
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.8)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(12)

        # Meta info
        self.set_font("Helvetica", "", 11)
        meta = [
            ("Version", self.doc_version),
            ("Effective Date", self.doc_date),
            ("Classification", "CONFIDENTIAL -- Internal Use Only"),
            ("Owner", "Advisory & Consulting Practice"),
            ("Approved By", "Managing Director, Advisory Services"),
        ]
        for label, val in meta:
            self.set_font("Helvetica", "B", 11)
            self.cell(45, 7, f"{label}:", align="R")
            self.set_font("Helvetica", "", 11)
            self.cell(0, 7, f"  {val}", new_x="LMARGIN", new_y="NEXT")
        self.ln(20)

        # Confidentiality notice
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(120, 120, 120)
        self.multi_cell(
            0, 5,
            "This document is the proprietary and confidential property of Meridian & Associates LLP. "
            "It is intended solely for internal use and for authorized client engagements. Unauthorized "
            "reproduction, distribution, or disclosure of this material is strictly prohibited. "
            "All frameworks, methodologies, and tools described herein are protected intellectual property.",
            align="C",
        )
        self.set_text_color(0, 0, 0)

    # -- header / footer ---------------------------------------------------

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Meridian & Associates LLP  |  {self.doc_title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.3)
        self.line(10, 13, 200, 13)
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-18)
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "CONFIDENTIAL", align="L")
        self.cell(0, 5, f"Page {self.page_no()}", align="R")
        self.set_text_color(0, 0, 0)

    # -- content helpers ---------------------------------------------------

    def section_heading(self, number: str, title: str):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 9, f"{number}  {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def sub_heading(self, number: str, title: str):
        self.ln(2)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0, 70, 130)
        self.cell(0, 8, f"{number}  {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def body(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet_list(self, items: list[str]):
        self.set_font("Helvetica", "", 10)
        for item in items:
            x = self.get_x()
            self.cell(8, 5.5, "-")  # bullet dash
            self.multi_cell(0, 5.5, item)
            self.set_x(x)
        self.ln(2)

    def bold_body(self, label: str, text: str):
        """Render a bold label followed by normal text on the same line."""
        self.set_font("Helvetica", "B", 10)
        self.cell(self.get_string_width(label) + 2, 5.5, label)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def new_content_page(self):
        self.add_page()


# ===========================================================================
# 1. Standard Project Lifecycle
# ===========================================================================
def gen_project_lifecycle():
    pdf = MeridianPDF("Standard Project Lifecycle Framework", "4.2", "January 2026")
    pdf.cover_page()
    pdf.new_content_page()

    # 1 - Executive Overview
    pdf.section_heading("1", "Executive Overview")
    pdf.body(
        "The Standard Project Lifecycle (SPL), branded externally as Meridian Accelerate(TM), is the firm's "
        "universal delivery framework, applicable across all Advisory and Consulting engagements regardless "
        "of industry, technology stack, or engagement size. Developed over two decades of transformation "
        "experience and refined through more than 1,200 completed engagements, the SPL provides a structured "
        "yet adaptable approach to delivering measurable client outcomes. Every Meridian project team is "
        "required to follow this lifecycle unless a formal exception has been approved by the Practice Lead "
        "and the Quality Assurance Director."
    )
    pdf.body(
        "The SPL consists of five sequential phases, each with defined entry criteria, key activities, "
        "deliverables, governance checkpoints, and exit criteria. While the phases are sequential, iterative "
        "loops within individual phases are encouraged, particularly during the Design and Build phases where "
        "emerging requirements and stakeholder feedback demand flexibility. The framework is complemented by "
        "cross-cutting disciplines including risk management, quality assurance, change management, and "
        "benefits realization that operate continuously throughout all five phases."
    )

    # 2 - Phase 1: Discover
    pdf.section_heading("2", "Phase 1: Discover (Weeks 1-6)")
    pdf.body(
        "The Discover phase establishes a comprehensive understanding of the client's current state, strategic "
        "objectives, pain points, and constraints. This phase is foundational; inadequate discovery is the "
        "single most common root cause of project overruns and scope disputes across the professional services "
        "industry. Meridian mandates a minimum of three weeks for Discover on any engagement exceeding $500K in "
        "total contract value."
    )

    pdf.sub_heading("2.1", "Current-State Assessment")
    pdf.body(
        "The engagement team conducts a structured current-state assessment that encompasses business processes, "
        "technology landscape, organizational structure, data architecture, and regulatory environment. The "
        "assessment uses Meridian's proprietary Maturity Model, which evaluates capabilities across five "
        "dimensions: process maturity, technology enablement, data governance, talent readiness, and innovation "
        "capacity. Each dimension is scored on a 1-5 scale with detailed rubrics."
    )

    pdf.sub_heading("2.2", "Stakeholder Interviews and Workshops")
    pdf.body(
        "A minimum of 15-25 stakeholder interviews are conducted across executive leadership, middle management, "
        "and operational staff. Interviews follow Meridian's Semi-Structured Interview Protocol (SSIP), which "
        "balances consistency with the flexibility to probe emerging themes. Workshops are facilitated using "
        "the MURAL digital whiteboarding platform for remote participants and physical war-room sessions for "
        "co-located teams."
    )
    pdf.bullet_list([
        "Executive sponsor alignment sessions (2-3 sessions, 90 minutes each)",
        "Process owner deep-dives (5-8 sessions covering end-to-end value streams)",
        "Technology architecture review with client IT leadership",
        "End-user focus groups to validate pain points and workarounds",
        "Regulatory and compliance landscape briefing with legal/risk teams",
    ])

    pdf.sub_heading("2.3", "Pain Point and Opportunity Identification")
    pdf.body(
        "All pain points, inefficiencies, and opportunities are cataloged in the Meridian Issue & Opportunity "
        "Register (IOR). Each entry is scored on a two-dimensional matrix: business impact (revenue, cost, risk, "
        "customer experience) and addressability (technical feasibility, organizational readiness, budget "
        "alignment). This prioritized register directly feeds into the Design phase's requirements backlog."
    )

    pdf.sub_heading("2.4", "Discover Phase Deliverables")
    pdf.bullet_list([
        "Current-State Assessment Report with maturity scores",
        "Stakeholder Interview Summary and Themes Analysis",
        "Issue & Opportunity Register (prioritized)",
        "Preliminary Scope and Boundary Document",
        "Discover Phase Findings Presentation to Steering Committee",
        "Updated Risk Register with initial risk ratings",
    ])
    pdf.bold_body("Governance Checkpoint:", "Discover Gate Review with project Steering Committee. Go/No-Go decision "
                   "based on completeness of current-state understanding and alignment on project scope boundaries.")

    # 3 - Phase 2: Design
    pdf.section_heading("3", "Phase 2: Design (Weeks 4-12)")
    pdf.body(
        "The Design phase translates discovery findings into a concrete future-state vision, solution "
        "architecture, and detailed requirements. This phase typically overlaps with the final weeks of Discover "
        "as early design hypotheses emerge from stakeholder workshops. The Design phase produces the blueprints "
        "that govern all subsequent Build and Test activities."
    )

    pdf.sub_heading("3.1", "Future-State Architecture")
    pdf.body(
        "The future-state architecture encompasses business process models (using BPMN 2.0 notation), "
        "technology architecture (logical and physical views following TOGAF ADM), data architecture (conceptual "
        "and logical data models), and integration architecture (API specifications, middleware design, event "
        "streaming topology). Each architecture artifact undergoes peer review by Meridian's Architecture "
        "Review Board (ARB) before client presentation."
    )

    pdf.sub_heading("3.2", "Requirements Specification")
    pdf.body(
        "Requirements are documented using a tiered approach: business requirements (BRDs) capture strategic "
        "outcomes, functional requirements (FRDs) detail system behaviors and user stories, and non-functional "
        "requirements (NFRs) address performance, scalability, security, and accessibility standards. Meridian "
        "utilizes a RICE scoring model (Reach, Impact, Confidence, Effort) to prioritize the requirements backlog "
        "and inform release planning."
    )

    pdf.sub_heading("3.3", "Solution Blueprint")
    pdf.body(
        "The Solution Blueprint is the single authoritative design document that integrates all architecture "
        "views, requirements, assumptions, constraints, and design decisions. It serves as the contract between "
        "the project team and the Steering Committee regarding what will be built. Any material deviation from "
        "the approved Solution Blueprint requires a formal Change Request."
    )

    pdf.sub_heading("3.4", "Design Phase Deliverables")
    pdf.bullet_list([
        "Future-State Business Process Models (BPMN 2.0)",
        "Solution Architecture Document (TOGAF-aligned)",
        "Functional and Non-Functional Requirements Specification",
        "Solution Blueprint (integrated design document)",
        "Data Migration Strategy and Mapping Document",
        "Integration Design Specification",
        "Updated Project Plan with Build phase work breakdown structure",
    ])
    pdf.bold_body("Governance Checkpoint:", "Design Gate Review. The Steering Committee approves the Solution Blueprint, "
                   "confirming that the proposed design addresses all prioritized requirements within budget and timeline "
                   "constraints. Formal sign-off required before Build commences.")

    # 4 - Phase 3: Build
    pdf.section_heading("4", "Phase 3: Build (Weeks 10-28)")
    pdf.body(
        "The Build phase is where the approved design is translated into configured, developed, and integrated "
        "solution components. Meridian employs an iterative build approach with two-week sprints, regardless of "
        "whether the overall project follows Agile or Waterfall methodology. Each sprint concludes with a "
        "demonstrable increment reviewed by the Product Owner and key stakeholders."
    )

    pdf.sub_heading("4.1", "Configuration and Development")
    pdf.body(
        "Solution components are built following Meridian's Secure Development Lifecycle (SDL), which embeds "
        "security reviews, code quality gates, and automated testing at every stage. All configuration changes "
        "are version-controlled, and all custom code undergoes mandatory peer review before merge. The team "
        "maintains a Definition of Done (DoD) checklist that includes unit test coverage (minimum 80%), "
        "code review approval, security scan pass, and documentation updates."
    )

    pdf.sub_heading("4.2", "Data Migration")
    pdf.body(
        "Data migration follows Meridian's four-stage ETL methodology: Extract (source system data pulls with "
        "completeness validation), Transform (cleansing, deduplication, format normalization, business rule "
        "application), Load (target system population with referential integrity checks), and Verify (automated "
        "reconciliation reports comparing source and target record counts, checksums, and sample audits). "
        "A minimum of three mock migrations are conducted before production cutover."
    )

    pdf.sub_heading("4.3", "Build Phase Deliverables")
    pdf.bullet_list([
        "Configured and developed solution components (sprint increments)",
        "Unit test results and code coverage reports",
        "Data migration scripts and reconciliation reports",
        "Integration test results for component interfaces",
        "Technical documentation and operations runbooks",
        "Sprint review recordings and demo artifacts",
        "Updated risk and issue registers",
    ])
    pdf.bold_body("Governance Checkpoint:", "Build Completion Gate. Confirmation that all solution components meet "
                   "the Definition of Done, data migration dry runs are successful, and the solution is ready for "
                   "formal testing. Entry criteria for Test phase must be satisfied.")

    # 5 - Phase 4: Test
    pdf.section_heading("5", "Phase 4: Test (Weeks 24-34)")
    pdf.body(
        "The Test phase validates that the solution meets all functional requirements, non-functional standards, "
        "and user expectations. Meridian's testing approach is risk-based: test cases are prioritized by the "
        "criticality of the underlying business process and the complexity of the technical implementation. "
        "Testing overlaps with the final Build sprints as completed components enter the test pipeline."
    )

    pdf.sub_heading("5.1", "System Integration Testing (SIT)")
    pdf.body(
        "SIT validates end-to-end business process flows across all integrated system components. Test scenarios "
        "are derived from the BPMN process models created during Design and cover both happy-path and exception "
        "flows. SIT is executed by the Meridian test team using structured test scripts in Azure DevOps Test Plans "
        "or Jira Xray, depending on the client's tooling standards."
    )

    pdf.sub_heading("5.2", "User Acceptance Testing (UAT)")
    pdf.body(
        "UAT is led by client business users with Meridian facilitation. Test scenarios are written in business "
        "language (not technical language) and map directly to the business requirements documented in the BRD. "
        "Meridian provides UAT coordinators, defect triage facilitators, and daily status reporting. UAT sign-off "
        "by the business process owners is a mandatory prerequisite for deployment."
    )

    pdf.sub_heading("5.3", "Performance and Regression Testing")
    pdf.body(
        "Performance testing validates that the solution meets NFR benchmarks under expected and peak load "
        "conditions. Load testing tools (Apache JMeter, Gatling, or k6) simulate concurrent user volumes at "
        "125% of projected peak. Regression testing ensures that defect fixes and late-stage configuration "
        "changes do not introduce unintended side effects. Automated regression suites are maintained throughout "
        "the Build and Test phases."
    )

    pdf.sub_heading("5.4", "Test Phase Deliverables")
    pdf.bullet_list([
        "Test Strategy and Test Plan documents",
        "SIT execution results with defect metrics",
        "UAT execution results with business sign-off",
        "Performance test results against NFR benchmarks",
        "Regression test suite and execution logs",
        "Defect aging and resolution reports",
        "Test Phase Summary Report and Go-Live Readiness Assessment",
    ])
    pdf.bold_body("Governance Checkpoint:", "Go-Live Readiness Gate. Steering Committee reviews test results, "
                   "outstanding defect counts (zero critical, near-zero high), performance benchmarks, UAT sign-off "
                   "status, and operational readiness. Formal Go/No-Go decision for production deployment.")

    # 6 - Phase 5: Deploy
    pdf.section_heading("6", "Phase 5: Deploy (Weeks 32-40)")
    pdf.body(
        "The Deploy phase transitions the solution from project delivery to business operations. This phase "
        "encompasses production cutover execution, hypercare support, knowledge transfer to the client's "
        "operational teams, and formal project closure. Meridian's deployment approach minimizes business "
        "disruption through detailed cutover planning and rehearsals."
    )

    pdf.sub_heading("6.1", "Cutover Planning and Execution")
    pdf.body(
        "The Cutover Plan is a minute-by-minute runbook that sequences all deployment activities, assigns "
        "responsibilities, defines rollback triggers and procedures, and establishes communication protocols. "
        "At least two cutover rehearsals are conducted in a production-mirror environment before the actual "
        "go-live event. The cutover window is negotiated with the client to minimize impact on business "
        "operations, typically scheduled over a weekend or holiday period."
    )

    pdf.sub_heading("6.2", "Hypercare and Stabilization")
    pdf.body(
        "Meridian provides a dedicated hypercare team for 2-4 weeks post go-live. The hypercare team operates "
        "on an enhanced support model with 12-hour coverage (extendable to 24/7 for critical deployments), "
        "15-minute response SLAs for severity-1 issues, and daily triage meetings with the client's operational "
        "leadership. Hypercare concludes with a formal Stabilization Assessment confirming that the solution is "
        "operating within defined tolerances."
    )

    pdf.sub_heading("6.3", "Knowledge Transfer")
    pdf.body(
        "Knowledge transfer begins during the Build phase and intensifies during Deploy. It includes formal "
        "training sessions for end users (role-based curricula), administrator training for IT operations, "
        "documentation handover (operations runbooks, configuration guides, architecture decision records), "
        "and shadowing periods where client staff work alongside Meridian consultants. Knowledge transfer "
        "effectiveness is measured through competency assessments and client readiness surveys."
    )

    pdf.sub_heading("6.4", "Deploy Phase Deliverables")
    pdf.bullet_list([
        "Cutover Plan and Execution Checklist",
        "Production deployment verification report",
        "Hypercare daily status reports and issue logs",
        "Knowledge transfer completion certificates",
        "Operations runbooks and support documentation",
        "Project Closure Report with lessons learned",
        "Benefits Realization Baseline for post-project tracking",
    ])
    pdf.bold_body("Governance Checkpoint:", "Project Closure Gate. Formal acceptance of all deliverables, "
                   "confirmation that knowledge transfer is complete, transition to BAU support, financial "
                   "close-out, and initiation of post-implementation review (scheduled 90 days after go-live).")

    # 7 - Governance Framework
    pdf.section_heading("7", "Cross-Phase Governance Framework")
    pdf.body(
        "Governance operates at three tiers throughout the project lifecycle. The Steering Committee (executive "
        "sponsors, C-suite representatives, Meridian Partner) meets monthly and at every phase gate to provide "
        "strategic direction and approve major decisions. The Project Board (project managers, workstream leads, "
        "business process owners) meets biweekly to manage scope, schedule, and budget. The Working Team "
        "(consultants, developers, testers, client SMEs) operates on a weekly cadence with daily standups "
        "during Build and Test phases."
    )
    pdf.body(
        "All governance forums follow standardized agenda templates, action-item tracking protocols, and "
        "escalation procedures. Decision logs are maintained in the project's SharePoint site and linked to "
        "the relevant phase deliverables. RAID (Risks, Assumptions, Issues, Dependencies) logs are reviewed "
        "at every governance forum and updated in real time."
    )

    # Cross-references -- Case Studies & Key Personnel
    pdf.section_heading("8", "Related Case Studies & Key Personnel")
    pdf.body(
        "The SPL has been successfully applied across engagements of all sizes and industries. "
        "The following case studies illustrate the SPL in practice across Meridian's client portfolio:"
    )
    pdf.bullet_list([
        "Financial Services Digital Transformation (Sarah Chen, Lead Partner) -- Core banking modernization demonstrating full SPL lifecycle execution at enterprise scale.",
        "Healthcare EHR Integration (Michael Torres, Lead Partner) -- Multi-system integration following SPL with intensive OCM and regulatory compliance requirements.",
        "Manufacturing ERP Transformation (James O'Sullivan, Lead Partner) -- SAP S/4HANA implementation utilizing SPL with augmented Build and Data Migration phases.",
        "Public Sector Cloud Migration (Dr. Priya Ramanathan, Lead Partner) -- FedRAMP-compliant cloud migration following SPL governance with enhanced security gate reviews.",
        "Retail Omnichannel Analytics (Robert Adeyemi, Lead Partner) -- Data platform modernization leveraging SPL with iterative analytics delivery sprints.",
        "Energy Sector Operational Technology (Lead Partner) -- OT/IT convergence program applying SPL with specialized safety and environmental compliance checkpoints.",
    ])

    # Cross-references -- Methodologies
    pdf.section_heading("9", "Related Meridian Methodologies")
    pdf.body(
        "The Standard Project Lifecycle integrates with and is supported by the following Meridian "
        "practice-specific methodologies and frameworks. Engagement teams should reference these "
        "documents for domain-specific guidance within each SPL phase:"
    )
    pdf.bullet_list([
        "Organizational Change Management Framework (v5.0) -- OCM activities are embedded in every SPL phase; the OCM Framework provides detailed guidance on stakeholder analysis, communications, training, and adoption measurement.",
        "Agile vs. Waterfall Delivery Methodology Guide (v3.0) -- Provides decision criteria and hybrid delivery models that operate within the SPL phase structure.",
        "Enterprise ERP Implementation Strategy (v2.3) -- SPL phases map directly to ERP implementation milestones; the ERP document provides platform-specific accelerators for SAP, Oracle, and Workday.",
        "Cloud Migration Methodology and Playbook (v3.5) -- Cloud migrations follow the SPL with augmented Discovery (Cloud Readiness Assessment) and Build (Migration Factory) activities.",
        "Cybersecurity Risk Assessment Methodology (v4.0) -- Security assessments are embedded in the SPL Design and Test phases; the Cybersecurity document provides the detailed assessment framework.",
        "Supply Chain Optimization Practice Guide (v2.1) -- Supply chain engagements follow the SPL with specialized analytical tools and industry benchmarks during Discovery and Design.",
        "Data, Analytics & AI Strategy Guide (v1.0) -- Data and AI engagements leverage the SPL with augmented current-state data maturity assessments and AI use case prioritization frameworks.",
    ])

    path = os.path.join(OUTPUT_DIR, "standard_project_lifecycle.pdf")
    pdf.output(path)
    print(f"  [1/7] {path}")


# ===========================================================================
# 2. Agile vs Waterfall
# ===========================================================================
def gen_agile_waterfall():
    pdf = MeridianPDF("Agile vs. Waterfall Delivery Methodology Guide", "3.0", "February 2026")
    pdf.cover_page()
    pdf.new_content_page()

    # 1
    pdf.section_heading("1", "Purpose and Scope")
    pdf.body(
        "This document provides Meridian engagement teams with a comprehensive guide for selecting, tailoring, "
        "and executing the appropriate delivery methodology for client engagements. The choice between Agile, "
        "Waterfall, and hybrid approaches has significant implications for project governance, stakeholder "
        "engagement, risk management, team structure, and ultimately, client outcomes. Meridian does not "
        "mandate a single methodology; rather, we equip our practitioners with the knowledge to make informed "
        "decisions based on engagement-specific factors."
    )

    # 2
    pdf.section_heading("2", "Methodology Selection Framework")
    pdf.body(
        "Meridian's Methodology Selection Matrix evaluates eight dimensions to recommend the optimal delivery "
        "approach for a given engagement. Each dimension is scored on a 1-5 scale, and the aggregate score "
        "maps to one of three methodology recommendations: Agile (score 32-40), Hybrid (score 20-31), or "
        "Waterfall (score 8-19)."
    )
    pdf.bullet_list([
        "Requirements Stability: Are requirements well-defined upfront (1) or expected to evolve (5)?",
        "Client Agile Maturity: Does the client have experienced Scrum teams (5) or no Agile experience (1)?",
        "Regulatory Constraints: Heavy compliance documentation required (1) vs. minimal (5)?",
        "Team Distribution: Fully co-located (5) vs. globally distributed across 4+ time zones (1)?",
        "Technology Risk: Proven, stable technology stack (1) vs. emerging/unproven technologies (5)?",
        "Time-to-Market Pressure: Flexible timeline (1) vs. hard competitive deadline (5)?",
        "Organizational Change Scope: Limited process change (1) vs. enterprise-wide transformation (5)?",
        "Stakeholder Availability: Limited access to business SMEs (1) vs. dedicated product owner (5)?",
    ])

    # 3
    pdf.section_heading("3", "Agile Delivery Model")
    pdf.sub_heading("3.1", "Core Principles at Meridian")
    pdf.body(
        "Meridian's Agile practice is grounded in the Agile Manifesto but adapted for the realities of "
        "large-scale consulting engagements where client organizations may be at varying levels of Agile "
        "maturity. We emphasize working software, customer collaboration, and responding to change while "
        "maintaining the governance rigor that enterprise clients and regulators expect."
    )

    pdf.sub_heading("3.2", "Sprint Ceremonies and Cadence")
    pdf.body(
        "Meridian standardizes on two-week sprints for most engagements, with one-week sprints available for "
        "rapid-prototyping phases and critical bug-fix periods. The sprint cadence includes the following "
        "ceremonies, each with defined durations, participants, and outputs."
    )
    pdf.bullet_list([
        "Sprint Planning (4 hours for a 2-week sprint): Product Owner presents prioritized backlog, team "
        "estimates using story points (modified Fibonacci scale), team commits to sprint goal.",
        "Daily Standup (15 minutes, timebox enforced): Each team member reports progress, plans, and blockers. "
        "Parking lot for detailed discussions. Scrum Master tracks velocity and removes impediments.",
        "Sprint Review / Demo (2 hours): Working increment demonstrated to stakeholders. Feedback captured "
        "as new backlog items. Acceptance criteria validated against Definition of Done.",
        "Sprint Retrospective (1.5 hours): Team reflects on process improvements. Action items assigned and "
        "tracked. Meridian uses the Start/Stop/Continue format by default.",
        "Backlog Refinement (ongoing, ~10% of sprint capacity): Stories elaborated, acceptance criteria "
        "defined, dependencies identified, estimates updated. Ensures the backlog is always ready for the "
        "next sprint planning session.",
    ])

    pdf.sub_heading("3.3", "Definition of Done (DoD)")
    pdf.body(
        "The Definition of Done is a quality gate that every user story must pass before it is considered "
        "complete. Meridian's standard DoD includes the following criteria, which may be extended based on "
        "engagement-specific requirements."
    )
    pdf.bullet_list([
        "Code complete and merged to the main branch via pull request",
        "Unit tests written and passing (minimum 80% code coverage)",
        "Integration tests passing in the CI/CD pipeline",
        "Code reviewed and approved by at least one peer",
        "Security scan (SAST/DAST) completed with no critical findings",
        "User-facing documentation updated",
        "Acceptance criteria verified by the Product Owner",
        "No open severity-1 or severity-2 defects against the story",
    ])

    pdf.sub_heading("3.4", "Velocity Tracking and Metrics")
    pdf.body(
        "Velocity is tracked as the number of story points completed per sprint. Meridian uses a rolling "
        "three-sprint average for forecasting purposes. Burndown charts are updated daily and displayed on "
        "the team's information radiator (physical board or Jira dashboard). Burnup charts provide a "
        "complementary view showing total scope against completed work, making scope changes visible. "
        "Additional metrics include sprint goal achievement rate (target: >85%), defect escape rate, "
        "and cycle time distribution."
    )

    pdf.sub_heading("3.5", "Agile at Scale: SAFe Framework")
    pdf.body(
        "For engagements involving multiple Agile teams (typically 4+ teams or 40+ team members), Meridian "
        "recommends the Scaled Agile Framework (SAFe) at the Essential or Large Solution configuration. "
        "SAFe introduces the Agile Release Train (ART) as the primary value delivery mechanism, operating "
        "on a 10-week Program Increment (PI) cadence. PI Planning is a two-day face-to-face event where "
        "all teams align on objectives, identify dependencies, and commit to PI goals. The Release Train "
        "Engineer (RTE) serves as the chief Scrum Master for the ART."
    )
    pdf.body(
        "Meridian has certified SAFe Program Consultants (SPCs) who can facilitate PI Planning, train "
        "Scrum Masters and Product Owners, and coach leadership on Lean-Agile principles. Our SAFe "
        "implementations typically achieve 30-40% improvement in time-to-market within three PIs."
    )

    # 4
    pdf.section_heading("4", "Waterfall Delivery Model")
    pdf.sub_heading("4.1", "When Waterfall Is Appropriate")
    pdf.body(
        "Waterfall remains the preferred methodology for engagements with fixed regulatory requirements, "
        "well-defined scope, limited stakeholder availability for iterative feedback, or contractual "
        "structures (e.g., firm-fixed-price) that demand detailed upfront planning. Meridian's Waterfall "
        "methodology aligns with the PMBOK Guide (7th Edition) and incorporates earned value management "
        "for quantitative progress tracking."
    )

    pdf.sub_heading("4.2", "Phase Gates and Milestones")
    pdf.body(
        "Waterfall projects are governed by formal phase gates that require documented deliverables, "
        "stakeholder sign-off, and Steering Committee approval before proceeding to the next phase. "
        "Key milestones include Requirements Baseline, Design Freeze, Code Complete, Test Complete, "
        "UAT Sign-Off, and Go-Live. Each milestone has defined entry criteria, exit criteria, and "
        "a formal review process."
    )

    pdf.sub_heading("4.3", "Risk Management in Waterfall")
    pdf.body(
        "Waterfall projects use a structured risk management approach with a formal Risk Register maintained "
        "throughout the project. Risks are identified through brainstorming sessions, historical analysis of "
        "similar engagements, and expert judgment. Each risk is assessed on probability (1-5) and impact (1-5) "
        "scales, and risks scoring 15+ on the P x I matrix are escalated to the Steering Committee with "
        "documented mitigation plans. Risk reviews are conducted biweekly."
    )

    # 5
    pdf.section_heading("5", "Hybrid Approaches")
    pdf.body(
        "Many Meridian engagements benefit from a hybrid approach that combines the predictability of Waterfall "
        "governance with the adaptability of Agile execution. The most common hybrid pattern is Water-Scrum-Fall: "
        "Waterfall phase gates at the project level with Agile sprints within the Build phase. This approach "
        "preserves the fixed-scope commitments that clients and procurement teams require while enabling "
        "iterative development and continuous stakeholder feedback during construction."
    )
    pdf.body(
        "Alternative hybrid patterns include Agile with Waterfall Milestones (Agile execution with contractual "
        "milestones mapped to specific sprint boundaries), Discovery-Agile (Waterfall discovery phase followed "
        "by fully Agile execution), and Parallel Tracks (Agile for software development, Waterfall for "
        "infrastructure and data migration running concurrently)."
    )

    # 6
    pdf.section_heading("6", "Tooling Standards")
    pdf.body(
        "Meridian maintains enterprise licenses and certified practitioners for the following project "
        "management and collaboration tools. Tool selection is based on client preferences, existing "
        "ecosystem, and engagement requirements."
    )
    pdf.bullet_list([
        "Jira (Atlassian): Primary tool for Agile backlog management, sprint tracking, and reporting. "
        "Supported configurations include Scrum boards, Kanban boards, and SAFe program boards.",
        "Azure DevOps: Preferred for Microsoft-centric clients. Provides integrated backlog management, "
        "CI/CD pipelines, test plans, and artifact repositories.",
        "Smartsheet: Used for Waterfall schedule management, Gantt charts, resource allocation, and "
        "executive-level reporting dashboards. Integrates with Power BI for advanced analytics.",
        "Confluence: Knowledge management and documentation platform. Project wikis, decision logs, "
        "and architecture decision records (ADRs) are maintained in Confluence.",
        "Microsoft Project / Project Online: Used for large Waterfall programs requiring earned value "
        "management, critical path analysis, and resource leveling.",
    ])

    # 7
    pdf.section_heading("7", "Client Stakeholder Engagement")
    pdf.body(
        "Stakeholder engagement models differ significantly between Agile and Waterfall, and selecting the "
        "right model is critical for project success. In Agile, the Product Owner is embedded with the delivery "
        "team and provides continuous prioritization and acceptance decisions. Stakeholder demos occur every "
        "two weeks, enabling rapid course correction. In Waterfall, stakeholder engagement is concentrated at "
        "phase gates and formal review sessions, with structured change request processes for mid-project "
        "adjustments."
    )
    pdf.body(
        "Regardless of methodology, Meridian requires a named Executive Sponsor with decision-making authority, "
        "a dedicated client Project Manager as the primary counterpart to Meridian's engagement manager, and "
        "identified Subject Matter Experts (SMEs) with allocated time for project participation. Our engagement "
        "success data shows that projects with >20% dedicated client SME time achieve 2.3x higher satisfaction "
        "scores than those with ad-hoc availability."
    )

    # 8
    pdf.section_heading("8", "Related Case Studies & Key Personnel")
    pdf.body(
        "Methodology selection decisions are illustrated in the following Standard Project Lifecycle "
        "case examples, which demonstrate Agile, Waterfall, and hybrid approaches in practice:"
    )
    pdf.bullet_list([
        "Retail Omnichannel Analytics -- Agile delivery with two-week sprints for iterative dashboard and ML model development. See Standard Project Lifecycle case study references.",
        "Manufacturing ERP Transformation -- Hybrid (Water-Scrum-Fall) approach: Waterfall governance with Agile sprints during SAP S/4HANA Build phase.",
        "Public Sector Cloud Migration -- Waterfall methodology selected due to FedRAMP compliance documentation requirements and fixed-price contract structure.",
        "Healthcare EHR Integration -- Hybrid approach with Agile development and Waterfall phase gates aligned to regulatory validation milestones.",
    ])

    # 9
    pdf.section_heading("9", "Related Meridian Methodologies")
    pdf.body(
        "The Agile vs. Waterfall methodology selection integrates with the following Meridian "
        "practice documents:"
    )
    pdf.bullet_list([
        "Standard Project Lifecycle Framework (v4.2) -- Both Agile and Waterfall delivery operate within the SPL's five-phase structure and governance checkpoints.",
        "Enterprise ERP Implementation Strategy (v2.3) -- ERP engagements use methodology selection criteria from this guide to determine whether Activate (Agile-aligned) or Waterfall-based delivery is appropriate.",
        "Organizational Change Management Framework (v5.0) -- OCM engagement models are calibrated to the selected delivery methodology (continuous Agile OCM vs. phase-gate Waterfall OCM).",
    ])

    path = os.path.join(OUTPUT_DIR, "agile_vs_waterfall.pdf")
    pdf.output(path)
    print(f"  [2/7] {path}")


# ===========================================================================
# 3. Organizational Change Management
# ===========================================================================
def gen_ocm():
    pdf = MeridianPDF("Organizational Change Management Framework", "5.0", "December 2025")
    pdf.cover_page()
    pdf.new_content_page()

    # 1
    pdf.section_heading("1", "Introduction to Meridian's OCM Approach")
    pdf.body(
        "Organizational Change Management (OCM) is a critical success factor for every transformation "
        "engagement. Meridian's research across 800+ completed projects confirms that initiatives with "
        "dedicated OCM workstreams are 3.4 times more likely to achieve their stated business objectives "
        "than those without structured change management. Our OCM framework integrates industry-leading "
        "methodologies, including Prosci ADKAR, Kotter's 8-Step Model, and the Bridges Transition Model, "
        "into a cohesive, practical approach tailored to the realities of large-scale enterprise transformation."
    )
    pdf.body(
        "The framework is organized around six pillars: Stakeholder Engagement, Communication, Training, "
        "Resistance Management, Adoption Measurement, and Sustainment. Each pillar operates across all "
        "project phases, with activities and deliverables calibrated to the current phase of the delivery "
        "lifecycle. OCM is not an afterthought or a supplementary workstream; it is a co-equal delivery "
        "track with dedicated resources, budget, and governance."
    )

    # 2
    pdf.section_heading("2", "Stakeholder Analysis and Influence Mapping")
    pdf.body(
        "Effective change management begins with a thorough understanding of who is affected by the change, "
        "how they are affected, and what influence they wield over the outcome. Meridian's stakeholder analysis "
        "follows a three-step process: identification, assessment, and engagement strategy development."
    )
    pdf.sub_heading("2.1", "Stakeholder Identification")
    pdf.body(
        "Using organizational charts, RACI matrices, and sponsor interviews, the OCM team identifies all "
        "individuals and groups who will be impacted by the change. Stakeholders are categorized into tiers: "
        "Tier 1 (directly impacted, daily workflow changes), Tier 2 (indirectly impacted, process or reporting "
        "changes), and Tier 3 (minimally impacted, awareness only). Each tier receives a calibrated level of "
        "OCM support and communication."
    )
    pdf.sub_heading("2.2", "Influence and Impact Mapping")
    pdf.body(
        "Each stakeholder or stakeholder group is plotted on a two-axis matrix: Level of Impact (how "
        "significantly their work will change) and Level of Influence (their ability to accelerate or "
        "derail adoption). High-impact, high-influence stakeholders receive intensive engagement including "
        "one-on-one coaching, early access to the solution, and roles as Change Champions. The influence "
        "map is revisited monthly and adjusted as organizational dynamics evolve."
    )

    # 3
    pdf.section_heading("3", "Change Impact Assessment")
    pdf.body(
        "The Change Impact Assessment (CIA) is a structured analysis of how the transformation will alter "
        "roles, processes, technology, organizational structure, and culture. For each impacted area, the "
        "CIA documents the current state, future state, magnitude of change (low/medium/high), affected "
        "populations, and recommended change interventions. The CIA is a living document updated as the "
        "solution design evolves during the Build phase."
    )
    pdf.bullet_list([
        "Process changes: New workflows, eliminated steps, altered approval chains, new handoff points",
        "Technology changes: New systems, retired systems, changed interfaces, new data entry requirements",
        "Role changes: New responsibilities, eliminated tasks, reporting structure changes, new skills required",
        "Cultural changes: Shift from siloed to collaborative, manual to automated, reactive to proactive",
        "Performance management changes: New KPIs, revised targets, altered incentive structures",
    ])

    # 4
    pdf.section_heading("4", "Communication Planning")
    pdf.body(
        "Meridian's communication strategy follows the principle of 'right message, right audience, right "
        "channel, right time.' The communication plan is a detailed calendar of messages, events, and "
        "touchpoints aligned to the project timeline and major milestones."
    )
    pdf.sub_heading("4.1", "Communication Channels")
    pdf.bullet_list([
        "Executive town halls: Quarterly sessions led by the Executive Sponsor. 45-60 minutes with live Q&A. "
        "Purpose: strategic context, progress updates, reinforcement of vision and commitment.",
        "Email newsletters: Biweekly during Design/Build, weekly during Deploy. Short, scannable format with "
        "key updates, upcoming milestones, and 'spotlight' features on team members or early wins.",
        "Intranet hub: Dedicated project page with FAQs, training resources, timeline, team contacts, and "
        "feedback submission form. Updated weekly by the OCM team.",
        "Manager talking points: Monthly one-page briefs for people managers to cascade key messages during "
        "team meetings. Ensures consistent messaging across the organization.",
        "Digital signage and screensavers: Awareness-level messaging in high-traffic areas during the "
        "pre-launch and launch periods.",
    ])

    pdf.sub_heading("4.2", "Message Architecture")
    pdf.body(
        "All communications follow Meridian's WIIFM (What's In It For Me) message architecture. Every "
        "message addresses three questions from the audience's perspective: Why is this change happening? "
        "How will it affect me specifically? Where can I get help? Messages are tailored by stakeholder "
        "tier and role, ensuring relevance and reducing information overload."
    )

    # 5
    pdf.section_heading("5", "Training Needs Analysis and Curriculum Design")
    pdf.body(
        "Training is designed to bridge the gap between current capabilities and the skills required to "
        "operate effectively in the future state. The Training Needs Analysis (TNA) maps each role to the "
        "specific system features, processes, and behaviors they will need to master. The TNA produces a "
        "role-to-training matrix that governs curriculum design and training delivery scheduling."
    )
    pdf.bullet_list([
        "Instructor-led training (ILT): 2-4 hour sessions for complex processes, hands-on system training, "
        "and role-specific workflows. Maximum class size of 15 for effective interaction.",
        "Virtual instructor-led training (VILT): Same content as ILT, adapted for remote delivery via "
        "Microsoft Teams or Zoom. Breakout rooms for practice exercises.",
        "Self-paced e-learning: Short modules (10-15 minutes) for awareness topics and refresher content. "
        "Hosted on the client's LMS or Meridian's training portal.",
        "Quick reference guides (QRGs): One-page, task-oriented job aids laminated and posted at workstations. "
        "Digital versions available via QR codes.",
        "Simulation environments: Sandbox systems with realistic data for hands-on practice. Available "
        "for 30 days post go-live.",
    ])

    # 6
    pdf.section_heading("6", "Resistance Management")
    pdf.body(
        "Resistance is a natural human response to change, not a failure of communication or training. "
        "Meridian's resistance management approach seeks to understand the root causes of resistance and "
        "address them through targeted interventions rather than coercion or dismissal."
    )
    pdf.sub_heading("6.1", "Root Cause Analysis")
    pdf.body(
        "Common root causes include fear of job loss, perceived loss of expertise or status, disagreement "
        "with the direction of change, change fatigue from previous initiatives, lack of trust in leadership, "
        "and insufficient understanding of the rationale. The OCM team uses pulse surveys, focus groups, and "
        "manager feedback channels to continuously monitor resistance signals."
    )
    pdf.sub_heading("6.2", "Intervention Strategies")
    pdf.bullet_list([
        "Active listening sessions: Small-group forums where concerns are heard without judgment and "
        "documented for leadership response.",
        "Peer advocacy: Change Champions drawn from respected colleagues who model adoption and provide "
        "informal coaching to their peers.",
        "Quick wins: Early demonstrations of value that build confidence in the change direction.",
        "Manager coaching: Equipping people managers with skills to have difficult conversations about "
        "change and to recognize resistance signals in their teams.",
        "Escalation protocol: Persistent, high-impact resistance that threatens project outcomes is "
        "escalated to the Steering Committee with recommended interventions.",
    ])

    # 7
    pdf.section_heading("7", "Adoption Metrics and Measurement")
    pdf.body(
        "Meridian tracks adoption through a balanced scorecard of leading and lagging indicators. Metrics "
        "are reported weekly during the Deploy phase and monthly during sustainment."
    )
    pdf.bullet_list([
        "Daily Active Users (DAU): System login and feature utilization data compared against expected "
        "adoption curves. Target: 80% DAU within 30 days of go-live.",
        "Feature utilization rates: Percentage of target users utilizing key features. Tracked at the "
        "individual feature level to identify training gaps.",
        "Support ticket volume and trends: Volume of how-to tickets vs. break-fix tickets. Declining "
        "how-to tickets indicate effective training; rising break-fix tickets indicate system issues.",
        "Training completion rates: Percentage of users who have completed required training modules. "
        "Target: 95% completion before go-live.",
        "User satisfaction surveys: Net Promoter Score (NPS) and task-completion confidence ratings "
        "administered at go-live, 30 days, and 90 days.",
        "Proficiency assessments: Skills-based evaluations aligned to the training curriculum. "
        "Minimum passing score of 80% required for role certification.",
    ])

    # 8
    pdf.section_heading("8", "Change Champion Network")
    pdf.body(
        "Change Champions are a volunteer network of 20-40 individuals drawn from across the impacted "
        "organization. Selected for their credibility, influence, and enthusiasm, Champions receive "
        "advanced training on the solution and change management principles. They serve as local advocates, "
        "feedback conduits, and peer coaches. The Champion network meets biweekly with the OCM team to "
        "share field intelligence, discuss emerging resistance patterns, and coordinate local activities."
    )

    # 9
    pdf.section_heading("9", "Prosci ADKAR Integration")
    pdf.body(
        "Meridian integrates the Prosci ADKAR model as the individual change management framework within "
        "our broader OCM approach. ADKAR provides a structured way to assess and address individual readiness "
        "across five sequential elements: Awareness of the need for change, Desire to participate and support "
        "the change, Knowledge of how to change, Ability to implement required skills and behaviors, and "
        "Reinforcement to sustain the change. ADKAR assessments are administered at key milestones (end of "
        "Design, mid-Build, pre-Deploy, and 30 days post go-live) to identify barrier points and target "
        "interventions at the specific ADKAR element where individuals are stuck."
    )

    # 10
    pdf.section_heading("10", "Post-Go-Live Sustainment")
    pdf.body(
        "Sustainment planning begins during the Build phase and extends 90-180 days beyond go-live. The "
        "sustainment plan transitions OCM activities from the project team to the client's permanent "
        "organization. Key sustainment elements include a designated Change Sustainability Lead within the "
        "client organization, an ongoing Champion network with quarterly check-ins, refresher training "
        "triggered by adoption metric thresholds, a continuous improvement feedback loop connected to the "
        "IT service management process, and annual change readiness assessments to support future "
        "initiatives building on the current transformation."
    )

    # 11
    pdf.section_heading("11", "Related Case Studies & Key Personnel")
    pdf.body(
        "The following case study and key personnel are directly relevant to organizational change management engagements:"
    )
    pdf.bullet_list([
        "Healthcare EHR Integration Case Study -- $18B health system; enterprise-wide EHR integration affecting 45,000+ clinical and administrative staff; led by Michael Torres, Lead Partner. Achieved 94% end-user adoption within 60 days of go-live through intensive OCM program.",
        "Lauren Mitchell, Senior Manager -- OCM Practice Lead, Prosci-certified Advanced Practitioner with 15+ years of experience leading change management for large-scale ERP, cloud, and digital transformation programs across healthcare, financial services, and manufacturing.",
    ])

    # 12
    pdf.section_heading("12", "Related Meridian Methodologies")
    pdf.body(
        "OCM is a cross-cutting discipline that supports all Advisory and Consulting engagements. "
        "The following documents describe engagements where OCM is most intensively deployed:"
    )
    pdf.bullet_list([
        "Standard Project Lifecycle Framework (v4.2) -- OCM activities are mapped to each SPL phase; this document provides the overarching delivery governance.",
        "Enterprise ERP Implementation Strategy (v2.3) -- ERP transformations are the most OCM-intensive engagement type; the ERP document details platform-specific change impacts.",
        "Cloud Migration Methodology and Playbook (v3.5) -- Cloud migrations require OCM for IT operations teams adopting new operating models and toolsets.",
        "Data, Analytics & AI Strategy Guide (v1.0) -- Data literacy programs and AI adoption initiatives are supported by the OCM Framework's training and adoption measurement pillars.",
    ])

    path = os.path.join(OUTPUT_DIR, "organizational_change_management.pdf")
    pdf.output(path)
    print(f"  [3/7] {path}")


# ===========================================================================
# 4. ERP Implementation Strategy
# ===========================================================================
def gen_erp():
    pdf = MeridianPDF("Enterprise ERP Implementation Strategy", "2.3", "November 2025")
    pdf.cover_page()
    pdf.new_content_page()

    # 1
    pdf.section_heading("1", "Executive Summary")
    pdf.body(
        "Enterprise Resource Planning (ERP) transformations represent the most complex and consequential "
        "technology programs that organizations undertake. With typical investments ranging from $15M to "
        "$150M+ for Fortune 500 companies, and implementation timelines spanning 14 to 36 months, the "
        "stakes are extraordinarily high. Meridian & Associates has delivered 180+ ERP implementations "
        "across SAP S/4HANA, Oracle Cloud ERP, and Workday, with an on-time, on-budget delivery rate of "
        "87% -- significantly above the industry average of 52% reported by Panorama Consulting."
    )
    pdf.body(
        "This document outlines Meridian's ERP implementation strategy, covering the full lifecycle from "
        "vendor selection through post-implementation optimization. Our approach is vendor-agnostic at the "
        "strategic level while incorporating platform-specific accelerators and best practices at the "
        "execution level."
    )

    # 2
    pdf.section_heading("2", "Assessment and Vendor Selection")
    pdf.sub_heading("2.1", "Business Case Development")
    pdf.body(
        "Before committing to an ERP transformation, Meridian helps clients develop a rigorous business case "
        "that quantifies expected benefits (cost reduction, revenue enablement, risk mitigation, operational "
        "efficiency), estimates total cost of ownership (TCO) over a 7-10 year horizon, and identifies "
        "intangible benefits such as improved decision-making, regulatory compliance readiness, and talent "
        "attraction. The business case includes a sensitivity analysis with optimistic, base, and pessimistic "
        "scenarios."
    )

    pdf.sub_heading("2.2", "Vendor Evaluation Framework")
    pdf.body(
        "Meridian's vendor evaluation uses a weighted scoring model across 12 dimensions: functional fit, "
        "technical architecture, integration capabilities, total cost of ownership, vendor financial stability, "
        "industry-specific functionality, user experience, mobile capabilities, analytics and reporting, "
        "extensibility, vendor support model, and implementation partner ecosystem. Clients participate in "
        "scripted demonstrations using their own business scenarios, and Meridian provides independent "
        "assessment of each vendor's strengths and limitations."
    )

    # 3
    pdf.section_heading("3", "Implementation Methodologies")
    pdf.sub_heading("3.1", "SAP Activate for S/4HANA")
    pdf.body(
        "For SAP S/4HANA implementations, Meridian follows the SAP Activate methodology with firm-specific "
        "enhancements. SAP Activate consists of six phases: Discover, Prepare, Explore, Realize, Deploy, and "
        "Run. Meridian's accelerators include pre-configured Fit-to-Standard workshop templates for 15 "
        "industries, pre-built data migration objects for common source systems (SAP ECC, Oracle E-Business "
        "Suite, JD Edwards), and integration content packages for Salesforce, Workday, and Ariba."
    )
    pdf.body(
        "Our S/4HANA practice emphasizes a 'Fit-to-Standard' approach that maximizes the use of SAP's "
        "standard processes and minimizes custom development. Experience shows that implementations with "
        "less than 15% customization achieve 40% faster go-live timelines and 60% lower total cost of "
        "ownership compared to heavily customized deployments."
    )

    pdf.sub_heading("3.2", "Oracle Unified Method (OUM)")
    pdf.body(
        "Oracle Cloud ERP implementations follow the Oracle Unified Method, which Meridian augments with "
        "additional data migration rigor and change management activities. OUM's iterative approach aligns "
        "well with Oracle's quarterly release cadence, and Meridian's Oracle practice maintains a regression "
        "testing framework that validates client-specific configurations against each quarterly update. Key "
        "modules include Financials (GL, AP, AR, FA), Procurement (PO, Sourcing, Supplier Qualification), "
        "and Project Portfolio Management."
    )

    pdf.sub_heading("3.3", "Workday Deployment Methodology")
    pdf.body(
        "Workday implementations follow a tenant-based deployment model with Meridian serving as the "
        "deployment partner. Our Workday practice specializes in HCM (Core HR, Compensation, Benefits, "
        "Talent Management, Recruiting) and Financials (GL, Accounts Payable, Revenue Management). Meridian's "
        "Workday accelerators include pre-built integration templates for ADP, Ceridian, and major payroll "
        "providers, as well as data conversion templates for PeopleSoft, SAP HR, and legacy HRIS systems."
    )

    # 4
    pdf.section_heading("4", "Data Migration Strategy")
    pdf.body(
        "Data migration is consistently the highest-risk workstream in ERP implementations. Meridian's data "
        "migration methodology consists of four phases executed iteratively across multiple mock migration "
        "cycles."
    )
    pdf.sub_heading("4.1", "Extract")
    pdf.body(
        "Data is extracted from source systems using automated extraction scripts that are version-controlled "
        "and repeatable. Extraction includes both structured data (database tables, flat files) and "
        "unstructured data (attachments, documents, images). Source system data profiling is conducted using "
        "Informatica Data Quality or Talend to identify data quality issues before migration begins."
    )

    pdf.sub_heading("4.2", "Cleanse and Transform")
    pdf.body(
        "Data cleansing addresses duplicates, missing values, format inconsistencies, and business rule "
        "violations. Transformation rules map source data structures to target data models, applying "
        "conversions (e.g., chart of accounts mapping, currency conversion, unit of measure standardization). "
        "All transformation rules are documented in a Data Mapping Specification and approved by data stewards "
        "from the client organization."
    )

    pdf.sub_heading("4.3", "Validate and Load")
    pdf.body(
        "Validation occurs at multiple levels: field-level (data type, format, range), record-level (business "
        "rule compliance, referential integrity), and set-level (completeness, reconciliation with source "
        "totals). Loading is performed using the target system's native data import tools (SAP Data Services, "
        "Oracle FBDI, Workday EIB) with automated error handling and retry logic. A minimum of three full mock "
        "migrations are conducted, each followed by a reconciliation report reviewed by the data migration lead "
        "and client data stewards."
    )

    # 5
    pdf.section_heading("5", "Integration Architecture")
    pdf.body(
        "Modern ERP implementations require integration with 15-50 adjacent systems. Meridian designs "
        "integration architectures that balance reliability, performance, and maintainability."
    )
    pdf.bullet_list([
        "Middleware platforms: MuleSoft Anypoint, Dell Boomi, Azure Integration Services, SAP BTP Integration "
        "Suite. Platform selection based on client's existing landscape and total integration volume.",
        "API-first design: RESTful APIs with OpenAPI 3.0 specifications for synchronous integrations. "
        "Event-driven architectures (Kafka, Azure Event Hubs) for real-time, high-volume data streams.",
        "Batch integration: Scheduled file-based transfers for high-volume, non-time-sensitive data "
        "(e.g., nightly GL journal entries, weekly payroll files). SFTP with PGP encryption for security.",
        "Real-time vs. near-real-time: Decision framework based on business criticality, data volume, "
        "system capabilities, and cost. Real-time integration adds 40-60% cost over batch alternatives.",
    ])

    # 6
    pdf.section_heading("6", "Business Process Reengineering")
    pdf.body(
        "ERP implementations provide a once-in-a-decade opportunity to redesign business processes. Meridian's "
        "BPR approach uses value stream mapping to identify waste, bottlenecks, and non-value-added activities "
        "in current processes. Future-state processes are designed to leverage ERP platform capabilities while "
        "incorporating industry best practices. Process designs are validated through Conference Room Pilots "
        "(CRPs) where business users execute realistic scenarios in the configured system."
    )
    pdf.sub_heading("6.1", "Chart of Accounts Redesign")
    pdf.body(
        "The chart of accounts (CoA) is the backbone of financial reporting and often requires significant "
        "redesign during ERP transformation. Meridian's CoA redesign approach balances statutory reporting "
        "requirements, management reporting needs, operational tracking, and intercompany accounting with "
        "the goal of simplification. Typical outcomes include a 30-50% reduction in the number of natural "
        "accounts, elimination of segment value proliferation, and alignment with the organization's future "
        "operating model."
    )

    # 7
    pdf.section_heading("7", "Cutover Planning and Dual Maintenance")
    pdf.body(
        "The cutover period -- the window between freezing the legacy system and going live on the new ERP -- "
        "is the highest-risk phase of the implementation. Meridian develops a detailed cutover plan that "
        "includes data freeze procedures, final data migration execution, system configuration lockdown, "
        "integration activation sequence, user provisioning, and validation checklists. Rollback criteria "
        "and procedures are defined in advance and rehearsed."
    )
    pdf.body(
        "During the dual maintenance period (typically 2-4 weeks pre-cutover), transactions entered in "
        "the legacy system must be replicated in the new ERP. Meridian provides dual-entry teams and "
        "automated synchronization scripts to minimize the risk of data discrepancies during this critical "
        "window."
    )

    # 8
    pdf.section_heading("8", "Timeline Guidelines")
    pdf.body(
        "ERP implementation timelines vary significantly based on organizational complexity, geographic "
        "scope, number of modules, and customization requirements. Meridian's benchmarks, based on "
        "historical engagement data, provide the following guidance."
    )
    pdf.bullet_list([
        "Mid-market (single entity, 500-2,000 employees, 3-5 modules): 14-18 months",
        "Upper mid-market (multi-entity, 2,000-10,000 employees, 5-8 modules): 18-24 months",
        "Enterprise (global, 10,000+ employees, full-suite deployment): 24-36 months",
        "Phased rollout (regional waves): Add 6-12 months per wave after initial go-live",
        "Post-implementation optimization: 6-12 month engagement beginning 90 days after go-live",
    ])

    # 9
    pdf.section_heading("9", "Related Case Studies & Key Personnel")
    pdf.body(
        "The following case study and key personnel are directly relevant to ERP implementation engagements:"
    )
    pdf.bullet_list([
        "Manufacturing ERP Transformation Case Study -- $4.8B global manufacturer; SAP S/4HANA implementation across 12 plants; led by James O'Sullivan, Lead Partner. Delivered on-time with 23% improvement in order-to-cash cycle time.",
        "David Kim, Managing Director -- ERP Practice Lead with 18+ years of SAP and Oracle implementation experience across manufacturing, distribution, and financial services.",
        "Marcus Wright, Senior Manager -- SAP S/4HANA certified architect specializing in Fit-to-Standard implementations and data migration for complex multi-entity deployments.",
        "Kwame Asante, Senior Manager -- SAP FICO specialist with deep expertise in chart of accounts redesign, intercompany accounting, and financial close optimization.",
    ])

    # 10
    pdf.section_heading("10", "Related Meridian Methodologies")
    pdf.body(
        "ERP implementations draw on expertise and frameworks from across Meridian's Advisory practice. "
        "The following documents provide supporting methodologies referenced throughout this guide:"
    )
    pdf.bullet_list([
        "Standard Project Lifecycle Framework (v4.2) -- The SPL provides the overarching delivery governance under which all ERP engagements operate.",
        "Organizational Change Management Framework (v5.0) -- ERP transformations require intensive OCM; Meridian mandates a dedicated OCM workstream for all ERP engagements exceeding $5M in contract value.",
        "Cybersecurity Risk Assessment Methodology (v4.0) -- Security assessments are embedded during the ERP Design phase to ensure the target architecture meets the client's security and compliance requirements.",
        "Cloud Migration Methodology and Playbook (v3.5) -- Cloud ERP deployments (SAP S/4HANA Cloud, Oracle Cloud ERP, Workday) follow the Cloud Migration landing zone and security frameworks in parallel with ERP configuration.",
        "Data, Analytics & AI Strategy Guide (v1.0) -- Data migration quality and post-go-live analytics strategy are supported by the firm's data governance and BI/reporting frameworks.",
    ])

    # 11
    pdf.section_heading("11", "Engagement Approach")
    pdf.body(
        "A typical Meridian ERP implementation engagement follows the timeline and team structure "
        "outlined below. Actual parameters are adjusted based on scope, organizational complexity, "
        "and geographic distribution."
    )
    pdf.bullet_list([
        "Timeline: 18-24 months for an upper mid-market engagement (5-8 modules, 2,000-10,000 employees); 24-36 months for global enterprise deployments.",
        "Team Composition: 1 Engagement Partner, 1 Program Director, 2-4 Workstream Leads (Functional, Technical, Data Migration, OCM), 6-15 Senior Consultants and Consultants, 1 Quality Assurance Director (part-time oversight).",
        "Key Deliverables: Business Case and Vendor Selection Report, Solution Blueprint, Configured System (sprint increments), Data Migration Reconciliation Report, Test Summary Report, Cutover Plan and Execution Checklist, Hypercare Status Reports, Knowledge Transfer Completion Package, Project Closure and Lessons Learned Report.",
    ])

    path = os.path.join(OUTPUT_DIR, "erp_implementation_strategy.pdf")
    pdf.output(path)
    print(f"  [4/7] {path}")


# ===========================================================================
# 5. Cloud Migration Methodology
# ===========================================================================
def gen_cloud_migration():
    pdf = MeridianPDF("Cloud Migration Methodology and Playbook", "3.5", "March 2026")
    pdf.cover_page()
    pdf.new_content_page()

    # 1
    pdf.section_heading("1", "Introduction")
    pdf.body(
        "Cloud migration is a strategic imperative for organizations seeking to modernize their technology "
        "estate, improve operational agility, reduce infrastructure costs, and accelerate innovation. "
        "Meridian & Associates has executed 250+ cloud migration programs, collectively migrating over "
        "18,000 workloads to AWS, Microsoft Azure, and Google Cloud Platform. This playbook codifies our "
        "methodology, tools, and lessons learned into a repeatable framework that Meridian engagement teams "
        "can apply to migrations of any scale."
    )

    # 2
    pdf.section_heading("2", "The 6R Migration Framework")
    pdf.body(
        "Meridian's migration strategy is anchored in the 6R framework, which classifies every application "
        "and workload into one of six disposition categories. The 6R assessment is conducted during the "
        "Discovery phase and drives the migration approach, timeline, and cost for each workload."
    )
    pdf.sub_heading("2.1", "Rehost (Lift and Shift)")
    pdf.body(
        "Rehosting moves workloads to the cloud with minimal or no changes to the application architecture. "
        "This is the fastest migration path and is appropriate for applications with limited business "
        "differentiation, approaching end-of-life, or where the primary goal is data center exit. Rehosting "
        "typically achieves 20-30% cost savings from infrastructure consolidation and reserved instance "
        "pricing alone. Tools: AWS Application Migration Service, Azure Migrate, Google Migrate for Compute."
    )

    pdf.sub_heading("2.2", "Replatform (Lift, Tinker, and Shift)")
    pdf.body(
        "Replatforming involves targeted optimizations during migration without changing the core architecture. "
        "Common replatforming moves include migrating databases to managed services (RDS, Azure SQL, Cloud SQL), "
        "containerizing applications with Docker/Kubernetes, and replacing self-managed middleware with PaaS "
        "equivalents. Replatforming adds 15-25% effort over rehosting but typically delivers 35-50% cost "
        "savings through managed service efficiencies."
    )

    pdf.sub_heading("2.3", "Refactor (Re-architect)")
    pdf.body(
        "Refactoring involves significant architecture changes to leverage cloud-native capabilities such as "
        "serverless computing (Lambda, Azure Functions), event-driven architectures, microservices decomposition, "
        "and managed AI/ML services. Refactoring delivers the highest long-term value but requires the most "
        "investment (3-5x the effort of rehosting). Meridian recommends refactoring for strategic, high-value "
        "applications that will remain in the portfolio for 5+ years."
    )

    pdf.sub_heading("2.4", "Repurchase (Drop and Shop)")
    pdf.body(
        "Repurchasing replaces an existing application with a SaaS equivalent (e.g., on-premises Exchange to "
        "Microsoft 365, custom CRM to Salesforce, on-premises ITSM to ServiceNow). The migration effort "
        "shifts from infrastructure to data migration and process adaptation. Meridian's SaaS transition "
        "practice provides vendor evaluation, data migration, integration design, and change management "
        "for repurchase scenarios."
    )

    pdf.sub_heading("2.5", "Retire")
    pdf.body(
        "Retirement decommissions applications that are no longer needed, redundant, or superseded by other "
        "systems. Meridian's portfolio rationalization analysis typically identifies 10-20% of applications "
        "as retirement candidates, reducing the migration scope and ongoing licensing and support costs. "
        "Retirement requires careful data archival and regulatory retention compliance."
    )

    pdf.sub_heading("2.6", "Retain")
    pdf.body(
        "Retention keeps applications in their current environment, either permanently (e.g., mainframe "
        "applications with prohibitive migration costs) or temporarily (deferred to a future migration wave). "
        "Retained applications require hybrid connectivity design (VPN, Direct Connect, ExpressRoute) and "
        "ongoing operational support planning."
    )

    # 3
    pdf.section_heading("3", "Cloud Readiness Assessment")
    pdf.body(
        "The Cloud Readiness Assessment (CRA) evaluates the organization's preparedness across six dimensions: "
        "application portfolio (technical debt, dependencies, licensing), infrastructure (network, compute, "
        "storage baseline), security and compliance (regulatory requirements, data residency, encryption "
        "standards), operations (monitoring, incident management, automation maturity), organizational "
        "readiness (cloud skills, team structure, vendor management), and financial readiness (FinOps "
        "capabilities, budget allocation, chargeback models)."
    )
    pdf.body(
        "Each dimension is scored on a five-level maturity scale: Initial (ad-hoc), Developing (documented), "
        "Defined (standardized), Managed (measured), and Optimizing (continuously improving). The CRA produces "
        "a roadmap of remediation activities that must be completed before or in parallel with migration waves."
    )

    # 4
    pdf.section_heading("4", "Landing Zone Architecture")
    pdf.body(
        "The landing zone is the foundational cloud environment that provides identity management, network "
        "architecture, security controls, logging, and governance guardrails for all migrated workloads. "
        "Meridian designs landing zones using the cloud provider's reference architectures as a starting "
        "point, customized for the client's specific requirements."
    )
    pdf.bullet_list([
        "AWS: Control Tower with Account Factory for Terraform (AFT), Service Control Policies, centralized "
        "logging via CloudTrail and Security Hub, transit gateway for network connectivity.",
        "Azure: Cloud Adoption Framework Landing Zones with Management Groups, Azure Policy for governance, "
        "Azure Monitor and Sentinel for observability and security, Hub-and-Spoke network topology.",
        "GCP: Resource hierarchy with Organizations, Folders, and Projects, Organization Policies, "
        "Cloud Logging and Security Command Center, Shared VPC for network isolation.",
    ])
    pdf.body(
        "Landing zone deployment is automated using Infrastructure-as-Code (Terraform, Bicep, or CloudFormation) "
        "and version-controlled in Git. Meridian maintains landing zone blueprints for 8 industry verticals "
        "(Financial Services, Healthcare, Government, Retail, Manufacturing, Energy, Media, Technology) that "
        "incorporate industry-specific compliance requirements."
    )

    # 5
    pdf.section_heading("5", "Migration Factory Model")
    pdf.body(
        "For large-scale migrations (200+ workloads), Meridian operates a Migration Factory model that "
        "industrializes the migration process through standardized patterns, automation, and parallel "
        "execution. The factory model consists of three swim lanes operating concurrently."
    )
    pdf.bullet_list([
        "Assessment Lane: Application discovery, dependency mapping, 6R categorization, migration "
        "planning. Throughput: 50-100 applications per wave assessed in 2-3 weeks.",
        "Migration Lane: Execution of migration runbooks for each 6R pattern. Automated tooling for "
        "rehost and replatform. Throughput: 50-100 workloads migrated per wave in 4-6 weeks.",
        "Validation Lane: Post-migration testing, performance benchmarking, security scanning, "
        "operational readiness. Throughput: aligned with Migration Lane output.",
    ])
    pdf.body(
        "Each migration wave follows a 10-week cadence: 2 weeks assessment, 4-6 weeks migration, 2 weeks "
        "validation and optimization. Waves overlap by 4 weeks, enabling continuous migration throughput. "
        "A typical enterprise migration completes in 4-6 waves over 9-15 months."
    )

    # 6
    pdf.section_heading("6", "Security and Compliance")
    pdf.body(
        "Cloud security is integrated into every phase of the migration, not bolted on afterward. Meridian's "
        "cloud security framework addresses identity and access management (IAM), network security, data "
        "protection, workload protection, and security operations."
    )
    pdf.bullet_list([
        "FedRAMP: For federal government clients, Meridian ensures that all cloud services are FedRAMP "
        "authorized at the appropriate impact level (Low, Moderate, High). Our FedRAMP practice includes "
        "System Security Plan (SSP) development and continuous monitoring.",
        "HIPAA: Healthcare clients require BAA agreements, PHI encryption at rest and in transit, access "
        "logging, and breach notification procedures. Meridian maintains HIPAA-compliant landing zone "
        "templates for all three major cloud providers.",
        "PCI-DSS: Payment card processing environments require network segmentation, vulnerability "
        "management, access controls, and audit logging per PCI-DSS v4.0 requirements.",
        "SOC 2 Type II: Meridian assists clients in achieving SOC 2 compliance for cloud-hosted services, "
        "covering Trust Service Criteria for security, availability, processing integrity, confidentiality, "
        "and privacy.",
    ])

    # 7
    pdf.section_heading("7", "FinOps and Cost Optimization")
    pdf.body(
        "Cloud cost management is a critical capability that many organizations underestimate. Without "
        "disciplined FinOps practices, cloud costs can exceed on-premises costs within 18-24 months of "
        "migration. Meridian's FinOps framework establishes the people, processes, and tools needed for "
        "continuous cost optimization."
    )
    pdf.bullet_list([
        "Cost visibility: Tagging standards, cost allocation to business units, showback/chargeback models, "
        "dashboard and reporting (CloudHealth, Azure Cost Management, AWS Cost Explorer).",
        "Rightsizing: Continuous analysis of compute, storage, and database utilization to identify "
        "over-provisioned resources. Typical savings: 25-40% of compute spend.",
        "Reserved capacity: Commitment-based discounts (Reserved Instances, Savings Plans, Committed Use "
        "Discounts) for predictable workloads. Typical savings: 30-60% vs. on-demand.",
        "Spot/preemptible instances: For fault-tolerant, stateless workloads (batch processing, CI/CD, "
        "dev/test environments). Typical savings: 60-90% vs. on-demand.",
        "Waste elimination: Automated policies to shut down non-production resources outside business hours, "
        "delete unattached storage volumes, and remove unused elastic IPs and load balancers.",
    ])

    # 8
    pdf.section_heading("8", "DevOps and SRE Enablement")
    pdf.body(
        "Cloud migration provides an opportunity to modernize software delivery and operations practices. "
        "Meridian's DevOps enablement offering establishes CI/CD pipelines, infrastructure-as-code practices, "
        "automated testing, and observability platforms. Our SRE (Site Reliability Engineering) practice "
        "introduces service level objectives (SLOs), error budgets, toil reduction, and incident management "
        "practices aligned with Google's SRE principles."
    )
    pdf.bullet_list([
        "CI/CD: GitHub Actions, Azure DevOps Pipelines, or GitLab CI. Automated build, test, security scan, "
        "and deployment for every code change.",
        "Infrastructure-as-Code: Terraform for multi-cloud, Bicep for Azure-only, CloudFormation for AWS-only. "
        "All infrastructure changes go through pull request review and automated validation.",
        "Observability: Datadog, Dynatrace, or cloud-native monitoring (CloudWatch, Azure Monitor, Cloud "
        "Monitoring) with distributed tracing, log aggregation, and alerting.",
        "Incident management: PagerDuty or Opsgenie for on-call rotation and escalation. Runbooks for common "
        "incidents. Blameless postmortems with published action items.",
    ])

    # 9
    pdf.section_heading("9", "Engagement Approach")
    pdf.body(
        "Cloud migration engagements are structured to deliver rapid, measurable progress through "
        "a phased wave model. The following outlines a typical engagement structure:"
    )
    pdf.bullet_list([
        "Timeline: 3-4 months for Cloud Readiness Assessment and Landing Zone deployment; 9-15 months for full migration execution (4-6 waves); 3-6 months for post-migration optimization.",
        "Team Composition: 1 Engagement Partner, 1 Cloud Program Director, 1-2 Cloud Architects (certified in target platform), 2-4 Migration Engineers, 1 Security and Compliance Lead, 1 FinOps Analyst, 1 OCM Consultant (for change management and training).",
        "Key Deliverables: Cloud Readiness Assessment Report, 6R Application Disposition Matrix, Landing Zone Architecture Document, Migration Runbooks (per pattern), Wave Execution Reports, Post-Migration Validation Reports, FinOps Operating Model and Dashboard, Knowledge Transfer Package.",
    ])

    # 10
    pdf.section_heading("10", "Related Case Studies & Key Personnel")
    pdf.body(
        "The following case study and key personnel are directly relevant to cloud migration engagements:"
    )
    pdf.bullet_list([
        "Public Sector Cloud Migration Case Study -- Federal agency FedRAMP-compliant migration of 400+ applications to AWS GovCloud; led by Dr. Priya Ramanathan, Lead Partner. Achieved $12M annual infrastructure cost reduction.",
        "Jordan Lee, Senior Manager -- Cloud Architecture Lead, AWS Solutions Architect Professional and Azure Solutions Architect Expert certified. Specializes in large-scale migration factory operations and multi-cloud landing zone design.",
    ])

    # 11
    pdf.section_heading("11", "Related Meridian Methodologies")
    pdf.body(
        "Cloud migration engagements intersect with several other Meridian Advisory practice "
        "areas. The following documents provide complementary guidance:"
    )
    pdf.bullet_list([
        "Cybersecurity Risk Assessment Methodology (v4.0) -- Security is integrated into every migration phase; the Cybersecurity Assessment framework is used for pre-migration security posture evaluation and post-migration validation.",
        "Standard Project Lifecycle Framework (v4.2) -- Cloud migrations follow the SPL governance structure, with migration waves mapping to SPL Build/Test/Deploy phases.",
        "Organizational Change Management Framework (v5.0) -- Cloud migrations require OCM support for IT operations teams transitioning from on-premises to cloud operating models.",
        "Data, Analytics & AI Strategy Guide (v1.0) -- Data platform modernization (data lake, lakehouse) is often executed as part of a cloud migration program.",
        "Enterprise ERP Implementation Strategy (v2.3) -- Cloud ERP migrations (e.g., on-premises SAP to S/4HANA Cloud) combine ERP transformation and cloud migration methodologies.",
    ])

    path = os.path.join(OUTPUT_DIR, "cloud_migration_methodology.pdf")
    pdf.output(path)
    print(f"  [5/7] {path}")


# ===========================================================================
# 6. Supply Chain Optimization
# ===========================================================================
def gen_supply_chain():
    pdf = MeridianPDF("Supply Chain Optimization Practice Guide", "2.1", "October 2025")
    pdf.cover_page()
    pdf.new_content_page()

    # 1
    pdf.section_heading("1", "Practice Overview")
    pdf.body(
        "Meridian's Supply Chain Optimization practice helps clients transform their end-to-end supply chains "
        "from cost centers into strategic competitive advantages. Our approach combines deep industry expertise, "
        "advanced analytics, and technology enablement to deliver measurable improvements in cost, service "
        "levels, resilience, and sustainability. Across 120+ supply chain engagements, Meridian clients have "
        "achieved average improvements of 15-25% in forecast accuracy, 12-18% in logistics cost reduction, "
        "and 20-30% in inventory optimization."
    )

    # 2
    pdf.section_heading("2", "Demand Sensing and Forecasting")
    pdf.body(
        "Traditional demand forecasting relies on historical sales data and statistical models that struggle "
        "to capture the volatility and complexity of modern markets. Meridian's demand sensing approach "
        "augments statistical baselines with machine learning models that incorporate demand signals from "
        "POS data, weather patterns, social media sentiment, economic indicators, promotional calendars, "
        "and competitive activity."
    )
    pdf.sub_heading("2.1", "ML Forecasting Models")
    pdf.body(
        "Meridian deploys ensemble forecasting models that combine multiple algorithms -- gradient boosted "
        "trees (XGBoost, LightGBM), recurrent neural networks (LSTM), and traditional ARIMA/ETS models -- to "
        "produce consensus forecasts with prediction intervals. Model selection is automated based on forecast "
        "accuracy metrics (MAPE, WMAPE, bias) evaluated on rolling holdout windows. Our models typically "
        "deliver 15-25% improvement in forecast accuracy compared to the client's existing methods, measured "
        "at the SKU-location-week level."
    )
    pdf.sub_heading("2.2", "Demand Sensing Integration")
    pdf.body(
        "Demand sensing signals are ingested through a cloud-based data pipeline (Azure Data Factory or AWS "
        "Glue) and processed in near-real-time. The sensing layer adjusts statistical forecasts based on "
        "short-term demand indicators, reducing forecast error in the 1-4 week horizon by an additional "
        "10-15%. Integration with the client's planning system (SAP IBP, Oracle Demand Management, Kinaxis "
        "RapidResponse, or Blue Yonder) enables automated forecast updates and exception-based planner review."
    )

    # 3
    pdf.section_heading("3", "Sales and Operations Planning (S&OP)")
    pdf.body(
        "S&OP is the cross-functional planning process that aligns demand, supply, inventory, and financial "
        "plans on a rolling 18-24 month horizon. Meridian designs and implements mature S&OP processes that "
        "elevate planning from a siloed, spreadsheet-driven exercise to an integrated, executive-level "
        "decision-making forum."
    )
    pdf.bullet_list([
        "Monthly S&OP cadence: Product Review (demand plan), Supply Review (capacity and constraints), "
        "Pre-S&OP (scenario analysis, gap closure options), Executive S&OP (decisions and commitments).",
        "Scenario planning: What-if analysis for demand shocks, supply disruptions, capacity expansion, "
        "pricing changes, and new product launches. Quantified impact on revenue, margin, and inventory.",
        "Performance metrics: Forecast accuracy (MAPE by product family), plan adherence (production and "
        "shipment vs. plan), inventory health (weeks of supply, slow-moving and obsolete), customer service "
        "level (OTIF -- On-Time In-Full delivery rate, target: >95%).",
    ])

    # 4
    pdf.section_heading("4", "Procurement and Strategic Sourcing")
    pdf.body(
        "Meridian's procurement optimization practice covers strategic sourcing, spend analytics, supplier "
        "relationship management, and procurement technology enablement."
    )
    pdf.sub_heading("4.1", "Spend Analytics")
    pdf.body(
        "Using tools such as Coupa, Jaggaer, or custom Power BI dashboards, Meridian classifies and analyzes "
        "100% of addressable spend to identify consolidation opportunities, maverick spending, contract "
        "leakage, and supplier rationalization candidates. Typical findings include 8-15% savings "
        "opportunities in indirect spend categories and 3-7% in direct materials through strategic sourcing "
        "events (RFPs, reverse auctions, long-term agreements)."
    )

    pdf.sub_heading("4.2", "Supplier Risk Scoring")
    pdf.body(
        "Meridian's supplier risk framework evaluates suppliers across financial stability (D&B ratings, "
        "credit scores), operational reliability (on-time delivery, quality defect rates), geographic risk "
        "(single-source, country risk indices), cybersecurity posture (third-party security assessments), "
        "and ESG compliance (environmental certifications, labor practices). Each supplier receives a "
        "composite risk score that drives segmentation into strategic, preferred, approved, and conditional "
        "tiers."
    )

    # 5
    pdf.section_heading("5", "Warehouse and Distribution")
    pdf.sub_heading("5.1", "WMS Implementation")
    pdf.body(
        "Meridian implements warehouse management systems (Manhattan Active WM, Blue Yonder WMS, SAP EWM, "
        "Oracle WMS Cloud) to optimize receiving, putaway, picking, packing, and shipping operations. Our "
        "WMS implementations include RF/barcode scanning integration, labor management modules, wave and "
        "task management, and yard management. Typical outcomes include 15-25% improvement in picking "
        "productivity, 30-40% reduction in shipping errors, and 20-30% improvement in space utilization."
    )

    pdf.sub_heading("5.2", "Slotting Optimization")
    pdf.body(
        "Slotting optimization assigns the right products to the right locations within the warehouse to "
        "minimize travel time, reduce congestion, and improve ergonomics. Meridian uses slotting optimization "
        "software (Optricity, Manhattan, or custom algorithms) to analyze order profiles, product velocity, "
        "cube utilization, and pick path efficiency. Reslotting is recommended quarterly and aligned with "
        "seasonal demand shifts."
    )

    # 6
    pdf.section_heading("6", "Transportation Management")
    pdf.body(
        "Transportation typically represents 50-65% of total logistics cost, making it the highest-impact "
        "optimization target in most supply chains."
    )
    pdf.sub_heading("6.1", "TMS Implementation")
    pdf.body(
        "Meridian implements transportation management systems (Oracle TMS, SAP TM, Blue Yonder TMS, MercuryGate) "
        "to automate carrier selection, load optimization, route planning, freight audit, and shipment visibility. "
        "TMS implementations typically achieve 12-18% reduction in transportation costs through optimized "
        "carrier selection, load consolidation, and mode conversion (e.g., LTL to FTL, parcel to LTL)."
    )

    pdf.sub_heading("6.2", "Route Optimization")
    pdf.body(
        "For clients with private fleets or dedicated contract carriage, Meridian deploys route optimization "
        "solutions that consider delivery time windows, vehicle capacity constraints, driver hours-of-service "
        "regulations, fuel costs, and traffic patterns. Dynamic routing capabilities enable real-time "
        "re-optimization in response to order changes, traffic disruptions, or vehicle breakdowns. Typical "
        "outcomes include 10-15% reduction in miles driven and 8-12% improvement in stops per route."
    )

    # 7
    pdf.section_heading("7", "Supply Chain Control Tower")
    pdf.body(
        "The control tower is a centralized visibility and decision-making hub that provides real-time "
        "monitoring of the end-to-end supply chain. Meridian designs control towers with three capability "
        "layers: visibility (real-time dashboards showing order status, inventory positions, shipment "
        "tracking, supplier performance), analytics (exception detection, root cause analysis, predictive "
        "alerts for potential disruptions), and orchestration (automated response playbooks, cross-functional "
        "collaboration tools, scenario simulation). Control tower platforms include Kinaxis, o9 Solutions, "
        "E2open, and custom builds on Databricks or Snowflake."
    )

    # 8
    pdf.section_heading("8", "Supply Chain Digital Twin")
    pdf.body(
        "A digital twin is a virtual replica of the physical supply chain that enables simulation, "
        "optimization, and what-if analysis without disrupting actual operations. Meridian builds digital "
        "twins using platforms such as anyLogistix, Coupa Supply Chain Design (formerly LLamasoft), or "
        "custom Python/SimPy models. Use cases include network design (optimal number and location of "
        "warehouses), inventory policy optimization (safety stock levels, reorder points), capacity planning "
        "(make-vs-buy decisions, capital investment timing), and risk simulation (impact of port closures, "
        "supplier failures, demand shocks)."
    )

    # 9
    pdf.section_heading("9", "ESG and Sustainability Integration")
    pdf.body(
        "Environmental, social, and governance (ESG) considerations are increasingly integral to supply "
        "chain strategy. Meridian helps clients measure, reduce, and report supply chain emissions and "
        "sustainability impacts."
    )
    pdf.bullet_list([
        "Scope 3 emissions tracking: Mapping and quantifying upstream (purchased goods, transportation, "
        "business travel) and downstream (product use, end-of-life) emissions using the GHG Protocol "
        "Corporate Value Chain Standard. Data collection through supplier surveys, spend-based estimation, "
        "and activity-based calculation.",
        "Sustainable sourcing: Supplier sustainability scorecards, preferred supplier programs for "
        "low-carbon materials, circular economy integration (recycled content, take-back programs).",
        "Green logistics: Mode shift analysis (road to rail/ocean), fleet electrification roadmaps, "
        "packaging optimization (right-sizing, material reduction, recyclable materials), carbon offset "
        "programs for residual emissions.",
        "Reporting and disclosure: CSRD, ISSB, CDP, and GRI-aligned sustainability reporting. Integration "
        "of ESG data into enterprise reporting platforms.",
    ])

    # 10
    pdf.section_heading("10", "Resilience and Risk Mitigation")
    pdf.body(
        "The disruptions of recent years -- pandemic, geopolitical conflicts, extreme weather events, "
        "semiconductor shortages -- have elevated supply chain resilience from a nice-to-have to a board-level "
        "priority. Meridian's resilience framework addresses four dimensions."
    )
    pdf.bullet_list([
        "Nearshoring and reshoring: Evaluating total cost of ownership (including risk premiums) for "
        "shifting production closer to end markets. Trade-off analysis between cost, lead time, quality, "
        "and resilience. Site selection support for Mexico, Eastern Europe, and Southeast Asia.",
        "Dual-sourcing and multi-sourcing: Identifying critical single-source components and developing "
        "alternative supplier qualification programs. Target: no more than 60% of volume for any critical "
        "component from a single supplier.",
        "Inventory buffers: Strategic safety stock positioning using multi-echelon inventory optimization "
        "(MEIO) models that balance service levels against inventory investment across the network.",
        "Contingency planning: Documented playbooks for supply disruption scenarios, demand surge events, "
        "and logistics capacity shortages. Tabletop exercises conducted annually with cross-functional "
        "participation.",
    ])

    # 11
    pdf.section_heading("11", "Engagement Approach")
    pdf.body(
        "Supply chain optimization engagements are structured to deliver quick wins in parallel "
        "with long-term strategic improvements. The following outlines a typical engagement:"
    )
    pdf.bullet_list([
        "Timeline: 8-12 weeks for diagnostic and opportunity assessment; 6-18 months for implementation of prioritized initiatives; ongoing performance management and continuous improvement.",
        "Team Composition: 1 Engagement Partner, 1 Supply Chain Program Director, 2-3 Functional Leads (Planning, Procurement, Logistics), 1-2 Data Analysts (demand modeling, network optimization), 1 OCM Consultant for process change adoption.",
        "Key Deliverables: Current-State Assessment and Maturity Scorecard, Opportunity Register with quantified benefits, Future-State Supply Chain Design, Implementation Roadmap, Digital Twin / Network Optimization Model, Control Tower Design and Configuration, Benefits Tracking Dashboard.",
    ])

    # 12
    pdf.section_heading("12", "Related Case Studies & Key Personnel")
    pdf.body(
        "The following case study and key personnel are directly relevant to supply chain optimization engagements:"
    )
    pdf.bullet_list([
        "Manufacturing ERP Transformation Case Study -- $4.8B global manufacturer; supply chain planning module implementation integrated with SAP S/4HANA; led by James O'Sullivan, Lead Partner. Achieved 18% reduction in inventory carrying costs and 22% improvement in OTIF delivery rates.",
        "Raj Krishnamurthy, Managing Director -- Data & Analytics Practice Lead with deep expertise in demand sensing, supply chain digital twins, and ML-driven forecasting. Has delivered 30+ supply chain analytics engagements across manufacturing and retail.",
    ])

    # 13
    pdf.section_heading("13", "Related Meridian Methodologies")
    pdf.body(
        "Supply chain engagements leverage expertise and frameworks across multiple Meridian practices:"
    )
    pdf.bullet_list([
        "Standard Project Lifecycle Framework (v4.2) -- All supply chain implementations follow the SPL governance and phase gate structure.",
        "Organizational Change Management Framework (v5.0) -- Process redesign and technology adoption require structured OCM support, particularly for warehouse and transportation technology implementations.",
        "Enterprise ERP Implementation Strategy (v2.3) -- Supply chain optimization frequently coincides with or follows ERP transformation, particularly for planning (MRP/MPS) and procurement modules.",
        "Data, Analytics & AI Strategy Guide (v1.0) -- Advanced analytics, demand sensing, and AI-powered planning tools are central to modern supply chain strategies.",
    ])

    path = os.path.join(OUTPUT_DIR, "supply_chain_optimization.pdf")
    pdf.output(path)
    print(f"  [6/7] {path}")


# ===========================================================================
# 7. Cybersecurity Risk Assessment
# ===========================================================================
def gen_cybersecurity():
    pdf = MeridianPDF("Cybersecurity Risk Assessment Methodology", "4.0", "January 2026")
    pdf.cover_page()
    pdf.new_content_page()

    # 1
    pdf.section_heading("1", "Engagement Overview")
    pdf.body(
        "Meridian's Cybersecurity Risk Assessment provides organizations with a comprehensive, independent "
        "evaluation of their security posture across people, processes, and technology. Our assessment "
        "methodology is aligned with the NIST Cybersecurity Framework (CSF) 2.0 and incorporates elements "
        "from ISO 27001, CIS Controls v8, and MITRE ATT&CK. The engagement is designed to provide actionable "
        "insights, not just findings -- every identified risk is accompanied by a prioritized remediation "
        "recommendation with estimated effort and cost."
    )
    pdf.body(
        "Typical engagement duration is 6-8 weeks for a mid-sized organization (1,000-10,000 employees), "
        "scalable to 10-12 weeks for large enterprises with complex environments. The assessment team "
        "consists of 3-5 senior security consultants with CISSP, CISM, OSCP, and/or GIAC certifications."
    )

    # 2
    pdf.section_heading("2", "Threat Landscape Analysis")
    pdf.body(
        "The assessment begins with a threat landscape analysis that identifies the most relevant threat "
        "actors, attack vectors, and tactics for the client's industry and operating environment. Meridian "
        "maintains a proprietary Threat Intelligence Database aggregating data from open-source intelligence "
        "(OSINT), commercial threat feeds (Recorded Future, Mandiant), industry ISACs, and our own incident "
        "response casework."
    )
    pdf.bullet_list([
        "Nation-state actors: Advanced persistent threats (APTs) targeting intellectual property, critical "
        "infrastructure, and sensitive government data. Relevant TTPs mapped to MITRE ATT&CK groups.",
        "Organized crime: Ransomware-as-a-Service (RaaS) operations, business email compromise (BEC), "
        "credential harvesting, and financial fraud. Analysis of sector-specific targeting patterns.",
        "Insider threats: Malicious insiders, negligent employees, and compromised credentials. Assessment "
        "of the client's insider threat program maturity.",
        "Supply chain threats: Third-party software compromises (e.g., SolarWinds-style attacks), managed "
        "service provider compromises, and open-source dependency vulnerabilities.",
    ])

    # 3
    pdf.section_heading("3", "NIST CSF Alignment Assessment")
    pdf.body(
        "The core of Meridian's assessment evaluates the client's security capabilities against the six "
        "functions of the NIST Cybersecurity Framework 2.0: Govern, Identify, Protect, Detect, Respond, "
        "and Recover. Each function is broken down into categories and subcategories, and the client's "
        "maturity is assessed on a five-tier scale."
    )
    pdf.bullet_list([
        "Govern: Organizational context, risk management strategy, policies, oversight, supply chain risk.",
        "Identify: Asset management, risk assessment, improvement planning. Comprehensive inventory of "
        "hardware assets, software assets, data assets, and cloud resources.",
        "Protect: Identity management and access control, awareness and training, data security, platform "
        "security, technology infrastructure resilience.",
        "Detect: Continuous monitoring, adverse event analysis. Evaluation of SIEM deployment, log "
        "coverage, detection rules, and mean time to detect (MTTD) metrics.",
        "Respond: Incident management, incident analysis, incident response reporting and communication, "
        "incident mitigation. Review of incident response plans and tabletop exercise history.",
        "Recover: Incident recovery plan execution, incident recovery communication. Assessment of backup "
        "and disaster recovery capabilities, RTOs, and RPOs.",
    ])

    # 4
    pdf.section_heading("4", "Zero Trust Architecture Evaluation")
    pdf.body(
        "Meridian evaluates the client's progress toward a Zero Trust architecture across the seven pillars "
        "defined in the CISA Zero Trust Maturity Model: User, Device, Network, Application Workload, Data, "
        "Visibility and Analytics, and Automation and Orchestration. For each pillar, we assess current-state "
        "maturity, identify gaps against the client's target maturity level, and recommend specific technology "
        "and process investments."
    )
    pdf.body(
        "Key Zero Trust capabilities assessed include: multi-factor authentication (MFA) coverage and strength, "
        "conditional access policies, microsegmentation implementation, software-defined perimeter (SDP) "
        "adoption, least-privilege access enforcement, just-in-time (JIT) access provisioning, continuous "
        "device compliance validation, and data-centric security controls (classification, labeling, DLP, "
        "encryption)."
    )

    # 5
    pdf.section_heading("5", "Identity and Access Management Maturity")
    pdf.body(
        "Identity is the new security perimeter. Meridian's IAM assessment covers the full identity lifecycle: "
        "provisioning, authentication, authorization, governance, and deprovisioning."
    )
    pdf.bullet_list([
        "Directory services: Active Directory domain health, Azure AD/Entra ID configuration, federation "
        "and SSO implementations, B2B and B2C identity scenarios.",
        "Privileged access management (PAM): Assessment of PAM tool deployment (CyberArk, BeyondTrust, "
        "Delinea), session recording, credential vaulting, just-in-time privilege elevation, and standing "
        "privilege inventory.",
        "Access governance: Access certification campaigns, segregation of duties (SoD) controls, role-based "
        "access control (RBAC) model effectiveness, orphaned account identification.",
        "Authentication strength: MFA adoption rates, phishing-resistant MFA (FIDO2, Windows Hello for "
        "Business), password policy effectiveness, and credential compromise monitoring.",
    ])

    # 6
    pdf.section_heading("6", "Endpoint and Cloud Security")
    pdf.sub_heading("6.1", "Endpoint Detection and Response (EDR)")
    pdf.body(
        "The assessment evaluates the client's EDR deployment coverage, configuration, and operational "
        "effectiveness. Key metrics include agent deployment rate (target: >98% of managed endpoints), "
        "detection rule coverage against MITRE ATT&CK techniques, alert investigation rate and mean time "
        "to investigate, and automated response action configuration. Leading EDR platforms assessed include "
        "CrowdStrike Falcon, Microsoft Defender for Endpoint, SentinelOne, and Carbon Black."
    )

    pdf.sub_heading("6.2", "Cloud Security Posture Management (CSPM)")
    pdf.body(
        "For clients with cloud workloads, Meridian assesses the cloud security posture using native and "
        "third-party tools (Microsoft Defender for Cloud, AWS Security Hub, Wiz, Orca, Prisma Cloud). The "
        "assessment covers IAM policy analysis, network exposure (public-facing resources, overly permissive "
        "security groups), encryption at rest and in transit, logging and monitoring coverage, and compliance "
        "against CIS Benchmarks for the relevant cloud platforms."
    )

    # 7
    pdf.section_heading("7", "Vulnerability Management")
    pdf.body(
        "Meridian assesses the maturity and effectiveness of the client's vulnerability management program "
        "across the full lifecycle: asset discovery, vulnerability scanning, risk prioritization, remediation "
        "tracking, and exception management."
    )
    pdf.bullet_list([
        "Scanning coverage: Percentage of assets scanned, scanning frequency (target: weekly for internet-"
        "facing, monthly for internal), authenticated vs. unauthenticated scans.",
        "Risk prioritization: Use of CVSS scores, CISA Known Exploited Vulnerabilities (KEV) catalog, and "
        "asset criticality for risk-based prioritization. Shift from severity-based to risk-based approach.",
        "Remediation SLAs: Critical vulnerabilities (CVSS 9.0+) remediated within 48 hours for internet-"
        "facing assets, 7 days for internal. High vulnerabilities (CVSS 7.0-8.9) within 14 days.",
        "Patching effectiveness: Percentage of vulnerabilities remediated within SLA, mean time to "
        "remediate, and reintroduction rate.",
    ])

    # 8
    pdf.section_heading("8", "Incident Response Assessment")
    pdf.body(
        "Meridian reviews the client's incident response program including the incident response plan (IRP), "
        "team structure and roles, communication protocols, forensic capabilities, and regulatory notification "
        "procedures. We evaluate the IRP against NIST SP 800-61r3 guidelines and assess the team's "
        "preparedness through a facilitated tabletop exercise simulating a realistic attack scenario "
        "(typically ransomware or business email compromise)."
    )
    pdf.body(
        "Key assessment areas include: incident classification and severity definitions, escalation procedures "
        "and decision trees, forensic evidence preservation procedures, legal counsel engagement triggers, "
        "regulatory notification timelines (GDPR 72-hour requirement, SEC 4-day rule, state breach notification "
        "laws), crisis communication templates, and post-incident review processes."
    )

    # 9
    pdf.section_heading("9", "Third-Party Risk Assessment")
    pdf.body(
        "Third-party risk is one of the fastest-growing attack vectors. Meridian evaluates the client's "
        "third-party risk management (TPRM) program including vendor inventory completeness, risk tiering "
        "methodology, assessment questionnaires (SIG Lite, SIG Core, CAIQ), continuous monitoring tools "
        "(SecurityScorecard, BitSight, RiskRecon), contract security requirements, and fourth-party "
        "visibility. The assessment produces a risk-ranked vendor list with specific remediation "
        "recommendations for high-risk third parties."
    )

    # 10
    pdf.section_heading("10", "Penetration Testing Approach")
    pdf.body(
        "Meridian's penetration testing offering complements the risk assessment with hands-on validation "
        "of security controls. Our testing methodology follows the PTES (Penetration Testing Execution "
        "Standard) and includes the following engagement types."
    )
    pdf.bullet_list([
        "External network penetration testing: Perimeter assessment of internet-facing assets, DNS "
        "enumeration, service identification, vulnerability exploitation, and post-exploitation activities.",
        "Internal network penetration testing: Assumes an initial foothold (compromised workstation) and "
        "attempts lateral movement, privilege escalation, domain compromise, and sensitive data access.",
        "Web application testing: OWASP Top 10 assessment, authentication and session management testing, "
        "input validation, business logic flaws, and API security testing.",
        "Social engineering: Phishing campaigns (email and SMS), pretexting, physical security assessments "
        "(badge cloning, tailgating, dumpster diving). Results measured as click rate, credential submission "
        "rate, and report rate.",
        "Red team engagements: Objective-based, adversary simulation exercises with no predefined scope "
        "limitations. Designed to test the client's detection and response capabilities against realistic "
        "threat scenarios. Duration: 4-8 weeks.",
    ])

    # 11
    pdf.section_heading("11", "Deliverables and Reporting")
    pdf.body(
        "The cybersecurity risk assessment produces three primary deliverables, each tailored to a different "
        "audience and purpose."
    )
    pdf.sub_heading("11.1", "Executive Briefing")
    pdf.body(
        "A 15-20 page presentation for the Board, C-suite, and senior leadership. Includes overall security "
        "posture rating (A-F scale), benchmark comparison against industry peers, top 5 strategic risks with "
        "business impact quantification, recommended investment priorities, and a 12-month strategic roadmap. "
        "Delivered as a 60-minute in-person briefing with Q&A."
    )

    pdf.sub_heading("11.2", "Risk Heat Map")
    pdf.body(
        "A visual representation of all identified risks plotted on a likelihood-vs-impact matrix, color-coded "
        "by NIST CSF function. The heat map enables rapid identification of the highest-priority risks and "
        "serves as a communication tool for risk committee discussions. Interactive version available in "
        "Power BI with drill-down to individual findings."
    )

    pdf.sub_heading("11.3", "Remediation Roadmap")
    pdf.body(
        "A detailed, prioritized plan of remediation actions organized into three horizons: Quick Wins "
        "(0-3 months, low effort, high impact), Foundation (3-9 months, moderate effort, structural "
        "improvements), and Strategic (9-18 months, significant investment, transformational capabilities). "
        "Each action item includes description, NIST CSF alignment, estimated effort (person-days), "
        "estimated cost, responsible party, dependencies, and expected risk reduction."
    )

    # 12
    pdf.section_heading("12", "CISO Advisory Services")
    pdf.body(
        "For clients without a full-time CISO or those seeking supplemental strategic guidance, Meridian "
        "offers a virtual CISO (vCISO) service. The vCISO provides strategic security leadership on a "
        "fractional basis (typically 2-4 days per month), including security program oversight, board and "
        "executive reporting, vendor evaluation and selection, security budget planning, regulatory "
        "compliance guidance, and incident response leadership. The vCISO engagement is staffed by a "
        "Meridian Director or Managing Director with 15+ years of security leadership experience."
    )

    # 13
    pdf.section_heading("13", "Engagement Approach")
    pdf.body(
        "Cybersecurity risk assessments are scoped based on organizational size, complexity, and "
        "regulatory environment. The following outlines a typical engagement structure:"
    )
    pdf.bullet_list([
        "Timeline: 6-8 weeks for mid-sized organizations (1,000-10,000 employees); 10-12 weeks for large enterprises; 4-6 weeks for focused assessments (single domain such as IAM or cloud security).",
        "Team Composition: 1 Engagement Partner (CISO-level experience), 1 Project Manager, 2-3 Senior Security Consultants (CISSP, CISM, OSCP), 1 Penetration Tester (OSCP, GPEN), 1 GRC Analyst.",
        "Key Deliverables: Executive Briefing (15-20 pages), Detailed Findings Report (50-100+ pages), Risk Heat Map (interactive Power BI), Remediation Roadmap (3-horizon plan), Tabletop Exercise Report, Optional: Penetration Test Report (separate deliverable).",
    ])

    # 14
    pdf.section_heading("14", "Related Case Studies & Key Personnel")
    pdf.body(
        "The following case study and key personnel are directly relevant to cybersecurity risk assessment engagements:"
    )
    pdf.bullet_list([
        "Financial Services Digital Transformation Case Study -- $285B global bank; comprehensive cybersecurity posture assessment integrated into core banking modernization; led by Sarah Chen, Lead Partner. Identified and remediated 47 critical security gaps pre-deployment.",
        "Alex Petrov, Managing Director -- Cybersecurity Practice Lead, CISSP and CISM certified with 20+ years of experience in financial services and critical infrastructure security. Former CISO at a Fortune 100 financial institution.",
        "Thomas Chen, Senior Manager -- IT Audit and GRC specialist with deep expertise in SOC reporting, NIST CSF assessments, and regulatory compliance (PCI-DSS, HIPAA, GLBA). Certified CISA and CRISC.",
    ])

    # 15
    pdf.section_heading("15", "Related Meridian Methodologies")
    pdf.body(
        "Cybersecurity assessments frequently connect to broader transformation and risk management "
        "initiatives across the firm. Related documents include:"
    )
    pdf.bullet_list([
        "Cloud Migration Methodology and Playbook (v3.5) -- Cloud security assessments are a standard component of Meridian's cloud migration program, performed during the Cloud Readiness Assessment phase.",
        "Standard Project Lifecycle Framework (v4.2) -- Security assessments are embedded in the SPL Design phase for all transformation engagements.",
        "Data, Analytics & AI Strategy Guide (v1.0) -- Data governance and responsible AI frameworks complement cybersecurity risk management for AI-enabled enterprises.",
        "Enterprise ERP Implementation Strategy (v2.3) -- ERP security architecture reviews are conducted during the ERP Design phase using the cybersecurity assessment methodology.",
    ])

    path = os.path.join(OUTPUT_DIR, "cybersecurity_risk_assessment.pdf")
    pdf.output(path)
    print(f"  [7/7] {path}")


# ===========================================================================
# 8. Data, Analytics & AI Strategy
# ===========================================================================
def gen_data_ai_strategy():
    pdf = MeridianPDF("Data, Analytics & AI Strategy Guide", "1.0", "March 2026")
    pdf.cover_page()
    pdf.new_content_page()

    # 1
    pdf.section_heading("1", "Executive Overview")
    pdf.body(
        "Data has emerged as the most critical strategic asset for modern enterprises. Organizations that "
        "excel at leveraging data for decision-making, operational optimization, and customer insight "
        "consistently outperform their peers. Meridian & Associates' Data, Analytics & AI practice helps "
        "clients build the foundational capabilities -- governance, architecture, talent, and culture -- "
        "required to realize the full value of their data assets and responsibly adopt artificial intelligence."
    )
    pdf.body(
        "Our practice has delivered 200+ data strategy and analytics engagements across financial services, "
        "healthcare, manufacturing, retail, and energy sectors. This guide codifies our methodologies, "
        "reference architectures, and accelerators into a comprehensive framework applicable to clients at "
        "every stage of data maturity -- from organizations still reliant on spreadsheets and manual reporting "
        "to advanced enterprises deploying production machine learning and generative AI at scale."
    )

    # 2
    pdf.section_heading("2", "Data Governance Framework")
    pdf.sub_heading("2.1", "Governance Operating Model")
    pdf.body(
        "Effective data governance establishes the policies, roles, processes, and metrics needed to manage "
        "data as an enterprise asset. Meridian's governance framework is aligned with the DAMA-DMBOK2 "
        "(Data Management Body of Knowledge) and organized around three tiers:"
    )
    pdf.bullet_list([
        "Strategic Tier (Data Governance Council): A cross-functional executive body (CDO, CIO, CFO, COO, "
        "CISO, business unit leaders) that sets data strategy, approves policies, resolves escalations, and "
        "allocates funding. Meets monthly. Chaired by the Chief Data Officer (CDO) or equivalent.",
        "Tactical Tier (Data Stewardship Committee): Domain data stewards from each business function who "
        "define business rules, resolve data quality issues, approve master data changes, and manage "
        "metadata. Meets biweekly. Each steward is accountable for the quality and integrity of data "
        "within their domain.",
        "Operational Tier (Data Custodians and Engineers): Technical teams responsible for implementing "
        "governance policies in platforms and pipelines -- access controls, data quality checks, lineage "
        "tracking, and retention management. Operates continuously with automated monitoring and alerting.",
    ])

    pdf.sub_heading("2.2", "Policy Framework")
    pdf.body(
        "Meridian assists clients in developing a comprehensive data policy framework covering:"
    )
    pdf.bullet_list([
        "Data Classification and Handling: Defining classification tiers (Public, Internal, Confidential, "
        "Restricted) with corresponding access controls, encryption requirements, and retention rules.",
        "Data Quality Standards: Defining data quality dimensions (accuracy, completeness, consistency, "
        "timeliness, uniqueness, validity) with measurable thresholds for each critical data element.",
        "Data Lineage and Cataloging: Requiring documentation of data origins, transformations, and "
        "consumption points for all regulated and critical data assets.",
        "Data Privacy and Ethics: Policies aligned with GDPR, CCPA/CPRA, HIPAA, and emerging AI "
        "regulations (EU AI Act). Includes data minimization, consent management, and right-to-erasure "
        "procedures.",
        "Data Retention and Disposal: Defining retention periods by data type and regulatory requirement, "
        "with automated disposal workflows for expired data.",
    ])

    # 3
    pdf.section_heading("3", "Modern Data Platform Architecture")
    pdf.sub_heading("3.1", "Lakehouse Architecture")
    pdf.body(
        "The lakehouse combines the low-cost storage and schema flexibility of a data lake with the "
        "ACID transactions, schema enforcement, and performance optimizations of a data warehouse. "
        "Meridian recommends the lakehouse as the default architecture for new data platform builds, "
        "leveraging open table formats (Delta Lake, Apache Iceberg, or Apache Hudi) for interoperability "
        "and vendor flexibility."
    )
    pdf.body(
        "Reference platforms include Databricks (Unity Catalog for governance, Delta Lake for storage, "
        "Photon engine for performance), Microsoft Fabric (OneLake, lakehouse, warehouse, and real-time "
        "analytics in a unified SaaS experience), and Snowflake (Iceberg Tables, dynamic tables, "
        "Snowpark for data engineering and ML). Platform selection is driven by the client's existing "
        "cloud platform (Azure, AWS, GCP), team skill sets, and total cost of ownership analysis."
    )

    pdf.sub_heading("3.2", "Data Mesh")
    pdf.body(
        "For large, complex organizations with distributed domain ownership of data, Meridian advises "
        "on data mesh architecture. Data mesh decentralizes data ownership to domain teams who produce "
        "and manage their own data products, while a central platform team provides self-service "
        "infrastructure (compute, storage, orchestration, governance) as a product. Key principles include:"
    )
    pdf.bullet_list([
        "Domain-Oriented Ownership: Each business domain (e.g., Finance, Marketing, Supply Chain) owns "
        "its analytical and operational data products end-to-end, from ingestion through quality "
        "management to consumer-facing interfaces.",
        "Data as a Product: Data products have clearly defined interfaces (APIs, SQL endpoints), SLAs "
        "(freshness, quality, availability), documentation, and discoverability through a central "
        "data catalog.",
        "Self-Service Infrastructure: The central platform team provides templated pipelines, compute "
        "environments, governance tooling, and observability -- enabling domain teams to build and "
        "operate data products without deep infrastructure expertise.",
        "Federated Computational Governance: Policies (access control, quality rules, retention) are "
        "defined centrally but enforced computationally through automated checks embedded in the "
        "platform -- not through manual review processes.",
    ])

    pdf.sub_heading("3.3", "Data Fabric")
    pdf.body(
        "Data fabric is an integration-centric architecture that provides a unified data management "
        "layer across heterogeneous environments (on-premises, multi-cloud, SaaS). Unlike data mesh, "
        "which emphasizes organizational decentralization, data fabric focuses on technical integration "
        "and automation. Key capabilities include automated metadata discovery, knowledge graph-based "
        "data cataloging, AI-driven data integration recommendations, and active metadata management. "
        "Meridian implements data fabric solutions using platforms such as Informatica Intelligent Data "
        "Management Cloud (IDMC), Denodo for data virtualization, and Collibra or Alation for data "
        "cataloging and governance."
    )

    # 4
    pdf.section_heading("4", "BI and Reporting Strategy")
    pdf.body(
        "Business intelligence and reporting remain the most widely used data capabilities and "
        "frequently represent the first area where clients see tangible value from data investments. "
        "Meridian's BI strategy covers the full stack from semantic modeling to dashboard delivery."
    )
    pdf.bullet_list([
        "Semantic Layer: Defining a centralized metrics layer (using dbt Semantic Layer, Looker "
        "LookML, or AtScale) that provides consistent metric definitions, business logic, and "
        "dimensional hierarchies across all reporting tools.",
        "Self-Service BI: Enabling business users to build their own reports and dashboards with "
        "governed data sources. Platforms: Power BI (for Microsoft-centric organizations), Tableau "
        "(for analytics-intensive use cases), and Looker (for data-product-centric approaches).",
        "Embedded Analytics: Integrating analytics directly into operational applications (CRM, "
        "ERP, customer portals) using embedded BI capabilities (Power BI Embedded, Tableau Embedded, "
        "Sigma Computing).",
        "Executive Dashboards: Designing C-suite and board-level reporting packages that distill "
        "complex data into actionable KPIs, trend analysis, and exception alerts. Delivered through "
        "Power BI or Tableau with mobile-optimized layouts.",
        "Report Migration and Rationalization: Auditing existing report inventories (which commonly "
        "number in the thousands), identifying redundant and unused reports, and consolidating to "
        "a rationalized set with clear ownership and refresh schedules.",
    ])

    # 5
    pdf.section_heading("5", "Advanced Analytics and ML Operationalization")
    pdf.sub_heading("5.1", "Analytics Maturity Model")
    pdf.body(
        "Meridian assesses client analytics maturity across a five-level model: Descriptive (what "
        "happened), Diagnostic (why it happened), Predictive (what will happen), Prescriptive (what "
        "should we do), and Autonomous (systems act independently). Most clients operate at Descriptive "
        "or Diagnostic levels; our engagements are designed to advance clients by one or two levels "
        "within 12-18 months, focusing on use cases with the highest business impact."
    )

    pdf.sub_heading("5.2", "Use Case Identification and Prioritization")
    pdf.body(
        "Meridian facilitates structured ideation workshops with business and technical stakeholders to "
        "identify analytics and ML use cases. Each use case is evaluated across four dimensions: business "
        "value (revenue impact, cost savings, risk reduction), data readiness (availability, quality, "
        "volume), technical feasibility (model complexity, infrastructure requirements), and organizational "
        "readiness (talent, process maturity, change appetite). Use cases are plotted on a value-vs-feasibility "
        "matrix and sequenced into a phased roadmap."
    )

    pdf.sub_heading("5.3", "MLOps Framework")
    pdf.body(
        "Operationalizing machine learning models requires an end-to-end MLOps framework that manages "
        "the ML lifecycle from experimentation through production deployment, monitoring, and retraining. "
        "Meridian's MLOps framework covers:"
    )
    pdf.bullet_list([
        "Experimentation: Version-controlled experiments using MLflow (integrated with Databricks), "
        "Azure Machine Learning, or Weights & Biases. All experiments are tracked with parameters, "
        "metrics, artifacts, and data lineage.",
        "Feature Engineering: Centralized feature stores (Databricks Feature Store, Feast, Tecton) "
        "that provide consistent, reusable, and point-in-time correct features across training and "
        "inference pipelines.",
        "Model Training and Validation: Automated training pipelines with hyperparameter tuning, "
        "cross-validation, and bias/fairness testing. Models are validated against holdout test sets "
        "and business-defined performance thresholds before promotion.",
        "Deployment: Containerized model serving (Docker/Kubernetes) for real-time inference or batch "
        "scoring. Blue/green and canary deployment patterns for safe rollouts. Integration with "
        "downstream applications via REST APIs or streaming endpoints.",
        "Monitoring and Drift Detection: Continuous monitoring of model performance (accuracy, "
        "precision, recall), data drift (feature distribution shifts), and concept drift (changing "
        "relationships between features and targets). Automated alerting and retraining triggers.",
        "Model Governance: Model registry (MLflow Model Registry, Azure ML Model Registry) with "
        "approval workflows, audit trails, and model cards documenting intended use, limitations, "
        "and ethical considerations.",
    ])
    pdf.body(
        "Reference platforms for MLOps include Databricks (end-to-end ML platform with Unity Catalog "
        "governance), Dataiku (visual ML development with strong governance and collaboration features, "
        "well-suited for teams with mixed technical skill levels), and Azure AI / Azure Machine Learning "
        "(enterprise-grade ML platform integrated with the Azure ecosystem)."
    )

    # 6
    pdf.section_heading("6", "Generative AI Advisory")
    pdf.sub_heading("6.1", "Use Case Identification")
    pdf.body(
        "Generative AI (GenAI) -- including large language models (LLMs), image generation, and code "
        "generation -- represents a transformational capability, but realizing value requires rigorous "
        "use case selection and responsible deployment. Meridian's GenAI advisory helps clients move "
        "beyond experimentation to production-grade AI applications."
    )
    pdf.body(
        "Our GenAI use case framework evaluates opportunities across three horizons:"
    )
    pdf.bullet_list([
        "Horizon 1 -- Productivity (0-6 months): Internal productivity tools such as document "
        "summarization, knowledge base Q&A (RAG-based), code generation assistance, meeting "
        "transcription and action item extraction, and email/report drafting. Low risk, high "
        "adoption, and rapid ROI.",
        "Horizon 2 -- Process Transformation (6-18 months): AI-augmented workflows in core "
        "business processes such as customer service (AI agents with human oversight), claims "
        "processing, contract analysis, proposal generation, and financial analysis automation. "
        "Moderate risk, requires process redesign and change management.",
        "Horizon 3 -- Business Model Innovation (12-36 months): AI-native products and services, "
        "personalized customer experiences, autonomous decision systems, and AI-driven market "
        "intelligence platforms. High investment, high potential, requires strategic commitment.",
    ])

    pdf.sub_heading("6.2", "Responsible AI Framework")
    pdf.body(
        "Meridian's Responsible AI framework provides guardrails for the ethical development and "
        "deployment of AI systems. The framework addresses:"
    )
    pdf.bullet_list([
        "Fairness and Bias: Testing models for disparate impact across protected classes. Using "
        "bias detection tools (Fairlearn, AI Fairness 360) during development and monitoring bias "
        "metrics in production.",
        "Transparency and Explainability: Providing model explanations appropriate to the audience "
        "(technical explanations for data scientists, business explanations for decision-makers, "
        "user-facing explanations for affected individuals). Tools: SHAP, LIME, InterpretML.",
        "Privacy and Data Protection: Ensuring training data complies with privacy regulations. "
        "Implementing data anonymization, differential privacy, and consent management. Evaluating "
        "model memorization risks for LLMs.",
        "Security and Robustness: Protecting AI systems against adversarial attacks, prompt "
        "injection, data poisoning, and model extraction. Implementing input validation, output "
        "filtering, and rate limiting for GenAI applications.",
        "Human Oversight: Defining appropriate levels of human-in-the-loop oversight based on "
        "the risk profile of each AI application. High-stakes decisions (credit, hiring, medical) "
        "require mandatory human review.",
        "Governance and Accountability: Establishing an AI Ethics Board, maintaining an AI use case "
        "registry, conducting periodic AI impact assessments, and defining escalation procedures for "
        "AI incidents.",
    ])

    pdf.sub_heading("6.3", "ROI Framework for AI Investments")
    pdf.body(
        "Quantifying the return on AI investments is essential for securing funding and demonstrating "
        "value. Meridian's AI ROI framework measures value across four categories:"
    )
    pdf.bullet_list([
        "Efficiency Gains: Time savings, FTE reallocation, and throughput increases. Measured through "
        "before/after process mining, time studies, and volume metrics. Typical GenAI productivity "
        "gains range from 15-40% for knowledge worker tasks.",
        "Quality Improvements: Error reduction, consistency gains, and compliance improvements. "
        "Measured through defect rates, rework rates, and audit findings.",
        "Revenue Impact: Faster time-to-market, improved customer experience, personalization-driven "
        "conversion, and new AI-enabled revenue streams.",
        "Risk Reduction: Earlier fraud detection, improved regulatory compliance, reduced security "
        "incidents, and better risk modeling accuracy.",
    ])

    # 7
    pdf.section_heading("7", "Data Quality Management")
    pdf.body(
        "Poor data quality is the most frequently cited barrier to analytics and AI adoption. Meridian's "
        "data quality management approach establishes proactive, automated quality monitoring embedded "
        "in data pipelines -- not retrospective cleansing exercises."
    )
    pdf.bullet_list([
        "Data Quality Profiling: Automated profiling of data sources to establish baselines for "
        "completeness, uniqueness, validity, consistency, timeliness, and accuracy. Tools: "
        "Great Expectations, Soda Core, Monte Carlo, dbt tests, Databricks expectations.",
        "Quality Rules and Thresholds: Defining business-driven quality rules (e.g., 'order amount "
        "must be positive', 'customer email must be valid format') with severity levels and automated "
        "alerting. Critical quality failures halt downstream pipelines.",
        "Data Observability: Continuous monitoring of data pipelines for anomalies in volume, "
        "freshness, schema changes, and distribution shifts. Platforms: Monte Carlo, Bigeye, "
        "Datadog Data Observability, or dbt + Elementary.",
        "Root Cause Resolution: Automated lineage tracing to identify the source of quality "
        "issues (source system, transformation logic, or integration point). Structured resolution "
        "workflow with data steward accountability.",
        "Quality Scorecards: Dashboard-based quality reporting for each data domain, with trend "
        "analysis, SLA compliance tracking, and executive-level data health summaries.",
    ])

    # 8
    pdf.section_heading("8", "Master Data Management")
    pdf.body(
        "Master Data Management (MDM) ensures that critical business entities -- customers, products, "
        "suppliers, employees, locations, and charts of accounts -- are defined consistently across "
        "all systems and processes. Meridian implements MDM solutions using the following approach:"
    )
    pdf.bullet_list([
        "MDM Strategy: Defining the MDM vision, scope (which domains to manage), implementation "
        "style (registry, consolidation, coexistence, or centralized), and governance model.",
        "Data Model Design: Creating the golden record schema for each master data domain, "
        "including attributes, hierarchies, relationships, and data quality rules.",
        "Match and Merge: Implementing probabilistic and deterministic matching algorithms to "
        "identify and merge duplicate records. Tools: Informatica MDM, Reltio, Profisee, "
        "Tamr, or custom Spark-based solutions.",
        "Stewardship Workflows: Designing data steward review and approval workflows for "
        "match/merge exceptions, new record creation, and golden record updates.",
        "Integration: Bidirectional synchronization between the MDM hub and consuming systems "
        "(ERP, CRM, data warehouse) using event-driven or batch integration patterns.",
    ])

    # 9
    pdf.section_heading("9", "Data Literacy and Culture")
    pdf.body(
        "Technology and governance alone are insufficient without a data-literate workforce. Meridian's "
        "data literacy program builds organizational capability across three levels:"
    )
    pdf.bullet_list([
        "Foundational Literacy (All Employees): Understanding data types, basic statistics, chart "
        "interpretation, data-driven decision-making principles, and data privacy responsibilities. "
        "Delivered through self-paced e-learning modules (2-4 hours total).",
        "Analytical Literacy (Business Analysts, Managers): Self-service BI tool proficiency (Power BI, "
        "Tableau), SQL fundamentals, statistical analysis concepts, and data storytelling. Delivered "
        "through instructor-led workshops (16-24 hours) with hands-on exercises using client data.",
        "Advanced Literacy (Data Engineers, Data Scientists, ML Engineers): Deep-dive training on the "
        "client's data platform (Databricks, Snowflake, Microsoft Fabric), MLOps practices, GenAI "
        "application development, and responsible AI principles. Delivered through bootcamp-style "
        "programs (40-80 hours) with certification assessments.",
    ])
    pdf.body(
        "Data literacy programs are complemented by community-building activities: Data Champions "
        "networks, internal data hackathons, lunch-and-learn series, and recognition programs for "
        "data-driven decision-making. The Organizational Change Management Framework (v5.0) provides "
        "the structured adoption and sustainment methodology for data literacy initiatives."
    )

    # 10
    pdf.section_heading("10", "Data Engineering and Pipeline Architecture")
    pdf.body(
        "Reliable, scalable data pipelines are the backbone of any modern data platform. Meridian "
        "designs and implements data engineering solutions using the following technology stack and "
        "best practices:"
    )
    pdf.bullet_list([
        "Orchestration: Apache Airflow (self-managed or cloud-managed via MWAA, Cloud Composer), "
        "Dagster (for asset-based orchestration), or Databricks Workflows for end-to-end pipeline "
        "scheduling, dependency management, and monitoring.",
        "Transformation: dbt (data build tool) for SQL-based transformations following the ELT "
        "pattern. dbt provides version-controlled transformations, automated testing, documentation "
        "generation, and lineage tracking -- critical for auditability and governance.",
        "Streaming: Apache Kafka (Confluent) or Azure Event Hubs for real-time data ingestion and "
        "event-driven architectures. Spark Structured Streaming or Flink for real-time "
        "transformations and analytics.",
        "Data Integration: Fivetran, Airbyte, or custom connectors for extracting data from "
        "SaaS applications, databases, APIs, and file sources into the lakehouse.",
        "Infrastructure as Code: Terraform for provisioning cloud infrastructure (compute, storage, "
        "networking). All pipeline infrastructure is version-controlled and deployed through CI/CD "
        "pipelines.",
    ])

    # 11
    pdf.section_heading("11", "Engagement Approach")
    pdf.body(
        "Data, Analytics & AI engagements follow Meridian's Standard Project Lifecycle with "
        "domain-specific activities in each phase. A typical engagement proceeds as follows:"
    )
    pdf.bullet_list([
        "Timeline: 6-8 weeks for Data Strategy and Roadmap; 3-6 months for data platform build "
        "and initial use case delivery; 6-12 months for MLOps implementation and AI at scale; "
        "ongoing for managed services and continuous optimization.",
        "Team Composition: 1 Engagement Partner, 1 Data Strategy Lead (CDO-level advisor), "
        "1-2 Data Architects (platform design and implementation), 2-4 Data Engineers "
        "(pipeline development), 1-2 Data Scientists/ML Engineers (for analytics and AI use cases), "
        "1 Data Governance Consultant, 1 OCM Consultant (for data literacy and adoption programs).",
        "Key Deliverables: Data Maturity Assessment and Benchmarking Report, Data Strategy and "
        "3-Year Roadmap, Data Governance Charter and Policy Framework, Data Platform Architecture "
        "Document, Implemented Data Pipelines and Quality Framework, BI/Reporting Deliverables "
        "(dashboards, semantic layer), ML Model Deployment and MLOps Framework, GenAI Use Case "
        "Playbook and Responsible AI Policy, Data Literacy Program Curriculum, Benefits Realization "
        "Report with ROI Metrics.",
    ])

    # 12
    pdf.section_heading("12", "Related Case Studies & Key Personnel")
    pdf.body(
        "The following case study and key personnel are directly relevant to data, analytics, and AI engagements:"
    )
    pdf.bullet_list([
        "Retail Omnichannel Analytics Case Study -- $12B national retailer; enterprise data platform and customer analytics program; led by Robert Adeyemi, Lead Partner. Delivered unified customer 360 platform enabling $45M incremental revenue through personalization.",
        "Raj Krishnamurthy, Managing Director -- Data & Analytics Practice Lead with expertise in data strategy, lakehouse architecture, and AI/ML operationalization. Has led 50+ data platform engagements across financial services, retail, and healthcare.",
        "Jessica Huang, Senior Manager -- Data Engineering Lead specializing in Databricks, Snowflake, and Microsoft Fabric implementations. Expert in data pipeline architecture, real-time streaming, and DataOps practices.",
        "Aisha Patel, Manager -- Data Analytics specialist with expertise in advanced analytics, statistical modeling, and BI platform implementations (Power BI, Tableau). Leads Meridian's data literacy program development practice.",
    ])

    # 13
    pdf.section_heading("13", "Related Meridian Methodologies")
    pdf.body(
        "Data, Analytics & AI engagements connect to a wide range of Meridian Advisory and "
        "Consulting capabilities. The following documents provide complementary guidance:"
    )
    pdf.bullet_list([
        "Standard Project Lifecycle Framework (v4.2) -- Data engagements follow the SPL governance model; the SPL's Discover phase includes data maturity assessment activities.",
        "Organizational Change Management Framework (v5.0) -- Data literacy programs and AI adoption initiatives are supported by the OCM framework's training, adoption measurement, and sustainment pillars.",
        "Cybersecurity Risk Assessment Methodology (v4.0) -- Data security, privacy, and AI security are assessed using the cybersecurity methodology, particularly for GenAI applications handling sensitive data.",
        "Cloud Migration Methodology and Playbook (v3.5) -- Data platform modernization is frequently part of a cloud migration program; the Cloud Migration playbook provides landing zone and security frameworks.",
        "Enterprise ERP Implementation Strategy (v2.3) -- ERP data migration quality and post-go-live analytics benefit from the data governance and quality management frameworks described in this guide.",
        "Supply Chain Optimization Practice Guide (v2.1) -- Advanced supply chain analytics, demand sensing, and digital twin capabilities are built on the data platform and MLOps frameworks described here.",
    ])

    path = os.path.join(OUTPUT_DIR, "data_ai_strategy.pdf")
    pdf.output(path)
    print(f"  [8/8] {path}")


# ===========================================================================
# Main
# ===========================================================================
if __name__ == "__main__":
    print("Generating Meridian & Associates knowledge base PDFs...")
    gen_project_lifecycle()
    gen_agile_waterfall()
    gen_ocm()
    gen_erp()
    gen_cloud_migration()
    gen_supply_chain()
    gen_cybersecurity()
    gen_data_ai_strategy()
    print("Done. All 8 PDFs generated.")
