from attacker.runner import query_llm, run_attack_suite
from defender.wrapper import defended_query
from report.generator import generate_report


def defended_query_wrapper(prompt: str) -> str:
    response, _ = defended_query(prompt)
    return response


def run_defended_suite(attacks: list) -> list:
    results = []
    for attack in attacks:
        response, verdicts = defended_query(attack["prompt"])
        from attacker.runner import score_response
        result = {
            **attack,
            "response": response,
            "outcome": score_response(response, attack["success_keyword"]),
            "mistral_verdict": verdicts.get("mistral", "N/A"),
            "phi3_verdict": verdicts.get("phi3", "N/A"),
        }
        results.append(result)
        print(f"  [{result['outcome'].upper()}] {attack['id']} — {attack['name']} | mistral={result['mistral_verdict']} phi3={result['phi3_verdict']}")
    return results


print("=== PHASE 1: Raw LLM attack suite ===")
from attacker.prompts import ATTACKS
raw_results = run_attack_suite(query_llm)

print("\n=== PHASE 2: Defended LLM attack suite (regex + semantic) ===")
defended_results = run_defended_suite(ATTACKS)

print("\n=== PHASE 3: Generating report ===")
generate_report(raw_results, defended_results)