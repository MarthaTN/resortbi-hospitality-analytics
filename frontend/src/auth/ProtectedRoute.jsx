
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../auth/useAuth";


function ProtectedRoute() {
    const { isAuthenticated, profileLoading, groups, logoutUser } = useAuth();
    const location = useLocation();

    if (!isAuthenticated) {
        return <Navigate to="/login" replace state={{ from: location }} />;
    }

    if (profileLoading) {
        return <main className="login-screen"><p className="state-message">Restoring your session…</p></main>;
    }

    if (!groups.length) {
        return (
            <main className="login-screen">
                <section className="login-card">
                    <p className="eyebrow">ACCESS NOT CONFIGURED</p>
                    <h1>No portal role assigned</h1>
                    <p className="muted">Your account is signed in, but it is not assigned to a recognized Django Group. Contact the system administrator.</p>
                    <button className="button button-primary" type="button" onClick={logoutUser}>Log out</button>
                </section>
            </main>
        );
    }

    const managementOnlyPaths = ["/dashboard", "/revenue", "/reports"];
    const isManagement = groups.some((group) => ["Administrator", "Executive", "Manager"].includes(group));
    if (!isManagement && managementOnlyPaths.includes(location.pathname)) {
        return <Navigate to="/occupancy" replace />;
    }

    return <Outlet />;
}

export default ProtectedRoute;
