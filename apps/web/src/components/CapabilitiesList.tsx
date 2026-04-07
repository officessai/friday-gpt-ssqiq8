const capabilities = [
  'Validates ideas while still questioning them.',
  'Connects data points in a clear, practical way.',
  'Adapts tone and communication style to the person.',
  'Keeps context tidy for longer, more useful sessions.'
]

export function CapabilitiesList() {
  return (
    <section className="card">
      <h2>What Friday can do</h2>
      <ul>
        {capabilities.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  )
}
