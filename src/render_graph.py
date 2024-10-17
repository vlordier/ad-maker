# render_graph.py
import logging
from graphviz import Digraph
from main_graph import MainGraph
from state_schemas import MainState

logging.basicConfig(level=logging.INFO)

def render_graph():
    # Create a new instance of MainGraph
    runner = MainGraph()

    # Create a directed graph using Graphviz
    dot = Digraph(comment='Ad Storyboard Design Flow')
    dot.attr(size='10,10')

    # Traverse the nodes and edges in the graph and add them to Graphviz
    for node_name in runner.graph.nodes:
        dot.node(node_name, node_name)  # Add the node to the graph

    # LangGraph might store edges differently, let's iterate the graph edges
    try:
        for from_node, to_nodes in runner.graph.edges:
            # This handles if edges are a set of tuples
            dot.edge(from_node, to_nodes)
    except TypeError:
        # If the edges are something else, adjust as necessary
        logging.error("Unexpected edge format. Please inspect your graph structure.")
        return

    # Generate the graph as a PNG
    output_file = 'ad_storyboard_graph'
    dot.render(output_file, format='png')  # This will generate a PNG image

    logging.info(f"Graph rendered and saved as {output_file}.png")

if __name__ == "__main__":
    render_graph()
