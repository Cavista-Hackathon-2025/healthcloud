import doctorImage from "@/assets/doctor.png";

export const UserInfo = () => {
    return (
        <div className="flex flex-row gap-2 p-2 rounded-sm bg-slate-200 items-center shadow-inner">
            <img
                src={doctorImage}
                className="rounded-full border border-slate-200 w-10 h-10"
            />
            <div className="flex flex-col text-sm justify-center">
                <h6 className="font-semibold text-sky-700">Dr. Julius Ekene</h6>
                <span className=" text-slate-500">General Practitioner</span>
            </div>
        </div>
    );
};
