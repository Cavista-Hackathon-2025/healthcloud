import { createBrowserRouter, RouterProvider } from "react-router";
import { TranscriptionRoutes } from "@/routes/transcription/TranscriptionRoutes";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const APP_ROUTES = [TranscriptionRoutes];

const router = createBrowserRouter([
    {
        children: APP_ROUTES.flat(),
    },
]);

const client = new QueryClient();

function App() {
    return (
        <QueryClientProvider client={client}>
            <RouterProvider router={router} />
        </QueryClientProvider>
    );
}

export default App;
