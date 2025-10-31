# Complete Setup Guide for QuantumFacts

This guide will walk you through setting up QuantumFacts from scratch, including all API keys and dependencies.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Python Setup](#python-setup)
3. [FFmpeg Installation](#ffmpeg-installation)
4. [Project Installation](#project-installation)
5. [API Keys Setup](#api-keys-setup)
6. [First Video Generation](#first-video-generation)
7. [YouTube Upload Setup (Optional)](#youtube-upload-setup-optional)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for dependencies + space for generated videos
- **Internet**: Stable connection for API calls and video downloads

---

## Python Setup

### Check if Python is Installed

```bash
python --version
# or
python3 --version
```

Should show Python 3.8 or higher.

### Install Python (if needed)

**Windows**:
1. Download from [python.org/downloads](https://www.python.org/downloads/)
2. Run installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"

**macOS**:
```bash
# Using Homebrew
brew install python3
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

## FFmpeg Installation

FFmpeg is required for video processing.

### Windows

**Method 1: Using Chocolatey (Recommended)**
```powershell
# Install Chocolatey first (if not installed)
# Visit: chocolatey.org/install

# Then install FFmpeg
choco install ffmpeg
```

**Method 2: Manual Installation**
1. Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Choose "Windows builds from gyan.dev"
3. Download "ffmpeg-release-essentials.zip"
4. Extract to `C:\ffmpeg`
5. Add to PATH:
   - Open "Environment Variables"
   - Edit "Path" in System variables
   - Add `C:\ffmpeg\bin`
   - Click OK

**Verify**:
```powershell
ffmpeg -version
```

### macOS

```bash
# Using Homebrew
brew install ffmpeg
```

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

**Verify**:
```bash
ffmpeg -version
```

---

## Project Installation

### 1. Clone Repository

```bash
# Navigate to where you want the project
cd ~/projects  # or C:\Users\YourName\projects on Windows

# Clone repository
git clone https://github.com/yourusername/QuantumFacts.git
cd QuantumFacts
```

### 2. Create Virtual Environment

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (CMD)**:
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - API calls
- `python-dotenv` - Environment variables
- `edge-tts` - Text-to-speech
- `pysubs2` - Subtitle generation
- `google-api-python-client` - YouTube API
- And more...

---

## API Keys Setup

You need 4 API keys (all have free tiers). Follow each section carefully.

### 1. API-Ninjas (Facts API)

**What it does**: Provides interesting random facts

**Steps**:
1. Go to [api-ninjas.com](https://api-ninjas.com/)
2. Click "Sign Up" in top right
3. Enter email and create password
4. Verify your email (check spam folder)
5. Log in → Go to "My Account"
6. You'll see your API Key
7. Copy the key

**Add to .env**:
```
API_NINJAS_KEY=your-actual-key-here
```

**Free Tier**: 50,000 requests/month (more than enough!)

---

### 2. OpenRouter (AI Script Generation)

**What it does**: Uses AI to create engaging scripts from facts

**Steps**:
1. Go to [openrouter.ai](https://openrouter.ai/)
2. Click "Sign In" → Choose "Sign in with Google" or "GitHub"
3. Authorize the app
4. Click your profile icon → "Keys"
5. Click "Create Key"
6. Give it a name (e.g., "QuantumFacts")
7. Copy the key (starts with `sk-or-v1-...`)

**Add to .env**:
```
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

**Free Tier**: Several free models available
- We use `mistralai/mistral-7b-instruct:free`
- No credit card required

---

### 3. Pexels (Video API)

**What it does**: Provides free high-quality stock videos

**Steps**:
1. Go to [pexels.com/api](https://www.pexels.com/api/)
2. Click "Get Started"
3. Sign up with email or Google
4. Confirm your email
5. Go to "Your API Key" page
6. Copy your API Key

**Add to .env**:
```
PEXELS_API_KEY=your-actual-key-here
```

**Free Tier**: 200 requests/hour

---

### 4. Pixabay (Video API)

**What it does**: Additional source for royalty-free videos

**Steps**:
1. Go to [pixabay.com](https://pixabay.com/)
2. Sign up for free account
3. Go to [pixabay.com/api/docs](https://pixabay.com/api/docs/)
4. Scroll down to "API Key"
5. Copy your key

**Add to .env**:
```
PIXABAY_API_KEY=your-actual-key-here
```

**Free Tier**: 5,000 requests/day

---

### Create Your .env File

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` with your favorite text editor:
```bash
# Windows
notepad .env

# macOS
open -e .env

# Linux
nano .env
```

3. Replace all placeholder values:
```env
API_NINJAS_KEY=your-api-ninjas-key-here
OPENROUTER_API_KEY=your-openrouter-api-key-here
PEXELS_API_KEY=your-pexels-api-key-here
PIXABAY_API_KEY=your-pixabay-api-key-here
```

4. Save the file

---

## First Video Generation

### Test Your Setup

```bash
# Run setup check
python setup_check.py
```

This will verify:
- ✅ Python version
- ✅ FFmpeg installation
- ✅ All required packages
- ✅ API keys configured

### Generate Your First Video!

```bash
cd src
python -m viral_shorts.main
```

**What happens**:
1. Fetches a random interesting fact
2. Generates engaging script with AI
3. Creates narration with text-to-speech
4. Finds and downloads background video
5. Adds animated captions
6. Saves final video

**Output location**: `src/output/YYYYMMDD_HHMMSS/YYYYMMDD_HHMMSS.mp4`

**Duration**: Takes 2-5 minutes depending on internet speed.

---

## YouTube Upload Setup (Optional)

If you want automatic YouTube uploads:

### 1. Create Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "QuantumFacts" → Create
4. Wait for project creation

### 2. Enable YouTube Data API v3

1. In Google Cloud Console, search for "YouTube Data API v3"
2. Click on it → Click "Enable"
3. Wait for it to enable

### 3. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. If prompted, configure consent screen:
   - User Type: "External"
   - App name: "QuantumFacts"
   - User support email: Your email
   - Developer contact: Your email
   - Save and Continue (skip scopes)
   - Add yourself as test user
4. Back to "Create OAuth 2.0 Client ID":
   - Application type: "Desktop app"
   - Name: "QuantumFacts Desktop"
   - Create
5. Download JSON file

### 4. Set Up Credentials

1. Rename downloaded file to `client_secrets.json`
2. Move to project root (same folder as README.md)
3. In `.env`, set:
   ```
   AUTO_PUBLISH=true
   ```

### 5. First Upload

```bash
cd src
python -m viral_shorts.main
```

- Browser will open automatically
- Sign in to your YouTube channel
- Click "Allow" to grant permissions
- Video will upload automatically

**Note**: You'll only need to authorize once. Token is saved for future uploads.

---

## Troubleshooting

### "FFmpeg not found"

**Solution**:
1. Verify installation: `ffmpeg -version`
2. If not found, reinstall FFmpeg
3. Make sure it's in system PATH
4. Restart terminal after PATH changes

### "ModuleNotFoundError"

**Solution**:
```bash
# Make sure virtual environment is activated
# Look for (venv) in terminal

# Reinstall dependencies
pip install -r requirements.txt
```

### "API Key Invalid" or "401 Unauthorized"

**Solution**:
1. Double-check API key in `.env`
2. Make sure no extra spaces
3. Make sure you copied the entire key
4. Verify key is active on provider's website

### Video Download Fails

**Possible causes**:
- Slow internet connection
- Rate limit exceeded
- Video region-restricted

**Solutions**:
- System automatically retries
- Try again in a few minutes
- Check internet connection

### "Permission Denied" on Linux/Mac

**Solution**:
```bash
# Make scripts executable
chmod +x setup.sh
chmod +x *.sh
```

### YouTube Upload Errors

**Common issues**:
1. **"Client secrets not found"**:
   - Make sure `client_secrets.json` is in project root
   - Check filename spelling

2. **"Quota exceeded"**:
   - YouTube API has daily upload limits
   - Wait 24 hours or request quota increase

3. **"Invalid grant"**:
   - Delete `oauth_token.json`
   - Run again to re-authorize

### Virtual Environment Issues (Windows)

**PowerShell execution policy error**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Still Having Issues?

1. Check the full error message
2. Search GitHub issues
3. Open a new issue with:
   - Your operating system
   - Python version
   - Full error message
   - Steps to reproduce

---

## Next Steps

### Customize Your Videos

1. **Change voice**: Edit `src/viral_shorts/narration/tts.py`
2. **Modify captions**: Edit `src/viral_shorts/config.py`
3. **Add music**: Put MP3 files in `src/assets/music/`

### Advanced Configuration

Check `.env` for more options:
- Video dimensions
- Frame rate
- Audio volumes
- Publishing settings

### Run Tests

```bash
pytest tests/ -v
```

### Set Up Automation

Create a scheduled task/cron job to generate videos automatically!

**Windows Task Scheduler**:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily/weekly)
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `-m viral_shorts.main`
7. Start in: `C:\path\to\QuantumFacts\src`

**Linux/Mac Cron**:
```bash
crontab -e

# Add line (runs daily at 10 AM):
0 10 * * * cd /path/to/QuantumFacts/src && /path/to/venv/bin/python -m viral_shorts.main
```

---

## Congratulations! 🎉

You're all set up! Generate amazing YouTube Shorts effortlessly.

**Need help?** Open an issue on GitHub or check the main README.md

---

Made with ❤️ Open Source
