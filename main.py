import sys

def split(input):
    sections = input.split()
    country = [list(map(int, row)) for row in sections[0].split(',')] # country inputs
    build = [list(map(cost_converter, row)) for row in sections[1].split(',')] # built inputs
    destroy = [list(map(cost_converter, row)) for row in sections[2].split(',')] # destroy inputs
    return country, build, destroy

def cost_converter(letter): # change letter to cost value
    if 'A' <= letter <= 'Z':
        return ord(letter) - ord('A') # ASCII minus A ASCII 
    elif 'a' <= letter <= 'z':
        return ord(letter) - ord('a') + 26 # ASCII minus a ASCII plus alphabet count

def construction(country, build, destroy): # design, build and remove roads
    # variable initialisation 
    cities = len(country)
    visited = [False] * cities
    connections = []
    total_cost = 0

    def search(city, connection): # find all connections from city
        visited[city] = True
        connection.append(city)
        for neighbouring in range(cities): # check neighbouring cities
            if country[city][neighbouring] == 1 and not visited[neighbouring]:
                search(neighbouring, connection)
        
    def find(path): # find the path between cities
        if component[path] != path:
            component[path] = find(component[path])
        return component[path]
    
    def union(path1, path2): # link the cities together
        root1 = find(path1)
        root2 = find(path2)
        if root1 != root2: # if different combine
            component[root2] = root1

    for city in range(cities): # search the cities for connections
        if not visited[city]:
            connection = []
            search(city, connection)
            connections.append(connection) # add connection

    for connection in connections: # investigate the conncetions
        num_connections = len(connection)
        if num_connections <= 1: # no connections
            continue
        
        roads = 0
        cost_destroy = []
        
        # calculate destory cost
        for i in range(num_connections): 
            for j in range(i + 1, num_connections):
                if country[connection[i]][connection[j]] == 1:
                    roads += 1
                    cost_destroy.append(destroy[connection[i]][connection[j]])
        
        extra_roads = roads - (num_connections - 1) 
        if extra_roads > 0: # remove cheapest extra roads
            cost_destroy.sort()
            total_cost += sum(cost_destroy[:extra_roads])

    num_links = len(connections)
    cost_build = []

    # calculate build cost
    for i in range(num_links): 
        for j in range(i + 1, num_links):
            min_build = float('inf')
            for c1 in connections[i]:   
                for c2 in connections[j]:
                    min_build = min(min_build, build[c1][c2])
            cost_build.append((min_build, i, j))
    
    cost_build.sort()   
    component = list(range(num_links))
            
    for cost, city1, city2 in cost_build: # add cheaper build
        if find(city1) != find(city2):
            total_cost += cost
            union(city1, city2)

    return total_cost # return min cost

if __name__ == "__main__":
    input = sys.stdin.read().strip()  # Read input
    country, build, destroy = split(input) # split input
    minimal_cost = construction(country, build, destroy) # get cost
    print(minimal_cost) # print cost