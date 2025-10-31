# QuantumFacts - Automated YouTube Shorts Generator 🎬# 🎬 Automated Viral YouTube Shorts Generator



[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)![License](https://img.shields.io/badge/license-MIT-green.svg)

[![Open Source ❤️](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red.svg)](https://github.com)![Status](https://img.shields.io/badge/status-active-success.svg)



> **Made with ❤️ Open Source** - An intelligent, fully-automated system that generates engaging YouTube Shorts about interesting facts.A fully automated content pipeline that generates viral YouTube Shorts from interesting facts. This "set-it-and-forget-it" system handles everything from content sourcing to final video upload—completely free of cost!



## ✨ What It Does## 🌟 Features



Automatically generates complete YouTube Shorts with:- **🤖 Fully Automated**: No manual intervention required

- 🤖 AI-powered engaging scripts- **💰 100% Free**: Uses only free-tier APIs and open-source tools

- 🎙️ Professional text-to-speech narration  - **📹 High Quality**: Professional voiceovers and dynamic subtitles

- 🎨 Dynamic word-by-word captions- **🎯 Algorithm-Optimized**: AI-generated titles, descriptions, and hashtags

- 🎬 Relevant background videos- **🔄 Continuous Production**: Generate videos on schedule or on-demand

- 📤 Optional auto-upload to YouTube- **📊 Smart Asset Management**: Automatic video and music selection



**One command. Complete video. Zero manual work.**## 🛠️ Technology Stack



## 🎥 Features### Core Technologies

- **Python 3.9+**: Main orchestration language

- **AI Script Generation**: Uses OpenRouter API (free) with Mistral-7B for natural, engaging narration- **FFmpeg**: Video processing and assembly

- **Professional Narration**: Microsoft Edge TTS with energetic, high-quality voices- **Google Colab**: Free GPU for TTS generation

- **Animated Captions**: Word-by-word subtitles perfectly synced with audio

- **Smart Video Selection**: Automatically finds and downloads relevant HD videos from Pexels/Pixabay### APIs & Services (All Free Tier)

- **YouTube Ready**: Portrait format (1080x1920), optimized for Shorts algorithm- **API-Ninjas**: Random interesting facts

- **Background Music**: Optional music mixing support- **OpenRouter**: Free LLM access (Meta Llama)

- **Auto Upload**: YouTube API integration for hands-free publishing- **Kyutai TTS**: High-quality text-to-speech

- **Retry Logic**: Robust error handling and automatic retries- **Pexels & Pixabay**: Royalty-free stock videos

- **YouTube Data API v3**: Automated video uploads

## 🚀 Quick Start- **YouTube Audio Library**: Copyright-safe music



### Prerequisites## 📋 Prerequisites



- Python 3.8+1. **Python 3.9 or higher**

- FFmpeg2. **FFmpeg** installed and in PATH

- API keys (all have free tiers)3. **API Keys** (all free):

   - API-Ninjas account

### Installation   - OpenRouter account

   - Pexels account

```bash   - Pixabay account (optional)

# 1. Clone repository   - Google Cloud Console (YouTube API)

git clone https://github.com/yourusername/QuantumFacts.git

cd QuantumFacts## 🚀 Quick Start



# 2. Create virtual environment### 1. Clone the Repository

python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate```bash

git clone https://github.com/yourusername/viral-shorts-generator.git

# 3. Install dependenciescd viral-shorts-generator

pip install -r requirements.txt```



# 4. Set up environment### 2. Install Dependencies

cp .env.example .env

# Edit .env with your API keys (see setup guide below)```bash

# Create virtual environment (recommended)

# 5. Generate your first video!python -m venv venv

cd src

python -m viral_shorts.main# Activate virtual environment

```# On Windows:

venv\Scripts\activate

Your video will be in `src/output/[timestamp]/[timestamp].mp4` 🎉# On Mac/Linux:

source venv/bin/activate

## 📋 Complete API Setup Guide

# Install packages

### 1️⃣ API-Ninjas (Facts API) - **FREE**pip install -r requirements.txt

```

Provides interesting random facts.

### 3. Install FFmpeg

1. Go to [api-ninjas.com](https://api-ninjas.com/)

2. Click "Sign Up" (free account)**Windows:**

3. Verify your email```bash

4. Go to "My Account" → Copy your API key# Using Chocolatey

5. Add to `.env`:choco install ffmpeg

   ```

   API_NINJAS_KEY=your-api-key-here# Or download from: https://ffmpeg.org/download.html

   ``````



**Free Tier**: 50,000 requests/month**Mac:**

```bash

---brew install ffmpeg

```

### 2️⃣ OpenRouter (AI Script Generation) - **FREE**

**Linux:**

Generates engaging scripts using AI models.```bash

sudo apt-get install ffmpeg

1. Go to [openrouter.ai](https://openrouter.ai/)```

2. Sign in with Google/GitHub

3. Go to "Keys" → "Create Key"### 4. Set Up API Keys

4. Copy the key (starts with `sk-or-v1-`)

5. Add to `.env`:1. Copy the example environment file:

   ```   ```bash

   OPENROUTER_API_KEY=your-api-key-here   copy .env.example .env

   ```   ```



**Free Tier**: Several free models available including Mistral-7B2. Get your API keys:



---   **API-Ninjas** (Facts):

   - Sign up at: https://api-ninjas.com/

### 3️⃣ Pexels (Video API) - **FREE**   - Get your API key from dashboard

   - Add to `.env`: `API_NINJAS_KEY=your_key_here`

High-quality stock video footage.

   **OpenRouter** (AI Scripts):

1. Go to [pexels.com/api](https://www.pexels.com/api/)   - Sign up at: https://openrouter.ai/

2. Click "Get Started" → Sign up   - Get API key from dashboard

3. Go to "Your API Key" → Copy key   - Add to `.env`: `OPENROUTER_API_KEY=your_key_here`

4. Add to `.env`:

   ```   **Pexels** (Stock Videos):

   PEXELS_API_KEY=your-api-key-here   - Sign up at: https://www.pexels.com/api/

   ```   - Get API key

   - Add to `.env`: `PEXELS_API_KEY=your_key_here`

**Free Tier**: 200 requests/hour

   **Pixabay** (Alternative Videos):

---   - Sign up at: https://pixabay.com/api/docs/

   - Get API key

### 4️⃣ Pixabay (Video API) - **FREE**   - Add to `.env`: `PIXABAY_API_KEY=your_key_here`



Additional source for royalty-free videos.   **YouTube Data API**:

   - Go to: https://console.cloud.google.com/

1. Go to [pixabay.com/api/docs](https://pixabay.com/api/docs/)   - Create a new project

2. Sign up for free account   - Enable "YouTube Data API v3"

3. Go to API section → Copy your key   - Create OAuth 2.0 credentials (Desktop app)

4. Add to `.env`:   - Download as `client_secrets.json` in project root

   ```

   PIXABAY_API_KEY=your-api-key-here### 5. Download Background Music

   ```

1. Go to: https://www.youtube.com/audiolibrary

**Free Tier**: 5,000 requests/day2. Download copyright-free music tracks

3. Place them in: `assets/music/`

---

### 6. Set Up Kyutai TTS (Google Colab)

### 5️⃣ YouTube Data API v3 (Optional - for auto-upload)

This project uses Kyutai TTS running on Google Colab for free GPU access:

Enables automatic video uploads to YouTube.

1. Open this Colab notebook: [Setup Guide](docs/colab_tts_setup.md)

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)2. Follow the setup instructions

2. Create new project (e.g., "QuantumFacts")3. Get your notebook URL

3. Enable "YouTube Data API v3":4. Add to `.env`: `COLAB_NOTEBOOK_URL=your_colab_url`

   - Search for it in API Library

   - Click "Enable"**Note**: For local development, the system will use placeholder TTS. See documentation for full Kyutai TTS setup.

4. Create OAuth 2.0 Credentials:

   - Go to "Credentials" → "Create Credentials"## 💻 Usage

   - Choose "OAuth 2.0 Client ID"

   - Application type: "Desktop app"### Generate a Single Video

   - Download JSON file

5. Rename file to `client_secrets.json````bash

6. Place in project root directorycd src

python -m viral_shorts.main

**First Run**: Browser will open for YouTube account authorization```



---### Test API Connections



### FFmpeg Installation```python

from viral_shorts.main import ViralShortsGenerator

**Windows**:

1. Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)generator = ViralShortsGenerator()

2. Extract to `C:\ffmpeg`generator.test_apis()

3. Add `C:\ffmpeg\bin` to system PATH```

4. Verify: `ffmpeg -version`

### Generate and Auto-Publish

**Linux**:

```bashSet in `.env`:

sudo apt update```bash

sudo apt install ffmpegAUTO_PUBLISH=true

``````



**Mac**:Or programmatically:

```bash```python

brew install ffmpeggenerator = ViralShortsGenerator()

```video_info = generator.generate_video(publish=True)

```

## ⚙️ Configuration

### Batch Generation

Customize settings in `.env`:

```python

```bashfrom viral_shorts.main import ViralShortsGenerator

# Video Settings

VIDEO_WIDTH=1080                # Portrait widthgenerator = ViralShortsGenerator()

VIDEO_HEIGHT=1920               # Portrait height

VIDEO_FPS=30                    # Frame rate# Generate 5 videos

VIDEO_DURATION_MAX=60           # Max duration in secondsfor i in range(5):

    print(f"\nGenerating video {i+1}/5...")

# Audio Settings    video_info = generator.generate_video()

BACKGROUND_MUSIC_VOLUME=0.2     # Music volume (0.0-1.0)    if video_info:

VOICE_VOLUME=1.0                # Voice volume        print(f"Success! Video: {video_info['title']}")

```

# Content Settings

FACTS_CATEGORY=random           # Fact category## 📁 Project Structure

VIDEO_LANGUAGE=en               # Language code

```

# Publishing Settingsviral-shorts-generator/

AUTO_PUBLISH=false              # Auto-upload to YouTube├── src/

YOUTUBE_PRIVACY_STATUS=public   # public, private, or unlisted│   └── viral_shorts/

YOUTUBE_CATEGORY_ID=28          # 28 = Science & Technology│       ├── __init__.py

```│       ├── main.py              # Main orchestration script

│       ├── config.py            # Configuration management

## 📁 Project Structure│       ├── content_sourcing/    # Fact fetching & parsing

│       ├── scripting/           # AI script generation

```│       ├── narration/           # TTS integration

QuantumFacts/│       ├── video_assembly/      # FFmpeg video creation

├── src/│       ├── publishing/          # YouTube upload

│   ├── viral_shorts/│       └── utils/               # Logger, storage, etc.

│   │   ├── content_sourcing/    # Fetch facts & extract keywords├── tests/                       # Unit tests

│   │   ├── scripting/           # AI script generation├── assets/

│   │   ├── narration/           # Text-to-speech (Edge TTS)│   └── music/                   # Background music files

│   │   ├── video_assembly/      # Video editing & captions├── output/                      # Generated videos

│   │   ├── publishing/          # YouTube upload├── temp/                        # Temporary files

│   │   ├── utils/               # Logging & storage├── requirements.txt             # Python dependencies

│   │   └── config.py            # Configuration settings├── pyproject.toml              # Project metadata

│   ├── output/                  # Generated videos├── .env.example                # Environment template

│   ├── assets/music/            # Background music files (optional)└── README.md                   # This file

│   └── temp/                    # Temporary files```

├── tests/                       # Unit tests

├── .env                         # Your API keys (DO NOT COMMIT)## 🎥 Video Generation Pipeline

├── .env.example                 # Template for .env

├── .gitignore                   # Git ignore rules1. **Fetch Fact**: Get random interesting fact from API-Ninjas

├── requirements.txt             # Python dependencies2. **Generate Script**: Use AI to create engaging script with title/hashtags

├── setup.bat                    # Windows setup script3. **Create Narration**: Generate voiceover with Kyutai TTS

├── setup.sh                     # Linux/Mac setup script4. **Find Video**: Search and download relevant stock footage

└── README.md                    # This file5. **Select Music**: Pick random background music

```6. **Assemble Video**: Combine all elements with FFmpeg

7. **Add Subtitles**: Create word-by-word animated captions

## 🎨 Customization8. **Upload**: Publish to YouTube with metadata



### Change Voice## ⚙️ Configuration



Edit `src/viral_shorts/narration/tts.py`:Edit `.env` file to customize:



```python```bash

# Available voices:# Video Settings

voice = "en-US-ChristopherNeural"  # Energetic male (current)VIDEO_WIDTH=1080

# voice = "en-US-GuyNeural"         # Professional maleVIDEO_HEIGHT=1920

# voice = "en-US-JennyNeural"       # Friendly femaleVIDEO_FPS=30

# voice = "en-US-AriaNeural"        # Warm femaleVIDEO_DURATION_MAX=60

```

# Audio Settings

### Modify Caption StyleBACKGROUND_MUSIC_VOLUME=0.2

VOICE_VOLUME=1.0

Edit `src/viral_shorts/config.py`:

# Publishing Settings

```pythonYOUTUBE_CATEGORY_ID=28          # Science & Technology

SUBTITLE_FONT = 'Arial'         # Font nameYOUTUBE_PRIVACY_STATUS=public   # public, private, or unlisted

SUBTITLE_FONT_SIZE = 24         # Font size (pixels)AUTO_PUBLISH=false

SUBTITLE_COLOR = '&H00FFFF&'    # Yellow in BGR format```

SUBTITLE_POSITION = 2           # 2=bottom-center, 5=top-center

SUBTITLE_MARGIN_V = 150         # Margin from bottom (pixels)## 🧪 Testing

```

Run unit tests:

### Add Background Music

```bash

1. Add `.mp3` files to `src/assets/music/`# Install test dependencies

2. System will randomly select one per videopip install pytest pytest-cov

3. Adjust volume in `.env`: `BACKGROUND_MUSIC_VOLUME=0.2`

# Run tests

## 🔧 Troubleshootingpytest tests/



### FFmpeg Not Found# With coverage

```bashpytest --cov=viral_shorts tests/

# Verify installation```

ffmpeg -version

## 📊 Monitoring & Logs

# If not found, add to PATH or reinstall

```Logs are saved to: `logs/viral_shorts.log`



### API Rate Limit ExceededView queue status:

- **API-Ninjas**: Wait 1 hour (50K/month limit)```python

- **Pexels**: Wait until next hour (200/hour limit)from viral_shorts.publishing.scheduler import VideoScheduler

- **Pixabay**: Generous limit (5K/day)

scheduler = VideoScheduler()

### Video Download Failsstats = scheduler.get_queue_stats()

- System automatically retries 3 times with exponential backoffprint(stats)

- Falls back to alternative videos if primary fails```

- Check internet connection

- Some videos may be region-restrictedStorage statistics:

```python

### ImportError or ModuleNotFoundErrorfrom viral_shorts.utils.storage import StorageManager

```bash

# Reinstall all dependenciesstorage = StorageManager()

pip install -r requirements.txt --force-reinstallstats = storage.get_storage_stats()

```print(stats)

```

### Caption Timing Issues

- Captions are synced based on audio duration## 🔧 Troubleshooting

- If issues persist, check Edge TTS installation:

  ```bash### Common Issues

  pip install --upgrade edge-tts

  ```**FFmpeg not found:**

```bash

## 📊 Usage Examples# Verify installation

ffmpeg -version

### Generate Single Video

```bash# Add to PATH if needed

cd src```

python -m viral_shorts.main

```**API Key errors:**

- Verify keys in `.env` file

### Run Tests- Check API quotas on respective dashboards

```bash- Ensure no extra spaces in `.env`

pytest tests/ -v

```**TTS not working:**

- Set up Google Colab notebook (see docs)

### Check Setup- Or use alternative TTS service

```bash- Fallback mode generates placeholder audio

python setup_check.py

```**YouTube upload fails:**

- Verify OAuth credentials

## 🤝 Contributing- Check `client_secrets.json` exists

- Re-authenticate if needed

Contributions are welcome! Here's how:

### Debug Mode

1. Fork the repository

2. Create a feature branchEnable detailed logging:

   ```bash```bash

   git checkout -b feature/AmazingFeature# In .env

   ```LOG_LEVEL=DEBUG

3. Commit your changes```

   ```bash

   git commit -m 'Add some AmazingFeature'## 🚀 Advanced Usage

   ```

4. Push to the branch### Scheduling Videos

   ```bash

   git push origin feature/AmazingFeature```python

   ```from viral_shorts.publishing.scheduler import VideoScheduler

5. Open a Pull Requestfrom datetime import datetime, timedelta



### Development Guidelinesscheduler = VideoScheduler()



- Follow PEP 8 style guide# Schedule for later

- Add tests for new featuresscheduler.add_to_queue(

- Update documentation    video_path=Path('output/video.mp4'),

- Keep commits atomic and well-described    title='My Video',

    description='Description',

## 📝 License    tags=['tag1', 'tag2'],

    scheduled_time=datetime.now() + timedelta(hours=2)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.)

```

## 🙏 Acknowledgments

### Custom Voice Settings

- [API-Ninjas](https://api-ninjas.com/) - Interesting facts API

- [OpenRouter](https://openrouter.ai/) - AI model access```python

- [Pexels](https://www.pexels.com/) - Free stock videosfrom viral_shorts.narration.voice_manager import VoiceManager

- [Pixabay](https://pixabay.com/) - Free stock videos

- [Microsoft Edge TTS](https://github.com/rany2/edge-tts) - High-quality text-to-speechvoice_mgr = VoiceManager()

- [FFmpeg](https://ffmpeg.org/) - Video processingvoice_mgr.set_voice('energetic')  # or 'calm', 'authoritative'

- [pysubs2](https://github.com/tkarabela/pysubs2) - Subtitle generation```



## 💡 Inspiration### Batch Scheduling



Built for content creators who want to automate their YouTube Shorts production while maintaining high quality. Perfect for:```python

- Educational channelsvideos = [...]  # List of video info dicts

- Fact channelsscheduler.schedule_batch(videos, interval_hours=3)

- Automated content pipelines```

- Learning AI/automation

## 📝 License

## ⭐ Support

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

If you find this project helpful:

- Give it a star ⭐## 🤝 Contributing

- Share it with others

- Consider contributingContributions are welcome! Please feel free to submit a Pull Request.

- Report issues or suggest features

1. Fork the project

## 🔮 Roadmap2. Create your feature branch (`git checkout -b feature/AmazingFeature`)

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)

- [ ] Multi-language support4. Push to the branch (`git push origin feature/AmazingFeature`)

- [ ] Custom fact sources5. Open a Pull Request

- [ ] Advanced caption animations

- [ ] Video templates## 📧 Support

- [ ] Batch video generation

- [ ] Analytics dashboardFor issues, questions, or suggestions:

- [ ] Scheduled publishing- Open an issue on GitHub

- Check existing issues and documentation

## 📞 Contact- Review troubleshooting guide above



Have questions or suggestions? Open an issue or start a discussion!## ⚠️ Disclaimer



---- Ensure you comply with YouTube's Terms of Service

- Verify content rights and licensing

<div align="center">- Monitor API usage to stay within free tiers

- This tool is for educational purposes

**Made with ❤️ Open Source**- Always review generated content before publishing



*Built for creators, by creators. Free forever.*## 🙏 Acknowledgments



[⭐ Star this repo](https://github.com/yourusername/QuantumFacts) | [🐛 Report Bug](https://github.com/yourusername/QuantumFacts/issues) | [💡 Request Feature](https://github.com/yourusername/QuantumFacts/issues)- API-Ninjas for fact data

- OpenRouter for free LLM access

</div>- Pexels & Pixabay for stock footage

- Kyutai for open-source TTS

---- YouTube for creator platform

- FFmpeg team for amazing tools

**⚠️ Important Note**: This project is for educational purposes. Ensure you comply with:

- YouTube's Terms of Service## 🗺️ Roadmap

- Content policies and guidelines

- Copyright and fair use laws- [ ] Web dashboard for monitoring

- API provider terms of service- [ ] Multiple voice options

- [ ] Custom subtitle styles

**Always verify** that your use case aligns with platform policies before automated publishing.- [ ] A/B testing for titles

- [ ] Analytics integration
- [ ] Multi-language support
- [ ] Video preview generation
- [ ] Automated thumbnail creation

---

**Made with ❤️ for creators who want to automate their content workflow**

⭐ Star this repo if you find it useful!
