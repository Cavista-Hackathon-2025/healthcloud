export interface ReportPreview {
    id: number | string;
    title: string;
    dateCreated: Date;
    summary: string;
    patientName: string;
    doctorName: string;
}

export interface Report {
    id: number | string;
    title: string;
    summary: string;
    dateCreated: Date;
    patientName: string;
    doctorName: string;
}
