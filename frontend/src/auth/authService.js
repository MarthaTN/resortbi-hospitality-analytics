
const API_URL = (
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api"
).replace(/\/$/, "");

async function readResponse(response, fallbackMessage) {
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(
            payload.detail || payload.error || fallbackMessage
        );
    }
    return payload;
}

export async function login(username, password) {
    const response = await fetch(`${API_URL}/auth/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ username, password }),
    });
    return readResponse(response, "Login failed. Check your username and password.");
}

export async function refreshAccessToken(refresh) {
    const response = await fetch(`${API_URL}/auth/token/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ refresh }),
    });
    return readResponse(response, "Your session has expired. Please log in again.");
}
