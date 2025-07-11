import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // url pro api a v dev to presmeruju proxi
  const API_BASE = process.env.REACT_APP_API_URL;

  useEffect(() => {
    setLoading(true);
    setError(null);

    fetch(`${API_BASE}/rates?usedb=true`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => {
        // muzu dostat pole nebo objekt
        const list = Array.isArray(json) ? json : json.rates ?? [];
        setData(list);
      })
      .catch((err) => {
        console.error("Chyba při stahování dat:", err);
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, [API_BASE]);

  if (loading) {
    return <p className="p-4">Načítám data z lokálního BE…</p>;
  }
  if (error) {
    return (
      <p className="p-4 text-red-600">Chyba při načítání: {error}</p>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Levy */}
      <div className="w-1/3 bg-white p-4 border-r overflow-y-auto">
        <h2 className="text-xl font-bold mb-4">Seznam měn</h2>
        {data.length === 0 && <p>Žádná data.</p>}
        {data.map((item) => (
          <button
            key={item.shortName}
            className={`w-full text-left px-4 py-2 mb-2 rounded transition-all duration-150
              ${selected?.shortName === item.shortName
                ? "bg-blue-100 font-bold"
                : "bg-gray-50"}
              hover:bg-blue-50`}
            onClick={() => setSelected(item)}
          >
            <div className="text-lg">{item.shortName}</div>
            <div className="text-sm text-gray-500">
              {item.name} – {item.country}
            </div>
            <div className="text-xs text-gray-400">
              Platnost: {item.validFrom?.slice(0, 10)}
            </div>
          </button>
        ))}
      </div>

      {/* pravy */}
      <div className="flex-1 p-8">
        <div className="sticky top-0 bg-white rounded shadow p-6 z-10">
          {!selected ? (
            <div className="text-gray-400 text-lg">Vyber měnu vlevo…</div>
          ) : (
            <>
              <h2 className="text-2xl font-bold mb-4">
                {selected.shortName} – {selected.name}
              </h2>
              {[
                ["Země", selected.country],
                ["Platnost od", selected.validFrom?.slice(0, 10)],
                ["Nákup", selected.valBuy],
                ["Prodej", selected.valSell],
                ["Střed", selected.valMid],
                ["Objem", selected.amount],
                ["currBuy", selected.currBuy],
                ["currSell", selected.currSell],
                ["currMid", selected.currMid],
                ["move", selected.move],
                ["version", selected.version],
                ["cnbMid", selected.cnbMid],
                ["ecbMid", selected.ecbMid],
              ].map(([label, val]) => (
                <div key={label} className="mb-2">
                  {label}: <b>{val ?? "–"}</b>
                </div>
              ))}
            </>
          )}
        </div>
      </div>
  
    </div>
  );
}

export default App;
