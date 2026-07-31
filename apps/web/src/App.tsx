import { ChatDemo } from './components/ChatDemo'
import { ContactForm } from './components/ContactForm'

const services = [
  {
    number: '01',
    title: 'Strona, która sprzedaje',
    text: 'Projektujemy szybkie strony z jasną ofertą, formularzem kontaktowym i analityką.'
  },
  {
    number: '02',
    title: 'Asystent AI dla klientów',
    text: 'Friday odpowiada na pytania, przedstawia ofertę i kieruje wartościowe rozmowy do człowieka.'
  },
  {
    number: '03',
    title: 'Automatyzacje bez chaosu',
    text: 'Łączymy formularze, pocztę, dokumenty i chmurę, żeby firma nie przepisywała danych ręcznie.'
  }
]

const packages = [
  {
    name: 'Start',
    price: 'od 499 zł',
    description: 'Pierwsze wdrożenie i uporządkowanie podstaw.',
    items: ['Audyt potrzeb', 'Prosta strona lub landing page', 'Formularz kontaktowy', 'Podstawowa konfiguracja domeny']
  },
  {
    name: 'Firma',
    price: 'od 999 zł',
    description: 'Kompletna obecność online z działającym AI.',
    items: ['Wszystko ze Start', 'Asystent Friday', 'Bezpieczny backend API', 'Analityka i optymalizacja'],
    featured: true
  },
  {
    name: 'Rozwój',
    price: 'od 1499 zł',
    description: 'Automatyzacje dopasowane do procesu firmy.',
    items: ['Wszystko z Firma', 'Integracje z chmurą', 'Automatyzacja dokumentów', 'Miesięczne wsparcie techniczne']
  }
]

function App() {
  return (
    <>
      <header className="site-header">
        <a className="brand" href="#top" aria-label="OfficeSSAI — strona główna">
          <span className="brand-mark">O</span>
          <span><strong>OFFICE</strong>SSAI</span>
        </a>
        <nav aria-label="Główna nawigacja">
          <a href="#uslugi">Usługi</a>
          <a href="#friday">Friday</a>
          <a href="#cennik">Cennik</a>
          <a className="nav-cta" href="#kontakt">Kontakt</a>
        </nav>
      </header>

      <main id="top">
        <section className="hero section-wrap">
          <div className="hero-copy">
            <h1>AI dla firmy, które naprawdę pracuje.</h1>
            <p>
              Łączymy stronę internetową, automatyzację i asystenta Friday w jeden prosty system,
              który zdobywa zapytania i oszczędza czas.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#kontakt">Uruchom projekt</a>
              <a className="button button-secondary" href="#friday">Zobacz Friday w akcji</a>
            </div>
            <p className="hero-note">Bez wystawiania kluczy API. Bez abonamentu za samo patrzenie na panel.</p>
          </div>
          <div className="hero-orbit" aria-hidden="true">
            <div className="orbit-ring orbit-ring-one" />
            <div className="orbit-ring orbit-ring-two" />
            <div className="orbit-core">AI</div>
            <span className="orbit-label orbit-openai">OpenAI</span>
            <span className="orbit-label orbit-azure">Azure</span>
            <span className="orbit-label orbit-github">GitHub</span>
          </div>
        </section>

        <section className="trust-strip" aria-label="Technologie">
          <span>OpenAI</span><span>Microsoft Azure</span><span>GitHub</span><span>Google AI</span><span>OVHcloud</span>
        </section>

        <section className="section-wrap section" id="uslugi">
          <div className="section-heading">
            <h2>Od pomysłu do działającego systemu</h2>
            <p>Nie sprzedajemy pudełka z napisem AI. Budujemy konkretny przepływ dla konkretnej firmy.</p>
          </div>
          <div className="service-list">
            {services.map((service) => (
              <article className="service-row" key={service.number}>
                <span>{service.number}</span>
                <h3>{service.title}</h3>
                <p>{service.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="friday-section section" id="friday">
          <div className="section-wrap friday-grid">
            <div className="friday-copy">
              <h2>Friday odbiera pierwszą zmianę</h2>
              <p>
                Asystent działa na bezpiecznym backendzie. Klucz modelu nigdy nie trafia do przeglądarki,
                a dostawcę możesz przełączyć między OpenAI i Azure przez konfigurację serwera.
              </p>
              <ul className="check-list">
                <li>Odpowiada na pytania o ofertę</li>
                <li>Zbiera kontekst przed rozmową z klientem</li>
                <li>Ma limit długości i kontrolowane komunikaty błędów</li>
                <li>Może rosnąć razem z bazą wiedzy firmy</li>
              </ul>
            </div>
            <ChatDemo />
          </div>
        </section>

        <section className="section-wrap section" id="cennik">
          <div className="section-heading">
            <h2>Prosty start, jasny koszt</h2>
            <p>Cena zależy od zakresu, ale punkt wejścia jest czytelny od pierwszej rozmowy.</p>
          </div>
          <div className="pricing-grid">
            {packages.map((item) => (
              <article className={`price-card${item.featured ? ' price-featured' : ''}`} key={item.name}>
                <div>
                  <h3>{item.name}</h3>
                  <strong>{item.price}</strong>
                  <p>{item.description}</p>
                </div>
                <ul>
                  {item.items.map((feature) => <li key={feature}>{feature}</li>)}
                </ul>
                <a className={item.featured ? 'button button-primary' : 'button button-secondary'} href="#kontakt">
                  Zapytaj o zakres
                </a>
              </article>
            ))}
          </div>
        </section>

        <section className="contact-section section" id="kontakt">
          <div className="section-wrap contact-grid">
            <div className="contact-copy">
              <h2>Zbudujmy pierwszy element, który zarabia</h2>
              <p>Opisz firmę i największy zator. Odpowiedź trafi na adres podany w formularzu.</p>
              <a href="mailto:s.szarpak@officessai.com">s.szarpak@officessai.com</a>
            </div>
            <ContactForm />
          </div>
        </section>
      </main>

      <footer>
        <div className="section-wrap footer-inner">
          <span>© {new Date().getFullYear()} OfficeSSAI</span>
          <span>Technologia ma pracować. Człowiek ma decydować.</span>
        </div>
      </footer>
    </>
  )
}

export default App
