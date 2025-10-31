# API Setup Guide

This guide will walk you through setting up all the required API keys for the Viral Shorts Generator.

## 1. API-Ninjas (Facts API)

**Purpose**: Fetch random interesting facts

**Setup Steps**:
1. Go to https://api-ninjas.com/
2. Click "Sign Up" (top right)
3. Create a free account
4. Go to "My Account" → "API Key"
5. Copy your API key
6. Add to `.env`: `API_NINJAS_KEY=your_key_here`

**Free Tier**: 50,000 requests/month

**Documentation**: https://api-ninjas.com/api/facts

---

## 2. OpenRouter (LLM API)

**Purpose**: Generate scripts, titles, and hashtags using AI

**Setup Steps**:
1. Go to https://openrouter.ai/
2. Click "Sign In" with Google/GitHub
3. Go to "Keys" section
4. Click "Create Key"
5. Copy your API key
6. Add to `.env`: `OPENROUTER_API_KEY=your_key_here`

**Free Models**:
- Meta Llama 3.1 8B (used by default)
- Google Gemma 7B
- Others in free tier

**Documentation**: https://openrouter.ai/docs

---

## 3. Pexels (Stock Videos)

**Purpose**: Download royalty-free vertical videos

**Setup Steps**:
1. Go to https://www.pexels.com/api/
2. Click "Get Started"
3. Fill in application details
4. API key is generated instantly
5. Copy your API key
6. Add to `.env`: `PEXELS_API_KEY=your_key_here`

**Free Tier**: 200 requests/hour

**License**: Free for commercial use

**Documentation**: https://www.pexels.com/api/documentation/

---

## 4. Pixabay (Alternative Videos)

**Purpose**: Additional source for stock videos

**Setup Steps**:
1. Go to https://pixabay.com/api/docs/
2. Click "Get Started"
3. Sign up for free account
4. API key shown in documentation
5. Copy your API key
6. Add to `.env`: `PIXABAY_API_KEY=your_key_here`

**Free Tier**: 5,000 requests/day

**License**: Free for commercial use

**Documentation**: https://pixabay.com/api/docs/

---

## 5. YouTube Data API v3

**Purpose**: Upload videos to YouTube automatically

**Setup Steps**:

### Step 1: Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Click "New Project"
3. Name it "Viral Shorts Generator"
4. Click "Create"

### Step 2: Enable YouTube API
1. In your project, go to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click on it and click "Enable"

### Step 3: Create OAuth Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: Viral Shorts Generator
   - User support email: your email
   - Developer contact: your email
   - Add scope: `../auth/youtube.upload`
   - Add test users: your email
4. Back to Create OAuth Client ID:
   - Application type: Desktop app
   - Name: Viral Shorts Generator
   - Click "Create"
5. Download the JSON file
6. Save it as `client_secrets.json` in project root

### Step 4: First Authentication
The first time you run the script, it will:
1. Open a browser window
2. Ask you to sign in with Google
3. Request permission to upload videos
4. Save credentials for future use

**Free Tier**: 10,000 quota units/day (enough for ~6 uploads)

**Documentation**: https://developers.google.com/youtube/v3

---

## Verification

Test all APIs:

```bash
cd src
python -c "from viral_shorts.main import ViralShortsGenerator; g = ViralShortsGenerator(); g.test_apis()"
```

You should see:
```
API Test Results:
  fact_api: ✓ PASS
  script_generator: ✓ PASS
  tts: ✓ PASS
  video_apis: {'pexels': True, 'pixabay': True}
  youtube: ✓ PASS
```

---

## Security Notes

⚠️ **IMPORTANT**:

1. **Never commit API keys** to version control
2. Keep `.env` file secure and private
3. Add `.env` to `.gitignore` (already done)
4. Rotate keys if accidentally exposed
5. Use environment variables in production

---

## Cost Monitoring

All APIs used are free tier, but monitor usage:

- **API-Ninjas**: Check dashboard for request count
- **OpenRouter**: Monitor credits in account
- **Pexels**: Rate limits are generous
- **Pixabay**: 5k/day should be plenty
- **YouTube**: Check quota in Google Cloud Console

---

## Troubleshooting

**401 Unauthorized**: Check API key is correct in `.env`

**403 Forbidden**: API might be disabled or quota exceeded

**Rate Limit**: Wait or use alternative API source

**Invalid Credentials**: Regenerate API key from provider

---

## Alternative Free Services

If you hit limits, consider:

**For Facts**:
- Random Facts API
- Useless Facts API
- Numbers API

**For Scripts**:
- Hugging Face Inference API
- Anthropic Claude (free tier)

**For Videos**:
- Unsplash (images only)
- Coverr (video clips)

**For TTS**:
- Google Cloud TTS (300 free chars/month)
- gTTS (Google Translate TTS - unlimited)

---

Need help? Check the main README or open an issue on GitHub.
