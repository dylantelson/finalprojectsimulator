import random
import modules
import pygame
import time
from pygame.locals import *

class ClassController():

	def __init__(self):
		pygame.init()
		pygame.font.init()
		font = pygame.font.SysFont('Comic Sans MS', 22)
		pygame.mixer.init()
		pygame.display.set_caption("Parkour Simulator 2017")
		clock = pygame.time.Clock()

		screen_width = 640
		screen_height = 480


		screen = pygame.display.set_mode([screen_width, screen_height])
		runnerboy = modules.MainCharacter((50, 249))

		randomfloory = 300

		floors = [modules.Floor((50, randomfloory))]
		randomfloory += random.randint(-50, 50)
		floors.append(modules.Floor((250, randomfloory)))
		randomfloory += random.randint(-50, 50)
		floors.append(modules.Floor((450, randomfloory)))
		randomfloory += random.randint(-50, 50)
		floors.append(modules.Floor((650, randomfloory)))

		powerups = []
		powerupscooldown = 0

		score = 0


		loop = True
		while loop:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						runnerboy.jump()
					elif event.key == pygame.K_DOWN:
						runnerboy.maxyspeed = 7
						runnerboy.gravitymultiplier = 5
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_DOWN:
						if powerupscooldown > 0:
							runnerboy.gravitymultiplier = 0.5
						else:
							runnerboy.gravitymultiplier = 1
						runnerboy.maxyspeed = 6

				if event.type == pygame.QUIT:
					loop = False

			for i in range(len(floors)):
				if floors[i].x + 150 < 0:
					randomfloory += random.randint(-50, 50)
					if randomfloory >= 420:
						randomfloory = 420
					elif randomfloory <= 60:
						randomfloory = 60
					floors[i] = modules.Floor((700, randomfloory))
					if random.randint(0,2) == 1:
						powerups.append(modules.Powerup((750, randomfloory - 43)))

			screen.fill((100,100,100))

			speed = runnerboy.speed

			if powerupscooldown > 0:
				powerupscooldown -= 1
				if powerupscooldown <= 0:
					runnerboy.gravitymultiplier = 1


			for i in range(len(floors)):
				floors[i].always(speed)
				screen.blit(floors[i].image, (floors[i].x, floors[i].y))

			for i in range(len(powerups)):
				powerups[i].always(speed)
				screen.blit(powerups[i].image, (powerups[i].x, powerups[i].y))
				if pygame.sprite.collide_rect(runnerboy, powerups[i]):
					if powerups[i].type == "chair":
						runnerboy.speed -= 1
						del powerups[i]
					elif powerups[i].type == "gravity":
						runnerboy.gravitymultiplier = 0.5
						del powerups[i]
						powerupscooldown = 150
					if len(powerups) > 0:
						for i in range(i, len(powerups)):
							powerups[i].always(speed)
							screen.blit(powerups[i].image, (powerups[i].x, powerups[i].y))
					break
				if powerups[i].x + 62 < 0:
					del powerups[i]
					if len(powerups) > 0:
						for i in range(i, len(powerups)):
							powerups[i].always(speed)
							screen.blit(powerups[i].image, (powerups[i].x, powerups[i].y))
					break

			runnerboy.always(floors,powerups)
			screen.blit(runnerboy.image, (runnerboy.x, runnerboy.y))

			if runnerboy.y > 480:
				loop = False

			score += 1

			scoretext = font.render((str(('Score: ' + str(score)))), True, (0,0,0))
			screen.blit(scoretext, (10, 10))

			if powerupscooldown > 0:
				screen.blit(font.render(('Gravity: ' + str(powerupscooldown)), True, (0,0,0)), (10, 25))

			pygame.display.update()
			clock.tick(60)

main = ClassController()
