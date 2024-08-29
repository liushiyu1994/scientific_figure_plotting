from .config import DataFigureConfig, ParameterName, Vector, FontWeight, CompositeFigure, DataName, \
    common_legend_generator, TextBox, TextConfig, ZOrderConfig, VerticalAlignment, HorizontalAlignment, \
    GeneralElements, default_parameter_extract, CommonFigureMaterials
from ..data_figure.scatter_data_figure import EmbeddedSolutionScatterDataFigure
from ..data_figure.histogram_data_figure import TimeLossDistanceHistogramDataFigure
from ..data_figure.bar_data_figure import DistanceAndLossBarDataFigure
from .random_optimized_distance_diagram import RandomOptimizedDistanceDiagram

Line = GeneralElements.Line


class RandomOptimizedFluxComparisonConfig(object):
    common_legend_font_size = 9


class RandomOptimizedFigureConfig(object):
    common_title_text_config = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.z_order: ZOrderConfig.default_text_z_order,
        # ParameterName.font_weight: FontWeight.bold,
        ParameterName.text_box: False
    }


class RandomOptimizedFluxLayout(CompositeFigure):
    height_to_width_ratio = 0.55

    def __init__(self, total_width=1, **kwargs):
        self.total_width = total_width
        left_axis_bottom_margin = 0 * total_width
        left_axis_top_margin = 0.01 * total_width
        left_axis_height = 0.4 * total_width
        left_axis_width = 0.42 * total_width
        left_axis_top = left_axis_bottom_margin + left_axis_height
        left_title_height = 0.05 * total_width
        left_title_gap = 0.01 * total_width
        left_title_center_y = left_axis_top + left_title_gap + left_title_height / 2
        left_title_center = Vector(left_axis_width * (0.5 + 0.03), left_title_center_y)
        left_title_size = Vector(left_axis_width, left_title_height)
        left_title_top = left_axis_top + left_title_gap + left_title_height

        right_axis_width = 0.52 * total_width
        right_axis_bottom = 0.01
        right_axis_left = left_axis_width + 0.032 * total_width
        right_axis_height = 0.3 * total_width
        right_axis_bottom_left = Vector(right_axis_left, right_axis_bottom)
        right_axis_size = Vector(right_axis_width, right_axis_height)
        right_axis_top = right_axis_bottom + right_axis_height
        legend_bottom = right_axis_top + 0.03 * total_width
        legend_height = 0.09 * total_width
        legend_center_y = legend_bottom + legend_height / 2
        legend_center = Vector(right_axis_left + 0.5 * right_axis_width, legend_center_y)
        legend_size = Vector(right_axis_width, legend_height)

        total_height = left_title_top + left_axis_top_margin
        self.height_to_width_ratio = total_height / total_width

        common_color_dict = CommonFigureMaterials.histogram_color_dict
        embedded_solution_config_dict = {
            ParameterName.bottom_left: (0, left_axis_bottom_margin),
            ParameterName.size: [left_axis_width, left_axis_height],
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: DataName.hct116_cultured_cell_line,
                ParameterName.color_dict: common_color_dict,
            },
        }
        legend_config_dict = {
            ParameterName.legend_center: legend_center,
            ParameterName.legend_area_size: legend_size,
            ParameterName.name_dict: CommonFigureMaterials.time_loss_name_dict,
            ParameterName.horiz_or_vertical: ParameterName.vertical,
            ParameterName.text_config_dict: {
                ParameterName.font_size: RandomOptimizedFluxComparisonConfig.common_legend_font_size,
                ParameterName.font_weight: FontWeight.bold
            }
        }
        solution_distance_config_dict = {
            ParameterName.bottom_left: right_axis_bottom_left,
            ParameterName.size: right_axis_size,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.solution_distance_data,
                ParameterName.data_name: DataName.hct116_cultured_cell_line,
                ParameterName.color_dict: common_color_dict,
                ParameterName.legend: True,
                ParameterName.legend_config_dict: legend_config_dict
            },
        }

        embedded_solution_scatter_figure_title_config_dict = {
            **RandomOptimizedFigureConfig.common_title_text_config,
            ParameterName.font_size: 10.5,
            ParameterName.width: left_title_size.x,
            ParameterName.height: left_title_size.y,
            ParameterName.string: 'PCA of random and optimized solutions',
            ParameterName.center: left_title_center,
        }
        embedded_solution_scatter_figure_title = TextBox(**embedded_solution_scatter_figure_title_config_dict)

        subfigure_element_dict = {
            'embedded_solution_scatter_figure': {
                'embedded_solution_scatter_figure':
                    EmbeddedSolutionScatterDataFigure(**embedded_solution_config_dict),
                'title': embedded_solution_scatter_figure_title,
            },
            'solution_distance_histogram_figure': {
                'solution_distance_histogram_figure':
                    TimeLossDistanceHistogramDataFigure(**solution_distance_config_dict)
            },
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height), background=False, **kwargs)


class RandomOptimizedLossDistanceWithDiagramComparison(CompositeFigure):
    height_to_width_ratio = 0.55

    def __init__(
            self, figure_data_parameter_dict, scale=1, **kwargs):
        total_width = default_parameter_extract(figure_data_parameter_dict, ParameterName.total_width, 1, pop=True)
        horiz_or_vertical = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.horiz_or_vertical, ParameterName.horizontal, pop=True)

        self.total_width = total_width

        left_axis_bottom_margin = 0.02 * total_width
        left_axis_top_margin = 0.01 * total_width
        right_axis_height = 0.21
        right_axis_bottom = 0

        if horiz_or_vertical == ParameterName.horizontal:
            left_axis_width = 0.33 * total_width
            left_axis_height = 0.28
            right_axis_width = 0.68 * total_width
            right_axis_left = left_axis_width - 0.005 * total_width
            left_diagram_center_x = left_axis_width / 2
        elif horiz_or_vertical == ParameterName.vertical:
            left_axis_width = 0.45 * total_width
            left_axis_height = 0.25
            right_axis_width = 0.9 * total_width
            right_axis_left = 0.04 * total_width
            left_diagram_center_x = right_axis_width / 2
        else:
            raise ValueError()

        right_axis_bottom_left = Vector(right_axis_left, right_axis_bottom)
        right_axis_size = Vector(right_axis_width, right_axis_height)
        right_axis_top = right_axis_bottom + right_axis_height
        x_axis_line_y_loc = right_axis_bottom + 0.02
        x_axis_line_x_range = Vector(0.12, 0.72) * right_axis_width + right_axis_left
        title_height = 0.03

        right_title_bottom = right_axis_top + 0.0035
        right_title_center_y = right_title_bottom + title_height / 2
        right_title_center = Vector(right_axis_left + right_axis_width / 2, right_title_center_y)
        right_title_top = right_title_bottom + title_height

        legend_bottom = right_title_top + 0.007
        legend_height = 0.098
        legend_center_y = legend_bottom + legend_height / 2
        diagram_legend_width = 0.55 * right_axis_width
        figure_legend_width = 0.55 * right_axis_width
        legend_gap = - 0.1 * right_axis_width
        legend_left = right_axis_left - 0.05 * total_width
        diagram_legend_center = Vector(legend_left + 0.5 * diagram_legend_width, legend_center_y)
        diagram_legend_size = Vector(diagram_legend_width, legend_height)
        figure_legend_center = Vector(
            legend_left + diagram_legend_width + legend_gap + 0.5 * figure_legend_width, legend_center_y)
        figure_legend_size = Vector(figure_legend_width, legend_height)
        legend_top = legend_bottom + legend_height

        if horiz_or_vertical == ParameterName.horizontal:
            left_axis_center_y = left_axis_bottom_margin + left_axis_height / 2
        elif horiz_or_vertical == ParameterName.vertical:
            left_axis_center_y = legend_top + left_axis_bottom_margin + left_axis_height / 2
        else:
            raise ValueError()
        target_center_of_left_diagram = Vector(left_diagram_center_x, left_axis_center_y)

        left_title_bottom = left_axis_center_y + left_axis_height / 2
        left_title_center_y = left_title_bottom + title_height / 2
        left_title_center = Vector(left_diagram_center_x, left_title_center_y)
        left_title_top = left_title_bottom + title_height

        total_height = max(left_title_top + left_axis_top_margin, legend_top)
        self.height_to_width_ratio = total_height / total_width

        common_legend_config_dict = {
            ParameterName.horiz_or_vertical: ParameterName.vertical,
            ParameterName.text_config_dict: {
                ParameterName.font_size: RandomOptimizedFluxComparisonConfig.common_legend_font_size + 2,
                ParameterName.font_weight: FontWeight.bold
            },
            ParameterName.location_config_dict: {
                ParameterName.total_verti_edge_ratio: 0.1,
                ParameterName.row_verti_edge_ratio: 0.9,
            },
        }
        diagram_legend_config_dict = {
            **common_legend_config_dict,
            ParameterName.legend_center: diagram_legend_center,
            ParameterName.legend_area_size: diagram_legend_size,
            ParameterName.name_dict: CommonFigureMaterials.best_and_other_optimized_solution_name_dict,
            ParameterName.shape: ParameterName.circle,
            ParameterName.alpha: None,
        }
        diagram_legend_obj = common_legend_generator(
            diagram_legend_config_dict, CommonFigureMaterials.optimum_with_random_color_dict)

        figure_legend_config_dict = {
            **common_legend_config_dict,
            ParameterName.legend_center: figure_legend_center,
            ParameterName.legend_area_size: figure_legend_size,
            ParameterName.name_dict: CommonFigureMaterials.distance_and_loss_name_dict,
            ParameterName.location_config_dict: {
                ParameterName.total_verti_edge_ratio: 0.1,
                ParameterName.row_verti_edge_ratio: 0.5,
            },
        }
        figure_legend_obj = common_legend_generator(
            figure_legend_config_dict, CommonFigureMaterials.distance_and_loss_legend_color_dict)

        distance_and_loss_config_dict = {
            ParameterName.bottom_left: right_axis_bottom_left,
            ParameterName.size: right_axis_size,
            ParameterName.figure_data_parameter_dict: {
                **figure_data_parameter_dict
            },
        }
        x_axis_line_config_dict = {
            ParameterName.start: Vector(x_axis_line_x_range[0], x_axis_line_y_loc),
            ParameterName.end: Vector(x_axis_line_x_range[1], x_axis_line_y_loc),
            **DataFigureConfig.common_axis_line_param_dict_generator(scale)
        }
        random_optimization_distance_diagram_title_config_dict = {
            **RandomOptimizedFigureConfig.common_title_text_config,
            ParameterName.font_size: 11,
            ParameterName.width: left_axis_width,
            ParameterName.height: title_height,
            ParameterName.string: 'Distance calculation diagram',
            ParameterName.center: left_title_center,
        }
        random_optimization_distance_diagram_title = TextBox(**random_optimization_distance_diagram_title_config_dict)
        distance_and_loss_figure_title_config_dict = {
            **RandomOptimizedFigureConfig.common_title_text_config,
            ParameterName.font_size: 11,
            ParameterName.width: right_axis_width,
            ParameterName.height: title_height,
            ParameterName.string: 'Distance and loss comparison',
            ParameterName.center: right_title_center,
        }
        distance_and_loss_figure_title = TextBox(**distance_and_loss_figure_title_config_dict)
        common_scale = 0.25
        random_optimization_distance_diagram = RandomOptimizedDistanceDiagram(scale=common_scale)
        center_of_distance_diagram = random_optimization_distance_diagram.calculate_center(
            random_optimization_distance_diagram, common_scale)
        random_optimization_distance_diagram.move_and_scale(
            bottom_left_offset=target_center_of_left_diagram - center_of_distance_diagram)

        distance_and_loss_figure = DistanceAndLossBarDataFigure(**distance_and_loss_config_dict)

        subfigure_element_dict = {
            'random_optimization_distance_diagram': {
                'random_optimization_distance_diagram': random_optimization_distance_diagram,
                'legend': diagram_legend_obj,
                'title': random_optimization_distance_diagram_title
            },
            'distance_and_loss_figure': {
                'distance_and_loss_figure': distance_and_loss_figure,
                'x_axis_line': Line(**x_axis_line_config_dict),
                'title': distance_and_loss_figure_title,
                'legend': figure_legend_obj,
            },
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height), background=False,
            scale=scale, **kwargs)


class RandomOptimizedLossDistanceComparison(CompositeFigure):
    height_to_width_ratio = 0.55

    def __init__(self, scale=1, **kwargs):
        total_width = 0.7
        self.total_width = total_width
        right_axis_height = 0.21
        right_axis_width = 0.68
        right_axis_bottom = 0
        right_axis_left = 0.005
        right_axis_bottom_left = Vector(right_axis_left, right_axis_bottom)
        right_axis_size = Vector(right_axis_width, right_axis_height)
        right_axis_top = right_axis_bottom + right_axis_height
        x_axis_line_y_loc = right_axis_bottom + 0.02
        x_axis_line_x_range = Vector(0.13, 0.72) * right_axis_width + right_axis_left
        title_height = 0.03
        right_title_bottom = right_axis_top + 0.0035
        right_title_center_y = right_title_bottom + title_height / 2
        right_title_center = Vector(right_axis_left + right_axis_width / 2, right_title_center_y)
        right_title_top = right_title_bottom + title_height

        legend_bottom = right_title_top + 0.007
        legend_height = 0.05
        legend_center_y = legend_bottom + legend_height / 2
        figure_legend_width = right_axis_width
        figure_legend_center = Vector(
            0.5 * figure_legend_width, legend_center_y)
        figure_legend_size = Vector(figure_legend_width, legend_height)
        legend_top = legend_bottom + legend_height

        total_height = legend_top
        self.height_to_width_ratio = total_height / total_width

        figure_legend_config_dict = {
            ParameterName.horiz_or_vertical: ParameterName.horizontal,
            ParameterName.text_config_dict: {
                ParameterName.font_size: RandomOptimizedFluxComparisonConfig.common_legend_font_size,
                ParameterName.font_weight: FontWeight.bold
            },
            ParameterName.legend_center: figure_legend_center,
            ParameterName.legend_area_size: figure_legend_size,
            ParameterName.name_dict: CommonFigureMaterials.distance_and_loss_name_dict,
            ParameterName.location_config_dict: {
                ParameterName.total_verti_edge_ratio: 0.1,
                ParameterName.row_verti_edge_ratio: 0.5,
            },
        }
        figure_legend_obj = common_legend_generator(
            figure_legend_config_dict, CommonFigureMaterials.distance_and_loss_legend_color_dict)

        distance_and_loss_config_dict = {
            ParameterName.bottom_left: right_axis_bottom_left,
            ParameterName.size: right_axis_size,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: DataName.hct116_cultured_cell_line_squared_loss,
                ParameterName.common_y_lim: (0, 5.5),
                ParameterName.y_tick_interval: 1
            },
        }
        x_axis_line_config_dict = {
            ParameterName.start: Vector(x_axis_line_x_range[0], x_axis_line_y_loc),
            ParameterName.end: Vector(x_axis_line_x_range[1], x_axis_line_y_loc),
            **DataFigureConfig.common_axis_line_param_dict_generator(scale)
        }
        distance_and_loss_figure_title_config_dict = {
            **RandomOptimizedFigureConfig.common_title_text_config,
            ParameterName.font_size: 11,
            ParameterName.width: right_axis_width,
            ParameterName.height: title_height,
            ParameterName.string: 'Distance and loss comparison',
            ParameterName.center: right_title_center,
        }
        distance_and_loss_figure_title = TextBox(**distance_and_loss_figure_title_config_dict)

        distance_and_loss_figure = DistanceAndLossBarDataFigure(**distance_and_loss_config_dict)

        subfigure_element_dict = {
            'distance_and_loss_figure': {
                'distance_and_loss_figure': distance_and_loss_figure,
                'x_axis_line': Line(**x_axis_line_config_dict),
                'title': distance_and_loss_figure_title,
                'legend': figure_legend_obj,
            },
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height), background=False,
            scale=scale, **kwargs)