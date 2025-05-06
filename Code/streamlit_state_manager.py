from genre_shifter import genre_shifter
from Utility.toolbox import find_repo_root, get_genres
root = find_repo_root()



import streamlit as st

movies = {
    "Alien" : "Data/trope_time_series/alien_tropes.csv",
    "Clueless" : f"{root}/Data/trope_time_series/clueless_tropes.csv",
    "Fellowship of The Ring" : f"{root}/Data/trope_time_series/Fellowship_of_the_Ring_filled.csv",
    "10 Things I Hate About You" : f"{root}/Data/trope_time_series/10_things_i_hate.csv"
}

def initialize_state():
    gs = genre_shifter()
    st.session_state.gs = gs
    st.session_state.movies = movies
    st.session_state.genres = get_genres()
    
