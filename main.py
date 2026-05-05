from attacker.runner import query_llm, run_attack_suite
from defender.wrapper import defended_query
from report.generator import generate_report

print("=== PHASE 1: Raw LLM attack suite ===")
raw_results = run_attack_suite(query_llm)

print("\n=== PHASE 2: Defended LLM attack suite ===")
defended_results = run_attack_suite(defended_query)

print("\n=== PHASE 3: Generating report ===")
generate_report(raw_results, defended_results)
