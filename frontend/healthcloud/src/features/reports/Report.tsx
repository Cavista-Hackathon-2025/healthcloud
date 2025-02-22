import { useReport } from "@/api/reports/useReport";
import { ErrorNotification } from "@/components/ErrorNotification";
import { Skeleton } from "@/components/ui/skeleton";
import { useParams } from "react-router-dom";

export const Report = () => {
    const { id } = useParams<{ id: string }>();

    const reportId = id ? Number(id) : 0;

    const { data: report, isError, isLoading } = useReport(reportId, true);

    console.log("Report: ", report);
    if (isLoading) {
        <div className="flex flex-col p-6 grow gap-2">
            <div className="flex grow overflow-y-auto flex-row gap-2 p-5 pl-1">
                <Skeleton className="w-full h-full" />
            </div>
        </div>;
    }

    if (isError || !report) {
        return (
            <div className="flex flex-col p-6 grow gap-2">
                <div className="flex grow overflow-y-auto flex-row gap-2 p-5 pl-1">
                    <ErrorNotification />
                </div>
            </div>
        );
    }

    return (
        <div className="flex flex-col p-6 grow gap-2">
            <h1 className="text-3xl font-semibold text-sky-800">
                {report.title}
            </h1>
            <div className="flex grow overflow-y-auto flex-row gap-2 p-5 pl-1">
                {report.summary}
            </div>
        </div>
    );
};
