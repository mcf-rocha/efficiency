from unittest import TestCase
from efficiency.dea import DEA
import numpy.testing as npt


class TestDEA(TestCase):

    def test_run_using_set_dmu_variables(self):
        dea = DEA()
        DMU_INPUTS = {
            '1': {'1': 20},
            '2': {'1': 40},
            '3': {'1': 40},
            '4': {'1': 60},
            '5': {'1': 70},
            '6': {'1': 50},
        }
        DMU_OUTPUTS = {
            '1': {'1': 20},
            '2': {'1': 30},
            '3': {'1': 50},
            '4': {'1': 40},
            '5': {'1': 60},
            '6': {'1': 20},
        }
        dea.set_dmu_variables(DMU_INPUTS, DMU_OUTPUTS)
        result = dea.run()
        for dmu_key, dmu_value in result.items():
            if dmu_key in ['dmu1','dmu3','dmu5']:
                self.assertEqual(1,dmu_value)

    def test_run_using_set_io(self):
        io = {
                0: {'pevs': 'A', 'inputs': [20], 'outputs': [20]},
                1: {'pevs': 'B', 'inputs': [40], 'outputs': [30]},
                2: {'pevs': 'C', 'inputs': [40], 'outputs': [50]},
                3: {'pevs': 'D', 'inputs': [60], 'outputs': [40]},
                4: {'pevs': 'E', 'inputs': [70], 'outputs': [60]},
                5: {'pevs': 'F', 'inputs': [50], 'outputs': [20]}
        }
        dea = DEA()
        dea.set_io(io)
        r = dea.run()
        print(r)
        npt.assert_equal(r, {'0': 1.0,
                             '1': 0.5999999880000002,
                             '2': 1.0,
                             '3': 0.7058823363321803,
                             '4': 1.0,
                             '5': 0.37499999531250006
                             })
