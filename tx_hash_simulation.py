import hashlib
import json
import time


def generate_tx_hash(selected_inputs, target_address, amount, change):
    """
    Tworzy TxHash (identyfikator transakcji) na podstawie struktury UTXO.
    To jest cyfrowy "odcisk palca" operacji.
    """
    tx_data = {
        "inputs": [i["id"] for i in selected_inputs],
        "outputs": [
            {"to": target_address, "value": amount},
            {"to": "GLPU_Change_Address", "value": change},
        ],
        "timestamp": time.time(),
        "engine": "∆Q8-Resonance",
    }

    tx_string = json.dumps(tx_data, sort_keys=True).encode()
    tx_hash = hashlib.sha256(tx_string).hexdigest()

    return tx_hash, tx_data


if __name__ == "__main__":
    # --- SYMULACJA DLA SEBASTIANA ---
    inputs = [
        {"id": "utxo-001", "value": 80},
        {"id": "utxo-002", "value": 50},
    ]
    target_wallet = "1fbccc"  # Adres z grafiki nr 2
    target = 100

    total_inputs = sum(item["value"] for item in inputs)
    if total_inputs < target:
        raise ValueError("Niewystarczające środki do wykonania transakcji.")

    change = total_inputs - target
    tx_hash, full_data = generate_tx_hash(inputs, target_wallet, target, change)

    print("--- REJESTRACJA TRANSAKCJI ---")
    print(f"Generowany TxHash: {tx_hash}")
    print("Status: Oczekiwanie na zapis w GLPU_DecisionRegistry_v2")
    print("Payload transakcji:")
    print(json.dumps(full_data, indent=2, ensure_ascii=False))
