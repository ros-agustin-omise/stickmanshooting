#!/usr/bin/env python3
"""
Simple script to run the Stickman Shooting Gallery in web mode.
This script uses pygbag to serve the game in your browser.
"""

import subprocess
import sys
import webbrowser
import time
from pathlib import Path

def main():
    print("🎯 Starting Stickman Shooting Gallery Web Server...")
    print("=" * 50)
    
    # Check if pygbag is installed
    try:
        import pygbag
        print("✅ Pygbag found!")
    except ImportError:
        print("❌ Pygbag not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygbag"])
        print("✅ Pygbag installed!")
    
    # Check if the web game file exists
    game_file = Path("web_shooting_gallery.py")
    if not game_file.exists():
        print("❌ Game file 'web_shooting_gallery.py' not found!")
        return
    
    # Check if template exists
    template_file = Path("index.html")
    if not template_file.exists():
        print("⚠️  Template file 'index.html' not found. Using default template.")
        template_arg = ""
    else:
        template_arg = "--template index.html"
    
    print("🚀 Starting web server...")
    print("📱 Your game will open automatically in your default browser")
    print("🌐 You can also manually visit: http://localhost:8080")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Build the web version
        build_cmd = f"pygbag --width 800 --height 600 {template_arg} --no_opt web_shooting_gallery.py"
        print("🔨 Building web version...")
        subprocess.run(build_cmd, shell=True, check=True)
        
        # Serve the built files
        print("🌐 Starting local server...")
        serve_cmd = "cd build/web && python3 -m http.server 8080"
        subprocess.run(serve_cmd, shell=True, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    
    print("👋 Thanks for playing!")

if __name__ == "__main__":
    main() 