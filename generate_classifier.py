import matplotlib.pyplot as plt

y_good_roads = [0.074, 0.109]
x_good_roads = [2, 2]

y_bad_roads = [0.598, 0.384]
x_bad_roads = [1, 1]

x_line = range(1, 3)
y_line = [0.275 for _ in range(1, 3)]

plt.scatter(x_good_roads, y_good_roads, c="blue", label="pistas boas")
plt.scatter(x_bad_roads, y_bad_roads, c="red", label="pistas Ruins")
plt.plot(x_line, y_line, c="purple")

plt.xlabel("Classificação das vias: 1-> ruim e 2-> boa")
plt.ylabel("Variância")
plt.legend()

plt.show()
