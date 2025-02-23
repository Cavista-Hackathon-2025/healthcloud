import logoImage from "@/assets/healthcloud_logo.png";
import { UserInfo } from "@/components/UserInfo";
import { ReportsPaths } from "@/routes/reports/ReportsPaths";
import { TranscriptionPaths } from "@/routes/transcription/TranscriptionPaths";
import { FaNotesMedical, FaRegFileLines } from "react-icons/fa6";
import { NavLink } from "react-router-dom";
import { LuVideotape } from "react-icons/lu";

export const Sidebar = () => {
    const LINKS = [
        {
            label: "Transcribe",
            icon: <FaNotesMedical />,
            href: TranscriptionPaths.TRANSCRIBE,
        },
        {
            label: "Reports",
            icon: <FaRegFileLines />,
            href: ReportsPaths.REPORTS,
        },
        {
            label: "Recordings",
            icon: <LuVideotape />,
            href: TranscriptionPaths.RECORDING_HISTORY,
        },
    ];

    return (
        <nav className="flex flex-col gap-1 justify-start p-4 h-full">
            <div className="flex flex-row items-center justify-start p-3">
                <img src={logoImage} alt="logo" className="w-18 h-18" />
                <div className="flex flex-col -mt-1">
                    <h3 className="text-xl text-sky-800 font-semibold">
                        HealthCloud
                    </h3>
                    <span className="text-xs text-right text-slate-500 -mt-1">
                        by{" "}
                        <span className="text-emerald-800 font-semibold">
                            BioTrio
                        </span>
                    </span>
                </div>
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
