import random
import os
import getch
# hi Pun - thank you for this impressive submission. Happy to say this is grade 9 standard :)
print("""
Welcome to

_________________________________________
  ____     ___     ____   _   _   _____ 
 |  _ \   / _ \   / ___| | | | | | ____|
 | |_) | | | | | | |  _  | | | | |  _|  
 |  _ <  | |_| | | |_| | | |_| | | |___ 
 |_| \_\  \___/   \____|  \___/  |_____|
_________________________________________

""")
width = int(input("Input grid Width\n"))
height = int(input("Input grid Height\n"))
print("Grid size is set to {} x {}".format(width, height))

#player info

class Coordinates:
	def __init__(self):
		self.x = 0
		self.y = 0

class Entity_stat:
	def __init__(self):
		self.health = 0
		self.coins = 0
		self.alive = True
		self.level = 1

player_stat = Entity_stat()
player_stat.alive = True
player_stat.coins = 0
player_stat.health = 10
player_stat.level = 1
player = Coordinates()
player.x = width // 2
player.y = height // 2

enemy = Coordinates()
enemy.x = 0
enemy.y = 0
enemy_stat = Entity_stat()
enemy_stat.health = 1
enemy_stat.alive = True

enemy1 = Coordinates()
enemy1.x = 0
enemy1.y = 0
enemy1_stat = Entity_stat()
enemy1_stat.health = 1
enemy1_stat.alive = True
print("The player starts at X:{} Y:{}".format(player.x, player.y))

def MovePlayer(player, direction):

	if direction.lower() == "a":
		player.x -= 1
	elif direction.lower() == "d":
		player.x += 1
	elif direction.lower() == "w":
		player.y += 1
	elif direction.lower() == "s":
		player.y -= 1

	check_boundaries(player)
	return player

def MakeGrid():
	grid = []
	in_list = False
	for i in range(height):
		row = []
		for u in range(width):
			n = random.randint(0, 20)
			m = random.randint(0, 20)
			x = random.randint(0, 50)
			y = random.randint(0, 50)
			q = random.randint(0, 50)
			w = random.randint(0, 50)
			if n == m:
				row += 'G'
			elif x == y:
				row += "♥"
			elif q == w and not in_list:
				row += "K"
				in_list = True
			else:
				row += '.'
		grid.append(row)
	return grid

def DisplayGrid(grid):
	Grid = ""
	grid_number = height
	row_number = 0
	for i in range(width + 2):
		Grid += "".join("- ")
	Grid += '\n'
	for row in grid:
		grid_number -= 1
		Grid += '| '
		for cell in row:
			row_number += 1
			if grid_number == player.y and row_number == player.x:
				Grid += "".join("P ")
			elif grid_number == enemy.y and row_number == enemy.x and enemy_stat.alive:
				Grid += "".join("E ")
			elif grid_number == enemy1.y and row_number == enemy1.x and enemy1_stat.alive:
				Grid += "".join("E ")
			else:
				Grid += "".join(cell + " ")
		row_number = 0
		Grid += "|"
		Grid += '\n'
	for i in range(width + 2):
		Grid += "".join("- ")
	print(Grid)

def coin_collection(player, grid, player_stat):
	grid_number = height
	row_number = 0
	collum = 0
	for row in grid:
		grid_number -= 1
		collum += 1
		for cell in row:
			row_number += 1
			# print("player is at {} x {}".format(player.x, player.y))
			# print("y =", collum)
			# print("x =", row_number)
			if cell == 'G' and grid_number == player.y and row_number == player.x:
				cell = '.'
				player_stat.coins += 1
				grid[collum - 1][row_number - 1] = '.'
		row_number = 0

def potion_collection(player, grid, player_stat):
	grid_number = height
	row_number = 0
	collum = 0
	for row in grid:
		grid_number -= 1
		collum += 1
		for cell in row:
			row_number += 1
			# print("player is at {} x {}".format(player.x, player.y))
			# print("y =", collum)
			# print("x =", row_number)
			if cell == '♥' and grid_number == player.y and row_number == player.x:
				cell = '.'
				player_stat.health += 1
				grid[collum - 1][row_number - 1] = '.'
		row_number = 0

def key_collection(player, grid, player_stat):
	grid_number = height
	row_number = 0
	collum = 0
	for row in grid:
		grid_number -= 1
		collum += 1
		for cell in row:
			row_number += 1
			if cell == 'K' and (grid_number == player.y and row_number == player.x):
				cell = '.'
				player_stat.level += 1
				grid[collum - 1][row_number - 1] = '.'
				print("You Have Collected a Key!")
		row_number = 0

def make_enemy(enemy, height, width):
	x = random.randint(1, width)
	y = random.randint(1, height)
	enemy.x = x
	enemy.y = y

def move_enemy(player, enemy, player_stat):
	#print(player.x)
	#print(player.y)
	#print(enemy.x)
	#print(enemy.y)
	if player.x < enemy.x:
		x = [enemy.x - player.x, "right"] #enemy is on the right of the player
	elif player.x > enemy.x:
		x = [player.x - enemy.x, "left"]
	else:
		x = [0,"none"]
	if player.y < enemy.y:
		y = [enemy.y - player.y, "up"] #enemy is above player
	elif player.y > enemy.y:
		y = [player.y - enemy.y, "down"]
	else:
		y = [0, "none"]
	#print(x)
	#print(y)
	if (x[0] == y[0]) or (x[0] == 0 and y[0] == 1) or (y[0] == 0 and x[0] == 1):
		damage_system(attack, player_stat, enemy_stat, enemy)
	elif y[0] > x[0]:
		if y[1] == "up":
			enemy.y -= 1
		elif y[1] == "down":
			enemy.y += 1
	elif x > y:
		if x[1] == "right":
			enemy.x -= 1
		elif x[1] == "left":
			enemy.x += 1
	
	check_boundaries(enemy)


def damage_system(attack, player_stat, entity_stat, entity):
	if player.x < entity.x:
		x = [entity.x - player.x, "right"] #enemy is on the right of the player
	elif player.x > entity.x:
		x = [player.x - entity.x, "left"]
	else:
		x = [0,"none"]

	if player.y < entity.y:
		y = [entity.y - player.y, "up"] #enemy is above player
	elif player.y > entity.y:
		y = [player.y - entity.y, "down"]
	else:
		y = [0, "none"]
	if (x[0] == y[0]) or (x[0] == 0 and y[0] == 1) or (y[0] == 0 and x[0] == 1):
		if not attack and entity_stat.alive:
			player_stat.health -= 1
		else:
			entity_stat.alive = False
			return True
	
def check_boundaries(entity):
	if entity.y < 0:
		entity.y = entity.y + 1
	if entity.x < 1:
		entity.x = entity.x + 1
	if entity.y > height - 1:
		entity.y = entity.y - 1
	if entity.x > width: 
		entity.x = entity.x - 1

def moved_direction(i): 
	if i == "w":
		x = "up"
	elif i == "a":
		x = "left"
	elif i == "s":
		x = "down"
	elif i == "d":
		x = "right"
	
	return x


grid = MakeGrid()
make_enemy(enemy, height, width)
level = 1

while player_stat.alive and player_stat.level == 1:
	key_collection(player, grid, player_stat)
	if player_stat.level != 1:
		continue
	if player_stat.health == 0:
		os.system('clear')
		player_stat.alive = False
		continue
	move = getch.getch()  # need to stop this crashing if i accidentally hit enter!
	os.system('clear')
	print("Level 1")
	if move == "q":
		attack = True
		damage_system(attack, player_stat, enemy_stat, enemy)
	else:
		attack = False
		MovePlayer(player, move)
		moved = moved_direction(move)
		print("you chose to go", moved)
	coin_collection(player, grid, player_stat)
	potion_collection(player, grid, player_stat)
	move_enemy(player, enemy, player_stat)
	print("♥" * player_stat.health)
	print("You have {} coins".format(player_stat.coins))
	print("The player is at X:{} Y:{}".format(player.x, player.y + 1))
	DisplayGrid(grid)

grid = MakeGrid()
make_enemy(enemy, height, width)
make_enemy(enemy1, height, width)
enemy_stat.alive = True

while player_stat.alive and player_stat.level == 2:
	key_collection(player, grid, player_stat)
	if player_stat.level != 2:
		continue
	if player_stat.health == 0:
		os.system('clear')
		player_stat.alive = False
		continue
	move = getch.getch() # what's this? OH i see! very good!
	os.system('clear')
	print("Level 2")
	print(enemy_stat.alive)
	print(enemy1_stat.alive)
	if move == "q":
		attack = True
		damage_system(attack, player_stat, enemy_stat, enemy)
		damage_system(attack, player_stat, enemy1_stat, enemy1)
	else:
		attack = False
		MovePlayer(player, move)
		moved = moved_direction(move)
		print("you chose to go", moved)
	coin_collection(player, grid, player_stat)
	potion_collection(player, grid, player_stat)
	move_enemy(player, enemy, player_stat)
	move_enemy(player, enemy1, player_stat)
	print("♥" * player_stat.health)
	print("You have {} coins".format(player_stat.coins))
	print("The player is at X:{} Y:{}".format(player.x, player.y + 1))
	DisplayGrid(grid)

if not player_stat.alive:
	print("""
	 __   __                    ____    _              _ 
	 \ \ / /   ___    _   _    |  _ \  (_)   ___    __| |
	  \ V /   / _ \  | | | |   | | | | | |  / _ \  / _` |
	   | |   | (_) | | |_| |   | |_| | | | |  __/ | (_| |
	   |_|    \___/   \__,_|   |____/  |_|  \___|  \__,_|
	
	""")
else:
	print("""
	  _____   _                _____               _ 
	 |_   _| | |__     ___    | ____|  _ __     __| |
	   | |   | '_ \   / _ \   |  _|   | '_ \   / _` |
	   | |   | | | | |  __/   | |___  | | | | | (_| |
	   |_|   |_| |_|  \___|   |_____| |_| |_|  \__,_|
                                                 
	""")
