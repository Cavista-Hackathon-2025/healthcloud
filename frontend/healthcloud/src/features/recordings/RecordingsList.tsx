import { generateDocumentTitle } from "@/utils/generateDocumentTitle";
import { useDocumentTitle } from "@uidotdev/usehooks";

export const RecordingsList = () => {
    useDocumentTitle(generateDocumentTitle("Recordings"));
    // const { data: reports, isError, isLoading } = useReports();

    // if (isLoading) {
    //     return (
    //         <div className="flex flex-col p-6 grow gap-2">
    //             <h1 className="text-3xl font-semibold text-sky-800">
    //                 Recordings
    //             </h1>
    //             <div className="flex grow overflow-y-auto flex-row gap-2 p-5 pl-1">
    //                 {/* {cloneComponent(
    //                     <Skeleton className="w-[20rem] h-[21rem]" />,
    //                     5
    //                 )} */}
    //             </div>
    //         </div>
    //     );
    // }

    // if (isError || !reports) {
    //     return (
    //         <div className="flex flex-col p-6 grow gap-2">
    //             <h1 className="text-3xl font-semibold text-sky-800">
    //                 My reports
    //             </h1>
    //             <div className="flex grow overflow-y-auto flex-row gap-2 p-5 pl-1">
    //                 <ErrorNotification />
    //             </div>
    //         </div>
    //     );
    // }

    return (
        <div className="flex flex-col p-6 grow gap-2">
            <h1 className="text-3xl font-semibold text-sky-800">Recordings</h1>
            <div className="flex grow overflow-y-auto flex-row gap-2 p-5 pl-1"></div>
        </div>
    );
};
