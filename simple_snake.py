import random
import time
import os
import sys
import tty
import termios

# 游戏设置
WIDTH = 20
HEIGHT = 10
DELAY = 0.2

# 获取键盘输入 (不需要外部依赖)
def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# 游戏初始化
snake = [(WIDTH//2, HEIGHT//2)]
direction = (1, 0)
food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
score = 0

def draw():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"分数: {score}")
    print("+" + "-" * WIDTH + "+")
    for y in range(HEIGHT):
        print("|", end="")
        for x in range(WIDTH):
            if (x, y) in snake:
                print("O", end="")
            elif (x, y) == food:
                print("*", end="")
            else:
                print(" ", end="")
        print("|")
    print("+" + "-" * WIDTH + "+")
    print("控制: w=上, s=下, a=左, d=右, q=退出")

def update_direction(key):
    global direction
    if key == 'w' and direction != (0, 1):
        direction = (0, -1)
    elif key == 's' and direction != (0, -1):
        direction = (0, 1)
    elif key == 'a' and direction != (1, 0):
        direction = (-1, 0)
    elif key == 'd' and direction != (-1, 0):
        direction = (1, 0)

def move():
    global snake, food, score
    
    head = ((snake[0][0] + direction[0]) % WIDTH, 
            (snake[0][1] + direction[1]) % HEIGHT)
    
    if head in snake:
        print("游戏结束! 撞到自己!")
        print(f"最终分数: {score}")
        sys.exit()
        
    snake.insert(0, head)
    
    if head == food:
        score += 10
        while True:
            food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
            if food not in snake:
                break
    else:
        snake.pop()

# 主游戏循环
while True:
    draw()
    
    # 非阻塞键盘输入
    try:
        key = get_key()
        if key == 'q':
            print("游戏退出")
            sys.exit()
        update_direction(key)
    except:
        pass
    
    move()
    time.sleep(DELAY)