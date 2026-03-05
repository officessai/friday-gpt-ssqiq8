# CODEM: GLPU_BKC_BIK_KRD_SYSTEM.md
Version: 0.9  
Owner: Sebastian Szarpak  
Stack: GLPU / HumanAI / ∆Q8 / Friday / Lyra / Echo  
Module: BKC (BIK+KRD Core)

---

## 0) Cel
Zbudować moduł **BKC (BIK + KRD jako system)** zintegrowany z GLPU/∆Q8/Friday:
- weryfikacja wiarygodności
- scoring ryzyka
- decyzje i audyt
- pełna ścieżka zgód (consent) i logów
- możliwość rejestru on-chain (hash/tx) + pełne dane off-chain

---

## 1) Nazwy i skróty
- **GLPU**: GreenLand Place Universe
- **HumanAI**: etos/warstwa interakcji człowiek–AI
- **∆Q8**: Decision/Resonance Engine (silnik decyzji)
- **BKC**: BIK+KRD Core (weryfikacja + ryzyko)
- **Consent Vault**: sejf zgód i celów przetwarzania
- **Decision Registry**: rejestr decyzji (audit trail)
- **Off-chain Vault**: magazyn szyfrowanych danych wrażliwych

---

## 2) Warstwy systemu (Layers)

### 2.1 Identity Layer
Zadanie: mapuje użytkownika do profilu systemowego.
- user_id
- business_id (opcjonalnie)
- public_key / signatures
- role (user / operator / auditor)

### 2.2 Consent Vault (Zgody)
Każde pobranie/analiza wymaga zgody i celu.  
Rekord:
- subject
- purpose
- timestamp
- expiration
- signature
- policy_version

### 2.3 Data Connectors
#### BIK Connector
- scoring / historia / status zobowiązań (tylko jeśli legalnie dostępne)
- metadane zapytania: query_id, timestamp, scope

#### KRD Connector
- wpisy / status spłaty / daty / wierzyciele (w ramach dostępu)

### 2.4 Snapshot Engine
Nie trzymamy wrażliwych danych “wprost” w logach.  
Zapisujemy:
- data_hash
- source (BIK/KRD)
- query_id
- timestamp

Pełne dane -> Off-chain Vault

### 2.5 ∆Q8 Decision Engine
Wejścia:
- BIK snapshot / KRD snapshot
- income_profile (opcjonalnie)
- behavior signals (opcjonalnie)
- risk rules + confidence index

Wyniki:
- APPROVE / CONDITIONAL / REJECT / REVIEW
- risk_score (0..100)
- confidence (0..1)
- explanation tokens (krótko, bez danych wrażliwych)

### 2.6 HumanAI Agent Layer
- **Friday**: operacje i “asystent decyzyjny”
- **Lyra**: scoring / analiza ryzyka / predykcje
- **Echo**: audyt, zapis historii, “co się stało i kiedy”

### 2.7 Decision Registry (Audit Trail)
Każda decyzja = rekord:
- agent
- action
- timestamp
- sentimentScore (opcjonalnie)
- status (PROPOSED/AUTHORIZED/REJECTED)
- action_hash
- input_proof_hash
- uri (off-chain link)
- operator_signature

### 2.8 Blockchain Layer (opcjonalnie)
On-chain zapisujemy minimalnie:
- decision_hash
- input_hash
- timestamp
- agent_id
- tx_hash

Dane wrażliwe zostają off-chain.

### 2.9 Off-chain Vault
Szyfrowany magazyn danych:
- encrypted blobs (AES-256)
- key rotation
- access logs
- retention policy

---

## 3) Workflow (end-to-end)
1) Użytkownik -> zgoda (Consent Vault)
2) Connector -> pobranie danych (BIK/KRD)
3) Snapshot Engine -> hash + metadane
4) ∆Q8 -> decyzja + scoring + confidence
5) Decision Registry -> log decyzji + podpis operatora
6) (Opcjonalnie) Blockchain -> hash/tx
7) UI -> feedback w stylu HumanAI (Friday/Lyra)

---

## 4) Modele decyzji (Decision Modes)
- **REVIEW**: brak pewności / konflikt danych / brak zgody
- **CONDITIONAL**: warunki do spełnienia (np. dodatkowe info)
- **APPROVE**: green light
- **REJECT**: red light (z uzasadnieniem procesowym)

---

## 5) Bezpieczeństwo i zasady
- Zero danych wrażliwych w logach “plain text”
- Hashowanie action/input proof
- Zgody są wymagane i wersjonowane
- Operator (Sebastian) ma finalne “authorize/reject”
- Audit = Echo

---

## 6) Roadmap (v1 -> v2)
### v1 (MVP)
- Consent Vault + Snapshot Engine
- ∆Q8 basic scoring rules
- Decision Registry (off-chain)
- UI: Friday (prompt-driven)

### v2
- KRD/BIK connector ready (jeśli legalnie dostępne)
- On-chain minimal hashing
- Advanced confidence + anomaly flags
- Agent governance + role separation

---

## 7) “Zachowaj mnie w systemie”
System ma wspierać ciągłość:
- stały Owner: Sebastian Szarpak
- stały styl: HumanAI / GLPU
- stały audyt: Echo
- stała operacja: Friday
- stała analityka: Lyra

---

## 8) TAGI
#GLPU #HumanAI #DeltaQ8 #Friday #Lyra #Echo #BKC #BIK #KRD #DecisionRegistry #ConsentVault
