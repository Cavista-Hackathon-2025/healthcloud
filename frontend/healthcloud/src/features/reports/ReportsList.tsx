import { useReports } from "@/api/reports/useReports";
import { ErrorNotification } from "@/components/ErrorNotification";
import { Skeleton } from "@/components/ui/skeleton";
import { ReportPreviewCard } from "@/features/reports/components/ReportPreviewCard";
import { cloneComponent } from "@/utils/cloneComponent";
import { generateDocumentTitle } from "@/utils/generateDocumentTitle";
import { useDocumentTitle } from "@uidotdev/usehooks";

export const ReportsList = () => {
    useDocumentTitle(generateDocumentTitle("My reports"));
    const { data: reports, isError, isLoading, isSuccess } = useReports();

    return (
        <div className="flex flex-col p-6 grow gap-2 h-screen">
            <h1 className="text-3xl font-semibold text-sky-800">Reports</h1>
            <div className="flex grow overflow-y-auto flex-row gap-4 p-5 pl-1 flex-wrap">
                {isLoading && (
                    <>
                        {" "}
                        {cloneComponent(
                            <Skeleton className="w-[16rem] h-[21rem]" />,
                            4
                        )}
                    </>
                )}

                {(isError || !reports) && !isLoading && <ErrorNotification />}

                {isSuccess && reports && (
                    <>
                        {reports.map((report) => (
                            <ReportPreviewCard report={report} />
                        ))}
                    </>
                )}
            </div>
        </div>
    );
};
