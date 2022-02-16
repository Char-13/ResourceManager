import networkx as nx
import matplotlib.pyplot as plt
import os


def main():
    p = 0
    r = 0
    # h = open('scenarios/scenario-2.txt', 'r')
    path = "scenarios/"
    os.chdir(path)
    fileNo = input("What file # would you like? (1, 2, 3, etc.) \n")
    foundfile = False
    fileCount = 1

    while not foundfile:
        for file in os.listdir():
            if fileCount == int(fileNo):
                foundfile = True
                h = open(file)
                num_lines = 2
                for i in range(num_lines):
                    if i == 0:
                        p = h.readline()
                    if i == 1:
                        r = h.readline()
                build_graph(int(p), int(r), file)
                break
            else:
                fileCount = fileCount + 1
            if fileCount == len(os.listdir()) + 1:
                print('Could not find file, exiting program')
                exit(0)


def build_graph(x, y, file):
    # create Di-Graph and list of nodes to build
    # got all nodes (somewhat) labeled differently. Need to figure out relation
    G = nx.DiGraph()
    proclist = []
    reslist = []
    for i in range(x):
        proclist.append("p{}".format(i))
    G.add_nodes_from(proclist)

    for j in range(y):
        reslist.append("r{}".format(j))
    G.add_nodes_from(reslist)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)

    # list we will use to draw edges
    superList = proclist + reslist

    # edge list to run proper add/remove edge commands
    edgeList = []
    h = open(file)
    f = h.readlines()
    for line in f:
        edgeList.append(line[:-1])
    edgeList.pop(0)
    edgeList.pop(0)
    # filledResources = []
    deadlock = False
    queueList = []

    for i in edgeList:
        for j in i:
            if j == "r":
                edgeExists = False
                # top chunk creates a request edge from the process to the resource.
                # calls my_edge which returns a tuple of p and r node to reference in superlist
                mytuple = (my_edge(i))
                print(superList[mytuple[0]] + ' has requested resource ' + superList[(len(proclist)) + mytuple[1]])
                G.add_edge((superList[mytuple[0]]), superList[(len(proclist)) + mytuple[1]])
                # try-except block that looks for cycle, rather than throwing error catches and prints false
                try:
                    nx.find_cycle(G, source=superList[mytuple[0]], orientation="original")
                    deadlock = True
                    print('Deadlock: ' + str(deadlock))
                except nx.exception.NetworkXNoCycle:
                    print('Deadlock: ' + str(deadlock))
                    deadlock = False
                nx.draw_networkx_nodes(G, pos)
                nx.draw(G, pos)
                plt.pause(2)
                # for loop to check if the resource is allocated to a process
                # if true then dont add the edge and add to queue
                # if false, add the edge as the resource is not allocated
                # probably check for cycles in this chunk of code
                for z in proclist:
                    if G.has_edge(superList[(len(proclist)) + mytuple[1]], z):
                        print('resource already allocated, added to queue')
                        tup = (superList[(len(proclist)) + mytuple[1]], superList[mytuple[0]])
                        queueList.append(tup)
                        edgeExists = True
                # chunk of code that removes the request edge and draws the allocated edge
                if not edgeExists:
                    G.remove_edge((superList[mytuple[0]]), superList[(len(proclist)) + mytuple[1]])
                    plt.clf()
                    nx.draw_networkx_nodes(G, pos)
                    nx.draw_networkx_labels(G, pos)
                    nx.draw(G, pos)
                    print(superList[mytuple[0]] + ' owns resource ' + superList[(len(proclist)) + mytuple[1]])
                    G.add_edge(superList[(len(proclist)) + mytuple[1]], superList[mytuple[0]])
                    nx.draw_networkx_nodes(G, pos)
                    nx.draw(G, pos)
                    plt.pause(2)
            # code that deletes edges that have been freed and allow resources to be re-allocated
            elif j == "f":
                mytuple = (my_edge(i))
                print('Process ' + superList[mytuple[0]] + ' frees resource ' + superList[len(proclist) + mytuple[1]])
                G.remove_edge(superList[(len(proclist)) + mytuple[1]], superList[mytuple[0]])
                # list of process requests that are now allowed to be allocated
                # goes through first item in list and adds the edge and removes the item afterwards
                # breaks out of loop because we only want to use the first item at time of use
                for x in queueList:
                    print('Resource ' + x[0] + ' was freed and reallocated to process ' + x[1] + ' from the queue.')
                    # removes requested edge and adds allocated edge
                    G.remove_edge(x[1], x[0])
                    G.add_edge(x[0], x[1])
                    queueList.pop(0)
                    break
                plt.clf()
                nx.draw_networkx_nodes(G, pos)
                nx.draw_networkx_labels(G, pos)
                nx.draw(G, pos)
                plt.pause(2)


def my_edge(x):
    count = 0
    source = None
    dest = None
    for i in x:
        if i.isdigit() and count == 0:
            source = int(i)
            print(source)
        if i.isdigit() and count == 2:
            dest = int(i)
            print(dest)

        if source is not None:
            count = count + 1
    return source, dest


if __name__ == '__main__':
    main()