import doctorPlaceholderImage from "@/assets/doctor.png";

export const Navbar = () => {
    return (
        <nav className="w-full flex flex-row p-4 justify-center bg-sky-50">
            <div className="flex rounded-full items-center gap-2 text-slate-800">
                <img
                    src={doctorPlaceholderImage}
                    alt="doctor"
                    className="w-8 h-8 rounded-full border border-slate-300"
                />
                <span>Dr. John Okoro</span>
            </div>
        </nav>
    );
};
