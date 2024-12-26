import glfw
from OpenGL.GL import *


def key_event(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def main(window):
    glfw.set_key_callback(window, key_event)

    # vertices = [0.0, 0.5, 0.5, 0.0, 0.3, -0.5, -0.3, -0.5, -0.5, 0.0]
    vertices = [
        0.0, 0.5,
        0.5, -0.5,
        -0.5, -0.5,
    ]

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

    vertexSource = r"""#version 150 core
    in vec2 position;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
    }
    """

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

    fragmentSource = r"""#version 150 core
    out vec4 color;
    void main()
    {
        color = vec4(1.0, 1.0, 1.0, 1.0);
    }
    """

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
    # Since a fragment shader is allowed to write to multiple buffers, you need to
    # explicitly specify which output is written to which buffer. This needs to happen
    # before linking the program. However, since this is 0 by default and there’s only
    # one output right now, the following line of code is not necessary
    # 
    # glBindFragDataLocation(shaderProgram, 0, "outColor")

    glLinkProgram(shaderProgram)
    glUseProgram(shaderProgram)

    vao = GLuint(0)
    glGenVertexArrays(1, vao)
    glBindVertexArray(vao)

    posAttrib = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(posAttrib, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(posAttrib)

    print(f"There are {glGetError()} errors before running mainloop")

    while not glfw.window_should_close(window):
        glDrawArrays(GL_TRIANGLES, 0, 3)
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
