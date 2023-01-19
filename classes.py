import pygame


def checkCollision(posA, As, posB, Bs):
    if posA.x < posB.x + Bs and posA.x + As > posB.x and posA.y < posB.y + Bs and posA.y + As > posB.y:
        return True
    return False


keys = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}
sep = 10


class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = keys["UP"]
        self.color = "white"


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = keys["UP"]
        self.stack = []

        self.stack.append(self)

        blackBox = Segment(self.x, self.y + sep)
        blackBox.direction = keys["UP"]
        blackBox.color = "NULL"
        self.stack.append(blackBox)

    def move(self, sn_sp, FPS):
        last_element = len(self.stack) - 1
        while last_element != 0:
            self.stack[last_element].direction = self.stack[last_element - 1].direction
            self.stack[last_element].x = self.stack[last_element - 1].x
            self.stack[last_element].y = self.stack[last_element - 1].y
            last_element -= 1
        if len(self.stack) < 2:
            last_segment = self
        else:
            last_segment = self.stack.pop(last_element)
        last_segment.direction = self.stack[0].direction
        if self.stack[0].direction == keys["UP"]:
            last_segment.y = self.stack[0].y - (sn_sp * FPS)
        elif self.stack[0].direction == keys["DOWN"]:
            last_segment.y = self.stack[0].y + (sn_sp * FPS)
        elif self.stack[0].direction == keys["LEFT"]:
            last_segment.x = self.stack[0].x - (sn_sp * FPS)
        elif self.stack[0].direction == keys["RIGHT"]:
            last_segment.x = self.stack[0].x + (sn_sp * FPS)
        self.stack.insert(0, last_segment)

    def getHead(self):
        return self.stack[0]

    def grow(self, sn_size):
        last_element = len(self.stack) - 1
        self.stack[last_element].direction = self.stack[last_element].direction
        if self.stack[last_element].direction == keys["UP"]:
            newSegment = Segment(self.stack[last_element].x, self.stack[last_element].y - sn_size)
            blackBox = Segment(newSegment.x, newSegment.y - sep)

        elif self.stack[last_element].direction == keys["DOWN"]:
            newSegment = Segment(self.stack[last_element].x, self.stack[last_element].y + sn_size)
            blackBox = Segment(newSegment.x, newSegment.y + sep)

        elif self.stack[last_element].direction == keys["LEFT"]:
            newSegment = Segment(self.stack[last_element].x - sn_size, self.stack[last_element].y)
            blackBox = Segment(newSegment.x - sep, newSegment.y)

        elif self.stack[last_element].direction == keys["RIGHT"]:
            newSegment = Segment(self.stack[last_element].x + sn_size, self.stack[last_element].y)
            blackBox = Segment(newSegment.x + sep, newSegment.y)

        blackBox.color = "NULL"
        self.stack.append(newSegment)
        self.stack.append(blackBox)

    def iterateSegments(self, delta):
        pass

    def setDirection(self, direction):
        if (self.direction == keys["RIGHT"] and
                direction == keys["LEFT"] or self.direction == keys["LEFT"] and direction == keys["RIGHT"]):
            pass
        elif (self.direction == keys["UP"] and direction == keys["DOWN"] or self.direction == keys[
            "DOWN"] and direction ==
              keys["UP"]):
            pass
        else:
            self.direction = direction

    def get_rect(self):
        rect = (self.x, self.y)
        return rect

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def checkCrash(self, sn_size):
        counter = 1
        while (counter < len(self.stack) - 1):
            if (checkCollision(self.stack[0], sn_size, self.stack[counter], sn_size) and self.stack[
                counter].color != "NULL"):
                return True
            counter += 1
        return False

    def draw(self, screen, sn_size):
        pygame.draw.rect(screen, pygame.color.Color("yellow"),
                         (self.stack[0].x, self.stack[0].y, sn_size, sn_size), 0)
        counter = 1
        while counter < len(self.stack):
            if self.stack[counter].color == "NULL":
                counter += 1
                continue
            pygame.draw.rect(screen, pygame.color.Color("white"),
                             (self.stack[counter].x, self.stack[counter].y, sn_size, sn_size), 0)
            counter += 1


class Apple:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.color.Color("red")

    def draw(self, screen, ap_size):
        pygame.draw.rect(screen, self.color, (self.x, self.y, ap_size, ap_size), 0)
