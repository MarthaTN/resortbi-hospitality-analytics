
import { useCallback, useEffect, useMemo, useState } from "react";
import { AuthContext } from "./authContextStore";
import { login } from "./authService";
import { getJson } from "../services/api";



export function AuthProvider({ children }) {
    const [accessToken, setAccessToken] = useState(() => sessionStorage.getItem("access"));
    const [refreshToken, setRefreshToken] = useState(() => sessionStorage.getItem("refresh"));
    const [user, setUser] = useState(null);
    const [profileLoading, setProfileLoading] = useState(() => Boolean(sessionStorage.getItem("access")));

    const logoutUser = useCallback(() => {
        sessionStorage.removeItem("access");
        sessionStorage.removeItem("refresh");
        setAccessToken(null);
        setRefreshToken(null);
        setUser(null);
        setProfileLoading(false);
    }, []);

    useEffect(() => {
        window.addEventListener("auth:logout", logoutUser);
        return () => window.removeEventListener("auth:logout", logoutUser);
    }, [logoutUser]);

    // Restore the current user's groups when a saved session is loaded.
    useEffect(() => {
        let active = true;
        if (!sessionStorage.getItem("access")) {
            return () => { active = false; };
        }

        // eslint-disable-next-line react-hooks/set-state-in-effect
        setProfileLoading(true);
        getJson("/auth/me/")
            .then((profile) => {
                if (active) setUser(profile);
            })
            .catch(() => {
                if (active) setUser(null);
            })
            .finally(() => {
                if (active) setProfileLoading(false);
            });

        return () => { active = false; };
    }, []);

    const loginUser = useCallback(async (username, password) => {
        const tokens = await login(username, password);
        if (!tokens.access || !tokens.refresh) {
            throw new Error("The server did not return the expected login tokens.");
        }

        sessionStorage.setItem("access", tokens.access);
        sessionStorage.setItem("refresh", tokens.refresh);
        setAccessToken(tokens.access);
        setRefreshToken(tokens.refresh);
        setProfileLoading(true);

        try {
            const profile = await getJson("/auth/me/");
            setUser(profile);
            setProfileLoading(false);
            return profile;
        } catch (error) {
            logoutUser();
            throw error;
        }
    }, [logoutUser]);

    const groups = useMemo(() => user?.groups ?? [], [user?.groups]);
    const isManagement = groups.some((group) => ["Administrator", "Executive", "Manager"].includes(group));
    const value = useMemo(() => ({
        accessToken,
        refreshToken,
        user,
        groups,
        isManagement,
        profileLoading,
        isAuthenticated: Boolean(accessToken && refreshToken),
        loginUser,
        logoutUser,
    }), [accessToken, refreshToken, user, groups, isManagement, profileLoading, loginUser, logoutUser]);

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}


