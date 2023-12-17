import pygame as pg
from camera import Camera
from settings import *


class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=0, pitch=0, roll=0):
        self.app = app
        super().__init__(position, yaw, pitch, roll)

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def handle_event(self, event):
        # adding and removing voxels with clicks
        key_state = pg.key.get_pressed()
        voxel_handler = self.app.scene.world.voxel_handler
        if key_state[KEYS['SET_VOXEL']]:
            voxel_handler.set_voxel()
        if key_state[KEYS['SWITCH_MODE']]:
            voxel_handler.switch_mode()


        # if event.type == pg.MOUSEBUTTONDOWN:
        #     voxel_handler = self.app.scene.world.voxel_handler
        #     if event.button == 3:
        #         voxel_handler.set_voxel()
        #     if event.button == 1:
        #         voxel_handler.switch_mode()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=-mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time
        rot_vel = PLAYER_ROT_SPEED * self.app.delta_time
        next_step = glm.vec3()
        if key_state[KEYS['PITCH_UP']]:
            self.rotate_pitch(-rot_vel)
        if key_state[KEYS['PITCH_DOWN']]:
            self.rotate_pitch(rot_vel)
        if key_state[KEYS['YAW_LEFT']]:
            self.rotate_yaw(rot_vel)
        if key_state[KEYS['YAW_RIGHT']]:
            self.rotate_yaw(-rot_vel)
        if key_state[KEYS['ROLL_LEFT']]:
            self.rotate_roll(-rot_vel)
        if key_state[KEYS['ROLL_RIGHT']]:
            self.rotate_roll(rot_vel)
        if key_state[KEYS['FORWARD']]:
            next_step.xyz += self.move_forward(vel)
        if key_state[KEYS['BACK']]:
            next_step.xyz += self.move_back(vel)
        if key_state[KEYS['STRAFE_R']]:
            next_step.xyz += self.move_right(vel)
        if key_state[KEYS['STRAFE_L']]:
            next_step.xyz += self.move_left(vel)
        if key_state[KEYS['UP']]:
            next_step.xyz += self.move_up(vel)
        if key_state[KEYS['DOWN']]:
            next_step.xyz += self.move_down(vel)

        self.move(next_step=next_step)

    def move(self, next_step):
        if not self.app.scene.world.voxel_handler.check_player_collision(self.position, dx=next_step[0]):
            self.position.x += next_step[0]

        if not self.app.scene.world.voxel_handler.check_player_collision(self.position, dy=next_step[1]):
            self.position.y += next_step[1]

        if not self.app.scene.world.voxel_handler.check_player_collision(self.position, dz=next_step[2]):
            self.position.z += next_step[2]
