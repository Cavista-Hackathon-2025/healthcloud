# test_audio.py
import sounddevice as sd
import numpy as np

def test_microphone(duration=5, sample_rate=16000):
    """
    Record audio for a few seconds and play it back
    """
    print(f"Recording {duration} seconds of audio...")
    
    # Record audio
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='float32'
    )
    
    # Wait until recording is done
    sd.wait()
    print("Recording finished!")
    
    # Play back the recording
    print("Playing back the recording...")
    sd.play(recording, sample_rate)
    sd.wait()
    print("Playback finished!")
    
    # Print some info about the recording
    print(f"Recording shape: {recording.shape}")
    print(f"Max amplitude: {np.max(np.abs(recording))}")

# List available audio devices
print("Available audio devices:")
print(sd.query_devices())
print("\nDefault devices:")
print(f"Input: {sd.query_devices(kind='input')}")
print(f"Output: {sd.query_devices(kind='output')}")

# Run the test
if __name__ == "__main__":
    test_microphone()