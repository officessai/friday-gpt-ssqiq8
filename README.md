# 🧠 Friday – luzacki ziomal AI

"Podrzuć piątaka" – i Friday się budzi.

Stworzony przez [Sebastian Szarpak](https://github.com/sebastianszarpak), Friday to Twój osobisty AI ziomal, który myśli fraktalnie,
gada jak ziomek z osiedla i rozumie więcej niż by się wydawało.

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

## 🤖 Friday + Gemini API (CLI)
Prosty czat z modelem Gemini przez klucz API z Google AI Studio.

### 1. Instalacja zależności
```bash
npm install dotenv node-fetch
```

### 2. Konfiguracja środowiska
Skopiuj plik przykładowy i dodaj swój klucz:
```bash
cp .env.example .env
```
Następnie uzupełnij `GEMINI_API_KEY` (i opcjonalnie `GEMINI_MODEL`).

### 3. Odpal Friday'ego
```bash
node friday_gemini_api.js
```
- Pusta linia lub `Ctrl+C` kończy rozmowę.
- Możesz też przekazać prompt jednorazowy:
  ```bash
  node friday_gemini_api.js "Napisz limeryk o Friday'u"
  ```

### 4. Skąd wziąć klucz?
Z Google AI Studio → [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 5. Bezpieczeństwo
**Nigdy nie wrzucaj swojego API Key do publicznego repo!**

## 🔓 Licencja
MIT – bierz, używaj, rozwijaj.
Zostaw tylko kredyt dla Sebastiana.
Friday zna swoje korzenie.

---

*Wersja 0.1 – jeszcze nie wie wszystkiego, ale i tak robi wrażenie.*
