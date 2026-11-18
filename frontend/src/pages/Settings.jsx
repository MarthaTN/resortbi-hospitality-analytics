
import { useAuth } from "../auth/useAuth";

function Settings() {
    const { isAuthenticated } = useAuth();
    const apiBase = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

    return (
        <section className="page-stack">
            <div className="page-heading"><div><p className="eyebrow">APPLICATION</p><h2>Settings & system information</h2><p className="muted">Configuration information for this local project build.</p></div></div>
            <article className="panel settings-panel">
                <h3>Session</h3>
                <div className="setting-row"><span>Authentication</span><strong className={isAuthenticated ? "status-good" : "status-bad"}>{isAuthenticated ? "Signed in" : "Signed out"}</strong></div>
                <p className="muted">User access is determined by Django Groups on the backend. This screen does not change user roles.</p>
                <h3>API connection</h3>
                <div className="setting-row"><span>Configured API base URL</span><code>{apiBase}</code></div>
                <p className="muted">Set VITE_API_BASE_URL in the frontend environment for a different backend address.</p>
                <h3>Data definitions</h3>
                <ul className="definition-list">
                    <li><strong>Reservation value:</strong> sum of reservation amounts; not verified cash collected.</li>
                    <li><strong>Occupancy:</strong> occupied room-nights divided by available room-nights.</li>
                    <li><strong>Visitor overview:</strong> reservation records grouped by country, not unique guest headcount.</li>
                </ul>
            </article>
        </section>
    );
}

export default Settings;
