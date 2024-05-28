import pandas as pd
from modules import SampleSizeCalculator as ssc


class RandomSampler:
    """
    A class used to sample a random subset from a DataFrame based on given parameters.

    Attributes:
        df (pd.DataFrame): The DataFrame to sample from.
        sample_portion (int): The portion of the population to sample, as a percentage.
        confidence_level (int): The desired confidence level for the sample.
        standard_error (int): The desired standard error for the sample.
    """

    def __init__(self,
                 df: pd.DataFrame,
                 sample_portion: int = 50,
                 confidence_level: int = 99,
                 standard_error: int = 1):
        """
        Initializes the RandomSampler with the DataFrame and sampling parameters.

        Args:
            df (pd.DataFrame): The DataFrame to sample from.
            sample_portion (int): The portion of the population to sample, as a percentage.
            confidence_level (int): The desired confidence level for the sample.
            standard_error (int): The desired standard error for the sample.

        Returns:
            pd.DataFrame: The randomly sampled DataFrame.
        """
        population_size = df.shape[0]
        sample_size = ssc.SampleSize(sample_portion=sample_portion,
                                     confidence_level=confidence_level,
                                     standard_error=standard_error).sample_size(
                                         population_size=population_size)
        self.random_sampled_df = df.sample(n=sample_size)

    def sampled_df(self):
        return self.random_sampled_df
