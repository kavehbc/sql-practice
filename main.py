import streamlit as st
import pandas as pd
import sqlite3
import os
import re
import base64
from pathlib import Path


def markdown_images(markdown):
    # example image markdown:
    # ![Test image](images/test.png "Alternate text")
    images = re.findall(r'(!\[(?P<image_title>[^\]]+)\]\((?P<image_path>[^\)"\s]+)\s*([^\)]*)\))', markdown)
    return images


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path, img_alt):
    img_format = img_path.split(".")[-1]
    img_html = f'<img src="data:image/{img_format.lower()};base64,{img_to_bytes(img_path)}" alt="{img_alt}" style="max-width: 100%;">'
    return img_html


def markdown_insert_images(markdown):
    images = markdown_images(markdown)

    for image in images:
        image_markdown = image[0]
        image_alt = image[1]
        image_path = image[2]
        if os.path.exists(image_path):
            markdown = markdown.replace(image_markdown, img_to_html(image_path, image_alt))
    return markdown


def main():
    markdown_file_path = "data/sql-murder-mystery/main.md"
    if not os.path.exists(markdown_file_path):
        st.error("Markdown file does not exist.")
    else:
        with open(markdown_file_path, 'r', encoding="utf-8") as outfile:
            markdown_content = outfile.read()
            readme = markdown_insert_images(markdown_content)
        st.markdown(readme, unsafe_allow_html=True)

    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("data/sql-murder-mystery/sql-murder-mystery.db")

    sql_query = st.text_area("SQL Query", value="SELECT * from person")
    btn_query = st.button("Run")

    if btn_query:
        df = pd.read_sql_query(sql_query, con)
        # Verify that result of SQL query is stored in the dataframe
        st.write(df)

    murderer = st.text_input("Murderer Name")
    btn_check = st.button("Check")
    if btn_check:
        cursor = con.cursor()
        check_query = f"INSERT INTO solution VALUES (1, '{murderer}');"
        cursor.execute(check_query)
        df = pd.read_sql_query("SELECT value FROM solution;", con)
        con.commit()
        st.write(df)

    con.close()


if __name__ == '__main__':
    st.set_page_config(
        page_title="SQL Practice",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            'Get Help': 'https://github.com/kavehbc/sql-practice',
            'Report a bug': "https://github.com/kavehbc/sql-practice",
            'About': "# SQL Practice"
        }
    )
    main()
