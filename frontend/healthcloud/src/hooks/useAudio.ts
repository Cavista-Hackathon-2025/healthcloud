import { useEffect, useRef, useState } from "react";
import RecordRTC from "recordrtc";
import WaveSurfer from "wavesurfer.js";
import { AUDIO_SAMPLE_RATE_IN_MS, WAVEFORM_COLOR } from "@/constants";

export const useAudio = (waveformElementId = "waveform") => {
    const [isRecording, setIsRecording] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
    const [duration, setDuration] = useState<number>(0);

    const wavesurferRef = useRef<WaveSurfer | null>(null);
    const recorderRef = useRef<RecordRTC | null>(null);
    const startTimeRef = useRef<number>(0);

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

        return () => {
            wavesurferRef.current?.destroy();
        };
    }, [waveformElementId]);

    const startRecording = async () => {
        if (isRecording) return;

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
        });
        startTimeRef.current = Date.now();
        setAudioBlob(null);
        setDuration(0);

        const recorder = new RecordRTC(stream, {
            type: "audio",
            disableLogs: true,
            mimeType: "audio/wav", // Ensure WAV format
            recorderType: RecordRTC.StereoAudioRecorder,
            timeSlice: AUDIO_SAMPLE_RATE_IN_MS,
            desiredSampRate: 16000, // Optional: Set sample rate
            numberOfAudioChannels: 1, // Mono audio
            ondataavailable: (blob) => {
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

    const stopRecording = async (): Promise<{
        blob: Blob;
        duration: number;
    } | null> => {
        if (!recorderRef.current) return null;

        return new Promise((resolve) => {
            recorderRef.current?.stopRecording(() => {
                const blob = recorderRef.current?.getBlob();
                const endTime = Date.now();
                const calculatedDuration = endTime - startTimeRef.current;

                if (blob) {
                    // Ensure WAV format
                    const wavBlob = new Blob([blob], { type: "audio/wav" });
                    setAudioBlob(wavBlob);
                    setDuration(calculatedDuration);
                    resolve({ blob: wavBlob, duration: calculatedDuration });
                } else {
                    resolve(null);
                }

                recorderRef.current?.destroy();
                recorderRef.current = null;
                setIsRecording(false);
                setIsPaused(false);
                wavesurferRef.current?.empty();
            });
        });
    };

    return {
        startRecording,
        stopRecording,
        pauseRecording,
        isRecording,
        isPaused,
        audioBlob,
        duration,
    };
};
