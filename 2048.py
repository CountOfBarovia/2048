# 2048 puzzle game

# Setup
import pygame, random
pygame.init()
pygame.display.init()
Time = pygame.time.Clock()
Clean = pygame.font.Font("Game Art/Fonts/Roboto-Light.ttf", 50)
Pixel = pygame.font.Font("Game Art/Fonts/Crang.ttf", 50)

# Window setup
ScreenW = 400
ScreenH = 400
Screen = pygame.display.set_mode((ScreenW, ScreenH))
pygame.display.set_caption("2048")
Blank = pygame.image.load("Game Art/Blank.png")
pygame.display.set_icon(Blank)

# Subroutine to convert a grid position to list position
def Convert(Grid):
        Pos = Grid[1] * 4
        Pos += Grid[0]
        Pos = int(Pos)
        return Pos

# Subroutine to convert a list position to grid position
def Back(Pos):
        x = (Pos % 4)
        Pos -= x
        y = Pos / 4
        return (x, y)

# Creating the squares
Pos = (20, 20)
Size = (75, 75)
class Number(pygame.sprite.Sprite):
        def __init__(self, num, col, pos):
                pygame.sprite.Sprite.__init__(self)
                self.num = num
                self.text = Clean.render(num, True, (255, 255, 255))
                if len(num) > 2:
                        Scale = 60 / self.text.get_width()
                        self.text = pygame.transform.scale_by(self.text, Scale)
                self.block = pygame.rect.Rect(pos, Size)
                self.block.topleft = pos
                self.col = col
                self.textrect = pygame.Surface.get_rect(self.text)
                self.textrect.center = self.block.center
        def update(self):
                pygame.draw.rect(Screen, self.col, self.block)
                pygame.Surface.blit(Screen, self.text, self.textrect)
        def move(self, pos, Direction, list):
                if self.num != " ":
                        Grid = Back(pos)
                        New = (Grid[0], Grid[1])
                        Newpos = Convert(New)
                        Done = False
                        while Direction != (0, 0) and not Done:
                                New = (New[0] + Direction[0], New[1] + Direction[1])
                                Newpos = Convert(New)
                                if New[0] == 4 and Direction == (1, 0):
                                        New = (New[0] - Direction[0], New[1] - Direction[1])
                                        Newpos = Convert(New)
                                        Done = True
                                elif New[0] == -1 and Direction == (-1, 0):
                                        New = (New[0] - Direction[0], New[1] - Direction[1])
                                        Newpos = Convert(New)
                                        Done = True
                                elif New[1] == 4 and Direction == (0, 1):
                                        New = (New[0] - Direction[0], New[1] - Direction[1])
                                        Newpos = Convert(New)
                                        Done = True
                                elif New[1] == -1 and Direction == (0, -1):
                                        New = (New[0] - Direction[0], New[1] - Direction[1])
                                        Newpos = Convert(New)
                                        Done = True
                                elif list[Newpos] != 0:
                                        if int(self.num) == list[Newpos]:
                                                list[pos] = 0
                                                list[Newpos] = int(self.num) * 2
                                                return list
                                        else:
                                                New = (New[0] - Direction[0], New[1] - Direction[1])
                                                Newpos = Convert(New)
                                        Done = True
                        list[pos] = 0
                        list[Newpos] = int(self.num)
                return list

# Subroutine to set a square to a number
def set(Value, Pos):
        if Value == 0:
                return Number(" ", (150, 221, 250), Pos)
        elif Value == 2:
                return Number("2", (54, 182, 255), Pos)
        elif Value == 4:
                return Number("4", (54, 88, 255), Pos)
        elif Value == 8:
                return Number("8", (80, 88, 220), Pos)
        elif Value == 16:
                return Number("16", (100, 70, 200), Pos)
        elif Value == 32:
                return Number("32", (120, 60, 180), Pos)
        elif Value == 64:
                return Number("64", (140, 50, 160), Pos)
        elif Value == 128:
                return Number("128", (150, 40, 150), Pos)
        elif Value == 256:
                return Number("256", (160, 40, 140), Pos)
        elif Value == 512:
                return Number("512", (180, 30, 120), Pos)
        elif Value == 1024:
                return Number("1024", (200, 30, 100), Pos)
        elif Value == 2048:
                return Number("2048", (220, 0, 60), Pos)

# Subroutine to transfer a list of numbers to a group of sprites
def transfer(Numbers, Group):
        Pos = (20, 20)
        Group.empty()
        for Number in Numbers:
                Square = set(Number, Pos)
                Pos = (Pos[0] + 95, Pos[1])
                if Pos[0] >= 400:
                        Pos = (20, Pos[1] + 95)
                Group.add(Square)
        return Group

# Subroutine to add a random 2 or 4. Returns False if there is no space.
def Add(Numbers):
        Spaces = []
        for i in range(0, len(Numbers)):
                if Numbers[i] == 0:
                        Spaces.append(Back(i))
        if len(Spaces) == 0:
                return Numbers
        else:
                Pos = random.choice(Spaces)
                Nums = [2, 2, 2, 2, 4]
                Num = random.choice(Nums)
                for i in Spaces:
                        if i == Pos:
                                Numbers[Convert(i)] = Num
                return Numbers

Direction = (0, 0)

# Make the text
Font = pygame.font.Font("Game Art/Fonts/Crang.ttf", 50)
Font2 = pygame.font.Font("Game Art/Fonts/pixel.ttf", 25)
EndText = Font.render("GAME OVER!", False, (255, 0, 0))
EndText_Rect = pygame.Surface.get_rect(EndText)
EndText_Rect.center = (ScreenW / 2, ScreenH / 4)
EndText2 = Font2.render("Press Enter to", False, (255, 0, 0))
EndText2_Rect = pygame.Surface.get_rect(EndText2)
EndText2_Rect.center = (ScreenW / 2, ScreenH / 2)
EndText3 = Font2.render("play again!", False, (255, 0, 0))
EndText3_Rect = pygame.Surface.get_rect(EndText3)
EndText3_Rect.center = (ScreenW / 2, ScreenH / 2 + 30)

# Full loops
while True:
        
        # Create/reset the lists of squares
        Numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        Numbers = Add(Numbers)
        Numbers = Add(Numbers)
        Squares = pygame.sprite.Group()
        Squares = transfer(Numbers, Squares)
        
        # Starting loop
        Game = False
        while not Game:

                # Clear the screen
                Screen.fill((166, 250, 255))

                # Check for inputs
                Events = pygame.event.get()
                for Event in Events:
                        if Event.type == pygame.KEYDOWN:
                                if Event.key == pygame.K_UP:
                                        Direction = (0, -1)
                                        Game = True
                                elif Event.key == pygame.K_RIGHT:
                                        Direction = (1, 0)
                                        Game = True
                                elif Event.key == pygame.K_DOWN:
                                        Direction = (0, 1)
                                        Game = True
                                elif Event.key == pygame.K_LEFT:
                                        Direction = (-1, 0)
                                        Game = True
                
                # Draw the squares
                Squares = transfer(Numbers, Squares)
                Squares.update()

                # Update the display
                pygame.display.update()

                # Limit frame rate
                Time.tick(40)

        # Game loop
        while Game:

                # Clear the screen
                Screen.fill((166, 250, 255))

                # Check for inputs
                Events = pygame.event.get()
                for Event in Events:
                        if Event.type == pygame.KEYDOWN:
                                if Event.key == pygame.K_UP:
                                        Direction = (0, -1)
                                elif Event.key == pygame.K_RIGHT:
                                        Direction = (1, 0)
                                elif Event.key == pygame.K_DOWN:
                                        Direction = (0, 1)
                                elif Event.key == pygame.K_LEFT:
                                        Direction = (-1, 0)
                
                # Draw the squares
                Done = 0
                if Direction == (0, 1) or Direction == (1, 0):
                        Pos = 15
                        for Square in reversed(list(Squares)):
                                LastNum = Numbers[Pos]
                                Numbers = Square.move(Pos, Direction, Numbers)
                                if Numbers[Pos] == LastNum:
                                        Done += 1
                                Pos -= 1
                elif Direction != (0, 0):
                        Pos = 0
                        for Square in Squares:
                                LastNum = Numbers[Pos]
                                Numbers = Square.move(Pos, Direction, Numbers)
                                if Numbers[Pos] == LastNum:
                                        Done += 1
                                Pos += 1
                if Direction != (0, 0):
                        print(Done)
                if Done == 16 and 0 not in Numbers:
                        Game = False
                if Direction != (0, 0):
                        Numbers = Add(Numbers)
                Squares = transfer(Numbers, Squares)
                Squares.update()

                # Update the display
                pygame.display.update()

                # Reset the movement
                Direction = (0, 0)

                # Limit frame rate
                Time.tick(40)

        # End game loop
        while not Game:
                
                # Clear the screen
                Screen.fill((166, 250, 255))

                # Check for inputs
                Events = pygame.event.get()
                for Event in Events:
                        if Event.type == pygame.KEYDOWN:
                                if Event.key == pygame.K_RETURN:
                                        Game = True
                
                # Draw the squares
                Squares = transfer(Numbers, Squares)
                Squares.update()

                # Print the text
                pygame.Surface.blit(Screen, EndText, EndText_Rect)
                pygame.Surface.blit(Screen, EndText2, EndText2_Rect)
                pygame.Surface.blit(Screen, EndText3, EndText3_Rect)
                
                # Update the display
                pygame.display.update()
                
                # Limit frame rate
                Time.tick(40)
