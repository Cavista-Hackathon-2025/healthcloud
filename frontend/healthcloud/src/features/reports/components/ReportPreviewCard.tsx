import { ReportsPaths } from "@/routes/reports/ReportsPaths";
import { Report } from "@/types/reports";
import { truncateText } from "@/utils/truncateText";
import { FaCalendar, FaUserDoctor } from "react-icons/fa6";
import { MdPersonalInjury } from "react-icons/md";
import { generatePath, Link } from "react-router-dom";

interface ReportPreviewCardProps {
    report: Report;
}

export const ReportPreviewCard = ({ report }: ReportPreviewCardProps) => {
    const REPORT_INFO_ITEMS = [
        {
            label: "Date Created",
            value: report?.dateCreated?.toLocaleDateString(),
            icon: <FaCalendar />,
        },
        {
            label: "Patient",
            value: report?.patientName,
            icon: <MdPersonalInjury />,
        },
        {
            label: "Doctor",
            value: report?.doctorName,
            icon: <FaUserDoctor />,
        },
    ];

    const reportUrl = generatePath(ReportsPaths.VIEW_REPORT, { id: report.id });

    return (
        <Link
            to={reportUrl}
            className="p-4 h-[21rem] bg-white rounded-lg shadow-sm shadow-sky-50 border border-slate-200 w-[20rem] flex flex-col hover:bg-sky-50 hover:border-sky-200 hover:shadow-sm hover:shadow-sky-200 hover:duration-100">
            <h3 className="font-semibold text-sky-600 text-lg leading-tight">
                {truncateText(report.title, 40, {
                    byWords: true,
                    addEllipsis: true,
                })}
            </h3>
            <p className="text-sm text-slate-500">
                {truncateText(report.summary, 120, {
                    byWords: true,
                    addEllipsis: true,
                })}
            </p>
            <div className="flex flex-col gap-1 mt-auto">
                {REPORT_INFO_ITEMS.map((item) => (
                    <div className="flex flex-row gap-2 items-center text-xs text-emerald-800">
                        {item.icon}
                        <span>{item.value}</span>
                    </div>
                ))}
            </div>
        </Link>
    );
};
