import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#Алгоритм Лианга-Барски (через параметрическое задание отрезков)
#Алгоритм отсечения выпуклого многоугольника 

def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    n = int(lines[0].strip())  # Number of segments
    segments = [tuple(map(int, line.strip().split())) for line in lines[1:n+1]]
    clipping_window = tuple(map(int, lines[n+1].strip().split()))

    return segments, clipping_window

def convert_segments_to_polygon(segments):
    return [segments[i][:2] for i in range(len(segments))] + [segments[-1][2:]]

def convex_polygon_clipping(subjectPolygon, clipPolygon):
    def inside(p, edge):
        a, b = edge
        return (b[0]-a[0])*(p[1]-a[1]) > (b[1]-a[1])*(p[0]-a[0])

    def computeIntersection(s, e, edge):
        a, b = edge
        dc = [a[0] - b[0], a[1] - b[1]]
        dp = [s[0] - e[0], s[1] - e[1]]
        n1 = a[0] * b[1] - a[1] * b[0]
        n2 = s[0] * e[1] - s[1] * e[0] 
        n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
        return [(n1*dp[0] - n2*dc[0]) * n3, (n1*dp[1] - n2*dc[1]) * n3]

    outputList = subjectPolygon
    for i in range(len(clipPolygon)):
        cp1 = clipPolygon[i]
        cp2 = clipPolygon[(i + 1) % len(clipPolygon)]
        inputList = outputList
        outputList = []
        s = inputList[-1]

        for subjectVertex in inputList:
            e = subjectVertex
            if inside(e, (cp1, cp2)):
                if not inside(s, (cp1, cp2)):
                    outputList.append(computeIntersection(s, e, (cp1, cp2)))
                outputList.append(e)
            elif inside(s, (cp1, cp2)):
                outputList.append(computeIntersection(s, e, (cp1, cp2)))
            s = e
    return outputList

def liang_barsky(clip_rect, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    p = [-dx, dx, -dy, dy]
    q = [x1 - clip_rect[0], clip_rect[2] - x1, y1 - clip_rect[1], clip_rect[3] - y1]

    u1, u2 = 0.0, 1.0
    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return None  # Отрезок параллелен и находится вне границы
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                u1 = max(u1, t)
            else:
                u2 = min(u2, t)

            if u1 > u2:
                return None  # Отрезок находится вне границы

    clipped_x1 = x1 + u1 * dx
    clipped_y1 = y1 + u1 * dy
    clipped_x2 = x1 + u2 * dx
    clipped_y2 = y1 + u2 * dy
    return clipped_x1, clipped_y1, clipped_x2, clipped_y2

def plot_liang_barsky_clipping(segments, clip_rect, ax):
    # Отрисовка отсекающего прямоугольника
    ax.add_patch(mpatches.Rectangle(clip_rect[:2], clip_rect[2] - clip_rect[0], clip_rect[3] - clip_rect[1], linewidth=2, edgecolor='black', facecolor='none'))

    # Отсечение и отрисовка каждого отрезка
    for segment in segments:
        x1, y1, x2, y2 = segment
        clipped_segment = liang_barsky(clip_rect, x1, y1, x2, y2)
        if clipped_segment:
            # Отрезок частично или полностью внутри окна
            ax.plot([clipped_segment[0], clipped_segment[2]], [clipped_segment[1], clipped_segment[3]], 'green', linewidth=1.5)
            # Если отрезок частично вне окна, рисуем его часть снаружи красным цветом
            if (x1, y1) != (clipped_segment[0], clipped_segment[1]):
                ax.plot([x1, clipped_segment[0]], [y1, clipped_segment[1]], 'red', linewidth=1.5)
            if (x2, y2) != (clipped_segment[2], clipped_segment[3]):
                ax.plot([x2, clipped_segment[2]], [y2, clipped_segment[3]], 'red', linewidth=1.5)
        else:
            # Отрезок полностью вне окна
            ax.plot([x1, x2], [y1, y2], 'red', linewidth=1.5)

    ax.set_xlim(0, 400)
    ax.set_ylim(0, 400)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)


def plot_results(filename):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Читаем данные из файла
    segments, clip_rect = read_input_file(filename)

    # Отсечение выпуклого многоугольника
    subjectPolygon = convert_segments_to_polygon(segments)
    clipPolygon = [(clip_rect[0], clip_rect[1]), (clip_rect[2], clip_rect[1]), (clip_rect[2], clip_rect[3]), (clip_rect[0], clip_rect[3])]
    clippedPolygon = convex_polygon_clipping(subjectPolygon, clipPolygon)
    patch = mpatches.Polygon(subjectPolygon, closed=True, facecolor='gray', edgecolor='black')
    ax2.add_patch(patch)
    patch = mpatches.Polygon(clipPolygon, closed=True, facecolor='none', edgecolor='blue', linewidth=2)
    ax2.add_patch(patch)
    patch = mpatches.Polygon(clippedPolygon, closed=True, facecolor='red', edgecolor='black', alpha=0.5)
    ax2.add_patch(patch)
    ax2.set_title("Convex Polygon Clipping")
    ax2.set_xlim(0, 400)
    ax2.set_ylim(0, 400)
    ax2.set_aspect('equal', adjustable='box')
    ax2.grid(True)

    # Отсечение с помощью алгоритма Лианга-Барски
    plot_liang_barsky_clipping(segments, clip_rect, ax1)
    ax1.set_title("Liang-Barsky Line Clipping")

    plt.show()

plot_results('input.txt')
