
export default function BarList({ items = [], labelKey, valueKey, formatValue = (value) => value }) {
    const max = Math.max(...items.map((item) => Number(item[valueKey]) || 0), 1);
    if (!items.length) return <p className="muted">No records are available for this period.</p>;
    return (
        <div className="bar-list">
            {items.map((item, index) => {
                const value = Number(item[valueKey]) || 0;
                return (
                    <div className="bar-row" key={`${item[labelKey]}-${index}`}>
                        <div className="bar-meta"><span>{item[labelKey] || "Unspecified resort"}</span><strong>{formatValue(value)}</strong></div>
                        <div className="bar-track"><div className="bar-fill" style={{ width: `${Math.max(value > 0 ? 2 : 0, value / max * 100)}%` }} /></div>
                    </div>
                );
            })}
        </div>
    );
}
