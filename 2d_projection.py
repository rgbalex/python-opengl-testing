import glfw
from OpenGL.GL import *
from glfw import swap_buffers, poll_events


def key_event(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def change_size_event(window, width, height):
    pass


def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(10)
    glColor3f(1, 0, 0)
    glBegin(GL_POINTS)
    glVertex2f(0, 0)
    glVertex2f(0.25, 0.25)
    glVertex2f(0.5, 0.5)
    glEnd()


def main():
    while not glfw.window_should_close(window):
        render()
        swap_buffers(window)
        poll_events()
    return 0


if __name__ == "__main__":
    glfw.init()
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)

    window = glfw.create_window(640, 480, "OpenGL Tutorials", None, None)

    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_event)
    glfw.set_window_size_callback(window, change_size_event)

    change_size_event(window, 640, 480)

    main()
