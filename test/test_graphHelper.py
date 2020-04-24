from unittest import TestCase
from efficiency.graph import GraphHelper
from efficiency.backlog import Backlog
import networkx as nx


class TestGraphHelper(TestCase):
    def test__remove_not_ready_candidate_nodes(self):
        FEATURES = {'start_node': 'begin', 'features': [
            {'id': 'begin',
             'requirements': [0],
             'adj_list': ['A'],
             },
            {'id': 'A',
             'requirements': [1],
             'adj_list': ['B', 'C'],
             },
            {'id': 'B',
             'requirements': [100000],
             'adj_list': ['D'],
             },
            {'id': 'C',
             'requirements': [1],
             'adj_list': ['D'],
             },
            {'id': 'D',
             'requirements': [1],
             'adj_list': [],
             },
        ]}
        #  A - B*
        #    \   \
        #      C - D
        p = Backlog(features=FEATURES)
        gh = GraphHelper(p.features_adjacent_list)
        nodes = gh._remove_not_ready_candidate_nodes({'begin','A','C'},{'D','B'})
        self.assertEqual(nodes,{'B'},msg='nodes={0}'.format(nodes))

    def test_get_next_candidate_nodes_of_a_path(self):
        FEATURES = {'start_node': 'begin', 'features': [
            {'id': 'begin',
             'requirements': [0],
             'adj_list': ['A'],
             },
            {'id': 'A',
             'requirements': [1],
             'adj_list': ['B', 'C'],
             },
            {'id': 'B',
             'requirements': [100000],
             'adj_list': ['D'],
             },
            {'id': 'C',
             'requirements': [1],
             'adj_list': ['D'],
             },
            {'id': 'D',
             'requirements': [1],
             'adj_list': [],
             },
        ]}
        #  A - B*
        #    \   \
        #      C - D
        p = Backlog(features=FEATURES)
        gh = GraphHelper(p.features_adjacent_list)
        nodes = gh.get_candidate_nodes({'begin', 'A', 'C'})
        self.assertEqual(nodes, {'B'}, msg='nodes={0}'.format(nodes))
