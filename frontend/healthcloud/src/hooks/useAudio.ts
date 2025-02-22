import { useEffect, useRef, useState } from "react";
import RecordRTC from "recordrtc";
import WaveSurfer from "wavesurfer.js";
import {
    AUDIO_SAMPLE_RATE_IN_MS,
    TRANSCRIPTION_WEBSOCKET_URL,
    WAVEFORM_COLOR,
} from "@/constants";

export const useAudio = (waveformElementId = "waveform") => {
    const [transcript, setTranscript] = useState("");
    const [isRecording, setIsRecording] = useState(false);
    const [isPaused, setIsPaused] = useState(false);

    const wavesurferRef = useRef<WaveSurfer | null>(null);
    const audioChunksRef = useRef<Blob[]>([]);
    const recorderRef = useRef<RecordRTC | null>(null);
    const websocketRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        wavesurferRef.current = WaveSurfer.create({
            container: `#${waveformElementId}`,
            waveColor: WAVEFORM_COLOR,
            progressColor: "purple",
            cursorColor: "white",
            backend: "WebAudio",
            barWidth: 5,
            barRadius: 5,
        });

        // WebSocket Connection
        websocketRef.current = new WebSocket(TRANSCRIPTION_WEBSOCKET_URL);
        websocketRef.current.onmessage = (event) => {
            setTranscript((prev) => prev + " " + event.data);
        };

        return () => {
            websocketRef.current?.close();
            wavesurferRef.current?.destroy();
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const startRecording = async () => {
        if (isRecording) return;

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
        });

        const recorder = new RecordRTC(stream, {
            type: "audio",
            disableLogs: true,
            mimeType: "audio/wav",
            recorderType: RecordRTC.StereoAudioRecorder,
            timeSlice: AUDIO_SAMPLE_RATE_IN_MS,
            ondataavailable: (blob) => {
                audioChunksRef.current.push(blob);
                if (websocketRef.current?.readyState === WebSocket.OPEN) {
                    websocketRef.current.send(blob);
                }

                // Load audio into WaveSurfer
                const reader = new FileReader();
                reader.readAsArrayBuffer(blob);
                reader.onloadend = () => {
                    wavesurferRef.current?.loadBlob(blob);
                };
            },
        });

        recorder.startRecording();
        recorderRef.current = recorder;
        setIsRecording(true);
        setIsPaused(false);
    };

    const pauseRecording = () => {
        if (!recorderRef.current || !isRecording) return;
        if (isPaused) {
            recorderRef.current.resumeRecording();
        } else {
            recorderRef.current.pauseRecording();
        }
        setIsPaused(!isPaused);
    };

    const stopRecording = () => {
        if (!recorderRef.current) return;
        recorderRef.current.stopRecording(() => {
            recorderRef.current?.destroy();
            recorderRef.current = null;
            setIsRecording(false);
            setIsPaused(false);
        });

        wavesurferRef.current?.empty();
        audioChunksRef.current = [];
    };

    return {
        startRecording,
        stopRecording,
        pauseRecording,
        transcript,
        isRecording,
        isPaused,
    };
};
