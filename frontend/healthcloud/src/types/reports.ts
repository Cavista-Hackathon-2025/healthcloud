export interface Report {
    id: number | string;
    title: string;
    summary: string;
    dateCreated: Date;
    patientName: string;
    doctorName: string;
}

// export type ReportDetailsImportanceRanking = "low" | "medium" | "high";

export interface ReportDetailsBlock {
    title: string;
    content: string;
    children?: ReportDetailsBlock[];
}
