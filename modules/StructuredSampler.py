import pandas as pd
import numpy as np


class StructuredSampler:
    """
    A class used to sample a structured subset from a DataFrame based on given parameters.

    Attributes:
        df (pd.DataFrame): The DataFrame to sample from.
        sample_size (int): The desired sample size.
        identifier_col (str): The column used for sorting the DataFrame.
        structure_parameters (list): List of columns used to define the structure.
    """

    def __init__(self,
                 df: pd.DataFrame,
                 sample_size: int,
                 identifier_col: str,
                 structure_parameters: list):
        """
        Initializes the StructuredSampler with the DataFrame and sampling parameters.

        Args:
            df (pd.DataFrame): The DataFrame to sample from.
            sample_size (int): The desired sample size.
            identifier_col (str): The column used for sorting the DataFrame.
            structure_parameters (list): List of columns used to define the structure.
        """
        self.df_cols = df.columns.to_list()
        self.sample_size = sample_size
        self.structure_parameters = structure_parameters

        if identifier_col in self.df_cols:
            self.df = df.sort_values(identifier_col)
        else:
            self.df = df.sort_index()

        self.population_size = self.df.shape[0]

        if self.sample_size > self.population_size:
            warning_message_size = '''
            The sample size is greater than the Dataframe size. Change it.
            '''
            return print(warning_message_size)

        available_cols = [col for col in self.df_cols if col != identifier_col]

        if set(self.structure_parameters).issubset(available_cols) == False:
            warning_message_parameters = '''
            Verify structure parameter(s).
            '''
            return print(warning_message_parameters)
        else:
            self.structure_parameters = self.structure_parameters

    def working_pivot_df(self):
        """
        Creates a pivot table with counts, weights, and sample sizes by 
        structure parameters.

        Returns:
            pd.DataFrame: The pivot table with counts and calculated weights 
            and sample sizes.
        """
        working_pivot_df = self.df.groupby(
            self.structure_parameters).size().reset_index(name='Count')
        for column in working_pivot_df.columns:
            if column == 'Count':
                weight_column_name = f'Weight(%)'
                sample_size_col_name = f'Sample_size_by_weight'

                working_pivot_df[weight_column_name] = np.round(
                    (working_pivot_df[column] / self.population_size) * 100, 4)

                working_pivot_df[sample_size_col_name] = np.round(
                    (working_pivot_df[column] / self.population_size
                     ) * self.sample_size).astype(int)

        return working_pivot_df

    def prestructure_sampling_df(self):
        """
        Creates the initial sample DataFrame before adjusting for the actual 
        sample size difference.

        Returns:
            pd.DataFrame: The pre-structured sample DataFrame.
        """
        working_pivot_df = self.working_pivot_df()
        prestructure_sampling_df = pd.DataFrame(columns=self.df_cols)
        sub_df = self.df.copy()
        for _, row in working_pivot_df.iterrows():
            temporal_indices_list = []
            temporal_sample_size = int(row['Sample_size_by_weight'])

            filtered_working_pivot_df = sub_df.loc[(
                sub_df[self.structure_parameters] ==
                row[self.structure_parameters]).all(axis=1)]

            incomplete_stucture_sample_rows = filtered_working_pivot_df.sample(
                n=temporal_sample_size)

            prestructure_sampling_df = pd.concat(
                [prestructure_sampling_df, incomplete_stucture_sample_rows])

            temporal_indices_list.extend(
                incomplete_stucture_sample_rows.index.tolist())

        return prestructure_sampling_df

    def original_without_prestructure(self):
        """
        Creates a DataFrame excluding the pre-structured sample rows.

        Returns:
            pd.DataFrame: The DataFrame excluding the pre-structured sample 
            rows.
        """
        working_pivot_df = self.working_pivot_df()
        sub_df = self.df.copy()
        for _, row in working_pivot_df.iterrows():
            temporal_indices_list = []
            temporal_sample_size = int(row['Sample_size_by_weight'])

            filtered_working_pivot_df = sub_df.loc[(
                sub_df[self.structure_parameters] ==
                row[self.structure_parameters]).all(axis=1)]

            incomplete_stucture_sample_rows = filtered_working_pivot_df.sample(
                n=temporal_sample_size)

            temporal_indices_list.extend(
                incomplete_stucture_sample_rows.index.tolist())

            sub_df = sub_df.drop(temporal_indices_list)
        original_without_prestructure = sub_df
        return original_without_prestructure

    def actual_vs_sample_size_difference(self):
        """
        Calculates the difference between the actual and desired sample size.

        Returns:
            int: The difference between the actual and desired sample size.
        """
        prestructure_sampling_df = self.prestructure_sampling_df()
        actual_vs_sample_size_difference = (prestructure_sampling_df.shape[0]
                                            - self.sample_size)
        return actual_vs_sample_size_difference

    def auxiliar_df_ascending(self):
        """
        Creates an auxiliary DataFrame sorted in ascending order by sample 
        size by weight.

        Returns:
            pd.DataFrame: The auxiliary DataFrame sorted in ascending order.
        """
        ascending_auxiliar_df = self.working_pivot_df()[
            'Sample_size_by_weight']
        ascending_auxiliar_df = ascending_auxiliar_df.value_counts(
        ).sort_index().reset_index()
        ascending_auxiliar_df.columns = ['Sample_size_by_weight', 'Count']
        auxiliar_df_ascending = ascending_auxiliar_df
        return auxiliar_df_ascending

    def auxiliar_df_descending(self):
        """
        Creates an auxiliary DataFrame sorted in descending order by sample 
        size by weight.

        Returns:
            pd.DataFrame: The auxiliary DataFrame sorted in descending order.
        """
        auxiliar_df_ascending = self.auxiliar_df_ascending()
        auxiliar_df_descending = auxiliar_df_ascending.sort_values(
            'Sample_size_by_weight', ascending=False)
        return auxiliar_df_descending

    def __get_sub_df_ascending_auxiliar__(self,
                                          auxiliar_df_ascending,
                                          actual_vs_sample_size_difference):
        """
        Creates a subset of the ascending auxiliary DataFrame until the 
        cumulative count reaches the sample size difference.

        Args:
            auxiliar_df_ascending (pd.DataFrame): The ascending auxiliary 
            DataFrame.
            actual_vs_sample_size_difference (int): The difference between the 
            actual and desired sample size.

        Returns:
            pd.DataFrame: The subset of the ascending auxiliary DataFrame.
        """
        sub_df_ascending_auxiliar = pd.DataFrame(
            columns=auxiliar_df_ascending.columns)
        temporal_ascending_auxiliar_count = 0

        for _, row in auxiliar_df_ascending.iterrows():
            count = row['Count']
            temporal_ascending_auxiliar_count += count

            sub_df_ascending_auxiliar = pd.concat(
                [sub_df_ascending_auxiliar, row.to_frame().T])

            if temporal_ascending_auxiliar_count >= abs(actual_vs_sample_size_difference):
                break

        sub_df_ascending_auxiliar = sub_df_ascending_auxiliar.reset_index(
            drop=True)
        return sub_df_ascending_auxiliar

    def __get_ascending_filtered_working_pivot__(self,
                                                 working_pivot_df,
                                                 values_ascending_filter,
                                                 actual_vs_sample_size_difference):
        """
        Filters the working pivot DataFrame based on the ascending filter 
        values.

        Args:
            working_pivot_df (pd.DataFrame): The working pivot DataFrame.
            values_ascending_filter (list): The list of ascending filter 
            values.
            actual_vs_sample_size_difference (int): The difference between the 
            actual and desired sample size.

        Returns:
            pd.DataFrame: The filtered working pivot DataFrame.
        """
        ascending_filtered_working_pivot = working_pivot_df[
            working_pivot_df['Sample_size_by_weight'].isin(
                values_ascending_filter)
        ].sample(n=abs(actual_vs_sample_size_difference))
        return ascending_filtered_working_pivot

    def __get_to_fill_ascending_working_pivot__(self,
                                                ascending_filtered_working_pivot,
                                                original_without_prestructure):
        """
        Creates a DataFrame with rows to be added to the pre-structured sample 
        to achieve the desired sample size.

        Args:
            ascending_filtered_working_pivot (pd.DataFrame): The filtered 
            working pivot DataFrame.
            original_without_prestructure (pd.DataFrame): The DataFrame 
            excluding the pre-structured sample rows.

        Returns:
            pd.DataFrame: The DataFrame with rows to be added.
        """
        to_fill_ascending_working_pivot = pd.DataFrame()

        for _, row in ascending_filtered_working_pivot.iterrows():
            temporal_fill = original_without_prestructure.loc[
                (original_without_prestructure[self.structure_parameters]
                 == row[self.structure_parameters]).all(axis=1)
            ].sample(n=1)

            to_fill_ascending_working_pivot = pd.concat(
                [to_fill_ascending_working_pivot, temporal_fill])

        return to_fill_ascending_working_pivot

    def __structured_sample_negative_difference__(self):
        """
        Adjusts the pre-structured sample by adding rows to match the desired 
        sample size.

        Returns:
            pd.DataFrame: The adjusted structured sample DataFrame.
        """
        prestructure_sampling_df = self.prestructure_sampling_df()
        original_without_prestructure = self.original_without_prestructure()
        actual_vs_sample_size_difference = self.actual_vs_sample_size_difference()
        auxiliar_df_ascending = self.auxiliar_df_ascending()
        working_pivot_df = self.working_pivot_df()

        sub_df_ascending_auxiliar = self.__get_sub_df_ascending_auxiliar__(
            auxiliar_df_ascending, actual_vs_sample_size_difference)
        values_ascending_filter = sub_df_ascending_auxiliar['Sample_size_by_weight'].tolist(
        )
        ascending_filtered_working_pivot = self.__get_ascending_filtered_working_pivot__(
            working_pivot_df, values_ascending_filter, actual_vs_sample_size_difference)
        to_fill_ascending_working_pivot = self.__get_to_fill_ascending_working_pivot__(
            ascending_filtered_working_pivot, original_without_prestructure)

        structured_sampled_df = pd.concat(
            [prestructure_sampling_df, to_fill_ascending_working_pivot])
        return structured_sampled_df

    def __get_sub_df_descending_auxiliar__(self,
                                           auxiliar_df_descending,
                                           actual_vs_sample_size_difference):
        """
        Creates a subset of the descending auxiliary DataFrame until the 
        cumulative count reaches the sample size difference.

        Args:
            auxiliar_df_descending (pd.DataFrame): The descending auxiliary 
            DataFrame.
            actual_vs_sample_size_difference (int): The difference between the 
            actual and desired sample size.

        Returns:
            pd.DataFrame: The subset of the descending auxiliary DataFrame.
        """
        sub_df_descending_auxiliar = pd.DataFrame(
            columns=auxiliar_df_descending.columns)
        temporal_descending_auxiliar_count = 0

        for _, row in auxiliar_df_descending.iterrows():
            count = row['Count']
            temporal_descending_auxiliar_count += count

            sub_df_descending_auxiliar = pd.concat(
                [sub_df_descending_auxiliar, row.to_frame().T])

            if temporal_descending_auxiliar_count >= abs(actual_vs_sample_size_difference):
                break

        sub_df_descending_auxiliar = sub_df_descending_auxiliar.reset_index(
            drop=True)
        return sub_df_descending_auxiliar

    def __get_descending_filtered_working_pivot__(self,
                                                  working_pivot_df,
                                                  values_descending_filter,
                                                  actual_vs_sample_size_difference):
        """
        Filters the working pivot DataFrame based on the descending filter 
        values.

        Args:
            working_pivot_df (pd.DataFrame): The working pivot DataFrame.
            values_descending_filter (list): The list of descending filter 
            values.
            actual_vs_sample_size_difference (int): The difference between the 
            actual and desired sample size.

        Returns:
            pd.DataFrame: The filtered working pivot DataFrame.
        """
        descending_filtered_working_pivot = working_pivot_df[
            working_pivot_df['Sample_size_by_weight'].isin(
                values_descending_filter)
        ].sample(n=abs(actual_vs_sample_size_difference))
        return descending_filtered_working_pivot

    def __get_to_remove_descending_working_pivot__(self,
                                                   descending_filtered_working_pivot,
                                                   prestructure_sampling_df):
        """
        Creates a DataFrame with rows to be removed from the pre-structured 
        sample to achieve the desired sample size.

        Args:
            descending_filtered_working_pivot (pd.DataFrame): The filtered 
            working pivot DataFrame.
            prestructure_sampling_df (pd.DataFrame): The pre-structured sample 
            DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with rows to be removed.
        """
        to_remove_descending_working_pivot = pd.DataFrame()

        for _, row in descending_filtered_working_pivot.iterrows():
            temporal_remove = prestructure_sampling_df.loc[
                (prestructure_sampling_df[self.structure_parameters]
                 == row[self.structure_parameters]).all(axis=1)
            ].sample(n=1)

            to_remove_descending_working_pivot = pd.concat(
                [to_remove_descending_working_pivot, temporal_remove])

        return to_remove_descending_working_pivot

    def __remove_rows_from_prestructure__(self,
                                          prestructure_sampling_df,
                                          to_remove_descending_working_pivot):
        """
        Removes specified rows from the pre-structured sample.

        Args:
            prestructure_sampling_df (pd.DataFrame): The pre-structured sample 
            DataFrame.
            to_remove_descending_working_pivot (pd.DataFrame): The DataFrame 
            with rows to be removed.

        Returns:
            pd.DataFrame: The adjusted structured sample DataFrame.
        """
        pre_merge_to_remove = pd.merge(
            prestructure_sampling_df,
            to_remove_descending_working_pivot,
            how='left',
            indicator=True)
        structured_sampled_df = pre_merge_to_remove[pre_merge_to_remove['_merge'] ==
                                                    'left_only'].drop(
            columns='_merge')
        return structured_sampled_df

    def __structured_sample_positive_difference__(self):
        """
        Adjusts the pre-structured sample by removing rows to match the desired
        sample size.

        Returns:
            pd.DataFrame: The adjusted structured sample DataFrame.
        """
        actual_vs_sample_size_difference = self.actual_vs_sample_size_difference()
        auxiliar_df_descending = self.auxiliar_df_descending()
        working_pivot_df = self.working_pivot_df()
        prestructure_sampling_df = self.prestructure_sampling_df()

        sub_df_descending_auxiliar = self.__get_sub_df_descending_auxiliar__(
            auxiliar_df_descending, actual_vs_sample_size_difference)
        values_descending_filter = sub_df_descending_auxiliar['Sample_size_by_weight'].tolist(
        )
        descending_filtered_working_pivot = self.__get_descending_filtered_working_pivot__(
            working_pivot_df, values_descending_filter, actual_vs_sample_size_difference)
        to_remove_descending_working_pivot = self.__get_to_remove_descending_working_pivot__(
            descending_filtered_working_pivot, prestructure_sampling_df)

        structured_sampled_df = self.__remove_rows_from_prestructure__(
            prestructure_sampling_df, to_remove_descending_working_pivot)
        return structured_sampled_df

    def structured_sample(self):
        """
        Generates the final structured sample DataFrame adjusted for the 
        desired sample size.

        Returns:
            pd.DataFrame: The final structured sample DataFrame.
        """
        actual_vs_sample_size_difference = self.actual_vs_sample_size_difference()

        if actual_vs_sample_size_difference < 0:
            return self.__structured_sample_negative_difference__()

        if actual_vs_sample_size_difference > 0:
            return self.__structured_sample_positive_difference__()

        if actual_vs_sample_size_difference == 0:
            return self.prestructure_sampling_df
