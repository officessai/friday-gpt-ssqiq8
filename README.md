# 🧠 Friday – luzacki ziomal AI

"Podrzuć piątaka" – i Friday się budzi.

Stworzony przez [Sebastian Szarpak](https://github.com/sebastianszarpak), Friday to Twój osobisty AI ziomal, który myśli fraktalnie, gada jak ziomek z osiedla i rozumie więcej niż by się wydawało.

## ✨ Co potrafi?
- 🔁 Zgadza się, ale kwestionuje.
- 🧠 Łączy dane w stylu SSQiQ8.
- 🎭 Dopasowuje styl rozmowy do człowieka.
- 🛠️ Integruje z OpenAI, NVIDIA NIM, Google AI, Codex.
- 📚 Uczy się z chmur... dosłownie.
- 📝 Prowadzi rejestr ECHO dla ważnych chwil.

## 🔧 Stack technologiczny:
- OpenAI GPT (Responses API, Tools)
- NVIDIA NIM + Brev.dev
- GitHub Actions (automatyzacja)
- Codex GPT / Friday prompt logic
- Future: Quantum Link™ 😎

## 📔 ECHO – cichy kronikarz

W katalogu `echo_agent/` znajdziesz implementację agenta ECHO. Reaguje on jedynie na
komendę `Zarejestruj`, przechowując zapis w neutralnym, poetycko-dokumentacyjnym
stylu. Przykład użycia:

```python
from echo_agent import EchoAgent

agent = EchoAgent()
agent.observe("Zarejestruj: Wybrzmiała decyzja zespołu")

for entry in agent.history():
    print(entry.render())
```

Testy jednostkowe uruchomisz poleceniem `pytest`.

## 🔓 Licencja
MIT – bierz, używaj, rozwijaj.  
Zostaw tylko kredyt dla Sebastiana.  
Friday zna swoje korzenie.

---

*Wersja 0.1 – jeszcze nie wie wszystkiego, ale i tak robi wrażenie.*
