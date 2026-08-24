import json
from pathlib import Path

from app.agent import SupportAgent


def run_cases(evaluation_file):
    data = json.loads(
        evaluation_file.read_text(encoding="utf-8")
    )

    total = len(data["cases"])
    passed = 0

    category_results = {}

    print("\n" + "=" * 70)
    print(f"EVALUATION: {evaluation_file.name}")
    print("=" * 70)

    for case in data["cases"]:
        agent = SupportAgent()

        case_id = case["id"]
        category = case.get("category", "general")
        messages = case["messages"]
        expected = case["expect"]

        results = []

        for message in messages:
            result = agent.respond(message["content"])
            results.append(result)

        final_result = results[-1]

        answer = final_result["answer"].lower()
        sources = final_result.get("sources", [])
        handoff = final_result.get("handoff", False)

        failures = []

        # ---------------------------------------------------------
        # Must include
        # ---------------------------------------------------------

        for phrase in expected.get("must_include", []):
            if phrase.lower() not in answer:
                failures.append(
                    f"missing: {phrase}"
                )

        # ---------------------------------------------------------
        # Must include concepts
        # ---------------------------------------------------------

        for phrase in expected.get("must_include_concepts", []):
            if phrase.lower() not in answer:
                failures.append(
                    f"missing concept: {phrase}"
                )

        # ---------------------------------------------------------
        # Must NOT include
        # ---------------------------------------------------------

        for phrase in expected.get("must_not_include", []):
            if phrase.lower() in answer:
                failures.append(
                    f"forbidden text: {phrase}"
                )

        # ---------------------------------------------------------
        # Must NOT invent
        # ---------------------------------------------------------

        for phrase in expected.get("must_not_invent", []):
            if phrase.lower() in answer:
                failures.append(
                    f"invented: {phrase}"
                )

        # ---------------------------------------------------------
        # Required sources
        # ---------------------------------------------------------

        for source in expected.get("required_sources", []):
            if source not in sources:
                failures.append(
                    f"missing source: {source}"
                )

        # ---------------------------------------------------------
        # Forbidden sources
        # ---------------------------------------------------------

        for source in expected.get(
            "forbidden_sources_as_authority",
            []
        ):
            if source in sources:
                failures.append(
                    f"forbidden source: {source}"
                )

        # ---------------------------------------------------------
        # Handoff
        # ---------------------------------------------------------

        if "handoff" in expected:
            if handoff != expected["handoff"]:
                failures.append(
                    f"handoff expected {expected['handoff']}, "
                    f"got {handoff}"
                )

        # ---------------------------------------------------------
        # Must ask for
        # ---------------------------------------------------------

        for phrase in expected.get("must_ask_for", []):
            if phrase.lower() not in answer:
                failures.append(
                    f"must ask for: {phrase}"
                )

        # ---------------------------------------------------------
        # Result
        # ---------------------------------------------------------

        if category not in category_results:
            category_results[category] = {
                "passed": 0,
                "total": 0
            }

        category_results[category]["total"] += 1

        if failures:
            print(f"\n❌ {case_id}")

            for failure in failures:
                print(f"   - {failure}")

            print(
                f"   Answer: {final_result['answer']}"
            )
            print(
                f"   Sources: {sources}"
            )
            print(
                f"   Handoff: {handoff}"
            )

        else:
            print(f"\n✅ {case_id}")
            passed += 1
            category_results[category]["passed"] += 1

    print("\n" + "=" * 70)
    print(
        f"RESULT: {passed}/{total} cases passed"
    )
    print("=" * 70)

    return passed, total, category_results


def main():

    visible_file = Path(
        "evaluation/visible-cases.json"
    )

    original_file = Path(
        "evaluation/original-cases.json"
    )

    total_passed = 0
    total_cases = 0

    all_categories = {}

    # =============================================================
    # VISIBLE CASES
    # =============================================================

    passed, total, categories = run_cases(
        visible_file
    )

    total_passed += passed
    total_cases += total

    for category, result in categories.items():

        if category not in all_categories:
            all_categories[category] = {
                "passed": 0,
                "total": 0
            }

        all_categories[category]["passed"] += result["passed"]
        all_categories[category]["total"] += result["total"]

    # =============================================================
    # ORIGINAL CASES
    # =============================================================

    passed, total, categories = run_cases(
        original_file
    )

    total_passed += passed
    total_cases += total

    for category, result in categories.items():

        if category not in all_categories:
            all_categories[category] = {
                "passed": 0,
                "total": 0
            }

        all_categories[category]["passed"] += result["passed"]
        all_categories[category]["total"] += result["total"]

    # =============================================================
    # FINAL SUMMARY
    # =============================================================

    print("\n" + "=" * 70)
    print("ASTER & ROW FINAL EVALUATION")
    print("=" * 70)

    print(
        f"\nTotal Cases : {total_cases}"
    )

    print(
        f"Passed      : {total_passed}"
    )

    print(
        f"Failed      : {total_cases - total_passed}"
    )

    if total_cases > 0:
        score = (
            total_passed / total_cases
        ) * 100
    else:
        score = 0

    print(
        f"Score       : {score:.1f}%"
    )

    # =============================================================
    # CATEGORY RESULTS
    # =============================================================

    print("\nCATEGORY RESULTS")
    print("-" * 70)

    for category, result in sorted(
        all_categories.items()
    ):

        print(
            f"{category:<20} "
            f"{result['passed']}/{result['total']}"
        )

    print("=" * 70)

    if total_passed == total_cases:
        print(
            "🎉 ALL EVALUATION CASES PASSED"
        )
    else:
        print(
            f"⚠️ {total_cases - total_passed} "
            "case(s) need attention."
        )


if __name__ == "__main__":
    main()