from unittest import TestCase
from efficiency.backlog import Backlog
import numpy.testing as npt

class TestBacklog(TestCase):

    def test_start_node(self):
        # requirements can be expressed in duration, effort, man sprints, ideal sprints etc., and can be more than one
        FEATURES = {'start_node': 'begin', 'features': [
            {'id': 'begin',
             'requirements': [0],
             'adj_list': ['A'],
             'benefits': [0, 0],
             },
            {'id': 'A',
             'requirements': [1],
             'adj_list': ['B', 'C'],
             'benefits': [1, 10],
             },
            {'id': 'B',
             'requirements': [1],
             'adj_list': [],
             'benefits': [2, 20],
             },
            {'id': 'C',
             'requirements': [1],
             'adj_list': ['D'],
             'benefits': [3, 30],
             },
            {'id': 'D',
             'requirements': [1],
             'adj_list': [],
             'benefits': [4, 40],
             },
        ]}
        b = Backlog(features=FEATURES)
        self.assertEqual(b.start_node, FEATURES['start_node'])

    def test_get_total_benefits(self):
        # requirements can be expressed in duration, effort, man sprints, ideal sprints etc., and can be more than one
        FEATURES = {'start_node': 'begin', 'features': [
            {'id': 'begin',
             'requirements': [0],
             'adj_list': ['A'],
             'benefits': [0, 0],
             },
            {'id': 'A',
             'requirements': [1],
             'adj_list': ['B', 'C'],
             'benefits': [1, 10],
             },
            {'id': 'B',
             'requirements': [1],
             'adj_list': [],
             'benefits': [2, 20],
             },
            {'id': 'C',
             'requirements': [1],
             'adj_list': ['D'],
             'benefits': [3, 30],
             },
            {'id': 'D',
             'requirements': [1],
             'adj_list': [],
             'benefits': [4, 40],
             },
        ]}
        b = Backlog(features=FEATURES)
        npt.assert_array_equal(b.get_total_benefits(['C', 'D']), [7, 70])

    def test_get_total_requirements(self):
        # requirements can be expressed in duration, effort, man sprints, ideal sprints etc., and can be more than one
        FEATURES = {'start_node': 'begin', 'features': [
            {'id': 'begin',
             'requirements': [0],
             'adj_list': ['A'],
             'benefits': [0, 0],
             },
            {'id': 'A',
             'requirements': [1],
             'adj_list': ['B', 'C'],
             'benefits': [1, 10],
             },
            {'id': 'B',
             'requirements': [1],
             'adj_list': [],
             'benefits': [2, 20],
             },
            {'id': 'C',
             'requirements': [1],
             'adj_list': ['D'],
             'benefits': [3, 30],
             },
            {'id': 'D',
             'requirements': [1],
             'adj_list': [],
             'benefits': [4, 40],
             },
        ]}
        b = Backlog(features=FEATURES)
        npt.assert_array_equal(b.get_total_requirements(['C', 'D']), [2])
