import { ReportPreviewCard } from "@/features/reports/components/ReportPreviewCard";
import { generateReports } from "@/mocks/generateReports";
import { generateDocumentTitle } from "@/utils/generateDocumentTitle";
import { faker } from "@faker-js/faker";
import { useDocumentTitle } from "@uidotdev/usehooks";

export const ReportsList = () => {
    useDocumentTitle(generateDocumentTitle("Reports"));
    // const { data: reports, isError, isLoading, isSuccess } = useReports();
    const mockReports = generateReports(faker.number.int({ min: 5, max: 20 }));
    console.log(mockReports);

    return (
        <div className="flex flex-col p-6 grow gap-2 h-screen">
            <h1 className="text-3xl font-semibold text-sky-800">Reports</h1>
            <div className="flex grow overflow-y-auto flex-row gap-4 p-5 pl-1 flex-wrap">
                {/* {isLoading && (
                    <>
                        {" "}
                        {cloneComponent(
                            <Skeleton className="w-[16rem] h-[21rem]" />,
                            4
                        )}
                    </>
                )}

                {(isError || !reports) && !isLoading && <ErrorNotification />} */}

                <>
                    {mockReports.map((report) => (
                        <ReportPreviewCard report={report} />
                    ))}
                </>
            </div>
        </div>
    );
};
