from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

width, height = 400, 400

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # glutWireTeapot(0.5) suggested but unsure if necessary
    glutSwapBuffers()





glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(width, height)
glutInitWindowPosition(100, 100)
window = glutCreateWindow("OpenGL Window")
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutMainLoop()


