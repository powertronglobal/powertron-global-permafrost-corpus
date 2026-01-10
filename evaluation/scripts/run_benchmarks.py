#!/usr/bin/env python3
"""
Powertron Corpus Evaluation Suite

Runs all three benchmarks and produces a summary report.

Usage:
    python run_benchmarks.py --results-file results.json
    python run_benchmarks.py --interactive  # For manual RAG Q&A scoring
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def load_benchmark(name: str) -> dict:
    """Load a benchmark file."""
    script_dir = Path(__file__).parent
    benchmark_path = script_dir.parent / "benchmarks" / f"{name}.json"
    with open(benchmark_path) as f:
        return json.load(f)


def score_numeric(expected: float, actual: float, tolerance: float = 0.01) -> float:
    """
    Score a numeric value.
    Returns 1.0 if within tolerance, 0.5 if within 5x tolerance, 0.0 otherwise.
    """
    if expected is None or actual is None:
        return 0.0

    if expected == 0:
        return 1.0 if actual == 0 else 0.0

    diff = abs(expected - actual) / abs(expected)

    if diff <= tolerance:
        return 1.0
    elif diff <= tolerance * 5:
        return 0.5
    else:
        return 0.0


def score_table_extraction(test_case: dict, actual_values: dict) -> dict:
    """
    Score a table extraction test case.

    Args:
        test_case: The benchmark test case with expected values
        actual_values: The extracted values to score

    Returns:
        dict with scores per field and total
    """
    expected = test_case.get("expected_values", {})
    scores = {}
    total_score = 0.0
    total_fields = 0

    for field, expected_val in expected.items():
        if expected_val is None:
            continue

        actual_val = actual_values.get(field)
        score = score_numeric(expected_val, actual_val)
        scores[field] = {
            "expected": expected_val,
            "actual": actual_val,
            "score": score
        }
        total_score += score
        total_fields += 1

    return {
        "test_id": test_case["id"],
        "field_scores": scores,
        "total_score": total_score,
        "max_score": total_fields,
        "percentage": (total_score / total_fields * 100) if total_fields > 0 else 0
    }


def score_measurement_reconstruction(test_case: dict, extracted: dict) -> dict:
    """
    Score a measurement reconstruction test case.

    Args:
        test_case: The benchmark test case with expected extraction
        extracted: The extracted structured data to score

    Returns:
        dict with scores per field and total
    """
    expected = test_case.get("expected_extraction", {})
    scores = {}
    total_score = 0.0
    total_fields = 0

    for field, expected_val in expected.items():
        actual_val = extracted.get(field)

        # Handle different types
        if isinstance(expected_val, bool):
            score = 1.0 if actual_val == expected_val else 0.0
        elif isinstance(expected_val, str):
            score = 1.0 if str(actual_val).lower() == expected_val.lower() else 0.0
        elif isinstance(expected_val, (int, float)):
            score = score_numeric(expected_val, actual_val, tolerance=0.005)
        else:
            score = 0.0

        scores[field] = {
            "expected": expected_val,
            "actual": actual_val,
            "score": score
        }
        total_score += score
        total_fields += 1

    return {
        "test_id": test_case["id"],
        "category": test_case.get("category"),
        "difficulty": test_case.get("difficulty"),
        "field_scores": scores,
        "total_score": total_score,
        "max_score": total_fields,
        "percentage": (total_score / total_fields * 100) if total_fields > 0 else 0
    }


def run_rag_benchmark_interactive() -> dict:
    """
    Run RAG Q&A benchmark interactively with human scoring.
    """
    benchmark = load_benchmark("rag_qa")
    results = []

    print("\n" + "=" * 60)
    print("RAG Q&A Benchmark - Interactive Scoring")
    print("=" * 60)
    print("\nScoring guide:")
    print("  3 = Correct answer with accurate citation")
    print("  2 = Correct answer, missing/incorrect citation")
    print("  1 = Partially correct or imprecise")
    print("  0 = Incorrect or hallucinated")
    print("  s = Skip this question")
    print("  q = Quit benchmark")
    print()

    for i, q in enumerate(benchmark["questions"]):
        print(f"\n--- Question {i+1}/{len(benchmark['questions'])} ---")
        print(f"ID: {q['id']} | Category: {q['category']} | Difficulty: {q['difficulty']}")
        print(f"\nQuestion: {q['question']}")
        print(f"\nGround Truth: {q['ground_truth']}")
        print(f"Sources: {', '.join(q['source_files'])}")

        while True:
            score_input = input("\nEnter model's answer score (0-3, s=skip, q=quit): ").strip().lower()

            if score_input == 'q':
                break
            elif score_input == 's':
                results.append({
                    "id": q["id"],
                    "skipped": True
                })
                break
            elif score_input in ['0', '1', '2', '3']:
                results.append({
                    "id": q["id"],
                    "category": q["category"],
                    "difficulty": q["difficulty"],
                    "score": int(score_input),
                    "max_score": 3
                })
                break
            else:
                print("Invalid input. Enter 0, 1, 2, 3, s, or q.")

        if score_input == 'q':
            break

    # Calculate summary
    scored = [r for r in results if not r.get("skipped")]
    total_score = sum(r["score"] for r in scored)
    max_score = sum(r["max_score"] for r in scored)

    return {
        "benchmark": "rag_qa",
        "total_questions": len(benchmark["questions"]),
        "questions_scored": len(scored),
        "questions_skipped": len(results) - len(scored),
        "total_score": total_score,
        "max_score": max_score,
        "percentage": (total_score / max_score * 100) if max_score > 0 else 0,
        "results": results
    }


def generate_report(results: dict) -> str:
    """Generate a text report from benchmark results."""
    lines = [
        "=" * 60,
        "POWERTRON CORPUS EVALUATION REPORT",
        f"Generated: {datetime.now().isoformat()}",
        "=" * 60,
        ""
    ]

    for benchmark_name, data in results.items():
        lines.append(f"\n{benchmark_name.upper().replace('_', ' ')}")
        lines.append("-" * 40)

        if "percentage" in data:
            lines.append(f"Score: {data.get('total_score', 0):.1f} / {data.get('max_score', 0):.1f}")
            lines.append(f"Percentage: {data['percentage']:.1f}%")

        if "questions_scored" in data:
            lines.append(f"Questions: {data['questions_scored']} scored, {data.get('questions_skipped', 0)} skipped")

        if "test_count" in data:
            lines.append(f"Test cases: {data['test_count']}")

    lines.append("\n" + "=" * 60)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run Powertron Corpus benchmarks")
    parser.add_argument("--results-file", type=str, help="Load results from JSON file for scoring")
    parser.add_argument("--interactive", action="store_true", help="Run RAG benchmark interactively")
    parser.add_argument("--output", type=str, default="evaluation_results.json", help="Output file for results")
    args = parser.parse_args()

    results = {}

    if args.interactive:
        # Run interactive RAG benchmark
        results["rag_qa"] = run_rag_benchmark_interactive()

    if args.results_file:
        # Load and score results from file
        with open(args.results_file) as f:
            submitted = json.load(f)

        # Score table extraction if present
        if "table_extraction" in submitted:
            benchmark = load_benchmark("table_extraction")
            table_results = []
            for test_case in benchmark["test_cases"]:
                if test_case["id"] in submitted["table_extraction"]:
                    actual = submitted["table_extraction"][test_case["id"]]
                    score = score_table_extraction(test_case, actual)
                    table_results.append(score)

            total = sum(r["total_score"] for r in table_results)
            max_total = sum(r["max_score"] for r in table_results)
            results["table_extraction"] = {
                "test_count": len(table_results),
                "total_score": total,
                "max_score": max_total,
                "percentage": (total / max_total * 100) if max_total > 0 else 0,
                "results": table_results
            }

        # Score measurement reconstruction if present
        if "measurement_reconstruction" in submitted:
            benchmark = load_benchmark("measurement_reconstruction")
            measure_results = []
            for test_case in benchmark["test_cases"]:
                if test_case["id"] in submitted["measurement_reconstruction"]:
                    extracted = submitted["measurement_reconstruction"][test_case["id"]]
                    score = score_measurement_reconstruction(test_case, extracted)
                    measure_results.append(score)

            total = sum(r["total_score"] for r in measure_results)
            max_total = sum(r["max_score"] for r in measure_results)
            results["measurement_reconstruction"] = {
                "test_count": len(measure_results),
                "total_score": total,
                "max_score": max_total,
                "percentage": (total / max_total * 100) if max_total > 0 else 0,
                "results": measure_results
            }

    # Generate and print report
    if results:
        report = generate_report(results)
        print(report)

        # Save results
        output_path = Path(__file__).parent.parent / "results" / args.output
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {output_path}")
    else:
        print("No benchmarks run. Use --interactive or --results-file")
        print("\nAvailable benchmarks:")
        print("  - rag_qa.json (25 Q&A pairs)")
        print("  - table_extraction.json (15 test cases)")
        print("  - measurement_reconstruction.json (20 test cases)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
