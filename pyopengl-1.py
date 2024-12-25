from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(1.0, 0.0)
    glVertex2f(0.0, 1.0)
    glEnd()
    glFlush()

if __name__ == '__main__':
    glutInit(sys.argv)
 
    glutInitContextVersion( 3, 3 );
    glutInitContextProfile( GLUT_CORE_PROFILE );
 
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(250, 250)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OpenGL Window")

    glBindTexture(GL_TEXTURE_2D, 0)

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    

    gluOrtho2D(0.0, 1.0, 0.0, 1.0)
    glutDisplayFunc(display)
    # glutIdleFunc(display)
    glutMainLoop()
