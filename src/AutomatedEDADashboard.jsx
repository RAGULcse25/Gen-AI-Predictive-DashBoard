import React from 'react';

const apiData = {
  "kpi_cards": {
    "total_records": 1482000,
    "total_attributes": 12,
    "target_sum": 543200000,
    "target_avg": 366.50
  },
  "trend_chart": [
    { "date": "1 Apr", "value": 4.2 },
    { "date": "8 Apr", "value": 5.1 },
    { "date": "15 Apr", "value": 4.8 },
    { "date": "22 Apr", "value": 5.8 },
    { "date": "29 Apr", "value": 6.4 },
    { "date": "6 May", "value": 7.2 },
    { "date": "13 May", "value": 6.9 },
    { "date": "20 May", "value": 8.4 },
    { "date": "27 May", "value": 7.9 }
  ],
  "category_distribution": {
    "feature_name": "Category",
    "data": [
      { "name": "Fruits & Vegetables", "percentage": 29.8, "color": "bg-emerald-500" },
      { "name": "Dairy & Breakfast", "percentage": 19.6, "color": "bg-amber-500" },
      { "name": "Snacks & Branded Foods", "percentage": 16.2, "color": "bg-orange-500" },
      { "name": "Beverages", "percentage": 12.8, "color": "bg-indigo-500" },
      { "name": "Personal Care", "percentage": 11.1, "color": "bg-pink-500" }
    ]
  },
  "top_rankings": {
    "feature_name": "City",
    "data": [
      { "name": "Mumbai", "value": 8.21 },
      { "name": "Delhi", "value": 6.72 },
      { "name": "Bengaluru", "value": 5.89 },
      { "name": "Pune", "value": 4.12 },
      { "name": "Hyderabad", "value": 3.56 },
      { "name": "Kolkata", "value": 2.94 }
    ]
  },
  "genai_insights": [
    "Sales are up by 21.6% compared to the previous timeframe evaluation.",
    "Fruits & Vegetables represents your single highest-performing target volume cluster.",
    "Geographically, Mumbai and Delhi drive over 40% of overall predictive weights."
  ]
};

export default function AutomatedEDADashboard() {
  const { kpi_cards, trend_chart, category_distribution, top_rankings, genai_insights } = apiData;

  return (
    <div className="flex h-screen w-full bg-[#0b0f17] text-white font-sans overflow-hidden">
      <aside className="w-64 bg-[#06080c] border-r border-[#1a2233] flex flex-col justify-between p-4 hidden md:flex">
        <div>
          <div className="flex items-center gap-2 mb-8 px-2">
            <span className="text-xl font-black text-emerald-400 tracking-wide">blinkit</span>
            <span className="text-xs text-gray-500 border border-gray-800 px-1 rounded">AI-EDA</span>
          </div>
          <nav className="space-y-1">
            <button className="w-full flex items-center gap-3 bg-emerald-950/40 text-emerald-400 font-medium px-3 py-2.5 rounded-lg text-sm border-l-4 border-emerald-500">
              <span>📊</span> Overview Dashboard
            </button>
            <button className="w-full flex items-center gap-3 text-gray-400 hover:bg-[#111827] hover:text-white px-3 py-2.5 rounded-lg text-sm transition">
              <span>📈</span> Predictive Modeling
            </button>
            <button className="w-full flex items-center gap-3 text-gray-400 hover:bg-[#111827] hover:text-white px-3 py-2.5 rounded-lg text-sm transition">
              <span>🤖</span> GenAI Copilot
            </button>
          </nav>
        </div>
        <div className="bg-[#111827] p-3 rounded-lg text-xs text-gray-400 border border-gray-800">
          <p>Data Refresh Engine Auto-Linked</p>
          <p className="text-gray-500 mt-1">Status: Stable (200 OK)</p>
        </div>
      </aside>

      <main className="flex-1 flex flex-col overflow-y-auto p-6 space-y-6">
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-[#1a2233]">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">AI-Powered Predictive Engine Dashboard</h1>
            <p className="text-xs text-gray-400 mt-0.5">Automated exploration, parsing, and context mapping</p>
          </div>
          <div className="flex flex-wrap gap-2 items-center text-xs">
            <div className="bg-[#161b26] border border-[#222b3c] px-3 py-2 rounded-lg text-gray-300">
              📅 Range: <span className="text-white font-medium">Auto-Detected Lifecycle</span>
            </div>
          </div>
        </header>

        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-[#161b26] border border-[#222b3c] p-4 rounded-xl relative overflow-hidden shadow-xl">
            <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Target Cumulative Weight</p>
            <h3 className="text-2xl font-bold mt-2">₹ {(kpi_cards.target_sum / 10000000).toFixed(2)} Cr</h3>
            <div className="text-xs text-emerald-400 flex items-center gap-1 mt-2 font-medium">
              <span>▲ +21.6%</span> <span className="text-gray-500">vs training baseline</span>
            </div>
            <div className="absolute right-3 top-3 text-xl opacity-20">💰</div>
          </div>

          <div className="bg-[#161b26] border border-[#222b3c] p-4 rounded-xl relative overflow-hidden shadow-xl">
            <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Total Analyzed Records</p>
            <h3 className="text-2xl font-bold mt-2">{(kpi_cards.total_records / 100000).toFixed(2)} Lakh</h3>
            <div className="text-xs text-emerald-400 flex items-center gap-1 mt-2 font-medium">
              <span>▲ +18.7%</span> <span className="text-gray-500">volume scale</span>
            </div>
            <div className="absolute right-3 top-3 text-xl opacity-20">📥</div>
          </div>

          <div className="bg-[#161b26] border border-[#222b3c] p-4 rounded-xl relative overflow-hidden shadow-xl">
            <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Target Evaluation Mean</p>
            <h3 className="text-2xl font-bold mt-2">{kpi_cards.target_avg.toFixed(2)}</h3>
            <div className="text-xs text-amber-400 flex items-center gap-1 mt-2 font-medium">
              <span>⚖ Mean Density</span> <span className="text-gray-500">per sample instance</span>
            </div>
            <div className="absolute right-3 top-3 text-xl opacity-20">🧮</div>
          </div>

          <div className="bg-[#161b26] border border-[#222b3c] p-4 rounded-xl relative overflow-hidden shadow-xl">
            <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Validated Features (Columns)</p>
            <h3 className="text-2xl font-bold mt-2">{kpi_cards.total_attributes} Columns</h3>
            <div className="text-xs text-blue-400 flex items-center gap-1 mt-2 font-medium">
              <span>✓ 100% Parsing</span> <span className="text-gray-500">integrity confirmed</span>
            </div>
            <div className="absolute right-3 top-3 text-xl opacity-20">🧱</div>
          </div>
        </section>

        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-[#161b26] border border-[#222b3c] p-5 rounded-xl lg:col-span-2 shadow-xl flex flex-col justify-between">
            <div className="flex justify-between items-center mb-4">
              <h4 className="text-sm font-semibold tracking-wide text-gray-300">Generated Sequence Over Time</h4>
              <span className="text-xs text-gray-400 bg-[#0b0f17] px-2 py-1 rounded border border-gray-800">Interval: Aggregated</span>
            </div>
            <div className="w-full h-48 bg-[#0b0f17]/50 rounded-lg border border-[#222b3c] p-2 relative flex items-end">
              <svg className="w-full h-full stroke-emerald-400 fill-none" viewBox="0 0 900 200">
                <path
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M 10 160 Q 110 130 220 145 T 440 90 T 660 110 T 890 30"
                />
              </svg>
              <div className="absolute bottom-1 left-0 right-0 flex justify-between px-4 text-[10px] text-gray-500">
                {trend_chart.map((pt, index) => <span key={index}>{pt.date}</span>)}
              </div>
            </div>
          </div>

          <div className="bg-[#161b26] border border-[#222b3c] p-5 rounded-xl shadow-xl flex flex-col justify-between">
            <h4 className="text-sm font-semibold tracking-wide text-gray-300 mb-3">Top Shares by {category_distribution.feature_name}</h4>
            <div className="flex flex-col space-y-2 flex-1 justify-center">
              {category_distribution.data.map((cat, index) => (
                <div key={index} className="text-xs">
                  <div className="flex justify-between text-gray-400 mb-1">
                    <span className="flex items-center gap-2">
                      <span className={`w-2.5 h-2.5 rounded-full ${cat.color} block`}></span>
                      {cat.name}
                    </span>
                    <span className="text-white font-mono">{cat.percentage}%</span>
                  </div>
                  <div className="w-full bg-[#0b0f17] h-1.5 rounded-full overflow-hidden">
                    <div className={`h-full ${cat.color}`} style={{ width: `${cat.percentage}%` }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="bg-[#161b26] border border-[#222b3c] p-5 rounded-xl shadow-xl">
          <h4 className="text-sm font-semibold tracking-wide text-gray-300 mb-4">Volume Performance Scaling by {top_rankings.feature_name}</h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {top_rankings.data.map((rank, index) => (
              <div key={index} className="bg-[#0b0f17]/60 border border-[#222b3c]/60 p-3 rounded-lg flex items-center justify-between">
                <div>
                  <span className="text-xs text-gray-500 font-mono mr-2">#{index + 1}</span>
                  <span className="text-sm font-medium text-gray-200">{rank.name}</span>
                </div>
                <div className="text-right">
                  <span className="text-sm font-bold text-emerald-400 font-mono">₹{rank.value} Cr</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        <footer className="bg-[#111c15] border border-emerald-900/60 rounded-xl p-4 shadow-2xl">
          <div className="flex items-center gap-2 border-b border-emerald-900/40 pb-2 mb-3">
            <span className="text-lg">✨</span>
            <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400">Automated Generative AI Insight Stream</h4>
          </div>
          <ul className="space-y-2 text-sm text-emerald-200/90 pl-1">
            {genai_insights.map((insight, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-emerald-500 select-none mt-0.5">•</span>
                <span>{insight}</span>
              </li>
            ))}
          </ul>
        </footer>
      </main>
    </div>
  );
}
