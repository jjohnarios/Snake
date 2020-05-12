import pygame
import time
import random
import os

class Cube():
	def __init__(self):
		self.width=int(display_width/20)
		self.height=int(display_height/20) # (40,40)
		self.x=-1
		self.y=-1
		pass

	def spawnCube(self,covered):
		'''
		Random spawn of Cube that snake tries to eat

		Attributes
		----------
		covered: snake's body
		'''

		x=random.randrange(20)
		y=random.randrange(1,20)
		x*=self.width
		y*=self.height
		while [x,y]  in covered: 
			x=random.randrange(1,20)
			y=random.randrange(1,20)
			x*=self.width
			y*=self.height
		self .x=x
		self.y=y
		pygame.draw.rect(screen,RED,(x,y,self.width,self.height))
		


class Score():
	'''
	Score of the game. Starts from 0.
	Every time the snake eats the cube score is being incremented by 10.
	'''
	def __init__(self):
		self.score=0 
		self.score_font=pygame.font.SysFont(None,50)

	def update(self):
		self.score+=10

	def draw(self):
		screen.fill(BLACK,(0,0,display_width,35))
		screen.blit(self.score_font.render("SCORE: "+ str(self.score),1,RED,None),(580,0))





class Snake:
	def __init__(self,name):
		self.name=name
		self.head=[400,400] #initial start position of snake
		self.restBody=[]
		self.tail=[]
		self.direction=None
		self.body=[self.head]

	def move(self,direction):
		if direction=="Left":
			self.direction="Left"
			return self.moveLeft()
		elif direction=="Right":
			self.direction="Right"
			return self.moveRight()
		elif direction=="Up":
			self.direction="Up"
			return self.moveUp()
		elif direction=="Down":
			self.direction="Down"
			return self.moveDown()

	def draw(self):
		for cb in self.body:
			pygame.draw.rect(screen,GREEN,(cb[0],cb[1],40,40))	


	def moveLeft(self):
		if self.head[0]-40 >= 0:
			self.clean()
			self.moveRestBodyAndTail()
			self.head[0]-=40
			self.body[0]=list(self.head)
		else:
			return self.game_loss()


	def moveRight(self):
		if self.head[0]+40 < display_width:
			self.clean()
			self.moveRestBodyAndTail()
			self.head[0]+=40

			self.body[0]=list(self.head)
		else:
			return self.game_loss()
	def moveUp(self):
		if self.head[1]-40 >=20:
			self.clean()
			self.moveRestBodyAndTail()
			self.head[1]-=40
			
			self.body[0]=list(self.head)
		else:
			return self.game_loss()

	def moveDown(self):
		if self.head[1]+40< display_height:
			self.clean()
			self.moveRestBodyAndTail()
			self.head[1]+=40
			self.body[0]=list(self.head)
		else:
			return self.game_loss()

	# Rest Body and Tail follow head 
	def moveRestBodyAndTail(self):
		if self.tail==[]:
			return
		if self.tail!=[] and self.restBody==[]:
			self.tail=list(self.head)
			self.body[len(self.body)-1]=list(self.tail)
		else:
			self.tail=list(self.restBody[len(self.restBody)-1])
			self.body.pop()
			self.restBody[0]=list(self.head)
			for i in range(1, len(self.restBody)):
				self.restBody[i]=list(self.restBody[i-1])
				if self.restBody[i] not in self.body:
					self.body.append(self.restBody[i])
			self.body.insert(0,[])
			

	# Clean to redraw
	def clean(self):
		for cb in self.body:
			pygame.draw.rect(screen,BLACK,(cb[0],cb[1],40,40))
			pygame.draw.rect(screen,(0,0,188),(cb[0],cb[1],40,40),3)

	def game_loss(self):
		print("Score= ",score.score)
		return True

	def eats(self):

		# Initial State , when snake is one cube
		if self.tail==[] and self.direction!=None:
			self.updateTail()
		elif self.tail!=[] and self.direction!=None:
			self.restBody.append(list(self.tail)) 
			for i in self.restBody:
				if i not in self.body:
					self.body.append(list(i))

			self.updateTail()
		
		self.body.append(self.tail)

	def updateTail(self):
		move=40
		if self.tail==[]:
			self.tail=list(self.head)
		if self.direction=="Left":
			self.tail[0]+=move
		if self.direction=="Right":
			self.tail[0]-=move
		if self.direction=="Up":
			self.tail[1]+=move
		if self.direction=="Down":
			self.tail[1]-=move


def createGrid():
	'''
	Draws a 20x20 Grid with 40x40 rectangles with outlines
	'''
	mainGrid=[]

	for i in range(20):
		l=[]
		for j in range(20):
			if i==0:
				x=1
			else:
				x=int(40*i)
			if j==0:
				y=40
			else:
				y=int(40*j)
			l.append(pygame.draw.rect(screen,(0,0,188),(x,y,40,40),3))
		mainGrid.append(l)

#for displaying text
def text_objects(text,color):
	text=font.render(text,True,color)
	return text,text.get_rect()


def message_to_screen(msg,color,displayW,displayH):
	text,textRect=text_objects(msg, color)
	textRect.center=(displayW,displayH)
	screen.blit(text,textRect)


def startingPage():
	'''
	Starting Page, Press ENTER or ESCAPE
	'''
	start=True

	while start:
		screen.fill(WHITE)
		for event in pygame.event.get():
			if event.type== pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					#start =False
					return True
				if event.key== pygame.K_ESCAPE:
					return False

		message_to_screen("PRESS ENTER TO START PLAYING", GREEN, display_width/2, display_height/2-30)
		message_to_screen("PRESS ESCAPE TO QUIT", GREEN, display_width/2, display_height/2)
		clock.tick(FPS)
		pygame.display.update()
	return True




# SETTINGS
display_width=800
display_height=800
FPS=13



pygame.init()
os.environ['SDL_VIDEO_CENTERED']='1'
screen=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Snake")
icon =pygame.image.load("snake.png")
pygame.display.set_icon(icon)

#In game Sounds
# used when jazzPiano.wav is available
#in_game_music=pygame.mixer.Sound("jazzPiano.wav")
#in_game_music.set_volume(0.05)
lose_music=pygame.mixer.Sound("lose.wav")
lose_music.set_volume(0.05)
eating_music=pygame.mixer.Sound("eating.wav")
eating_music.set_volume(0.05)

clock=pygame.time.Clock()
RED=(255,0,0)
GREEN=(0,255,0)
BLACK=(0,0,0)
WHITE=(255,255,255)
score=Score()
cube=Cube()
snake=Snake("John")

#used font for starting screen
font=pygame.font.SysFont(None,30)



if startingPage()==False:
	running=False
else:
	screen.fill(BLACK)
	createGrid()
	running=True
	direction=None
	end=False
	gameLoss=False
	eaten=False
	cube.spawnCube(snake.body)

#pygame.mixer.Channel(0).play(in_game_music,-1)	

# Game Loop (should be a function)

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running=False

		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_LEFT and direction!="Right":
				direction="Left"
			elif event.key==pygame.K_RIGHT and direction!="Left":
				direction="Right"
			elif event.key==pygame.K_DOWN and direction!="Up":
				direction="Down"
			elif event.key==pygame.K_UP and direction!="Down":
				direction="Up"


	if direction:
		gameLoss=snake.move(direction)



		#snake runs on itself
	for i in snake.body[1:]:
		if i==snake.head:
			gameLoss=True

		
	if gameLoss:
		pygame.mixer.Channel(0).stop()
		pygame.mixer.Channel(1).play(lose_music,0)
		time.sleep(3.3)
		running=False
		
	# Snake eats the cube
	if snake.head[0]==cube.x and snake.head[1]==cube.y:
		pygame.mixer.Channel(1).play(eating_music,0)
		eaten=True

	if eaten==True:
		snake.eats()
		score.update()
		cube.spawnCube(snake.body)
	eaten=False

	
	snake.draw()
	score.draw()
	pygame.display.update()
	clock.tick(FPS)


pygame.quit()
exit()