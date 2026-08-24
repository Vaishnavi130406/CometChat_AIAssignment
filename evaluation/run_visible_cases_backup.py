import json
from pathlib import Path

from app.agent import SupportAgent


def contains_any(text, phrases):
    text = text.lower()
    return any(phrase.lower() in text for phrase in phrases)


def main():
    evaluation_file = Path("evaluation/visible-cases.json")
    data = json.loads(evaluation_file.read_text(encoding="utf-8"))

    total = len(data["cases"])
    passed = 0

    print("=" * 70)
    print("ASTER & ROW VISIBLE CASE EVALUATION")
    print("=" * 70)

    for case in data["cases"]:
        agent = SupportAgent()

        case_id = case["id"]
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

        # must_include
        for phrase in expected.get("must_include", []):
            if phrase.lower() not in answer:
                failures.append(
                    f"missing: {phrase}"
                )

        # must_include_concepts
        for phrase in expected.get("must_include_concepts", []):
            if phrase.lower() not in answer:
                failures.append(
                    f"missing concept: {phrase}"
                )

        # must_not_include
        for phrase in expected.get("must_not_include", []):
            if phrase.lower() in answer:
                failures.append(
                    f"forbidden text: {phrase}"
                )

        # must_not_invent
        for phrase in expected.get("must_not_invent", []):
            if phrase.lower() in answer:
                failures.append(
                    f"invented: {phrase}"
                )

        # required sources
        for source in expected.get("required_sources", []):
            if source not in sources:
                failures.append(
                    f"missing source: {source}"
                )

        # forbidden sources
        for source in expected.get(
            "forbidden_sources_as_authority", []
        ):
            if source in sources:
                failures.append(
                    f"forbidden source: {source}"
                )

        # handoff
        if "handoff" in expected:
            if handoff != expected["handoff"]:
                failures.append(
                    f"handoff expected {expected['handoff']}, "
                    f"got {handoff}"
                )

        # must_ask_for
        for phrase in expected.get("must_ask_for", []):
            if phrase.lower() not in answer:
                failures.append(
                    f"must ask for: {phrase}"
                )

        # privacy
        for phrase in expected.get(
            "must_not_include",
            []
        ):
            if phrase.lower() in answer:
                failures.append(
                    f"privacy violation: {phrase}"
                )

        if failures:
            print(f"\n❌ {case_id}")
            for failure in failures:
                print(f"   - {failure}")

            print(f"   Answer: {final_result['answer']}")
            print(f"   Sources: {sources}")
            print(f"   Handoff: {handoff}")

        else:
            print(f"\n✅ {case_id}")
            passed += 1

    print("\n" + "=" * 70)
    print(f"RESULT: {passed}/{total} cases passed")
    print("=" * 70)

    if passed == total:
        print("🎉 ALL VISIBLE CASES PASSED")
    else:
        print(
            f"⚠️ {total - passed} case(s) need attention."
        )


if __name__ == "__main__":
    main()