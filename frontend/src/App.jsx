import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";

import Dashboard from "./pages/Dashboard";
import Revenue from "./pages/Revenue";
import Occupancy from "./pages/Occupancy";
import Visitors from "./pages/Visitors";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";
import Login from "./pages/Login";
import ProtectedRoute from "./auth/ProtectedRoute";

function App() {
    return (
        <BrowserRouter>
    <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />}>
            <Route element={<DashboardLayout />}>
                <Route
                    path="/dashboard"
                    element={<Dashboard />}
                />

                <Route
                    path="/revenue"
                    element={<Revenue />}
                />

                <Route
                    path="/occupancy"
                    element={<Occupancy />}
                />

                <Route
                    path="/visitors"
                    element={<Visitors />}
                />

                <Route
                    path="/reports"
                    element={<Reports />}
                />

                <Route
                    path="/settings"
                    element={<Settings />}
                />
            </Route>
        </Route>

        <Route
            path="*"
            element={<Navigate to="/dashboard" replace />}
        />
    </Routes>
</BrowserRouter>
    );
}

export default App;