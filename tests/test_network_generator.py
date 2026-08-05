from src.network.network_generator import generate_network


print("Random Network")
g1 = generate_network(
    "random",
    20,
    {"p": 0.3}
)

print(
    g1.number_of_nodes(),
    g1.number_of_edges()
)

print()

print("Small World Network")
g2 = generate_network(
    "small_world",
    20,
    {
        "k": 4,
        "p": 0.2
    }
)

print(
    g2.number_of_nodes(),
    g2.number_of_edges()
)