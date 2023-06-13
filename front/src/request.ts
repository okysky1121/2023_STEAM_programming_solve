import qs from "query-string";

type Location = {};
type LocationResponse = { result: Location[] };

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const request = (path: string, query: object) => {
  return fetch(`${BASE_URL}/api${path}?${qs.stringify(query)}`);
};

const requestSearch = async (q: string) => {
  const res = await request("/search", { q });
  const results: LocationResponse = await res.json();

  return results.result;
};

const requestNearby = async (lat: number, lon: number) => {
  const res = await request("/nearby", { lat, lon });
  const results: LocationResponse = await res.json();

  return results.result;
};

export { requestSearch, requestNearby };
