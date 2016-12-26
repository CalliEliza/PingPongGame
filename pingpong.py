# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 13
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
constant = 35
stop = False

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT /2 ]
    vel_hor = random.randrange(2, 4)
    vel_ver = random.randrange(1, 3)
    if direction:
        ball_vel = [vel_hor, vel_ver]
    else:
        ball_vel = [- vel_hor, vel_ver]
        
        

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2, stop
    spawn_ball(RIGHT)
    score1 = 0
    score2 = 0
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle2_pos = [WIDTH - 1 - HALF_PAD_WIDTH, HEIGHT / 2]
    paddle1_vel = 0
    paddle2_vel = 0
    stop = False
    
def reset():
    new_game()
    
def stop():
    global ball_pos, ball_vel  # these are numbers
    global score1, score2, stop
    ball_vel = [0,0]
    ball_pos=[WIDTH/2,HEIGHT/2]  
    stop = True
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, constant
    
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] -= ball_vel[1]
    if ball_pos[1] <= 20 or ball_pos[1] >= 379:
        ball_vel[1] = - ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "white", "pink")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] <= 40 and paddle1_vel <=0:
        paddle1_pos[1] = paddle1_pos[1]
    elif paddle1_pos[1] >= 359 and paddle1_vel >=0:
        paddle1_pos[1] = paddle1_pos[1]
    else:
        paddle1_pos[1] += paddle1_vel
    
    if paddle2_pos[1] <= 40 and paddle2_vel <= 0:
        paddle2_pos[1] = paddle2_pos[1]
    elif paddle2_pos[1] >= 359 and paddle2_vel >=0:
        paddle2_pos[1] = paddle2_pos[1]
    else:
        paddle2_pos[1] += paddle2_vel
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos[1] + constant),(0, paddle1_pos[1] - constant),(10, paddle1_pos[1] - constant),(10, paddle1_pos[1] + constant)], 2, "white", "purple")
    canvas.draw_polygon([(590, paddle2_pos[1] + constant),(590, paddle2_pos[1] - constant),(599, paddle2_pos[1] - constant),(599, paddle2_pos[1] + constant)], 2, "white", "green")
    # determine whether paddle and ball collide    
    if ball_pos[0] < 28 and abs(ball_pos[1] - paddle1_pos[1]) > constant:
        score2 += 1
        spawn_ball(LEFT)
    elif ball_pos[0] < 28 and abs(ball_pos[1] - paddle1_pos[1]) <= constant:
        ball_vel[0] = - ball_vel[0] * 1.1
    if ball_pos[0] > 571 and abs(ball_pos[1] - paddle2_pos[1]) > constant:
        score1 += 1
        spawn_ball(RIGHT)
    if ball_pos[0] > 571 and abs(ball_pos[1] - paddle2_pos[1]) <= constant:
        ball_vel[0] = - ball_vel[0] * 1.1
    player1_score = "score: " + str(score1)
    player2_score = "score: " + str(score2)
    canvas.draw_text(player1_score, [150, 20], 24, "magenta")
    canvas.draw_text(player2_score, [330, 20], 24, "lime")
    if stop == True:
        if player1_score > player2_score:
            winner = "Player One wins!"
            canvas.draw_text(winner, [150,50],24, "Aqua")
        elif player2_score > player1_score:
            winner = "Plaer Two wins!"
            canvas.draw_text(winner, [330,50],24, "Aqua")
        
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = - 3
        
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel =  3
    
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = - 3
        
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 3
           
def keyup(key):
    global paddle1_vel, paddle2_vel
    if (key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]):
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
        


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", reset, 100)
frame.add_button("Stop", stop, 100)


# start frame
new_game()
frame.start()
