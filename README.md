# StatsCalculator
A non-confidential version of the Stats App made for NIQ's internal use.

This Data Sampling and Manipulation Toolkit is a comprehensive Streamlit application designed to assist users in various data sampling and manipulation tasks. It offers several features and sub-applications, including:

- Sampling Calculator App: This app allows users to calculate the required sample size based on parameters such as population size, confidence level, standard error, and sample portion. Users can upload their dataset and perform random or structured sampling directly from the app.

- Item Replacing App: This papp allows users to replace specific items or rows in a working dataset with corresponding items from a master dataset. Users can upload both the master and working datasets, select an identifier column (e.g., unique IDs, names, or codes), and specify the items they want to replace. The app supports two modes of replacement: direct replacement and structured replacement. In direct replacement mode, users can directly select the items to be replaced. In structured replacement mode, users can specify additional structure columns to maintain the dataset's structure during the replacement process. This app ensures that the replaced dataset retains the desired structure and characteristics.

- Random Sampling App: This app enables users to upload their dataset and perform random sampling by specifying the desired sample size.

- Structured Sampling App: Similar to the Random Sampling App, this app allows users to perform structured sampling on their dataset. Users can select an identifier column and structure parameters to guide the sampling process, ensuring that the sample maintains the desired data structure.

The application is built using the Streamlit framework and provides a user-friendly interface for data exploration, manipulation, and analysis. It offers various customization options, such as selecting columns, specifying parameters, and downloading the resulting datasets in CSV format.
