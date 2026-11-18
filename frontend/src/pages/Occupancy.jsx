
import { useMemo, useState } from "react";
import AnalyticsFilters from "../components/AnalyticsFilters";
import { defaultDateRange } from "../utils/dateRange";
import MetricCard from "../components/MetricCard";
import useAnalyticsData from "../hooks/useAnalyticsData";
import { buildQuery } from "../services/api";

function Occupancy() {
    const [filters, setFilters] = useState(defaultDateRange);
    const path = useMemo(() => `/analytics/occupancy/${buildQuery(filters)}`, [filters]);
    const { data: response, loading, error, reload } = useAnalyticsData(path);
    const data = response?.data;

    return (
        <section className="page-stack">
            <div className="page-heading"><div><p className="eyebrow">ROOM PERFORMANCE</p><h2>Occupancy</h2><p className="muted">Occupancy is calculated using occupied room-nights.</p></div><button className="button button-secondary" onClick={reload} type="button">Refresh</button></div>
            <AnalyticsFilters value={filters} onApply={setFilters} />
            {loading && <p className="state-message">Loading occupancy…</p>}
            {error && <div className="alert alert-error" role="alert">{error}</div>}
            {data && !loading && <>
                <div className="metrics-grid">
                    <MetricCard label="Occupancy rate" value={`${data.occupancy_rate}%`} hint="Occupied room-nights ÷ available room-nights" />
                    <MetricCard label="Active rooms" value={data.total_rooms} hint="Assumed available for the selected period" />
                    <MetricCard label="Occupied room-nights" value={data.occupied_room_nights} />
                    <MetricCard label="Available room-nights" value={data.available_room_nights} />
                </div>
                <article className="panel">
                    <div className="panel-heading"><div><h3>Occupancy rate</h3><p className="muted">{data.period_nights} reporting night(s) in the selected range</p></div><strong>{data.occupancy_rate}%</strong></div>
                    <div className="large-progress"><div style={{ width: `${Math.min(Number(data.occupancy_rate) || 0, 100)}%` }} /></div>
                    <p className="footnote">{data.metric_definition} If the rate exceeds 100%, review overlapping reservations or room inventory rather than hiding the data-quality issue.</p>
                </article>
            </>}
        </section>
    );
}

export default Occupancy;
