"""File for visualizing the binary trees used."""
import pydot
from IPython.display import Image, display
from classes import *
from main import *


def tree_to_svg(G: pydot.Dot, tree: Expr, visited_names: set, identifier: int) -> None:
    """Takes in a directed graph and a binary tree, adds the nodes and edges
    of the binary tree to the graphviz directed graph object.

    visited_names keeps track of the names (identifiers) of the nodes already used, to make sure the nodes'
    names are not duplicated. Note that the names for the node objects are merely unique identifiers; they are not
    actually displayed on the graph.

    Preconditions:
        - identifier not in visited_names
        - all(isinstance(element, str) for element in visited_names)
        - all elements in visited_names are strings of natural numbers
    """
    visited_names.add(identifier)

    # new_identifier will be the name of the child nodes
    new_identifier = identifier + 1
    while new_identifier in visited_names:
        new_identifier += 1
    visited_names.add(new_identifier)
    root_name = str(identifier)

    node = None

    # Add the root to dot
    if isinstance(tree, Plus):
        node = pydot.Node(name=root_name, label='+')
    elif isinstance(tree, Multiply):
        node = pydot.Node(name=root_name, label='*')
    elif isinstance(tree, Const):
        node = pydot.Node(name=root_name, label=str(tree.name))
    elif isinstance(tree, Pow):
        node = pydot.Node(name=root_name, label='^')
    elif isinstance(tree, Var):
        node = pydot.Node(name=root_name, label=tree.name)
    elif isinstance(tree, Trig):
        node = pydot.Node(name=root_name, label=tree.name)
    elif isinstance(tree, Log):
        node = pydot.Node(name=root_name, label='ln' if str(tree.base.name) == 'e' else 'log ' + str(tree.base.name))
    G.add_node(node)

    if isinstance(tree, Plus) or isinstance(tree, Multiply):
        # Recurse into the left subtree
        tree_to_svg(G, tree.left, visited_names, new_identifier)
        edge = pydot.Edge(root_name, str(new_identifier))
        G.add_edge(edge)

        # Refresh new_identifier
        while new_identifier in visited_names:
            new_identifier += 1

        # Recurse into the right subtree
        tree_to_svg(G, tree.right, visited_names, new_identifier)
        edge = pydot.Edge(root_name, str(new_identifier))
        G.add_edge(edge)

    if isinstance(tree, Pow):
        # Recurse into the base
        tree_to_svg(G, tree.left, visited_names, new_identifier)
        edge = pydot.Edge(root_name, str(new_identifier))
        G.add_edge(edge)

        # Refresh new_identifier
        while new_identifier in visited_names:
            new_identifier += 1

        # Recurse into the exponent
        tree_to_svg(G, tree.right, visited_names, new_identifier)
        edge = pydot.Edge(root_name, str(new_identifier))
        G.add_edge(edge)

    if isinstance(tree, Trig):
        # Recurse into the parameter
        tree_to_svg(G, tree.arg, visited_names, new_identifier)
        edge = pydot.Edge(root_name, str(new_identifier))
        G.add_edge(edge)

    if isinstance(tree, Log):
        # Recurse into the parameter
        tree_to_svg(G, tree.arg, visited_names, new_identifier)
        edge = pydot.Edge(root_name, str(new_identifier))
        G.add_edge(edge)


def visualization_runner(tree: Expr) -> None:
    """The runner function.
    """
    G = pydot.Dot(graph_type="digraph")
    G.size = "7.75,10.25"

    # Example tree below
    # tree = Multiply(Trig('sin', Var('x')), Power(Trig('cos', Var('x')), Num(-1))).differentiate('x')

    tree_to_svg(G, tree, set(), 0)

    im = Image(G.create_svg())

    display(im)

    G.write_svg('graph.svg')
