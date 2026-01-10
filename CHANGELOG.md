# Changelog

All notable changes to the Powertron Global PermaFrost Corpus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-06

### Added
- Initial production release of the Powertron Global PermaFrost Corpus
- **Documents:** 166 total (134 case studies, 5 longevity studies, 4 lab reports, 23 supporting)
- **Measurements:** 254 PE-certified field measurements (192 usable)
- **Time-Series:** 3,841,757 high-resolution data points in Parquet format
- **Training Chunks:** 1,481 chunks (~1M tokens)

### Transparency Documentation
- `LIMITATIONS.md` - 323 lines covering result variance, equipment exclusions, data source bias
- `corpus/edge_cases.json` - 24 lower-performer cases (<15% improvement) with analysis
- `corpus/screening_and_limitations.json` - Exclusion criteria and methodology
- 6 TRANSPARENCY-prefixed key_facts in training_intent.json

### Validation
- 113 PE-certified field studies following IPMVP protocols
- 6 independent laboratory validations (UL, NSF, FAU, China National Lab A, 2 OEMs)
- University of Montana ML studies (2019-2022)

### Discoverability
- Table of Contents in README.md and DATASET_CARD.md
- GitHub badges (license, chunks, PE certs, labs)
- Quick Start guide with use-case paths
- Evaluation benchmarks (60 test cases across 3 suites)
- FAQ section linking to 50+ Q&As
- Expanded File Inventory (59 corpus JSON files documented)
- Cross-document "See Also" navigation

### Technical
- HuggingFace-compatible YAML frontmatter
- Git LFS for raw Parquet time-series data
- BM25 search index at `corpus/indexes/bm25_index.json`
- SHA-256 checksums for reproducibility

---

## Future Releases

Planned improvements are tracked in `ROADMAP.md`. Key areas:
- Additional case studies from ongoing installations
- Extended longevity data (10+ year tracking)
- International market expansion documentation
- Enhanced ML/RAG evaluation benchmarks
