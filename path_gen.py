from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import QgsProject, QgsVectorLayer, QgsMapLayer
import csv


class Node(QgsVectorLayer):
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):

        self.parent = parent
        self.position = position
        # if statement to see if the node is defined 
        if self.tot_Layer.defined(position.x, position.y):
            self.defined = True
        else:
            self.defined = False

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Astar:
    @staticmethod
    def path(self, tot_layer, start_point, end_point):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, start_point)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end_point)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1),
                                 (1, 1)]:  # Adjacent squares this needs to be adjusted

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(tot_layer) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(tot_layer[len(tot_layer) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if tot_layer[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # checking if child is defined

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


class Totdet:
    def __init__(self, pos_layer, wind_layer, water_layer):
        self.initialPos = pos_layer  # incomplete this should reference the
        self.finalPos = pos_layer
        self.windLayer = wind_layer
        self.waterLayer = water_layer

    def math_model(self):
        # insert Math model with wind and water data
        # initial position and final position describe only the two adjacent points not the goal

        return 1

    def point_passed(self, point):
        x = 8  # size of grid in km^2
        number_to_define = (x / 2 + 1) ** 2  # number of nodes to define
        step = 2  # unit step of grid usually 2 km
        index = [0.0, 0.0]
        offset = [-x / (step * 2), -x / (step * 2)]  # determines where the starting node is in the x,x grid
        relative_position = []
        defined_points = []

        # defines all nodes relative to the given node with the determined offset
        i = int(number_to_define)
        while i != 0:

            if index[0] < (x / 2 + 1):
                relative_position.append([index[0] + offset[0], index[1] + offset[1]])
                index[0] += 1
                i -= 1
            else:
                index[0] = 0
                index[1] += 1

        positions_to_define = [point for y in relative_position]

        # i is already zero from previous loop
        while i != number_to_define:
            positions_to_define[i] = [positions_to_define[i][0] + relative_position[i][0],
                                      positions_to_define[i][1] + relative_position[i][1]]
            i += 1

        i = 0
        while i != number_to_define:
            defined_points.append(self.math_model(positions_to_define[i]))
            i += 1
        return defined_points
    # need to define the points still

    @staticmethod
    def line_passed(self, geometry_linspace, r):
        # Calculation with self dot mathModel in r around the line
        return 1
