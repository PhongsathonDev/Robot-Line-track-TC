import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Load music
pygame.mixer.music.load("Test/happy.mp3")

# Set volume (0.0 to 1.0)
pygame.mixer.music.set_volume(1)  # 50% volume

# Play music
pygame.mixer.music.play()

# Wait until the music finishes playing
while pygame.mixer.music.get_busy():
    time.sleep(0.5)
