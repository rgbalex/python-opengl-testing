import glfw
import numpy as np
from OpenGL.GL import *

vertexSource = r"""#version 150 core
in vec2 position;
in vec3 color;
out vec3 Color;
void main()
{
    Color = color;
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragmentSource = r"""#version 150 core
in vec3 Color;
out vec4 outColor;
void main()
{
    outColor = vec4(Color, 1.0);
}
"""


def key_event(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def main(window):
    glfw.set_key_callback(window, key_event)

    vao = GLuint(-1)
    glGenVertexArrays(1, vao)
    glBindVertexArray(vao)

    vbo = GLuint(-1)
    glGenBuffers(1, vbo)

    # fmt: off
    vertices = np.array([
    -0.5,  0.5, 1.0, 0.0, 0.0, # Top-left
     0.5,  0.5, 0.0, 1.0, 0.0, # Top-right
     0.5, -0.5, 0.0, 0.0, 1.0, # Bottom-right
    -0.5, -0.5, 1.0, 1.0, 1.0, # Bottom-left
    ], dtype=np.float32)
    # fmt: on

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(
        GL_ARRAY_BUFFER,
        len(vertices) * 4,
        (GLfloat * len(vertices))(*vertices),
        GL_STATIC_DRAW,
    )

    ebo = GLuint(-1)
    glGenBuffers(1, ebo)

    elements = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(
        GL_ELEMENT_ARRAY_BUFFER,
        len(elements) * 4,
        (GLuint * len(elements))(*elements),
        GL_STATIC_DRAW,
    )

    vertexShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertexShader, vertexSource, None)
    glCompileShader(vertexShader)

    status = ctypes.c_int(-1)
    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, status)

    print(f"Vertex shader compile status is {status}")

    if not status:
        print(f"Status is equal to {status == GL_TRUE}")
        print("Shader compilation failed")
        print("Note: Cannot get the shader log to print")
        return 0

    fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragmentShader, fragmentSource, None)
    glCompileShader(fragmentShader)

    status = ctypes.c_int(-1)
    glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, status)

    print(f"Fragment shader compile status is {status}")

    if not status:
        print(f"Status is equal to {status == GL_TRUE}")
        print("Shader compilation failed")
        print("Note: Cannot get the shader log to print")
        return 0

    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertexShader)
    glAttachShader(shaderProgram, fragmentShader)

    glBindFragDataLocation(shaderProgram, 0, "outColor")
    glLinkProgram(shaderProgram)
    glUseProgram(shaderProgram)

    posAttrib = glGetAttribLocation(shaderProgram, "position")
    glEnableVertexAttribArray(posAttrib)
    glVertexAttribPointer(
        posAttrib, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(ctypes.c_float), None
    )

    colorAttrib = glGetAttribLocation(shaderProgram, "color")
    glEnableVertexAttribArray(colorAttrib)
    glVertexAttribPointer(
        index=colorAttrib,
        size=3,
        type=GL_FLOAT,
        normalized=GL_FALSE,
        stride=5 * sizeof(ctypes.c_float),
        pointer=(ctypes.c_void_p(2 * sizeof(ctypes.c_float))),
    )

    print(f"There are {glGetError()} errors before running mainloop")

    while not glfw.window_should_close(window):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glfw.swap_buffers(window)

        glfw.poll_events()

    glDeleteProgram(shaderProgram)
    glDeleteShader(fragmentShader)
    glDeleteShader(vertexShader)

    glDeleteBuffers(1, ebo)
    glDeleteBuffers(1, vbo)

    glDeleteVertexArrays(1, vao)

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

    window = glfw.create_window(640, 480, "OpenGL Tutorials", None, None)

    glfw.make_context_current(window)

    main(window)
