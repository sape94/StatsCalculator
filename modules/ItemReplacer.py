import pandas as pd


class ItemReplacerCheck:
    """
    A class to check if a working DataFrame is a subdataframe of a master 
    DataFrame.

    Attributes:
        master (pd.DataFrame): The master DataFrame.
        working (pd.DataFrame): The working DataFrame to be checked.
    """

    def __init__(self,
                 master_df: pd.DataFrame,
                 working_df: pd.DataFrame):
        """
        Initializes the ItemReplacerCheck with the master and working DataFrames.

        Args:
            master_df (pd.DataFrame): The master DataFrame.
            working_df (pd.DataFrame): The working DataFrame to be checked.
        """
        self.master = master_df
        self.working = working_df

    def is_subdataframe(self):
        """
        Checks if the working DataFrame is a subdataframe of the master 
        DataFrame.

        Returns:
            bool: True if the working DataFrame is a subdataframe of the master DataFrame, False otherwise.
        """
        if self.working.shape[1] != self.master.shape[1]:
            return False
        if not all(self.working.columns == self.master.columns):
            return False
        merged = pd.merge(self.working,
                          self.master,
                          on=list(self.working.columns),
                          how='left',
                          indicator=True)
        return merged['_merge'].eq('both').all()


class DirectItemReplacer:
    """
    A class to replace specific items in a working DataFrame with new items 
    from a master DataFrame.

    Attributes:
        master (pd.DataFrame): The master DataFrame.
        working (pd.DataFrame): The working DataFrame.
        identifier_col (str): The column name used to identify items.
        items_to_replace (list): The list of items to replace in the working DataFrame.
    """

    def __init__(self,
                 master_df: pd.DataFrame,
                 working_df: pd.DataFrame,
                 identifier_col: str,
                 items_to_replace: list):
        """
        Initializes the DirectItemReplacer with the master and working 
        DataFrames, identifier column, and items to replace.

        Args:
            master_df (pd.DataFrame): The master DataFrame.
            working_df (pd.DataFrame): The working DataFrame.
            identifier_col (str): The column name used to identify items.
            items_to_replace (list): The list of items to replace in the working DataFrame.
        """
        self.master = master_df
        self.working = working_df
        self.identifier_col = identifier_col
        self.items_to_replace = items_to_replace

    def check_items_in_working_df(self):
        """
        Checks if all items to replace are present in the working DataFrame.

        Returns:
            bool: True if all items are present, False otherwise.
        """
        missing_items = [item for item in self.items_to_replace if item not in
                         self.working[self.identifier_col].values]
        if len(missing_items) > 1:
            return False
        return True

    def __remove_rows_from_working_df__(self):
        """
        Removes rows in the working DataFrame that are listed in 
        items_to_replace.

        Returns:
            pd.DataFrame: The working DataFrame with the specified rows removed.
        """
        filter_condition = self.working[self.identifier_col].isin(
            self.items_to_replace)
        return self.working[~filter_condition]

    def __remainder_rows_from_master_df__(self):
        """
        Retrieves the remaining rows in the master DataFrame that are not in 
        the working DataFrame.

        Returns:
            pd.DataFrame: The remaining rows in the master DataFrame.
        """
        filter_condition = self.master[self.identifier_col].isin(
            self.working[self.identifier_col])
        return self.master[~filter_condition]

    def replacer(self):
        """
        Replaces the specified rows in the working DataFrame with rows from 
        the master DataFrame.

        Returns:
            pd.DataFrame: The updated working DataFrame with the specified rows replaced.
        """
        removed_items_length = len(self.items_to_replace)
        new_rows = self.__remainder_rows_from_master_df__().sample(
            n=removed_items_length)
        new_working = pd.concat([self.__remove_rows_from_working_df__(),
                                 new_rows])
        return new_working


class StructuredItemReplacer:
    """
    A class to replace specific items in a working DataFrame with new items 
    from a master DataFrame, based on structure columns.

    Attributes:
        master (pd.DataFrame): The master DataFrame.
        working (pd.DataFrame): The working DataFrame.
        identifier_col (str): The column name used to identify items.
        items_to_replace (list): The list of items to replace in the working DataFrame.
        structure_cols (list): The columns used to define the structure for replacement.
    """

    def __init__(self,
                 master_df: pd.DataFrame,
                 working_df: pd.DataFrame,
                 identifier_col: str,
                 items_to_replace: list,
                 structure_cols: list):
        """
        Initializes the StructuredItemReplacer with the master and working 
        DataFrames, identifier column, items to replace, and structure columns.

        Args:
            master_df (pd.DataFrame): The master DataFrame.
            working_df (pd.DataFrame): The working DataFrame.
            identifier_col (str): The column name used to identify items.
            items_to_replace (list): The list of items to replace in the working DataFrame.
            structure_cols (list): The columns used to define the structure for replacement.
        """
        self.master = master_df
        self.working = working_df
        self.identifier_col = identifier_col
        self.items_to_replace = items_to_replace
        self.structure_cols = structure_cols

    def check_items_in_working_df(self):
        """
        Checks if all items to replace are present in the working DataFrame.

        Returns:
            bool: True if all items are present, False otherwise.
        """
        missing_items = [item for item in self.items_to_replace if item not in
                         self.working[self.identifier_col].values]
        if len(missing_items) > 1:
            return False
        return True

    def __remove_rows_from_working_df__(self):
        """ Removes rows in the working DataFrame that are listed in 
        items_to_replace.

        Returns:
            pd.DataFrame: The working DataFrame with the specified rows removed.
        """
        filter_condition = self.working[self.identifier_col].isin(
            self.items_to_replace)
        return self.working[~filter_condition]

    def __removed_rows_from_working_df__(self):
        """ Retrieves the rows removed from the working DataFrame based on 
        items_to_replace.

        Returns:
            pd.DataFrame: The rows removed from the working DataFrame.
        """
        filter_condition = self.working[self.identifier_col].isin(
            self.items_to_replace)
        return self.working[filter_condition]

    def __remainder_rows_from_master_df__(self):
        """ Retrieves the remaining rows in the master DataFrame that are not 
        in the working DataFrame.

        Returns:
            pd.DataFrame: The remaining rows in the master DataFrame.
        """
        filter_condition = self.master[self.identifier_col].isin(
            self.working[self.identifier_col])
        return self.master[~filter_condition]

    def replacer(self):
        """ Replaces the specified rows in the working DataFrame with rows 
        from the master DataFrame based on structure columns.

        Returns:
            pd.DataFrame: The updated working DataFrame with the specified rows replaced.
        """
        updated_working_df = self.__remove_rows_from_working_df__()
        removed_from_working_df = self.__removed_rows_from_working_df__()
        replacement_rows = pd.DataFrame(columns=self.master.columns)
        for _, row in removed_from_working_df.iterrows():
            temp_df = self.__remainder_rows_from_master_df__()
            for col in self.structure_cols:
                temp_df = temp_df[temp_df[col] == row[col]]
                if temp_df.empty:
                    break
            if temp_df.empty:
                replacement_row = self.__remainder_rows_from_master_df__(
                ).iloc[0]
            else:
                replacement_row = temp_df.iloc[0]
            replacement_rows = pd.concat(
                [replacement_rows, replacement_row.to_frame().transpose()])
        final_df = pd.concat(
            [updated_working_df, replacement_rows]).reset_index(drop=True)
        self.working = final_df
        return self.working
