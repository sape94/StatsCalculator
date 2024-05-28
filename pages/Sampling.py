import streamlit as st
import pandas as pd
from modules import CustomStreamlit as cst
from modules import SampleSizeCalculator as ssc
from modules import RandomSampler as rs
from modules import StructuredSampler as ss

cst.Header('Sample Size Calculator | App', 'images/NIQ_logo.png')

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
                                          index=0)

    if selected2 == 'All':
        cst.Subheader('Sampling Calculator App', '')

        st.markdown('The **sample size\' formula** is the following:')
        st.latex(r'n = \frac{NZ^{2}pq}{e^{2}(N-1)+Z^{2}pq};')
        st.markdown('')
        description_message = r'''
        where $n$ is the **sample size**, $N$ the **population size**, $e$ the 
        **standard error**, $Z$ the **Z-score value** wich is dependent of the 
        **confidence level**, $p$ the **sample portion**, and $q=(1-p)$.
        '''
        st.write(description_message)
        st.markdown('')

        with st.expander('If you want to upload a Dataframe, expand this section. When you finish you can collapse it again.'):
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

        with st.expander(r'Expand this section if you know the **sample portion** from previous samples.'):
            p_100 = st.slider(
                r'Select the sample\'s portion value, $p$, (%):', 0, 100, 50)
            p = int(p_100)

        col_conf_lev, col_z_score = st.columns(2, gap='medium')

        with col_conf_lev:
            st.write('Select the **confidence level** (%):')
            conf_lev = st.selectbox(
                r'',
                ('99', '98', '95', '90', '85', '80'))

        with col_z_score:
            z_score_dict = {99: 2.576,
                            98: 2.326,
                            95: 1.96,
                            90: 1.645,
                            85: 1.44,
                            80: 1.282}
            st.write(r'Then, the **Z-score value**, $Z$, is:')
            z_s = str(z_score_dict[int(conf_lev)])
            z_box = st.selectbox(r'',
                                 (f'{z_s}', '0'), disabled=True)

        st.markdown('')
        st.markdown('')

        col_stnd_error, col_population_size = st.columns(2, gap='medium')

        with col_stnd_error:
            st.write(r'Select, $e$, the **standard error**(%):')
            s_e = st.selectbox(
                r'',
                ('1', '2', '3', '4', '5', '10', '20'))

        with col_population_size:
            if uploaded_file is not None:
                st.write(r'The **population size**, $N$, is:')
                N = df.shape[0]
                N_s = str(N)
                z_box = st.selectbox(
                    r'',
                    (f'{N_s}', '4'), disabled=True)
            else:
                st.write(r'Type the **population size**, $N$:')
                N = st.number_input('', min_value=1)

        st.markdown('')
        st.markdown('')

        col_sample_size_left, col_sample_size, col_sample_size_right = st.columns([
                                                                                  1, 2, 1], gap='medium')

        with col_sample_size:
            n = ssc.SampleSize(sample_portion=p,
                               confidence_level=conf_lev,
                               standard_error=s_e).sample_size(population_size=N)

            st.markdown(
                r':arrow_forward::arrow_forward: Then, the **sample size** is:')
            st.latex(f'n = {n}')

        st.markdown('')
        st.markdown('')

        if uploaded_file is not None:

            with st.expander('If you want to sample the Dataframe, expand this section. When you finish you can collapse it again.'):
                samp_ans = st.radio('Do you want to sample your Dataframe?',
                                    ('No.',
                                     'Yes, with a non-stratified (random) method.',
                                     'Yes, with a stratified (structured) method.'))

                if samp_ans == 'Yes, with a non-stratified (random) method.':
                    @st.cache_data
                    def cached_df(df, p, conf_lev, s_e):
                        cached_df = rs.RandomSampler(df=df,
                                                     sample_portion=p,
                                                     confidence_level=conf_lev,
                                                     standard_error=s_e).sampled_df()
                        return cached_df

                    def second_cached_df(df, p, conf_lev, s_e):
                        second_cached_df = rs.RandomSampler(df=df,
                                                            sample_portion=p,
                                                            confidence_level=conf_lev,
                                                            standard_error=s_e).sampled_df()
                        return second_cached_df

                    sampled_df = cached_df(df, p=p, conf_lev=conf_lev, s_e=s_e)
                    if st.button(':inbox_tray: Press here to re-sample :inbox_tray:'):
                        df = df.sample(frac=1)
                        sampled_df = second_cached_df(df,
                                                      p=p,
                                                      conf_lev=conf_lev,
                                                      s_e=s_e)

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

                if samp_ans == 'Yes, with a stratified (structured) method.':

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
                                         'pages/Replacing.py', 'center')
                        st.write('')
                        st.write('')

        col_z_core_explanation, col_z_score_explanation_right = st.columns([
                                                                           2, 1], gap='medium')

        with col_z_core_explanation:
            with st.expander('Complementary info'):
                st.write(r'The **Z-score value**, $Z$, is such that:')
                st.latex(
                    r'\int_{Z}^{\infty}\textrm{w}_{\textrm{G}}(\tau)\textrm{d}\tau=\frac{\alpha}{2};')
                st.write('where:')
                st.markdown(
                    r'- $\textrm{w}_{\textrm{G}}(\tau)$ is the **normal** probability density function,')
                st.write(r'- $\alpha\in[0,1]$, the **confidence level**.')
                st.write('')

    if selected2 == 'Random':
        st.switch_page('pages/Random.py')

    if selected2 == 'Structured':
        st.switch_page('pages/Structured.py')

if selected == 'Home':
    st.switch_page('StatsCalculator.py')


if selected == 'Replacing':
    st.switch_page('pages/Replacing.py')

cst.Footer()
