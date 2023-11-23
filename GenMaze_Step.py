import random
import matplotlib.pyplot as plt


class Maze:
    def __init__(self, Y, X, start, end):
        self.start = start
        self.end = end
        self.Height = Y
        self.Width = X
        self.maze = {}
        self.level = {}
        self.path = None
        self.OldNode = {}
        self.directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        for i in range(Y):
            for j in range(X):
                self.maze[(i, j)] = [True, True, True, True, False, False] #[Left, Top, Right, Bottom, Visited]
        while not(self.start in self.maze):
            print('Invalid Starting Point')
            self.start = eval(input('Enter new starting point(in form of (y,x)): '))

        while not(self.end in self.maze):
            print('Invalid Ending Point')
            self.end = eval(input('Enter new ending point(in form of (y,x)): '))

    def generateMaze(self):
        current = random.choice(list(self.maze))
        self.updateMaze(current)
        self.wallLines()

    def updateMaze(self, current):
        self.maze[current][4] = True
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        updateWall = {(0, 1): 2,
                      (0, -1): 0,
                      (1, 0): 3,
                      (-1, 0): 1}
        for i, j in directions:
            y = current[0] + i
            x = current[1] + j
            check = (y, x)
            if 0 <= y <= self.Height - 1 and self.Width - 1 >= x >= 0 and not self.maze[check][4]:
                self.maze[current][updateWall[(i, j)]] = False
                self.maze[check][updateWall[(-i, -j)]] = False
                self.maze[check][4] = True
                self.updateMaze(check)

    def startPath(self, z):
        current = self.start
        self.level = {0: [current]}
        self.OldNode = {current: current}
        self.makePath(0, z)

    def makePath(self, level, z):
        endNode = 0
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        row = []
        for i in self.level[level]:
            directionIndex = 0
            for u, w in directions:
                if not self.maze[i][directionIndex]:
                    y = i[0] + u
                    x = i[1] + w

                    if not (y, x) == self.OldNode[i]:
                        row.append((y, x))
                        self.OldNode[(y, x)] = i
                        if z == 1:
                            plt.plot([i[1] + 0.5, x + 0.5], [-i[0] - 0.5, -y - 0.5], color = 'blue')
                        if (y, x) == self.end:
                            endNode = (y, x)
                            break
                directionIndex += 1
            if not endNode == 0:
                break
            if z == 1:
                plt.draw()
                plt.pause(0.0001)

        self.level[level + 1] = row
        if endNode == 0:
            self.makePath(level+1, z)

        else:
            self.tracePath(endNode)

    def tracePath(self, endNode):
        x = endNode
        y = self.OldNode[x]
        self.path = [endNode]
        while not x == y:
            self.path.insert(0, y)
            x = y
            y = self.OldNode[x]

    def graphMaking(self):
        pathGraphX = []
        pathGraphY = []
        for i in self.path:
            pathGraphX.append(i[1] + 0.5)
            pathGraphY.append(-i[0] - 0.5)
            plt.plot(pathGraphX[-2:], pathGraphY[-2:], color='red')
            plt.draw()
            plt.pause(0.001)
        plt.show()


    def wallLines(self):
        plotWall = {0: [(0, 0), (-1, 0)],
                    1: [(0, 0), (0, 1)]}
        for i in self.maze:
            plt.plot([0, self.Width, self.Width, 0], [0, 0, -self.Height, -self.Height], color='black')
            direction = 0
            for j in self.maze[i][0:2]:
                if j:
                    x = [i[1] + plotWall[direction][0][1], i[1] + plotWall[direction][1][1]]
                    y = [-i[0] + plotWall[direction][0][0], -i[0] + plotWall[direction][1][0]]
                    plt.plot(x, y, color='black')
                direction += 1


z = 'y'
y = int(input('Enter Height Of The Maze: '))
x = int(input('Enter Width Of The Maze: '))
startpt = eval(input('Enter starting point(in form of (y,x)): '))
endpt = eval(input('Enter ending point(in form of (y,x)): '))
while z == 'y':
    maze = Maze(y, x, startpt, endpt)
    maze.generateMaze()
    if input('Do you want Visual Representation of Path Finding?: ') == 'y':
        maze.startPath(1)
    else:
        maze.startPath(0)
    maze.graphMaking()
    z = input("press 'y' for new seek or any other key to exit")
