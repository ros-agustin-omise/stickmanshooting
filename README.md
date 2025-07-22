# 🎯 Stickman Shooting Gallery

A fun and engaging shooting gallery game built with Python and Pygame, featuring animated stickman targets, multiple weapon types, and a high score system.

![Game Screenshot](gameplay_preview.png)
*Screenshot of the game in action*

## 🎮 Features

### Multiple Weapon Types
- **Pistol** - Accurate single shots with moderate damage
- **Shotgun** - Spread shots perfect for close-range targets  
- **Rifle** - High precision sniper shots with maximum damage
- **Machine Gun** - Rapid fire with lower accuracy

### Dynamic Targets
- **Stationary Stickmen** - Standard targets that appear and disappear
- **Running Stickmen** - Moving targets that run across the screen
- **Health System** - Targets with multiple hit points and visual damage states
- **Multiple Poses** - Standing, kneeling, and crawling stickman animations

### Game Features
- ⏱️ **60-second timed gameplay**
- 🏆 **High score system with persistent leaderboard**
- 👤 **Player name entry for high scores**
- 🎨 **Particle effects and animations**
- 🎯 **Different crosshairs for each weapon type**
- 📈 **Progressive difficulty**

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/stickman-shooting-gallery.git
   cd stickman-shooting-gallery
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python shooting_gallery2.py
   ```

## 🎮 How to Play

### Controls
- **Mouse** - Aim your crosshair
- **Left Click** - Shoot
- **1-4 Keys** - Switch between weapons
- **Enter** - Confirm name entry (high score)
- **Backspace** - Delete characters (name entry)

### Gameplay
1. Select your weapon using keys 1-4
2. Click "Start" to begin the game
3. Aim with your mouse and left-click to shoot
4. Hit as many targets as possible within 60 seconds
5. Earn bonus points for moving targets
6. Enter your name if you achieve a high score!

### Scoring
- **Stationary Target Kill**: 10 points
- **Running Target Kill**: 20 points  
- **Partial Damage**: 2 points per hit

## 🔧 System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.6+
- **RAM**: 512MB minimum
- **Storage**: 50MB free space

## 📁 Project Structure

```
stickman-shooting-gallery/
├── shooting_gallery2.py    # Main game file
├── running.py              # Simple running stickman demo
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── highscores.json        # High scores data (created automatically)
└── screenshots/           # Game screenshots
```

## 🎯 Weapon Stats

| Weapon | Fire Rate | Accuracy | Damage | Special |
|--------|-----------|----------|---------|---------|
| Pistol | ●●● | ●●●●● | ●● | Balanced |
| Shotgun | ● | ●● | ●● | Multiple pellets |
| Rifle | ●● | ●●●●● | ●●●● | High damage |
| Machine Gun | ●●●●● | ●● | ● | Rapid fire |

## 🏆 High Score System

The game automatically saves your high scores to `highscores.json`. The leaderboard displays the top 5 scores on the main menu, and the system tracks the top 10 scores overall.

## 🛠️ Development

### Built With
- **Python 3** - Programming language
- **Pygame** - Game development library
- **JSON** - High score data persistence

### Key Components
- `Crosshair` class - Handles aiming and weapon-specific crosshairs
- `StickmanTarget` class - Animated targets with health and movement
- `Particle` class - Visual effects system
- High score management functions
- Multiple game states (menu, playing, game_over, enter_name)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎮 Future Enhancements

- [ ] Sound effects and background music
- [ ] Power-ups and special weapons
- [ ] Multiple game modes
- [ ] Network multiplayer
- [ ] Mobile touch controls
- [ ] Achievement system
- [ ] Customizable targets

## 🐛 Known Issues

- None currently reported! Please open an issue if you find any bugs.

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation above
- Make sure you have the required dependencies installed

## 🌟 Acknowledgments

- Built with Python and Pygame
- Inspired by classic carnival shooting galleries
- Thanks to all contributors and players!

---

**Enjoy the game and happy shooting! 🎯** 