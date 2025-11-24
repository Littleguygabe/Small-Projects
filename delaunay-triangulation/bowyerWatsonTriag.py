import matplotlib.pyplot as plt
import numpy as np

class Triangle:
    def __init__(self, v1, v2, v3) -> None:
        self.vertices = np.array([v1, v2, v3]) 
        self.edges = np.array([[v1, v2], [v2, v3], [v3, v1]])

    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        # Simple bounding box check first for speed
        return np.allclose(np.sort(self.vertices, axis=0), np.sort(other.vertices, axis=0))

    def __hash__(self):
        v_sorted = np.sort(self.vertices, axis=0)
        return hash(tuple(map(tuple, v_sorted)))

    def display(self):
        plot_positions = np.vstack([self.vertices, self.vertices[0]])
        plt.plot(plot_positions[:, 0], plot_positions[:, 1], 'b-', linewidth=0.5)

    def displayFill(self):
        plot_positions = np.vstack([self.vertices, self.vertices[0]])
        plt.plot(plot_positions[:, 0], plot_positions[:, 1], 'b-', linewidth=0.5)
        plt.fill(plot_positions[:, 0], plot_positions[:, 1],color='green') 

def getSuperTriangle(points):
    x_max = points[:, 0].max()
    x_min = points[:, 0].min()
    y_max = points[:, 1].max()
    y_min = points[:, 1].min()
    
    w, h = x_max - x_min, y_max - y_min

    triangle_points = np.array([
        [x_min - w*1.5, y_min - h],
        [x_max + w*1.5, y_min - h],
        [x_min + w * 0.5, y_max + h]
    ])
    return triangle_points 

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

def checkInTriangle(point_to_check, circle_perim_points):
    p0, p1, p2 = circle_perim_points[0], circle_perim_points[1], circle_perim_points[2]

    orientation = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])

    if orientation < 0:
        p1, p2 = p2, p1

    checking_matrix = np.array([
        [p0[0], p0[1], p0[0]**2 + p0[1]**2, 1],
        [p1[0], p1[1], p1[0]**2 + p1[1]**2, 1],
        [p2[0], p2[1], p2[0]**2 + p2[1]**2, 1],
        [point_to_check[0], point_to_check[1], point_to_check[0]**2 + point_to_check[1]**2, 1]
    ])

    d = det_4x4(checking_matrix)
    return d > 0

def formEdgePointTriangle(edge, point):
    return Triangle(edge[0], edge[1], point)

def checkEdges(edge_to_check, edges):
    for edge in edges:
        if np.allclose(edge, edge_to_check) or np.allclose(edge, edge_to_check[::-1]):
            return True
    return False

def runBowyerWatson(points):
    v1,v2,v3 = getSuperTriangle(points)
    st = Triangle(v1,v2,v3)
    triangulation = {st}

    for point in points:
        badTriangles = set()
        for triangle in triangulation:
            if checkInTriangle(point, triangle.vertices):
                badTriangles.add(triangle)

        polygon = set()
        for t1 in badTriangles:
            for edge in t1.edges:
                shared = False
                for t2 in badTriangles:
                    if t1 == t2: 
                        continue
                    if checkEdges(edge, t2.edges):
                        shared = True
                        break
                
                if not shared:
                    tup_edge = (tuple(edge[0]), tuple(edge[1]))
                    polygon.add(tup_edge)

        for triangle in badTriangles:
            triangulation.discard(triangle)

        for edge in polygon:
            triangulation.add(formEdgePointTriangle(np.array(edge), point))
            
    final_triangulation = list(triangulation)

    #want to keep the super triangle for generating voronoi graph

    # for triangle in final_triangulation:
    #     shares_super_vertex = False
    #     for v in triangle.vertices:
    #         for sv in [v1,v2,v3]:
    #             if np.allclose(v, sv):
    #                 shares_super_vertex = True
    #                 break
    #         if shares_super_vertex: break
            
    #     if shares_super_vertex:
    #         triangulation.discard(triangle)



    if __name__ == '__main__':
        plt.figure()
        plt.scatter(points[:,0], points[:,1], color='red', zorder=10)
        for triangle in triangulation:
            triangle.display()

    return triangulation

def drawEdge(edge,prev_edge):
    p1, p2 = edge
    # To plot a line from p1 to p2, plt.plot needs a list of x-coordinates and a list of y-coordinates
    x_coords, y_coords = [p1[0], p2[0]], [p1[1], p2[1]]
    
    print(f"Plotting edge: {p1} to {p2}")
    
    plt.plot(x_coords, y_coords, color='red')
    
    if prev_edge is not None:
        prev_p1, prev_p2 = prev_edge
        prev_x, prev_y = [prev_p1[0], prev_p2[0]], [prev_p1[1], prev_p2[1]]
        plt.plot(prev_x, prev_y, color='black')

    prev_edge = edge

    return prev_edge

def getSharedTriangles(edge, triangulation):
    shared_triangles = []
    edge_np = np.array(edge)

    for t in triangulation:
        for t_edge in t.edges:
            if np.allclose(t_edge, edge_np) or np.allclose(t_edge, edge_np[::-1]):
                shared_triangles.append(t)
                break
    
    t1 = shared_triangles[0] if len(shared_triangles) > 0 else None
    t2 = shared_triangles[1] if len(shared_triangles) > 1 else None
    return t1, t2

def getCircumCenter(triangle):
    a,b,c = triangle.vertices
    ax,ay = a
    bx,by = b
    cx,cy = c

    
    D = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))

    ux = (1/D)*((ax**2+ay**2)*(by-cy)+(bx**2+by**2)*(cy-ay)+(cx**2+cy**2)*(ay-by))
    uy = (1/D)*((ax**2+ay**2)*(cx-bx)+(bx**2+by**2)*(ax-cx)+(cx**2+cy**2)*(bx-ax))

    #need to fix this function

    return (ux,uy)

def runVoronoi(triangulation): #triangulation has the super triangle contained
    #flatted to get all the edges of the triangles in the array and remove duplicate edges
    
    flattened_edges = set()
    for t in triangulation:
        for edge in t.edges:
            v1, v2 = edge
            v1_tuple = tuple(v1.tolist())
            v2_tuple = tuple(v2.tolist())
            # To avoid duplicate edges like (a,b) and (b,a), we use a canonical representation (sorted)
            canonical_edge = tuple(sorted((v1_tuple, v2_tuple)))
            flattened_edges.add(canonical_edge)
    
    prev_edge = None
    for edge in flattened_edges:

        #calculate the circumcentre of the 2 triangles that share this edge

        t1,t2 = getSharedTriangles(edge,triangulation)

        if t1:
            t1.displayFill()
            centre = getCircumCenter(t1)
            plt.plot(centre[0],centre[1],marker = 'x',color='blue')

        if t2:
            centre = getCircumCenter(t2)
            plt.plot(centre[0],centre[1],marker = 'x',color='blue')
            t2.displayFill()
        
        prev_edge = drawEdge(edge,prev_edge)
        plt.pause(0.2)

if __name__ == '__main__':
    plt.ion()
    points = np.array([[3.0, 0.0], [2.0, 0.0], [2.0, 0.75],
                   [2.5, 0.75], [2.5, 0.6], [2.25, 0.6], 
                   [2.25, 0.2], [3.0, 0.2], [3.0, 0.0]])

    triangulation = runBowyerWatson(points)
    runVoronoi(triangulation)
    plt.ioff()
    plt.show()