import streamlit as st

import streamlit_state_manager as ssm
from Utility.toolbox import get_genres


if "initialized" not in st.session_state:
    ssm.initialize_state()
    st.session_state.initialized = True


genres = st.session_state.genres
movies = st.session_state.movies
titles = list(movies.keys())
gs = st.session_state.gs


st.set_page_config(layout="wide")
write_text = "First, select two movies -- note that they can be the same movie. Then select the genre to compare" \
+ "and the time range to compare. Once you're all set up, click Compare."


# Create the Streamlit app
with st.sidebar:
    st.header("Genre Comparison")
    st.write(write_text)


    selections = []
    for i in range(2):
        selection = st.selectbox(f"Movie {i+1}", titles, index=titles.index("Alien"), key=i)
        if selection != "-- Choose a Movie --":
            selections.append(selection)
    refmovie, compmovie = selections

    genre = st.selectbox("Select a Genre", get_genres())

    cutoff = st.number_input("Enter number of tropes to cutoff", value=35, key="cutoff")
    ref1 = st.number_input("Enter comparison start time percentage", value=0, key="ref1")
    ref2 = st.number_input("Enter comparison end time percentage", value=50, key="ref2")
    comp1 = st.number_input("Enter comparison start time percentage", value=50, key="comp1")
    comp2 = st.number_input("Enter comparison end time percentage", value=100, key="comp2")

    if not (0 <= ref1 < ref2 <= 100 and 0 <= comp1 < comp2 <= 100):
        st.error("Please enter valid ranges: start must be less than end, and values should be between 0 and 100.")
    else:
        ref_range_decimals = (ref1 / 100, ref2 / 100)
        comp_range_decimals = (comp1 / 100, comp2 / 100)


if st.button("Compare"):
    if refmovie == compmovie:
        fig = gs.plot_comparison(genre, movies[refmovie], refmovie, ref_range_decimals, comp_range_decimals)
    else:
        fig = gs.plot_two(refmovie, compmovie, genre, cutoff)
    st.pyplot(fig)