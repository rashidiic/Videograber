def get_mock_response(filename: str = "audio.mp3") -> dict:
    return {
        "status": "ok",
        "filename": filename,
        "duration_seconds": 237,
        "language": "en",
        "confidence": 0.97,
        "transcription": (
            "This is a mocked transcription of the uploaded audio file. "
            "Replace this text with real transcription results once the "
            "actual speech-to-text API endpoint is integrated."
        ),
        "sample_rate_hz": 44100,
        "bitrate_kbps": 192,
        "channels": 2,
    }
