import streamlit as st

dashboard = st.Page(
    'reports/trend.py', title='Dashboard', icon=":material/dashboard:", default=True
)
dashboard2 = st.Page(
    'reports/trend2.py', title='Dashboard2', icon=":material/dashboard:"
)


pg = st.navigation(
    {
        'Reports': [dashboard, dashboard2]
    }
)

pg.run()