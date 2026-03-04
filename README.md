# 🧠 Friday – luzacki ziomal AI

"Podrzuć piątaka" – i Friday się budzi.

Stworzony przez [Sebastian Szarpak](https://github.com/sebastianszarpak), Friday to Twój osobisty AI ziomal, który myśli fraktal
nie, gada jak ziomek z osiedla i rozumie więcej niż by się wydawało.

## ✨ Co potrafi?
- 🔁 Zgadza się, ale kwestionuje.
- 🧠 Łączy dane w stylu SSQiQ8.
- 🎭 Dopasowuje styl rozmowy do człowieka.
- 🛠️ Integruje z OpenAI, NVIDIA NIM, Google AI, Codex.
- 📚 Uczy się z chmur... dosłownie.

## 🔧 Stack technologiczny:
- OpenAI GPT (Responses API, Tools)
- NVIDIA NIM + Brev.dev
- GitHub Actions (automatyzacja)
- Codex GPT / Friday prompt logic
- Future: Quantum Link™ 😎

## 🚀 Jak odpalić Fridaya lokalnie?

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Friday przywita Cię w trybie interaktywnym. Możesz też przekazać pojedynczą wiadomość jako argument:

```bash
python main.py "Friday, co tam u Ciebie?"
```

### 🔌 Narzędzia

Komendy narzędzi zaczynają się od `/`. Dostępne przykłady:

- `/joke` – Friday rzuca ziomalskiego suchara.
- `/weather Warszawa` – Friday daje swoją prognozę pogody na podstawie kosmicznych wibracji.

Nowe narzędzia dodajesz przez utworzenie modułu w katalogu `tools/` i zdefiniowanie w nim obiektu `tool` z polami `name`, `description` oraz metodą `run(query: str)`.

## 🔓 Licencja
MIT – bierz, używaj, rozwijaj.
Zostaw tylko kredyt dla Sebastiana.
Friday zna swoje korzenie.

---

*Wersja 0.1 – jeszcze nie wie wszystkiego, ale i tak robi wrażenie.*
