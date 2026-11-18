
import { useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const { loginUser, isAuthenticated, profileLoading } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    if (isAuthenticated && !profileLoading) return <Navigate to="/dashboard" replace />;

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");
        setLoading(true);
        try {
            await loginUser(username.trim(), password);
            navigate(location.state?.from?.pathname || "/dashboard", { replace: true });
        } catch (loginError) {
            setError(loginError.message || "Login failed. Please try again.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="login-screen">
            <section className="login-card">
                <div className="login-brand"><div className="login-logo">R</div><div><strong>ResortBI</strong><span>HOSPITALITY INTELLIGENCE</span></div></div>
                <p className="eyebrow">MANAGEMENT PORTAL</p>
                <h1>Welcome back</h1>
                <p className="muted">Sign in with your portal account to continue.</p>
                <form className="login-form" onSubmit={handleSubmit}>
                    <label htmlFor="username">Username</label>
                    <input id="username" type="text" value={username} onChange={(event) => setUsername(event.target.value)} autoComplete="username" required />
                    <label htmlFor="password">Password</label>
                    <input id="password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" required />
                    {error && <div className="alert alert-error" role="alert">{error}</div>}
                    <button className="button button-primary login-submit" type="submit" disabled={loading}>{loading ? "Signing in…" : "Sign in"}</button>
                </form>
                <p className="login-footnote">Access is managed by the system administrator.</p>
            </section>
        </main>
    );
}

export default Login;
