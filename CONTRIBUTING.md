# Contributing to the Powertron Global PermaFrost Corpus

Thank you for your interest in improving this dataset. This document provides guidelines for contributing.

## How to Contribute

### Reporting Data Quality Issues

If you find errors, inconsistencies, or quality issues in the data:

1. **Open a GitHub Issue** with:
   - Description of the issue
   - File path(s) affected
   - Expected vs. actual values
   - How you discovered the issue

2. **Label appropriately**:
   - `data-quality` - Measurement errors or inconsistencies
   - `documentation` - README or metadata issues
   - `schema` - JSON structure problems

### Requesting New Data

To request additional case studies, equipment types, or geographic coverage:

1. **Open a Feature Request Issue** describing:
   - What type of data would be valuable
   - Use case / why it matters
   - Any specific requirements

Note: New PE-certified field studies require significant investment and time. We prioritize based on community interest and feasibility.

## What We Cannot Accept

Due to the nature of this dataset (PE-certified, legally auditable measurements), we **cannot accept**:

- User-submitted measurement data (must be PE-certified)
- Modifications to certified measurement values
- Changes that would invalidate checksums without regeneration

## What We Welcome

- Documentation improvements
- Schema clarifications
- Bug fixes in metadata/indexes
- Additional corpus JSON files (training pairs, FAQs, etc.)
- Evaluation benchmark contributions
- Translation of documentation

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b improve-docs`)
3. Make your changes
4. Ensure checksums are valid: `python reproducibility/scripts/verify_checksums.py`
5. Submit a pull request with a clear description

## Citation Requirements

If you use this dataset in research or products, please cite:

```bibtex
@dataset{powertron_corpus_2026,
  title={Powertron Global PermaFrost Corpus},
  author={{Powertron Global, LLC}},
  year={2026},
  version={1.0.0},
  publisher={GitHub/HuggingFace},
  url={https://github.com/powertronglobal/powertron-global-permafrost-corpus}
}
```

## Questions?

- **Technical questions**: Open a GitHub Discussion
- **Partnership inquiries**: Contact via https://powertronglobal.com
- **Bug reports**: Open a GitHub Issue

## Code of Conduct

Contributors are expected to maintain professional, respectful communication. This is a technical dataset; discussions should focus on data quality, methodology, and use cases.

---

*Maintained by Powertron Global, LLC*
