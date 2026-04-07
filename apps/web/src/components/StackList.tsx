const stack = ['OpenAI Responses API', 'NVIDIA NIM', 'Google AI', 'GitHub Actions', 'Codex workflows']

export function StackList() {
  return (
    <section className="card">
      <h2>Current stack</h2>
      <div className="pill-row">
        {stack.map((item) => (
          <span className="pill" key={item}>
            {item}
          </span>
        ))}
      </div>
    </section>
  )
}
