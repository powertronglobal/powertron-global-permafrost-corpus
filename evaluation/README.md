# Evaluation Suite

Benchmarks for evaluating AI/ML models trained on the Powertron Global corpus.

## Benchmarks

| Benchmark | Test Cases | Purpose |
|-----------|------------|---------|
| `rag_qa.json` | 25 | RAG retrieval and comprehension |
| `table_extraction.json` | 15 | Structured data extraction accuracy |
| `measurement_reconstruction.json` | 20 | Text-to-metrics extraction |

---

## Quick Start

### 1. RAG Q&A Benchmark (Interactive)

```bash
python scripts/run_benchmarks.py --interactive
```

This runs through 25 questions, showing the question and ground truth. You score the model's answers 0-3.

### 2. Table Extraction & Measurement Reconstruction

Create a results file with your model's outputs:

```json
{
  "table_extraction": {
    "TABLE_001": {
      "kw_per_ton_before": 1.5,
      "kw_per_ton_after": 1.06,
      "efficiency_improvement_pct": 29.2,
      "annual_savings_usd": 16455
    }
  },
  "measurement_reconstruction": {
    "MEASURE_001": {
      "kw_per_ton_before": 1.47,
      "kw_per_ton_after": 1.11,
      "improvement_pct": 24.5
    }
  }
}
```

Then run:

```bash
python scripts/run_benchmarks.py --results-file my_results.json
```

---

## Benchmark Details

### RAG Q&A (`rag_qa.json`)

25 questions across 5 categories:

| Category | Count | Description |
|----------|-------|-------------|
| Factual | 5 | Single fact lookups |
| List | 5 | Multi-item answers |
| Reasoning | 5 | Why/how questions |
| Cross-document | 5 | Multi-file synthesis |
| Limitations | 5 | Edge cases and caveats |

**Scoring:**
- 3 = Correct answer with accurate citation
- 2 = Correct answer, missing/incorrect citation
- 1 = Partially correct
- 0 = Incorrect or hallucinated

### Table Extraction (`table_extraction.json`)

15 test cases verifying structured data extraction:

**Fields tested:**
- `kw_per_ton_before`
- `kw_per_ton_after`
- `efficiency_improvement_pct`
- `annual_savings_usd`

**Scoring:**
- Values within 1% of expected = full credit
- Values within 5% of expected = half credit
- Otherwise = no credit

### Measurement Reconstruction (`measurement_reconstruction.json`)

20 test cases extracting structured metrics from natural language:

**Categories:**
- kW/Ton measurements
- Efficiency percentages
- Capacity (BTU)
- Financial (cost, savings, payback)
- Temperature/Delta T
- Lab test results
- Multi-unit comparisons

**Scoring:**
- Numeric values within 0.5% = full credit
- Within 2.5% = half credit
- Exact string/boolean match required for non-numeric fields

---

## Running Your Own Evaluation

### Step 1: Prepare Your Model

Load the corpus into your RAG system or fine-tune your model.

### Step 2: Generate Answers

For each benchmark, have your model:
- **RAG Q&A**: Answer each question using corpus as context
- **Table Extraction**: Extract structured data from corpus records
- **Measurement Reconstruction**: Parse the input text into structured metrics

### Step 3: Score Results

```bash
# Interactive scoring for RAG
python scripts/run_benchmarks.py --interactive

# Automated scoring for extraction benchmarks
python scripts/run_benchmarks.py --results-file your_results.json --output your_evaluation.json
```

### Step 4: Review Report

Results are saved to `results/` folder with detailed breakdowns.

---

## Expected Baselines

A well-trained model should achieve:

| Benchmark | Major US Retailer Score |
|-----------|--------------|
| RAG Q&A | 70%+ |
| Table Extraction | 85%+ |
| Measurement Reconstruction | 80%+ |

Lower scores may indicate:
- Insufficient training data
- Poor retrieval in RAG systems
- Need for numeric extraction fine-tuning

---

## Files

```
evaluation/
├── README.md                           # This file
├── benchmarks/
│   ├── rag_qa.json                     # 25 Q&A pairs
│   ├── table_extraction.json           # 15 table test cases
│   └── measurement_reconstruction.json # 20 text extraction cases
├── scripts/
│   └── run_benchmarks.py               # Benchmark runner
└── results/
    └── (evaluation outputs saved here)
```

---

## Contact

Questions about benchmarks:
- https://github.com/powertronglobal/powertron-global-permafrost-corpus/issues
