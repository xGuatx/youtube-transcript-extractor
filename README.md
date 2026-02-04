# YouTube Video Tools

Python tools to extract YouTube video segments and transcribe audio using Whisper (OpenAI).

## Features

### 1. Web Interface - Video Segment Extraction
- Cut portions of YouTube videos (start/end timestamps)
- Download only the desired segment
- Support for age-restricted videos (via cookies)

### 2. CLI - Audio Transcription
- Download audio from YouTube videos
- Transcribe to text with Whisper (NVIDIA GPU supported)
- Save output to `transcription.txt`

## Prerequisites

- Python 3.8+
- ffmpeg
- (Optional) NVIDIA GPU + CUDA for accelerated Whisper
- (Optional) Docker with nvidia-container-toolkit

## Installation

### Local

```bash
pip install -r requirements.txt
```

### Docker (with NVIDIA GPU)

```bash
docker compose up -d
```

## Usage

### Web Interface (video extraction)

```bash
python app.py
```

Access: `http://localhost:5000`

- Enter the YouTube URL
- Set timestamps (start/end in seconds)
- Download the extracted segment

### Command Line (transcription)

```bash
python youtube_transcriber.py
```

Follow the interactive prompts to enter the URL.

### Docker

```bash
# With NVIDIA GPU
docker compose up -d

# Web access
http://localhost:5000
```

## Cookies for Age-Restricted Videos

For videos requiring authentication:

1. Install a browser extension (e.g., "Get cookies.txt")
2. Log in to YouTube
3. Export cookies to `cookies.txt`
4. Place the file in the project root

**Security:** Never commit `cookies.txt`!

## Generated Files

- `downloads/` - Extracted video segments
- `transcription.txt` - Audio transcriptions

## GPU Configuration

The docker-compose includes NVIDIA GPU mapping:

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

Make sure you have installed:
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

## Troubleshooting

**"Video unavailable" or age restriction:**
- Provide a valid `cookies.txt`

**Dependency error:**
```bash
pip install -r requirements.txt
```

**GPU not detected in Docker:**
```bash
# Check installation
nvidia-smi
docker run --rm --gpus all nvidia/cuda:12.1-base nvidia-smi
```

**Port already in use:**
- Change the port in `docker-compose.yml`

## License

MIT - Respect YouTube's Terms of Service.
