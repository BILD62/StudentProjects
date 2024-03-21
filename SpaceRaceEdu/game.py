import pyxel
import random
import math

###CONFIGURATION VARIABLES
# Set to help easily change the variables in future coding revise
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
PLAYER_SPEED = 3
QUESTIONBOX_CENTER_Y = 100
QUESTIONBOX_WIDTH = 130
QUESTIONBOX_HEIGHT = 30
QUESTIONBOX_COLOR = 15
QUESTIONTEXT_COLOR = 0
ANSWER_CIRCLE_RADIUS = 35
PLAYER_SIZE = 30
CENTER_SAFE_ZONE_RADIUS = 80
METEOR_COLOR = 13


###HELPER FUNCTIONS
def estimateTextSize(text):
    # We estimate how much we need to shift to the left for the text to be centered
    return len(text) * 3


def getDistance(x1, y1, x2, y2):
    dX = x2 - x1
    dY = y2 - y1
    # We calculate the distance between two points.
    return math.sqrt(dX * dX + dY * dY)


def isInSafezone(x, y):
    # We check that the xy are not too close to the middle
    # Error Handling: we need to prevent immediate collisions with the meteor or overlapping with the player's spawn point
    if (x > (SCREEN_WIDTH / 2) - CENTER_SAFE_ZONE_RADIUS) and (x < (SCREEN_WIDTH / 2) + CENTER_SAFE_ZONE_RADIUS):
        if (y > (SCREEN_HEIGHT / 2) - CENTER_SAFE_ZONE_RADIUS) and (y < (SCREEN_HEIGHT / 2) + CENTER_SAFE_ZONE_RADIUS):
            return True

    return False


class Player:
    def __init__(self, id):
        """
        We construct the players ship with a set of player parts.
        """
        self.id = id
        self.score = 0
        self.resetPosition()
        self.radius = 16

    def resetPosition(self):
        """
        We set the player to be in the middle of the screen.
        """
        self.X = SCREEN_WIDTH / 2
        self.Y = SCREEN_HEIGHT / 2

    def collidesWith(self, x, y, size):
        """
        Given an object in space,
        check if the object collides with this player (circle).
        We do this by checking if the distance to the center of the circle
        is less or equal to the sum of the radius of the player and the object.

        Args:
            x (int): x coordinate in space
            y (int): y coordinate in space
            size (int): size of the other object

        Returns:
            boolean: True if collision
        """
        directionVectorLength = getDistance(x, y, self.X, self.Y)
        if (directionVectorLength <= self.radius + size):
            return True
        else:
            return False

    def draw(self):
        if self.id == 1:
            pyxel.blt(self.X - 16, self.Y - 16, 0, 0, 0, 32, 32, pyxel.COLOR_WHITE)
        else:
            pyxel.blt(self.X - 16, self.Y - 16, 0, 32, 0, 32, 32, pyxel.COLOR_WHITE)

    def updateMovement(self):
        """
        We check the keyboard state and move the player accordingly.
        Player with id 1 moves with the arrow keys.
        Player with id 2 moves with WASD
        """
        if (self.id == 1):
            if pyxel.btn(pyxel.KEY_UP) and self.Y > 0 + PLAYER_SPEED:
                self.Y -= PLAYER_SPEED
            # Error Handling: we check two players won't be out of the screen
            if pyxel.btn(pyxel.KEY_DOWN) and self.Y < SCREEN_HEIGHT - PLAYER_SPEED:
                self.Y += PLAYER_SPEED

            if pyxel.btn(pyxel.KEY_RIGHT) and self.X < SCREEN_WIDTH - PLAYER_SPEED:
                self.X += PLAYER_SPEED
            if pyxel.btn(pyxel.KEY_LEFT) and self.X > 0 + PLAYER_SPEED:
                self.X -= PLAYER_SPEED

        elif (self.id == 2):
            if pyxel.btn(pyxel.KEY_W) and self.Y > 0 + PLAYER_SPEED:
                self.Y -= PLAYER_SPEED
            if pyxel.btn(pyxel.KEY_S) and self.Y < SCREEN_HEIGHT - PLAYER_SPEED:
                self.Y += PLAYER_SPEED

            if pyxel.btn(pyxel.KEY_D) and self.X < SCREEN_WIDTH - PLAYER_SPEED:
                self.X += PLAYER_SPEED
            if pyxel.btn(pyxel.KEY_A) and self.X > 0 + PLAYER_SPEED:
                self.X -= PLAYER_SPEED

    def update(self):
        self.updateMovement()


class Meteor:
    def __init__(self, x, y, radius):
        """
        We create a meteor in space

        Args:
            x (int): desired x coordinate
            y (int): desired y coordinate
            radius (int): desired size
        """
        self.X = x
        self.Y = y
        self.radius = radius

    def draw(self):
        pyxel.circ(self.X, self.Y, self.radius, METEOR_COLOR)

    def collidesWithPlayer(self, playerObject):
        """
        Given a player object, check if we (the meteor) collide with the player
        Args:
            playerObject (Player): the player to check

        Returns:
            boolean: True if collision, else false
        """
        return playerObject.collidesWith(self.X, self.Y, self.radius)


class Question:
    def __init__(self, question):
        """
        Every question consists of a question text,
        as well as a list of potential answers

        Args:
            question (string): the question as a text
        """
        self.question = question
        self.potentialAnswers = []

    def addPotentialAnswer(self, answer):
        self.potentialAnswers.append(answer)

    def getPlayerSelectedAnswer(self, player):
        for answer in self.potentialAnswers:
            if answer.collidesWithPlayer(player):
                return answer

        return None

    def removePotentialAnswer(self, answer):
        if answer in self.potentialAnswers:
            self.potentialAnswers.remove(answer)

    def draw(self):
        textSize = estimateTextSize(self.question) * 1.7
        # First we draw a box
        pyxel.rect(SCREEN_WIDTH / 2 - (QUESTIONBOX_WIDTH / 2), QUESTIONBOX_CENTER_Y - (QUESTIONBOX_HEIGHT / 2),
                   QUESTIONBOX_WIDTH, QUESTIONBOX_HEIGHT, QUESTIONBOX_COLOR)
        # Then we draw the text
        pyxel.text(SCREEN_WIDTH / 2 - (textSize / 2), QUESTIONBOX_CENTER_Y - 5, self.question, QUESTIONTEXT_COLOR)
        for answer in self.potentialAnswers:
            answer.draw()


class Vocabulary:
    def __init__(self, word, translation, type):
        self.word = word
        self.translation = translation
        self.type = type


class Answer:
    def __init__(self, text, isRight, x, y):
        """
        Every answer consists of the text,
        the information if it is the right answer or not,
        and the x and y coordinate of the answer bubble.

        Args:
            text (string): text of the answer
            isRight (bool): is this the right answer?
            x (int): x coordinate
            y (int): y coordinate
        """
        self.text = text
        self.isRight = isRight
        self.X = x
        self.Y = y

    def draw(self):
        """
        We draw the potential answer.
        We first draw a circle and then put the text inside
        """
        pyxel.circ(self.X, self.Y, ANSWER_CIRCLE_RADIUS, 7)
        # We estimate how much we need to shift to the left for the text to be centered
        textSize = estimateTextSize(self.text) * 1.5
        pyxel.text(self.X - (textSize / 2), self.Y - 4, self.text, 0)

    def collidesWithPlayer(self, playerObject):
        """
        Given a player object, check if we (the answer) collide with the player
        Args:
            playerObject (Player): the player to check

        Returns:
            boolean: True if collision, else false
        """
        return playerObject.collidesWith(self.X, self.Y, ANSWER_CIRCLE_RADIUS)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="TDYYJ - Space Race Edu")
        #We set up drawings.pyxres to players to draw the shape of them
        pyxel.load("drawings.pyxres")
        self.players = [Player(1), Player(2)]
        self.meteors = []
        self.vocabularies = []
        self.vocabulariesByType = {}
        self.loadVocabularies()
        self.resetRound()

        pyxel.run(self.update, self.draw)

    def loadVocabularies(self):
        self.vocabularies = []
        # vocabulary is a comma separated file with Format: Word, Solution, Type
        file = open("vocabulary.txt", mode="r", encoding="utf-8")
        lines = file.readlines()
        for line in lines:
            values = line.split(",")
            if len(values) != 3:
                print("(ERROR) Invalid vocabulary entry:")  # Error Handling
                print(line)
            else:
                newVoc = Vocabulary(values[0], values[1], values[2])
                self.vocabularies.append(newVoc)
                if not newVoc.type in self.vocabulariesByType:
                    self.vocabulariesByType[newVoc.type] = []

                self.vocabulariesByType[newVoc.type].append(newVoc)

    def generateQuestion(self):
        # We randomly select a vocabulary
        vocab = self.vocabularies[random.randint(0, len(self.vocabularies) - 1)]
        self.currentQuestion = Question(vocab.word)
        # We add the right answer to our potential answer list, we place all questions far away for now
        self.currentQuestion.addPotentialAnswer(Answer(vocab.translation, True, -100, -100))
        # We grab 7 other random answers of the same type
        otherAnswers = random.sample(self.vocabulariesByType[vocab.type],
                                     min(7, len(self.vocabulariesByType[vocab.type])))
        # Check if we got the same answer twice, we make a word set
        words = set()
        words.add(vocab.translation)
        for otherAnswer in otherAnswers:
            words.add(otherAnswer.translation)

        if len(words) < 8:
            # If there are not enough unique words of that type or we grabbed the actual answer, we just try to add other random vocabularies
            tries = 0
            while (len(words) < 8 and tries < 100):
                tries += 1
                otherVocab = self.vocabularies[random.randint(0, len(self.vocabularies) - 1)]
                words.add(otherVocab.translation)

        # We add the potential answers
        print(words)
        for word in words:
            if word != vocab.translation:
                print(word)
                self.currentQuestion.addPotentialAnswer(Answer(word, False, -100, -100))

        # We randomly place all the answers, but far from the center and far from each other
        for answer in self.currentQuestion.potentialAnswers:
            # We search for a random position
            for i in range(1000):
                x = pyxel.rndi(20, SCREEN_WIDTH - 20)
                y = pyxel.rndi(20, SCREEN_HEIGHT - 20)
                # First we check that the xy are not too close to the middle
                if isInSafezone(x, y):
                    continue

                if (x > SCREEN_WIDTH / 2 - (
                        QUESTIONBOX_WIDTH / 2) - 25 and x < SCREEN_WIDTH / 2 + QUESTIONBOX_WIDTH + 25):
                    if (y > QUESTIONBOX_CENTER_Y - (
                            QUESTIONBOX_HEIGHT / 2) - 25 and y < QUESTIONBOX_CENTER_Y + QUESTIONBOX_HEIGHT + 25):
                        continue

                # Then we check if we are too close to another answer
                isOkay = True
                for otherAnswer in self.currentQuestion.potentialAnswers:
                    distance = getDistance(x, y, otherAnswer.X, otherAnswer.Y)
                    if distance < ANSWER_CIRCLE_RADIUS * 2 + PLAYER_SIZE:
                        isOkay = False
                        break

                if not isOkay:
                    continue

                # We are good, let's set the answer xy to here
                answer.X = x
                answer.Y = y
                print(f"Answer {answer.text} at {answer.X}, {answer.Y}")
                break

    def generateMeteor(self, radius):
        """
        Given a list of meteors and the current question,
        find a good position that fits a meteor of the given size.
        Returns a meteor object

        Args:
            radius (int): wanted radius of the meteor
        """

        for i in range(100):
            x = pyxel.rndi(0, SCREEN_WIDTH)
            y = pyxel.rndi(0, SCREEN_HEIGHT)

            # First we check that the xy are not too close to the middle
            if (x > (SCREEN_WIDTH / 2) - CENTER_SAFE_ZONE_RADIUS) and (
                    x < (SCREEN_WIDTH / 2) + CENTER_SAFE_ZONE_RADIUS):
                if (y > (SCREEN_HEIGHT / 2) - CENTER_SAFE_ZONE_RADIUS) and (
                        y < (SCREEN_HEIGHT / 2) + CENTER_SAFE_ZONE_RADIUS):
                    continue

            # Then we check if it is too close to any other meteors
            isOkay = True
            for meteor in self.meteors:
                distance = getDistance(x, y, meteor.X, meteor.Y)
                if distance < meteor.radius + radius + PLAYER_SIZE + 10:
                    isOkay = False
                    break

            if not isOkay:
                continue

            # We check that it is not too close to any answers
            for answer in self.currentQuestion.potentialAnswers:
                distance = getDistance(x, y, answer.X, answer.Y)
                if distance < ANSWER_CIRCLE_RADIUS + radius + PLAYER_SIZE:
                    isOkay = False
                    break

            if not isOkay:
                continue

            # We need to check that the meteor is not on top of the question box
            if (x > SCREEN_WIDTH / 2 - (QUESTIONBOX_WIDTH / 2) and x < SCREEN_WIDTH / 2 + QUESTIONBOX_WIDTH):
                if (y > QUESTIONBOX_CENTER_Y - (
                        QUESTIONBOX_HEIGHT / 2) and y < QUESTIONBOX_CENTER_Y + QUESTIONBOX_HEIGHT):
                    continue

            # The position is good, we create the meteor
            self.meteors.append(Meteor(x, y, radius))
            return

    def resetRound(self):
        self.generateQuestion()

        self.meteors.clear()
        for i in range(250):
            self.generateMeteor(pyxel.rndi(3, 7))

        for player in self.players:
            player.resetPosition()

    def update(self):
        for player in self.players:
            player.update()
            # Check meteors
            for meteor in self.meteors:
                if meteor.collidesWithPlayer(player):
                    player.resetPosition()

            # Check answers
            selectedAnswer = self.currentQuestion.getPlayerSelectedAnswer(player)
            if selectedAnswer is not None:
                if selectedAnswer.isRight:
                    player.score += 1
                    self.resetRound()
                    return
                else:
                    self.currentQuestion.removePotentialAnswer(selectedAnswer)

    def draw(self):
        pyxel.cls(0)

        # We draw the scores
        scoreX = SCREEN_WIDTH - 100
        scoreY = 50
        for player in self.players:
            pyxel.text(scoreX, scoreY, f"Player {player.id}: {player.score}", 7)
            scoreY = + 30

        # We draw the question, which also in turn draws the potential answers
        self.currentQuestion.draw()
        # Draw meteors
        for meteor in self.meteors:
            meteor.draw()
        # Draw players
        for player in self.players:
            player.draw()


App()