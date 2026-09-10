function AgentScorecard({ result }) {
  const agentColors = {
    executive_summary: "#2196F3",
    key_insights: "#4CAF50",
    citations: "#FF9800",
    document_validation: "#9C27B0",
    highlights: "#F44336",
    response_composer: "#1a1a2e"
  };

  const agentIcons = {
    executive_summary: "📝",
    key_insights: "💡",
    citations: "🔖",
    document_validation: "✅",
    highlights: "✨",
    response_composer: "🔍"
  };

  return (
    <div>
      <div style={{ background: "#1a1a2e", color: "white", padding: "1rem",
        borderRadius: "10px", marginBottom: "1.5rem" }}>
        <p style={{ margin: 0 }}>Report ID: <strong>{result.report_id}</strong></p>
        <p style={{ margin: 0 }}>Chunks analyzed: <strong>{result.total_chunks}</strong></p>
        <p style={{ margin: 0 }}>Project type: <strong>{result.project_type}</strong> | City tier: <strong>{result.city_tier}</strong></p>
      </div>

      {Object.entries(result.agents).map(([agent, output]) => (
        <div key={agent} style={{ marginBottom: "1.5rem", border: `2px solid ${agentColors[agent]}`,
          borderRadius: "10px", overflow: "hidden" }}>
          <div style={{ background: agentColors[agent], color: "white",
            padding: "0.75rem 1rem", fontWeight: "bold", fontSize: "1rem" }}>
            {agentIcons[agent]} {agent.charAt(0).toUpperCase() + agent.slice(1)} Agent
          </div>
          <div style={{ padding: "1rem", whiteSpace: "pre-wrap", fontSize: "0.9rem", lineHeight: "1.6" }}>
            {typeof output === "object" ? JSON.stringify(output, null, 2) : output}
          </div>
        </div>
      ))}
    </div>
  );
}

export default AgentScorecard;