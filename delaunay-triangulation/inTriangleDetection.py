import numpy as np

def det_4x4(m):
    det_0 = (m[1][1] * (m[2][2] * m[3][3] - m[2][3] * m[3][2]) -
             m[1][2] * (m[2][1] * m[3][3] - m[2][3] * m[3][1]) +
             m[1][3] * (m[2][1] * m[3][2] - m[2][2] * m[3][1]))

    det_1 = (m[1][0] * (m[2][2] * m[3][3] - m[2][3] * m[3][2]) -
             m[1][2] * (m[2][0] * m[3][3] - m[2][3] * m[3][0]) +
             m[1][3] * (m[2][0] * m[3][2] - m[2][2] * m[3][0]))

    det_2 = (m[1][0] * (m[2][1] * m[3][3] - m[2][3] * m[3][1]) -
             m[1][1] * (m[2][0] * m[3][3] - m[2][3] * m[3][0]) +
             m[1][3] * (m[2][0] * m[3][1] - m[2][1] * m[3][0]))

    det_3 = (m[1][0] * (m[2][1] * m[3][2] - m[2][2] * m[3][1]) -
             m[1][1] * (m[2][0] * m[3][2] - m[2][2] * m[3][0]) +
             m[1][2] * (m[2][0] * m[3][1] - m[2][1] * m[3][0]))

    return (m[0][0] * det_0) - (m[0][1] * det_1) + (m[0][2] * det_2) - (m[0][3] * det_3)




if __name__ == '__main__':
    circle_perim_points = [
        [2,2],
        [0,0],
        [4,0]
    ]

    point_to_check = [2,1]

    #use the Guibas & Stolfi method of finding the det of a specific matrix to establish if a point is within a circle
    #if the det(m) > 0 then the point is within the circle

    checking_matrix = np.array([
        [circle_perim_points[0][0],circle_perim_points[0][1],circle_perim_points[0][0]**2+circle_perim_points[0][1]**2,1],
        [circle_perim_points[1][0],circle_perim_points[1][1],circle_perim_points[1][0]**2+circle_perim_points[1][1]**2,1],
        [circle_perim_points[2][0],circle_perim_points[2][1],circle_perim_points[2][0]**2+circle_perim_points[2][1]**2,1],
        [point_to_check[0],point_to_check[1],point_to_check[0]**2+point_to_check[1]**2,1]
    ])

    detm = det_4x4(checking_matrix)

    if detm>0:
        print(f'{point_to_check} is within the circle')

    else:
        print(f'{point_to_check} is not inside the circle')