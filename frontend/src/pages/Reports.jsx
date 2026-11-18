
import { useMemo, useState } from "react";
import AnalyticsFilters from "../components/AnalyticsFilters";
import { defaultDateRange } from "../utils/dateRange";
import useAnalyticsData from "../hooks/useAnalyticsData";
import { buildQuery } from "../services/api";

function exportCsv(rows) {
    const header = ["Resort", "Reservation value (NAD)", "Reservation count"];
    const values = rows.map((row) => [row.resort_name, row.total_revenue, row.reservation_count]);
    const escape = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
    const csv = [header, ...values].map((row) => row.map(escape).join(",")).join("\r\n");
    const blob = new Blob(["\uFEFF", csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "nwr-reservation-value-report.csv";
    link.click();
    URL.revokeObjectURL(url);
}

function Reports() {
    const [filters, setFilters] = useState(defaultDateRange);
    const path = useMemo(() => `/analytics/revenue/${buildQuery(filters)}`, [filters]);
    const { data: response, loading, error, reload } = useAnalyticsData(path);
    const rows = response?.data?.revenue_by_resort || [];

    return (
        <section className="page-stack">
            <div className="page-heading"><div><p className="eyebrow">DATA EXPORT</p><h2>Reports</h2><p className="muted">Generate a CSV summary of reservation value by resort.</p></div><button className="button button-secondary" onClick={reload} type="button">Refresh</button></div>
            <AnalyticsFilters value={filters} onApply={setFilters} />
            {loading && <p className="state-message">Preparing report data…</p>}
            {error && <div className="alert alert-error" role="alert">{error}</div>}
            {!loading && !error && response && <>
                <div className="panel-heading report-actions"><div><h3>Reservation value report</h3><p className="muted">{rows.length} resort row(s)</p></div><button className="button button-primary" type="button" disabled={!rows.length} onClick={() => exportCsv(rows)}>Export CSV</button></div>
                <div className="table-wrap"><table><thead><tr><th>Resort</th><th>Reservation value (NAD)</th><th>Reservations</th></tr></thead><tbody>
                    {rows.length ? rows.map((row) => <tr key={row.resort_name}><td>{row.resort_name}</td><td>{Number(row.total_revenue).toLocaleString("en-NA", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td><td>{row.reservation_count}</td></tr>) : <tr><td colSpan="3">No records found for this period.</td></tr>}
                </tbody></table></div>
                <p className="footnote">This export uses reservation amounts grouped by check-in date. It is not a financial statement and does not verify payments received.</p>
            </>}
        </section>
    );
}

export default Reports;
