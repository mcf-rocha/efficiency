from efficiency.backlog import Backlog
from efficiency.graph import GraphHelper
from efficiency.dea import DEA
import numpy as np
import logging


class Iplan:
    def __init__(self, features, cycle_restrictions=[]):
        self.__backlog = Backlog(features=features)
        self.__graph_helper = GraphHelper(self.__backlog.features_adjacent_list)
        self.__cycle_restrictions = cycle_restrictions

    @property
    def backlog(self):
        return self.__backlog

    def __is_a_valid_release_plan(self, plan):
        # print('-------------- checking if plan requirements ', self.__backlog.get_total_requirements(plan),
        #      'comply with cycle restrictions', self.__cycle_restrictions)
        return all(np.less_equal(self.__backlog.get_total_requirements(plan), self.__cycle_restrictions))

    def __get_next_candidate_nodes(self, plan):
        return self.__graph_helper.get_candidate_nodes(plan)

    def __generate_pevs_next_cycle(self, existing_pevs=None):
        final_plans = []
        if existing_pevs is None:
            candidate_plans = [[self.__backlog.start_node]]
        else:
            candidate_plans = existing_pevs.copy()
        while len(candidate_plans) > 0:
            # logging.debug(' candidate plans', candidate_plans)
            a_plan = candidate_plans.pop()
            logging.info(f'--- analysing plan {a_plan} (this plan was poped from candidate_plans)')
            next_nodes = self.__get_next_candidate_nodes(a_plan)
            # logging.debug('------ candidate nodes', next_nodes)
            if len(next_nodes) > 0:
                new_plan_generated_a_candidate = False
                for n in next_nodes:
                    new_plan = a_plan.copy()
                    new_plan.append(n)
                    # logging.debug('--------- new plan to consider', new_plan)
                    if self.__is_a_valid_release_plan(new_plan):
                        # logging.debug('------------ it was added to candidates')
                        candidate_plans.append(new_plan)
                        new_plan_generated_a_candidate = True
                    else:
                        # logging.debug('------------ not added to candidates')
                        pass
                if not new_plan_generated_a_candidate:  # a_plan not in final_plans:
                    # logging.debug('---- the analysed one was considered final')
                    final_plans.insert(0, a_plan)
            else:
                final_plans.insert(0, a_plan)
            logging.warning(f'final_plans={len(final_plans)} candidate_plans={len(candidate_plans)}')
            # TODO: If the order of the items in each plan is not relevant, we can remove duplicates by returning set(tuple(sorted(x)) for x in final_plans)
        return final_plans

    def generate_pevs_release(self, number_of_cycles=1):
        original_cr = self.__cycle_restrictions.copy()
        existing_pevs = None
        for i in range(1, number_of_cycles + 1):
            print('----- Executing cycle number = ', i)
            cr = [j * i for j in self.__cycle_restrictions]
            print('------ Cycle restrictions = ', cr)
            self.__cycle_restrictions = cr.copy()
            pevs = self.__generate_pevs_next_cycle(existing_pevs)
            if pevs == existing_pevs:
                print('----- Will not analyse the next', number_of_cycles - i,
                      'cycles because the current cycle brought the same plans as the previous cycle ')
                break
            else:
                existing_pevs = pevs.copy()
        self.__cycle_restrictions = original_cr.copy()
        print('Final plan is', pevs)
        return pevs

    def dea_run(self, number_of_cycles=1):
        pevs = self.generate_pevs_release(number_of_cycles=number_of_cycles)
        result = {}
        for i in range(len(pevs)):
            result[str(i)] = {'pevs': pevs[i],
                              'inputs': self.__backlog.get_total_requirements(pevs[i]),
                              'outputs': self.__backlog.get_total_benefits(pevs[i])
                              }
        print('io will be like', result)
        dea = DEA()
        dea.set_io(result)
        r = dea.run()
        print('DEA run', r)
        final = []
        for k, v in r.items():
            p = result[k]
            final.append({'pevs': p['pevs'],
                          'inputs': p['inputs'],
                          'outputs': p['outputs'],
                          'efficiency': v})
        print('final', final)
        return {'efficiencies': final}
