# ⚡ VortexDL

> A powerful, extensible video & audio downloader — yt-dlp supercharged with a clean API, smart presets, and an optional web UI.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Usage](#cli-usage)
- [Web UI](#web-ui)
- [Configuration](#configuration)
- [Supported Sites](#supported-sites)
- [Architecture](#architecture)
- [Development](#development)
- [License](#license)

---

## Features

- 🎬 **Video + Audio download** — MP4, MKV, WEBM, MP3, FLAC, AAC, OPUS
- 📋 **Playlist & channel support** — bulk download with smart filtering
- 🎯 **Format selection** — by quality, codec, filesize, or custom selectors
- 🔐 **Cookie & auth support** — browser cookie extraction, netrc, custom headers
- 🧩 **Extractor plugins** — drop-in `.py` files in `extractors/` to add new sites
- 📊 **Rich progress UI** — speed, ETA, size, concurrent downloads
- 🔁 **Retry & resume** — automatic retry with exponential backoff, partial file resume
- ✂️ **Post-processing** — FFmpeg merge, thumbnail embed, metadata tagging, SponsorBlock
- 🌐 **Web UI** — browser-based interface with queue management
- ⚙️ **Config profiles** — YAML-based presets per site or use case
- 📁 **Smart output templates** — dynamic filename generation with metadata tokens

---

## Installation

### From PyPI

```bash
pip install vortexdl
```

### From source

```bash
git clone https://github.com/you/vortexdl
cd vortexdl
pip install -e ".[dev]"
```

### Requirements

| Dependency | Version | Purpose |
|-----------|---------|---------|
| Python | ≥ 3.10 | Runtime |
| yt-dlp | ≥ 2024.1 | Core extraction engine |
| rich | ≥ 13.0 | Terminal UI |
| click | ≥ 8.1 | CLI framework |
| PyYAML | ≥ 6.0 | Config parsing |
| aiohttp | ≥ 3.9 | Async HTTP |
| ffmpeg | system | Post-processing |

Install FFmpeg:
```bash
# Ubuntu / Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
winget install ffmpeg
```

---

## Quick Start

```bash
# Download best quality video
vortexdl https://youtube.com/watch?v=dQw4w9WgXcQ

# Audio only (best quality MP3)
vortexdl -x --audio-format mp3 https://youtube.com/watch?v=dQw4w9WgXcQ

# Download 1080p with subtitles
vortexdl -f "bestvideo[height=1080]+bestaudio" --subs https://youtube.com/watch?v=...

# Batch from file
vortexdl --batch urls.txt

# Start web UI on localhost:8080
vortexdl serve --port 8080
```

---

## CLI Usage

```
Usage: vortexdl [OPTIONS] [URLS]...

Options:
  -f, --format TEXT          Format selector (e.g. "bestvideo+bestaudio")
  -o, --output TEXT          Output template (default: %(title)s.%(ext)s)
  -x, --extract-audio        Extract audio only
      --audio-format TEXT    Audio format: mp3|aac|flac|opus|m4a [mp3]
      --audio-quality TEXT   Audio quality 0(best)-9(worst) or bitrate [0]
  -p, --playlist             Download full playlist
      --playlist-start INT   Start index for playlist [1]
      --playlist-end INT     End index for playlist
      --playlist-filter TEXT Filter playlist items by title regex
  -r, --rate-limit TEXT      Max download rate (e.g. 500K, 2M)
  -R, --retries INT          Number of retries [10]
      --concurrent INT       Concurrent fragment downloads [4]
  -c, --continue             Resume partial downloads
      --no-overwrite         Skip if file already exists
      --cookies TEXT         Path to Netscape cookies file
      --cookies-from TEXT    Browser to extract cookies from
      --proxy TEXT           Proxy URL
      --subs                 Download subtitles
      --sub-langs TEXT       Subtitle languages (e.g. "en,es")
      --embed-subs           Embed subtitles in video
      --embed-thumbnail      Embed thumbnail in file
      --embed-metadata       Write metadata to file
      --sponsorblock         Skip sponsored segments (YouTube)
      --batch TEXT           File with list of URLs
      --config TEXT          Path to config file
      --profile TEXT         Config profile to use
  -q, --quiet                Suppress output
  -v, --verbose              Verbose output
      --dry-run              Show what would be downloaded without downloading
      --version              Show version and exit
  -h, --help                 Show this help message
```

### Format Selectors

VortexDL uses yt-dlp's format selection syntax:

| Selector | Description |
|----------|-------------|
| `best` | Best single file (video+audio) |
| `bestvideo+bestaudio` | Best video merged with best audio |
| `bestvideo[height<=1080]+bestaudio` | Max 1080p video + best audio |
| `bestvideo[ext=mp4]+bestaudio[ext=m4a]` | MP4/M4A only |
| `worst` | Smallest file |
| `bv*[fps>30]+ba` | 60fps+ video + any audio |

### Output Templates

Tokens available in `-o` templates:

| Token | Description |
|-------|-------------|
| `%(title)s` | Video title |
| `%(id)s` | Video ID |
| `%(uploader)s` | Channel/uploader name |
| `%(upload_date)s` | Upload date (YYYYMMDD) |
| `%(ext)s` | File extension |
| `%(resolution)s` | Video resolution |
| `%(playlist_title)s` | Playlist title |
| `%(playlist_index)s` | Index in playlist |
| `%(duration)s` | Duration in seconds |

Example:
```bash
vortexdl -o "Downloads/%(uploader)s/%(upload_date)s - %(title)s.%(ext)s" URL
```

---

## Web UI

Start the web interface:
```bash
vortexdl serve --port 8080 --host 0.0.0.0
```

Then open `http://localhost:8080` in your browser.

Features:
- Paste URLs or drag & drop
- Live download queue with progress bars
- Format picker
- Output directory browser
- Download history
- Settings panel

---

## Configuration

VortexDL looks for config files in this order:

1. `--config` flag path
2. `./vortexdl.yaml`
3. `~/.config/vortexdl/config.yaml`
4. `~/.vortexdl.yaml`

### Example `vortexdl.yaml`

```yaml
# Default settings
defaults:
  format: "bestvideo[height<=1080]+bestaudio/best"
  output: "~/Downloads/%(uploader)s/%(title)s.%(ext)s"
  retries: 10
  concurrent: 4
  embed_metadata: true
  embed_thumbnail: true

# Named profiles — activate with --profile NAME
profiles:
  audio:
    extract_audio: true
    audio_format: mp3
    audio_quality: "0"
    output: "~/Music/%(uploader)s/%(title)s.%(ext)s"

  4k:
    format: "bestvideo[height<=2160]+bestaudio/best"
    output: "~/Videos/4K/%(title)s.%(ext)s"

  archive:
    output: "~/Archive/%(uploader)s/%(upload_date)s/%(title)s [%(id)s].%(ext)s"
    write_info_json: true
    write_thumbnail: true
    no_overwrite: true

# Site-specific overrides
sites:
  youtube.com:
    sponsorblock: true
    sponsorblock_categories: [sponsor, intro, outro, selfpromo]

  twitch.tv:
    format: best
    live_from_start: true
```

---

## Supported Sites

VortexDL supports **all sites yt-dlp supports** (1800+), plus custom extractors via plugins.

Popular examples:

- YouTube (videos, Shorts, playlists, channels, live streams)
- Twitter / X
- Instagram (posts, reels, stories)
- TikTok
- Reddit
- Twitch (VODs, clips, live)
- Vimeo
- Dailymotion
- SoundCloud
- Bandcamp
- Facebook
- Bilibili
- NicoNico
- And 1800+ more via yt-dlp

### Writing a Custom Extractor

Create `my_site.py` in `~/.config/vortexdl/extractors/`:

```python
from vortexdl.extractors.base import BaseExtractor

class MySiteExtractor(BaseExtractor):
    SITE_NAME = "mysite"
    URL_PATTERN = r"https?://mysite\.com/video/(?P<id>[A-Za-z0-9_-]+)"

    def extract(self, url: str) -> dict:
        video_id = self.match_id(url)
        # ... fetch and return info dict
        return {
            "id": video_id,
            "title": "...",
            "formats": [...],
        }
```

---

## Architecture

```
VortexDL
├── CLI Layer (click)           ← User-facing commands
├── Web Layer (aiohttp)         ← Browser UI + REST API
├── Core
│   ├── Downloader              ← Orchestrates download jobs
│   ├── FormatSelector          ← Parses & resolves format strings
│   ├── Merger                  ← FFmpeg wrapper for mux/convert
│   └── JobQueue                ← Concurrent job management
├── Extractors
│   ├── YouTubeExtractor        ← YouTube-specific logic
│   ├── GenericExtractor        ← yt-dlp fallback
│   └── PluginLoader            ← Loads user extractor plugins
├── PostProcessors
│   ├── FFmpegPP                ← Merge, convert, compress
│   ├── MetadataPP              ← ID3/Matroska tag writer
│   ├── ThumbnailPP             ← Embed cover art
│   └── SponsorBlockPP          ← Chapter/segment removal
└── Utils
    ├── Logger                  ← Rich-based logging
    ├── Progress                ← Live progress bars
    ├── Config                  ← YAML config loader
    └── Sanitizer               ← Filename cleaning
```

---

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check vortexdl/
mypy vortexdl/

# Format
black vortexdl/ tests/
```

### Running tests

```bash
pytest tests/                         # All tests
pytest tests/test_downloader.py -v   # Specific module
pytest -k "test_format_selector"     # Match test name
pytest --cov=vortexdl                # With coverage
```

---

## License

MIT License — see [LICENSE](LICENSE).

---

*VortexDL is not affiliated with YouTube or any other platform.*
