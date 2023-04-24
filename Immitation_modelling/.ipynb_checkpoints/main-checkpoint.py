from Latex.latex import make_latex
import pydot
import dot2tex
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from math import factorial, exp
import sympy as sp
import re

var = 26
g = 1
n = var

name = "Пролыгина Алина Максимовна"
name_short = "Пролыгина А. М."

T = 1
dt = 0.001
N = 100


def graph(Ra, Rb, Na, Nb):
    # GREEN STATE
    graph = pydot.Dot("my_graph", graph_type="digraph", bgcolor="yellow")

    # Start node
    graph.add_node(pydot.Node("s" + str(Na) + str(Ra) + str(Nb) + str(Rb),
                              texlbl="$S^{" + str(Na) + str(Ra) + "}_{" + str(Nb) + str(Rb) + "}$",
                              style="filled",
                              fillcolor="green"))

    prev_line = ["s" + str(Na) + str(Ra) + str(Nb) + str(Rb)]
    now_line = []

    paths = dict()
    paths["s" + str(Na) + str(Ra) + str(Nb) + str(Rb)] = [0, 0, 0]
    p = 1

    # new line
    for node in prev_line:
        nNa = int(node[1])
        nRa = int(node[2])
        nNb = int(node[3])
        nRb = int(node[4])

        if nRb > 0:
            graph.add_node(pydot.Node("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb - 1),
                                      texlbl="$S^{" + str(nNa) + str(nRa) + "}_{" + str(nNb) + str(nRb - 1) + "}$"))
            paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb - 1)] = [
                p,
                paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][1],
                paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][2] + 1]
            p = p + 1
            graph.add_edge(pydot.Edge("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb), "s" + str(nNa) + str(nRa) + str(nNb) + str(nRb - 1),
                                      color="blue", label=" ", texlbl=f"${nNb}\\lambda_B$"))
            now_line.append("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb - 1))

        if nRa > 0:
            graph.add_node(pydot.Node("s" + str(nNa) + str(nRa - 1) + str(nNb) + str(nRb),
                                      texlbl="$S^{" + str(nNa) + str(nRa - 1) + "}_{" + str(nNb) + str(nRb) + "}$"))
            paths["s" + str(nNa) + str(nRa - 1) + str(nNb) + str(nRb)] = [
                p,
                paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][1] + 1,
                paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][2]]
            p = p + 1
            graph.add_edge(pydot.Edge("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb),
                                      "s" + str(nNa) + str(nRa - 1) + str(nNb) + str(nRb),
                                      color="blue", label=" ", texlbl=f"${nNa}\\lambda_A$"))
            now_line.append("s" + str(nNa) + str(nRa - 1) + str(nNb) + str(nRb))

    while len(now_line) > 0:
        prev_line = now_line
        now_line = []

        for node in prev_line:
            nNa = int(node[1])
            nRa = int(node[2])
            nNb = int(node[3])
            nRb = int(node[4])

            if nRb > 0:
                if "s" + str(nNa) + str(nRa) + str(nNb) + str(nRb - 1) not in now_line:
                    graph.add_node(pydot.Node("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb - 1),
                                          texlbl="$S^{" + str(nNa) + str(nRa) + "}_{" + str(nNb) + str(nRb - 1) + "}$"))

                    paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb - 1)] = [p,
                        paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][1],
                        paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][2] + 1]
                    p = p + 1

                    now_line.append("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb - 1))
                graph.add_edge(pydot.Edge("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb),
                                          "s" + str(nNa) + str(nRa) + str(nNb) + str(nRb - 1),
                                          color="blue", label=" ", texlbl=f"${nNb}\\lambda_B$"))
            else:
                graph.add_node(pydot.Node("s" + str(nNa) + str(nRa) + str(nNb - 1) + str(nRb),
                                          texlbl="$S^{" + str(nNa) + str(nRa) + "}_{" + str(nNb - 1) + str(nRb) + "}$",
                                          style="filled",
                                          fillcolor="red"))

                paths["s" + str(nNa) + str(nRa) + str(nNb - 1) + str(nRb)] = [-p,
                    paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][1],
                    paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][2] + 1]
                p = p + 1

                graph.add_edge(pydot.Edge("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb),
                                          "s" + str(nNa) + str(nRa) + str(nNb - 1) + str(nRb),
                                          color="blue", label=" ", texlbl=f"${nNb}\\lambda_B$"))

            if nRa > 0:
                if "s" + str(nNa) + str(nRa - 1) + str(nNb) + str(nRb) not in now_line:
                    graph.add_node(pydot.Node("s" + str(nNa) + str(nRa - 1) + str(nNb) + str(nRb),
                                          texlbl="$S^{" + str(nNa) + str(nRa - 1) + "}_{" + str(nNb) + str(nRb) + "}$"))

                    paths["s" + str(nNa) + str(nRa - 1) + str(nNb) + str(nRb)] = [
                        p,
                        paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][1] + 1,
                        paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][2]]
                    p = p + 1

                    now_line.append("s" + str(nNa) + str(nRa - 1) + str(nNb) + str(nRb))
                graph.add_edge(pydot.Edge("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb),
                                          "s" + str(nNa) + str(nRa - 1) + str(nNb) + str(nRb),
                                          color="blue", label=" ", texlbl=f"${nNa}\\lambda_A$"))
            else:
                if nNa > 1:
                    if "s" + str(nNa - 1) + str(nRa) + str(nNb) + str(nRb) not in now_line:
                        graph.add_node(pydot.Node("s" + str(nNa - 1) + str(nRa) + str(nNb) + str(nRb),
                                                  texlbl="$S^{" + str(nNa - 1) + str(nRa) + "}_{" + str(nNb) + str(nRb) + "}$"))

                        paths["s" + str(nNa - 1) + str(nRa) + str(nNb) + str(nRb)] = [
                            p,
                            paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][1] + 1,
                            paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][2]]
                        p = p + 1

                        now_line.append("s" + str(nNa - 1) + str(nRa) + str(nNb) + str(nRb))
                    graph.add_edge(pydot.Edge("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb),
                                              "s" + str(nNa - 1) + str(nRa) + str(nNb) + str(nRb),
                                              color="blue", label=" ", texlbl=f"${nNa}\\lambda_A$"))
                else:
                    graph.add_node(pydot.Node("s" + str(nNa - 1) + str(nRa) + str(nNb) + str(nRb),
                                              texlbl="$S^{" + str(nNa - 1) + str(nRa) + "}_{" + str(nNb) + str(nRb) + "}$",
                                              style="filled", fillcolor="red"))
                    paths["s" + str(nNa - 1) + str(nRa) + str(nNb) + str(nRb)] = [
                        -p,
                        paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][1] + 1,
                        paths["s" + str(nNa) + str(nRa) + str(nNb) + str(nRb)][2]]
                    p = p + 1
                    graph.add_edge(pydot.Edge("s" + str(nNa) + str(nRa) + str(nNb) + str(nRb),
                                              "s" + str(nNa - 1) + str(nRa) + str(nNb) + str(nRb),
                                              color="blue", label=" ", texlbl=f"${nNa}\\lambda_A$"))

    return graph, paths


def matrix(l_A, l_B, graph_dot):
    edges = graph_dot.get_edges()
    nodes = graph_dot.get_nodes()

    d = np.zeros((len(nodes), len(nodes)))
    l1_pat = re.compile(r"\$.\\lambda_A\$")
    l2_pat = re.compile(r"\$.\\lambda_B\$")

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            for edge in edges:
                if edge.get_source() == nodes[i].get_name() and edge.get_destination() == nodes[j].get_name():
                    if re.match(l1_pat, edge.get_attributes()['texlbl']):
                        d[i][j] = int(edge.get_attributes()['texlbl'][1]) * l_A
                    elif re.match(l2_pat, edge.get_attributes()['texlbl']):
                        d[i][j] = int(edge.get_attributes()['texlbl'][1]) * l_B
        d[i][i] = 0 - sum(d[i])
    return d


def kolmogorov(m):
    s = ""
    for i in range(m.shape[0]):
        s = s + "P^\prime_{" + str(i) + "} = "
        for j in range(m.shape[0]):
            if i != j:
                if m[j][i] >= 1:
                    s = s + str(int(m[j][i])) + "P_{" + str(j) + "} (t) +"
                if m[j][i] <= -1:
                    s = s[:-1] + "-" + str(abs(int(m[j][i]))) + "P_{" + str(j) + "} (t) +"
        for j in range(m.shape[0]):
            if i != j:
                if m[i][j] >= 1:
                    s = s[:-1] + "-" + str(abs(int(m[i][j]))) + "P_{" + str(i) + "} (t) +"
                if m[i][j] <= -1:
                    s = s + str(int(m[i][j])) + "P_{" + str(i) + "} (t) +"
        s = s[:-1] + "\\\\ \n"
    s = s[:-4]
    return s


def f(y, t, m):
    res = []
    # print(y)
    # m[-1] = np.ones(m.shape[0])
    for i in range(m.shape[0]):
        a = 0
        for j in range(m.shape[0]):
            if i != j:
                a += m[j][i] * y[j]
        for j in range(m.shape[0]):
            if i != j:
                a -= m[i][j] * y[j]
        res.append(a)
    return res


def kolmogorov_solution(m):
    t = np.linspace(0, 1, 40)  # vector of time
    y0 = [0] * m.shape[0]  # start value
    y0[0] = 1
    # y0[-1] = 1
    w = odeint(f, y0, t, args=(m,))  # solve eq.
    # print(w)
    fig = plt.figure(facecolor='white')
    for i in range(len(w[0]) - 1):
        plt.plot(t, w[:, i])
    plt.ylabel("z")
    plt.xlabel("t")
    plt.grid(True)
    plt.show()


def P(n, t, paths, lambda_A, lambda_B, Na, Nb):
    for path in paths:
        if paths[path][0] == n:
            k = (Na * lambda_A) ** paths[path][1] * (Nb * lambda_B) ** paths[path][2] / factorial(
                paths[path][1]) / factorial(paths[path][2])
            return k * exp(-(Na * lambda_A + Nb * lambda_B) * t) * t ** (paths[path][1] + paths[path][2])


def P_graphs_0(paths, lambda_A, lambda_B, Na, Nb):
    t_step = T / n
    fig5, ax5 = plt.subplots()
    ax5.grid()
    ax5.set_ylabel('P')
    ax5.set_xlabel('t')
    x = [t_step * i for i in range(n)]
    for path in paths:
        if paths[path][0] == 0:
            ax5.plot(x, [P(paths[path][0], t, paths, lambda_A, lambda_B, Na, Nb) for t in x], label='$P_{0}(t)$')
    ax5.legend()
    fig5.savefig('Latex/res/Images/graph_0.png')


def P_graphs(paths, lambda_A, lambda_B, Na, Nb):
    n = 100
    t_step = T / n
    fig1, ax1 = plt.subplots()
    ax1.grid()
    ax1.set_ylabel('P')
    ax1.set_xlabel('t')
    x = [t_step * i for i in range(n)]
    for path in paths:
        if paths[path][0] > 0:
            ax1.plot(x, [P(paths[path][0], t, paths, lambda_A, lambda_B, Na, Nb) for t in x], label='$P_{' + str(paths[path][0]) + '}(t)$')
    ax1.legend()
    fig1.savefig('Latex/res/Images/graph.png')


def reliability(paths, lambda_A, lambda_B, t, Na, Nb):
    y = 0
    if t < 0:
        return None
    l = [0] * 10
    for path in paths:
        if paths[path][0] > 0:
            k = (Na * lambda_A) ** paths[path][1] * (Nb * lambda_B) ** paths[path][2] / factorial(
                paths[path][1]) / factorial(paths[path][2])
            l[paths[path][1] + paths[path][2]] = l[paths[path][1] + paths[path][2]] + k
    i = 9

    while i >= 0:
        if l[i] > 0:
            y = y + l[i] * t ** i
        i = i - 1
    y = y + 1
    return 1 - y * exp(- (Na * lambda_A + Nb * lambda_B) * t)


def reliability_graphs(paths, lambda_A, lambda_B, Na, Nb):
    n = 100
    t_step = T / n
    fig2, ax2 = plt.subplots()
    ax2.grid()
    ax2.set_ylabel('P')
    ax2.set_xlabel('t')
    x = [t_step * i for i in range(n)]
    ax2.plot(x, [1 - reliability(paths, lambda_A, lambda_B, t, Na, Nb) for t in x], label='$R(t)$')
    ax2.legend()
    # fig2.show()
    fig2.savefig('Latex/res/Images/R_t.png')


def my_funcs(paths, lambda_A, lambda_B, t, Na, Nb):
    l = [0] * 10
    y = 0
    for path in paths:
        if paths[path][0] > 0:
            k = (Na * lambda_A) ** paths[path][1] * (Nb * lambda_B) ** paths[path][2] / factorial(paths[path][1]) / factorial(
                paths[path][2])
            l[paths[path][1] + paths[path][2]] = l[paths[path][1] + paths[path][2]] + k
    i = 9

    while i >= 0:
        if l[i] > 0:
            y = y + l[i] * t ** i
        i = i - 1
    y = y + 1

    return y


def r_t(paths, lambda_A, lambda_B, Na, Nb):
    n = 100
    t_step = T / n
    t = sp.Symbol('t')
    e = sp.exp(-(Na * lambda_A + Nb * lambda_B)*t)
    R_t = -e * my_funcs(paths, lambda_A, lambda_B, t, Na, Nb)
    r = R_t.diff(t)

    # строим график плотности распределения
    function_r = sp.sympify(r)
    values = [function_r.subs(t, val) for val in np.arange(0, T, t_step)]
    fig3, ax3 = plt.subplots()
    ax3.grid()
    ax3.plot(np.arange(0, T, t_step), values, color='red', label='r(t)')
    # fig3.show()
    fig3.savefig('Latex/res/Images/r.png')

    # находим матожидание
    mu = -sp.integrate(R_t, (t, 0.0, sp.oo)).evalf()

    return mu


def F_t(l,y):
    return -np.log(1-y)/l


def find_lambda(line):
    flag = True
    for i in range(len(line)):
        if line[i] > 0:
            if flag:
                lb = [i, line[i]]
                flag = False
            else:
                la = [i, line[i]]

    return lb, la


def MD(m):
    current_s = 0
    current_t = 0
    states_tr = [current_s]
    t_tr = [0]

    while np.max(m[current_s]) != 0:  # пока не упали в терминальное
        lb, la = find_lambda(m[current_s])
        t_a = F_t(la[1], np.random.uniform(low=0.0, high=1.0, size=None))
        t_b = F_t(lb[1], np.random.uniform(low=0.0, high=1.0, size=None))
        current_t += min(t_a, t_b)
        current_s = la[0]*(t_a < t_b) + lb[0]*(t_a >= t_b)
        states_tr.append(current_s)
        t_tr.append(current_t)

    return current_t, states_tr, t_tr


def imitational_modeling(m, N):
    fig4, ax4 = plt.subplots()
    plt.yticks(np.arange(0, len(paths), step=1))
    ax4.grid()
    ax4.set_ylabel('$S_n$')
    ax4.set_xlabel('t')
    t_term = []
    for i in range(N):
        term, s_tr, t_tr = MD(m)
        t_term.append(term)
        # расширяем списки для красивой отрисовки
        if i < 16:
            plt.plot(t_tr + [term+(dt*i) for i in range(int((T-term)/dt))], s_tr + [s_tr[-1] for _ in range(int((T-term)/dt))])

    ax4.legend()
    # fig2.show()
    fig4.savefig('Latex/res/Images/term.png')
    return np.mean(t_term), '%.3f' % np.sqrt(N * np.var(t_term) / (N - 1))


def kolm_difs(m):
    t = sp.symbols('t')
    P = sp.Function('P')
    dd = "-12*P - 8*P"
    dd = sp.sympify(dd)
    dd = sp.Eq(sp.diff(P, t), dd)
    print(dd)
    sol = sp.dsolve(dd, P(t))
    print(sol)


if __name__ == "__main__":
    # Initialisation
    l_A = g + (n % 3)
    l_B = g + (n % 5)
    Na = 2 + (g % 2)
    Nb = 2 + (n % 2)
    Ra = 4 + (g % 2)
    Rb = 5 - (g % 2)

    # kolm_difs(1)

    # Creating graph
    graph_dot, paths = graph(Ra - Na, Rb - Nb, Na, Nb)

    # Crating graph picture
    graph_tex = dot2tex.dot2tex(str(graph_dot), texmode="math", figonly=True, figpreamble="label=graph")
    # matrix_np = matrix(l_A, l_B, graph_dot)
    print(matrix_np)
    # matrix = matrix_np.tolist()
    print(matrix)

    # Holmogorov equations
    # kolm_difs(matrix_np)

    # Creating functions graph
    P_graphs(paths, l_A, l_B, Na, Nb)
    P_graphs_0(paths, l_A, l_B, Na, Nb)
    print("... wrote P_graphs.png")

    reliability_graphs(paths, l_A, l_B, Na, Nb)

    mu = r_t(paths, l_A, l_B, Na, Nb)

    # MODELING
    t_term = []
    sr, otkl = imitational_modeling(matrix, N)

    make_latex(var, g, name, name_short, l_A, l_B, Na, Nb, Ra, Rb, graph_tex,
               graph_dot.get_nodes(), matrix_np, kolmogorov(matrix_np), paths, mu, sr, otkl)
