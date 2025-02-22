import logoImage from "@/assets/healthcloud_logo.png";
import { UserInfo } from "@/components/UserInfo";
import { ReportPaths } from "@/routes/reports/ReportsPaths";
import { TranscriptionPaths } from "@/routes/transcription/TranscriptionPaths";
import { FaNotesMedical, FaRegFileLines } from "react-icons/fa6";
import { LuVideotape } from "react-icons/lu";
import { NavLink } from "react-router-dom";

export const Sidebar = () => {
    const LINKS = [
        {
            label: "Sessions",
            icon: <FaNotesMedical />,
            href: TranscriptionPaths.START_SESSION,
        },
        {
            label: "Reports",
            icon: <FaRegFileLines />,
            href: ReportPaths.REPORTS,
        },
        {
            label: "Past Recordings",
            icon: <LuVideotape />,
            href: TranscriptionPaths.RECORDING_HISTORY,
        },
    ];

    return (
        <nav className="flex flex-col gap-1 justify-start p-4 h-full">
            <div className="flex flex-row items-center justify-start p-3">
                <img src={logoImage} alt="logo" className="w-16 h-16" />
                <h3 className="text-xl text-sky-800 font-semibold">
                    HealthCloud
                </h3>
            </div>
            {LINKS.map((link) => (
                <NavLink
                    className={({ isActive }) =>
                        [
                            "flex flex-row gap-2 items-center justify-start p-3 duration-75 rounded-sm",
                            isActive
                                ? "bg-sky-200 text-sky-700"
                                : "text-slate-500 hover:text-sky-700 hover:bg-slate-200",
                        ].join(" ")
                    }
                    key={link.label}
                    to={link.href}>
                    {link.icon}
                    <span>{link.label}</span>
                </NavLink>
            ))}
            <div className=" mt-auto">
                <UserInfo />
            </div>
        </nav>
    );
};
