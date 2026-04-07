from bot.services.mock_data import get_mock_response


class TestGetMockResponse:
    def test_returns_dict(self) -> None:
        assert isinstance(get_mock_response(), dict)

    def test_has_expected_keys(self) -> None:
        result = get_mock_response()
        expected_keys = {
            "status", "filename", "duration_seconds", "language",
            "confidence", "transcription", "sample_rate_hz",
            "bitrate_kbps", "channels",
        }
        assert set(result.keys()) == expected_keys

    def test_status_is_ok(self) -> None:
        assert get_mock_response()["status"] == "ok"

    def test_filename_reflects_input(self) -> None:
        assert get_mock_response("song.mp3")["filename"] == "song.mp3"

    def test_confidence_between_0_and_1(self) -> None:
        assert 0.0 <= get_mock_response()["confidence"] <= 1.0

    def test_transcription_is_non_empty_string(self) -> None:
        assert isinstance(get_mock_response()["transcription"], str)
        assert len(get_mock_response()["transcription"]) > 0

    def test_duration_is_positive(self) -> None:
        assert get_mock_response()["duration_seconds"] > 0