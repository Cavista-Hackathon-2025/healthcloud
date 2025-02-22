import { RecordButton } from "@/features/transcription/components/RecordButton";
import { generateDocumentTitle } from "@/utils/generateDocumentTitle";
import { useDocumentTitle } from "@uidotdev/usehooks";

export const RecordSession = () => {
    useDocumentTitle(generateDocumentTitle("Record Session"));

    return (
        <div className="flex flex-col justify-center items-center p-2 grow">
            <RecordButton />
        </div>
    );
};
