from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass

import numpy as np

from opps.model import Bend, Elbow, Flange, Pipe, Pipeline, Point


class PipelineEditor:
    def __init__(self, origin=(0, 0, 0)):
        self.pipeline = Pipeline()
        self.control_points = [Point(0,0,0)]

    def set_active_point(self, point):
        return
        self.current_point = np.array(point)

    def set_deltas(self, deltas):
        self.deltas = np.array(deltas)

    def add_pipe(self, deltas=None):
        if deltas != None:
            self.deltas = deltas

        current_point = self.control_points[-1]
        next_point = Point(*(current_point.coords() + self.deltas))

        new_pipe = Pipe(
            current_point, 
            next_point,
        )

        self.control_points.append(next_point)
        self.pipeline.add_structure(new_pipe)
        self.update_joints_2()

    def add_bend(self):
        start_point = self.control_points[-1]
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        self.control_points.append(corner_point)
        self.control_points.append(end_point)

        new_bend = Bend(
            start_point,
            end_point,
            corner_point,
            0.3
        )
        self.pipeline.add_structure(new_bend)
        self.update_joints_2() 
    
    def update_joints_2(self):
        for joint in self.pipeline.components:
            if not isinstance(joint, Bend):
                continue
            
            connected_points = self._oposite_point_2(joint.start) + self._oposite_point_2(joint.end)
            if len(connected_points) < 2:
                continue

            oposite_a, oposite_b, *_ = connected_points
            # print(joint)
            joint.normalize_values_2(oposite_a, oposite_b)
            # print(joint)
            # print()

    def _oposite_point_2(self, point):
        oposite_points = []
        for pipe in self.pipeline.components:
            if not isinstance(pipe, Pipe):
                continue

            if pipe.start == point:
                oposite_points.append(pipe.end)

            elif pipe.end == point:
                oposite_points.append(pipe.start)
        
        return oposite_points

    def move_control_point(self, origin, target):
        coords_mapper = dict()
        coords_mapper[tuple(origin)] = target

        for structure in self.pipeline.components:
            structure.map_coords(coords_mapper)

        if (self.current_point == origin).all:
            self.current_point = target            
        self._update_joints()

    def _update_joints(self):
        coords_mapper = dict()
        for joint in self.pipeline.components:
            if not isinstance(joint, Bend):
                continue

            oposite_a = self._oposite_point(joint.start)
            oposite_b = self._oposite_point(joint.end)
            
            if oposite_a is None:
                continue

            if oposite_b is None:
                continue
                
            old_start = joint.start
            old_end = joint.end

            joint.start = oposite_a
            joint.end = oposite_b
            joint.normalize_values()

            coords_mapper[tuple(old_start)] = joint.start
            coords_mapper[tuple(old_end)] = joint.end

        for structure in self.pipeline.components:
            structure.map_coords(coords_mapper)

    def _pipes_at(self, point):
        pipes = []
        for pipe in self.pipeline.components:
            if not isinstance(pipe, Pipe):
                continue
            if (pipe.start == point).all():
                pipes.append(pipe)
            elif (pipe.end == point).all():
                pipes.append(pipe)
        return pipes

    def _oposite_point(self, point):
        oposite_point = None
        for pipe in self.pipeline.components:
            if not isinstance(pipe, Pipe):
                continue

            if (pipe.start == point).all():
                oposite_point = pipe.end
                break

            elif (pipe.end == point).all():
                oposite_point = pipe.start
                break

        return oposite_point




    # def add_pipe(self):    
    #     self.dismiss()

    #     if (self.deltas == (0,0,0)).all():
    #         return
        
    #     connected_pipes = self.pipeline.find_pipes_at(self.current_point)
    #     self.backup.extend(connected_pipes)
    #     for structure in connected_pipes:
    #         self.pipeline.remove_structure(structure)
        
    #     new_pipe = Pipe(self.current_point, self.current_point + self.deltas)
    #     new_pipe.color = (255, 0, 0)
    #     self.staged_structures.append(new_pipe)
        
    #     connected_pipes_copy = deepcopy(connected_pipes)
    #     self.staged_structures.extend(connected_pipes_copy)
    #     bends = self.add_joints(self.staged_structures)
    #     for bend in bends:
    #         bend.color = (255, 0, 0)

    #     for structure in self.staged_structures:
    #         self.pipeline.add_structure(structure)

    def add_flange(self):
        new_flange = Flange(self.current_point)
        # self.control_points_to_structures[tuple(self.current_point)].append(new_flange)
        # self.structure_to_control_points[new_flange].append(new_flange)
    
    def dismiss(self):
        return
    
    def commit(self):
        return
        self.current_point = self.current_point.coords() + self.deltas
        # for structure in self.staged_structures:
        #     structure.color = (255, 255, 255)
        # self.staged_structures.clear()
        # self.backup.clear()
        # self.recalculate_control_points()

    def reposition_structure(self, obj):
        if isinstance(obj, Pipe):
            self.reposition_pipe(obj)
        elif isinstance(obj):
            self.reposition_flange(obj)
        else:
            raise ValueError("OPSI")

    def reposition_pipe(self, pipe: Pipe):
        pipe.start = self.current_point
        pipe.end = pipe.start + self.deltas

    def reposition_flange(self, flange: Flange):
        flange.position = flange

    # def move_control_point(self, target):
    #     origin = tuple(self.current_point)
    #     target = tuple(target)

    #     if origin == target:
    #         return

    #     if target in self.control_points_to_structures:
    #         return

    #     origin_structures = self.control_points_to_structures[origin]
    #     if not origin_structures:
    #         return

    #     self.current_point = np.array(target)
    #     # self.control_points_to_structures[target] = origin_structures
    #     # self.control_points_to_structures.pop(origin)

    #     new_coordinates = dict()
    #     new_coordinates[origin] = target
    #     for joint in origin_structures:
    #         if not isinstance(joint, Bend | Elbow):
    #             continue
    #         for point in joint.get_points():
    #             new_coordinates[tuple(point)] = target
        
    #     for structure in origin_structures:
    #         structure.map_coords(new_coordinates)

    #     self.recalculate_control_points()
        
    #     for structures in self.control_points_to_structures.values():
    #         self.update_joints(structures)
    #         to_remove = []
    #         for i, struct in enumerate(structures):
    #             if struct is None:
    #                 to_remove.append(i)
    #         for i in reversed(to_remove):
    #             print("alguém?")
    #             structures.pop(i)

    def update_joints(self, structures):
        for joint in structures:
            if not isinstance(joint, Bend):
                continue

            oposite_a = self.get_oposite_point(joint.start, structures)
            oposite_b = self.get_oposite_point(joint.end, structures)
            
            if oposite_a is None:
                continue

            if oposite_b is None:
                continue
                
            old_start = joint.start
            old_end = joint.end

            joint.start = oposite_a
            joint.end = oposite_b
            joint.normalize_values()

            self.replace_point(old_start, joint.start, structures)
            self.replace_point(old_end, joint.end, structures)


    def recalculate_control_points(self):
        self.control_points_to_structures.clear()
        pipes = [i for i in self.pipeline.components if isinstance(i, Pipe)]
        joints = [i for i in self.pipeline.components if isinstance(i, Bend)]

        for pipe in pipes:
            self.control_points_to_structures[tuple(pipe.start)].append(pipe)
            self.control_points_to_structures[tuple(pipe.end)].append(pipe)

        for joint in joints:
            start_structures = self.control_points_to_structures.pop(tuple(joint.start), [])
            end_structures = self.control_points_to_structures.pop(tuple(joint.end), [])
            merged_structures = [joint] + start_structures + end_structures
            self.control_points_to_structures[tuple(joint.corner)] = merged_structures
        
    def add_joints(self, structures):
        pipe_groups = defaultdict(list)
        pipes = [i for i in structures if isinstance(i, Pipe)]
        bends = []

        for pipe in pipes:
            pipe_groups[tuple(pipe.start)].append(pipe)
            pipe_groups[tuple(pipe.end)].append(pipe)

        for pipe_group in pipe_groups.values():
            if len(pipe_group) != 2:
                continue
            bend = self.connect_pipes_with_bend(*pipe_group)
            if bend is not None:
                bends.append(bend)

        structures.extend(bends)

        return bends
    
    def get_pipes_at(self, point, structures):
        pipes = []
        for pipe in structures:
            if not isinstance(pipe, Pipe):
                continue
            if (pipe.start == point).all():
                oposite_point = pipe.end
                break

            elif (pipe.end == point).all():
                oposite_point = pipe.start
                break
        return pipes

    def get_oposite_point(self, point, structures):
        oposite_point = None
        for pipe in structures:
            if not isinstance(pipe, Pipe):
                continue

            if (pipe.start == point).all():
                oposite_point = pipe.end
                break

            elif (pipe.end == point).all():
                oposite_point = pipe.start
                break

        return oposite_point
    
    def replace_point(self, old_point, new_point, structures):
        for pipe in structures:
            if not isinstance(pipe, Pipe):
                continue

            if (pipe.start == old_point).all():
                pipe.start = new_point
                break

            elif (pipe.end == old_point).all():
                pipe.end = new_point
                break

    def connect_pipes_with_bend(self, pipe_a, pipe_b):
        # avoid configurations like ← → or → ←
        if (pipe_a.start == pipe_b.end).all():
            pipe_a, pipe_b = pipe_b, pipe_a
        elif (pipe_a.end == pipe_b.end).all():
            pipe_b.start, pipe_b.end = pipe_b.end, pipe_b.start
        elif (pipe_a.start == pipe_b.start).all():
            pipe_a.start, pipe_a.end = pipe_a.end, pipe_a.start

        bend = Bend(start=pipe_a.start, 
                    end=pipe_b.end, 
                    corner=pipe_a.end,
                    curvature=pipe_a.diameter / 2,
                    diameter=pipe_a.diameter)

        if np.isnan(bend.center).any():
            return None

        pipe_a.end = bend.start
        pipe_b.start = bend.end
        return bend

    def remove_joints(self, structures):
        joints = [i for i in structures if isinstance(i, Bend)]
        pipes = [i for i in structures if isinstance(i, Pipe)]

        indexes_to_remove = []
        for i, s in enumerate(structures):
            if isinstance(s, Bend):
                indexes_to_remove.append(i)
        indexes_to_remove.sort(reverse=True)

        for i in indexes_to_remove:
            structures.pop(i)

        replace_dict = dict()
        for joint in joints:
            replace_dict[tuple(joint.start)] = joint.get_corner()
            replace_dict[tuple(joint.end)] = joint.get_corner()

        for pipe in pipes:
            pipe.start = np.array(replace_dict.get(tuple(pipe.start), pipe.start))
            pipe.end = np.array(replace_dict.get(tuple(pipe.end), pipe.end))