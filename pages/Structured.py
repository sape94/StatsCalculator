import streamlit as st
import pandas as pd
from modules import CustomStreamlit as cst
from modules import StructuredSampler as ss

cst.Header('Structured Sampler | App', 'images/NIQ_logo.png')

selected = cst.Custom().set_menu(options=['Home', 'Sampling', 'Replacing'],
                                 icons=['house',
                                        'calculator',
                                        'box-arrow-in-down-left'],
                                 index=1)

if selected == 'Sampling':
    left_space, sub_menu, right_space = st.columns([1, 8, 1], gap='small')
    with sub_menu:
        selected2 = cst.Custom().set_menu(options=['All', 'Random', 'Structured'],
                                          icons=['bricks',
                                                 'shuffle',
                                                 'file-bar-graph'],
                                          index=2)

    if selected2 == 'All':
        st.switch_page('pages/Sampling.py')

    if selected2 == 'Random':
        st.switch_page('pages/Random.py')

    if selected2 == 'Structured':
        cst.Subheader('Structured Sampling App', '')
        with st.expander('Upload your Dataframe. When you finish you can collapse this section.'):
            st.write(
                'Upload the CSV file that contains the working Dataframe:')
            uploaded_file = st.file_uploader("Choose a file",
                                             type=['csv'],
                                             key='gral_settings_df'
                                             )
            if uploaded_file is not None:

                df = pd.read_csv(uploaded_file, encoding='UTF8')

                file_name_df = uploaded_file.name.replace('.csv', '')

                st.write(df)

        st.markdown('')

        if uploaded_file is None:
            cst.ColoredCaption('Please upload a Dataframe to continue.')

        if uploaded_file is not None:
            col_sample_size_left, col_sample_size, col_sample_size_right = st.columns(
                [1, 5, 1], gap='medium')

            with col_sample_size:
                sample_size_string = st.number_input(
                    r'Type the **sample size**, $n$:', min_value=1, max_value=df.shape[0])
                n = int(sample_size_string)

            st.write('')
            st.write('')

            with st.expander('Expand this section to show your **Structure Sampled Dataframe**:'):
                identifier_column_option = st.checkbox(
                    'Select an **identifier** column')

                df_cols = df.columns.to_list()
                identifier_col = []

                if identifier_column_option:
                    identifier_col_list = st.multiselect(
                        'This would be the column that uniquely identifies the items of the Dataframe.', df_cols, max_selections=1)

                    if identifier_col_list != []:
                        identifier_col = identifier_col_list[0]

                st.write('')
                st.write('Select the **structure** parameters column(s):')
                structure_df_cols = [
                    item for item in df_cols if item != identifier_col]
                structure_parameters_list = st.multiselect(
                    'This would be the parameters that will define the structure of the Dataframe for stratification.',
                    structure_df_cols)

                if structure_parameters_list == []:
                    cst.ColoredCaption(
                        'You must select the structure column(s) if you want to continue.')

                else:
                    structured_pivot_df = ss.StructuredSampler(df,
                                                               n,
                                                               identifier_col,
                                                               structure_parameters_list).working_pivot_df()
                    structured_df = ss.StructuredSampler(df,
                                                         n,
                                                         identifier_col,
                                                         structure_parameters_list).structured_sample()

                    st.write(
                        'Weighted pivot given the selected structure:')
                    st.write(structured_pivot_df)
                    pivot_structure_sampled_df_csv = structured_pivot_df.to_csv(
                        index=False)
                    col_pivot_left, col_pivot_right = st.columns(
                        2, gap='medium')

                    with col_pivot_right:
                        st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                           data=pivot_structure_sampled_df_csv,
                                           file_name=f'PIVOT_STRUCTURE_{file_name_df}.csv',
                                           mime='text/csv')

                    st.write(
                        'Sampled Dataframe given the selected structure:')
                    st.write(structured_df)
                    structured_df_csv = structured_df.to_csv(
                        index=False)
                    col_structure_left, col_structure_right = st.columns(
                        2, gap='medium')

                    with col_structure_right:
                        st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                           data=structured_df_csv,
                                           file_name=f'STRUCTURED_SAMPLE_{file_name_df}.csv',
                                           mime='text/csv')

                    st.write('')
                    st.write(
                        'Don\'t forget to **download** your sampled Dataframe.')

                    st.write(
                        'If you want to remove items from the sampled Dataframe use our:')
                    cst.Subsubheader('Replacing App',
                                     '/Replacing', 'center')
                    st.write('')
                    st.write('')


if selected == 'Home':
    st.switch_page('StatsCalculator.py')


if selected == 'Replacing':
    st.switch_page('pages/Replacing.py')

cst.Footer()
