import { ReportPaths } from "@/routes/reports/ReportsPaths";
import { FaNotesMedical, FaRegFileLines } from "react-icons/fa6";
import { Link } from "react-router-dom";
import logoImage from "@/assets/healthcloud_logo.png";
import { TranscriptionPaths } from "@/routes/transcription/TranscriptionPaths";
import { LuVideotape } from "react-icons/lu";

export const Sidebar = () => {
    const LINKS = [
        {
            label: "Sessions",
            icon: <FaNotesMedical />,
            href: "/",
        },
        {
            label: "Reports",
            icon: <FaRegFileLines />,
            href: ReportPaths.REPORTS,
        },
        {
            label: "Past Recordings",
            icon: <LuVideotape />,
            href: TranscriptionPaths.PAST_RECORDINGS,
        },
    ];

    return (
        <nav className="flex flex-col gap-1 justify-start p-4">
            <div className="flex flex-row items-center justify-start p-3">
                <img src={logoImage} alt="logo" className="w-16 h-16" />
                <h3 className="text-xl text-sky-800 font-semibold">
                    HealthCloud
                </h3>
            </div>
            {LINKS.map((link) => (
                <Link
                    className="flex flex-row gap-2 items-center justify-start p-3 text-slate-500 hover:text-sky-700 hover:bg-slate-200 duration-75 rounded-sm"
                    key={link.label}
                    to={link.href}>
                    {link.icon}
                    <span>{link.label}</span>
                </Link>
            ))}
        </nav>
    );
};
