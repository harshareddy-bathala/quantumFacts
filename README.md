# QuantumFacts - Automated YouTube Shorts Generator 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Open Source ](https://img.shields.io/badge/Open%%20Source-%%E2%%9D%%A4-red.svg)](https://github.com)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com)

> **Made with  Open Source** - A fully automated content pipeline that generates viral YouTube Shorts from interesting facts. This "set-it-and-forget-it" system handles everything from content sourcing to final video upload—completely free of cost!

##  Features

- ** Fully Automated**: No manual intervention required
- ** 100%% Free**: Uses only free-tier APIs and open-source tools
- ** High Quality**: Professional voiceovers and dynamic subtitles
- ** Algorithm-Optimized**: AI-generated titles, descriptions, and hashtags
- ** Continuous Production**: Generate videos on schedule or on-demand
- ** Smart Asset Management**: Automatic video and music selection

##  What It Does

Automatically generates complete YouTube Shorts with:

-  AI-powered engaging scripts
-  Professional text-to-speech narration
-  Dynamic word-by-word captions perfectly synced
-  Relevant HD background videos
-  Optional background music
-  Auto-upload to YouTube with optimized metadata

**One command. Complete video. Zero manual work.**

##  Technology Stack

### Core Technologies

- **Python 3.9+**: Main orchestration language
- **FFmpeg**: Video processing and assembly
- **Microsoft Edge TTS**: High-quality text-to-speech with natural voices
- **pysubs2**: Advanced subtitle generation

### APIs & Services (All Free Tier)

- **API-Ninjas**: Random interesting facts (50K requests/month)
- **OpenRouter**: Free LLM access with Mistral-7B
- **Pexels**: Royalty-free stock videos (200/hour)
- **Pixabay**: Alternative stock videos (5K/day)
- **YouTube Data API v3**: Automated video uploads

##  Prerequisites

1. **Python 3.9 or higher**
2. **FFmpeg** installed and in PATH
3. **API Keys** (all free):
   - API-Ninjas account
   - OpenRouter account
   - Pexels account
   - Pixabay account (optional)
   - Google Cloud Console (YouTube API)

##  Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/harshareddy-bathala/quantumFacts.git
cd quantumFacts
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Install FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### 4. Set Up API Keys

See **[SETUP.md](SETUP.md)** for detailed instructions on obtaining all API keys.

Quick setup:
```bash
copy .env.example .env
# Edit .env with your API keys
```

### 5. Generate Your First Video!

```bash
cd src
python -m viral_shorts.main
```

Your video will be in `src/output/[timestamp]/[timestamp].mp4` 

##  Usage

### Generate a Single Video

```bash
cd src
python -m viral_shorts.main
```

### Generate and Auto-Publish

Set in `.env`:
```bash
AUTO_PUBLISH=true
```

### Batch Generation

```python
from viral_shorts.main import ViralShortsGenerator

generator = ViralShortsGenerator()

# Generate 5 videos
for i in range(5):
    print(f"\nGenerating video {i+1}/5...")
    video_info = generator.generate_video()
    if video_info:
        print(f"Success! Video: {video_info['title']}")
```

##  Project Structure

```
quantumFacts/
 src/
    viral_shorts/
        main.py              # Main orchestration
        config.py            # Configuration
        content_sourcing/    # Fact fetching
        scripting/           # AI script generation
        narration/           # TTS integration
        video_assembly/      # Video creation
        publishing/          # YouTube upload
        utils/               # Utilities
 tests/                       # Unit tests
 requirements.txt             # Dependencies
 .env.example                # Environment template
 SETUP.md                    # Setup guide
 CONTRIBUTING.md             # Contribution guidelines
 README.md                   # This file
```

##  Video Generation Pipeline

1. **Fetch Fact**: Get random interesting fact from API-Ninjas
2. **Generate Script**: Use AI to create engaging script
3. **Create Narration**: Generate voiceover with Microsoft Edge TTS
4. **Find Video**: Search and download relevant stock footage
5. **Assemble Video**: Combine all elements with FFmpeg
6. **Add Subtitles**: Create word-by-word animated captions
7. **Upload**: Optionally publish to YouTube with metadata

##  Configuration

Edit `.env` file to customize:

```bash
# Video Settings
VIDEO_WIDTH=1080
VIDEO_HEIGHT=1920
VIDEO_FPS=30
VIDEO_DURATION_MAX=60

# Audio Settings
BACKGROUND_MUSIC_VOLUME=0.2
VOICE_VOLUME=1.0

# Publishing Settings
YOUTUBE_CATEGORY_ID=28          # Science & Technology
YOUTUBE_PRIVACY_STATUS=public
AUTO_PUBLISH=false
```

##  Customization

### Change Voice

Edit `src/viral_shorts/narration/tts.py`:

```python
# Available voices:
voice = "en-US-ChristopherNeural"  # Energetic male (current)
# voice = "en-US-GuyNeural"         # Professional male
# voice = "en-US-JennyNeural"       # Friendly female
# voice = "en-US-AriaNeural"        # Warm female
```

### Modify Caption Style

Edit `src/viral_shorts/config.py`:

```python
SUBTITLE_FONT = 'Arial'
SUBTITLE_FONT_SIZE = 24
SUBTITLE_COLOR = '&H00FFFF&'    # Yellow
SUBTITLE_POSITION = 2           # Bottom-center
SUBTITLE_MARGIN_V = 150
```

##  Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# With coverage
pytest --cov=viral_shorts tests/
```

##  Troubleshooting

### Common Issues

**FFmpeg not found:**
- Verify installation: `ffmpeg -version`
- Add to PATH if needed

**API Key errors:**
- Verify keys in `.env` file
- Check API quotas on dashboards
- Ensure no extra spaces in `.env`

**Video download fails:**
- System automatically retries 3 times
- Falls back to alternative videos
- Check internet connection

**YouTube upload fails:**
- Verify OAuth credentials
- Check `client_secrets.json` exists
- Re-authenticate if needed

### Debug Mode

```bash
# In .env
LOG_LEVEL=DEBUG
```

##  Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- [API-Ninjas](https://api-ninjas.com/) - Facts API
- [OpenRouter](https://openrouter.ai/) - AI model access
- [Pexels](https://www.pexels.com/) - Stock videos
- [Pixabay](https://pixabay.com/) - Stock videos
- [Microsoft Edge TTS](https://github.com/rany2/edge-tts) - Text-to-speech
- [FFmpeg](https://ffmpeg.org/) - Video processing
- [pysubs2](https://github.com/tkarabela/pysubs2) - Subtitle generation

##  Disclaimer

- Ensure you comply with YouTube's Terms of Service
- Verify content rights and licensing
- Monitor API usage to stay within free tiers
- This tool is for educational purposes
- Always review generated content before publishing

##  Roadmap

- [ ] Web dashboard for monitoring
- [ ] Multiple voice options
- [ ] Custom subtitle animations
- [ ] A/B testing for titles
- [ ] Analytics integration
- [ ] Multi-language support
- [ ] Automated thumbnail creation

---

<div align="center">

**Made with  Open Source**

*Built for creators, by creators. Free forever.*

[ Star this repo](https://github.com/harshareddy-bathala/quantumFacts) | [ Report Bug](https://github.com/harshareddy-bathala/quantumFacts/issues) | [ Request Feature](https://github.com/harshareddy-bathala/quantumFacts/issues)

</div>
