from .config import DataFigureConfig, ParameterName, Vector, it, Keywords, \
    np, default_parameter_extract, CommonFigureMaterials, \
    DataName, CommonFigureString, BarDataFigure, BasicFluxErrorBarDataFigure, \
    symmetrical_lim_tick_generator_with_zero
from ..figure_data_loader import embedded_flux_data


GroupDataFigure = DataFigureConfig.GroupDataFigure
common_data_label = ''


class DistanceAndLossDataFigureConfig(object):
    separated_optimized_solution_num = 5
    collected_optimized_solution_num_list = [20, 100]


class DistanceAndLossBarDataFigure(BarDataFigure):
    @staticmethod
    def distance_or_loss_filtering(
            optimized_value_array, unoptimized_value_array, separated_optimized_solution_num,
            collected_optimized_solution_num_list):
        separated_optimized_value_array = optimized_value_array[:separated_optimized_solution_num]
        mean_value_list = []
        std_value_list = []
        for each_separated_value in separated_optimized_value_array:
            mean_value_list.append(each_separated_value)
            std_value_list.append(np.nan)
        for collected_optimized_solution_num in collected_optimized_solution_num_list:
            collected_value_array = optimized_value_array[:collected_optimized_solution_num]
            mean_value_list.append(np.mean(collected_value_array))
            std_value_list.append(np.std(collected_value_array))

        mean_value_list.append(np.mean(unoptimized_value_array))
        std_value_list.append(np.std(unoptimized_value_array))

        mean_value_array = np.array(mean_value_list)
        std_value_array = np.array(std_value_list)
        return mean_value_array, std_value_array

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        # ax_total_bottom_left = DataFigureConfig.common_ax_total_bottom_left
        # ax_total_size = DataFigureConfig.common_ax_total_size
        default_ax_total_bottom_left = Vector(0.09, 0.19)
        default_ax_total_size = Vector(0.78, 1 - default_ax_total_bottom_left.y)
        ax_total_bottom_left = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_total_bottom_left, default_ax_total_bottom_left)
        ax_total_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_total_size, default_ax_total_size)
        color_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.color_dict, CommonFigureMaterials.distance_and_loss_color_dict)

        common_label_width = GroupDataFigure.label_width * scale
        common_label_height = GroupDataFigure.label_height * scale
        common_tick_label_text_size = GroupDataFigure.x_y_axis_tick_label_font_size * scale

        figure_config_dict = {
            ParameterName.column_width: 0.7,
            ParameterName.edge: 0.05,
            ParameterName.x_label_format_dict: {
                ParameterName.axis_label_distance: 0.025 * scale,
                ParameterName.width: common_label_width,
                ParameterName.height: common_label_height,
                ParameterName.font_size: GroupDataFigure.x_y_axis_tick_label_font_size * scale,
                ParameterName.axis_label_location: 0.41666
            },
            ParameterName.x_tick_label_format_dict: {
                ParameterName.axis_tick_label_distance: 0.005 * scale,
                ParameterName.width: common_label_width,
                ParameterName.height: common_label_height,
                ParameterName.font_size: GroupDataFigure.x_y_axis_smaller_label_font_size * scale,
            },
            ParameterName.y_label_format_dict: (
                {
                    ParameterName.axis_label_distance: 0.028 * scale,
                    ParameterName.width: common_label_width,
                    ParameterName.height: common_label_height,
                    ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size * scale,
                    ParameterName.font_color: color_dict[ParameterName.loss]
                },
                {
                    ParameterName.axis_label_distance: 0.043 * scale,
                    ParameterName.width: common_label_width,
                    ParameterName.height: common_label_height,
                    ParameterName.font_size: GroupDataFigure.x_y_axis_tick_label_font_size * scale,
                    ParameterName.font_color: color_dict[ParameterName.net_distance]
                }
            ),
            ParameterName.y_tick_label_format_dict:
            (
                {
                    ParameterName.axis_tick_label_distance: 0.008 * scale,
                    ParameterName.font_size: common_tick_label_text_size,
                    ParameterName.font_color: color_dict[ParameterName.loss]
                },
                {
                    ParameterName.axis_tick_label_distance: 0.008 * scale,
                    ParameterName.font_size: common_tick_label_text_size,
                    ParameterName.font_color: color_dict[ParameterName.net_distance]
                }
            ),
            ParameterName.bar_param_dict: {
                ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order,
                ParameterName.alpha: DataFigureConfig.alpha_for_bar_plot
            },
            ParameterName.error_bar_param_dict: DataFigureConfig.common_error_bar_param_dict_generator(scale)
        }

        *_, separated_distance_and_loss_dict, _ = embedded_flux_data.return_data(**figure_data_parameter_dict)
        (
            difference_vector_to_optimized_flux_solution, raw_distance_to_optimized_flux_solution,
            filtered_net_distance_to_optimized_flux_solution, optimized_loss_array) = separated_distance_and_loss_dict[
            ParameterName.optimized]
        (
            difference_vector_to_unoptimized_flux_solution, raw_distance_to_unoptimized_flux_solution,
            filtered_net_distance_to_unoptimized_flux_solution, unoptimized_loss_array) = separated_distance_and_loss_dict[
            ParameterName.unoptimized]

        separated_optimized_solution_num = DistanceAndLossDataFigureConfig.separated_optimized_solution_num
        collected_optimized_solution_num_list = DistanceAndLossDataFigureConfig.collected_optimized_solution_num_list
        array_len = separated_optimized_solution_num + len(collected_optimized_solution_num_list) + 1

        distance_y_lim = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_lim_2, (0, 3600))
        distance_y_tick_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_tick_interval_2, 1000)
        distance_y_tick = np.arange(*distance_y_lim, distance_y_tick_interval)

        loss_mean_array, loss_std_array = self.distance_or_loss_filtering(
            optimized_loss_array, unoptimized_loss_array,
            separated_optimized_solution_num, collected_optimized_solution_num_list)
        raw_distance_mean_array, raw_distance_std_array = self.distance_or_loss_filtering(
            raw_distance_to_optimized_flux_solution, raw_distance_to_unoptimized_flux_solution,
            separated_optimized_solution_num, collected_optimized_solution_num_list)
        net_distance_mean_array, net_distance_std_array = self.distance_or_loss_filtering(
            filtered_net_distance_to_optimized_flux_solution, filtered_net_distance_to_unoptimized_flux_solution,
            separated_optimized_solution_num, collected_optimized_solution_num_list)
        data_array_dict = {
            ParameterName.loss: (0, loss_mean_array, 0),
            ParameterName.distance: (1, raw_distance_mean_array, 1),
            ParameterName.net_distance: (1, net_distance_mean_array, 1),
        }
        data_error_bar_array_dict = {
            ParameterName.loss: loss_std_array,
            ParameterName.distance: raw_distance_std_array,
            ParameterName.net_distance: net_distance_std_array,
        }

        x_tick_labels = [
            CommonFigureString.minimal_loss,
            *[f'{CommonFigureString.number}{index + 2}' for index in range(separated_optimized_solution_num - 1)],
            *[f'{CommonFigureString.top} {collected_num}' for collected_num in collected_optimized_solution_num_list],
            CommonFigureString.random_fluxes_wrap
        ]

        loss_y_lim = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_lim, (0, 22))
        loss_y_tick_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_tick_interval, 5)
        loss_y_tick = np.arange(*loss_y_lim, loss_y_tick_interval)

        y_lim = (loss_y_lim, distance_y_lim)
        y_ticks = (loss_y_tick, distance_y_tick)
        y_labels = (CommonFigureString.loss, CommonFigureString.euclidean_distance)

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: [ax_total_bottom_left],
            ParameterName.ax_size_list: [ax_total_size],
            ParameterName.color_dict: color_dict,
            ParameterName.data_nested_list: [(data_array_dict, data_error_bar_array_dict)],
            ParameterName.array_len_list: [array_len],
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.x_label_list: [CommonFigureString.optimized_solution],
            ParameterName.x_tick_labels_list: [x_tick_labels],
            ParameterName.y_lim_list: [y_lim],
            ParameterName.y_label_list: [y_labels],
            ParameterName.y_ticks_list: [y_ticks],
            ParameterName.y_tick_labels_list: [(Keywords.default, Keywords.default)],

            ParameterName.max_bar_num_each_group: 2,
            ParameterName.legend: False,
            ParameterName.twin_x_axis: True,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, scale=scale, # twin_x_axis=True,
            bottom_left_offset=bottom_left_offset, base_z_order=base_z_order, z_order_increment=z_order_increment,
            background=False, **kwargs)


class CommonDifferenceFluxErrorBarDataFigure(BasicFluxErrorBarDataFigure):
    ax_total_bottom_left = Vector(0, 0)
    ax_total_size = Vector(1, 1) - ax_total_bottom_left
    ax_y_interval = 0.015

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        bar_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_interval, Vector(0, self.ax_y_interval))
        flux_name_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.flux_name_list, None, force=True)
        relative_error = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.flux_relative_distance, False, pop=True)

        data_nested_list = []
        vector_array_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.net_optimized_diff_vector_list, None, force=True, pop=True)
        data_label_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.data_label, it.repeat(common_data_label), pop=True)
        subplot_name_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.subplot_name_list, None, pop=True)
        text_axis_loc_pair = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.text_axis_loc_pair, Vector(0.5, 0.9), pop=True)

        specific_subplot_name_text_format_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.subplot_name_text_format_dict, {}, pop=True)
        subplot_name_text_format_dict = {
            ParameterName.font_size: 12,
            **specific_subplot_name_text_format_dict,
        }

        _, select_average_reoptimize_color_dict = CommonFigureMaterials.select_average_solution_name_color_dict(
            CommonFigureMaterials, with_reoptimization=True, with_traditional_method=True,
            different_simulated_data=True)
        color_dict = {
            common_data_label: CommonFigureMaterials.default_flux_error_bar_color,
            **select_average_reoptimize_color_dict,
        }

        for current_vector_array, data_label in zip(vector_array_list, data_label_list):
            current_vector_dim = len(np.shape(current_vector_array))
            if current_vector_dim == 1:
                mean_diff_vector = current_vector_array
                std_diff_vector = np.nan * np.ones_like(current_vector_array)
            elif current_vector_dim == 2:
                mean_diff_vector = np.mean(current_vector_array, axis=0)
                std_diff_vector = np.std(current_vector_array, axis=0)
            else:
                raise ValueError()
            data_nested_list.append((
                {data_label: mean_diff_vector, },
                {data_label: std_diff_vector, },
            ))

        total_axis_num = len(data_nested_list)
        ax_total_bottom_left_list = []
        ax_total_size_list = []
        ax_y_interval = bar_interval
        ax_total_size = self.ax_total_size
        ax_total_bottom_left = self.ax_total_bottom_left
        ax_height = (1 - ax_y_interval * (total_axis_num - 1)) / total_axis_num
        for index in range(total_axis_num - 1, -1, -1):
            ax_bottom_left = Vector(
                ax_total_bottom_left.x, ax_total_bottom_left.y + (ax_height + ax_y_interval) * index)
            ax_total_bottom_left_list.append(ax_bottom_left)
            ax_total_size_list.append(Vector(ax_total_size.x, ax_height))
        y_lim = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_lim, None, pop=True)
        y_ticks = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_ticks_list, None, pop=True)
        y_abs_lim = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_abs_lim, 350.0001, pop=True)
        y_tick_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_tick_interval, 100, pop=True)
        y_label = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_label, CommonFigureString.difference, pop=True
        )
        if y_lim is None and y_ticks is None:
            y_lim, y_ticks = symmetrical_lim_tick_generator_with_zero(y_abs_lim, None, y_tick_interval)
        elif y_lim is None or y_ticks is None:
            raise ValueError()
        cutoff_value_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.cutoff, None, pop=True)
        y_tick_labels = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_tick_labels_list, None, pop=True)
        if y_tick_labels is None:
            y_tick_labels = []
            if relative_error:
                label_format_str = '{:.0%}'
            else:
                label_format_str = '{:.0f}'
            for y_tick in y_ticks:
                try:
                    each_ax_y_ticks = y_tick
                    current_y_tick_label = [label_format_str.format(y_tick) for y_tick in each_ax_y_ticks]
                except TypeError:
                    current_y_tick_label = label_format_str.format(y_tick)
                y_tick_labels.append(current_y_tick_label)

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: ax_total_bottom_left_list,
            ParameterName.ax_size_list: ax_total_size_list,
            ParameterName.color_dict: color_dict,
            ParameterName.data_nested_list: data_nested_list,
            ParameterName.flux_name_list: flux_name_list,
            ParameterName.cutoff: cutoff_value_list,

            ParameterName.common_y_lim: y_lim,
            ParameterName.common_y_label: y_label,
            ParameterName.y_ticks_list: y_ticks,
            ParameterName.default_y_tick_label_list: y_tick_labels,

            ParameterName.subplot_name_list: subplot_name_list,
            ParameterName.subplot_name_text_format_dict: subplot_name_text_format_dict,
            ParameterName.text_axis_loc_pair: text_axis_loc_pair,
            **figure_data_parameter_dict
        }

        super().__init__(
            figure_data_parameter_dict, bottom_left, size, **kwargs)


class HCT116OptimizedFluxErrorBarDataFigure(CommonDifferenceFluxErrorBarDataFigure):

    separated_optimized_solution_num = DistanceAndLossDataFigureConfig.separated_optimized_solution_num
    collected_optimized_solution_num_list = DistanceAndLossDataFigureConfig.collected_optimized_solution_num_list

    @staticmethod
    def calculate_row_num(
            self, with_single_optimized_solutions=True, with_collected_optimized_set=True, with_unoptimized_set=True,
            **kwargs):
        total_row_num = 0
        if with_single_optimized_solutions:
            total_row_num += self.separated_optimized_solution_num - 1
        if with_collected_optimized_set:
            total_row_num += len(self.collected_optimized_solution_num_list)
        if with_unoptimized_set:
            total_row_num += 1
        return total_row_num

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        bar_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_interval, Vector(0, self.ax_y_interval))
        *_, separated_distance_and_loss_dict, flux_name_list = embedded_flux_data.return_data(
            **figure_data_parameter_dict)
        net_target_optimized_diff_vector, *_ = separated_distance_and_loss_dict[ParameterName.optimized]
        net_target_unoptimized_diff_vector, *_ = separated_distance_and_loss_dict[ParameterName.unoptimized]
        self.with_single_optimized_solutions = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.with_single_optimized_solutions, True)
        self.with_collected_optimized_set = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.with_collected_optimized_set, True)
        self.with_unoptimized_set = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.with_unoptimized_set, True)
        with_glns_m = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.with_glns_m, False)

        separated_optimized_solution_num = self.separated_optimized_solution_num
        collected_optimized_solution_num_list = self.collected_optimized_solution_num_list

        net_optimized_diff_vector_list = []
        subplot_name_list = []
        if self.with_single_optimized_solutions:
            net_optimized_diff_vector_list.extend([
                current_optimized_net_diff_vector_array
                for current_optimized_net_diff_vector_array
                in net_target_optimized_diff_vector[1:separated_optimized_solution_num, :]
            ])
            subplot_name_list.extend([
                f'{CommonFigureString.number}{index + 2} optimized solution'
                for index in range(separated_optimized_solution_num - 1)])
        if self.with_collected_optimized_set:
            for collected_num_index, collected_num in enumerate(collected_optimized_solution_num_list):
                net_optimized_diff_vector_list.append(net_target_optimized_diff_vector[:collected_num, :])
                subplot_name_list.append(f'{CommonFigureString.top} {collected_num}')
        if self.with_unoptimized_set:
            net_optimized_diff_vector_list.append(net_target_unoptimized_diff_vector)
            subplot_name_list.append(CommonFigureString.random_fluxes)

        # y_abs_lim = 350.0001
        # y_tick_interval = 100
        if with_glns_m:
            middle_y_lim, middle_y_ticks = symmetrical_lim_tick_generator_with_zero(
                280, 280, 100)
            top_y_lim = [290, 650]
            y_lim = [middle_y_lim, top_y_lim]
            y_ticks = [middle_y_ticks, [350, 550]]
            y_label = [CommonFigureString.relative_error, None]
            broken_y_axis_ratio = [(0, 0.79), (0.84, 1)]

            extra_figure_data_parameter_dict = {
                ParameterName.broken_y_axis: broken_y_axis_ratio,
                ParameterName.common_y_lim: y_lim,
                ParameterName.common_y_label: y_label,
                ParameterName.y_ticks_list: y_ticks,
                ParameterName.y_label_format_dict: {ParameterName.axis_label_location: 0.7, },
                ParameterName.text_axis_loc_pair: Vector(0.4, 0.9),
            }
        else:
            extra_figure_data_parameter_dict = {
                ParameterName.y_abs_lim: 350.0001,
                ParameterName.y_tick_interval: 100,
            }

        figure_data_parameter_dict = {
            ParameterName.net_optimized_diff_vector_list: net_optimized_diff_vector_list,
            ParameterName.ax_interval: bar_interval,
            ParameterName.flux_name_list: flux_name_list,

            ParameterName.subplot_name_list: subplot_name_list,
            **extra_figure_data_parameter_dict,
            **figure_data_parameter_dict
        }

        super().__init__(
            figure_data_parameter_dict, bottom_left, size, **kwargs)
