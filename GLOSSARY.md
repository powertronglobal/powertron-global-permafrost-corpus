# HVAC Terminology Glossary

This glossary defines key terms used throughout the Powertron Global PermaFrost Corpus. Understanding these concepts is essential for interpreting the measurement data and performance metrics.

---

## Efficiency Metrics

| Term | Definition | Good Values |
|------|------------|-------------|
| **COP** | Coefficient of Performance. Ratio of cooling output to energy input (dimensionless). Higher = more efficient. | 3.0-5.0+ |
| **EER** | Energy Efficiency Ratio. Cooling capacity (BTU/hr) divided by power input (watts). | 10-15+ |
| **SEER** | Seasonal Energy Efficiency Ratio. Like EER but averaged over a cooling season. | 14-25+ |
| **kW/ton** | Kilowatts per ton of cooling. Power required to produce one ton of cooling. Lower = more efficient. | 0.6-1.2 |

### Calculating COP from kW/ton

```
COP = 3.517 / (kW/ton)

Example: 1.0 kW/ton = COP of 3.517
Example: 0.7 kW/ton = COP of 5.02 (very efficient)
```

---

## Capacity Measurements

| Term | Definition | Notes |
|------|------------|-------|
| **Ton** | Unit of cooling capacity. 1 ton = 12,000 BTU/hr = 3.517 kW of cooling. | Named after ice melting rate |
| **BTU** | British Thermal Unit. Energy to raise 1 lb of water by 1°F. | 1 BTU = 1,055 joules |
| **BTU/hr** | Cooling rate (power). | 12,000 BTU/hr = 1 ton |
| **CFM** | Cubic Feet per Minute. Airflow rate through the system. | Higher CFM = more air movement |

---

## Thermodynamic Properties

| Term | Definition | Why It Matters |
|------|------------|----------------|
| **Enthalpy** | Total heat content of air (BTU/lb). Combines temperature and humidity. | Used to calculate actual cooling delivered |
| **Delta Enthalpy** | Difference between return air and supply air enthalpy. | Directly measures cooling work done |
| **Dry Bulb** | Standard air temperature (what a thermometer reads). | Basic temperature measurement |
| **Wet Bulb** | Temperature accounting for humidity (evaporative cooling effect). | Used with dry bulb to calculate enthalpy |
| **Dewpoint** | Temperature at which moisture condenses from air. | Indicates humidity level |
| **Superheat** | Temperature above refrigerant boiling point at evaporator. | Indicates proper refrigerant charge |
| **Subcooling** | Temperature below refrigerant condensing point at condenser. | Indicates proper refrigerant charge |

---

## Equipment Types

| Abbreviation | Full Name | Description |
|--------------|-----------|-------------|
| **DX** | Direct Expansion | Refrigerant evaporates directly in the air handler coil |
| **RTU** | Rooftop Unit | Packaged HVAC unit installed on building roof |
| **AHU** | Air Handling Unit | Component that conditions and circulates air |
| **CRAC** | Computer Room Air Conditioner | Precision cooling for data centers |
| **CRAH** | Computer Room Air Handler | Chilled water version of CRAC |
| **VRF** | Variable Refrigerant Flow | Multi-zone system with variable-speed compressor |
| **Chiller** | Chiller | Produces chilled water for building cooling |
| **Compressor** | Compressor | Heart of refrigeration cycle; compresses refrigerant |
| **Condenser** | Condenser | Rejects heat to outdoors; refrigerant condenses |
| **Evaporator** | Evaporator | Absorbs heat from indoors; refrigerant evaporates |

---

## Refrigerants

| Name | Type | Notes |
|------|------|-------|
| **R-22** | HCFC | Phased out (ozone depleting); common in older systems |
| **R-410A** | HFC | Current standard for residential/light commercial |
| **R-134a** | HFC | Common in automotive and some commercial |
| **R-407C** | HFC blend | R-22 replacement in existing systems |

---

## Measurement & Verification Terms

| Term | Definition |
|------|------------|
| **M&V** | Measurement and Verification. Process of quantifying energy savings. |
| **IPMVP** | International Performance Measurement and Verification Protocol. Industry standard for M&V. |
| **Baseline** | Pre-intervention performance measurement period. |
| **Post-treatment** | Performance measurement after intervention (e.g., after PermaFrost NMR). |
| **Weather normalization** | Adjusting data to account for different weather conditions between baseline and post periods. |
| **PE Certified** | Validated and stamped by a licensed Professional Engineer. Legally binding. |

---

## Oil Fouling (The Problem PermaFrost NMR Addresses)

| Term | Definition |
|------|------------|
| **Oil fouling** | Accumulation of compressor lubricant on heat exchanger surfaces, reducing heat transfer. |
| **Thermal barrier** | Insulating layer (oil film) that reduces efficiency of heat exchangers. |
| **Capacity degradation** | Loss of cooling capacity over time due to fouling and wear. |
| **Thermal restoration** | Recovery of lost cooling capacity after treatment. |

### ASHRAE Research on Oil Fouling

- **RP-751**: 1-2% oil by weight causes 33% reduction in heat transfer coefficient
- **RP-601**: Documents thermal barrier effect of lubricant on heat exchanger surfaces
- **Industry data**: Systems lose 20-40% efficiency within first 5-10 years from oil fouling

---

## Common Formulas

### Cooling Capacity (Tons)

```
Tons = (CFM × Delta_Enthalpy × 4.5) / 12,000

Where:
  CFM = Airflow rate
  Delta_Enthalpy = Return air enthalpy - Supply air enthalpy
  4.5 = Air density factor (lb/ft³ × 60 min/hr)
  12,000 = BTU/hr per ton
```

### Energy Efficiency Ratio (EER)

```
EER = (Cooling BTU/hr) / (Power in Watts)
    = (Tons × 12,000) / (kW × 1,000)
```

### Coefficient of Performance (COP)

```
COP = (Cooling Output in kW) / (Power Input in kW)
    = (Tons × 3.517) / kW
    = 3.517 / (kW/ton)
```

### Improvement Percentage

```
Improvement % = ((Post - Baseline) / Baseline) × 100

Example: COP improved from 2.0 to 3.5
Improvement = ((3.5 - 2.0) / 2.0) × 100 = 75%
```

---

## Quick Reference: What Good Looks Like

| Metric | Poor | Average | Good | Excellent |
|--------|------|---------|------|-----------|
| **kW/ton** | >1.5 | 1.0-1.5 | 0.7-1.0 | <0.7 |
| **COP** | <2.5 | 2.5-3.5 | 3.5-5.0 | >5.0 |
| **EER** | <8 | 8-12 | 12-16 | >16 |

---

## Further Reading

- ASHRAE Handbook of Fundamentals (thermodynamic properties)
- AHRI Standard 340/360 (commercial equipment testing)
- IPMVP Core Concepts (measurement and verification)
- `corpus/methodology_notes.json` - Measurement methodology used in this corpus
- `INSTRUMENTATION.md` - Sensor specifications and accuracy

---

*For questions about terminology, open a GitHub Discussion.*
