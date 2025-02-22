import { axiosService } from "@/api/axiosConfig";
import { Report } from "@/types/reports";
import { useQuery } from "@tanstack/react-query";

const getReport = async (id: number) => {
    const response = await axiosService.get<Report>(`reports/${id}/`);
    return response.data;
};

export const useReport = (id: number, enabled = true) => {
    return useQuery({
        queryKey: ["reports", "detail", id],
        queryFn: () => getReport(id),
        enabled: enabled,
    });
};
