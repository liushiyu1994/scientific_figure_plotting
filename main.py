import enum
import argparse


class FigureName(enum.Enum):
    figure_1 = '1'


def arg_setting(figure_parser):
    def figure_running(args):
        figure_parser_main(figure_parser, args)

    # figure_parser = subparsers.add_parser('figure', help='Run figure generation functions')
    figure_name_display = '{}'.format(',  '.join([figure_name.value for figure_name in FigureName]))
    figure_parser.add_argument(
        'figure_name', nargs='?', type=str,
        help='The figure needs to plot', metavar=figure_name_display)
    figure_parser.add_argument(
        '-s', '--svg', action='store_true', default=False,
        help='Store the figure in SVG format.'
    )
    figure_parser.add_argument(
        '-b', '--background', action='store_true', default=False,
        help='Add white background in SVG format.'
    )
    figure_parser.set_defaults(func=figure_running)


def figure_parser_main(figure_parser=None, args=None):
    figure_name = args.figure_name
    if figure_name is None:
        figure_parser.print_help()
    else:
        from example_figures.figure_content.figure_content_loader import figure_plotting_main
        figure_plotting_main(figure_name, output_svg=args.svg, background=args.background)


def main():
    parser = argparse.ArgumentParser(
        prog='Figure', description='Figure plotting package')
    arg_setting(parser)
    args = parser.parse_args()
    figure_parser_main(parser, args)


if __name__ == '__main__':
    main()

