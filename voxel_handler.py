import random

from settings import *
from meshes.chunk_mesh_builder import get_chunk_index


class VoxelHandler:
    def __init__(self, world):
        self.app = world.app
        self.chunks = world.chunks

        # ray casting result
        self.chunk = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_pos = None
        self.voxel_world_pos = None
        self.voxel_normal = None

        self.interaction_mode = 0  # 0: remove voxel   1: add voxel
        self.new_voxel_id = DIRT

    def add_voxel(self):
        if self.voxel_id:
            # check voxel id along normal
            result = self.get_voxel_id(self.voxel_world_pos + self.voxel_normal)

            # is the new place empty?
            if not result[0]:
                _, voxel_index, _, chunk = result
                chunk.voxels[voxel_index] = self.new_voxel_id
                chunk.mesh.rebuild()

                # was it an empty chunk
                if chunk.is_empty:
                    chunk.is_empty = False

    def rebuild_adj_chunk(self, adj_voxel_pos):
        index = get_chunk_index(adj_voxel_pos)
        if index != -1:
            self.chunks[index].mesh.rebuild()

    def rebuild_adjacent_chunks(self):
        lx, ly, lz = self.voxel_local_pos
        wx, wy, wz = self.voxel_world_pos

        if lx == 0:
            self.rebuild_adj_chunk((wx - 1, wy, wz))
        elif lx == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx + 1, wy, wz))

        if ly == 0:
            self.rebuild_adj_chunk((wx, wy - 1, wz))
        elif ly == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx, wy + 1, wz))

        if lz == 0:
            self.rebuild_adj_chunk((wx, wy, wz - 1))
        elif lz == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx, wy, wz + 1))

    def remove_voxel(self):
        if self.voxel_id:
            self.chunk.voxels[self.voxel_index] = 0

            self.chunk.mesh.rebuild()
            self.rebuild_adjacent_chunks()

    def set_voxel(self):
        if self.interaction_mode:
            self.add_voxel()
        else:
            self.remove_voxel()

    def switch_mode(self):
        self.interaction_mode = not self.interaction_mode

    def update(self):
        self.ray_cast()

    def ray_cast(self):
        # start point
        x1, y1, z1 = self.app.player.position
        # end point
        x2, y2, z2 = self.app.player.position + self.app.player.forward * MAX_RAY_DIST

        current_voxel_pos = glm.ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0)
        step_dir = -1

        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):

            result = self.get_voxel_id(voxel_world_pos=current_voxel_pos)
            if result[0]:
                self.voxel_id, self.voxel_index, self.voxel_local_pos, self.chunk = result
                self.voxel_world_pos = current_voxel_pos

                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True

            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_pos.x += dx
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_voxel_pos.y += dy
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
        return False

    def grow_plant(self, plant_seed_voxel):
        pass

    def change_voxel(self, voxel_world_pos_x, voxel_world_pos_y, voxel_world_pos_z):

        chunk_index = get_chunk_index((voxel_world_pos_x, voxel_world_pos_y, voxel_world_pos_z))
        chunk = self.chunks[chunk_index]
        chunk.voxels[chunk.voxels.size - 1] = 99
        chunk.mesh.rebuild()

        if chunk.is_empty:
            chunk.is_empty = False

        # result = self.get_voxel_id(voxel_world_pos)
        # if result[0]:
        #     _, voxel_index, _, chunk = result
        #     chunk.voxels[voxel_index] = new_voxel_id
        #     chunk.mesh.rebuild()
        #
        #     # was it an empty chunk
        #     if chunk.is_empty:
        #         chunk.is_empty = False

    def add_test_voxels(self):

        for y in range(100):

            voxel_world_pos_x = random.randint(0, WORLD_W * CHUNK_SIZE - 2)
            voxel_world_pos_y = random.randint(20, 20)
            voxel_world_pos_z = random.randint(0, WORLD_H * CHUNK_SIZE - 2)

            chunk_index = get_chunk_index((voxel_world_pos_x, 20, voxel_world_pos_z))
            chunk = self.chunks[chunk_index]
            for i in range(0, chunk.voxels.size):
                chunk.voxels[i] = 1
            chunk.mesh.rebuild()

            if chunk.is_empty:
                chunk.is_empty = False

    #        voxel_index = random.randint(0, self.app.scene.world.voxels.size - 1)

        # voxel_world_pos_x = random.randint(0, WORLD_W * CHUNK_SIZE - 2)
        # voxel_world_pos_y = random.randint(10, WORLD_D * CHUNK_SIZE - 2)
        # voxel_world_pos_z = random.randint(0, WORLD_H * CHUNK_SIZE - 2)
        #
        # voxel_world_pos = glm.ivec3(voxel_world_pos_x, voxel_world_pos_y, voxel_world_pos_z)

        # voxel_world_pos = glm.ivec3(1, 1, 1)
        #
        # result = self.get_voxel_id(voxel_world_pos)
        # #
        # # # is the new place empty?
        # # if not result[0]:
        # _, voxel_index, _, chunk = result
        #
        # chunk.voxels[voxel_index] = self.new_voxel_id
        # chunk.mesh.rebuild()

        # was it an empty chunk
        # if chunk.is_empty:
        #      chunk.is_empty = False


    def get_voxel_id(self, voxel_world_pos):
        cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE

        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
            chunk_index = cx + WORLD_W * cz + WORLD_AREA * cy
            chunk = self.chunks[chunk_index]

            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * CHUNK_SIZE

            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            voxel_id = chunk.voxels[voxel_index]

            return voxel_id, voxel_index, voxel_local_pos, chunk
        return 0, 0, 0, 0


    def check_player_collision(self, player_position, dx=0, dy=0, dz=0):
        # start point
        x1, y1, z1 = self.app.player.position
        # end point

        int_pos = (
            int(player_position.x + dx + (
                PLAYER_SIZE if dx > 0 else -PLAYER_SIZE if dx < 0 else 0)
                ),
            int(player_position.y + dy + (
                PLAYER_SIZE if dy > 0 else -PLAYER_SIZE if dy < 0 else 0)
                ),
            int(player_position.z + dz + (
                PLAYER_SIZE if dz > 0 else -PLAYER_SIZE if dz < 0 else 0)
                )
        )

        next_pos = glm.ivec3(int(player_position.x + dx + (PLAYER_SIZE if dx > 0 else -PLAYER_SIZE if dx < 0 else 0)),
                             int(player_position.y + dy + (PLAYER_SIZE if dy > 0 else -PLAYER_SIZE if dy < 0 else 0)),
                             int(player_position.z + dz + (PLAYER_SIZE if dz > 0 else -PLAYER_SIZE if dz < 0 else 0)))

        result = self.get_voxel_id(voxel_world_pos=next_pos)

        if result[0] and (0 <= next_pos[0] <= WORLD_W * CHUNK_SIZE and 0 <= next_pos[1] <= WORLD_H * CHUNK_SIZE and 0 <= next_pos[2] <= WORLD_D * CHUNK_SIZE):
            return True
        else:
            return False


