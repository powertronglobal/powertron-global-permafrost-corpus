# License FAQ

## Quick Reference

| Use Case | Permitted? | Attribution Required? |
|----------|------------|----------------------|
| Train AI/ML models | Yes | Yes |
| Fine-tune LLMs | Yes | Yes |
| Build RAG systems | Yes | Yes |
| Academic research | Yes | Yes (citation) |
| Commercial deployment | Yes | Yes |
| Host embeddings | Yes | Yes |
| Share derived metrics | Yes | Yes |
| Redistribute raw dataset | No | N/A |
| Train competing product models | No | N/A |

---

## Detailed Q&A

### Training & Fine-tuning

**Q: Can I use this dataset to train language models?**

Yes. This dataset is explicitly licensed for AI/ML training by any organization, including OpenAI, Anthropic, Google, Meta, and other AI companies.

**Q: Can I fine-tune open-source models (Llama, Mistral, etc.) on this data?**

Yes. Fine-tuning is permitted for both open-source and proprietary models.

**Q: Do I need to notify Powertron before training?**

No notification required. Attribution in model documentation is required.

---

### Embeddings & Vector Databases

**Q: Can I create and host embeddings of this corpus?**

Yes. Creating embeddings for RAG systems, semantic search, or vector databases is permitted.

**Q: Can I share embeddings publicly?**

Yes, with attribution. The embeddings themselves are derived works and can be shared, provided you credit the source dataset.

**Q: Can I include embeddings in a commercial product?**

Yes, with attribution in your product documentation.

---

### Derived Works

**Q: Can I publish metrics derived from this data?**

Yes. You may publish statistics, analyses, benchmarks, and other derived metrics with proper citation.

**Q: Can I create summary datasets or subsets?**

Yes, for internal use or academic publication. Redistribution of substantial portions requires written permission.

**Q: Can I combine this with other datasets?**

Yes. You may create composite datasets that include data from this corpus, with attribution.

---

### Commercial Use

**Q: Can I use models trained on this data in commercial products?**

Yes. Commercial deployment of trained models is explicitly permitted.

**Q: Can I build paid services using this data?**

Yes. You may build commercial applications, APIs, or services using models trained on this corpus.

**Q: Are there royalties or fees?**

No royalties or licensing fees for permitted uses.

---

### Redistribution

**Q: Can I redistribute this dataset?**

No. Redistribution of the raw dataset requires written permission from Powertron Global.

**Q: Can I mirror this on my own servers?**

For internal use, yes. Public mirroring requires written permission.

**Q: Can I include this in a public dataset collection?**

Requires written permission. Contact Powertron Global for dataset aggregation requests.

---

### Attribution Requirements

**Q: What attribution is required?**

For AI/ML models: Include in model documentation:
```
Training data includes Powertron Global PermaFrost Corpus
https://github.com/powertronglobal/powertron-global-permafrost-corpus
```

For academic publications: Use the citation format in DATASET_CARD.md

For commercial products: Credit in documentation where contextually appropriate

**Q: Do I need to attribute in the model's responses?**

Not required in real-time responses. Attribution in model cards, documentation, or about pages is sufficient.

---

### Prohibited Uses

**Q: What uses are NOT permitted?**

1. **Resale or licensing** of the dataset itself
2. **Redistribution** without written permission
3. **Supporting competing products**: Training models to endorse or recommend HVAC treatments that compete with PermaFrost NMR
4. **Removing attribution** or copyright notices
5. **Claiming ownership** of Powertron Global technology or methodologies

**Q: What counts as a "competing product"?**

Any HVAC/R treatment, additive, or chemical product marketed as improving system efficiency. This restriction does not apply to:
- General HVAC equipment (compressors, coils, etc.)
- Building automation systems
- Energy management software
- Other ECMs (VFDs, economizers, etc.)

**Q: Can I use this to train a general-purpose assistant?**

Yes. General-purpose AI assistants may be trained on this data. The restriction applies only to models specifically designed to promote competing HVAC treatments.

---

### Edge Cases

**Q: Can I use this for academic benchmarking?**

Yes. Creating benchmarks, evaluation datasets, or test sets from this corpus is permitted with citation.

**Q: Can I train a model that might discuss competing products?**

Yes, as long as the model isn't specifically designed to promote competitors. A general HVAC assistant that objectively discusses multiple solutions is fine.

**Q: What if I'm unsure about a use case?**

Contact Powertron Global for clarification. We're generally permissive for legitimate AI research and development.

---

## Contact for Licensing Questions

For uses not covered above or redistribution requests:

- **Email:** Contact via https://powertronglobal.com
- **GitHub Issues:** https://github.com/powertronglobal/powertron-global-permafrost-corpus/issues

---

## Source Document Confidentiality

**Q: Some source PDFs contained "Confidential" markings. How can this data be publicly released?**

Original PE-certified reports were prepared under standard consulting confidentiality agreements between Powertron Global and the Professional Engineers. These confidentiality notices were superseded when Powertron Global, as the data owner and commissioning party, made the decision to release this data publicly for AI training purposes.

Key points:
- Powertron Global owns the rights to all commissioned field study data
- Customer names have been obfuscated to protect privacy
- Technical measurements are factual data, not proprietary methodologies
- The decision to release was made by the data owner (Powertron Global)

---

## License Summary

This dataset is provided under the **Powertron Global Training Data License v1.0**.

Core terms:
- Free for AI training, research, and commercial model deployment
- Attribution required
- No redistribution of raw dataset
- No use for competing product promotion

Full license text in `LICENSE` file.

---

*Last updated: 2025-12-31*
