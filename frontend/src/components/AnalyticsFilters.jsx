
import { useState } from "react";


export default function AnalyticsFilters({ value, onApply }) {
    const [draft, setDraft] = useState(value);
    function update(field, nextValue) {
        setDraft((current) => ({ ...current, [field]: nextValue }));
    }
    function submit(event) {
        event.preventDefault();
        if (draft.startDate && draft.endDate && draft.startDate > draft.endDate) return;
        onApply(draft);
    }

    return (
        <form className="filters" onSubmit={submit}>
            <label>
                From
                <input type="date" value={draft.startDate} max={draft.endDate} onChange={(event) => update("startDate", event.target.value)} required />
            </label>
            <label>
                To
                <input type="date" value={draft.endDate} min={draft.startDate} onChange={(event) => update("endDate", event.target.value)} required />
            </label>
            <label className="resort-filter">
                Resort (optional)
                <input type="text" value={draft.resortName} onChange={(event) => update("resortName", event.target.value)} placeholder="All resorts" />
            </label>
            <button className="button button-primary" type="submit">Apply filters</button>
        </form>
    );
}
