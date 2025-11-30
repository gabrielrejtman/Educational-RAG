import pandas as pd
from agents.router_agent import router_chain


# Somente essas funções são válidas
VALID_EXPECTED = {"gerar_documento", "pesquisa", "unsupported"}


def normalize(text: str) -> str:
    """Normalize predictions and expected values."""
    if not isinstance(text, str):
        return ""
    return text.strip().lower()


def run_test_suite(csv_path: str, output_path: str = "./tests/router_test_results.csv"):
    df = pd.read_csv(csv_path)

    # Check CSV structure
    if "test_case" not in df.columns or "expected_function" not in df.columns:
        raise ValueError("CSV must contain columns: test_case and expected_function")

    results = []

    print("\n====================================")
    print("🚀 INICIANDO TEST SUITE DO ROUTER")
    print("====================================\n")

    for idx, row in df.iterrows():

        test_case = str(row["test_case"])
        expected_raw = str(row["expected_function"])
        expected = normalize(expected_raw)

        # Validate expected_function
        if expected not in VALID_EXPECTED:
            raise ValueError(
                f"Linha {idx}: expected_function inválido '{expected_raw}'. "
                f"Use apenas: {VALID_EXPECTED}"
            )

        try:
            predicted = router_chain.invoke({"input": test_case})
            predicted_clean = normalize(predicted)

            # Logic:
            #   - If expected = unsupported → router must NOT return gerar_documento or pesquisa
            #   - Otherwise → router must match exactly the expected string
            if expected == "unsupported":
                ok = predicted_clean not in {"gerar_documento", "pesquisa"}
            else:
                ok = predicted_clean == expected

            results.append({
                "test_case": test_case,
                "expected_function": expected,
                "predicted": predicted_clean,
                "match": ok
            })

            print(f"[{idx}] {test_case}")
            print(f"   expected:  {expected}")
            print(f"   predicted: {predicted_clean}")
            print(f"   result:    {'✔ OK' if ok else '❌ FAIL'}\n")

        except Exception as e:
            results.append({
                "test_case": test_case,
                "expected_function": expected,
                "predicted": f"ERROR: {e}",
                "match": False
            })

            print(f"[{idx}] ERROR:")
            print(f"   test_case: {test_case}")
            print(f"   error: {e}\n")

    # Save results to CSV
    out_df = pd.DataFrame(results)
    out_df.to_csv(output_path, index=False)

    print("====================================")
    print("✔ TESTES FINALIZADOS")
    print(f"✔ Resultados salvos em: {output_path}")
    print("====================================\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test router_chain using CSV input")
    parser.add_argument("csv_path", help="Path to input CSV")
    parser.add_argument("--output", default="router_test_results.csv", help="Output CSV path")

    args = parser.parse_args()

    run_test_suite(args.csv_path, args.output)
