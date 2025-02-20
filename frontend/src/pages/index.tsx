import { useState } from "react";

export default function Home() {
  const [city, setCity] = useState<string>("");
  const [days, setDays] = useState<number>(7);
  const [averageTemp, setAverageTemp] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const fetchAverageTemperature = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/weather/average?city=${city}&days=${days}`
      );
      if (!response.ok) throw new Error("Failed to fetch data");

      const data: { average_temperature: number } = await response.json();
      setAverageTemp(data.average_temperature);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const isButtonDisabled = loading || city.trim() === "" || days <= 0;

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 p-6">
      <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-md">
        <h1 className="mb-4 text-center text-xl font-semibold text-gray-700">
          Weather Average Temperature
        </h1>
        <div className="space-y-4">
          <div>
            <label htmlFor="city" className="mb-1 block text-sm font-medium text-gray-700">
              City
            </label>
            <input
              id="city"
              type="text"
              placeholder="Enter city"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="w-full rounded border border-gray-300 p-2 text-gray-700 focus:border-blue-500 focus:ring focus:ring-blue-300"
            />
          </div>

          <div>
            <label htmlFor="days" className="mb-1 block text-sm font-medium text-gray-700">
              Number of Days
            </label>
            <input
              id="days"
              type="number"
              placeholder="Enter days"
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="w-full rounded border border-gray-300 p-2 text-gray-700 focus:border-blue-500 focus:ring focus:ring-blue-300"
            />
          </div>

          <button
            onClick={fetchAverageTemperature}
            disabled={isButtonDisabled}
            className={`w-full rounded p-2 text-white transition ${
              isButtonDisabled
                ? "cursor-not-allowed bg-gray-400"
                : "bg-blue-500 hover:bg-blue-600"
            }`}
          >
            {loading ? "Loading..." : "Get Average Temperature"}
          </button>

          {error && <p className="text-sm text-red-500">{error}</p>}

          {averageTemp !== null && (
            <p className="text-center text-lg font-medium text-gray-700">
              Average Temperature: <span className="text-blue-500">{averageTemp}°C</span>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
