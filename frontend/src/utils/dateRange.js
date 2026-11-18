function isoDate(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}

export function defaultDateRange() {
    const today = new Date();
    const start = new Date(today);
    start.setDate(today.getDate() - 29);

    return {
        startDate: isoDate(start),
        endDate: isoDate(today),
        resortName: ""
    };
}