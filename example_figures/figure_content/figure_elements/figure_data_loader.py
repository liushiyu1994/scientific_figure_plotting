from ..common.config import FigureDataKeywords, BasicFigureData


class DatasetClass(object):
    renal_carcinoma_data_set = 'renal_carcinoma_data_set'
    colon_cancer_data_set = 'colon_cancer_data_set'


class Keywords(object):
    kidney = 'kidney'
    carcinoma = 'carcinoma'


class LossFigureData(BasicFigureData):
    data_prefix = FigureDataKeywords.loss_data_comparison

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def return_data(self, data_name, result_label_layout_list=None, **kwargs):
        if data_name not in self.processed_data_dict:
            current_data_obj = self._return_figure_data(data_name)
            loss_data_dict = current_data_obj.loss_data_dict
            filtered_loss_data_dict = current_data_obj.filtered_loss_data_dict
            if data_name in DatasetClass.renal_carcinoma_data_set:
                loss_data_dict = self._process_kidney_carcinoma_comparison_data(loss_data_dict)
                filtered_loss_data_dict = self._process_kidney_carcinoma_comparison_data(filtered_loss_data_dict)
            elif data_name in DatasetClass.colon_cancer_data_set:
                loss_data_dict = self._process_colon_cancer_cell_line_comparison_data(loss_data_dict)
                filtered_loss_data_dict = self._process_colon_cancer_cell_line_comparison_data(filtered_loss_data_dict)
            self.processed_data_dict[data_name] = (loss_data_dict, filtered_loss_data_dict)
        else:
            loss_data_dict, filtered_loss_data_dict = self.processed_data_dict[data_name]
        if result_label_layout_list is not None:
            updated_loss_data_dict = {}
            updated_filtered_loss_data_dict = {}
            for row_index, row_data_label_list in enumerate(result_label_layout_list):
                for col_index, data_label_list in enumerate(row_data_label_list):
                    current_loss_data_dict = {data_label: loss_data_dict[data_label] for data_label in data_label_list}
                    current_filtered_loss_data_dict = {
                        data_label: filtered_loss_data_dict[data_label] for data_label in data_label_list}
                    updated_loss_data_dict[(row_index, col_index)] = current_loss_data_dict
                    updated_filtered_loss_data_dict[(row_index, col_index)] = current_filtered_loss_data_dict
            loss_data_dict = updated_loss_data_dict
            filtered_loss_data_dict = updated_filtered_loss_data_dict
        return loss_data_dict, filtered_loss_data_dict

    @staticmethod
    def _process_kidney_carcinoma_comparison_data(raw_data_dict):
        new_data_dict = {}
        for data_label, data_vector in raw_data_dict.items():
            group_name, patient_id_str = data_label.split('__')
            if group_name == Keywords.kidney or group_name == Keywords.carcinoma:
                patient_id = patient_id_str[0]
                if patient_id not in new_data_dict:
                    new_data_dict[patient_id] = {}
                new_data_dict[patient_id][group_name] = data_vector
        return new_data_dict

    @staticmethod
    def _process_colon_cancer_cell_line_comparison_data(raw_data_dict):
        new_data_dict = {}
        for data_label, data_vector in raw_data_dict.items():
            cell_line, condition_str = data_label.split('__')
            condition = condition_str[0]
            if cell_line not in new_data_dict:
                new_data_dict[cell_line] = {}
            new_data_dict[cell_line][condition] = data_vector
        return new_data_dict


loss_data = LossFigureData()


class TimeFigureData(BasicFigureData):
    data_prefix = FigureDataKeywords.time_data_distribution

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def return_data(self, data_name, **kwargs):
        if data_name not in self.processed_data_dict:
            current_data_obj = self._return_figure_data(data_name)
            time_data_dict = current_data_obj.time_data_dict
            self.processed_data_dict[data_name] = time_data_dict
        else:
            time_data_dict = self.processed_data_dict[data_name]
        return time_data_dict


time_data = TimeFigureData()


class BestSolutionData(BasicFigureData):
    data_prefix = FigureDataKeywords.best_solution

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def _figure_data_preprocess(self, data_name):
        if data_name not in self.processed_data_dict:
            current_data_obj = self._return_figure_data(data_name)
            best_loss_data = current_data_obj.best_loss_data
            best_solution_vector = current_data_obj.best_solution_vector
            flux_name_index_dict = current_data_obj.flux_name_index_dict
            self.processed_data_dict[data_name] = (best_loss_data, best_solution_vector, flux_name_index_dict)
        else:
            best_loss_data, best_solution_vector, flux_name_index_dict = self.processed_data_dict[data_name]
        return best_loss_data, best_solution_vector, flux_name_index_dict

    def return_data(self, data_name, **kwargs):
        return self._figure_data_preprocess(data_name)


best_solution_data = BestSolutionData()


class EmbeddedFluxData(BasicFigureData):
    data_prefix = FigureDataKeywords.embedding_visualization

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def _figure_data_preprocess(self, data_name):
        if data_name in self.processed_data_dict:
            content_tuple = self.processed_data_dict[data_name]
        else:
            current_data_obj = self._return_figure_data(data_name)
            embedded_flux_data_dict = current_data_obj.embedded_flux_data_dict
            complete_distance_dict = current_data_obj.complete_distance_dict
            separated_distance_and_loss_dict = current_data_obj.separated_distance_and_loss_dict
            flux_name_list = current_data_obj.flux_name_list
            content_tuple = (
                embedded_flux_data_dict, complete_distance_dict, separated_distance_and_loss_dict, flux_name_list)
            self.processed_data_dict[data_name] = content_tuple
        return content_tuple

    def return_data(self, data_name, **kwargs):
        return self._figure_data_preprocess(data_name)


embedded_flux_data = EmbeddedFluxData()

