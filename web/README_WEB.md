# 🎯 Stickman Shooting Gallery - Web Edition

Welcome to the browser-based version of Stickman Shooting Gallery! This guide will help you get your game running in any modern web browser.

## 🚀 Quick Start

### Method 1: Using the Run Script (Recommended)
```bash
python run_web.py
```
This script will automatically:
- Install dependencies if needed
- Start the web server
- Open your game in the browser

### Method 2: Manual Command
```bash
pygbag --serve --width 800 --height 600 --template index.html web_shooting_gallery.py
```

## 📋 Prerequisites

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for initial setup)

## 🔧 Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python -c "import pygame, pygbag; print('✅ All dependencies installed!')"
   ```

## 🎮 Game Features

### 🔫 Multiple Weapons
- **Pistol (1)**: Balanced accuracy and power
- **Shotgun (2)**: High damage, low accuracy, multiple pellets
- **Rifle (3)**: High accuracy, high damage, slower rate
- **Machine Gun (4)**: Fast rate, lower accuracy

### 🎯 Target Types
- **Stationary Targets**: Classic shooting gallery targets
- **Running Targets**: Moving targets for extra challenge
- **Health System**: Some targets require multiple hits
- **Dynamic States**: Targets can be standing, kneeling, or crawling

### 🏆 Scoring System
- **Hit Points**: 2 points per hit
- **Kill Bonus**: 10 points (stationary), 20 points (running)
- **Time Limit**: 60 seconds of intense action
- **High Scores**: Local leaderboard with name entry

## 🌐 Web Deployment Options

### Local Development Server
The easiest way to test your game:
```bash
python run_web.py
```
Game will be available at: `http://localhost:8080`

### Online Hosting

#### Option 1: GitHub Pages
1. Create a new repository on GitHub
2. Upload all files including the generated `dist/` folder
3. Enable GitHub Pages in repository settings
4. Your game will be live at: `https://yourusername.github.io/repository-name`

#### Option 2: Netlify (Drag & Drop)
1. Run `pygbag web_shooting_gallery.py` to generate the `dist/` folder
2. Visit [netlify.com](https://netlify.com)
3. Drag the `dist/` folder onto the Netlify deploy area
4. Get instant web hosting with a custom URL

#### Option 3: Vercel
1. Install Vercel CLI: `npm install -g vercel`
2. Run `vercel` in your project directory
3. Follow the prompts for instant deployment

## 📁 File Structure

```
stickmanshooting/
├── web_shooting_gallery.py    # Web-compatible game code
├── shooting_gallery2.py       # Original desktop version
├── index.html                 # Custom HTML template
├── run_web.py                 # Easy deployment script
├── requirements.txt           # Python dependencies
├── README_WEB.md             # This documentation
└── dist/                     # Generated web files (after running pygbag)
```

## 🎮 Controls

- **Mouse**: Aim your crosshair
- **Left Click**: Fire your weapon
- **Keys 1-4**: Switch between weapons
- **Enter**: Confirm name entry for high scores

## 🔧 Customization

### Modify Game Settings
Edit `web_shooting_gallery.py` to customize:
- Game duration (default: 60 seconds)
- Weapon properties (damage, accuracy, cooldown)
- Target spawn rates and behavior
- Scoring system

### Customize Appearance
Edit `index.html` to modify:
- Page styling and colors
- Game description and features
- Loading screen appearance
- Responsive design elements

## 🐛 Troubleshooting

### Game Won't Load
- Ensure you have a stable internet connection
- Try refreshing the browser page
- Check browser console for error messages (F12)

### Performance Issues
- Close other browser tabs
- Use Chrome or Firefox for best performance
- Lower the game resolution if needed

### Audio Issues
- Web browsers may block audio until user interaction
- Click anywhere on the page to enable audio

## 🌟 Browser Compatibility

✅ **Fully Supported:**
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

⚠️ **Limited Support:**
- Internet Explorer (not recommended)
- Very old mobile browsers

## 📱 Mobile Support

The game works on mobile devices with touch controls:
- Tap to aim and shoot
- On-screen controls for weapon switching
- Responsive design adapts to screen size

## 🎯 Tips for Best Experience

1. **Use a mouse** for desktop play for better accuracy
2. **Full-screen mode** provides better immersion
3. **Headphones** enhance the audio experience
4. **Stable internet** ensures smooth loading

## 🔄 Updates and Versions

To update your web version:
1. Make changes to `web_shooting_gallery.py`
2. Re-run `pygbag` to regenerate web files
3. Upload the new `dist/` folder to your hosting platform

## 🤝 Contributing

Want to improve the game? Consider:
- Adding new weapon types
- Creating different target types
- Implementing power-ups
- Adding sound effects
- Creating new game modes

## 📞 Support

If you encounter issues:
1. Check the browser console (F12) for errors
2. Verify all files are properly uploaded
3. Test with different browsers
4. Ensure dependencies are correctly installed

---

**Enjoy your browser-based shooting gallery experience! 🎯** 