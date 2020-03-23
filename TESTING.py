class Test(object):
    def __inti__(self):
        self.something = 0
        pass

    def TESTCalc(self, test_list):
        test_list[1] = test_list[1] * 8
        test_list[0] = test_list[0] * 8
        return test_list


point = [123.0, 256.0]
x = 8  # size of grid in km^2
number_to_define = (x / 2 + 1) ** 2  # number of nodes to define
step = 2  # unit step of grid usually 2 km
index = [0.0, 0.0]
offset = [-x / (step * 2), -x / (step * 2)]  # determines where the starting node is in the x,x grid
relative_position = []

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
defined_points = []

BS = Test

while i != number_to_define:
    defined_points.append(Test.TESTCalc(positions_to_define[i]))
    i += 1

print(defined_points)


