export const useClipboard = () => {
    const canCopy = navigator.clipboard;

    const copyToClipboard = (text: string) => {
        if (!canCopy) {
            return false;
        } else {
            navigator.clipboard.writeText(text);
            return true;
        }
    };

    return { canCopy, copyToClipboard };
};
