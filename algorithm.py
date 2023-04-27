import matplotlib.pyplot as plt
import networkx as nx
import random
import math


def create_multigraph_struct(graph):
    G = nx.MultiDiGraph()
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] != 0 and i != j:
                G.add_edge(f'{i}', f'{j}', weight=graph[i][j])
    return G


def create_graph_struct(path_arr, graph):
    G = nx.DiGraph()
    data = []
    for j in range(len(path_arr)):
        if j + 1 < len(path_arr):
            data.append(path_arr[j + 1])
    data.append(path_arr[0])
    for i in range(len(path_arr)):
        G.add_edge(f'{path_arr[i]}', f'{data[i]}', weight=graph[path_arr[i]][data[i]])
    return G


def make_plt(flag, path_arr, graph, i, path_len, t):
    """Рисует графы с помощью бибилиотеки matplotlib и сохраняет в папку pictures"""
    pos = {'0': [0, 0.25],
           '1': [-0.55, 0.25],
           '2': [-0.55, -0.4],
           '3': [0.2, -0.5],
           '4': [0.45, 0],
           '5': [-0.15, -0.0775903]}
    path = ''

    if flag == 'multi':
        G = create_multigraph_struct(graph)
        snapshot_name = "pictures/initial.png"
    else:
        G = create_graph_struct(path_arr, graph)
        snapshot_name = f"pictures/{i}.png"
        path = f'{str(path_arr[0])}-{str(path_arr[1])}-' \
               f'{str(path_arr[2])}-{str(path_arr[3])}-' \
               f'{str(path_arr[4])}-{str(path_arr[5])}'

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='green', alpha=0.6)
    # edges
    nx.draw_networkx_edges(G, pos, width=2)
    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    if flag == "basic":
        # edge weight labels
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        plt.title(f'Номер итерации: {i}')
        plt.text(0.7, 0, f'Путь: {path}')
        plt.text(0.7, -0.07, f'Длина пути: {path_len}')
        plt.text(0.7, -0.14, f'Температура: {t}')
    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(snapshot_name, dpi=65, bbox_inches='tight')
    plt.close()


def draw_graph(data, graph):
    """Визуализация графов"""
    flag = 'multi'
    make_plt(flag, data[0][1], graph, 0, data[0][0], data[0][3])

    # рисуем стадии работы цикла
    for i in range(len(data)):
        flag = 'basic'
        make_plt(flag, data[i][1], graph, data[i][0], data[i][2], data[i][3])


def generate_random_path(graph):
    """Генерирует рандомно гамильтонов цикл в графе и считает его длину"""
    g_flag = 0
    path = []
    leng = 0
    while g_flag == 0:
        list = [0, 1, 2, 3, 4, 5]
        path = []
        leng = 0
        v = random.choice(list)
        path.append(v)
        list.remove(v)
        for i in range(1, len(graph)):
            flag = 0
            while flag == 0:
                v = random.choice(list)
                if graph[path[i-1]][v] != 0:
                    path.append(v)
                    list.remove(v)
                    leng += graph[path[i-1]][v]
                    flag = 1
        if graph[path[len(graph)-1]][path[0]] != 0:
            leng += graph[path[len(graph)-1]][path[0]]
            g_flag = 1

    return path, leng


def check_edges(path, graph):
    """Проверяет является ли путь гамильтоновым циклом"""
    leng = -1
    for i in range(len(path)):
        if i == len(path)-1:
            if graph[path[i]][path[0]] == 0:
                return False, leng
            else:
                leng += graph[path[i]][path[0]]
        else:
            if graph[path[i]][path[i+1]] == 0:
                return False, leng
            else:
                leng += graph[path[i]][path[i+1]]
    return True, leng


def simulated_annealing_method(graph, alpha):
    data_for_pics = []

    # находим рандомный цикл в графе
    path, len_path = generate_random_path(graph)
    t = 100
    i = 0

    data_for_pics.append([i, path, len_path, t])

    while data_for_pics[i][1] != data_for_pics[i-1][1] != data_for_pics[i-2][2] != data_for_pics[i-3][3] or i < 4:
        path1 = path.copy()
        len1_path = 0

        g_flag = 0
        while g_flag == 0:
            # генерируем индексы по которым будем менять вершины в пути
            flag = 0
            v1 = random.randint(0, 5)
            v2 = -1
            while flag == 0:
                v2 = random.randint(0, 5)
                if v2 != v1:
                    flag = 1
            path1[v1], path1[v2] = path1[v2], path1[v1]

            # проверяем является ли новый путь гамильтоновым циклом
            booll, new_len = check_edges(path1, graph)
            if booll:
                g_flag = 1
                len1_path = new_len

        # вычисляем дельту длин маршрутов
        delta_l = len1_path - len_path

        if delta_l < 0:
            path = path1
            len_path = len1_path
        else:
            p_rand = random.randint(0, 100)
            p = 100 * math.exp(-delta_l/t)
            if p > p_rand:
                path = path1
                len_path = len1_path

        i += 1
        data_for_pics.append([i, path, len_path, round(t, 2)])
        t *= alpha

    for el in data_for_pics:
        print(el)

    draw_graph(data_for_pics, graph)
    return data_for_pics