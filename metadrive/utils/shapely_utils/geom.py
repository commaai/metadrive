import heapq
from typing import Union
from metadrive.utils.math import norm
from itertools import combinations


def cut_polygon_along_parallel_edges(polygon):
    """
    (Deprecated) Given a polygon, cut it into several slices. This is for creating the crosswalk.
    Args:
        polygon: a list of 2D points,

    Returns: polygon pieces, which forms the original polygon after being combined.

    """
    raise DeprecationWarning("Stop using this. Not robust enough")


def calculate_slope(p1, p2):
    """
    Calculate the slope of a line segment.
    Args:
        p1: point 1
        p2: point 2

    Returns:

    """
    # Handle the case of a vertical line segment
    if p1[0] == p2[0]:
        return float('inf')
    else:
        return (p2[1] - p1[1]) / (p2[0] - p1[0])


def length(edge):
    """
    Return the length of an edge
    Args:
        edge: edge, two points

    Returns:

    """
    p_1 = edge[0]
    p_2 = edge[1]
    return norm(p_1[0] - p_2[0], p_1[1] - p_2[1])


def size(edge):
    """
    The size of the edge
    Args:
        edge: two points defining an edge

    Returns: length^2 of a vector

    """
    p_1 = edge[0]
    p_2 = edge[1]
    x = p_1[0] - p_2[0]
    y = p_1[1] - p_2[1]
    return x**2 + y**2


def find_longest_parallel_edges(polygon: Union[list, object]):
    """
    Find and return the longest parallel edges of a polygon. If it can not find, return the longest two edges instead.
    Args:
        polygon: object with .exterior.coords attribute, or list of 2D points representing a polygon

    Returns:

    """

    edges = []
    longest_parallel_edges = None
    coords = list(polygon.exterior.coords) if hasattr(polygon, 'exterior') else polygon

    # Extract the edges from the polygon
    for i in range(len(coords) - 1):
        edge = (coords[i], coords[i + 1])
        edges.append(edge)
    edges.append((coords[-1], coords[0]))

    # Compare each edge with every other edge
    for edge1, edge2 in combinations(edges, 2):
        slope1 = calculate_slope(*edge1)
        slope2 = calculate_slope(*edge2)

        # Check if the slopes are equal (or both are vertical)
        if abs(slope1 - slope2) < 0.5:
            max_len = max(length(edge1), length(edge2))
            if longest_parallel_edges is None or max_len > longest_parallel_edges[-1]:
                longest_parallel_edges = ((edge1, edge2), max_len)

    if longest_parallel_edges:
        return longest_parallel_edges[0]
    else:
        # return sorted(edges, key=lambda edge: size(edge))[-2:]
        return heapq.nlargest(2, edges, key=lambda edge: size(edge))


def find_longest_edge(polygon: Union[list, object]):
    """
    Return the longest edge of a polygon
    Args:
        polygon: object with .exterior.coords attribute, or list of 2D points representing a polygon

    Returns: the longest edge

    """
    coords = list(polygon.exterior.coords) if hasattr(polygon, 'exterior') else polygon
    edges = []
    # Extract the edges from the polygon
    for i in range(len(coords) - 1):
        edge = (coords[i], coords[i + 1])
        edges.append(edge)
    edges.append((coords[-1], coords[0]))
    return heapq.nlargest(1, edges, key=lambda edge: size(edge))
