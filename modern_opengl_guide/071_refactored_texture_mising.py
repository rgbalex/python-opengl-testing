import glfw
import numpy as np
from PIL import Image
from OpenGL.GL import *

from helper_functions import *

vertexSource = loadShader("./modern_opengl_guide/resources/vertex.glsl")

fragmentSource = loadShader("./modern_opengl_guide/resources/fragment.glsl")


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
        # Position       Color     Texcoords
        -0.5,  0.5, 1.0, 0.0, 0.0, 0.0, 0.0, # Top-left
         0.5,  0.5, 0.0, 1.0, 0.0, 1.0, 0.0, # Top-right
         0.5, -0.5, 0.0, 0.0, 1.0, 1.0, 1.0, # Bottom-right
        -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0  # Bottom-left
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

    vertexShader = setup_shader(
        "modern_opengl_guide/resources/vertex.glsl", GL_VERTEX_SHADER
    )
    fragmentShader = setup_shader(
        "modern_opengl_guide/resources/fragment.glsl", GL_FRAGMENT_SHADER
    )

    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertexShader)
    glAttachShader(shaderProgram, fragmentShader)

    glBindFragDataLocation(shaderProgram, 0, "outColor")
    glLinkProgram(shaderProgram)
    glUseProgram(shaderProgram)

    posAttrib = glGetAttribLocation(shaderProgram, "position")
    glEnableVertexAttribArray(posAttrib)
    glVertexAttribPointer(
        posAttrib, 2, GL_FLOAT, GL_FALSE, 7 * sizeof(ctypes.c_float), None
    )

    colorAttrib = glGetAttribLocation(shaderProgram, "color")
    glEnableVertexAttribArray(colorAttrib)
    glVertexAttribPointer(
        index=colorAttrib,
        size=3,
        type=GL_FLOAT,
        normalized=GL_FALSE,
        stride=7 * sizeof(ctypes.c_float),
        pointer=(ctypes.c_void_p(2 * sizeof(ctypes.c_float))),
    )

    texAttrib = glGetAttribLocation(shaderProgram, "texcoord")
    glEnableVertexAttribArray(texAttrib)
    glVertexAttribPointer(
        index=texAttrib,
        size=2,
        type=GL_FLOAT,
        normalized=GL_FALSE,
        stride=7 * sizeof(ctypes.c_float),
        pointer=(ctypes.c_void_p(5 * sizeof(ctypes.c_float))),
    )

    textures = (GLuint * 2)()
    glGenTextures(2, textures)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, textures[0])

    # Load texture
    image = (
        Image.open("./modern_opengl_guide/resources/red_brick_diff_1k.jpg")
        .convert("RGB")
        .transpose(Image.FLIP_TOP_BOTTOM)
    )
    img_data = np.array(image.getdata(), np.uint8).flatten().tobytes()

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGB,
        image.width,
        image.height,
        0,
        GL_RGB,
        GL_UNSIGNED_BYTE,
        img_data,
    )

    glUniform1i(glGetUniformLocation(shaderProgram, "tex1"), 0)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, textures[1])

    # Load texture
    image2 = (
        Image.open("./modern_opengl_guide/resources/red_brick_diff_1k_rotated.jpg")
        .convert("RGB")
        .transpose(Image.FLIP_TOP_BOTTOM)
    )
    img_data2 = np.array(image2.getdata(), np.uint8).flatten().tobytes()

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGB,
        image.width,
        image.height,
        0,
        GL_RGB,
        GL_UNSIGNED_BYTE,
        img_data2,
    )

    glUniform1i(glGetUniformLocation(shaderProgram, "tex2"), 1)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

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

    main(setup())
