from figure_plotting_package.main import draw_figure


def test_figure_content_loader(figure_direct, figure_name):
    import importlib
    current_file_name = f'figure_{figure_name}'
    current_direct = __name__[:__name__.rindex('.')]
    current_file_path = f'{current_direct}.{figure_direct}.{current_file_name}'
    imported_lib = importlib.import_module(current_file_path)
    Figure = imported_lib.Figure
    return Figure


def figure_plotting_main(figure_name, output_svg=False, background=False):
    figure_obj = test_figure_content_loader('figures', figure_name)()
    draw_figure(figure_obj, output_svg, background)
