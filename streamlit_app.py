# ref: https://gw-quickview.streamlit.app/?ref=streamlit-io-gallery-favorites
# 사용해야하는 것: tabs, multipages

import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.markdown(
    """
    # 현황정보

    - 다음은 현황에 대한 그래프 입니다.
    """    
)

@st.cache_data
def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source


stock_data = get_data()

hover = alt.selection_single(
    fields=["date"],
    nearest=True,
    on="mouseover",
    empty="none",
)

lines = (
    alt.Chart(stock_data, title="Evolution of stock prices")
    .mark_line()
    .encode(
        x="date",
        y="price",
        color="symbol",
    )
)

points = lines.transform_filter(hover).mark_circle(size=65)

tooltips = (
    alt.Chart(stock_data)
    .mark_rule()
    .encode(
        x="yearmonthdate(date)",
        y="price",
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[
            alt.Tooltip("date", title="Date"),
            alt.Tooltip("price", title="Price (USD)"),
        ],
    )
    .add_selection(hover)
)

data_layer = lines + points + tooltips

ANNOTATIONS = [
    ("Sep 01, 2007", 450, "🙂", "Something's going well for GOOG & AAPL."),
    ("Nov 01, 2008", 220, "🙂", "The market is recovering."),
    ("Dec 01, 2007", 750, "😱", "Something's going wrong for GOOG & AAPL."),
    ("Dec 01, 2009", 680, "😱", "A hiccup for GOOG."),
]
annotations_df = pd.DataFrame(
    ANNOTATIONS, columns=["date", "price", "marker", "description"]
)
annotations_df.date = pd.to_datetime(annotations_df.date)

annotation_layer = (
    alt.Chart(annotations_df)
    .mark_text(size=20, dx=-10, dy=0, align="left")
    .encode(x="date:T", y=alt.Y("price:Q"), text="marker", tooltip="description")
)

combined_chart = data_layer + annotation_layer
st.altair_chart(combined_chart, use_container_width=True)

# import streamlit as st

# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
# )

# st.write("# Welcome to Streamlit! 👋")

# st.sidebar.success("Select a demo above.")

# st.markdown(
#     """
#     Streamlit is an open-source app framework built specifically for
#     Machine Learning and Data Science projects.
#     **👈 Select a demo from the sidebar** to see some examples
#     of what Streamlit can do!
#     ### Want to learn more?
#     - Check out [streamlit.io](https://streamlit.io)
#     - Jump into our [documentation](https://docs.streamlit.io)
#     - Ask a question in our [community
#         forums](https://discuss.streamlit.io)
#     ### See more complex demos
#     - Use a neural net to [analyze the Udacity Self-driving Car Image
#         Dataset](https://github.com/streamlit/demo-self-driving)
#     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
# """
# )