"""
Quick setup verification script
Tests that all components are properly installed
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("✗ ERROR: Python 3.9+ required")
        return False
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Extract version
            first_line = result.stdout.split('\n')[0]
            print(f"✓ {first_line}")
            return True
        else:
            print("✗ FFmpeg not working properly")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg not found")
        print("  Install from: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        print(f"✗ Error checking FFmpeg: {e}")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_file = Path('.env')
    if env_file.exists():
        print("✓ .env file exists")
        return True
    else:
        print("✗ .env file not found")
        print("  Copy .env.example to .env and add your API keys")
        return False

def check_directories():
    """Check if required directories exist"""
    dirs = ['assets/music', 'output', 'temp', 'logs']
    all_exist = True
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"! {dir_name}/ directory will be created")
            dir_path.mkdir(parents=True, exist_ok=True)
    return True

def check_packages():
    """Check if required packages are installed"""
    required = {
        'requests': 'requests',
        'pysubs2': 'pysubs2',
        'dotenv': 'dotenv',
        'google-auth': 'google.auth',
        'google-api-python-client': 'googleapiclient'
    }
    
    all_installed = True
    for package_name, import_name in required.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name} installed")
        except ImportError:
            print(f"✗ {package_name} not installed")
            all_installed = False
    
    if not all_installed:
        print("\nInstall missing packages:")
        print("  pip install -r requirements.txt")
    
    return all_installed

def main():
    """Run all checks"""
    print("=" * 60)
    print("  Viral Shorts Generator - Setup Check")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("FFmpeg", check_ffmpeg),
        ("Environment File", check_env_file),
        ("Directories", check_directories),
        ("Python Packages", check_packages)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All checks passed! You're ready to generate videos.")
        print("\nNext steps:")
        print("  1. Add API keys to .env file")
        print("  2. Download music to assets/music/")
        print("  3. Run: python src/viral_shorts/main.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
    print("=" * 60)
    
    return 0 if all(results) else 1

if __name__ == '__main__':
    sys.exit(main())
