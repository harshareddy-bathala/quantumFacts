"""
Example usage scripts for the Viral Shorts Generator
Demonstrates various ways to use the system
"""

from pathlib import Path
from viral_shorts.main import ViralShortsGenerator
from viral_shorts.config import OUTPUT_DIR


def example_1_simple_generation():
    """Example 1: Generate a single video"""
    print("=" * 60)
    print("Example 1: Simple Video Generation")
    print("=" * 60)
    
    generator = ViralShortsGenerator()
    video_info = generator.generate_video()
    
    if video_info:
        print(f"\n✓ Success!")
        print(f"  Video: {video_info['video_path']}")
        print(f"  Title: {video_info['title']}")
    else:
        print("\n✗ Failed to generate video")


def example_2_batch_generation():
    """Example 2: Generate multiple videos"""
    print("=" * 60)
    print("Example 2: Batch Video Generation")
    print("=" * 60)
    
    generator = ViralShortsGenerator()
    num_videos = 3
    
    successful = []
    failed = []
    
    for i in range(num_videos):
        print(f"\n--- Generating video {i+1}/{num_videos} ---")
        video_info = generator.generate_video()
        
        if video_info:
            successful.append(video_info)
            print(f"✓ Video {i+1} completed: {video_info['title']}")
        else:
            failed.append(i+1)
            print(f"✗ Video {i+1} failed")
    
    print("\n" + "=" * 60)
    print(f"Batch Complete: {len(successful)} successful, {len(failed)} failed")
    print("=" * 60)


def example_3_test_apis():
    """Example 3: Test all API connections"""
    print("=" * 60)
    print("Example 3: API Connection Tests")
    print("=" * 60)
    
    generator = ViralShortsGenerator()
    results = generator.test_apis()
    
    print("\nTest Summary:")
    all_passed = all(
        v if not isinstance(v, dict) else all(v.values())
        for v in results.values()
    )
    
    if all_passed:
        print("✓ All APIs are working!")
    else:
        print("✗ Some APIs failed. Check configuration.")


def example_4_scheduled_uploads():
    """Example 4: Schedule videos for later upload"""
    print("=" * 60)
    print("Example 4: Scheduled Upload")
    print("=" * 60)
    
    from viral_shorts.publishing.scheduler import VideoScheduler
    from datetime import datetime, timedelta
    
    generator = ViralShortsGenerator()
    scheduler = VideoScheduler()
    
    # Generate video
    print("\nGenerating video...")
    video_info = generator.generate_video()
    
    if video_info:
        # Schedule for 2 hours from now
        scheduled_time = datetime.now() + timedelta(hours=2)
        
        scheduler.add_to_queue(
            video_path=Path(video_info['video_path']),
            title=video_info['title'],
            description=video_info['description'],
            tags=video_info.get('hashtags', []),
            scheduled_time=scheduled_time
        )
        
        print(f"✓ Video scheduled for: {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        
        # Show queue stats
        stats = scheduler.get_queue_stats()
        print(f"\nQueue Status:")
        print(f"  Pending: {stats['pending']}")
        print(f"  Uploaded: {stats['uploaded']}")
        print(f"  Failed: {stats['failed']}")


def example_5_custom_voice():
    """Example 5: Use different voice settings"""
    print("=" * 60)
    print("Example 5: Custom Voice Settings")
    print("=" * 60)
    
    from viral_shorts.narration.voice_manager import VoiceManager
    
    voice_mgr = VoiceManager()
    
    # List available voices
    print("\nAvailable voices:")
    for voice in voice_mgr.list_voices():
        print(f"  - {voice['name']}: {voice['style']} ({voice['gender']})")
    
    # Get recommended voice for content type
    recommended = voice_mgr.recommend_voice('fact')
    print(f"\nRecommended voice for facts: {recommended}")
    
    # Get voice settings
    settings = voice_mgr.get_voice_settings(recommended)
    print(f"Voice settings: {settings}")


def example_6_storage_management():
    """Example 6: Manage storage and cleanup"""
    print("=" * 60)
    print("Example 6: Storage Management")
    print("=" * 60)
    
    from viral_shorts.utils.storage import StorageManager
    
    storage = StorageManager()
    
    # Get storage stats
    print("\nStorage Statistics:")
    stats = storage.get_storage_stats()
    for location, info in stats.items():
        print(f"  {location}:")
        print(f"    Size: {info['size_mb']} MB")
        print(f"    Files: {info['files']}")
    
    # List recent videos
    print("\nRecent Videos:")
    videos = storage.list_videos()
    for i, video in enumerate(videos[:5], 1):
        print(f"  {i}. {video.name}")
    
    # Clean temp files
    print("\nCleaning temporary files...")
    deleted = storage.clean_temp_directory(older_than_hours=24)
    print(f"✓ Deleted {deleted} temporary files")


def example_7_content_analysis():
    """Example 7: Analyze and preview content"""
    print("=" * 60)
    print("Example 7: Content Analysis")
    print("=" * 60)
    
    from viral_shorts.content_sourcing.fetchers import FactFetcher
    from viral_shorts.content_sourcing.parsers import FactParser
    from viral_shorts.scripting.script_generator import ScriptGenerator
    
    # Fetch fact
    fetcher = FactFetcher()
    parser = FactParser()
    script_gen = ScriptGenerator()
    
    print("\nFetching fact...")
    fact_data = fetcher.fetch_random_fact()
    
    if fact_data:
        # Parse fact
        parsed = parser.parse_fact(fact_data)
        print(f"\nFact: {parsed['text']}")
        print(f"Length: {parsed['word_count']} words")
        
        # Extract keywords
        keywords = parser.extract_keywords(parsed['text'])
        print(f"Keywords: {', '.join(keywords)}")
        
        # Generate script
        print("\nGenerating script...")
        script_data = script_gen.generate_script(parsed['text'])
        
        if script_data:
            print(f"\nTitle: {script_data['title']}")
            print(f"Hook: {script_data['hook']}")
            print(f"Hashtags: {', '.join(script_data.get('hashtags', []))}")


def menu():
    """Interactive menu for examples"""
    examples = [
        ("Simple Video Generation", example_1_simple_generation),
        ("Batch Generation (3 videos)", example_2_batch_generation),
        ("Test API Connections", example_3_test_apis),
        ("Scheduled Upload", example_4_scheduled_uploads),
        ("Custom Voice Settings", example_5_custom_voice),
        ("Storage Management", example_6_storage_management),
        ("Content Analysis", example_7_content_analysis),
    ]
    
    print("\n" + "=" * 60)
    print("  Viral Shorts Generator - Example Scripts")
    print("=" * 60)
    print("\nChoose an example to run:\n")
    
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  0. Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (0-7): ").strip()
            choice = int(choice)
            
            if choice == 0:
                print("Goodbye!")
                break
            elif 1 <= choice <= len(examples):
                print()
                examples[choice-1][1]()
                input("\nPress Enter to continue...")
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            input("\nPress Enter to continue...")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Run specific example
        example_num = sys.argv[1]
        if example_num == '1':
            example_1_simple_generation()
        elif example_num == '2':
            example_2_batch_generation()
        elif example_num == '3':
            example_3_test_apis()
        elif example_num == '4':
            example_4_scheduled_uploads()
        elif example_num == '5':
            example_5_custom_voice()
        elif example_num == '6':
            example_6_storage_management()
        elif example_num == '7':
            example_7_content_analysis()
        else:
            print(f"Unknown example: {example_num}")
            print("Usage: python examples.py [1-7]")
    else:
        # Show interactive menu
        menu()
