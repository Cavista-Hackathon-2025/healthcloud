export interface Patient {
    id: string;
    name: string;
}

export interface Doctor {
    id: string;
    name: string;
}

export type SegmentType =
    | "DIAGNOSIS"
    | "ALLEVIATING_WORRIES"
    | "WARNINGS"
    | "GENERAL_DISCUSSIONS"
    | "INFORMATION_EXCHANGE"
    | "PRESCRIPTIONS";
export interface ReportSegment {
    id: string;
    title: string;
    type: SegmentType;
    content: string;
    keypoints: string[];
}
export interface Report {
    id: number | string;
    title: string;
    summary: string;
    dateCreated: Date;
    patient: Patient;
    doctor: Doctor;
    segments?: ReportSegment[];
}
