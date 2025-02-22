import { RecordSession } from "@/features/transcription/RecordSession";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { RouteObject } from "react-router-dom";
import { TranscriptionPaths } from "./TranscriptionPaths";

export const TranscriptionRoutes: RouteObject[] = [
    {
        path: "/dashboard",
        element: <DashboardLayout />,
        children: [
            {
                path: TranscriptionPaths.TRANSCRIBE,
                element: <RecordSession />,
            },
        ],
    },
];
