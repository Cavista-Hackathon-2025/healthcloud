import { useAudio } from "@/hooks/useAudio";
import { generateDocumentTitle } from "@/utils/generateDocumentTitle";
import { useDocumentTitle } from "@uidotdev/usehooks";
import clsx from "clsx";
import { FaMicrophone, FaPause, FaPlay, FaStop } from "react-icons/fa6";

export const RecordSession = () => {
    useDocumentTitle(generateDocumentTitle("Record Session"));
    const {
        startRecording,
        isRecording,
        pauseRecording,
        isPaused,
        stopRecording,
    } = useAudio("waveform");

    const isRecordingStarted = isRecording;
    const isRecordingStartedAndPaused = isRecording && isPaused;
    const isRecordingNotStarted = !isRecording && !isPaused;
    const isRecordingOngoing = isRecording && !isPaused;

    return (
        <div className="flex flex-col justify-center items-center p-2 grow gap-2">
            <div id="waveform" className=" h-48 rounded-lg w-[32rem]"></div>
            <div className="py-2 px-4 text-center w-84 mb-2 text-slate-500 bg-slate-50 rounded-md">
                and then we didn't really need to do the things we needed
            </div>
            <div className="flex flex-row gap-2">
                <button
                    className={clsx(
                        "flex flex-row gap-2 py-3 px-5 text-white  duration-100 shadow-sm rounded-full items-center font-semibold",
                        isRecordingNotStarted &&
                            "bg-rose-500 hover:bg-rose-600",
                        isRecordingOngoing && "bg-amber-500 bg-amber-60",
                        isRecordingStartedAndPaused &&
                            "bg-rose-500 hover:bg-rose-600"
                    )}
                    onClick={isRecording ? pauseRecording : startRecording}>
                    {isRecordingNotStarted && (
                        <>
                            <FaMicrophone />
                            <span>Start recording</span>
                        </>
                    )}
                    {isRecordingStartedAndPaused && (
                        <>
                            <FaPlay />
                            <span>Resume recording</span>
                        </>
                    )}
                    {isRecordingOngoing && (
                        <>
                            <FaPause />
                            <span>Pause recording</span>
                        </>
                    )}
                </button>

                {isRecordingStarted && (
                    <button
                        className="py-3 px-5 text-white bg-red-500 hover:bg-red-600 duration-100 shadow-sm rounded-full font-semibold"
                        onClick={stopRecording}>
                        <FaStop />
                    </button>
                )}
            </div>
        </div>
    );
};
