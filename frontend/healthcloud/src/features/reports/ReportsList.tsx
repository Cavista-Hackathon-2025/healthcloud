import { ReportPreviewCard } from "@/features/reports/components/ReportPreviewCard";
import { ReportPreview } from "@/types/reports";

const MOCK_REPORTS: ReportPreview[] = [
    {
        id: "dkh28y9",
        title: "Accident report - Composite fracture",
        summary:
            "Patient was involved in a car accident and sustained a composite fracture, amongst other minor to severe injuries",
        dateCreated: new Date(),
        patientName: "Jimmy Agbaje",
        doctorName: "Dr. Julius Ekene",
    },

    {
        id: "dfs9y29",
        title: "Surgical report - Appendectomy",
        summary: "Patient underwent an appendectomy surgery",
        dateCreated: new Date(),
        patientName: "Chinwe Okafor",
        doctorName: "Dr. Julius Ekene",
    },

    {
        id: "dsfiw7t8",
        title: "Consultation report - Hypertension",
        summary: "Patient was diagnosed with hypertension",
        dateCreated: new Date(),
        patientName: "Bola Akindele",
        doctorName: "Dr. Julius Ekene",
    },

    {
        id: "qerhohidf",
        title: "Laboratory report - Blood test",
        summary: "Patient did a blood test",
        dateCreated: new Date(),
        patientName: "Righteous Obono",
        doctorName: "Dr. Julius Ekene",
    },

    {
        id: "09sfsd0u0",
        title: "Radiology report - X-ray",
        summary: "Patient did an X-ray scan",
        dateCreated: new Date(),
        patientName: "Tolu Adewale",
        doctorName: "Dr. Julius Ekene",
    },
];
export const ReportsList = () => {
    return (
        <div className="flex flex-col p-6 grow gap-2">
            <h1 className="text-3xl font-semibold text-sky-800">My reports</h1>
            <div className="flex grow overflow-y-auto flex-row gap-2 p-5 pl-1">
                {MOCK_REPORTS.map((report) => (
                    <ReportPreviewCard report={report} />
                ))}
            </div>
        </div>
    );
};
