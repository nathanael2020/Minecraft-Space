from settings import *
from frustum import Frustum

class Camera:
    def __init__(self, position, yaw, pitch, roll=0):
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)
        self.roll = glm.radians(roll)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

        self.frustum = Frustum(self)

    def update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)
    def update_vectors(self):

        damping_factor = 0.970

        #        forward = glm.vec3(0, 0, -1)
        #        up = glm.vec3(0, 1, 0)
        #        right = glm.vec3(1, 0, 0)

        self.yaw *= damping_factor
        self.pitch *= damping_factor
        self.roll *= damping_factor

        forward = self.forward
        up = self.up
        right = self.right

        yaw_matrix = glm.rotate(glm.mat4(1.0), glm.radians(self.yaw), up)
        yawed_forward = glm.vec3(yaw_matrix * glm.vec4(forward, 0.0))
        yawed_right = glm.normalize(glm.cross(up, yawed_forward))

        roll_matrix = glm.rotate(glm.mat4(1.0), glm.radians(self.roll), yawed_forward)
        rolled_right = glm.vec3(roll_matrix * glm.vec4(yawed_right, 0.0))
        rolled_up = glm.vec3(roll_matrix * glm.vec4(up, 0.0))

        pitch_matrix = glm.rotate(glm.mat4(1.0), glm.radians(self.pitch), rolled_right)
        pitched_forward = glm.vec3(pitch_matrix * glm.vec4(yawed_forward, 0.0))
        pitched_up = glm.vec3(pitch_matrix * glm.vec4(rolled_up, 0.0))

        #        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        #        self.forward.y = glm.sin(self.pitch)
        #        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(pitched_forward)
        self.right = glm.normalize(rolled_right)
        self.up = glm.normalize(pitched_up)

    def rotate_pitch(self, delta_y):
        self.pitch += .67 * delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def rotate_roll(self, delta_z):
        self.roll += 0.75 * delta_z

    def move_left(self, velocity):
#        self.position -= self.right * velocity
        return self.right.xyz * velocity

    def move_right(self, velocity):
#        self.position += self.right * velocity
        return -self.right.xyz * velocity

    def move_up(self, velocity):
#        self.position += self.up * velocity
        return self.up.xyz

    def move_down(self, velocity):
#        self.position -= self.up * velocity
        return -self.up.xyz * velocity

    def move_forward(self, velocity):
#        self.position += self.forward * velocity
        return self.forward.xyz * velocity

    def move_back(self, velocity):
#        self.position -= self.forward * velocity
        return -self.forward.xyz * velocity
