import logoImage from "@/assets/healthcloud_logo.png";
import { TranscriptionPaths } from "@/routes/transcription/TranscriptionPaths";
import { FaHouse } from "react-icons/fa6";
import { Link, useRouteError } from "react-router-dom";

export const GlobalError = () => {
    const error = useRouteError();
    console.error(error);

    return (
        <main className="h-screen w-screen flex justify-center items-center flex-col gap-2">
            <img src={logoImage} alt="logo" className="w-32 h-32" />
            <h1 className="text-5xl font-semibold text-sky-800 -mt-8 max-w-1/3 text-center">
                Something terrible happened :\
            </h1>
            <p className="text-lg text-slate-400 max-w-1/3 text-center mb-2">
                Our app seems to need some medical attention (or perhaps you
                just entered an incorrect URL). Please stand by while we address
                this!
            </p>
            <Link
                to={TranscriptionPaths.TRANSCRIBE}
                className="bg-sky-700 text-white py-2 px-4 rounded-full flex flex-row items-center justify-center gap-2">
                <FaHouse />
                <span>Back to Transcribe</span>
            </Link>
        </main>
    );
};
