import toml
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

config = toml.load('./.streamlit/config.toml')
version = config['settings']['version']
primaryColor = config['theme']['primaryColor']
textColor = config['theme']['textColor']
backgroundColor = config['theme']['backgroundColor']
secondaryBackgroundColor = config['theme']['secondaryBackgroundColor']
tertiaryBackgroundColor = config['settings']['tertiaryBackgroundColor']
selectedBackgroundColor = config['settings']['selectedBackgroundColor']
iconColor = config['settings']['iconColor']
accentTextColor = config['settings']['accentTextColor']
warningColor = config['settings']['warningColor']
pagePath = config['footer']['pagePath']
logoPath = config['footer']['logoPath']

this_project_signature = 'Sergio Pelayo from NIQ LatAm\'s Automation & Innovation Team'


class Custom:

    def __init__(self):
        pass

    def __set_page_config__(self,
                            title: str):
        self.page_config = st.set_page_config(
            page_title=title,
            layout='centered',
            initial_sidebar_state='collapsed'
        )
        hide_menu_style = """
                <style>
                #MainMenu {visibility: display;}
                </style>
                """
        self.hide_menu = st.markdown(hide_menu_style,
                                     unsafe_allow_html=True)
        return self.page_config, self.hide_menu

    def __set_banner__(self,
                       banner_path: str):
        image = Image.open(banner_path)
        self.set_banner = st.image(image,
                                   use_column_width='always',
                                   output_format='png')
        return self.set_banner

    def set_menu(self,
                 options: list,
                 icons: list,
                 index: int = 0,
                 navlink_selected_color: str = selectedBackgroundColor):
        option_menu_own = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            menu_icon='cast',
            default_index=index,
            orientation='horizontal',
            styles={
                "container": {"padding": "0!important",
                              "background-color": f"{secondaryBackgroundColor}"},
                "icon": {"color": f"{iconColor}",
                         "font-size": "15px"},
                "nav-link": {"color": f"{textColor}",
                             "font-size": "15px",
                             "text-align": "centered",
                             "margin": "0px",
                             "--hover-color": f"{tertiaryBackgroundColor}"},
                "nav-link-selected": {"color": f"{secondaryBackgroundColor}",
                                      "background-color": f"{navlink_selected_color}"},
            }
        )
        return option_menu_own

    def __set_footer__(self,
                       page_path: str = pagePath,
                       signature: str = this_project_signature,
                       logo_path: str = logoPath,
                       alternate_logo: str = 'ALT'
                       ):
        style = f"""
        <style>
        a:link , a:visited{{
        color: {textColor};
        background-color: transparent;
        text-decoration: none;
        }}

        a:hover,  a:active {{
        color: {primaryColor};
        opacity: 1;
        background-color: transparent;
        text-decoration: underline;
        }}

        #page-container {{
        position: relative;
        min-height: 10vh;
        }}

        footer{{
            visibility:hidden;
        }}
        .footer {{
        position: relative;
        left: 0;
        top:230px;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: {textColor};
        opacity: 0.7;
        text-align: left; 
        }}
        </style>
        """
        footer = f"""
        {style}
        <div id="page-container">
        <div class="footer">
        <p style='font-size: 0.875em;'>Developed by <a style='display: inline;
        text-align:
        left;' href="{page_path}" target="_blank">
        <img src="{logo_path}"
        alt="{alternate_logo}" height= "20"/><br>{signature}.
        </br></a>Version {version}.</p>
        </div>
        </div>
        """
        return st.write(footer, unsafe_allow_html=True)

    def __subheader__(self,
                      subheader: str,
                      href: str,
                      align: str = 'left'):
        style = f'''
        <style>
        .subhead-item {{
            backgroundcolor: transparent;
        }}
        .subhead-item:hover {{
            color: {accentTextColor};
        }}
        </style>
        '''
        subheader = f'''
        {style}
        <a style='display: inline; text-align: {align}; color: {textColor};
        ; text-decoration: none; '
        href="{href}" target="_self">
        <h3 class="subhead-item">
        {subheader}
        </h3>
        </a>
        '''
        return st.write(subheader, unsafe_allow_html=True)

    def __subsubheader__(self,
                         subsubheader: str,
                         href: str,
                         align: str = 'left'):
        style = f'''
        <style>
        .subsubhead-item {{
            color: {accentTextColor};
            backgroundcolor: transparent;
        }}
        .subsubhead-item:hover {{
            color: {iconColor};
        }}
        </style>
        '''
        subsubheader = f'''
        {style}
        <a style='display: inline; text-align: {align}; color: {textColor};
        ; text-decoration: none; '
        href="{href}" target="_self">
        <h4 class="subsubhead-item">
        {subsubheader}
        </h4>
        </a>
        '''
        return st.write(subsubheader, unsafe_allow_html=True)

    def __topic_as_caption__(self,
                             topic: str,
                             caption: str):
        topic = f'''
        <div style="text-align: left;
        color: {iconColor};">
        {topic}</div>
        '''
        caption = f'''
        <div style="text-align: justify;
        margin-top: 5px;
        ">{caption}</div>'''
        topic = st.write(topic, unsafe_allow_html=True)
        caption = st.caption(caption, unsafe_allow_html=True)
        space = st.header('')
        return topic, caption, space

    def __colored_caption__(self,
                            caption: str):
        caption = f'''
        <p style="color: {accentTextColor};">
        {caption}
        </p>
        '''
        return st.caption(caption, unsafe_allow_html=True)

    def __warning_caption__(self,
                            caption: str):
        caption = f'''
        <p style="color: {warningColor};">
        {caption}
        </p>
        '''
        return st.caption(caption, unsafe_allow_html=True)


class Header:

    def __init__(self,
                 title: str,
                 banner_path: str):
        Custom().__set_page_config__(title=title)
        Custom().__set_banner__(banner_path=banner_path)


class Footer:

    def __init__(self,
                 page_path: str = pagePath,
                 signature: str = this_project_signature,
                 logo_path: str = logoPath,
                 alternate_logo: str = 'ALT'
                 ):
        Custom().__set_footer__(page_path,
                                signature,
                                logo_path,
                                alternate_logo)


class Subheader:

    def __init__(self,
                 subheader: str,
                 href: str,
                 align: str = 'left'):
        Custom().__subheader__(subheader, href, align)


class Subsubheader:

    def __init__(self,
                 subsubheader: str,
                 href: str,
                 align: str = 'left'):
        Custom().__subsubheader__(subsubheader, href, align)


class TopicAsCaption:

    def __init__(self,
                 topic: str,
                 caption: str):
        Custom().__topic_as_caption__(topic, caption)


class ColoredCaption:

    def __init__(self,
                 caption: str):
        Custom().__colored_caption__(caption)


class WarningCaption:

    def __init__(self,
                 caption: str):
        Custom().__warning_caption__(caption)
