import { useQuery } from "@tanstack/react-query";

export const useReports = () => {
    return useQuery({
        queryKey: ["reports", "list"],
    });
};
