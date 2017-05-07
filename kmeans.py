import csv
import math
import random
import sys

import matplotlib.pyplot as plt
import matplotlib.markers as mks

import importlib
# This wasn't working for some reason
Axes3D = importlib.import_module('mpl_toolkits.mplot3d').Axes3D

TYPES = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']

class Iris(object):

    def __init__(self, row):
        self.sepal_length = float(row[0])
        self.sepal_width = float(row[1])
        self.petal_length = float(row[2])
        self.petal_width = float(row[3])
        self.name = row[4]

    def coords(self):
        return [
            self.sepal_length,
            self.sepal_width,
            self.petal_length,
            self.petal_width
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

def main():
    # Open and parse file
    iris_file = open('iris.csv', 'rb')
    irises = [Iris(i) for i in csv.reader(iris_file)]
    names = [i.name for i in irises]

    # Parameters
    k = 7
    itr = 5

    if len(sys.argv) == 3:
        k = int(sys.argv[1])
        itr = int(sys.argv[2])

    print 'Running k means with k =', k, 'for', itr, 'iterations'

    # Run
    centroids, clusters = k_means(k, itr, irises)

    # Run metrics
    ss = 0
    for i in xrange(len(clusters)):
        ss += ss_total(centroids[i], clusters[i])
    print 'SS Total:', ss

    scores = score(clusters, names)

    for i in xrange(len(clusters)):
        print i, '&',

        avg = 0
        for j in xrange(len(TYPES)):
            print round(scores[j][i], 2), '&',
            avg += scores[j][i] * names.count(TYPES[j]) / len(names)
        print round(avg, 2), '\\\\'

    graph(centroids, clusters, irises)

def graph(centroids, clusters, all_data):

    slmax = max(i.sepal_length for i in all_data)
    swmax = max(i.sepal_width for i in all_data)
    plmax = max(i.petal_length for i in all_data)
    pwmax = max(i.petal_width for i in all_data)

    xmark = mks.MarkerStyle('x')

    fig1 = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig1, elev=-150, azim=110)
    for i in xrange(len(clusters)):
        color = ['r', 'g', 'b'][i]

        for j in xrange(len(clusters[i])):
            x = clusters[i][j].sepal_length
            y = clusters[i][j].sepal_width
            z = clusters[i][j].petal_length
            name = clusters[i][j].name

            marker = mks.MarkerStyle(['o', '^', 's'][TYPES.index(name)], 'none')
            ax.scatter(x, y, z, c = color, marker = marker)

        c = centroids[i]
        ax.scatter(c[0], c[1], c[2], color = 'k', marker = xmark)

    ax.set_title("Sepal Length vs Sepal Width vs Petal Length")
    ax.set_xlabel("Sepal Length")
    ax.set_xlim(slmax, 0)
    ax.set_ylabel("Sepal Width")
    ax.set_ylim(0, swmax)
    ax.set_zlabel("Petal Length")
    ax.set_zlim(plmax, 0)

    fig2 = plt.figure(2, figsize=(8, 6))
    ax = Axes3D(fig2, elev=-150, azim=110)
    for i in xrange(len(clusters)):
        color = ['r', 'g', 'b'][i]
        for j in xrange(len(clusters[i])):
            x = clusters[i][j].sepal_length
            y = clusters[i][j].sepal_width
            z = clusters[i][j].petal_width
            name = clusters[i][j].name

            marker = mks.MarkerStyle(['o', '^', 's'][TYPES.index(name)])
            ax.scatter(x, y, z, c = color, marker = marker)

        c = centroids[i]
        ax.scatter(c[0], c[1], c[3], color = 'k', marker = xmark)

    ax.set_title("Sepal Length vs Sepal Width vs Petal Length")
    ax.set_xlabel("Sepal Length")
    ax.set_xlim(slmax, 0)
    ax.set_ylabel("Sepal Width")
    ax.set_ylim(0, swmax)
    ax.set_zlabel("Petal Width")
    ax.set_zlim(pwmax, 0)

    fig3 = plt.figure(3, figsize=(8, 6))
    ax = Axes3D(fig3, elev=-150, azim=110)
    for i in xrange(len(clusters)):
        color = ['r', 'g', 'b'][i]
        for j in xrange(len(clusters[i])):
            x = clusters[i][j].sepal_length
            y = clusters[i][j].petal_length
            z = clusters[i][j].petal_width
            name = clusters[i][j].name

            marker = mks.MarkerStyle(['o', '^', 's'][TYPES.index(name)])
            ax.scatter(x, y, z, c = color, marker = marker)

        c = centroids[i]
        ax.scatter(c[0], c[2], c[3], color = 'k', marker = xmark)

    ax.set_title("Sepal Length vs Sepal Width vs Petal Length")
    ax.set_xlabel("Sepal Length")
    ax.set_xlim(slmax, 0)
    ax.set_ylabel("Petal Length")
    ax.set_ylim(0, plmax)
    ax.set_zlabel("Petal Width")
    ax.set_zlim(pwmax, 0)

    fig4 = plt.figure(4, figsize=(8, 6))
    ax = Axes3D(fig4, elev=-150, azim=110)
    for i in xrange(len(clusters)):
        color = ['r', 'g', 'b'][i]
        for j in xrange(len(clusters[i])):
            x = clusters[i][j].sepal_width
            y = clusters[i][j].petal_length
            z = clusters[i][j].petal_width
            name = clusters[i][j].name

            marker = mks.MarkerStyle(['o', '^', 's'][TYPES.index(name)])
            ax.scatter(x, y, z, c = color, marker = marker)

        c = centroids[i]
        ax.scatter(c[1], c[2], c[3], color = 'k', marker = xmark)

    ax.set_title("Sepal Length vs Sepal Width vs Petal Length")
    ax.set_xlabel("Sepal Width")
    ax.set_xlim(swmax, 0)
    ax.set_ylabel("Petal Length")
    ax.set_ylim(0, plmax)
    ax.set_zlabel("Petal Width")
    ax.set_zlim(pwmax, 0)

    plt.show()

def k_means(k, itr, irises):
    # Create random clusters
    centroids = [random.choice(irises).coords() for _ in range(k)]

    # Iterate iter times
    for ii in xrange(itr):

        # Divide irises into clusters
        clusters = cluster(centroids, irises)

        for i in xrange(k):
            centroids[i] = [0, 0, 0, 0]

            # Add up all coords in cluster
            for j in xrange(len(clusters[i])):
                coords = clusters[i][j].coords()
                centroids[i][0] += coords[0]
                centroids[i][1] += coords[1]
                centroids[i][2] += coords[2]
                centroids[i][3] += coords[3]

            # Test for empty cluster
            if len(clusters[i]) == 0:
                continue

            # Average out coords
            centroids[i][0] = centroids[i][0] / len(clusters[i])
            centroids[i][1] = centroids[i][1] / len(clusters[i])
            centroids[i][2] = centroids[i][2] / len(clusters[i])
            centroids[i][3] = centroids[i][3] / len(clusters[i])

    # Make final clusters
    clusters = cluster(centroids, irises)
    return centroids, clusters

def cluster(centroids, irises):
    # Create a new cluster for each centroid
    clusters = [[] for _ in range(len(centroids))]

    for i in irises:
        # Fit data into clusters, solving ties randomly
        dists = [distance(i.coords(), c) for c in centroids]
        mins = [ii for ii, x in enumerate(dists) if x == min(dists)]
        clusters[random.choice(mins)].append(i)

    return clusters

def distance(a, b):
    sum = 0
    for i in xrange(len(a)):
        sum += (a[i] - b[i]) ** 2
    # Don't sqrt because no information is gained
    return sum

def ss_total(centroid, irises):
    sum = 0
    for i in irises:
        sum += distance(centroid, i.coords())
    return sum

def score(clusters, all_names):
    f1s = [[], [], []]

    corrects = find_corrects(clusters)
    for i in xrange(len(corrects)):
        correct_names = [iris.name for iris in corrects[i]]
        correct_count = float(correct_names.count(TYPES[i]))

        for c in clusters:
            recall = correct_count / all_names.count(TYPES[i])
            precision = correct_count / len(c)
            f1s[i].append(2 * precision * recall / (precision + recall))

    return f1s

def find_corrects(clusters):
    counts = [[], [], []]

    # Get count of each type in cluster
    for c in clusters:
        names = [i.name for i in c]
        counts[0].append(names.count(TYPES[0]))
        counts[1].append(names.count(TYPES[1]))
        counts[2].append(names.count(TYPES[2]))

    # Find the ones with the largest amount of each type
    correct_indexes = []
    for c in counts:
        maxes = [i for i, x in enumerate(c) if x == max(c)]
        correct_indexes.append(random.choice(maxes))

    if len(set(correct_indexes)) != 3:
        # One set was chosen as the correct one for two types
        # Print warning to see if this even needs to be handled
        print 'One set is correct for two types! Handle this!'

    return [clusters[i] for i in correct_indexes]

def cluster_sort_key(cluster, name):
    correct = float([iris.name for iris in cluster].count(name))
    return correct / len(cluster)

if __name__ == '__main__':
    main()
