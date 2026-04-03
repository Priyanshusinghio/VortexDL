# Changelog

All notable changes to VortexDL are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — Initial Release

### Added
- Full CLI via Click with all major yt-dlp options exposed
- YAML-based layered config (defaults → profiles → site overrides → CLI flags)
- `vortexdl serve` — aiohttp-powered web UI with REST + SSE API
- Live progress bars via Rich (speed, ETA, concurrent fragments)
- Audio extraction via FFmpeg post-processor (MP3, FLAC, AAC, Opus, M4A, WAV)
- SponsorBlock integration for YouTube
- Subtitle download + embedding
- Thumbnail embedding (ID3 APIC, MP4 covr)
- Metadata tagging via mutagen (MP3, M4A, FLAC, OGG)
- Cookie support: file and live browser extraction
- Playlist download with start/end/filter
- Extractor plugin system with `BaseExtractor` base class
- Auto-discovery of plugins from `~/.config/vortexdl/extractors/`
- `vortexdl info` — format table without downloading
- Cross-platform filename sanitizer
- Comprehensive test suite (pytest)
- Full documentation: CLI reference, config guide, plugin guide, web API reference
