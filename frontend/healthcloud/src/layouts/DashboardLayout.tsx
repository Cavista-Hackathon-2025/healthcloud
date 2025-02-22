// import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { Outlet } from "react-router-dom";

export const DashboardLayout = () => {
    return (
        <main className="grid grid-cols-12 w-screen h-screen bg-slate-100">
            <aside className="col-span-2 h-full bg-slate-100">
                <Sidebar />
            </aside>
            <div className="bg-white col-span-12 flex flex-col md:col-span-10 h-full shadow-sm rounded-l-lg shadow-slate-200">
                {/* <Navbar /> */}
                <Outlet />
            </div>
        </main>
    );
};
