from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx
import folium
from folium.plugins import AntPath
import requests
import math
import time
def load_data_from_txt(filepath):
    coordinates = []
    demands = []

    num_vehicles = None
    capacity = None

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            # ler configurações
            if line.startswith("#"):
                parts = line.replace("#", "").split()

                if parts[0] == "vehicles":
                    num_vehicles = int(parts[1])

                elif parts[0] == "capacity":
                    capacity = int(parts[1])

                continue

            # ler nós
            parts = line.split()

            node_id = int(parts[0])
            lat = float(parts[1])
            lon = float(parts[2])
            demand = int(parts[3])

            coordinates.append((lat, lon))
            demands.append(demand)

    return coordinates, demands, num_vehicles, capacity

def haversine_distance(coord1, coord2):
    """
    Calcula a distância entre dois pontos geográficos
    utilizando a fórmula de Haversine.

    Retorna a distância em metros.
    """

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371000  # raio médio da Terra em metros

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(lat1) *
        math.cos(lat2) *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return int(R * c)

def create_distance_matrix_from_coords(coords):
    size = len(coords)
    matrix = []

    for i in range(size):
        row = []

        for j in range(size):
            if i == j:
                row.append(0)
            else:
                row.append(
                    haversine_distance(
                        coords[i],
                        coords[j]
                    )
                )

        matrix.append(row)

    return matrix
def get_real_route(coords):
    base_url = "http://router.project-osrm.org/route/v1/driving/"

    # OSRM usa lon,lat (invertido)
    coord_str = ";".join([f"{lon},{lat}" for lat, lon in coords])

    url = f"{base_url}{coord_str}?overview=full&geometries=geojson"

    response = requests.get(url)
    data = response.json()

    route = data["routes"][0]["geometry"]["coordinates"]

    # converter de volta para (lat, lon)
    return [(lat, lon) for lon, lat in route]

# All data model is using dummy data, but most of it should be hard-coded for performance
def create_data_model():
    data = {}

    # carregar dados do arquivo
    coords, demands, num_vehicles, capacity = load_data_from_txt("dados3.txt")

    data["coordinates"] = coords
    data["demands"] = demands

    # gerar matriz de distância a partir das coordenadas
    data["distance_matrix"] = create_distance_matrix_from_coords(coords)

    # valores padrão (caso não estejam no txt)
    if num_vehicles is None:
        num_vehicles = 5

    if capacity is None:
        capacity = 15

    data["num_vehicles"] = num_vehicles
    data["vehicle_capacities"] = [capacity] * num_vehicles
    data["depot"] = 0

    return data

def get_real_route_segmented(coords):
    full_path = []

    for i in range(len(coords) - 1):
        segment = get_real_route([coords[i], coords[i+1]])
        full_path.extend(segment)

    return full_path

def plot_real_routes_map(data, routes):
    coords = data["coordinates"]

    # Criar mapa
    m = folium.Map(location=coords[0], zoom_start=13)

    colors = ["red", "blue", "green", "purple", "orange"]

    for i, route in enumerate(routes):
        color = colors[i % len(colors)]

        route_coords = [coords[node] for node in route]

        try:
            real_path = get_real_route_segmented(route_coords)

            popup = folium.Popup(
                f"Caminhão {i + 1}: {' → '.join(map(str, route))}",
                max_width=300
            )
            tooltip = folium.Tooltip(
                f"Caminhão {i + 1}: {' → '.join(map(str, route))}"
            )

            ant_path = AntPath(
                locations=real_path,
                color=color,
                weight=5,
                opacity=0.8,
                delay=2500,
            )

            ant_path.add_child(tooltip)
            ant_path.add_child(popup)
            ant_path.add_to(m)

        except Exception as e:
            print(f"Erro real: {e}")

        #  Marcadores com Ordem da rota
        for stop_index, node in enumerate(route):
            if node == data["depot"]:
                # Depósito
                folium.Marker(
                    location=coords[node],
                    popup="Depósito (0)",
                    icon=folium.Icon(color="black", icon="home")
                ).add_to(m)

            else:
                folium.Marker(
                    location=coords[node],
                    popup=f"Nó {node}",
                    icon=folium.DivIcon(
                        html=f"""
                        <div style="
                            font-size: 12px;
                            color: white;
                            background-color: {color};
                            border-radius: 50%;
                            width: 20px;
                            height: 20px;
                            text-align: center;
                            line-height: 20px;
                        ">
                            {node}
                        </div>
                        """
                    )
                ).add_to(m)

   # Legenda
    legend_html = """
    <div style="
    position: fixed; 
    bottom: 50px; left: 50px; width: 200px; height: auto; 
    background-color: white; 
    border:2px solid grey; z-index:9999; 
    font-size:14px;
    padding: 10px;
    ">
    <b>Legenda</b><br>
    """

    for i in range(len(routes)):
        color = colors[i % len(colors)]
        legend_html += f"""
        <i style="background:{color};width:10px;height:10px;display:inline-block;"></i>
        Caminhão {i+1}<br>
        """

    legend_html += "</div>"

    m.get_root().html.add_child(folium.Element(legend_html))

    # Salvar e abrir
    m.save("mapa_real.html")
    webbrowser.open("mapa_real.html")

def get_routes(data, manager, routing, assignment):
    routes = []

    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(assignment, vehicle_id):
            continue

        index = routing.Start(vehicle_id)
        route = []

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            index = assignment.Value(routing.NextVar(index))

        route.append(manager.IndexToNode(index))
        routes.append(route)

    return routes

def plot_routes(data, routes):
    G = nx.DiGraph()
    coords = data["coordinates"]

    for i, (x, y) in enumerate(coords):
        G.add_node(i, pos=(x, y))

    pos = nx.get_node_attributes(G, 'pos')

    plt.figure(figsize=(10, 8))

    colors = ["red", "blue", "green", "purple", "orange", "brown"]
    legend_elements = []

    for i, route in enumerate(routes):
        color = colors[i % len(colors)]


        edges = [(route[j], route[j+1]) for j in range(len(route)-1)]

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edges,
            edge_color=color,
            width=2,
            arrows=True,
            arrowstyle='-|>',
            arrowsize=20
        )

        legend_elements.append(
            Line2D([0], [0], color=color, lw=2, label=f'Caminhão {i+1}')
        )

    # Nós
    nx.draw_networkx_nodes(G, pos, node_size=300)
    nx.draw_networkx_labels(G, pos)

    # Destacar depósito
    nx.draw_networkx_nodes(G, pos, nodelist=[0], node_color='yellow', node_size=500)

    plt.legend(handles=legend_elements)
    plt.title("Rotas dos Caminhões (CVRP - Direcionado)")
    plt.show()

def preprocess_data(data):
    max_capacity = max(data["vehicle_capacities"])

    valid_nodes = []

    # Always keep depot on nodes
    valid_nodes.append(0)

    # Filtrar nós válidos
    for i in range(1, len(data["demands"])):
        if data["demands"][i] <= max_capacity:
            valid_nodes.append(i)
        else:
            print(f"Removendo nó {i} (demanda {data['demands'][i]} > capacidade máxima)")

    # Filtered distance matrix
    new_matrix = []
    for i in valid_nodes:
        row = []
        for j in valid_nodes:
            row.append(data["distance_matrix"][i][j])
        new_matrix.append(row)

    # Create new demands
    new_demands = [data["demands"][i] for i in valid_nodes]

    # Update data
    data["distance_matrix"] = new_matrix
    data["demands"] = new_demands

    return data

def print_solution(data, manager, routing, assignment):
    # Prints assignment on console.
    print(f"Objective: {assignment.ObjectiveValue()}\n")
    # Display dropped nodes.
    dropped_nodes = "Dropped nodes:"
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if assignment.Value(routing.NextVar(node)) == node:
            dropped_nodes += f" {manager.IndexToNode(node)}"
    print(dropped_nodes)
    print("\n")
    # Display routes
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(assignment, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        plan_output = f"Route for truck {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"Total Distance of all routes: {total_distance}m")
    print(f"Total Load of all routes: {total_load}")


def main():
    # Solve the CVRP problem.
    # Instantiate the data problem.
    data = create_data_model()

    data = preprocess_data(data)
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        # Returns the distance between the two nodes.
        # Convert from routing variable Index to distance matrix Node Index.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        # Returns the demand of the node.
        # Convert from routing variable Index to demands Node Index.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )
    # Allow to drop nodes.
    penalty = sum(max(row) for row in data["distance_matrix"])
    # penalty = max(data["distance_matrix"] * 10)
    for node in range(len(data["distance_matrix"])):
        if node == data["depot"]:
            continue
        routing.AddDisjunction([node], penalty)

    # Setting first solution heuristic. I am using the cheapest path metric as a baseline
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.SAVINGS
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.guided_local_search_lambda_coefficient = 0.1

    search_parameters.time_limit.FromSeconds(20) # set time limit to 20 seconds

    # Solve the problem.
    inicio = time.time()
    assignment = routing.SolveWithParameters(search_parameters)



    # Print solution on console.
    if assignment:
        print_solution(data, manager, routing, assignment)
        # gerar e plotar rotas
        routes = get_routes(data, manager, routing, assignment)
        plot_routes(data, routes)
        plot_real_routes_map(data, routes)  # Grafo geográfico real
    fim_total = time.time()
    print(f"Execution time: {fim_total - inicio:.4f} s")
if __name__ == "__main__":
    main()
