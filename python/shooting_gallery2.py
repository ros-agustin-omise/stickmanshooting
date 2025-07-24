import pygame
import sys
import random
import math
import json
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Shooting Gallery")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARK_RED = (139, 0, 0)
GRAY = (128, 128, 128)

# Game variables
clock = pygame.time.Clock()
FPS = 60
score = 0
game_over = False
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 48)
game_time = 60  # Game lasts for 60 seconds
start_time = 0
game_state = "menu"  # menu, playing, game_over, enter_name
player_name = ""
is_new_high_score = False
high_scores = []

# High score file
HIGHSCORE_FILE = "highscores.json"

# Hide the mouse cursor
pygame.mouse.set_visible(False)

# Load high scores from file
def load_high_scores():
    global high_scores
    try:
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, 'r') as f:
                high_scores = json.load(f)
        else:
            high_scores = []
    except:
        high_scores = []

# Save high scores to file
def save_high_scores():
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump(high_scores, f, indent=2)
    except:
        pass  # Fail silently if can't save

# Add a new high score
def add_high_score(name, score):
    global high_scores
    high_scores.append({"name": name, "score": score})
    # Sort by score (descending) and keep top 10
    high_scores.sort(key=lambda x: x["score"], reverse=True)
    high_scores = high_scores[:10]
    save_high_scores()

# Check if current score is a high score
def is_high_score(score):
    if len(high_scores) < 10:
        return True
    return score > high_scores[-1]["score"]

# Load high scores at startup
load_high_scores()

# Professional sound system using numpy and pygame
import numpy as np

# Removed old synthetic gun sound generation - now using real .mp3 files!

def create_sound(frequency, duration, volume=0.3, wave_type='sine'):
    """Create a simple sound for non-gun effects"""
    sample_rate = 22050
    frames = int(duration * sample_rate)
    
    # Create time array
    t = np.linspace(0, duration, frames, False)
    
    # Generate waveform
    if wave_type == 'sine':
        wave = np.sin(frequency * 2 * np.pi * t)
    elif wave_type == 'square':
        wave = np.sign(np.sin(frequency * 2 * np.pi * t))
    elif wave_type == 'sawtooth':
        wave = 2 * (t * frequency - np.floor(t * frequency + 0.5))
    else:
        wave = np.sin(frequency * 2 * np.pi * t)
    
    # Apply envelope
    fade_frames = int(0.01 * sample_rate)
    if fade_frames > 0:
        wave[:fade_frames] *= np.linspace(0, 1, fade_frames)
        wave[-fade_frames:] *= np.linspace(1, 0, fade_frames)
    
    # Apply volume and convert to 16-bit
    wave = (wave * volume * 32767).astype(np.int16)
    
    # Convert to stereo
    stereo_wave = np.zeros((frames, 2), dtype=np.int16)
    stereo_wave[:, 0] = wave
    stereo_wave[:, 1] = wave
    stereo_wave = np.ascontiguousarray(stereo_wave)
    
    return pygame.sndarray.make_sound(stereo_wave)

# Removed create_gun_sound function - now loading real .mp3 files directly!

# Function to try loading a real sound file
def try_load_sound_file(filename, volume=0.7):
    """Try to load a sound file with volume control, return None if not found"""
    try:
        if os.path.exists(filename):
            sound = pygame.mixer.Sound(filename)
            sound.set_volume(volume)  # Set volume for real sounds
            print(f"   ✅ Loaded real sound file: {filename} (volume: {volume})")
            return sound
        else:
            return None
    except Exception as e:
        print(f"   ❌ Failed to load {filename}: {e}")
        return None

# Create all sound effects
try:
    sounds = {}
    
    # Load real gun sounds from .mp3 files
    # Different volumes for different weapon types for realism
    real_pistol = try_load_sound_file("pistol.mp3", 0.8)
    real_shotgun = try_load_sound_file("shotgun.mp3", 0.9)  # Shotgun louder
    real_rifle = try_load_sound_file("rifle-gunshot.mp3", 0.85)
    real_machine_gun = try_load_sound_file("machine-gun.mp3", 0.6)  # Machine gun quieter for rapid fire
    
    # Verify all gun sounds loaded successfully
    if not all([real_pistol, real_shotgun, real_rifle, real_machine_gun]):
        missing = []
        if not real_pistol: missing.append("pistol.mp3")
        if not real_shotgun: missing.append("shotgun.mp3")
        if not real_rifle: missing.append("rifle-gunshot.mp3")
        if not real_machine_gun: missing.append("machine-gun.mp3")
        raise Exception(f"Missing required sound files: {', '.join(missing)}")
    
    sounds = {
        'pistol': real_pistol,
        'shotgun': real_shotgun,
        'rifle': real_rifle,
        'machine_gun': real_machine_gun,
        'hit': create_sound(1400, 0.04, 0.5, 'sine'),
        'fall': create_sound(250, 0.25, 0.6, 'sawtooth'),
        'click': create_sound(1000, 0.03, 0.4, 'sine'),
        'beep': create_sound(600, 0.08, 0.5, 'sine'),
        'game_over': create_sound(180, 0.6, 0.7, 'sawtooth'),
        'victory': create_sound(523, 0.4, 0.6, 'sine')  # C note
    }
    
    # All sounds loaded successfully
    sound_count = len([s for s in sounds.values() if s is not None])
    print(f"   - Successfully loaded {sound_count} total sound effects")
    print("   - All weapon sounds: 🔫 Pistol | 💥 Shotgun | 🎯 Rifle | 🔫 Machine Gun (ALL REAL)")
    
    # Set pygame mixer volume to maximum
    pygame.mixer.set_num_channels(8)  # Allow multiple sounds to play simultaneously
    
    print("🔊 Professional weapon audio system initialized!")
    print("   - ✅ Using 4/4 REAL gun sound files (.mp3)!")
    print("   - 🔥 Authentic weapon audio for maximum immersion")
    print("   - 🎧 Optimized volume levels for each weapon type")
    print("   - 🎯 Ready for intense shooting action!")
    SOUND_AVAILABLE = True
    
except Exception as e:
    sounds = {}
    SOUND_AVAILABLE = False
    print(f"🔊 Audio system failed to initialize: {e}")

# Sound effect functions with realistic audio
def play_gun_sound(gun_type):
    """Play realistic gun sound based on weapon type"""
    if SOUND_AVAILABLE and gun_type in sounds:
        sounds[gun_type].play()

def play_hit_sound():
    """Play satisfying hit sound"""
    if SOUND_AVAILABLE and 'hit' in sounds:
        sounds['hit'].play()

def play_fall_sound():
    """Play dramatic target fall sound"""
    if SOUND_AVAILABLE and 'fall' in sounds:
        sounds['fall'].play()

def play_ui_sound(sound_type):
    """Play appropriate UI sound"""
    if SOUND_AVAILABLE:
        sound_map = {
            'click': 'click',
            'menu_select': 'beep', 
            'game_over': 'game_over',
            'high_score': 'victory'
        }
        sound_key = sound_map.get(sound_type, 'click')
        if sound_key in sounds:
            sounds[sound_key].play()

# Gun types
guns = {
    "pistol": {
        "name": "Pistol",
        "cooldown": 500,  # milliseconds between shots
        "accuracy": 5,    # spread in pixels (lower is more accurate)
        "damage": 1,      # hits to kill a target
        "color": BLUE,
        "size": 18,
        "key": pygame.K_1,
        "recoil": 5,      # recoil amount
        "flash_duration": 100,  # milliseconds
    },
    "shotgun": {
        "name": "Shotgun",
        "cooldown": 1000,
        "accuracy": 25,
        "damage": 1,
        "pellets": 5,     # number of projectiles per shot
        "color": RED,
        "size": 22,
        "key": pygame.K_2,
        "recoil": 15,
        "flash_duration": 150,
    },
    "rifle": {
        "name": "Rifle",
        "cooldown": 700,
        "accuracy": 2,
        "damage": 2,      # Rifle does more damage
        "color": GREEN,
        "size": 20,
        "key": pygame.K_3,
        "recoil": 8,
        "flash_duration": 120,
    },
    "machine_gun": {
        "name": "Machine Gun",
        "cooldown": 150,
        "accuracy": 15,
        "damage": 0.5,    # Machine gun does less damage per bullet
        "color": YELLOW,
        "size": 16,
        "key": pygame.K_4,
        "recoil": 3,
        "flash_duration": 80,
    }
}

current_gun = "pistol"
last_shot_time = 0

class Particle:
    def __init__(self, x, y, color, velocity_range=3, size_range=(2, 5), life_range=(20, 40)):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(size_range[0], size_range[1])
        self.velocity_x = random.uniform(-velocity_range, velocity_range)
        self.velocity_y = random.uniform(-velocity_range, velocity_range)
        self.life = random.randint(life_range[0], life_range[1])
        self.alpha = 255
        self.fade_rate = 255 / self.life
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.life -= 1
        self.alpha = max(0, self.alpha - self.fade_rate)
        return self.life > 0
    
    def draw(self, surface):
        if self.alpha > 0:
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, int(self.alpha)), (self.size, self.size), self.size)
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))

class Crosshair:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 20
        self.recoil_x = 0
        self.recoil_y = 0
        self.flash_time = 0
        self.hit_confirm_time = 0
        self.particles = []
    
    def update(self):
        # Get mouse position
        pos = pygame.mouse.get_pos()
        self.x = pos[0] + self.recoil_x
        self.y = pos[1] + self.recoil_y
        
        # Reduce recoil over time
        if self.recoil_x > 0:
            self.recoil_x = max(0, self.recoil_x - 1)
        elif self.recoil_x < 0:
            self.recoil_x = min(0, self.recoil_x + 1)
            
        if self.recoil_y > 0:
            self.recoil_y = max(0, self.recoil_y - 1)
        elif self.recoil_y < 0:
            self.recoil_y = min(0, self.recoil_y + 1)
        
        # Update particles
        for particle in self.particles[:]:
            if not particle.update():
                self.particles.remove(particle)
    
    def draw(self):
        gun = guns[current_gun]
        size = gun["size"]
        color = gun["color"]
        current_time = pygame.time.get_ticks()
        
        # Draw muzzle flash if recently fired
        if current_time - self.flash_time < gun["flash_duration"]:
            # Draw muzzle flash
            flash_size = size * 1.5
            flash_color = YELLOW
            flash_surface = pygame.Surface((flash_size * 2, flash_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(flash_surface, (*flash_color, 150), (flash_size, flash_size), flash_size)
            screen.blit(flash_surface, (self.x - flash_size, self.y - flash_size))
        
        # Draw hit confirmation if recently hit a target
        if current_time - self.hit_confirm_time < 300:
            # Draw hit confirmation circle
            confirm_size = size * 1.2
            confirm_color = GREEN
            confirm_surface = pygame.Surface((confirm_size * 2, confirm_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(confirm_surface, (*confirm_color, 100), (confirm_size, confirm_size), confirm_size, 2)
            screen.blit(confirm_surface, (self.x - confirm_size, self.y - confirm_size))
        
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
        
        # Draw crosshair based on gun type
        if current_gun == "pistol":
            # Simple crosshair
            pygame.draw.circle(screen, color, (self.x, self.y), size, 1)
            pygame.draw.line(screen, color, (self.x - size, self.y), (self.x + size, self.y), 1)
            pygame.draw.line(screen, color, (self.x, self.y - size), (self.x, self.y + size), 1)
        
        elif current_gun == "shotgun":
            # Wider crosshair with spread indicator
            pygame.draw.circle(screen, color, (self.x, self.y), size, 1)
            pygame.draw.circle(screen, color, (self.x, self.y), size//2, 1)
            pygame.draw.line(screen, color, (self.x - size, self.y), (self.x + size, self.y), 1)
            pygame.draw.line(screen, color, (self.x, self.y - size), (self.x, self.y + size), 1)
        
        elif current_gun == "rifle":
            # Precision crosshair
            pygame.draw.line(screen, color, (self.x - size, self.y), (self.x + size, self.y), 1)
            pygame.draw.line(screen, color, (self.x, self.y - size), (self.x, self.y + size), 1)
            pygame.draw.circle(screen, color, (self.x, self.y), 3, 1)
            # Range finder dots
            pygame.draw.circle(screen, color, (self.x, self.y - size//2), 1)
            pygame.draw.circle(screen, color, (self.x, self.y + size//2), 1)
            pygame.draw.circle(screen, color, (self.x - size//2, self.y), 1)
            pygame.draw.circle(screen, color, (self.x + size//2, self.y), 1)
        
        elif current_gun == "machine_gun":
            # Fast-paced crosshair
            pygame.draw.circle(screen, color, (self.x, self.y), size, 1)
            pygame.draw.line(screen, color, (self.x - size//2, self.y), (self.x + size//2, self.y), 1)
            pygame.draw.line(screen, color, (self.x, self.y - size//2), (self.x, self.y + size//2), 1)
            # Bullet counter dots
            for i in range(4):
                angle = i * math.pi / 2
                x = self.x + math.cos(angle) * (size * 0.7)
                y = self.y + math.sin(angle) * (size * 0.7)
                pygame.draw.circle(screen, color, (int(x), int(y)), 2)
        
        # Small center dot for all guns
        pygame.draw.circle(screen, RED, (self.x, self.y), 2)
    
    def shoot(self):
        gun = guns[current_gun]
        bullets = []
        
        # Play shooting sound
        play_gun_sound(current_gun)
        
        # Apply recoil
        recoil = gun["recoil"]
        self.recoil_x = random.randint(-recoil, recoil)
        self.recoil_y = -recoil  # Always kick upward
        
        # Set flash time
        self.flash_time = pygame.time.get_ticks()
        
        # Create muzzle particles
        for _ in range(10):
            self.particles.append(
                Particle(self.x, self.y, ORANGE, 
                         velocity_range=5, 
                         size_range=(1, 3), 
                         life_range=(10, 20))
            )
        
        if current_gun == "shotgun":
            # Shotgun fires multiple pellets
            for _ in range(gun["pellets"]):
                spread_x = random.randint(-gun["accuracy"], gun["accuracy"])
                spread_y = random.randint(-gun["accuracy"], gun["accuracy"])
                bullets.append(Bullet(self.x + spread_x, self.y + spread_y))
        else:
            # Other guns fire a single bullet with varying accuracy
            spread_x = random.randint(-gun["accuracy"], gun["accuracy"])
            spread_y = random.randint(-gun["accuracy"], gun["accuracy"])
            bullets.append(Bullet(self.x + spread_x, self.y + spread_y))
            
        return bullets
    
    def register_hit(self):
        # Set hit confirmation time
        self.hit_confirm_time = pygame.time.get_ticks()

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True
    
    def check_hit(self, target):
        # Simple point collision detection
        if not target.active or target.falling:
            return False
            
        # Check if bullet position is within the target's hit area
        distance = math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)
        return distance < target.hit_radius

class StickmanTarget:
    def __init__(self):
        self.reset()
        self.hit_radius = 25  # Radius for hit detection
        self.visible_time = random.randint(2, 5) * 1000  # 2-5 seconds in milliseconds
        self.appear_time = 0
        self.active = False  # Start inactive
        self.health = 3      # Default max health
        self.max_health = 3
        self.hit_effect = None
        self.particles = []
        self.falling = False
        self.fall_angle = 0
        self.fall_speed = 0
        
        # Running properties
        self.is_running = False
        self.speed = 0
        self.direction = 1  # 1 for right, -1 for left
        self.run_frame = 0
        self.frame_counter = 0
        
        # Health state
        self.state = "standing"  # standing, kneeling, crawling
        
        # Crawling animation properties
        self.crawl_frame = 0
        self.crawl_up = True  # Whether the stickman is in the up position of crawling
    
    def reset(self):
        self.active = True
        self.particles = []
        self.falling = False
        self.fall_angle = 0
        self.fall_speed = 0
        self.state = "standing"
        self.crawl_frame = 0
        self.crawl_up = True
        
        # Determine if this will be a stationary or running stickman
        self.is_running = random.random() < 0.4  # 40% chance of being a runner
        
        if self.is_running:
            # Running stickman setup
            self.direction = random.choice([-1, 1])
            self.speed = random.uniform(2, 5)
            
            # Start from either left or right side
            if self.direction == 1:  # Moving right
                self.x = -20  # Start off-screen to the left
            else:  # Moving left
                self.x = WIDTH + 20  # Start off-screen to the right
                
            self.y = random.randint(100, HEIGHT - 150)
            self.run_frame = 0
            self.frame_counter = 0
            self.visible_time = 15000  # Longer time for running targets
        else:
            # Stationary stickman setup
            self.x = random.randint(50, WIDTH - 50)
            self.y = random.randint(100, HEIGHT - 150)
            self.visible_time = random.randint(2, 5) * 1000  # 2-5 seconds
        
        # Common properties
        self.color = RED
        self.appear_time = pygame.time.get_ticks()
        
        # Health based on difficulty (later targets have more health)
        self.max_health = random.randint(2, 4)
        self.health = self.max_health
    
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Update particles
        for particle in self.particles[:]:
            if not particle.update():
                self.particles.remove(particle)
        
        # Update falling animation
        if self.falling:
            self.fall_angle += self.fall_speed
            if self.fall_angle >= 90:  # Completely fallen
                self.active = False
            return
        
        # Update health state
        health_percent = self.health / self.max_health
        if health_percent <= 0.33:
            self.state = "crawling"
        elif health_percent <= 0.66:
            self.state = "kneeling"
        else:
            self.state = "standing"
        
        # Running animation and movement
        if self.is_running and not self.falling:
            # Move the stickman based on state
            if self.state == "crawling":
                # Very slow when crawling
                self.x += self.direction * (self.speed * 0.3)
            elif self.state == "kneeling":
                # Slower when kneeling
                self.x += self.direction * (self.speed * 0.6)
            else:
                # Normal speed when standing
                self.x += self.direction * self.speed
            
            # Check if stickman has moved off-screen
            if (self.direction == 1 and self.x > WIDTH + 20) or (self.direction == -1 and self.x < -20):
                self.active = False
                return
            
            # Update animation frame
            self.frame_counter += 1
            animation_speed = 5
            if self.state == "kneeling":
                animation_speed = 7  # Slower animation when kneeling
            elif self.state == "crawling":
                animation_speed = 10  # Even slower when crawling
                
            if self.frame_counter >= animation_speed:
                self.run_frame = (self.run_frame + 1) % 4
                if self.state == "crawling":
                    # Toggle crawling position (up/down)
                    self.crawl_up = not self.crawl_up
                self.frame_counter = 0
        
        # Check if the target should disappear (for stationary targets)
        if not self.is_running and current_time - self.appear_time > self.visible_time:
            self.active = False
    
    def hit(self, damage):
        # Play hit sound
        play_hit_sound()
        
        # Reduce health
        self.health -= damage
        
        # Create hit effect particles
        for _ in range(10):
            self.particles.append(
                Particle(self.x, self.y, (200, 200, 200),  # White/gray particles
                         velocity_range=4, 
                         size_range=(2, 5), 
                         life_range=(20, 40))
            )
        
        # If health is depleted, start falling animation
        if self.health <= 0:
            # Play target fall sound
            play_fall_sound()
            self.falling = True
            self.fall_speed = random.uniform(3, 6)
            # Fall direction (left or right)
            self.fall_direction = random.choice([-1, 1])
    
    def draw(self):
        if not self.active:
            return
        
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
        
        # Determine color based on health
        if self.health >= self.max_health * 0.66:
            color = RED
        elif self.health >= self.max_health * 0.33:
            color = ORANGE
        else:
            color = DARK_RED
        
        # Apply falling animation if active
        if self.falling:
            # Create a surface for the stickman
            stickman_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
            
            # Draw stickman on the surface
            # Head
            pygame.draw.circle(stickman_surface, color, (30, 15), 10)
            
            # Body
            pygame.draw.line(stickman_surface, color, (30, 25), (30, 45), 2)
            
            # Arms
            pygame.draw.line(stickman_surface, color, (30, 30), (18, 35), 2)
            pygame.draw.line(stickman_surface, color, (30, 30), (42, 35), 2)
            
            # Legs
            pygame.draw.line(stickman_surface, color, (30, 45), (20, 60), 2)
            pygame.draw.line(stickman_surface, color, (30, 45), (40, 60), 2)
            
            # Rotate the surface
            angle = self.fall_angle * self.fall_direction
            rotated_surface = pygame.transform.rotate(stickman_surface, angle)
            
            # Get the new rect and position it
            rect = rotated_surface.get_rect(center=(self.x, self.y))
            
            # Draw the rotated stickman
            screen.blit(rotated_surface, rect.topleft)
            
        elif self.state == "crawling":
            # Draw crawling stickman with up and down motion
            
            # Determine if in up or down position
            is_up = self.crawl_up
            if self.is_running:
                is_up = self.crawl_up
            else:
                # For stationary stickmen, alternate every second
                is_up = (pygame.time.get_ticks() // 1000) % 2 == 0
            
            if is_up:
                # UP POSITION - Body raised, arms extended, legs bent
                
                # Head position (higher in up position)
                head_y = self.y - 10
                pygame.draw.circle(screen, color, (int(self.x), int(head_y)), 8)
                
                # Body (slightly arched)
                body_length = 20
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 8), 
                                (self.x, head_y + 18), 2)
                
                # Arms (extended forward)
                # Left arm
                arm_x_offset = 8 * self.direction if self.is_running else 8
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 12), 
                                (self.x - arm_x_offset, head_y + 20), 2)
                
                # Right arm
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 12), 
                                (self.x + arm_x_offset, head_y + 20), 2)
                
                # Legs (bent under body)
                # Left leg
                leg_x_offset = 10 * self.direction if self.is_running else 10
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 18), 
                                (self.x - leg_x_offset, head_y + 25), 2)
                
                # Right leg
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 18), 
                                (self.x + leg_x_offset, head_y + 25), 2)
                
            else:
                # DOWN POSITION - Body lowered, arms bent supporting weight, legs extended
                
                # Head position (lower in down position)
                head_y = self.y - 5
                pygame.draw.circle(screen, color, (int(self.x), int(head_y)), 8)
                
                # Body (horizontal)
                body_length = 20
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 8), 
                                (self.x, head_y + 15), 2)
                
                # Arms (bent supporting weight)
                # Left arm
                arm_x_offset = 12 * self.direction if self.is_running else 12
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 10), 
                                (self.x - arm_x_offset, head_y + 8), 2)
                
                # Right arm
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 10), 
                                (self.x + arm_x_offset, head_y + 8), 2)
                
                # Legs (extended behind)
                # Left leg
                leg_x_offset = 15 * self.direction if self.is_running else 15
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 15), 
                                (self.x - leg_x_offset, head_y + 18), 2)
                
                # Right leg
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 15), 
                                (self.x + leg_x_offset, head_y + 18), 2)
                
        elif self.state == "kneeling":
            # Draw kneeling stickman
            # Head (lower than standing)
            head_y = self.y - 10
            pygame.draw.circle(screen, color, (int(self.x), int(head_y)), 10)
            
            # Body (shorter)
            pygame.draw.line(screen, color, (self.x, head_y + 10), (self.x, head_y + 25), 2)
            
            if self.is_running:
                # Running kneeling animation
                # Arms - animate based on running
                arm_offset = 8 if self.run_frame % 2 == 0 else -8
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 15), 
                                (self.x - 10 * self.direction, head_y + 15 - arm_offset), 2)
                pygame.draw.line(screen, color, 
                                (self.x, head_y + 15), 
                                (self.x + 10 * self.direction, head_y + 15 + arm_offset), 2)
                
                # Legs - one knee on ground, one bent
                if self.run_frame % 2 == 0:
                    # Front leg moving forward
                    pygame.draw.line(screen, color, 
                                    (self.x, head_y + 25), 
                                    (self.x + 12 * self.direction, head_y + 30), 2)
                    # Back leg kneeling
                    pygame.draw.line(screen, color, 
                                    (self.x, head_y + 25), 
                                    (self.x - 8 * self.direction, head_y + 35), 2)
                else:
                    # Front leg kneeling
                    pygame.draw.line(screen, color, 
                                    (self.x, head_y + 25), 
                                    (self.x + 8 * self.direction, head_y + 35), 2)
                    # Back leg moving forward
                    pygame.draw.line(screen, color, 
                                    (self.x, head_y + 25), 
                                    (self.x - 12 * self.direction, head_y + 30), 2)
            else:
                # Stationary kneeling stickman
                # Arms
                pygame.draw.line(screen, color, (self.x, head_y + 15), (self.x - 12, head_y + 20), 2)
                pygame.draw.line(screen, color, (self.x, head_y + 15), (self.x + 12, head_y + 20), 2)
                
                # Legs - both knees on ground
                pygame.draw.line(screen, color, (self.x, head_y + 25), (self.x - 10, head_y + 35), 2)
                pygame.draw.line(screen, color, (self.x, head_y + 25), (self.x + 10, head_y + 35), 2)
            
        elif self.is_running:
            # Draw running stickman (standing)
            # Head
            pygame.draw.circle(screen, color, (int(self.x), int(self.y - 15)), 10)
            
            # Body
            pygame.draw.line(screen, color, (self.x, self.y - 5), (self.x, self.y + 15), 2)
            
            # Arms - animate based on running
            arm_offset = 10 if self.run_frame % 2 == 0 else -10
            pygame.draw.line(screen, color, 
                            (self.x, self.y), 
                            (self.x - 12 * self.direction, self.y - arm_offset), 2)
            pygame.draw.line(screen, color, 
                            (self.x, self.y), 
                            (self.x + 12 * self.direction, self.y + arm_offset), 2)
            
            # Legs - animate based on running
            leg_offset = 15 if self.run_frame % 2 == 0 else -15
            pygame.draw.line(screen, color, 
                            (self.x, self.y + 15), 
                            (self.x - 10 * self.direction + leg_offset, self.y + 30), 2)
            pygame.draw.line(screen, color, 
                            (self.x, self.y + 15), 
                            (self.x + 10 * self.direction - leg_offset, self.y + 30), 2)
            
        else:
            # Draw normal stationary stickman (standing)
            # Head
            pygame.draw.circle(screen, color, (int(self.x), int(self.y - 15)), 10)
            
            # Body
            pygame.draw.line(screen, color, (self.x, self.y - 5), (self.x, self.y + 15), 2)
            
            # Arms
            pygame.draw.line(screen, color, (self.x, self.y), (self.x - 12, self.y + 5), 2)
            pygame.draw.line(screen, color, (self.x, self.y), (self.x + 12, self.y + 5), 2)
            
            # Legs
            pygame.draw.line(screen, color, (self.x, self.y + 15), (self.x - 10, self.y + 30), 2)
            pygame.draw.line(screen, color, (self.x, self.y + 15), (self.x + 10, self.y + 30), 2)
        
        # Draw health bar for targets with more than 1 health
        if self.max_health > 1 and not self.falling:
            health_width = 30
            health_height = 4
            
            # Adjust health bar position based on stickman state
            if self.state == "crawling":
                health_y = self.y - 20
            elif self.state == "kneeling":
                health_y = self.y - 25
            else:
                health_y = self.y - 35
                
            health_x = self.x - health_width 
            health_y = self.y - 35
                
            health_x = self.x - health_width // 2
            
            # Background
            pygame.draw.rect(screen, (100, 100, 100), (health_x, health_y, health_width, health_height))
            
            # Health remaining
            health_percent = self.health / self.max_health
            pygame.draw.rect(screen, GREEN, (health_x, health_y, int(health_width * health_percent), health_height))

# Create game objects
crosshair = Crosshair()
targets = [StickmanTarget() for _ in range(15)]  # Increased pool size
active_targets = []  # Currently visible targets

# Background elements
def draw_background():
    # Draw a simple shooting range background
    pygame.draw.rect(screen, (200, 200, 200), (0, HEIGHT - 100, WIDTH, 100))  # Floor
    pygame.draw.line(screen, BLACK, (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 3)  # Floor line
    
    # Draw some target stands
    for x in range(50, WIDTH, 150):
        pygame.draw.rect(screen, (139, 69, 19), (x, HEIGHT - 100, 20, 60))  # Stand

def draw_gun_info():
    # Draw current gun info
    gun = guns[current_gun]
    gun_text = font.render(f"Gun: {gun['name']}", True, gun["color"])
    screen.blit(gun_text, (WIDTH // 2 - 80, HEIGHT - 40))
    
    # Draw gun selection help
    help_text = small_font.render("Press 1-4 to change weapons", True, BLACK)
    screen.blit(help_text, (WIDTH // 2 - 100, HEIGHT - 20))

def draw_menu():
    # Draw title
    title_font = pygame.font.SysFont(None, 72)
    title = title_font.render("Stickman Shooting Gallery", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    # Draw high scores
    if high_scores:
        high_score_title = big_font.render("HIGH SCORES", True, BLACK)
        screen.blit(high_score_title, (50, 120))
        
        for i, entry in enumerate(high_scores[:5]):  # Show top 5
            score_text = font.render(f"{i+1}. {entry['name']}: {entry['score']}", True, BLACK)
            screen.blit(score_text, (50, 160 + i * 30))
    
    # Draw gun selection options
    y_pos = 320
    instruction = font.render("Select your weapon:", True, BLACK)
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, y_pos))
    
    y_pos += 50
    for i, (gun_id, gun) in enumerate(guns.items()):
        color = gun["color"]
        text = font.render(f"{i+1}. {gun['name']}", True, color)
        
        # Highlight current selection
        if gun_id == current_gun:
            pygame.draw.rect(screen, (200, 200, 200), 
                            (WIDTH // 2 - 150, y_pos - 5, 300, 40), 0)
            pygame.draw.rect(screen, color, 
                            (WIDTH // 2 - 150, y_pos - 5, 300, 40), 2)
        
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos))
        
        # Add gun stats
        damage_text = "●" * int(gun["damage"] * 2) if gun["damage"] >= 0.5 else "½"
        stats = small_font.render(
            f"Rate: {'●' * (5 - gun['cooldown'] // 200)}  " +
            f"Accuracy: {'●' * (5 - gun['accuracy'] // 5)}  " +
            f"Damage: {damage_text}", 
            True, color)
        screen.blit(stats, (WIDTH // 2 - stats.get_width() // 2, y_pos + 25))
        
        y_pos += 70
    
    # Draw start instruction
    start_text = font.render("Click to Start", True, BLACK)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, y_pos + 30))

def draw_name_entry():
    # Draw semi-transparent background
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Draw name entry dialog
    dialog_width = 400
    dialog_height = 200
    dialog_x = (WIDTH - dialog_width) // 2
    dialog_y = (HEIGHT - dialog_height) // 2
    
    pygame.draw.rect(screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height))
    pygame.draw.rect(screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 3)
    
    # Draw congratulations text
    congrats_text = big_font.render("NEW HIGH SCORE!", True, GREEN)
    screen.blit(congrats_text, (dialog_x + 20, dialog_y + 20))
    
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (dialog_x + 20, dialog_y + 70))
    
    # Draw name prompt
    prompt_text = font.render("Enter your name:", True, BLACK)
    screen.blit(prompt_text, (dialog_x + 20, dialog_y + 100))
    
    # Draw name input box
    input_box = pygame.Rect(dialog_x + 20, dialog_y + 130, 360, 30)
    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    
    # Draw entered name
    name_surface = font.render(player_name + "_", True, BLACK)  # Add cursor
    screen.blit(name_surface, (input_box.x + 5, input_box.y + 5))
    
    # Draw instruction
    instruction = small_font.render("Press ENTER to confirm", True, BLACK)
    screen.blit(instruction, (dialog_x + 20, dialog_y + 170))

# Game loop
running = True
start_time = pygame.time.get_ticks()
last_spawn_time = 0
spawn_interval = 1000  # Spawn a new target every 1 second initially

while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = 0  # Ensure elapsed_time is always defined
    remaining_time = game_time  # Initialize remaining_time with full game time
    
    if game_state == "playing":
        elapsed_time = (current_time - start_time) // 1000  # Convert to seconds
        remaining_time = max(0, game_time - elapsed_time)
    
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if game_state == "menu":
                    # Start the game
                    play_ui_sound("click")
                    game_state = "playing"
                    start_time = pygame.time.get_ticks()
                    score = 0
                    active_targets = []
                    
                elif game_state == "playing":
                    # Check if enough time has passed since last shot (cooldown)
                    if current_time - last_shot_time >= guns[current_gun]["cooldown"]:
                        # Create bullets at the crosshair position
                        bullets = crosshair.shoot()
                        last_shot_time = current_time
                        
                        # Check for hits
                        hit = False
                        for bullet in bullets:
                            for target in active_targets:
                                if target.active and not target.falling and bullet.check_hit(target):
                                    # Apply damage
                                    damage = guns[current_gun]["damage"]
                                    target.hit(damage)
                                    
                                    # Award points based on target type
                                    if target.health <= 0:
                                        # Bonus points for running targets
                                        if target.is_running:
                                            score += 20
                                        else:
                                            score += 10
                                        crosshair.register_hit()  # Show hit confirmation
                                    else:
                                        # Partial points for hits that don't kill
                                        score += 2
                                    
                                    hit = True
                                    break
                            if hit:
                                break
                
                elif game_state == "game_over":
                    # Reset game
                    play_ui_sound("click")
                    game_state = "menu"
                    
        if event.type == pygame.KEYDOWN:
            if game_state == "enter_name":
                if event.key == pygame.K_RETURN:
                    # Confirm name entry
                    if player_name.strip():  # Make sure name is not empty
                        play_ui_sound("click")
                        add_high_score(player_name.strip(), score)
                        game_state = "menu"
                        player_name = ""
                elif event.key == pygame.K_BACKSPACE:
                    # Delete character
                    player_name = player_name[:-1]
                else:
                    # Add character (limit to reasonable length)
                    if len(player_name) < 15 and event.unicode.isprintable():
                        player_name += event.unicode
            else:
                # Gun selection
                for gun_id, gun_info in guns.items():
                    if event.key == gun_info["key"]:
                        current_gun = gun_id
                        play_ui_sound("menu_select")
                        break
                

                        
                if event.key == pygame.K_r and game_state == "game_over":
                    # Reset game
                    play_ui_sound("click")
                    game_state = "menu"
    
    # Update crosshair position
    crosshair.update()
    
    if game_state == "menu":
        draw_menu()
        
    elif game_state == "playing":
        draw_background()
        
        # Update active targets
        for target in active_targets[:]:
            target.update()
            if not target.active:
                active_targets.remove(target)
        
        # Spawn new targets
        if current_time - last_spawn_time > spawn_interval and len(active_targets) < 6:
            # Get an inactive target from the pool
            available_targets = [t for t in targets if t not in active_targets]
            if available_targets:
                new_target = random.choice(available_targets)
                new_target.reset()
                active_targets.append(new_target)
                last_spawn_time = current_time
                
                # Gradually decrease spawn interval (make game harder)
                if elapsed_time > 30:  # After 30 seconds
                    spawn_interval = max(500, 1000 - (elapsed_time - 30) * 10)
        
        # Check if game time is up
        if remaining_time <= 0:
            if is_high_score(score):
                play_ui_sound("high_score")
                game_state = "enter_name"
                is_new_high_score = True
            else:
                play_ui_sound("game_over")
                game_state = "game_over"
                is_new_high_score = False
        
        # Draw active targets
        for target in active_targets:
            if target.active:
                target.draw()
        
        # Draw score and time
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        time_text = font.render(f"Time: {remaining_time}s", True, BLACK)
        screen.blit(time_text, (WIDTH - 150, 10))
        
        # Draw gun info
        draw_gun_info()
        
    elif game_state == "enter_name":
        draw_background()
        draw_name_entry()
        
    elif game_state == "game_over":
        draw_background()
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        game_over_text = font.render("GAME OVER!", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
        
        restart_text = font.render("Click to return to menu", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 50))
    
    # Draw crosshair (always on top, except during name entry)
    if game_state != "enter_name":
        crosshair.draw()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()