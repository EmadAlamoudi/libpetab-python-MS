import warnings
from os import path
from tempfile import TemporaryDirectory
import pandas as pd
import pytest
from petab.C import *
from petab import Problem
# from petab.visualize import (MPLPlotter)
from petab.visualize.plotter import (MPLPlotter)
from petab.visualize.plotting import VisualizationSpec, Figure, VisSpecParser

import matplotlib.pyplot as plt


@pytest.fixture
def data_file_Fujita():
    return "doc/example/example_Fujita/Fujita_measurementData.tsv"


@pytest.fixture
def condition_file_Fujita():
    return "doc/example/example_Fujita/Fujita_experimentalCondition.tsv"


@pytest.fixture
def data_file_Fujita_wrongNoise():
    return "doc/example/example_Fujita/Fujita_measurementData_wrongNoise.tsv"


@pytest.fixture
def data_file_Fujita_nanData():
    return "doc/example/example_Fujita/Fujita_measurementData_nanData.tsv"


@pytest.fixture
def simu_file_Fujita():
    return "doc/example/example_Fujita/Fujita_simulatedData.tsv"


@pytest.fixture
def data_file_Fujita_minimal():
    return "doc/example/example_Fujita/Fujita_measurementData_minimal.tsv"


@pytest.fixture
def visu_file_Fujita_small():
    return "doc/example/example_Fujita/Fujita_visuSpec_small.tsv"


@pytest.fixture
def visu_file_Fujita_wo_dsid():
    return "doc/example/example_Fujita/visuSpecs/Fujita_visuSpec_1.tsv"


@pytest.fixture
def visu_file_Fujita_minimal():
    return "doc/example/example_Fujita/visuSpecs/Fujita_visuSpec_mandatory.tsv"


@pytest.fixture
def visu_file_Fujita_empty():
    return "doc/example/example_Fujita/visuSpecs/Fujita_visuSpec_empty.tsv"


@pytest.fixture
def data_file_Isensee():
    return "doc/example/example_Isensee/Isensee_measurementData.tsv"


@pytest.fixture
def condition_file_Isensee():
    return "doc/example/example_Isensee/Isensee_experimentalCondition.tsv"


@pytest.fixture
def vis_spec_file_Isensee():
    return "doc/example/example_Isensee/Isensee_visualizationSpecification.tsv"


@pytest.fixture
def simulation_file_Isensee():
    return "doc/example/example_Isensee/Isensee_simulationData.tsv"


def test_visualization_with_dataset_list(data_file_Isensee,
                                         condition_file_Isensee,
                                         simulation_file_Isensee):
    datasets = [['JI09_150302_Drg345_343_CycNuc__4_ABnOH_and_ctrl',
                 'JI09_150302_Drg345_343_CycNuc__4_ABnOH_and_Fsk'],
                ['JI09_160201_Drg453-452_CycNuc__ctrl',
                 'JI09_160201_Drg453-452_CycNuc__Fsk',
                 'JI09_160201_Drg453-452_CycNuc__Sp8_Br_cAMPS_AM']]

    # TODO: is condition_file needed here
    vis_spec_parcer = VisSpecParser(condition_file_Isensee, data_file_Isensee)
    figure, dataprovider = vis_spec_parcer.parse_from_dataset_ids(datasets)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()  # assemble actual plot

    vis_spec_parcer = VisSpecParser(condition_file_Isensee, data_file_Isensee,
                                    simulation_file_Isensee)
    figure, dataprovider = vis_spec_parcer.parse_from_dataset_ids(datasets)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()


def test_visualization_without_datasets(data_file_Fujita,
                                        condition_file_Fujita,
                                        simu_file_Fujita):
    sim_cond_num_list = [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5]]
    sim_cond_id_list = [['model1_data1'], ['model1_data2', 'model1_data3'],
                        ['model1_data4', 'model1_data5'], ['model1_data6']]
    observable_num_list = [[0], [1], [2], [0, 2], [1, 2]]
    observable_id_list = [['pS6_tot'], ['pEGFR_tot'], ['pAkt_tot']]

    vis_spec_parcer = VisSpecParser(condition_file_Fujita, data_file_Fujita)
    figure, dataprovider = vis_spec_parcer.parse_from_conditions_list(
        sim_cond_id_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    figure, dataprovider = vis_spec_parcer.parse_from_conditions_list(
        sim_cond_num_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    figure, dataprovider = vis_spec_parcer.parse_from_observables_list(
        observable_id_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    figure, dataprovider = vis_spec_parcer.parse_from_observables_list(
        observable_num_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    # with simulations
    vis_spec_parcer = VisSpecParser(condition_file_Fujita, data_file_Fujita,
                                    simu_file_Fujita)
    figure, dataprovider = vis_spec_parcer.parse_from_conditions_list(
        sim_cond_id_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    figure, dataprovider = vis_spec_parcer.parse_from_conditions_list(
        sim_cond_num_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    figure, dataprovider = vis_spec_parcer.parse_from_observables_list(
        observable_id_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    figure, dataprovider = vis_spec_parcer.parse_from_observables_list(
        observable_num_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    # TODO: with provided noise


def test_visualization_only_simulations(condition_file_Fujita,
                                        simu_file_Fujita):
    sim_cond_num_list = [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5]]
    sim_cond_id_list = [['model1_data1'], ['model1_data2', 'model1_data3'],
                        ['model1_data4', 'model1_data5'], ['model1_data6']]
    observable_num_list = [[0], [1], [2], [0, 2], [1, 2]]
    observable_id_list = [['pS6_tot'], ['pEGFR_tot'], ['pAkt_tot']]

    vis_spec_parcer = VisSpecParser(condition_file_Fujita,
                                    sim_data=simu_file_Fujita)
    figure, dataprovider = vis_spec_parcer.parse_from_conditions_list(
        sim_cond_id_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    figure, dataprovider = vis_spec_parcer.parse_from_conditions_list(
        sim_cond_num_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    figure, dataprovider = vis_spec_parcer.parse_from_observables_list(
        observable_id_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    figure, dataprovider = vis_spec_parcer.parse_from_observables_list(
        observable_num_list)
    plotter = MPLPlotter(figure, dataprovider)
    plotter.generate_figure()

    # TODO: with provided noise


def test_VisualizationSpec():
    test_spec = {PLOT_NAME:'test_plot',
                 PLOT_TYPE_SIMULATION: LINE_PLOT,
                 PLOT_TYPE_DATA: MEAN_AND_SD,
                 X_VALUES: 'test_xValues',
                 X_SCALE: LOG,
                 Y_SCALE: LIN,
                 LEGEND_ENTRY: ['test_legend'],
                 DATASET_ID: ['test_dataset_id'],
                 Y_VALUES: ['test_yValue'],
                 Y_OFFSET: [0.],
                 X_OFFSET: [0.],
                 X_LABEL: 'test_xLabel',
                 Y_LABEL: 'test_yLabel'
                  }
    assert {**{'figureId': 'fig0', PLOT_ID: 'plot0'}, **test_spec} == \
        VisualizationSpec(plot_id='plot0', plot_settings=test_spec).__dict__


def test_VisualizationSpec_from_df():
    dir_path = path.dirname(path.realpath(__file__))
    example_path = f'{dir_path}/../doc/example/example_Isensee/' \
                   f'Isensee_visualizationSpecification.tsv'
    VisualizationSpec.from_df(example_path)
    VisualizationSpec.from_df(pd.read_csv(example_path, sep='\t'))
    # TODO some assertion
    # TODO check warning and error
    pass
