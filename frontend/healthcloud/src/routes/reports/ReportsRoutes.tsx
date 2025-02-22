import { Report } from "@/features/reports/Report";
import { ReportsList } from "@/features/reports/ReportsList";
import { ReportTest } from "@/features/reports/ReportTest";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { ReportsPaths } from "@/routes/reports/ReportsPaths";
import { RouteObject } from "react-router-dom";

export const ReportsRoutes: RouteObject[] = [
    {
        path: "/dashboard",
        element: <DashboardLayout />,
        children: [
            {
                path: ReportsPaths.REPORTS,
                element: <ReportsList />,
            },
            {
                path: "/dashboard/reports/test",
                element: <ReportTest />,
            },
            {
                path: ReportsPaths.VIEW_REPORT,
                element: <Report />,
            },
        ],
    },
];
