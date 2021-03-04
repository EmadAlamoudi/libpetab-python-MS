import numpy as np
import pandas as pd

from typing import Dict, List, Optional, Tuple, Union, TypedDict

from .. import problem, measurements, core, conditions
from ..problem import Problem
from ..C import *
from collections.abc import Sequence
from numbers import Number
import warnings

# for typehints
IdsList = List[str]
NumList = List[int]


# also for type hints
class VisDict(TypedDict):
    PLOT_NAME: str
    PLOT_TYPE_SIMULATION: str
    PLOT_TYPE_DATA: str
    X_VALUES: str
    X_OFFSET: List[Number]
    X_LABEL: str
    X_SCALE: str
    Y_VALUES: List[str]
    Y_OFFSET: List[Number]
    Y_LABEL: str
    Y_SCALE: str
    LEGEND_ENTRY: List[Number]
    DATASET_ID: List[str]


class VisualizationSpec_full:
    def __init__(self,
                 conditions_data: pd.DataFrame,
                 exp_data: pd.DataFrame,
                 vis_spec: pd.DataFrame
                 ):
        """
        full visualization specification

        if vis_spec is not provided directly it can be generated from
        dataset_id_list or sim_cond_id_list or sim_cond_num_list or
        observable_id_list or observable_num_list
        # TODO: all of these options should be kept?

        :param exp_data:
        :param conditions_data:
        :param vis_spec:
        """
        # self.measurements = exp_data
        # self.conditions = conditions_data
        self.subplot_vis_specs = []
        # vis spec file + additioal styles/settings ?

        # TODO: vis_spec doesn't need to be extended anymore? will be done in
        #  VisualizationSpec ?

        # get unique plotIDs
        plot_ids = np.unique(vis_spec[PLOT_ID])

        # loop over unique plotIds
        for plot_id in plot_ids:
            # get indices for specific plotId
            ind_plot = (vis_spec[PLOT_ID] == plot_id)
            self.subplot_vis_specs.append(
                VisualizationSpec.from_df(vis_spec[ind_plot]))

    @staticmethod
    def from_dataset_ids(dataset_id_list: Optional[List[IdsList]] = None,
                         plotted_noise: Optional[str] = MEAN_AND_SD
                         ) -> 'VisualizationSpec_full':
        # create vis spec dataframe

        # vis spec that is created for the first plot
        # plotId | datasetId | legendEntry | yValues | plotTypeData
        # plot1  | dataset_1 | dataset_1   |         | plotted_noise
        # plot1  | dataset_2 | dataset_2   |         | plotted_noise


        pass

    @staticmethod
    def from_condition_ids(sim_cond_id_list: Optional[List[IdsList]] = None,
                           plotted_noise: Optional[str] = MEAN_AND_SD
                           ) -> 'VisualizationSpec_full':
        pass

    @staticmethod
    def from_observable_ids(observable_id_list: Optional[List[IdsList]] = None,
                            plotted_noise: Optional[str] = MEAN_AND_SD,
                            ) -> 'VisualizationSpec_full':
        pass


class VisualizationSpec:
    def __init__(self,
                 plot_id: str,
                 plot_settings: VisDict,
                 fig_id: str = 'fig0'
                 ):
        """
        visualization specification for one plot

        :param plot_id:
        :param plot_settings:
        :param fig_id:
        """
        # vis spec file + additioal styles/settings ?
        self.figureId = fig_id
        setattr(self, PLOT_ID, plot_id)
        for key,val in plot_settings.items():
            setattr(self,key,val)
        if PLOT_NAME not in vars(self):
            setattr(self, PLOT_NAME, getattr(self, PLOT_ID))
        if PLOT_TYPE_SIMULATION not in vars(self):
            setattr(self, PLOT_TYPE_SIMULATION, LINE_PLOT)
        if PLOT_TYPE_DATA not in vars(self):
            setattr(self, PLOT_TYPE_DATA, MEAN_AND_SD)
        # TODO datasetId optional so default should be created
        if X_VALUES not in vars(self):
            setattr(self, X_VALUES, TIME)
        if X_OFFSET not in vars(self):
            setattr(self, X_OFFSET, 0)
        if X_LABEL not in vars(self):
            setattr(self, X_LABEL, getattr(self, X_VALUES))

        if X_SCALE not in vars(self):
            setattr(self, X_SCALE, LIN)
        # TODO yValues optional but should be created one level above
        # TODO in docs: yValues list of observables, how default label?
        if Y_LABEL not in vars(self):
            setattr(self, Y_LABEL, 'values')
        if Y_OFFSET not in vars(self):
            setattr(self, Y_OFFSET, 0.)
        if LEGEND_ENTRY not in vars(self):
            setattr(self, LEGEND_ENTRY, getattr(self, DATASET_ID))

    @staticmethod
    def from_df(vis_spec_df: Union[pd.DataFrame, str]) -> \
            List['VisualizationSpec']:
        # check if file path or pd.DataFrame is passed
        if isinstance(vis_spec_df, str):
            vis_spec_df = pd.read_csv(vis_spec_df, sep='\t', index_col=PLOT_ID)
        elif vis_spec_df.index.name != PLOT_ID:
            vis_spec_df.set_index(PLOT_ID, inplace=True)
        uni_plot_ids = vis_spec_df.index.unique().to_list()
        vis_spec_list = []
        # create a VisualizationSpec object for each PlotId
        for plot_id in uni_plot_ids:
            vis_spec_dict = {}
            for col in vis_spec_df:
                print(plot_id, col)
                entry = vis_spec_df.loc[plot_id, col]
                if col in VISUALIZATION_DF_SUBPLOT_LEVEL_COLS:
                    entry = np.unique(entry)
                    if entry.size > 1:
                        warnings.warn(f'For {PLOT_ID} {plot_id} in column '
                                      f'{col} contradictory settings ({entry})'
                                      f'. Proceeding with first entry '
                                      f'({entry[0]}).')
                    entry=entry[0]

                # check if values are allowed
                if col in [Y_SCALE, X_SCALE] and entry not in \
                        OBSERVABLE_TRANSFORMATIONS:
                    raise ValueError(f'{X_SCALE} and {Y_SCALE} have to be '
                                     f'one of the following: '
                                     + ', '.join(OBSERVABLE_TRANSFORMATIONS))
                elif col == PLOT_TYPE_DATA and entry not in \
                        PLOT_TYPES_DATA:
                    raise ValueError(f'{PLOT_TYPE_DATA} has to be one of the '
                                     f'following: '
                                     + ', '.join(PLOT_TYPES_DATA))
                elif col == PLOT_TYPE_SIMULATION and entry not in \
                        PLOT_TYPES_SIMULATION:
                    raise ValueError(f'{PLOT_TYPE_SIMULATION} has to be one of'
                                     f' the following: '
                                     + ', '.join(PLOT_TYPES_DATA))
                # append new entry to dict
                vis_spec_dict[col] = entry
            vis_spec_list.append(VisualizationSpec(plot_id, vis_spec_dict))
        return vis_spec_list


class Figure:
    def __init__(self,
                 conditions_data: Union[str, pd.DataFrame],
                 exp_data: Union[str, pd.DataFrame],
                 simulations: Optional[Union[str, pd.DataFrame]] = None,
                 vis_spec: Optional[Union[str, pd.DataFrame]] = None,  # full vis_spec
                 dataset_ids_per_plot: Optional[List[IdsList]] = None,
                 sim_cond_id_list: Optional[List[IdsList]] = None,
                 sim_cond_num_list: Optional[List[NumList]] = None,
                 observable_id_list: Optional[List[IdsList]] = None,
                 observable_num_list: Optional[List[NumList]] = None,
                 plotted_noise: Optional[str] = MEAN_AND_SD):
        """

        :param vis_spec: the whole vis spec
        :param dataset_ids_per_plot
            e.g. dataset_ids_per_plot = [['dataset_1', 'dataset_2'],
                                         ['dataset_1', 'dataset_4', 'dataset_5']]
        :param plotted_noise
            only in addition to one of the lists with ids or numbers
        """
        # TODO: rename this class?
        if isinstance(conditions_data, str):
            conditions_data = conditions.get_condition_df(conditions_data)

        # import from file in case experimental data is provided in file
        if isinstance(exp_data, str):
            exp_data = measurements.get_measurement_df(exp_data)

        if vis_spec:
            self.vis_spec = VisualizationSpec_full(exp_data, conditions_data,
                                                   vis_spec)
        elif dataset_ids_per_plot:
            self.vis_spec = VisualizationSpec_full.from_dataset_ids(
                dataset_ids_per_plot, plotted_noise)
        elif sim_cond_id_list:
            pass
        elif observable_id_list:
            pass
        else:
            raise TypeError("Not enough arguments. Either vis_spec should be "
                            "provided or one of the following lists: "
                            "dataset_ids_per_plot, sim_cond_id_list, "
                            "sim_cond_num_list, observable_id_list, "
                            "observable_num_list")
        self.data_provider = DataProvider(conditions_data, exp_data,
                                          simulations)
        self.subplots = []  # list of SinglePlots

        for subplot_vis_spec in self.vis_spec.subplot_vis_specs:
            self._add_subplot(subplot_vis_spec)

    @property
    def num_subplots(self) -> int:
        return len(self.subplots)

    def _add_subplot(self,
                     subplot_vis_spec):
        measurements_to_plot, simulation_to_plot = \
            self.data_provider.select_by_vis_spec(subplot_vis_spec)

        if subplot_vis_spec.plotTypeSimulation == 'BarPlot':
            subplot = BarPlot(subplot_vis_spec, measurements_to_plot,
                              simulation_to_plot)
        elif subplot_vis_spec.plotTypeSimulation == 'ScatterPlot':
            subplot = ScatterPlot(subplot_vis_spec, measurements_to_plot,
                                  simulation_to_plot)
        else:
            subplot = LinePlot(subplot_vis_spec, measurements_to_plot,
                               simulation_to_plot)

        self.subplots.append(subplot)


class DataToPlot:
    """
    data for one individual line
    """
    def __init__(self):
        # so far created based on the dataframe returned by get_data_to_plot
        self.xValues = []  # what is in the condition_ids parameter of get_data_to_plot
        self.mean = []  # means of replicates
        self.noise_model = None
        self.sd = []
        self.sem = []  # standard error of mean
        self.repl = []  # single replicates


class DataProvider:
    """
    Handles data selection
    """
    def __init__(self,
                 exp_conditions: Union[str, pd.DataFrame],
                 measurements: Union[str, pd.DataFrame],
                 simulations: Optional[Union[str, pd.DataFrame]] = None):
        self.conditions = exp_conditions
        self.measurements = measurements
        self.simulations = simulations
        # validation of dfs?
        # extending
        pass

    def check_datarequest_consistency(self):
        # check if data request is meaningful
        # check_vis_spec_consistency functionality
        pass

    def group_by_measurement(self):
        pass

    def select_by_dataset_ids(self, dataset_ids_per_plot: IdsList
                              ) -> List[Tuple[DataToPlot, DataToPlot]]:
        """

        :param dataset_ids_per_plot:
        :return:

        datasets = [['dataset_1', 'dataset_2'],
                   ['dataset_1', 'dataset_4', 'dataset_5']]
        """
        pass

    def select_by_condition_ids(self, condition_ids: IdsList):
        pass

    def select_by_condition_numbers(self, condition_nums: NumList):
        pass

    def select_by_observable_ids(self, observable_ids: IdsList):
        pass

    def select_by_observable_numbers(self, observable_nums: NumList):
        pass

    def select_by_vis_spec(self, vis_spec: VisualizationSpec
                           ) -> Tuple[DataToPlot, DataToPlot]:
        # TODO: maybe other select_by aren't needed
        measurements_to_plot = None
        simulations_to_plot = None
        return measurements_to_plot, simulations_to_plot


class SinglePlot:
    def __init__(self,
                 plot_spec,
                 measurements_to_plot: Optional[DataToPlot],
                 simulations_to_plot: Optional[DataToPlot]):
        self.id = None
        self.plot_spec = plot_spec  # dataframe, vis spec of a single plot

        if measurements_to_plot is None and simulations_to_plot is None:
            raise TypeError('Not enough arguments. Either measurements_to_plot '
                            'or simulations_to_plot should be provided.')
        self.measurements_to_plot = measurements_to_plot
        self.simulations_to_plot = simulations_to_plot

        self.xValues = plot_spec[X_VALUES]

        # parameters of a specific plot
        self.title = ''
        self.xLabel = X_LABEL
        self.yLabel = Y_LABEL

    def matches_plot_spec(self,
                          df: pd.DataFrame,
                          col_id: str,
                          x_value: Union[float, str],
                          plot_spec: pd.Series) -> pd.Series:
        """
        constructs an index for subsetting of the dataframe according to what is
        specified in plot_spec.

        Parameters:
            df:
                pandas data frame to subset, can be from measurement file or
                simulation file
            col_id:
                name of the column that will be used for indexing in x variable
            x_value:
                subsetted x value
            plot_spec:
                visualization spec from the visualization file

        Returns:
            index:
                Boolean series that can be used for subsetting of the passed
                dataframe
        """

        subset = (
                (df[col_id] == x_value) &
                (df[DATASET_ID] == plot_spec[DATASET_ID])
        )
        if plot_spec[Y_VALUES] == '':
            if len(df.loc[subset, OBSERVABLE_ID].unique()) > 1:
                ValueError(
                    f'{Y_VALUES} must be specified in visualization table if '
                    f'multiple different observables are available.'
                )
        else:
            subset &= (df[OBSERVABLE_ID] == plot_spec[Y_VALUES])
        return subset

    def get_measurements_to_plot(self) -> Optional[pd.DataFrame]:

        # get datasetID and independent variable of first entry of plot1
        dataset_id = self.plot_spec[DATASET_ID]
        indep_var = self.xValues

        # define index to reduce exp_data to data linked to datasetId
        ind_dataset = self.measurements_df[DATASET_ID] == dataset_id

        # gather simulationConditionIds belonging to datasetId
        uni_condition_id, uind = np.unique(
            self.measurements_df[ind_dataset][SIMULATION_CONDITION_ID],
            return_index=True)
        # keep the ordering which was given by user from top to bottom
        # (avoid ordering by names '1','10','11','2',...)'
        uni_condition_id = uni_condition_id[np.argsort(uind)]
        col_name_unique = SIMULATION_CONDITION_ID

        # Case separation of independent parameter: condition, time or custom
        if indep_var == TIME:
            # obtain unique observation times
            uni_condition_id = np.unique(measurements_df[ind_dataset][TIME])
            col_name_unique = TIME

        # create empty dataframe for means and SDs
        meas_to_plot = pd.DataFrame(
            columns=['mean', 'noise_model', 'sd', 'sem', 'repl'],
            index=uni_condition_id
        )
        for var_cond_id in uni_condition_id:

            # TODO (#117): Here not the case: So, if entries in measurement file:
            #  preequCondId, time, observableParams, noiseParams,
            #  are not the same, then  -> differ these data into
            #  different groups!
            # now: go in simulationConditionId, search group of unique
            # simulationConditionId e.g. rows 0,6,12,18 share the same
            # simulationCondId, then check if other column entries are the same
            # (now: they are), then take intersection of rows 0,6,12,18 and checked
            # other same columns (-> now: 0,6,12,18) and then go on with code.
            # if there is at some point a difference in other columns, say e.g.
            # row 12,18 have different noiseParams than rows 0,6, the actual code
            # would take rows 0,6 and forget about rows 12,18

            # compute mean and standard deviation across replicates
            subset = matches_plot_spec(self.measurements_df,
                                       col_id, var_cond_id,
                                       self.plot_spec)
            data_measurements = self.measurements_df.loc[
                subset,
                MEASUREMENT
            ]

            meas_to_plot.at[var_cond_id, 'mean'] = np.mean(data_measurements)
            meas_to_plot.at[var_cond_id, 'sd'] = np.std(data_measurements)

            if (plot_spec.plotTypeData == PROVIDED) & sum(subset):
                if len(self.measurements_df.loc[subset, NOISE_PARAMETERS].unique()) > 1:
                    raise NotImplementedError(
                        f"Datapoints with inconsistent {NOISE_PARAMETERS} is "
                        f"currently not implemented. Stopping.")
                tmp_noise = self.measurements_df.loc[subset, NOISE_PARAMETERS].values[0]
                if isinstance(tmp_noise, str):
                    raise NotImplementedError(
                        "No numerical noise values provided in the measurement "
                        "table. Stopping.")
                if isinstance(tmp_noise, Number) or tmp_noise.dtype == 'float64':
                    meas_to_plot.at[var_cond_id, 'noise_model'] = tmp_noise

            # standard error of mean
            meas_to_plot.at[var_cond_id, 'sem'] = \
                np.std(data_measurements) / np.sqrt(len(data_measurements))

            # single replicates
            meas_to_plot.at[var_cond_id, 'repl'] = \
                data_measurements

        return meas_to_plot

    def get_simulations_to_plot(self) -> Optional[pd.DataFrame]:
        if self.simulations_df is None:
            return None

         # get datasetID and independent variable of first entry of plot1
        dataset_id = self.plot_spec[DATASET_ID]
        indep_var = self.xValues

        # define index to reduce exp_data to data linked to datasetId
        ind_dataset = self.simulations_df[DATASET_ID] == dataset_id

        # gather simulationConditionIds belonging to datasetId
        uni_condition_id, uind = np.unique(
            self.simulations_df[ind_dataset][SIMULATION_CONDITION_ID],
            return_index=True)
        # keep the ordering which was given by user from top to bottom
        # (avoid ordering by names '1','10','11','2',...)'
        uni_condition_id = uni_condition_id[np.argsort(uind)]
        col_name_unique = SIMULATION_CONDITION_ID

        # Case separation of independent parameter: condition, time or custom
        if indep_var == TIME:
            # obtain unique observation times
            uni_condition_id = np.unique(self.simulations_df_df[ind_dataset][TIME])
            col_name_unique = TIME

        # create empty dataframe for means and SDs
        sim_to_plot = pd.DataFrame(
            columns=['sim'],
            index=uni_condition_id
        )
        for var_cond_id in uni_condition_id:

            simulation_measurements = self.simulations_df.loc[
                matches_plot_spec(self.simulations_df, col_id, var_cond_id,
                                  self.plot_spec),
                SIMULATION
            ]
            sim_to_plot.at[var_cond_id, 'sim'] = np.mean(
                simulation_measurements
            )
        return sim_to_plot


class LinePlot(SinglePlot):
    def __init__(self,
                 vis_spec,
                 measurements_df: Optional[DataToPlot],
                 simulations_df: Optional[DataToPlot]):
        super().__init__(vis_spec, measurements_df, simulations_df)


class BarPlot(SinglePlot):
    def __init__(self,
                 vis_spec,
                 measurements_df: Optional[DataToPlot],
                 simulations_df: Optional[DataToPlot]):
        super().__init__(vis_spec, measurements_df, simulations_df)


class ScatterPlot(SinglePlot):
    def __init__(self,
                 vis_spec,
                 measurements_df: Optional[DataToPlot],
                 simulations_df: Optional[DataToPlot]):
        super().__init__(vis_spec, measurements_df, simulations_df)