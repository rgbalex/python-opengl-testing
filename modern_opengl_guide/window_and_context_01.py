import glfw
from OpenGL.GL import *


def key_event(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def main(window):
    glfw.set_key_callback(window, key_event)

    vertices = [0.0, 0.5, 0.5, 0.0, 0.3, -0.5, -0.3, -0.5, -0.5, 0.0]

    number_of_buffers = 1
    gl_list = (GLint * number_of_buffers)()
    glGenBuffers(number_of_buffers, gl_list)
    glBindBuffer(GL_ARRAY_BUFFER, gl_list[0])
    glBufferData(
        GL_ARRAY_BUFFER,
        len(vertices) * 4,
        (GLfloat * len(vertices))(*vertices),
        GL_STATIC_DRAW,
    )

    # make vertexSource the value of the file simple_shader.
    vertexSource = r"""#version 330 core
in vec2 position;

void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}"""

    vertexShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertexShader, vertexSource, None)

    glCompileShader(vertexShader)

    status = ctypes.c_int(-1)
    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, status)

    print(f"Shader compile status is {status}")

    if not status:
        print(f"Status is equal to {status == GL_TRUE}")
        print("Shader compilation failed")
        return 0

    while not glfw.window_should_close(window):
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    return 0


if __name__ == "__main__":
    glfw.init()
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.DEPTH_BITS, 24)
    glfw.window_hint(glfw.STENCIL_BITS, 2)
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.set_error_callback(
        lambda error, description: print(f"Error: {error}, Description: {description}")
    )

    window = glfw.create_window(640, 480, "Rope Simulation", None, None)

    glfw.make_context_current(window)

    main(window)
