export const truncateText = (
    text: string,
    maxLength: number,
    options?: {
        byWords?: boolean;
        addEllipsis?: boolean;
    }
) => {
    const { byWords = false, addEllipsis = false } = options || {};

    if (text.length <= maxLength) return text;

    if (byWords) {
        const words = text.split(" ");
        let truncated = "";
        for (const word of words) {
            if ((truncated + " " + word).trim().length > maxLength) break;
            truncated += (truncated ? " " : "") + word;
        }
        return addEllipsis ? truncated + "…" : truncated;
    } else {
        return addEllipsis
            ? text.slice(0, maxLength).trim() + "…"
            : text.slice(0, maxLength);
    }
};
