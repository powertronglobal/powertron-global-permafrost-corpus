# Instrumentation & Calibration Specifications

This document consolidates sensor specifications, calibration standards, and measurement accuracy details for all data in the Powertron Global PermaFrost Corpus.

---

## Calibration Standards

All instrumentation used in PE-certified measurements adheres to:

| Standard | Description |
|----------|-------------|
| **NIST-traceable** | All sensors calibrated to National Institute of Standards and Technology standards |
| **ASHRAE 37** | Methods of Testing for Rating Electrically Driven Unitary Air-Conditioning and Heat Pump Equipment |
| **AHRI 340/360** | Performance Rating of Commercial and Industrial Unitary Air-Conditioning and Heat Pump Equipment |

---

## Field Measurement Instruments

The following instruments were used in the FAU academic validation and PE-certified field studies:

### Temperature & Humidity

| Instrument | Model | Measurement | Accuracy | Calibration |
|------------|-------|-------------|----------|-------------|
| **Fieldpiece Psychrometer** | SRH3 | Dry bulb, wet bulb, humidity | ±1% | NIST-traceable |
| **Testo Digital Analyzer** | 550 | Pressure, temperature | ±0.75% | CE certified |

### Airflow

| Instrument | Model | Measurement | Accuracy | Calibration |
|------------|-------|-------------|----------|-------------|
| **Fieldpiece Anemometer** | STA2 | CFM (hot wire) | ±1% | NIST-traceable |

### Electrical

| Instrument | Model | Measurement | Accuracy | Calibration |
|------------|-------|-------------|----------|-------------|
| **Fluke True RMS Multimeter** | 381 | Voltage, amperage, power factor | ±0.01% | NIST-traceable |
| **FLUKE Multimeter** | 16 | Voltage, temperature | Per FLUKE specs | Factory calibrated |

---

## IoT Monitoring Platform (F2 FMV)

For continuous monitoring studies, the F2 FMV platform provides:

| Specification | Value |
|---------------|-------|
| **Power Meter Class** | IEC 62053-22 Class 0.5s |
| **ANSI Standard** | ANSI C12.20 Class 0.5 |
| **Classification** | Revenue Grade Accuracy |
| **Measurement Points** | Up to 50 per device |
| **Sampling Rate** | 1-second intervals (raw) |
| **Resampling** | 30-second median for analysis |

### Calculated Metrics

The platform computes in real-time:
- kW/ton (energy efficiency)
- COP (Coefficient of Performance)
- EER (Energy Efficiency Ratio)
- Superheat and subcooling
- Enthalpy-based capacity

---

## Measurement Uncertainty

Based on instrument specifications and propagated error:

| Metric | Typical Accuracy | Notes |
|--------|------------------|-------|
| **Temperature** | ±0.5°F | NIST-calibrated sensors |
| **Power (kW)** | ±1-2% | Revenue-grade metering |
| **Airflow (CFM)** | ±5% | Varies by measurement method |
| **Pressure** | ±0.75% | Testo 550 specification |
| **Electrical (V, A, PF)** | ±0.01% | Fluke 381 specification |
| **Calculated efficiency** | ±2-3% | Propagated from sensor accuracy |

### Important Notes

- Error bars and confidence intervals are **not provided** in source documents
- Calculated metrics (COP, EER, kW/ton) inherit uncertainty from input measurements
- Weather normalization uses TMY3 data and degree-day methodology

---

## Laboratory Testing Standards

Third-party lab tests followed these standards:

| Lab | Standards Applied |
|-----|-------------------|
| **NSF International** | ANSI/AHRI 340/360-2007, Good Laboratory Practice (40 CFR Part 160) |
| **Underwriters Laboratories** | IPMVP Option B, UL field verification protocols |
| **China National Lab A (China)** | GB/T7725-2004, ISO5151, ASHRAE 58 |
| **Florida Atlantic University** | IPMVP Option B, ASHRAE methodologies |

---

## Key Measurements Collected

Per IPMVP Option B (Retrofit Isolation: All Parameter Measurement):

| Category | Measurements |
|----------|--------------|
| **Refrigerant** | Suction line temp/pressure, discharge line temp/pressure |
| **Air Side** | Supply air temp (dry bulb, wet bulb), return air temp (dry bulb, wet bulb) |
| **Electrical** | Voltage, amperage, power factor, kW |
| **Operational** | Runtime hours, compressor status |

---

## Data Quality Exclusions

Measurements were excluded from analysis when:

| Reason | Impact |
|--------|--------|
| Incomplete baseline data | Baseline measurements interrupted |
| Calibration issues | Instrumentation errors discovered during analysis |
| Mechanical issues | Compressor failures, refrigerant leaks found |
| Site access restrictions | Post-measurement access denied |

**Excluded records:** 62 of 254 (24.4%) - retained in raw data for transparency but excluded from statistical analysis per IPMVP protocols.

---

## Verification Process

1. **Field Engineer** collects measurements using calibrated instruments
2. **PE Review** validates methodology and data quality
3. **Calculation** using ASHRAE/AHRI standard formulas
4. **Certification** by licensed Professional Engineer

For UL-verified studies, UL personnel witnessed and verified all baseline and post-treatment measurements.

---

## References

- `corpus/methodology_notes.json` - Detailed measurement methodology
- `corpus/third_party_validation.json` - Lab testing specifics
- `corpus/fau_test_records.json` - Academic validation details
- `corpus/powertron_patents.json` - Patented M&V methodology (US11062404B2)

---

*For questions about measurement methodology, open a GitHub Discussion.*
