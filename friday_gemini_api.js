#!/usr/bin/env node

require('dotenv').config();
const readline = require('readline');

const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

const API_KEY = process.env.GEMINI_API_KEY;
const MODEL = process.env.GEMINI_MODEL || 'gemini-1.5-flash-latest';

if (!API_KEY) {
  console.error('❌ Brak zmiennej środowiskowej GEMINI_API_KEY. Dodaj ją do pliku .env.');
  process.exit(1);
}

async function askGemini(prompt) {
  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}`;

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      contents: [
        {
          role: 'user',
          parts: [{ text: prompt }]
        }
      ]
    })
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Gemini API zwróciło błąd ${response.status}: ${errorBody}`);
  }

  const data = await response.json();
  const candidate = data?.candidates?.[0];
  const parts = candidate?.content?.parts || [];
  const text = parts
    .map((part) => part.text)
    .filter(Boolean)
    .join('\n')
    .trim();

  if (!text) {
    throw new Error('Gemini API nie zwróciło żadnej treści. Sprawdź prompt lub konfigurację.');
  }

  return text;
}

function startChat() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log('🤖 Friday x Gemini — pogadajmy! (Ctrl+C lub pusta linia żeby wyjść)');

  const askQuestion = () => {
    rl.question('\nTy: ', async (input) => {
      const trimmed = input.trim();

      if (!trimmed) {
        rl.close();
        return;
      }

      try {
        const reply = await askGemini(trimmed);
        console.log(`Friday: ${reply}`);
      } catch (error) {
        console.error(`Błąd: ${error.message}`);
      }

      askQuestion();
    });
  };

  rl.on('SIGINT', () => {
    rl.close();
  });

  rl.on('close', () => {
    console.log('\n👋 Do zobaczenia!');
    process.exit(0);
  });

  askQuestion();
}

const cliPrompt = process.argv.slice(2).join(' ').trim();

(async () => {
  if (cliPrompt) {
    try {
      const reply = await askGemini(cliPrompt);
      console.log(`Friday: ${reply}`);
    } catch (error) {
      console.error(`Błąd: ${error.message}`);
      process.exitCode = 1;
    }
    return;
  }

  startChat();
})();
