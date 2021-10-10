import time
import math
import random

import glfw
import cv2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

import win32api
import win32con


ft = 1/10
d = 512


def 生成opengl纹理(文件名):
    npdata = cv2.imread(文件名, -1)
    w, h, 通道数 = npdata.shape
    assert 通道数==4
    纹理 = np.zeros([d, d, 通道数], dtype=npdata.dtype)
    纹理[:w, :h] = npdata
    纹理座标 = (w / d, h / d)
 
    width, height = 纹理.shape[:2]
    纹理编号 = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, 纹理编号)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_BGRA, GL_UNSIGNED_BYTE, 纹理)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return 纹理编号, 纹理座标


def opengl绘图循环():
    纹理编号, 纹理座标 = 生成opengl纹理('self.png')

    glClearColor(0, 0, 0, 0)

    def 画图(强度):
        glClear(GL_COLOR_BUFFER_BIT)
        glBindTexture(GL_TEXTURE_2D, 纹理编号)
        glColor4f(1, 1, 1, 强度)
        a = b = -1
        c = d = 1
        q, w = 纹理座标
        [[p1, p2],
         [p4, p3]] = np.array([
             [[a, b, 0, 1, 0, q], [a, d, 0, 1, 0, 0]],
             [[c, b, 0, 1, w, q], [c, d, 0, 1, w, 0]],
         ])
        glBegin(GL_QUADS)
        for p in [p1, p2, p3, p4]:
            glTexCoord2f(*p[4:])
            glVertex4f(*(p[:4]))
        glEnd()
        glfw.swap_buffers(window)

    t = None
    tj = []
    while True:
        if t is None:
            画图(0.001)
            t = time.time()
        else:
            dt = time.time() - t
            if dt>ft:
                画图(0)
                break
            强度 = (1 - abs((dt - ft/2)/(ft/2)))
            tj.append('%.4f - %.4f' % (dt, 强度))
            画图(强度*0.05)


glfw.init()
window = None

def e():
    global window
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
    glfw.window_hint(glfw.DECORATED, False)
    glfw.window_hint(glfw.RESIZABLE, False)
    glfw.window_hint(glfw.FLOATING, True)
    glfw.window_hint(glfw.VISIBLE, False)
    glfw.window_hint(glfw.FOCUS_ON_SHOW, False)
    window = glfw.create_window(d, d, 'self', None, None)

    hwn = glfw.get_win32_window(window)
    style = win32api.GetWindowLong(hwn, win32con.GWL_EXSTYLE)
    win32api.SetWindowLong(hwn, win32con.GWL_EXSTYLE, (style & ~win32con.WS_EX_APPWINDOW) | win32con.WS_EX_TOOLWINDOW)

    glfw.show_window(window)

    monitor_size = glfw.get_video_mode(glfw.get_primary_monitor()).size
    glfw.set_window_pos(window, monitor_size.width - d, monitor_size.height - d)
    glfw.make_context_current(window)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
    opengl绘图循环()
    glfw.destroy_window(window)

while True:
    time.sleep(random.randint(60, 360))
    e()
