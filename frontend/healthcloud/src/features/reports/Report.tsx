import { useReport } from "@/api/reports/useReport";
import { ErrorNotification } from "@/components/ErrorNotification";
import { Skeleton } from "@/components/ui/skeleton";
import { ShareReportViaQRCodeModal } from "@/features/reports/components/ShareReportViaQRCodeModal";
import { useModal } from "@/hooks/useModal";
import { ReportsPaths } from "@/routes/reports/ReportsPaths";
import { generateDocumentTitle } from "@/utils/generateDocumentTitle";
import { useDocumentTitle } from "@uidotdev/usehooks";
import { FaAngleRight, FaPaperPlane } from "react-icons/fa6";
import { Link, useParams } from "react-router-dom";

export const Report = () => {
    const { id } = useParams<{ id: string }>();
    const reportId = id ? Number(id) : 0;
    const {
        data: report,
        isError,
        isLoading,
    } = useReport(reportId, Boolean(reportId));

    const reportTitle = report?.title || "Report";
    const { openModal, closeModal, isOpen } = useModal("share");
    useDocumentTitle(generateDocumentTitle(reportTitle));

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
        <>
            {isOpen && (
                <ShareReportViaQRCodeModal
                    report={report}
                    onClose={closeModal}
                />
            )}

            <div className="flex flex-col p-6 grow gap-2">
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
                <div className="flex grow overflow-y-auto flex-row gap-2 p-5 pl-1">
                    {report.summary}
                </div>
                <button onClick={openModal}>
                    <FaPaperPlane />
                    <span>Share</span>
                </button>
            </div>
        </>
    );
};
