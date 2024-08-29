from ..figure_data_loader import embedded_flux_data
from .config import np, Vector, ParameterName, DataFigureConfig, ScatterDataFigure


GroupDataFigure = DataFigureConfig.GroupDataFigure


class EmbeddedSolutionScatterDataFigure(ScatterDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        ax_total_bottom_left = Vector(0.1, 0.1)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left

        marker_size = 0.8 * scale
        color_dict = figure_data_parameter_dict[ParameterName.color_dict]
        embedded_flux_data_dict, *_ = embedded_flux_data.return_data(
            **figure_data_parameter_dict)

        common_text_config = {
            ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size,
            ParameterName.width: GroupDataFigure.label_width,
            ParameterName.height: GroupDataFigure.label_height,
        }
        figure_config_dict = {
            ParameterName.y_label_format_dict: {
                ParameterName.axis_label_distance: GroupDataFigure.adjacent_y_label_distance,
                **common_text_config
            },
            ParameterName.x_label_format_dict: {
                ParameterName.axis_label_distance: GroupDataFigure.adjacent_x_label_distance,
                **common_text_config
            }
        }

        complete_data_dict = {}
        x_min = y_min = np.inf
        x_max = y_max = -np.inf
        x_value_array_list = []
        y_value_array_list = []
        marker_color_list = []
        for data_label, embedded_flux_array in embedded_flux_data_dict.items():
            x_value_array = embedded_flux_array[:, 0]
            y_value_array = embedded_flux_array[:, 1]
            x_min = np.minimum(x_min, np.min(x_value_array))
            x_max = np.maximum(x_max, np.max(x_value_array))
            y_min = np.minimum(y_min, np.min(y_value_array))
            y_max = np.maximum(y_max, np.max(y_value_array))
            current_label_data_dict = {
                ParameterName.x_value_array: x_value_array,
                ParameterName.y_value_array: y_value_array,
                ParameterName.marker_size: marker_size,
                ParameterName.marker_color: [color_dict[data_label]],  # To avoid warning from matplotlib
                ParameterName.scatter_param_dict: {
                    ParameterName.alpha: 0.8,
                    ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order
                }
            }
            complete_data_dict[data_label] = current_label_data_dict
            x_value_array_list.append(x_value_array)
            y_value_array_list.append(y_value_array)
            marker_color_list.extend([color_dict[data_label]] * len(x_value_array))

        current_tissue_data_dict = {
            ParameterName.x_value_array: np.concatenate(x_value_array_list),
            ParameterName.y_value_array: (np.concatenate(y_value_array_list), None),
            ParameterName.marker_size: marker_size,
            ParameterName.marker_color: marker_color_list,  # To avoid warning from matplotlib
            ParameterName.scatter_param_dict: {
                ParameterName.alpha: 0.8,
                ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order
            },
        }
        x_lim = Vector(x_min, x_max) + Vector(-1, 1) * 0.1 * (x_max - x_min)
        y_lim = Vector(y_min, y_max) + Vector(-1, 1) * 0.1 * (y_max - y_min)

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: [ax_total_bottom_left],
            ParameterName.ax_size_list: [ax_total_size],
            ParameterName.color_dict: None,
            ParameterName.data_nested_list: [current_tissue_data_dict],
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.x_lim_list: [x_lim],
            ParameterName.x_ticks_list: [[]],
            ParameterName.x_label_list: ['PC 1'],
            ParameterName.y_lim_list: [y_lim],
            ParameterName.y_ticks_list: [[]],
            ParameterName.y_label_list: ['PC 2'],

            ParameterName.legend: False,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, scale=scale,
            bottom_left_offset=bottom_left_offset, base_z_order=base_z_order, z_order_increment=z_order_increment,
            **kwargs)

