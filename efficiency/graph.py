import networkx as nx


class GraphHelper:
    def __init__(self, edges):
        G = nx.DiGraph()
        G.add_edges_from(edges)
        if nx.is_directed_acyclic_graph(G):
            self.__graph = G
        else:
            raise Exception('The graph is not a DAG')
            # TODO: Pinpoint what are the nodes/edges that cause the graph not to be a DAG

    def _get_node_successors(self, node):
        return self.__graph.successors(node)

    def _get_node_predecessors(self, node):
        return self.__graph.predecessors(node)

    # def _remove_not_ready_candidate_nodes1(self, path, candidate_nodes):
    #     # Remove from candidate_nodes the ones that don't have all predecessors in the path
    #     not_ready = set()
    #     for n in candidate_nodes:
    #         predecessors = set(self._get_node_predecessors(n))
    #         not_ready = not_ready.union(predecessors.difference(path))
    #     #print('-----------------------==== returning', candidate_nodes.intersection(not_ready))
    #     return candidate_nodes.intersection(not_ready)

    def _remove_not_ready_candidate_nodes(self, path, candidate_nodes):
        # TODO: Find out if there is a more efficient way of doing what follows? See the previous method.
        # Remove from candidate_nodes the ones that don't have all predecessors in the path
        for n in candidate_nodes:
            predecessors = self._get_node_predecessors(n)
            for p in predecessors:
                if p not in path:  # p
                    candidate_nodes = candidate_nodes.copy() - set(n)
                    print('----------------------- removing node', n, 'from the candidate nodes')
        return candidate_nodes
        #  A - B
        #    \   \
        #      C - D
        # ABC pre    BC
        # AC path    ABC
        # BD candi   D

    def get_candidate_nodes(self, path):
        nodes = set()
        for node in path:
            nodes = nodes.union(set(self._get_node_successors(node)))
        nodes = nodes.difference(path)  # remove the ones already in path
        nodes = self._remove_not_ready_candidate_nodes(path, nodes.copy())
        return nodes