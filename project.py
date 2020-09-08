from tkinter import *
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def plotSerie(serief):
    plt.clf()
    plt.plot(serief, color='blue')
    plt.title('Time Series')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.axis('off')


def sliding_windows(m, t, series):
    coords = []
    for i in range(0, len(series) - 1):
        if i + m * t > len(series) - 1:
            return coords
        else:
            point = []
            for j in range(0, m + 1):
                point.append(series[i + j * t])
            coords.append(point)
    return coords


def plot_2d(window):
    fig = plt.figure()

    ax = fig.add_subplot(111)
    x = []
    y = []
    for i in window:
        x.append(i[0])
        y.append(i[1])

    ax.scatter(x, y, s=30, c='r')
    ax.text(0.05, 0.95, "", transform=ax.transAxes)

    plt.show()


##plot sliding windows com matplotlib (usando scatter plot)
def plot_3d(window):
    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []
    for i in window:
        x.append(i[0])
        y.append(i[1])
        z.append(i[2])
    print(len(x), len(y), len(z))

    ax.scatter3D(x, y, z, s=30, c='r')
    ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

    plt.show()


##plot sliding windows com matplotlib (usando scatter plot)
def plot_4d(window):
    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []
    t = []
    for i in window:
        x.append(i[0])  # transformar para numpay array, verificar o mesmo formato
        y.append(i[1])
        z.append(i[2])
        t.append(i[3])
    x2 = np.array(x)
    y2 = np.array(y)
    z2 = np.array(z)
    c = np.array(t)
    img = ax.scatter(x2, y2, z2, c=c, cmap=plt.hot())
    fig.colorbar(img)
    plt.show()


##Converter window num numpy array. Retorna  unique values (esses valores foram plotados).
def toNumpyArray(window):  # p encontrar a matriz de dists
    np_array = np.unique(np.asarray(window), axis=0)
    return np_array


# Obter a Matriz de Distância para/de todos os pontos
def getDistanceMatrix(numpy_window):
    dist_matrix = []
    for i in numpy_window:
        line = []
        for j in numpy_window:
            dist = np.linalg.norm(i - j)
            line.append(dist)
        dist_matrix.append(line)
    return np.asarray(dist_matrix)


## Matriz simplicial
def getEmptySimplicialMatrix(dist_matrix):
    simplicial_matrix = np.zeros((len(dist_matrix[0]), len(dist_matrix)))
    return simplicial_matrix


##update na matriz simplicial. Critério :(se 2 pontos  são menores ou iguais a distancia, atualize o valor na matriz simplicial para 1)
def updateSimplicialMatrix(simplicial_matrix, dist_matrix, dist):
    for i in range(0, len(dist_matrix)):
        for j in range(0, len(dist_matrix)):
            if dist_matrix[i][j] <= dist:
                simplicial_matrix[i][j] = 1
    return simplicial_matrix


##obter lista de simplices atualizando a distância de início até que todos os "elementos" estejam conectados
def getSimplicialList(simplicial_matrix, dist_matrix, start_dist, step):
    simplicial_list = []
    while np.all(simplicial_matrix) != 1:
        simplicial_matrix = updateSimplicialMatrix(simplicial_matrix, dist_matrix, start_dist)
        simplicial_list.append(simplicial_matrix.copy())
        start_dist = start_dist + step
    return simplicial_list


##Método auxiliar para obter apenas os simpliciais
# noinspection PyGlobalUndefined
def getUniqueSimplicialList(simplicial_list):
    global found
    unique_simplicial_list = [simplicial_list[0]]
    for simplicial in simplicial_list:
        for unique_simplicial in unique_simplicial_list:
            found = 0
            if (simplicial == unique_simplicial).all():
                found = 1
                break
        if found == 0:
            unique_simplicial_list.append(simplicial)
    return unique_simplicial_list


## Todos as tuplas "válidas" desde simplices até criar os grafos
def getTuplesFromSimplicialList(simplicial_list):
    list_of_tuples = []
    for simplicial in simplicial_list:
        tuples = []
        for i in range(0, len(simplicial)):
            for j in range(0, len(simplicial[i])):
                if simplicial[i][j] == 1:
                    tuples.append((i, j))
        list_of_tuples.append(tuples)
    return list_of_tuples


## Criando os grafos a partir das tuplas de simpliciais
def get_graph_list(list_of_tuples):
    graph_list = []
    for i in list_of_tuples:
        g = nx.Graph()
        g.add_edges_from(i)
        graph_list.append(g)
    return graph_list


##Plot grafo
options = {
    'node_color': 'red',
    'node_size': 50,
    'width': 0.1,
}


def plotGraph(graph):
    nx.draw(graph, **options)
    plt.show()


class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Times", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()

        self.sextoContainer = Frame(master)
        self.sextoContainer["pady"] = 20
        self.sextoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Convertendo Séries Temporais em Complexos Simpliciais",
                            fg="purple")
        self.titulo["font"] = ("Helvetica", "16", "bold")
        self.titulo.pack()

        self.tipoEntraLabel = Label(self.segundoContainer, text="Série Temporal", font=self.fontePadrao)
        self.tipoEntraLabel.pack(side=LEFT)

        self.tipoEntra = Entry(self.segundoContainer)
        self.tipoEntra["width"] = 25
        self.tipoEntra["font"] = self.fontePadrao
        self.tipoEntra.pack(side=LEFT)

        self.dimensaoLabel = Label(self.terceiroContainer,
                                   text="Escolha o parâmetro d, lembre-se que ele corresponde a dimensão de reconstrução",
                                   font=self.fontePadrao)
        self.dimensaoLabel.pack(side=LEFT)

        self.dimensao = Entry(self.terceiroContainer)
        self.dimensao["width"] = 30
        self.dimensao["font"] = self.fontePadrao
        self.dimensao.pack(side=LEFT)

        self.delayLabel = Label(self.quartoContainer,
                                text="Escolha o parâmetro tau, lembre-se que ele corresponde ao delay da reconstrução",
                                font=self.fontePadrao)
        self.delayLabel.pack(side=LEFT)

        self.delay = Entry(self.quartoContainer)
        self.delay["width"] = 30
        self.delay["font"] = self.fontePadrao
        self.delay.pack(side=LEFT)

        self.autenticar = Button(self.quintoContainer)
        self.autenticar["text"] = "Converter TS em SC"
        self.autenticar["font"] = ("Times", "10")
        self.autenticar["width"] = 20
        self.autenticar["command"] = self.converteTsinSC
        self.autenticar.pack()

    def converteTsinSC(self):
        serie = eval(self.tipoEntra.get())
        d = int(self.dimensao.get())
        tau = int(self.delay.get())

        plotSerie(serie)
        window_t = sliding_windows(d, tau, serie)
        if d == 4:
            plot_4d(window_t)
        elif d == 3:
            plot_3d(window_t)
        elif d == 2:
            plot_2d(window_t)
        elif d == 1:
            print("Com esse valor de d não conseguiremos reconstruir o espaço, que tal escolher um outro valor?!")
        else:
            plot_4d(window_t)

        numpy_window = toNumpyArray(window_t)
        dist_matrix = getDistanceMatrix(numpy_window)
        simplicial_matrix = getEmptySimplicialMatrix(dist_matrix)
        simplicial_list = getSimplicialList(simplicial_matrix, dist_matrix, 0.1, 0.8)
        unique = getUniqueSimplicialList(simplicial_list)
        list_of_tuples = getTuplesFromSimplicialList(unique)
        graph_list = get_graph_list(list_of_tuples)
        print("Matriz de distâncias:", np.array_str(dist_matrix, precision=3))
        plotGraph(graph_list[-1])


janela = Tk()
Application(janela)
janela.mainloop()
