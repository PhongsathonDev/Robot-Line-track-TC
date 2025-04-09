import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Load and play music
pygame.mixer.music.load("sound.mp3")
pygame.mixer.music.play()

# Wait for it to finish
while pygame.mixer.music.get_busy():
    time.sleep(0.5)
