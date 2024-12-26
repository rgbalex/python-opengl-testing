"""
Install PyOpenGL:
$ pip install PyOpenGL

Run this file:
$ python main.py

Controls:
- ESC - closes the demo
- '+' key - increases rotation speed
- '-' key - decreases rotation speed (if speed is negative, rotation direction changes)
- '*' key - switch up the colors
"""
import sys

import OpenGL.GL as gl
import OpenGL.GLU as glu
import glfw


angle = 0.0
speed = 0.1
colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0)]



def change_size(width, height):
    if height == 0:
        height = 1
    ratio = float(width)/float(height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glViewport(0, 0, width, height)
    glu.gluPerspective(45, ratio, 1, 1000)
    gl.glMatrixMode(gl.GL_MODELVIEW)


def render():
    global angle
    # gl.glClearColor(0.3, 1.0, 0.11, 0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    gl.glLoadIdentity()

    glu.gluLookAt(
        0.0, 0.0, 10.0,
        0.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
    )

    gl.glRotatef(angle, 0.0, 1.0, 0.0)

    gl.glBegin(gl.GL_TRIANGLES)

    gl.glColor3f(*colors[0])
    gl.glVertex3f(-2.0, -2.0, 0.0)

    gl.glColor3f(*colors[1])
    gl.glVertex3f(2.0, -2.0, 0.0)

    gl.glColor3f(*colors[2])
    gl.glVertex3f(0.0, 2.0, 0.0)

    gl.glEnd()

    angle += speed


def input_handler(window, key, scancode, action, mods):
    global speed, colors
    # print this out (for debug reasons)
    print("Key pressed: %r" % (key))

    if key == 256 and action == glfw.PRESS:  # (ESCAPE) close the demo
        glfw.set_window_should_close(window, True)
    if key == 61 and action == glfw.PRESS:  # increase rotation speed
        speed += 0.1
    elif key == 45 and action == glfw.PRESS:  # decrease rotation speed (going into negative values will reverse the rotation direction)
        speed -= 0.1
    elif key == 56 and action == glfw.PRESS:  # rotate the colors array
        colors = [*colors[1:], colors[0]]


def main():
    glfw.init()    
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)

    window = glfw.create_window(640, 480, "Hello World", None, None)
    
    glfw.make_context_current(window)
    
    glfw.set_key_callback(window, input_handler)
    glfw.set_window_size_callback(window, change_size)
    
    # necessary to calculate camera viewport
    change_size(640, 480)


    while not glfw.window_should_close(window):
        render()
        glfw.swap_buffers(window)
        glfw.poll_events()
    return 0


if __name__ == "__main__":
    sys.exit(main())
