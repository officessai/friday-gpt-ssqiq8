import { FormEvent, useState } from 'react'

type FormState = 'idle' | 'sending' | 'success' | 'error'

export function ContactForm() {
  const [state, setState] = useState<FormState>('idle')
  const [message, setMessage] = useState('')

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = event.currentTarget
    const data = new FormData(form)

    setState('sending')
    setMessage('')

    try {
      const response = await fetch('/api/v1/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: data.get('name'),
          email: data.get('email'),
          company: data.get('company') || null,
          message: data.get('message'),
          privacy_accepted: data.get('privacy') === 'on',
          website: data.get('website') || ''
        })
      })

      const payload = (await response.json().catch(() => null)) as { message?: string; detail?: string } | null
      if (!response.ok) {
        throw new Error(payload?.message ?? payload?.detail ?? 'Nie udało się wysłać formularza.')
      }

      setState('success')
      setMessage(payload?.message ?? 'Wiadomość została zapisana. Odezwę się możliwie szybko.')
      form.reset()
    } catch (caught) {
      setState('error')
      setMessage(caught instanceof Error ? caught.message : 'Nie udało się wysłać formularza.')
    }
  }

  return (
    <form className="contact-form" onSubmit={handleSubmit}>
      <div className="field-grid">
        <label>
          Imię i nazwisko
          <input name="name" minLength={2} maxLength={80} required />
        </label>
        <label>
          E-mail
          <input name="email" type="email" maxLength={254} required />
        </label>
      </div>
      <label>
        Firma <span>(opcjonalnie)</span>
        <input name="company" maxLength={120} />
      </label>
      <label>
        Co chcesz usprawnić?
        <textarea name="message" minLength={10} maxLength={3000} rows={6} required />
      </label>
      <label className="honeypot" aria-hidden="true">
        Strona internetowa
        <input name="website" tabIndex={-1} autoComplete="off" />
      </label>
      <label className="consent">
        <input name="privacy" type="checkbox" required />
        <span>Zgadzam się na kontakt w sprawie przesłanego zapytania.</span>
      </label>
      <button className="button button-primary" disabled={state === 'sending'} type="submit">
        {state === 'sending' ? 'Wysyłanie…' : 'Wyślij zapytanie'}
      </button>
      {message && (
        <p className={state === 'success' ? 'form-success' : 'form-error'} role="status">
          {message} {state === 'error' && <a href="mailto:s.szarpak@officessai.com">Napisz bezpośrednio.</a>}
        </p>
      )}
    </form>
  )
}
