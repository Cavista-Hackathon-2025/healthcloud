import { axiosService } from "@/api/axiosConfig";
import { Report } from "@/types/reports";
import { useQuery } from "@tanstack/react-query";

const getReport = async (id: number | string) => {
    const response = await axiosService.get<Report>(`reports/${id}/`);
    return response.data;
};

export const useReport = (id: number | string, enabled = true) => {
    return useQuery({
        queryKey: ["reports", "detail", id],
        queryFn: () => getReport(id),
        enabled: enabled,
    });
};
