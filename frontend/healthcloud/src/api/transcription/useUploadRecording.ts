import { axiosService } from "@/api/axiosConfig";
import { useMutation } from "@tanstack/react-query";

interface UploadData {
    recording: Blob;
    duration: number;
}
const uploadTranscription = async (data: UploadData) => {
    const formData = new FormData();
    formData.append("file", data.recording, "recording.wav");
    formData.append("duration", data.duration.toString());

    const response = await axiosService.post("/recording/upload/", formData, {
        headers: { "content-type": "multipart/form-data" },
    });
    return response.data;
};

export const useUploadRecording = (onSuccess: () => void) => {
    return useMutation({
        mutationFn: (data: UploadData) => uploadTranscription(data),
        onSuccess: () => {
            onSuccess();
        },
    });
};
