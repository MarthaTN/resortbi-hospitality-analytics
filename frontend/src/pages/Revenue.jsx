
import { useMemo, useState } from "react";
import AnalyticsFilters from "../components/AnalyticsFilters";
import { defaultDateRange } from "../utils/dateRange";
import MetricCard from "../components/MetricCard";
import BarList from "../components/BarList";
import useAnalyticsData from "../hooks/useAnalyticsData";
import { buildQuery } from "../services/api";

const money = (value) => `N$ ${Number(value || 0).toLocaleString("en-NA", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

function Revenue() {
    const [filters, setFilters] = useState(defaultDateRange);
    const query = buildQuery(filters);
    const path = useMemo(() => `/analytics/revenue/${query}`, [query]);
    const comparisonPath = useMemo(() => `/analytics/revenue/comparison/${query}`, [query]);
    const { data: response, loading, error, reload } = useAnalyticsData(path);
    const { data: comparisonResponse, loading: comparisonLoading, error: comparisonError } = useAnalyticsData(comparisonPath);
    const data = response?.data;
    const comparison = comparisonResponse?.data;

    return (
        <section className="page-stack">
            <div className="page-heading"><div><p className="eyebrow">PERFORMANCE</p><h2>Revenue & reservation value</h2><p className="muted">Reservation amounts grouped by check-in date.</p></div><button className="button button-secondary" onClick={reload} type="button">Refresh</button></div>
            <AnalyticsFilters value={filters} onApply={setFilters} />
            {loading && <p className="state-message">Loading reservation values…</p>}
            {error && <div className="alert alert-error" role="alert">{error}</div>}
            {data && !loading && <>
                <div className="metrics-grid metrics-grid-small">
                    <MetricCard label="Total reservation value" value={money(data.total_revenue)} hint="Not verified cash collected" />
                    <MetricCard label="Reservations" value={data.reservation_count ?? 0} />
                    <MetricCard label="Change vs previous period" value={comparisonLoading ? "…" : comparison?.percentage_change == null ? "N/A" : `${Number(comparison.percentage_change) > 0 ? "+" : ""}${comparison.percentage_change}%`} hint={comparison?.percentage_change == null ? "No previous-period baseline" : `Difference: ${money(comparison.difference)}`} />
                </div>
                {comparisonError && <div className="alert alert-error" role="alert">{comparisonError}</div>}
                <article className="panel">
                    <div className="panel-heading"><div><h3>Reservation value by resort</h3><p className="muted">Select a resort above to narrow the results.</p></div></div>
                    <BarList items={data.revenue_by_resort || []} labelKey="resort_name" valueKey="total_revenue" formatValue={money} />
                </article>
                <p className="footnote">{data.metric_definition}</p>
            </>}
        </section>
    );
}

export default Revenue;
