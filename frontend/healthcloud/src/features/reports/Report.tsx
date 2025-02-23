import { ReportSegmentCard } from "@/features/reports/components/ReportSegmentCard";
import { ShareReportViaQRCodeModal } from "@/features/reports/components/ShareReportViaQRCodeModal";
import { useModal } from "@/hooks/useModal";
import { generateReports } from "@/mocks/generateReports";
import { ReportsPaths } from "@/routes/reports/ReportsPaths";
import { generateDocumentTitle } from "@/utils/generateDocumentTitle";
import { useDocumentTitle } from "@uidotdev/usehooks";
import { FaAngleRight, FaPaperPlane } from "react-icons/fa6";
import { Link } from "react-router-dom";

export const Report = () => {
    // const { id } = useParams<{ id: string }>();
    // const reportId = id || "";

    // const {
    //     data: report,
    //     isError,
    //     isLoading,
    // } = useReport(reportId, Boolean(reportId));
    const report = generateReports(1)[0];
    const reportTitle = report?.title || "Report";
    const { openModal, closeModal, isOpen } = useModal("share");
    useDocumentTitle(generateDocumentTitle(reportTitle));

    // if (isLoading) {
    //     <div className="flex flex-col p-6 grow gap-2">
    //         <div className="flex grow overflow-y-auto flex-row gap-2 p-5 pl-1">
    //             <Skeleton className="w-full h-full" />
    //         </div>
    //     </div>;
    // }

    // if (isError || !report) {
    //     return (
    //         <div className="flex flex-col p-6 grow gap-2">
    //             <div className="flex grow overflow-y-auto flex-row gap-2 p-5 pl-1">
    //                 <ErrorNotification />
    //             </div>
    //         </div>
    //     );
    // }

    return (
        <>
            {isOpen && (
                <ShareReportViaQRCodeModal
                    report={report}
                    onClose={closeModal}
                />
            )}

            <div className="flex flex-col p-6 grow h-full w-full">
                <div className="flex flex-row gap-4 text-3xl items-center">
                    <Link
                        to={ReportsPaths.REPORTS}
                        className="text-slate-400 text-3xl font-semibold hover:text-sky-600">
                        Reports
                    </Link>
                    <FaAngleRight className="text-slate-300 text-lg" />
                    <h1 className="text-3xl font-semibold text-sky-800">
                        {report.title}
                    </h1>
                </div>
                <p className="flex overflow-y-auto flex-row gap-2 mt-2 text-slate-500 mb-4 max-w-1/2">
                    {report.summary}
                </p>

                {/* Scrollable container for ReportSegmentCards */}
                <div className="flex grow flex-row flex-wrap gap-2 overflow-y-auto max-h-[68vh] p-2 border border-gray-300 rounded-md">
                    {report.segments?.map((segment) => (
                        <ReportSegmentCard segment={segment} key={segment.id} />
                    ))}
                </div>

                <button
                    onClick={openModal}
                    className="mt-4 flex flex-row py-2 px-8 rounded-md text-white bg-emerald-800 hover:bg-emerald-900 w-fit items-center justify-center gap-2">
                    <FaPaperPlane />
                    <span>Share</span>
                </button>
            </div>
        </>
    );
};
