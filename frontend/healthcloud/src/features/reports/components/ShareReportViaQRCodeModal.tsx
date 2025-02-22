import { useClipboard } from "@/hooks/useClipboard";
import { ModalLayout } from "@/layouts/ModalLayout";
import { ReportsPaths } from "@/routes/reports/ReportsPaths";
import { Report } from "@/types/reports";
import { generateAbsoluteURL } from "@/utils/generateAbsoluteURL";
import { FaCopy, FaXmark } from "react-icons/fa6";
import QRCode from "react-qr-code";
import { generatePath } from "react-router-dom";
import { toast } from "sonner";

interface ShareReportViaQRCodeModalProps {
    report: Report;
    onClose: () => void;
}

export const ShareReportViaQRCodeModal = ({
    report,
    onClose,
}: ShareReportViaQRCodeModalProps) => {
    const reportRelativeUrl = generatePath(ReportsPaths.VIEW_REPORT_EXTERNAL, {
        id: report.id,
    });

    const { canCopy, copyToClipboard } = useClipboard();

    const reportUrl = generateAbsoluteURL(reportRelativeUrl);

    const handleCopyLink = () => {
        if (canCopy) {
            copyToClipboard(reportUrl);
            toast.success("Link copied to clipboard");
        } else {
            toast.error("Failed to copy link to clipboard");
        }

        onClose();
    };

    return (
        <ModalLayout>
            <div className="flex flex-col relative bg-white p-6 py-8 rounded-md shadow-md w-80 h-fit">
                <button
                    className="absolute top-4 right-4 text-sky-900"
                    onClick={onClose}>
                    <FaXmark />
                </button>
                <div className="flex flex-col items-center">
                    <h4 className="text-xl font-semibold text-sky-800 text-center">
                        Share this report
                    </h4>
                    <p className=" text-slate-600 leading-tight">
                        Scan the QR code below to view this report
                    </p>
                    <div className="my-3 mt-5">
                        <QRCode
                            size={256}
                            style={{
                                height: "auto",
                                maxWidth: "100%",
                                width: "100%",
                            }}
                            value={reportUrl}
                            viewBox={`0 0 256 256`}
                        />
                    </div>
                    <button
                        onClick={handleCopyLink}
                        className="mt-4 bg-emerald-800 text-white rounded-md p-2 w-full text-center items-center flex flex-row gap-2 justify-center hover:bg-emerald-900 duration-100">
                        <FaCopy />
                        <span>Copy link</span>
                    </button>
                </div>
            </div>
        </ModalLayout>
    );
};
