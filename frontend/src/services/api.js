
import { refreshAccessToken } from "../auth/authService";

const API_URL = (
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api"
).replace(/\/$/, "");

function endSession() {
    sessionStorage.removeItem("access");
    sessionStorage.removeItem("refresh");
    window.dispatchEvent(new Event("auth:logout"));
}

export async function apiFetch(path, options = {}) {
    const makeRequest = (token) => fetch(`${API_URL}${path}`, {
        ...options,
        headers: {
            Accept: "application/json",
            ...(options.body ? { "Content-Type": "application/json" } : {}),
            ...options.headers,
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
    });

    const access = sessionStorage.getItem("access");
    let response = await makeRequest(access);
    if (response.status !== 401) return response;

    const refresh = sessionStorage.getItem("refresh");
    if (!refresh) {
        endSession();
        throw new Error("Your session has expired. Please log in again.");
    }

    let tokens;
    try {
        tokens = await refreshAccessToken(refresh);
    } catch (error) {
        endSession();
        throw error;
    }

    if (tokens.access) sessionStorage.setItem("access", tokens.access);
    if (tokens.refresh) sessionStorage.setItem("refresh", tokens.refresh);

    response = await makeRequest(tokens.access);
    if (response.status === 401) {
        endSession();
        throw new Error("Your session has expired. Please log in again.");
    }
    return response;
}

export async function getJson(path) {
    const response = await apiFetch(path);
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(payload.error || payload.detail || "The request could not be completed.");
    }
    return payload;
}

export function buildQuery({ startDate, endDate, resortName }) {
    const params = new URLSearchParams();
    if (startDate) params.set("start_date", startDate);
    if (endDate) params.set("end_date", endDate);
    if (resortName?.trim()) params.set("resort_name", resortName.trim());
    const query = params.toString();
    return query ? `?${query}` : "";
}
