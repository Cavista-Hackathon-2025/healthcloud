import { ReportSegment, SegmentType } from "@/types/reports";
import React from "react";
import {
    FaGlobe,
    FaMessage,
    FaPills,
    FaStethoscope,
    FaTriangleExclamation,
} from "react-icons/fa6";
import { PiPersonArmsSpreadFill } from "react-icons/pi";

interface ReportSegmentCardProps {
    segment: ReportSegment;
}

const ICON_MAPPING: Record<SegmentType, React.ReactElement> = {
    DIAGNOSIS: <FaStethoscope />,
    ALLEVIATING_WORRIES: <PiPersonArmsSpreadFill />,
    WARNINGS: <FaTriangleExclamation />,
    GENERAL_DISCUSSIONS: <FaMessage />,
    PRESCRIPTIONS: <FaPills />,
    INFORMATION_EXCHANGE: <FaGlobe />,
};

const LABEL_MAPPING: Record<SegmentType, string> = {
    DIAGNOSIS: "Diagnosis",
    ALLEVIATING_WORRIES: "Alleviating Worries",
    WARNINGS: "Warnings",
    GENERAL_DISCUSSIONS: "General Discussions",
    PRESCRIPTIONS: "Prescriptions",
    INFORMATION_EXCHANGE: "Information Exchange",
};

const segmentColors: Record<SegmentType, string> = {
    DIAGNOSIS: "bg-blue-100 border-blue-300 text-blue-800",
    ALLEVIATING_WORRIES: "bg-teal-100 border-teal-300 text-teal-800",
    WARNINGS: "bg-red-100 border-red-300 text-red-800",
    GENERAL_DISCUSSIONS: "bg-gray-100 border-gray-300 text-gray-800",
    INFORMATION_EXCHANGE: "bg-purple-100 border-purple-300 text-purple-800",
    PRESCRIPTIONS: "bg-emerald-100 border-emerald-300 text-emerald-800",
};

export const ReportSegmentCard = ({ segment }: ReportSegmentCardProps) => {
    return (
        <table className="w-auto max-w-md border border-gray-300 rounded-lg">
            <thead>
                <tr className={`${segmentColors[segment.type]}`}>
                    <th className="py-2 px-3 text-sm font-medium flex items-center gap-2">
                        {ICON_MAPPING[segment.type]}
                        <span>{LABEL_MAPPING[segment.type]}</span>
                    </th>
                </tr>
            </thead>
            <tbody>
                {segment.keypoints.map((point, index) => (
                    <tr
                        key={index}
                        className="border-t border-gray-200 hover:bg-gray-50 transition">
                        <td className="py-1.5 px-3 text-sm text-gray-600">
                            {point}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};
