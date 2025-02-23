import { createBrowserRouter, Navigate, RouterProvider } from "react-router";
import { TranscriptionRoutes } from "@/routes/transcription/TranscriptionRoutes";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReportsRoutes } from "@/routes/reports/ReportsRoutes";
import { Toaster } from "sonner";
import { RecordingsRoutes } from "@/routes/recordings/RecordingsRoutes";
import { GlobalError } from "@/components/GlobalError";
import { TranscriptionPaths } from "@/routes/transcription/TranscriptionPaths";
import { RootLayout } from "@/layouts/RootLayout";

const APP_ROUTES = [TranscriptionRoutes, ReportsRoutes, RecordingsRoutes];

const router = createBrowserRouter([
    {
        path: "/",
        element: <RootLayout />,
        errorElement: <GlobalError />,
        children: [
            {
                index: true,
                element: (
                    <Navigate to={TranscriptionPaths.TRANSCRIBE} replace />
                ),
            },
            ...APP_ROUTES.flat(),
        ],
    },
]);

const client = new QueryClient();

function App() {
    return (
        <QueryClientProvider client={client}>
            <Toaster position="top-right" />
            <RouterProvider router={router} />
        </QueryClientProvider>
    );
}

export default App;
