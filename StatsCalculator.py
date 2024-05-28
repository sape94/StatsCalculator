import streamlit as st
from modules import CustomStreamlit as cst

cst.Header('StatsCalculator | Home', 'images/NIQ_logo.png')

selected = cst.Custom().set_menu(options=['   Home   ', 'Sampling', 'Replacing'],
                                 icons=['house',
                                        'calculator',
                                        'box-arrow-in-down-left'])

if selected == '   Home   ':
    st.header('List of available apps and sub apps')

    cst.Subheader('Sampling Calculator App', '/Sampling')

    sampling_app_desc = '''
    You can use it directly as a calculator
    or you can upload the Dataframe to obtain your sample size.
    After that you can sample your Dataframe or
    re-sample it if you like using either a random sampler or a strutured 
    sampler.
    '''
    cst.TopicAsCaption('Description', sampling_app_desc)

    cst.Subheader('Item Replacing App', '/Replacing')

    replacing_app_desc = '''
    By uploading a Master Dataframe and a Working Dataframe
    you can remove items from the Working Dataframe
    by selecting the columns that you are most interested in to mantain
    the structure, and the items to be replaced with items from the
    Mater Dataframe.
    The items to be replaced can be uploaded too, if you want.
    '''
    cst.TopicAsCaption('Description', replacing_app_desc)

    cst.Subheader('Random Sampling App', '/Random')

    random_app_desc = '''
    By uploading a Dataframe you can sample it by providing the sample size value.
    This sample will take randomly the number provided.
    '''
    cst.TopicAsCaption('Description', random_app_desc)

    cst.Subheader('Structured Sampling App', '/Structured')

    structured_app_desc = '''
    By uploading a Dataframe you can sample it by providing the sample size value.
    This sample will take the number provided along with the selected structure
    given by your needs.
    '''
    cst.TopicAsCaption('Description', structured_app_desc)

if selected == 'Sampling':
    st.switch_page('pages/Sampling.py')

if selected == 'Replacing':
    st.switch_page('pages/Replacing.py')

cst.Footer()
