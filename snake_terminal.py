import random
import time
import os
import sys
from getkey import getkey

# 游戏区域大小
WIDTH = 20
HEIGHT = 10

# 初始化蛇和食物
snake = [(WIDTH // 2, HEIGHT // 2)]
food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
direction = (1, 0)  # 初始向右移动
score = 0

# 安装getkey如果不存在
try:
    from getkey import getkey
except ImportError:
    print("正在安装getkey库...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "getkey"])
    from getkey import getkey

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_game():
    clear_screen()
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

def move_snake():
    global snake, food, score
    
    # 计算新头部位置
    head_x = (snake[0][0] + direction[0]) % WIDTH
    head_y = (snake[0][1] + direction[1]) % HEIGHT
    new_head = (head_x, head_y)
    
    # 检查是否撞到自己
    if new_head in snake:
        print("游戏结束! 你撞到了自己!")
        print(f"最终分数: {score}")
        sys.exit()
    
    # 移动蛇
    snake.insert(0, new_head)
    
    # 检查是否吃到食物
    if new_head == food:
        score += 10
        # 生成新食物
        while True:
            food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
            if food not in snake:
                break
    else:
        # 没吃到食物则移除尾部
        snake.pop()

# 主游戏循环
while True:
    draw_game()
    
    # 非阻塞获取按键
    try:
        key = getkey()
        if key == 'q':
            print("游戏退出")
            sys.exit()
        update_direction(key)
    except:
        pass
    
    move_snake()
    time.sleep(0.2)