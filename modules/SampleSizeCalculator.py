class SampleSize:
    """
    A class used to calculate the sample size needed for a given population size
    based on sampling parameters such as sample portion, confidence level, and standard error.

    Attributes:
        sample_portion (int): The portion of the population to sample, as a percentage.
        confidence_level (int): The desired confidence level for the sample.
        standard_error (int): The desired standard error for the sample.
        p_value (float): The proportion of the population to sample, as a decimal.
        confidence_level (int): The desired confidence level for the sample.
        standard_error (float): The desired standard error for the sample, as a decimal.
        q_value (float): The complement of the p-value (1 - p_value).
        Z_score (float): The z-score corresponding to the confidence level.
    """

    def __init__(self,
                 sample_portion: int = 50,
                 confidence_level: int = 99,
                 standard_error: int = 1):
        """
        Initializes the SampleSize with sampling parameters.

        Args:
            sample_portion (int): The portion of the population to sample, as a percentage.
            confidence_level (int): The desired confidence level for the sample.
            standard_error (int): The desired standard error for the sample.
        """

        self.p_value = float(sample_portion)/100
        self.confidence_level = int(confidence_level)
        self.standard_error = float(standard_error)/100

        z_score_dict = {99: 2.576,
                        98: 2.326,
                        95: 1.96,
                        90: 1.645,
                        85: 1.44,
                        80: 1.282}

        self.q_value = 1 - self.p_value
        self.Z_score = z_score_dict[self.confidence_level]

    def sample_size(self,
                    population_size: int):
        """
        Calculates the sample size needed for a given population size.

        Args:
            population_size (int): The size of the population.

        Returns:
            int: The calculated sample size.
        """
        numerator = population_size*(self.Z_score**2)*self.p_value*self.q_value
        denominator = (self.standard_error**2)*(population_size-1) + \
            (self.Z_score**2)*self.p_value*self.q_value
        sample_size = int(numerator/denominator)
        return sample_size
