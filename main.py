import pygame
import random
from datetime import datetime


# Generates a curve from any number of given points
# A recursive function
def generate_curve(points, t):
    new_points = []
    for i in range(len(points)-1):
        tup = [0, 0]
        tup[0] = points[i][0]-((points[i][0]-points[i+1][0])*t)
        tup[1] = points[i][1]-((points[i][1]-points[i+1][1])*t)
        tup = tuple(tup)
        new_points.append(tup)
    if len(new_points) > 1:
        return generate_curve(new_points, t)
    else:
        new_points = (int(new_points[0][0]), int(new_points[0][1]))
        return new_points


# A function that makes a new random curve given the number of points and window height and width
def new_curve(num_of_points, window_height, window_width):
    points = []
    for i in range(num_of_points):
        points.append((random.randint(0, window_width), random.randint(0, window_height)))

    return points


# The main code
def main():
    # Initialising the pygame window
    window_height = 500
    window_width = 500
    pygame.init()
    pygame.display.set_caption("Bezier Curves")
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

    # Generates a list of random list of points at the specified length
    num_of_points = 4
    points = [new_curve(num_of_points, window_height, window_width)]

    # Variables for the loop, like resolution of the curve and the size of the selection of the points circles
    resolution = 50
    mouse_down = False
    radius = 10
    not_visible = False
    moving = [0, 0, False]
    changed = True
    prev_moved = None

    # Variables to measure the frame rate
    frames = 0
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # A variable that allows you to make the curve always a closed loop
    loop = False
    if loop:
        add = points[0]
        points.append(add)

    # The main game loop
    while True:

        # Gets the time at every frame
        now = datetime.now()
        if not current_time == now.strftime("%H:%M:%S"):
            print(f'There are {frames} fps')
            frames = 0
            current_time = now.strftime("%H:%M:%S")

        # Makes the curve a closed loop depending on the loop variable
        if loop:
            points[len(points)-1] = points[0]

        # Gets the mouse position every frame
        mouse_pos = pygame.mouse.get_pos()

        # Every frame this allows the code to get inputs from the user, like key presses and mouse clicks
        for event in pygame.event.get():

            # Checks whether the window has been resized
            if event.type == pygame.VIDEORESIZE:
                # Updates the width and height values when the window is resized
                changed = True
                # window_width = event.w
                # window_height = event.h

            # Quits the code if the cross on the game window if pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Gets whether the mouse is pressed and changes a variable to store it
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                moving[2] = False

            # Gets the keyboard presses
            if event.type == pygame.KEYDOWN:
                changed = True

                # If the p key is pressed then it sets a variable to hide everything but the curve
                if event.key == pygame.K_p:
                    if not not_visible:
                        not_visible = True
                    else:
                        not_visible = False
                if event.key == pygame.K_n:
                    points.append(new_curve(num_of_points, window_height, window_width))
                if event.key == pygame.K_BACKSPACE:
                    if prev_moved is not None:
                        points.remove(points[prev_moved])
                        prev_moved -= 1

        if changed:

            # Fills the screen with black to cover up the versions of the curve
            screen.fill((27, 18, 18))

            for j in range(len(points)):
                # Generates the curve every frame at the given resolution
                curve_points = []
                for i in range(resolution+1):
                    new_point = generate_curve(points[j], (1/resolution)*i)
                    curve_points.append(new_point)

                # Draws the curve
                for i in range(len(curve_points)-1):
                    pygame.draw.line(screen, (200, 50, 50), curve_points[i], curve_points[i + 1])
                changed = False

            # Checks whether anything other than the curve should be visible
            if not not_visible:
                for j in range(len(points)):
                    # Draws lines between the points that define the curves
                    if num_of_points != 4:
                        for i in range(len(points[j]) - 1):
                            pygame.draw.line(screen, (202, 207, 210), points[j][i], points[j][i + 1])
                    else:
                        pygame.draw.line(screen, (202, 207, 210), points[j][0], points[j][1])
                        pygame.draw.line(screen, (202, 207, 210), points[j][2], points[j][3])

                    # Draws the circles at the points that define the curve
                    for i in range(len(points[j])):
                        pygame.draw.ellipse(screen, (200, 200, 200), (points[j][i][0] - (radius / 2),
                                                                      points[j][i][1] - (radius / 2), radius, 10))

        # Checks whether anything other than the curve should be visible
        if not not_visible:

            # Updates the points that are selected and only one at a time
            for j in range(len(points)):
                one_done = False
                for i in range(len(points[j])):
                    if mouse_down and points[j][i][0]-radius < mouse_pos[0] < points[j][i][0]+radius and \
                       points[j][i][1]-radius < mouse_pos[1] < points[j][i][1]+radius and not one_done:
                        prev_moved = j
                        moving[0] = j
                        moving[1] = i
                        moving[2] = True
                        one_done = True
                        changed = True
                    if moving[2] and i == moving[1] and j == moving[0]:
                        points[j][i] = mouse_pos

        # Updates the display window
        pygame.display.update()

        # Adds a frame to the frame counter
        frames += 1


if __name__ == '__main__':
    main()
