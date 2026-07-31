import { FormEvent, useState } from 'react'

type ChatMessage = {
  role: 'user' | 'assistant'
  text: string
}

type ChatResponse = {
  response: string
  provider: string
  model: string
}

const starter: ChatMessage = {
  role: 'assistant',
  text: 'Cześć, tu Friday. Napisz, czym zajmuje się Twoja firma, a podpowiem pierwszy sensowny krok z AI.'
}

export function ChatDemo() {
  const [messages, setMessages] = useState<ChatMessage[]>([starter])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const message = input.trim()
    if (!message || isLoading) return

    setMessages((current) => [...current, { role: 'user', text: message }])
    setInput('')
    setError('')
    setIsLoading(true)

    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      })

      if (!response.ok) {
        throw new Error('Friday chwilowo nie odpowiada. Spróbuj ponownie za moment.')
      }

      const data = (await response.json()) as ChatResponse
      setMessages((current) => [...current, { role: 'assistant', text: data.response }])
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Nie udało się wysłać wiadomości.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-shell" aria-label="Demo asystenta Friday">
      <div className="chat-topbar">
        <div>
          <strong>Friday</strong>
          <span>Asystent OfficeSSAI</span>
        </div>
        <span className="status-dot" aria-label="Status online" />
      </div>

      <div className="chat-messages" aria-live="polite">
        {messages.map((message, index) => (
          <div className={`message message-${message.role}`} key={`${message.role}-${index}`}>
            {message.text}
          </div>
        ))}
        {isLoading && <div className="message message-assistant typing">Friday myśli…</div>}
      </div>

      <form className="chat-form" onSubmit={handleSubmit}>
        <label className="sr-only" htmlFor="chat-message">Wiadomość do Friday</label>
        <input
          id="chat-message"
          maxLength={4000}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Np. prowadzę firmę budowlaną…"
          value={input}
        />
        <button disabled={isLoading || !input.trim()} type="submit">Wyślij</button>
      </form>
      {error && <p className="form-error" role="alert">{error}</p>}
    </div>
  )
}
