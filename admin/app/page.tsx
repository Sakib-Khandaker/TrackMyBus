export default function Dashboard() {
  const cards = [
    ["Active buses", "0"],
    ["Active trips", "0"],
    ["Routes", "0"],
    ["Locations today", "0"],
  ];

  return (
    <main style={{ padding: 32 }}>
      <h1>LocateX Admin</h1>
      <p>Transportation operations dashboard</p>

      <section style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
        gap: 16,
        marginTop: 24
      }}>
        {cards.map(([label, value]) => (
          <article key={label} style={{
            border: "1px solid #ddd",
            borderRadius: 12,
            padding: 20
          }}>
            <div>{label}</div>
            <strong style={{ fontSize: 28 }}>{value}</strong>
          </article>
        ))}
      </section>
    </main>
  );
}
