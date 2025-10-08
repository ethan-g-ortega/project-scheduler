import { useState } from "react";

type Weather = {
  city: string; tempC: number; tempF: number; condition: string;
  sourceTs: string; source: string; cached: boolean;
};


export default function Weather() {
    const [city, setCity] = useState("Riverside,US");
    const [data, setData] = useState<Weather | null>(null);
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState<string | null>(null);

    async function fetchWeather(){
        setLoading(true);
        setErr(null);
        const res = await fetch(`/api/weather?city=${encodeURI(city)}&units=metric`)
        if (!res.ok) { 
            setErr(`Error ${res.status}`);
            setLoading(false);
        }
        setData(await res.json());
        setLoading(false);
    }

    return (
        <div>
            <input value={city} onChange={e => setCity(e.target.value)} />
            <button onClick={fetchWeather} disabled={loading}>Get Weather</button>
            {loading && <p>Loading...</p>}
            {err && <p style={{color: 'red'}}>{err}</p>}
            {data && (
                <div>
                    <h3>{data.city}</h3>
                    <p>{data.condition}</p>
                    <p>{data.tempC}°C / {data.tempF}°F</p>
                    <small>{data.cached ? "cached" : "live"} · {data.sourceTs}</small>
                </div>
            )}
        </div>
    )
}