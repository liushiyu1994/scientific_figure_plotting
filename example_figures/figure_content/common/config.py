from figure_plotting_package.common.config import ParameterName as GeneralParameterName
from figure_plotting_package.common.classes import Vector, VerticalAlignment, HorizontalAlignment, FontWeight, LineStyle
from figure_plotting_package.common.color import ZOrderConfig, ColorConfig, TextConfig
from figure_plotting_package.common.common_figure_materials import CommonElementConfig
from figure_plotting_package.common.built_in_packages import it
from figure_plotting_package.common.third_party_packages import np
from figure_plotting_package.common.common_functions import (
    calculate_center_bottom_offset, default_parameter_extract, symmetrical_lim_tick_generator_with_zero)
from figure_plotting_package.common.figure_data_format import BasicFigureData as RawBasicFigureData

from figure_plotting_package.data_figure.config import Keywords, ParameterName as DataParameterName, DataFigureConfig

from figure_plotting_package.diagrams.config import ParameterName as DiagramParameterName

from figure_plotting_package.elements import Elements as GeneralElements, common_legend_generator


class ParameterName(DataParameterName, DiagramParameterName):
    pass


class Direct(object):
    common_data_direct = 'common_data'
    common_submitted_raw_data_direct = f'{common_data_direct}/raw_data'
    figure_raw_data_direct = f'{common_data_direct}/figure_raw_data'
    figure_output_direct = 'example_figures/output_figure'


class DataName(object):
    hct116_cultured_cell_line = 'hct116_cultured_cell_line'
    hct116_cultured_cell_line_with_glns_m = 'hct116_cultured_cell_line_with_glns_m'
    hct116_cultured_cell_line_squared_loss = 'hct116_cultured_cell_line_squared_loss'
    raw_model_all_data = 'raw_model_all_data'
    raw_model_raw_data = 'raw_model_raw_data'
    raw_model_with_glns_m_raw_data = 'raw_model_with_glns_m_raw_data'
    raw_model_with_glns_m_all_data = 'raw_model_with_glns_m_all_data'

    optimization_from_solutions_raw_data = 'optimization_from_raw_data_average_solutions'
    optimization_from_solutions_all_data = 'optimization_from_all_data_average_solutions'
    optimization_from_batched_raw_data = 'optimization_from_batched_simulated_raw_data'
    optimization_from_batched_all_data = 'optimization_from_batched_simulated_all_data'

    data_sensitivity = 'data_sensitivity'


class CommonFigureString(object):
    difference_from_best_optimized_solution = 'Difference from the minimal loss solution'

    selected_solution = 'Selected solutions'
    selected_solution_wrap = 'Selected\nsolutions'
    random_fluxes = 'Random initial fluxes'
    random_fluxes_wrap = 'Random\ninitial fluxes'
    optimized_solution = 'Optimized solutions'
    optimized_solution_wrap = 'Optimized\nsolutions'
    best_optimized_solution = 'The minimal loss solution'
    best_optimized_solution_wrap = 'The minimal loss\nsolution'
    averaged_solution = 'Averaged solutions'
    averaged_solution_wrap = 'Averaged\nsolutions'
    reoptimized_solution = 'Re-optimized solutions'
    reoptimized_solution_wrap = 'Re-optimized\nsolutions'
    traditional_solution = 'Benchmark'
    traditional_solution_wrap = 'Benchmark'
    traditional_solution_double_wrap = 'Benchmark'
    different_simulated_solution_distance_wrap = 'Distance between\nsimulated solutions'

    unconstrained_fluxes = 'Unconstrained fluxes'
    unconstrained_fluxes_wrap = 'Unconstrained\nfluxes'
    constrained_fluxes = 'Constrained fluxes'
    constrained_fluxes_wrap = 'Constrained\nfluxes'
    flux_sloppiness_wrap = 'Flux variability\nin optimized solutions'

    loss_function_str = 'Loss value'
    left_parenthesis = r'\mathrm{(}'
    right_parenthesis = r'\mathrm{)}'
    math_n = r'\mathit{n}'
    math_m = r'\mathit{m}'
    bold_math_n = r'\mathbf{n}'
    bold_math_m = r'\mathbf{m}'
    m_over_n = f'{math_m}/{math_n}'
    initial_flux = r'\mathbf{v}_0'
    known_flux = r'$\mathbf{v^\prime}$'
    flux_vector = r'\mathbf{v}'
    optimal_flux_vector = r'\mathbf{v}\mathit{^*}'
    loss_function = r'\mathit{L}' + left_parenthesis + '\mathbf{v}' + right_parenthesis

    glc_input = 'GLC input'
    gln_input = 'GLN input'
    cma = 'CIT-MAL Antiport (CMA)'
    cma_wrap = 'CIT-MAL Antiport\n(CMA)'
    ama = 'AKG-MAL Antiport (AMA)'
    ama_wrap = 'AKG-MAL Antiport\n(AMA)'

    no_1_string = '①'
    no_2_string = '②'
    no_3_string = '③'

    average_running_time = 'Running time (s)'
    final_loss = r'\mathit{L^*}'
    final_loss_with_equation = f'Final loss ${final_loss}$'
    final_loss_with_equation_bold = 'Final loss $\mathbf{L^*}$'
    initial_points = f'${math_n}$ initial points'
    n_optimized_solutions = f'${math_n}$ optimized solutions'
    m_selected_solutions = f'${math_m}$ selected solutions'
    best_solution = r'Best solution'
    euclidean_distance = 'Euclidean distance'
    raw_euclidean_distance = f'{euclidean_distance} (all fluxes)'
    net_euclidean_distance = f'{euclidean_distance} (net fluxes)'
    minimal_loss = 'Minimal loss'
    loss = 'Loss'
    number = 'No.'
    top = 'Top'
    difference = 'Difference'
    relative_error = 'Relative error'
    simulated_data = 'Simulated data'

    @staticmethod
    def fixed_flux_string_generator(fixed_value):
        return 'Fixed value: {:.1f}'.format(fixed_value)


class CommonFigureMaterials(object):
    optimum_color_dict = {
        ParameterName.local_optimum: ColorConfig.selected_solution_color,
        ParameterName.global_optimum: ColorConfig.global_optimum_color_with_alpha,
    }
    optimum_with_random_color_dict = {
        ParameterName.unoptimized: ColorConfig.random_flux_color_with_alpha,
        **optimum_color_dict,
    }
    optimum_with_random_text_color_dict = {
        ParameterName.unoptimized: ColorConfig.random_flux_color,
        ParameterName.local_optimum: ColorConfig.selected_solution_text_color,
        ParameterName.global_optimum: ColorConfig.global_optimum_color,
    }
    histogram_color_dict = {
        ParameterName.unoptimized: ColorConfig.random_flux_color,
        ParameterName.optimized: ColorConfig.selected_solution_text_color,
    }
    random_fluxes_str = CommonFigureString.random_fluxes
    optimized_solution_str = CommonFigureString.optimized_solution
    best_optimized_solution_str = CommonFigureString.best_optimized_solution
    time_loss_name_dict = {
        ParameterName.optimized: optimized_solution_str,
        ParameterName.unoptimized: random_fluxes_str
    }
    best_and_other_optimized_solution_name_dict = {
        ParameterName.unoptimized: random_fluxes_str,
        ParameterName.local_optimum: optimized_solution_str,
        ParameterName.global_optimum: best_optimized_solution_str,
    }
    distance_and_loss_name_dict = {
        ParameterName.loss: 'Loss of solution',
        ParameterName.distance: CommonFigureString.raw_euclidean_distance,
        ParameterName.net_distance: CommonFigureString.net_euclidean_distance,
    }
    distance_and_loss_color_dict = {
        ParameterName.loss: ColorConfig.loss_color,
        ParameterName.distance: ColorConfig.raw_distance_color,
        ParameterName.net_distance: ColorConfig.net_distance_color,
    }
    distance_and_loss_legend_color_dict = {
        **distance_and_loss_color_dict,
        ParameterName.net_distance: ColorConfig.net_distance_legend_color,
    }
    default_flux_error_bar_color = ColorConfig.averaged_solution_text_color

    def select_average_solution_name_color_dict(
            self, with_reoptimization=False, with_traditional_method=False,
            different_simulated_data=False, with_simulated_mid_data=False, wrap_name=True, traditional_double_wrap=True):
        if wrap_name:
            selected_solution_str = CommonFigureString.selected_solution_wrap
            averaged_solution_str = CommonFigureString.averaged_solution_wrap
            reoptimized_solution_str = CommonFigureString.reoptimized_solution_wrap
            if traditional_double_wrap:
                traditional_solution_str = CommonFigureString.traditional_solution_double_wrap
            else:
                traditional_solution_str = CommonFigureString.traditional_solution_wrap
        else:
            selected_solution_str = CommonFigureString.selected_solution
            averaged_solution_str = CommonFigureString.averaged_solution
            reoptimized_solution_str = CommonFigureString.reoptimized_solution
            traditional_solution_str = CommonFigureString.traditional_solution
        different_simulated_solution_distance_wrap_str = CommonFigureString.different_simulated_solution_distance_wrap

        base_name_dict = {
            ParameterName.selected: selected_solution_str,
            ParameterName.averaged: averaged_solution_str,
        }
        base_color_dict = {
            ParameterName.selected: ColorConfig.selected_solution_text_color,
            ParameterName.averaged: ColorConfig.averaged_solution_text_color,
        }
        if with_reoptimization:
            base_name_dict = {
                **base_name_dict,
                ParameterName.optimized: reoptimized_solution_str,
            }
            base_color_dict = {
                **base_color_dict,
                ParameterName.optimized: ColorConfig.reoptimized_solution_text_color,
            }
        if with_traditional_method:
            base_name_dict = {
                ParameterName.traditional: traditional_solution_str,
                **base_name_dict,
            }
            base_color_dict = {
                ParameterName.traditional: ColorConfig.different_simulated_distance,
                **base_color_dict,
            }
        if different_simulated_data:
            base_name_dict = {
                ParameterName.different_simulated_distance: different_simulated_solution_distance_wrap_str,
                **base_name_dict,
            }
            base_color_dict = {
                ParameterName.different_simulated_distance: ColorConfig.different_simulated_distance,
                **base_color_dict,
            }
        if with_simulated_mid_data:
            base_name_dict = {
                **base_name_dict,
                ParameterName.simulated: CommonFigureString.simulated_data,
            }
            base_color_dict = {
                **base_color_dict,
                ParameterName.simulated: ColorConfig.reoptimized_solution_color,
            }
        return base_name_dict, base_color_dict



class BasicFigureData(RawBasicFigureData):
    data_direct = Direct.figure_raw_data_direct


class FigureDataKeywords(object):
    loss_data_comparison = 'loss_data_comparison'
    embedding_visualization = 'embedding_visualization'
    time_data_distribution = 'time_data_distribution'
    best_solution = 'best_solution'


class ProtocolSearchingMaterials(object):
    all_data_target_optimization_size = 20000
    all_data_target_selection_size = 100
    all_data_target_selection_ratio = all_data_target_selection_size / all_data_target_optimization_size

    experimental_data_target_optimization_size = 20000
    experimental_data_target_selection_size = 100
    experimental_data_target_selection_ratio = experimental_data_target_selection_size / \
        experimental_data_target_optimization_size

    all_data_text_comment_config_dict = {
        ParameterName.reaction_flux_num: 85,
        ParameterName.total_flux_num: 85,
        ParameterName.total_mid_num: 42,
        ParameterName.mid_metabolite_num: 42,
    }
    experimental_data_text_comment_config_dict = {
        ParameterName.reaction_flux_num: 85,
        ParameterName.total_flux_num: 105,
        ParameterName.total_mid_num: 22,
        ParameterName.mid_metabolite_num: 42,
    }


class MetabolicNetworkConfig(object):
    common_experimental_mid_metabolite_set = {
        'GLC_c', 'FBP_c', 'DHAP_c', 'GAP_c', '3PG_c', 'PEP_c',
        'PYR_c', 'PYR_m', 'LAC_c', 'ALA_c', 'ERY4P_c',
        'CIT_m', 'MAL_m', 'AKG_m', 'SUC_m', 'ASP_m',
        'SER_c', 'GLY_c', 'ASP_c', 'CIT_c', 'MAL_c',
        'GLU_m', 'GLN_m', 'GLU_c', 'GLN_c', 'AKG_c', 'RIB5P_c'
    }
    common_experimental_mixed_mid_metabolite_set = {
        'PYR_c', 'PYR_m', 'CIT_m', 'CIT_c', 'MAL_m', 'MAL_c',
        'GLU_m', 'GLU_c', 'GLN_m', 'GLN_c', 'ASP_m', 'ASP_c',
        'AKG_m', 'AKG_c',
    }
    common_biomass_metabolite_set = {
        'ALA_c', 'RIB5P_c', 'GLY_c', 'SER_c', 'ASP_c',
        'ACCOA_c', 'GLU_c', 'GLN_c',
    }
    common_input_metabolite_set = {
        'GLC_e', 'GLN_e', 'ASP_e', 'SER_e', 'GLY_e', 'ALA_e', 'LAC_e',
    }
    infusion_input_metabolite_set = {
        'GLC_e', 'GLC_unlabelled_e', 'GLN_e', 'ASP_e', 'SER_e', 'GLY_e', 'ALA_e', 'LAC_e',
    }
    common_c13_labeling_metabolite_set = {
        'GLC_e',
    }
    common_boundary_flux_set = {
        'GLC_input'
    }
    infusion_boundary_flux_set = {
        'GLC_input', 'GLC_unlabelled_input'
    }
    common_diagram_network_setting_dict = {
        ParameterName.input_metabolite_set: common_input_metabolite_set,
        ParameterName.c13_labeling_metabolite_set: common_c13_labeling_metabolite_set,
        ParameterName.mid_data_metabolite_set: common_experimental_mid_metabolite_set,
        ParameterName.mixed_mid_data_metabolite_set:
            common_experimental_mixed_mid_metabolite_set,
        ParameterName.biomass_metabolite_set: common_biomass_metabolite_set,
        ParameterName.boundary_flux_set: common_boundary_flux_set,
        # ParameterName.reaction_raw_value_dict: {'GLC_input': 200},
        ParameterName.reaction_text_dict: {'GLC_input': CommonFigureString.fixed_flux_string_generator(200)},
        ParameterName.reaction_text_config_dict: {ParameterName.font_weight: FontWeight.bold},
    }
    common_data_flux_network_setting_dict = {}
    common_scale = 0.35

    exchange_flux_alpha_dict = {
        ParameterName.alpha: 0.7
    }
    exchange_diagram_network_config = {
        ParameterName.extra_parameter_dict: {
            'CIT_trans': dict(exchange_flux_alpha_dict),
            'AKGMAL_m': dict(exchange_flux_alpha_dict),
            'ASPTA_m': dict(exchange_flux_alpha_dict),
            'ASPTA_c': dict(exchange_flux_alpha_dict),
        }
    }
    normal_network_display_text_dict = {
        'GLC_input': CommonFigureString.glc_input,
        'GLN_input': CommonFigureString.gln_input,
        'LDH_c': 'LDH_c',
        'CS_m': 'CS_m',
        'GAPD_PGK_c': 'GAPD_c',
    }
    exchange_network_display_text_dict = {
        'CIT_trans': CommonFigureString.cma_wrap,
        'AKGMAL_m': CommonFigureString.ama_wrap,
    }


class PHGDHRawMaterials(object):
    diagram_network_config_dict = {
        **MetabolicNetworkConfig.common_diagram_network_setting_dict,
    }
    data_flux_network_setting_dict = {
        **MetabolicNetworkConfig.common_data_flux_network_setting_dict,
        ParameterName.absolute_value_output_value_dict: {
            0: 0.05,
            50: 0.55,
            200: 0.8,
            350: 1,
        }
    }


class BasicFigure(GeneralElements.Figure):
    figure_output_direct = Direct.figure_output_direct
    top_margin_ratio = 0.05
    side_margin_ratio = 0.02
