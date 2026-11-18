
import { useMemo, useState } from "react";
import AnalyticsFilters from "../components/AnalyticsFilters";
import { defaultDateRange } from "../utils/dateRange";
import MetricCard from "../components/MetricCard";
import BarList from "../components/BarList";
import useAnalyticsData from "../hooks/useAnalyticsData";
import { buildQuery } from "../services/api";

const money = (value) => `N$ ${Number(value || 0).toLocaleString("en-NA", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

function Dashboard() {
    const [filters, setFilters] = useState(defaultDateRange);
    const path = useMemo(() => `/analytics/dashboard/${buildQuery(filters)}`, [filters]);
    const { data: response, loading, error, reload } = useAnalyticsData(path);
    const data = response?.data;

    return (
        <section className="page-stack">
            <div className="page-heading">
                <div><p className="eyebrow">OVERVIEW</p><h2>Management dashboard</h2><p className="muted">A summary of reservation activity for the selected period.</p></div>
                <button className="button button-secondary" onClick={reload} type="button">Refresh</button>
            </div>
            <AnalyticsFilters value={filters} onApply={setFilters} />
            {loading && <p className="state-message">Loading dashboard data…</p>}
            {error && <div className="alert alert-error" role="alert">{error}</div>}
            {data && !loading && (
                <>
                    {data.revenue_alert && <div className="alert alert-warning" role="status"><strong>Revenue alert:</strong> {data.revenue_alert.message}</div>}
                    <div className="metrics-grid">
                        <MetricCard label="Reservation value" value={money(data.revenue?.total_revenue)} hint="Reservation amounts, not verified cash collected" />
                        <MetricCard label="Reservations" value={data.revenue?.reservation_count ?? 0} hint="Counted reservations in the period" />
                        <MetricCard label="Occupancy rate" value={`${data.occupancy?.occupancy_rate ?? 0}%`} hint={`${data.occupancy?.occupied_room_nights ?? 0} occupied room-nights`} />
                        <MetricCard label="Reservation records" value={data.visitors?.total_reservations ?? 0} hint="Not a unique guest headcount" />
                    </div>
                    <div className="content-grid">
                        <article className="panel">
                            <div className="panel-heading"><div><h3>Reservation value by resort</h3><p className="muted">Grouped by reservation check-in date</p></div></div>
                            <BarList items={data.revenue?.revenue_by_resort || []} labelKey="resort_name" valueKey="total_revenue" formatValue={money} />
                        </article>
                        <article className="panel">
                            <div className="panel-heading"><div><h3>Country breakdown</h3><p className="muted">Based on reservation records</p></div></div>
                            <div className="breakdown-list">
                                <div><span>Namibia</span><strong>{data.visitors?.namibian_reservations ?? 0}</strong></div>
                                <div><span>Other countries</span><strong>{data.visitors?.foreign_reservations ?? 0}</strong></div>
                                <div><span>Country not recorded</span><strong>{data.visitors?.unknown_country_reservations ?? 0}</strong></div>
                            </div>
                        </article>
                    </div>
                    <p className="footnote">Metrics depend on the quality and completeness of imported reservation records. Reservation value is not the same as verified payments received.</p>
                </>
            )}
        </section>
    );
}

export default Dashboard;
