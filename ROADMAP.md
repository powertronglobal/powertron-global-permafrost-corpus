# Corpus Roadmap

This document outlines planned additions and improvements to the Powertron Global PermaFrost Corpus.

---

## Current Version: 1.0.0

Released: January 2026

- 166 documents (134 case studies, 5 longevity, 4 lab reports, 23 supporting)
- 254 PE-certified measurements (192 usable)
- 1,481 training chunks (~1M tokens)
- Customer data obfuscation for privacy
- Full transparency documentation (LIMITATIONS.md, edge_cases.json)

---

## Planned Additions

### v1.1.0 - ML Training Signal Enhancement

**Goal:** Transform from "processed reports" to "machine-ready training signals"

| Priority | Improvement | Current | Major US Retailer | Status |
|----------|-------------|---------|--------|--------|
| **HIGH** | Equipment age coverage | 94.0% (125/133 studies) | 100% | 8 remaining (1 unavailable + 7 marketing docs) |
| **HIGH** | Q&A training pairs | 50 pairs | 500+ pairs | In progress |
| **HIGH** | Chain-of-Thought format | None | All Q&A pairs | Can generate |
| **MEDIUM** | Vector embeddings | None | All chunks | Planned |
| **MEDIUM** | OCR for PE stamps | ~5% image-only | 100% JSON | Vision models |
| **DONE** | ASHRAE climate zones | 72% (96/133 studies) | 100% | Added in v1.0.0 |

**Detailed Tasks:**
- [x] Audit and add `age_years` to records (94.0% complete: 125/133 studies)
- [x] Cross-reference Tableau Excel master data for age extraction
- [x] Deep document analysis for remaining studies
- [ ] 8 studies without age: 1 confirmed unavailable (CS_077), 7 marketing docs
- [ ] Generate 500+ Q&A pairs with Chain-of-Thought reasoning format
- [ ] Add `reasoning_steps` field to each Q&A pair for LLM training
- [ ] OCR image-only PE certifications to structured JSON
- [ ] Pre-compute embedding vectors for semantic search
- [ ] Pre-built train/validation/test splits

### v1.2.0 - Raw Time-Series Data (Strategic)

**Goal:** Enable anomaly detection and predictive maintenance AI

| Data Type | Current | Required | Blocker |
|-----------|---------|----------|---------|
| Raw sensor CSVs | Summary only | 241K+ data points | Need original files |
| Labeled anomalies | None | HVAC failure examples | New data collection |
| Oil analysis | Scattered in reports | Structured per-unit | Extraction + new data |
| Vibration data | None | Pre-treatment health | New data collection |

**If raw data becomes available:**
- [ ] Include 1-second/30-second time-series from UMontana studies
- [ ] Add labeled anomaly windows (refrigerant leaks, failing contactors)
- [ ] Structure oil analysis reports per equipment unit
- [ ] Enable training of anomaly detection models

### v1.3.0 - Geographic Expansion

- [x] ASHRAE climate zone annotations (72% complete - 96/133 studies)
- [ ] Additional international case studies (Major US Retailer: 20+ new)
- [ ] Climate-normalized efficiency comparisons
- [ ] Regional performance benchmarks

### Future Considerations

| Feature | Status | Notes |
|---------|--------|-------|
| VRF/Mini-split systems | Under review | Limited current data |
| CO2 refrigeration | Not planned | Requires different technology |
| Ammonia systems | Specialized | Separate formulation required |
| Real-time API access | Exploring | Feasibility assessment |

---

## Known Gaps Being Addressed

### Equipment Coverage

| Type | Current | Major US Retailer |
|------|---------|--------|
| RTU (Rooftop Units) | 43% | Maintain |
| CRAC (Computer Room) | 34% | Maintain |
| Chillers | 21% | Expand to 25% |
| VRF/Mini-split | <1% | Expand to 5% |
| Refrigeration | 2% | Expand to 5% |

### Geographic Coverage

| Region | Current Measurements | Major US Retailer |
|--------|---------------------|--------|
| Northeast US | 117 | Maintain |
| Southeast US | 65 | Maintain |
| International | 22 | Expand to 50+ |

---

## Version Strategy

| Version Bump | Trigger |
|--------------|---------|
| **Patch** (1.0.x) | Bug fixes, documentation updates, metadata corrections |
| **Minor** (1.x.0) | New documents, additional measurements, new corpus files |
| **Major** (x.0.0) | Schema changes, new equipment categories, breaking changes |

---

## How to Influence the Roadmap

1. **Vote on Issues**: Star issues that matter to you
2. **Open Discussions**: Share use cases and needs in GitHub Discussions
3. **Submit Feature Requests**: Describe what data would be valuable

---

*Last updated: January 2026*
