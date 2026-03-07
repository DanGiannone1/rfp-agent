# Knowledge Base Sample Data

This directory contains synthetic PDF documents that populate the Foundry IQ knowledge base for local development and testing. All documents are generated — no real client, personnel, or pricing data is included.

## Structure

| Directory | Contents |
|---|---|
| `audit_assurance/` | Audit methodology, independence policies, PCAOB quality results, transition plans |
| `advisory_consulting/` | Project lifecycle, ERP/cloud/cybersecurity methodologies, change management |
| `tax_services/` | Tax compliance, transfer pricing, ASC 740, M&A due diligence, SALT |
| `common_firm_wide/` | Firm overview, capabilities, DEI policy, ESG report, infosec, BCDR, legal terms |
| `brand_guidelines/` | Proposal writing guide, editorial standards |
| `compliance_certifications/` | SOC 2 Type II, ISO 27001, industry certifications |
| `past_proposals/` | Sample winning proposals (financial audit, ERP implementation, tax compliance) |
| `pricing_frameworks/` | Cost model framework, discount and margin guidance, rate cards |
| `resource_capacity/` | Personnel skills database, team capacity overview |
| `talent_proof_sources/` | Executive/manager/staff bios, case studies across industries |
| `customer_intelligence/` | Client profiles (ACME Manufacturing, Statewide Health, Metro Transit) |
| `historical_performance/` | Bid and engagement performance summaries |

## Indexing into the Knowledge Base

```bash
# Upload PDFs to ADLS and index into Azure AI Search
uv run python index_knowledge_base.py
```

This script reads all PDFs from this directory, uploads them to the configured ADLS Gen2 account, and triggers the Azure AI Search indexer to make them searchable via `knowledge_base_retrieve`.

See `setup_knowledge_base.py` for initial knowledge source and KB creation.
