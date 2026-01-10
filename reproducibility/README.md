# Reproducibility

This folder contains checksums and verification tools to ensure corpus integrity.

## Quick Start

### Verify Checksums

```bash
cd /path/to/powertron-global-permafrost-corpus
python reproducibility/scripts/verify_checksums.py
```

Expected output:
```
Verifying corpus_files.sha256...
  Passed: 56, Failed: 0, Missing: 0

Verifying extracted_text.sha256...
  Passed: 155, Failed: 0, Missing: 0

Verifying chunks.sha256...
  Passed: 155, Failed: 0, Missing: 0

SUCCESS: All checksums verified!
```

### Verbose Mode

```bash
python reproducibility/scripts/verify_checksums.py --verbose
```

Shows status for each file.

---

## Checksum Files

| File | Contents |
|------|----------|
| `checksums/corpus_files.sha256` | 56 corpus JSON files |
| `checksums/extracted_text.sha256` | 155 ALL_TEXT.txt files |
| `checksums/chunks.sha256` | 155 JSONL chunk files |

### Format

Standard SHA-256 checksum format:
```
<sha256_hash>  <relative_path>
```

Example:
```
a1b2c3d4...  corpus/manifest.json
e5f6g7h8...  documents/case-study-001/dataset/ALL_TEXT.txt
```

---

## Extraction Methodology

The corpus was extracted using these tools and parameters:

### Text Extraction

- **Tool:** PyMuPDF 1.23.x
- **Fallback:** pdfplumber, pytesseract (OCR)
- **Output:** `documents/*/extracted/text/page-NNNN.txt`

### Chunking

- **Tokenizer:** `cl100k_base` (OpenAI tiktoken)
- **Major US Retailer:** 800 tokens per chunk
- **Range:** 400-1200 tokens
- **Overlap:** 50 tokens
- **Split priority:** section → paragraph → sentence → hard limit

### ALL_TEXT.txt Format

```
═══ PAGE 001 ═══
[extracted text from page 1]

═══ PAGE 002 ═══
[extracted text from page 2]
```

---

## Source PDFs

Source PDFs are not included in this repository due to size constraints.

To fully reproduce the extraction:
1. Obtain source PDFs from Powertron Global
2. Place in `source/` folder
3. Run extraction pipeline (contact for scripts)

---

## Pinned Dependencies

```
pymupdf==1.23.26
tiktoken==0.5.2
pdfplumber==0.10.3
pikepdf==8.10.1
langdetect==1.0.9
```

---

## Contact

For extraction scripts or source PDF access:
- https://powertronglobal.com
- https://github.com/powertronglobal/powertron-global-permafrost-corpus/issues
