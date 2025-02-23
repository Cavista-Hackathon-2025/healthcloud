import { axiosService } from "@/api/axiosConfig";
import { useMutation } from "@tanstack/react-query";

const uploadTranscription = async (recording: Blob) => {
    const formData = new FormData();
    formData.append("file", recording);

    const response = await axiosService.post("/transcription/upload", formData);
    return response.data;
};

export const useUploadRecording = () => {
    return useMutation({
        mutationFn: (recording: Blob) => uploadTranscription(recording),
    });
};
