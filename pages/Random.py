import streamlit as st
import pandas as pd
from modules import CustomStreamlit as cst

cst.Header('Random Sampler | App', 'images/NIQ_logo.png')

selected = cst.Custom().set_menu(options=['   Home   ', 'Sampling', 'Replacing'],
                                 icons=['house',
                                        'calculator',
                                        'box-arrow-in-down-left'],
                                 index=1)

if selected == 'Sampling':
    left_space, sub_menu, right_space = st.columns([1, 8, 1], gap='small')
    with sub_menu:
        selected2 = cst.Custom().set_menu(options=['   All   ', 'Random', 'Structured'],
                                          icons=['bricks',
                                                 'shuffle',
                                                 'file-bar-graph'],
                                          index=1)

    if selected2 == '   All   ':
        st.switch_page('pages/Sampling.py')

    if selected2 == 'Random':
        cst.Subheader('Random Sampling App', '')

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

            with st.expander('Expand this section to show your **Randomly Sampled Dataframe**:'):
                @st.cache_data
                def cached_df(df, sample_size):
                    cached_df = df.sample(frac=1).sample(n=sample_size)
                    return cached_df

                def second_cached_df(df, sample_size):
                    second_cached_df = df.sample(frac=1).sample(n=sample_size)
                    return second_cached_df

                sampled_df = cached_df(df, n)
                if st.button(':inbox_tray: Press here to re-sample :inbox_tray:'):
                    df = df.sample(frac=1)
                    sampled_df = second_cached_df(df, n)

                st.write(sampled_df)
                sampled_df_csv = sampled_df.to_csv(index=False)

                col_save_random_left, col_save_random = st.columns(
                    2, gap='medium')

                with col_save_random:
                    st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                       data=sampled_df_csv,
                                       file_name=f'SAMPLED_{file_name_df}.csv',
                                       mime='text/csv')

                st.write('')
                st.write(
                    'Don\'t forget to **download** your sampled Dataframe.')
                st.write(
                    'If you want to remove items from the sampled Dataframe use our:')
                cst.Subsubheader('Replacing App',
                                 'pages/Replacing.py', 'center')
                st.write('')
                st.write('')

    if selected2 == 'Structured':
        st.switch_page('pages/Structured.py')

if selected == '   Home   ':
    st.switch_page('StatsCalculator.py')


if selected == 'Replacing':
    st.switch_page('pages/Replacing.py')

cst.Footer()
