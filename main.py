# Import necessary libraries
import math
import random
from pygame.locals import *
import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the game screen with a resolution of 800x600 pixels
screen = pygame.display.set_mode((800, 600))

# Load the background image for the game
background = pygame.image.load('background.png')

# Load and play the background music in an infinite loop
mixer.music.load("background.wav")
# Uncomment the line below to enable background music
# mixer.music.play(-1)

# Set the caption and icon for the game window
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Initialize score variables
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying the score
textX = 10  # X-coordinate for the score display
testY = 10  # Y-coordinate for the score display

# Player settings
playerImg = pygame.image.load('player.png')  # Load the player image
playerX = 370  # Initial X-coordinate of the player
playerY = 480  # Initial Y-coordinate of the player
playerX_change = 0  # Variable to track player's horizontal movement

# Function to draw the player on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy settings
enemyImg = []  # List to store enemy images
enemyX = []  # List to store enemy X-coordinates
enemyY = []  # List to store enemy Y-coordinates
enemyX_change = []  # List to store enemy horizontal movement speed
enemyY_change = []  # List to store enemy vertical movement speed
num_of_enemies = 6  # Number of enemies in the game

# Create multiple enemies and initialize their properties
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))  # Load enemy image
    enemyX.append(random.randint(0, 736))  # Random initial X-coordinate
    enemyY.append(random.randint(50, 150))  # Random initial Y-coordinate
    enemyX_change.append(2)  # Horizontal movement speed (slower than original)
    enemyY_change.append(20)  # Vertical movement speed (slower than original)

# Function to draw an enemy on the screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Function to display the score on the screen
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))  # Render score text
    screen.blit(score, (x, y))  # Draw the score on the screen

# Bullet settings
bulletImg = pygame.image.load('bullet.png')  # Load bullet image
bulletX = 0  # Initial X-coordinate of the bullet
bulletY = 480  # Initial Y-coordinate of the bullet
bulletX_change = 0  # Horizontal movement speed (not used)
bulletY_change = 10  # Vertical movement speed
bullet_state = "ready"  # State of the bullet: "ready" or "fire"

# Function to fire the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"  # Change bullet state to "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # Draw the bullet on the screen

# Function to detect collision between bullet and enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))  # Calculate distance
    if distance < 27:  # If distance is less than 27 pixels, collision occurs
        return True
    else:
        return False

# Function to set the background (fill with black and draw the background image)
def set_background():
    global background
    screen.fill((0, 0, 0))  # Fill the screen with black color
    screen.blit(background, (0, 0))  # Draw the background image

# Function to handle bullet movement
def move_bullet():
    global bulletX, bulletY, bullet_state
    if bulletY <= 0:  # If bullet goes off-screen, reset its position
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":  # If bullet is in "fire" state, move it upwards
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

# Function to handle game input (keyboard events)
def game_input():
    global running, playerX_change, bulletX, playerX, bulletY
    for event in pygame.event.get():  # Loop through all events
        if event.type == pygame.QUIT:  # If user closes the window, stop the game
            running = False
        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Move player left
                playerX_change = -5
            if event.key == pygame.K_RIGHT:  # Move player right
                playerX_change = 5
            if event.key == pygame.K_SPACE:  # Fire bullet
                if bullet_state == "ready":  # Only fire if bullet is ready
                    bulletSound = mixer.Sound("laser.wav")  # Load laser sound
                    bulletSound.play()  # Play laser sound
                    bulletX = playerX  # Set bullet's X-coordinate to player's X-coordinate
                    fire_bullet(bulletX, bulletY)  # Fire the bullet
        # Handle key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # Stop player movement
                playerX_change = 0
    playerX += playerX_change  # Update player's X-coordinate
    if playerX <= 0:  # Prevent player from moving out of the left boundary
        playerX = 0
    elif playerX >= 736:  # Prevent player from moving out of the right boundary
        playerX = 736

# Function to handle enemy movement
def enemy_movement():
    global enemyX, enemyX_change, enemyY, enemyY_change
    for i in range(num_of_enemies):  # Loop through all enemies
        enemyX[i] += enemyX_change[i]  # Move enemy horizontally
        if enemyX[i] <= 0:  # If enemy hits the left boundary
            enemyX_change[i] = 2  # Reverse horizontal direction
            enemyY[i] += enemyY_change[i]  # Move enemy down
        elif enemyX[i] >= 736:  # If enemy hits the right boundary
            enemyX_change[i] = -2  # Reverse horizontal direction
            enemyY[i] += enemyY_change[i]  # Move enemy down
        enemy(enemyX[i], enemyY[i], i)  # Draw the enemy on the screen

# Function to handle collisions between bullets and enemies
def collision():
    global num_of_enemies, enemyX, enemyY, bulletX, bulletY, bullet_state, score_value
    for i in range(num_of_enemies):  # Loop through all enemies
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)  # Check for collision
        if collision:  # If collision occurs
            explosionSound = mixer.Sound("explosion.wav")  # Load explosion sound
            explosionSound.play()  # Play explosion sound
            bulletY = 480  # Reset bullet position
            bullet_state = "ready"  # Change bullet state to "ready"
            score_value += 1  # Increment score
            enemyX[i] = random.randint(0, 736)  # Respawn enemy at a random X-coordinate
            enemyY[i] = random.randint(50, 150)  # Respawn enemy at a random Y-coordinate

# Main game loop
running = True
while running:
    set_background()  # Set the background
    game_input()  # Handle user input
    enemy_movement()  # Move enemies
    collision()  # Check for collisions
    move_bullet()  # Move the bullet
    player(playerX, playerY)  # Draw the player
    show_score(textX, testY)  # Display the score
    pygame.display.update()  # Update the display
