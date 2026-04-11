from bot.logging_config import get_logger

logger = get_logger(__name__)


def format_response(data: dict) -> str:
    lines: list[str] = []
    lines.append("🎵 <b>Audio processing result</b>")
    lines.append("")

    filename = data.get("filename")
    if filename:
        lines.append(f"📄 <b>File:</b> <code>{filename}</code>")

    duration = data.get("duration_seconds")
    if duration is not None:
        minutes, seconds = divmod(int(duration), 60)
        lines.append(f"⏱️ <b>Duration:</b> {minutes}m {seconds}s")

    lang = data.get("language")
    if lang:
        lines.append(f"🌍 <b>Language:</b> {lang}")

    confidence = data.get("confidence")
    if confidence is not None:
        confidence_pct = (
            confidence * 100
            if isinstance(confidence, float) and confidence <= 1
            else confidence
        )
        lines.append(f"✅ <b>Confidence:</b> {confidence_pct:.0f}%")

    sample_rate = data.get("sample_rate_hz")
    if sample_rate is not None:
        lines.append(f"🔊 <b>Sample rate:</b> {sample_rate} Hz")

    bitrate = data.get("bitrate_kbps")
    if bitrate is not None:
        lines.append(f"📊 <b>Bitrate:</b> {bitrate} kbps")

    channels = data.get("channels")
    if channels is not None:
        channel_info = (
            "stereo"
            if channels == 2
            else "mono" if channels == 1 else f"{channels} channels"
        )
        lines.append(f"🎧 <b>Channels:</b> {channel_info}")

    transcription = data.get("transcription")
    if transcription:
        lines.append("")
        lines.append("📝 <b>Transcription:</b>")
        lines.append(f"<code>{transcription}</code>")

    return "\n".join(lines)
