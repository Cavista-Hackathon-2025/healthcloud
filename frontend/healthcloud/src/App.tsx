import { createBrowserRouter, RouterProvider } from "react-router";
import { TranscriptionRoutes } from "@/routes/transcription/TranscriptionRoutes";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReportsRoutes } from "@/routes/reports/ReportsRoutes";
import { Toaster } from "sonner";

const APP_ROUTES = [TranscriptionRoutes, ReportsRoutes];

const router = createBrowserRouter([
    {
        children: APP_ROUTES.flat(),
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
