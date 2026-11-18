
import { useEffect, useState } from "react";
import { getJson } from "../services/api";

export default function useAnalyticsData(path) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [reloadKey, setReloadKey] = useState(0);

    useEffect(() => {
        let active = true;
        // A new request must show its loading state immediately.
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setLoading(true);
       
        setError("");
        getJson(path)
            .then((result) => {
                if (active) setData(result);
            })
            .catch((requestError) => {
                if (active) setError(requestError.message || "Unable to load data.");
            })
            .finally(() => {
                if (active) setLoading(false);
            });
        return () => { active = false; };
    }, [path, reloadKey]);

    return { data, loading, error, reload: () => setReloadKey((value) => value + 1) };
}
