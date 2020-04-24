import pyDEA.core.data_processing.input_data as in_data
import pyDEA.core.data_processing.parameters as param
import pyDEA.core.utils.model_factory as factory


class DEA:

    def __init__(self, return_to_scale='VRS', form='env', orientation='output'):
        self.__return_to_scale = return_to_scale
        self.__form = form
        self.__orientation = orientation
        self.__dea_params = param.Parameters()
        self.__dea_params.update_parameter('RETURN_TO_SCALE', return_to_scale)
        self.__dea_params.update_parameter('DEA_FORM', form)
        self.__dea_params.update_parameter('ORIENTATION', orientation)
        self.__dea_params.update_parameter('INPUT_CATEGORIES', 'i1')
        self.__dea_params.update_parameter('OUTPUT_CATEGORIES', 'o1')
        # self.dea_params.print_all_parameters()

    @property
    def return_to_scale(self):
        return self.__return_to_scale

    @return_to_scale.setter
    def return_to_scale(self, return_to_scale):
        self.__return_to_scale = return_to_scale

    @property
    def form(self):
        return self.__form

    @form.setter
    def form(self, form):
        self.__form = form

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, orientation):
        self.__orientation = orientation

    def set_dmu_variables(self, dmu_inputs={}, dmu_outputs={}):
        self.__dea_data = in_data.InputData()
        for id_dmu, inputs in dmu_inputs.items():
            for id_input, value in inputs.items():
                self.__dea_data.add_coefficient('dmu' + id_dmu, 'in' + id_input, value)
        for id_dmu, outputs in dmu_outputs.items():
            for id_output, value in outputs.items():
                self.__dea_data.add_coefficient('dmu' + id_dmu, 'out' + id_output, value)
        self.__dea_data.add_input_category('in1')
        self.__dea_data.add_output_category('out1')
        # self.dea_params.update_parameter('INPUT_CATEGORIES', 'in1')
        # self.dea_params.update_parameter('OUTPUT_CATEGORIES', 'out1')
        # dea_data.print_coefficients()

    def run(self):
        model = factory.create_model(self.__dea_params, self.__dea_data)
        solution = model.run()
        r = {}
        s = solution.efficiency_scores
        for dmu_key in sorted(s.keys()):
            r[self.__dea_data.get_dmu_user_name(dmu_key)] = s[dmu_key]
        return r
        # model_solution.print_solution()
        # print(model_solution.efficiency_scores)

    def set_io(self, io):
        self.__dmu_names = {}
        self.__dea_data = in_data.InputData()
        for i in io:
            id_dmu = i
            inputs = io[i]['inputs']
            outputs = io[i]['outputs']
            self.__dmu_names.update({str(id_dmu):io[i]['pevs']})
            for j in range(len(inputs)):
                id_input = j
                value = inputs[j]
                self.__dea_data.add_coefficient(str(id_dmu), 'in' + str(id_input), value)
            for k in range(len(outputs)):
                id_output = k
                value = outputs[k]
                self.__dea_data.add_coefficient(str(id_dmu), 'out' + str(id_output), value)
        for x in range(j+1):
            self.__dea_data.add_input_category('in' + str(x))
            print('setting', 'in' + str(x))
        for x in range(k+1):
            self.__dea_data.add_output_category('out' + str(x))
            print('setting', 'out' + str(x))


if __name__ == "__main__":
    import sys

    try:
        DMU_INPUTS = sys.argv[1]
        DMU_OUTPUTS = sys.argv[2]
    except IndexError as error:
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
    finally:
        dea = DEA()
        dea.set_dmu_variables(DMU_INPUTS, DMU_OUTPUTS)
        result = dea.run()
        for dmu_key, dmu_value in result.items():
            print(dmu_key, '\t', dmu_value)
