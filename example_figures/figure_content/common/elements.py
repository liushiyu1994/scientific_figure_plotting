from .config import GeneralElements
from ..figure_elements.complex_figure import (
    DataAcquisitionDiagram, OptimizationDiagram, TimeLossStack, ProtocolDiagram,
    RandomOptimizedLossDistanceWithDiagramComparison,
    OptimizedAllFluxComparisonBarDataFigure,
    FluxSloppinessDiagram,
)


class Elements(GeneralElements):
    DataAcquisitionDiagram = DataAcquisitionDiagram
    OptimizationDiagram = OptimizationDiagram
    TimeLossStack = TimeLossStack
    ProtocolDiagram = ProtocolDiagram
    RandomOptimizedLossDistanceWithDiagramComparison = RandomOptimizedLossDistanceWithDiagramComparison
    OptimizedAllFluxComparisonBarDataFigure = OptimizedAllFluxComparisonBarDataFigure
    FluxSloppinessDiagram = FluxSloppinessDiagram
