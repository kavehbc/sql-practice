import streamlit as st
import pandas as pd
import sqlite3
import os
from utils.markdown import markdown_insert_images


def main():
    dbs = ["sql-murder-mystery"]
    db = st.sidebar.selectbox("Database", options=dbs)

    markdown_file_path = f"data/{db}/main.md"
    if not os.path.exists(markdown_file_path):
        st.error("Markdown file does not exist.")
    else:
        with open(markdown_file_path, 'r', encoding="utf-8") as outfile:
            markdown_content = outfile.read()
            readme = markdown_insert_images(markdown_content)
        st.markdown(readme, unsafe_allow_html=True)

    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect(f"data/{db}/{db}.db")

    sql_query = st.text_area("SQL Query", value="")
    btn_query = st.button("Run")

    if btn_query:
        df = pd.read_sql_query(sql_query, con)
        # Verify that result of SQL query is stored in the dataframe
        st.write(df)

    # -- DB custom commands
    if db == "sql-murder-mystery":
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
