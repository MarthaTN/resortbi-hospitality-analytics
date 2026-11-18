
import { useMemo, useState } from "react";
import AnalyticsFilters from "../components/AnalyticsFilters";
import { defaultDateRange } from "../utils/dateRange";
import MetricCard from "../components/MetricCard";
import useAnalyticsData from "../hooks/useAnalyticsData";
import { buildQuery } from "../services/api";

function Visitors() {
    const [filters, setFilters] = useState(defaultDateRange);
    const path = useMemo(() => `/analytics/visitors/${buildQuery(filters)}`, [filters]);
    const { data: response, loading, error, reload } = useAnalyticsData(path);
    const data = response?.data;

    return (
        <section className="page-stack">
            <div className="page-heading"><div><p className="eyebrow">GUEST MIX</p><h2>Visitor overview</h2><p className="muted">Country breakdown based on reservation records.</p></div><button className="button button-secondary" onClick={reload} type="button">Refresh</button></div>
            <AnalyticsFilters value={filters} onApply={setFilters} />
            {loading && <p className="state-message">Loading visitor data…</p>}
            {error && <div className="alert alert-error" role="alert">{error}</div>}
            {data && !loading && <>
                <div className="metrics-grid">
                    <MetricCard label="Reservation records" value={data.total_reservations} hint="Not unique visitors or people count" />
                    <MetricCard label="Namibian reservations" value={data.namibian_reservations} />
                    <MetricCard label="Foreign reservations" value={data.foreign_reservations} />
                    <MetricCard label="Country not recorded" value={data.unknown_country_reservations} />
                </div>
                <article className="panel">
                    <div className="panel-heading"><div><h3>Reservation country mix</h3><p className="muted">Share of records with country information</p></div></div>
                    <div className="country-bar">
                        <div className="country-namibian" style={{ width: `${data.total_reservations ? data.namibian_reservations / data.total_reservations * 100 : 0}%` }} />
                        <div className="country-foreign" style={{ width: `${data.total_reservations ? data.foreign_reservations / data.total_reservations * 100 : 0}%` }} />
                        <div className="country-unknown" style={{ width: `${data.total_reservations ? data.unknown_country_reservations / data.total_reservations * 100 : 0}%` }} />
                    </div>
                    <p className="footnote">{data.metric_definition}</p>
                </article>
            </>}
        </section>
    );
}

export default Visitors;
