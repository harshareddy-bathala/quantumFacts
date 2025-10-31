# Video Generation Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                   AUTOMATED VIDEO GENERATION PIPELINE                │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────┐
    │  STEP 1: CONTENT SOURCING                                    │
    │  ────────────────────────                                    │
    │  ┌──────────────┐                                           │
    │  │ API-Ninjas   │ ──► Fetch random interesting fact         │
    │  │ Facts API    │                                           │
    │  └──────────────┘                                           │
    │         │                                                     │
    │         ▼                                                     │
    │  ┌──────────────┐                                           │
    │  │ FactParser   │ ──► Parse, validate, extract keywords     │
    │  └──────────────┘                                           │
    └──────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────┐
    │  STEP 2: SCRIPT GENERATION                                   │
    │  ─────────────────────────                                   │
    │  ┌──────────────┐                                           │
    │  │ OpenRouter   │ ──► Generate engaging script              │
    │  │ (Llama 3.1)  │     • Hook (attention grabber)            │
    │  └──────────────┘     • Main script (storytelling)          │
    │         │              • Call-to-action                      │
    │         ▼              • Title (SEO optimized)               │
    │  ┌──────────────┐     • Description                         │
    │  │   AI LLM     │     • Hashtags (trending)                │
    │  │  Processing  │                                           │
    │  └──────────────┘                                           │
    └──────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────┐
    │  STEP 3: VOICE NARRATION                                     │
    │  ───────────────────────                                     │
    │  ┌──────────────┐                                           │
    │  │ Kyutai TTS   │ ──► Generate high-quality voiceover       │
    │  │ (via Colab)  │     • Natural-sounding voice              │
    │  └──────────────┘     • Word-level timestamps               │
    │         │              • Expressive delivery                 │
    │         ▼                                                     │
    │  ┌──────────────┐                                           │
    │  │  Audio File  │ ──► narration.wav + timestamps.json       │
    │  └──────────────┘                                           │
    └──────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────┐
    │  STEP 4: VISUAL ASSETS                                       │
    │  ─────────────────────                                       │
    │  ┌──────────────┐     ┌──────────────┐                     │
    │  │   Pexels     │ ──► │   Pixabay    │ ──► Search videos   │
    │  │     API      │     │     API      │                     │
    │  └──────────────┘     └──────────────┘                     │
    │         │                      │                             │
    │         └──────────┬───────────┘                            │
    │                    ▼                                         │
    │         ┌──────────────────┐                               │
    │         │  Find Best Match  │ ──► Based on keywords        │
    │         └──────────────────┘                               │
    │                    │                                         │
    │                    ▼                                         │
    │         ┌──────────────────┐                               │
    │         │ Download Video   │ ──► background.mp4            │
    │         │ (Portrait/9:16)  │                               │
    │         └──────────────────┘                               │
    └──────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────┐
    │  STEP 5: BACKGROUND MUSIC                                    │
    │  ────────────────────────                                    │
    │  ┌──────────────────┐                                       │
    │  │ YouTube Audio    │ ──► Pre-downloaded copyright-free     │
    │  │    Library       │     music tracks                      │
    │  └──────────────────┘                                       │
    │         │                                                     │
    │         ▼                                                     │
    │  ┌──────────────────┐                                       │
    │  │ Random Selection │ ──► music.mp3                        │
    │  └──────────────────┘                                       │
    └──────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────┐
    │  STEP 6: SUBTITLE GENERATION                                 │
    │  ───────────────────────────                                 │
    │  ┌──────────────────┐                                       │
    │  │ Word Timestamps  │ ──► Convert to ASS format             │
    │  │   (from TTS)     │     • Word-by-word animation          │
    │  └──────────────────┘     • Styled text                     │
    │         │                  • Positioned & timed             │
    │         ▼                                                     │
    │  ┌──────────────────┐                                       │
    │  │  pysubs2 (ASS)   │ ──► subtitles.ass                    │
    │  └──────────────────┘                                       │
    └──────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────┐
    │  STEP 7: VIDEO ASSEMBLY (FFmpeg)                            │
    │  ───────────────────────────────────                        │
    │  ┌────────────────────────────────────────────┐            │
    │  │  INPUT COMPONENTS:                         │            │
    │  │  • background.mp4 (video)                  │            │
    │  │  • narration.wav (voice)                   │            │
    │  │  • music.mp3 (background music)            │            │
    │  │  • subtitles.ass (animated text)           │            │
    │  └────────────────────────────────────────────┘            │
    │                    │                                         │
    │                    ▼                                         │
    │  ┌──────────────────────────────────┐                      │
    │  │  FFmpeg Processing:               │                      │
    │  │  1. Scale video to 1080x1920     │                      │
    │  │  2. Crop to 9:16 aspect ratio    │                      │
    │  │  3. Mix voice + music audio      │                      │
    │  │  4. Burn-in animated subtitles   │                      │
    │  │  5. Encode to H.264/AAC          │                      │
    │  └──────────────────────────────────┘                      │
    │                    │                                         │
    │                    ▼                                         │
    │         ┌──────────────────┐                               │
    │         │   Final Video    │ ──► video.mp4 (ready!)        │
    │         │  (1080x1920px)   │                               │
    │         └──────────────────┘                               │
    └──────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────┐
    │  STEP 8: PUBLISHING                                          │
    │  ──────────────────                                          │
    │  ┌──────────────────┐                                       │
    │  │  Video Ready?    │                                       │
    │  └──────────────────┘                                       │
    │         │                                                     │
    │         ├─── Manual ──► Save to output/ folder              │
    │         │                                                     │
    │         └─── Auto ────► ┌──────────────────┐               │
    │                         │ YouTube API v3   │                │
    │                         │    Upload        │                │
    │                         └──────────────────┘                │
    │                                │                             │
    │                                ▼                             │
    │                         ┌──────────────────┐               │
    │                         │  Set Metadata:   │                │
    │                         │  • Title         │                │
    │                         │  • Description   │                │
    │                         │  • Tags          │                │
    │                         │  • Category      │                │
    │                         │  • Privacy       │                │
    │                         └──────────────────┘                │
    │                                │                             │
    │                                ▼                             │
    │                         ┌──────────────────┐               │
    │                         │  🎉 PUBLISHED!   │                │
    │                         │  Live on YouTube │                │
    │                         └──────────────────┘                │
    └──────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  PARALLEL PROCESSES                                                │
│  ─────────────────────                                             │
│                                                                    │
│  • Logging: Real-time colored console output + file logging       │
│  • Storage: Automatic file organization and cleanup               │
│  • Error Handling: Retry logic and graceful degradation          │
│  • Scheduling: Queue management for batch uploads                 │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  KEY FEATURES                                                      │
│  ────────────                                                      │
│                                                                    │
│  ✓ 100% Automated - No manual intervention                        │
│  ✓ 100% Free - All tools and APIs are free-tier                  │
│  ✓ High Quality - Professional video output                       │
│  ✓ SEO Optimized - AI-generated metadata                         │
│  ✓ Scalable - Generate multiple videos                           │
│  ✓ Scheduled - Queue and time uploads                            │
│  ✓ Monitored - Comprehensive logging                             │
│  ✓ Robust - Error handling and retries                           │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

Average Generation Time: 2-5 minutes per video
Output Format: MP4 (H.264/AAC, 1080x1920, 30fps)
Typical Duration: 30-60 seconds
Storage per Video: ~10-30 MB
