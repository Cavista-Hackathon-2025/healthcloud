import { axiosService } from "@/api/axiosConfig";
import { Report } from "@/types/reports";
import { useQuery } from "@tanstack/react-query";

const getReports = async () => {
    const response = await axiosService.get<Report[]>("reports/");
    return response.data;
};

export const useReports = (enabled = true) => {
    return useQuery({
        queryKey: ["reports", "list"],
        queryFn: getReports,
        enabled: enabled,
    });
};
