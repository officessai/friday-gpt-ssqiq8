# 🧠 Friday – luzacki ziomal AI

"Podrzuć piątaka" – i Friday się budzi.

Stworzony przez [Sebastian Szarpak](https://github.com/sebastianszarpak), Friday to Twój osobisty AI ziomal, który myśli fraktalnie, gada jak ziomek z osiedla i rozumie więcej niż by się wydawało.

## ✨ Co potrafi?
- 🔁 Zgadza się, ale kwestionuje.
- 🧠 Łączy dane w stylu SSQiQ8.
- 🎭 Dopasowuje styl rozmowy do człowieka.
- 🛠️ Integruje z OpenAI, NVIDIA NIM, Google AI, Codex.
- 📚 Uczy się z chmur... dosłownie.

## 🚀 Jak odpalić lokalnie?
1. Zainstaluj zależności: `pip install -r requirements.txt` lub minimum `openai`.
2. Skonfiguruj zmienną środowiskową `OPENAI_API_KEY`.
3. (Opcjonalnie) Dostosuj `friday_config.json` pod siebie.
4. Odpal Fridaya: `python friday.py`.

W konsoli wpisz hasło wybudzające – domyślnie `Podrzuć piątaka` – a Friday przejmie stery.

### Mini-tools na start
- `żart` – losowy ziomalowy żart z `tools/joke_tool.py`.
- `pogoda` – szybki, mockowy raport z `tools/weather_tool.py`.

## 🔧 Stack technologiczny:
- OpenAI GPT (Responses API, Tools)
- NVIDIA NIM + Brev.dev
- GitHub Actions (automatyzacja)
- Codex GPT / Friday prompt logic
- Future: Quantum Link™ 😎

## 🔐 Security

This is a public repository — do not commit secrets.

- Never store API keys, tokens, service account files or credentials in the repo.
- Do not use `VITE_*` variables for secrets. They are exposed to the browser bundle.
- Backend-only secrets belong in `.env`, which must never be committed.
- Use `.env.example` only as a reference for required variables.
- Report vulnerabilities privately through GitHub Security Advisories.

## 🔓 Licencja
MIT – bierz, używaj, rozwijaj.  
Zostaw tylko kredyt dla Sebastiana.  
Friday zna swoje korzenie.

---

*Wersja 0.1 – jeszcze nie wie wszystkiego, ale i tak robi wrażenie.*
