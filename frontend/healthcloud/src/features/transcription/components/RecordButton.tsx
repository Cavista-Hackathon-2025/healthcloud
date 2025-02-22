import { FaMicrophone } from "react-icons/fa6";

export const RecordButton = () => {
    return (
        <button className="flex flex-row gap-2 py-3 px-5 text-white bg-rose-500 hover:bg-rose-600 duration-100 shadow-sm rounded-full items-center font-semibold">
            <FaMicrophone className="text-2xl" />
            <span>Start recording</span>
        </button>
    );
};
