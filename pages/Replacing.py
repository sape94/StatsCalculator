import streamlit as st
import pandas as pd
from modules import CustomStreamlit as cst
from modules import ItemReplacer as ir

cst.Header('Item Replacing | App', 'images/NIQ_logo.png')

selected = cst.Custom().set_menu(options=['Home', 'Sampling', 'Replacing'],
                                 icons=['house',
                                        'calculator',
                                        'box-arrow-in-down-left'],
                                 index=2)

if selected == 'Replacing':

    cst.Subheader('Item Replacing App', '')

    @st.cache_data
    def cache_df(df):
        df = df.copy()
        cached_df = df
        return cached_df

    def cache_df_2(df):
        df_2 = df.copy()
        cached_df_2 = df_2
        return cached_df_2

    st.write(
        'Please provide Dataframes such that the Master Dataframe contains the Working Dataframe.')
    st.write('')
    with st.expander('Upload the CSV file that contains the  **Master Dataframe**:'):
        master_uploaded_file = st.file_uploader("Choose a file",
                                                type=['csv'],
                                                key='master_df'
                                                )
        if master_uploaded_file is not None:
            master_df = pd.read_csv(master_uploaded_file, encoding='UTF8')

            master_file_name_df = master_uploaded_file.name.replace('.csv', '')

            master_df = cache_df(master_df)
            st.write(master_df)
        st.caption('You can collapse this section if you want.')
    st.markdown('')
    with st.expander('Upload the CSV file that contains the  **Working Dataframe**:'):
        working_master_uploaded_file = st.file_uploader("Choose a file",
                                                        type=['csv'],
                                                        key='working_df'
                                                        )
        if working_master_uploaded_file is not None:

            working_df = pd.read_csv(
                working_master_uploaded_file, encoding='UTF8')

            working_file_name_df = working_master_uploaded_file.name.replace(
                '.csv', '')

            working_df = cache_df_2(working_df)
            st.write(working_df)
        st.caption('You can collapse this section if you want.')

    if master_uploaded_file is None and working_master_uploaded_file is None:
        st.write('')
        cst.ColoredCaption(
            'Please upload the Master Dataframe and the Working Dataframe.')
    if master_uploaded_file is not None and working_master_uploaded_file is None:
        st.write('')
        cst.ColoredCaption('Please upload the Working Dataframe.')
    if master_uploaded_file is None and working_master_uploaded_file is not None:
        st.write('')
        cst.ColoredCaption('Please upload the Master Dataframe.')
    if master_uploaded_file is not None and working_master_uploaded_file is not None:
        if not ir.ItemReplacerCheck(master_df, working_df).is_subdataframe():
            cst.WarningCaption(
                'Your Working Dataframe is not a subdataframe of your Master Dataframe.')

        else:
            st.write('')
            st.write('Select a column to **identify** the items:')
            df_cols = master_df.columns
            identifier_col_list = st.multiselect(
                'This would be the column that uniquely identifies the items of the Dataframe.', df_cols, max_selections=1)

            replacement_left, replacement_option, replacement_right = st.columns([
                3, 8, 3])

            if identifier_col_list != []:
                identifier_col = identifier_col_list[0]

                with replacement_option:

                    replacement_mode = st.radio('Replacing option',
                                                ('Direct replacement',
                                                 'Structured replacement'),
                                                horizontal=True,
                                                label_visibility='hidden')
                    st.write('')

                remove_mode_answer = st.radio(f'Provide the items by {identifier_col} that you want to remove:',
                                              ('Do it by selecting items from a list.',
                                               'Upload a Dataframe that contains the items you want to remove.'))

                items_to_replace = []

                removing_items_df = pd.DataFrame(
                    {f'{identifier_col}': [1, 2]})

                if remove_mode_answer == 'Do it by selecting items from a list.':
                    items_to_replace = st.multiselect(
                        f'Select the stores that you want to remove by {identifier_col}:', working_df[[f'{identifier_col}']])

                if remove_mode_answer == 'Upload a Dataframe that contains the items you want to remove.':
                    removing_items_file = st.file_uploader('Choose a file containing the selected identifier column and the items you want to replace:',
                                                           type=['csv'],
                                                           key='removing_items_df'
                                                           )
                    if removing_items_file is not None:

                        removing_items_df = pd.read_csv(
                            removing_items_file, encoding='UTF8')

                        if identifier_col in removing_items_df.columns:

                            items_to_replace = removing_items_df[identifier_col].to_list(
                            )

                if items_to_replace == [] or None:
                    cst.ColoredCaption('You dataframe is the same as before.')

                if identifier_col not in removing_items_df.columns:
                    cst.WarningCaption(
                        'You must verify that the file you uploaded contains the same identifier column.')

                if replacement_mode == 'Direct replacement' and identifier_col in removing_items_df.columns:
                    replacing_condition = ir.DirectItemReplacer(master_df,
                                                                working_df,
                                                                identifier_col,
                                                                items_to_replace).check_items_in_working_df()
                    if replacing_condition == True:
                        replaced_df = ir.DirectItemReplacer(master_df,
                                                            working_df,
                                                            identifier_col,
                                                            items_to_replace).replacer()

                        st.write('Working Dataframe with replaced items:')

                        st.write(replaced_df)

                        replaced_df_csv = replaced_df.to_csv(index=False)

                        col_save_replace_left, col_save_replcae = st.columns(
                            2, gap='medium')

                        with col_save_replcae:
                            st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                               data=replaced_df_csv,
                                               file_name=f'REPLACED_ITEMS_{working_file_name_df}.csv',
                                               mime='text/csv')

                        st.write('')
                        st.write(
                            'Don\'t forget to **download** your Working Dataframe with replaced rows.')
                        st.write('')
                        st.write('')

                    else:
                        cst.WarningCaption(
                            'You must verify that your selected items are in you working Dataframe.')

                if replacement_mode == 'Structured replacement' and identifier_col in removing_items_df.columns:
                    st.write('')
                    st.write(
                        'Select columns by priority to get the **structure**:')
                    structure_available_cols = [
                        col for col in df_cols if col != identifier_col]
                    max_selections_structure = len(structure_available_cols)
                    structure_col_list = st.multiselect(
                        'This would be the columns that will determine the grouping characteristics.',
                        structure_available_cols,
                        max_selections=max_selections_structure)

                    if structure_col_list == []:
                        cst.ColoredCaption(
                            'You must select at leadt one structure column.')

                    else:

                        replacing_condition = ir.StructuredItemReplacer(master_df,
                                                                        working_df,
                                                                        identifier_col,
                                                                        items_to_replace,
                                                                        structure_col_list).check_items_in_working_df()
                        if replacing_condition == True:
                            replaced_df = ir.StructuredItemReplacer(master_df,
                                                                    working_df,
                                                                    identifier_col,
                                                                    items_to_replace,
                                                                    structure_col_list).replacer()

                            st.write('Working Dataframe with replaced items:')

                            st.write(replaced_df)

                            replaced_df_csv = replaced_df.to_csv(index=False)

                            col_save_replace_left, col_save_replcae = st.columns(
                                2, gap='medium')

                            with col_save_replcae:
                                st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                                   data=replaced_df_csv,
                                                   file_name=f'REPLACED_ITEMS_{working_file_name_df}.csv',
                                                   mime='text/csv')

                            st.write('')
                            st.write(
                                'Don\'t forget to **download** your Working Dataframe with replaced rows.')
                            st.write('')
                            st.write('')

                        else:
                            cst.WarningCaption(
                                'You must verify that your selected items are in you working Dataframe.')


if selected == 'Home':
    st.switch_page('StatsCalculator.py')

if selected == 'Sampling':
    st.switch_page('pages/Sampling.py')

cst.Footer()
