// import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { Outlet } from "react-router-dom";

export const DashboardLayout = () => {
    return (
        <main className="grid grid-cols-12 w-screen h-screen">
            <aside className="col-span-2 h-full bg-slate-100">
                <Sidebar />
            </aside>
            <div className="flex flex-col col-span-10 h-full shadow-sm shadow-slate-100">
                {/* <Navbar /> */}
                <Outlet />
            </div>
        </main>
    );
};
