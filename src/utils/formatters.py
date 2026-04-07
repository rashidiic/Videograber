from bot.logging_config import get_logger

logger = get_logger(__name__)


def format_response(data: dict) -> str:
    lines: list[str] = []
    lines.append("Audio processing result")
    lines.append("=" * 32)

    filename = data.get("filename")
    if filename:
        lines.append(f"File: {filename}")

    duration = data.get("duration_seconds")
    if duration is not None:
        minutes, seconds = divmod(int(duration), 60)
        lines.append(f"Duration: {minutes}m {seconds}s")

    lang = data.get("language")
    if lang:
        lines.append(f"Language: {lang}")

    confidence = data.get("confidence")
    if confidence is not None:
        lines.append(f"Confidence: {confidence:.0%}")

    sample_rate = data.get("sample_rate_hz")
    if sample_rate is not None:
        lines.append(f"Sample rate: {sample_rate} Hz")

    bitrate = data.get("bitrate_kbps")
    if bitrate is not None:
        lines.append(f"Bitrate: {bitrate} kbps")

    channels = data.get("channels")
    if channels is not None:
        lines.append(f"Channels: {channels} (stereo)" if channels == 2 else f"Channels: {channels}")

    transcription = data.get("transcription")
    if transcription:
        lines.append("")
        lines.append("Transcription:")
        lines.append(transcription)

    return "\n".join(lines)