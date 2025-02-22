import { ShareReportViaQRCodeModal } from "@/features/reports/components/ShareReportViaQRCodeModal";
import { useModal } from "@/hooks/useModal";
import { ReportsPaths } from "@/routes/reports/ReportsPaths";
import { Report } from "@/types/reports";
import { FaAngleRight } from "react-icons/fa6";
import { Link } from "react-router-dom";

export const ReportTest = () => {
    const report: Report = {
        id: 1,
        title: "Cerebral Palsy Report",
        summary: "Summary",
        dateCreated: new Date(),
        patientName: "Patient",
        doctorName: "Doctor",
    };

    const { isOpen, openModal, closeModal } = useModal("share");

    return (
        <div className="flex flex-col p-6 grow gap-2">
            {isOpen && (
                <ShareReportViaQRCodeModal
                    report={report}
                    onClose={closeModal}
                />
            )}
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
            <button onClick={openModal}>Share</button>
        </div>
    );
};
