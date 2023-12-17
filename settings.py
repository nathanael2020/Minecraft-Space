from numba import njit
import numpy as np
import glm
import math
import pygame as pg

# OpenGL settings
MAJOR_VER, MINOR_VER = 3, 3
DEPTH_SIZE = 24
NUM_SAMPLES = 1  # antialiasing

# resolution
WIN_RES = glm.vec2(1000, 800)

KEYS = {
    'PITCH_UP': pg.K_s,
    'PITCH_DOWN': pg.K_w,
    'YAW_LEFT': pg.K_a,
    'YAW_RIGHT': pg.K_d,
    'ROLL_LEFT': pg.K_q,
    'ROLL_RIGHT': pg.K_e,
    'FORWARD': pg.K_UP,
    'BACK': pg.K_DOWN,
    'UP': pg.K_PERIOD,
    'DOWN': pg.K_COMMA,
    'STRAFE_L': pg.K_LEFT,
    'STRAFE_R': pg.K_RIGHT,
    'INTERACT': pg.K_f,
    'SWITCH_MODE': pg.K_n,
    'SET_VOXEL': pg.K_m,
    'WEAPON_3': pg.K_3,
}

# world generation
SEED = 16

# ray casting
MAX_RAY_DIST = 6

# chunk
CHUNK_SIZE = 12
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)

# world
WORLD_W, WORLD_H = 12, 9
WORLD_D = WORLD_W
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# world center
CENTER_XZ = WORLD_W * H_CHUNK_SIZE
CENTER_Y = WORLD_H * H_CHUNK_SIZE

# camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)  # vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # horizontal FOV
NEAR = 0.1
FAR = 65.0
PITCH_MAX = glm.radians(89)

# player
PLAYER_SIZE = 0.25
PLAYER_SPEED = 0.012
PLAYER_ROT_SPEED = 0.008
# PLAYER_POS = glm.vec3(CENTER_XZ, WORLD_H * CHUNK_SIZE, CENTER_XZ)
PLAYER_POS = glm.vec3(75, 35, 160)
MOUSE_SENSITIVITY = 0.002

# colors
BG_COLOR = glm.vec3(0.58, 0.83, 0.99)

# textures
SAND = 1
GRASS = 2
DIRT = 3
STONE = 4
SNOW = 5
LEAVES = 6
WOOD = 7

# terrain levels
SNOW_LVL = 54
STONE_LVL = 49
DIRT_LVL = 40
GRASS_LVL = 8
SAND_LVL = 7

# tree settings
TREE_PROBABILITY = 0.01
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

# water
WATER_LINE = 5.6
WATER_AREA = 5 * CHUNK_SIZE * WORLD_W

# cloud
CLOUD_SCALE = 25
CLOUD_HEIGHT = WORLD_H * CHUNK_SIZE * 2
