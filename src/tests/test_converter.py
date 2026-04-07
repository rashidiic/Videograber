from bot.utils.formatters import format_response


class TestFormatResponse:
    def test_basic_format(self) -> None:
        data = {
            "status": "ok", "filename": "test.mp3",
            "duration_seconds": 180, "language": "en",
            "confidence": 0.95, "transcription": "Hello world",
            "sample_rate_hz": 44100, "bitrate_kbps": 192, "channels": 2,
        }
        result = format_response(data)
        assert "test.mp3" in result
        assert "3m 0s" in result
        assert "Hello world" in result
        assert "95%" in result

    def test_missing_keys(self) -> None:
        assert "ok" not in format_response({"status": "ok"})

    def test_empty_dict(self) -> None:
        assert "Audio processing result" in format_response({})

    def test_stereo_label(self) -> None:
        assert "stereo" in format_response({"channels": 2})

    def test_mono_no_stereo_label(self) -> None:
        assert "stereo" not in format_response({"channels": 1})