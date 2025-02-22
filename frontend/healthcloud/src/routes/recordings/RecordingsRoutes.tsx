import { RecordingsList } from "@/features/recordings/RecordingsList";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { RecordingsPaths } from "@/routes/recordings/RecordingsPaths";
import { RouteObject } from "react-router-dom";

export const RecordingsRoutes: RouteObject[] = [
    {
        path: "/dashboard",
        element: <DashboardLayout />,
        children: [
            {
                path: RecordingsPaths.RECORDINGS,
                element: <RecordingsList />,
            },
        ],
    },
];
