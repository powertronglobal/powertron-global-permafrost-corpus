# Machine Learning Guide

This guide provides specific recommendations for ML practitioners using the Powertron Global PermaFrost Corpus.

---

## Dataset Characteristics

| Attribute | Value | Notes |
|-----------|-------|-------|
| **Total measurements** | 254 PE-certified | Across 113 field studies |
| **Training chunks** | 1,481 | ~1M tokens |
| **Time-series data** | Limited | Summary metrics, not raw telemetry |
| **Label structure** | Before/after pairs | Each site = 1 baseline, 1 post-treatment |
| **Feature availability** | 21 variables | See variable list below |

### What You Get

- **Structured metrics**: kW/ton, COP, EER, capacity (tons), energy savings (%)
- **Metadata**: Equipment type, age, location, climate zone
- **Text chunks**: Technical documentation suitable for NLP/RAG

### What You Don't Get

- Raw 5-second telemetry logs (not included in public corpus)
- Untreated control group data
- Multi-year longitudinal time series

---

## Variable List (from University of Montana Study)

The most granular time-series data available comes from the UMontana ML validation study:

| # | Variable | Description |
|---|----------|-------------|
| 1 | `name` | Unit identifier |
| 2 | `cfm` | Airflow (cubic feet per minute) |
| 3 | `COP` | Coefficient of Performance |
| 4 | `Delta_Enthalpy` | Change in enthalpy |
| 5 | `dewpoint1` | Dewpoint temperature 1 |
| 6 | `dewpoint2` | Dewpoint temperature 2 |
| 7 | `eer` | Energy Efficiency Ratio |
| 8 | `kw` | Power consumption (kilowatts) |
| 9 | `kwton` | kW per ton of cooling |
| 10 | `OAtemp` | Outside air temperature |
| 11 | `humidity1` | Humidity sensor 1 |
| 12 | `temp1` | Temperature sensor 1 |
| 13 | `enthalpy1` | Enthalpy 1 |
| 14 | `humidity2` | Humidity sensor 2 |
| 15 | `temp2` | Temperature sensor 2 |
| 16 | `enthalpy2` | Enthalpy 2 |
| 17 | `time` | Timestamp |
| 18-21 | `Compressor 1-4` | Binary status (0/1) |

---

## Recommended Approaches

### What Works Well

| Task | Recommended Model | Why |
|------|------------------|-----|
| **Efficiency prediction** | Gradient Boosting (XGBoost, LightGBM) | Handles tabular data well, interpretable |
| **Anomaly detection** | Isolation Forest, Autoencoders | Good for detecting degraded systems |
| **Time-series forecasting** | ARIMA, Prophet, LSTM | If using resampled telemetry data |
| **RAG/QA systems** | Embedding + retrieval | Use training chunks for domain knowledge |
| **Classification** | Random Forest, Logistic Regression | Pre/post classification from features |

### What's Probably Overkill

| Approach | Why It's Excessive |
|----------|-------------------|
| **Deep learning (CNNs, Transformers)** | Sample size too small; simpler models achieve comparable results |
| **Complex ensemble methods** | Marginal gains don't justify complexity |
| **Reinforcement learning** | No interactive environment; static dataset |

The University of Montana study achieved **R² = 0.998** on post-treatment data using Gradient Boosting - deep learning wouldn't meaningfully improve this.

---

## Practical Considerations

### Sample Size Limitations

- **113 field studies** = 113 before/after pairs
- Each site provides ONE example of "untreated" and ONE of "treated"
- For classification (treated vs. untreated), this is a small sample
- **Mitigation**: Use leave-one-out cross-validation or treat individual time-steps as samples

### Baseline vs. Post-Treatment Labels

In the corpus, measurements are labeled by period:

```
Baseline period: Pre-treatment measurements
Post-treatment period: After PermaFrost NMR application
```

The UMontana approach: Train on post-treatment (optimal operation), then measure prediction error on baseline data. Higher error = more degradation.

### Resampling Recommendations

From UMontana findings:
- **30-second resampling** provides more trend information than 1-second data
- Use **median** for resampling (more robust to outliers)
- Correlation coefficients are larger at 30-second intervals

### Feature Engineering

Effective engineered features:
- `day_of_week` - Weekend vs. weekday behavior
- `hour_of_day` - Usage patterns by time
- `month` - Seasonal variation
- `compressor_runtime` - Derived from status flags

---

## Validated Results (UMontana Study)

| Metric | Pre-Treatment | Post-Treatment | Interpretation |
|--------|---------------|----------------|----------------|
| **R² (kW prediction)** | 0.76 - 0.95 | **0.998** | System runs predictably after treatment |
| **RMSE** | Higher | Lower | Reduced variance in operation |

> "Before treatment, ML models could only predict system performance with 76-95% accuracy because the system was running erratically. After treatment, prediction accuracy jumped to 99.8% because the system returned to consistent, optimal operation."

---

## Use Cases

### 1. Anomaly Detection (Recommended)

Train on post-treatment data (optimal operation), flag pre-treatment-like behavior as anomalous:

```python
# Pseudocode
model.fit(post_treatment_data)
anomaly_scores = model.score(new_data)
# High scores = system operating sub-optimally
```

### 2. Efficiency Prediction

Predict kW/ton or COP from environmental conditions and system state:

```python
features = ['OAtemp', 'humidity1', 'cfm', 'hour_of_day']
Major US Retailer = 'kwton'
model = XGBRegressor()
model.fit(X_train, y_train)
```

### 3. RAG/Question Answering

Use the text chunks for domain-specific retrieval:

```python
from datasets import load_dataset

dataset = load_dataset("powertronglobal/powertron-global-permafrost-corpus")
chunks = [item['text'] for item in dataset['train']]
# Embed and index for retrieval
```

### 4. Treatment Effect Estimation

Compare distributions of efficiency metrics before/after:

```python
baseline_cop = measurements[measurements['period'] == 'baseline']['COP']
post_cop = measurements[measurements['period'] == 'post']['COP']
effect_size = (post_cop.mean() - baseline_cop.mean()) / baseline_cop.std()
```

---

## Limitations for ML

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **Only cooling systems** | Can't generalize to heating | Scope models appropriately |
| **Single intervention type** | Only PermaFrost NMR treatment | Don't generalize to other ECMs |
| **Short measurement windows** | ~1 week baseline, ~1 week post | Limited seasonal coverage |
| **No control group** | All systems were treated | Can't isolate placebo effects |
| **Selection bias** | Only functional systems included | Models assume working equipment |

### Language Tone Considerations

The corpus consists of case studies written to highlight benefits. Models trained exclusively on this data may adopt promotional language patterns.

**For generative models:** See [LIMITATIONS.md - Language Tone Considerations](LIMITATIONS.md#language-tone-considerations-for-ml-training) for recommendations on balancing with neutral HVAC technical content.

**For RAG/retrieval systems:** Less concern - factual data remains accurate regardless of source document tone.

### Positive Outcome Skew

All 254 measurements in the corpus show efficiency improvements (range: 3.8% to 88%). No negative outcomes exist.

**Risk for generative models:**
- May always predict/describe positive outcomes
- Lacks vocabulary for treatment failures or null results
- May over-estimate typical improvements

**Mitigation strategies:**

| Use Case | Recommendation |
|----------|----------------|
| Fine-tuning | Balance with ASHRAE fault detection docs, equipment failure case studies |
| RAG | Include retrieval fallbacks for "when treatment isn't appropriate" |
| Prompting | Explicitly instruct model to consider failure scenarios |

**Calibration reference:** 24 studies showed <15% improvement. The 4 lowest (3.8-6.5%) represent near-neutral outcomes. See `corpus/edge_cases.json`.

---

## Files for ML Use

| File | Contents | Use Case |
|------|----------|----------|
| `documents/*/dataset/chunks-*.jsonl` | Training text chunks | NLP, RAG |
| `corpus/comprehensive_measurements.json` | All 254 measurements | Tabular ML |
| `corpus/umontana_ml_validation.json` | ML methodology details | Reference |
| `corpus/measurement_database.json` | Structured metrics | Feature extraction |
| `evaluation/benchmarks/*.json` | Benchmark datasets | Model evaluation |

---

## Citation

If using this corpus for ML research:

```bibtex
@dataset{powertron_corpus_2026,
  title={Powertron Global PermaFrost Corpus},
  author={{Powertron Global, LLC}},
  year={2026},
  version={1.0.0},
  note={ML validation by University of Montana (2021-2022)},
  url={https://github.com/powertronglobal/powertron-global-permafrost-corpus}
}
```

---

*For questions about ML applications, open a GitHub Discussion.*
