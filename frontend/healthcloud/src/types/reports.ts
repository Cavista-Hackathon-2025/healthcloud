export interface ReportPreview {
    id: string;
    title: string;
    dateCreated: Date;
    summary: string;
    patientName: string;
    doctorName: string;
}

export interface Report {
    id: number;
    title: string;
    summary: string;
    dateCreated: string;
}
