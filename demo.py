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

import OpenGL as _gl
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut


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

    glut.glutSwapBuffers()

    angle += speed


def input_handler(key, x, y):
    global speed, colors
    # print this out (for debug reasons)
    print("Key pressed: %r (x: %r, y: %r)" % (key, x, y))

    if key == b'\x1b':  # (ESCAPE) close the demo
        sys.exit(0)

    if key == b'+':  # increase rotation speed
        speed += 0.1
    elif key == b'-':  # decrease rotation speed (going into negative values will reverse the rotation direction)
        speed -= 0.1
    elif key == b'*':  # rotate the colors array
        colors = [*colors[1:], colors[0]]


def main(argv):
    glut.glutInit(argv)
    glut.glutInitWindowPosition(100, 100)
    glut.glutInitWindowSize(1000, 750)
    glut.glutInitDisplayMode(glut.GLUT_RGBA | glut.GLUT_DOUBLE | glut.GLUT_DEPTH)
    window = glut.glutCreateWindow("Python OpenGL Demo")

    glut.glutDisplayFunc(render)
    glut.glutReshapeFunc(change_size)
    glut.glutIdleFunc(render)
    glut.glutKeyboardFunc(input_handler)
    glut.glutMainLoop()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
