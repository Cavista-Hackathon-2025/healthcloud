import { Outlet } from "react-router-dom";

export const RootLayout = () => {
    return (
        <main className="flex flex-col h-screen w-screen">
            <Outlet />
        </main>
    );
};
