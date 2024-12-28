import glfw
import ctypes
from OpenGL.GL import *


def setup():
    glfw.init()
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.DEPTH_BITS, 24)
    glfw.window_hint(glfw.STENCIL_BITS, 2)
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.set_error_callback(lambda e, d: print(f"Error: {e}, Description: {d}"))
    window = glfw.create_window(640, 480, "OpenGL Tutorials", None, None)
    glfw.make_context_current(window)
    return window


def loadShader(filename):
    with open(filename, "r") as file:
        return file.read()


def setup_shader(filename, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, loadShader(filename), None)
    glCompileShader(shader)
    status = ctypes.c_int(-1)
    glGetShaderiv(shader, GL_COMPILE_STATUS, status)

    if not status:
        raise Exception(f"{shader_type} compilation failed")

    return shader
