import requests
import streamlit as st
import pandas as pd


st.title("Paradise Episode Information")


def paradise():
    showUrl = "https://api.tvmaze.com/shows/75030/episodes"
    r = requests.get(showUrl)
    showData = r.json()

    episodes = []
    ratings = []
    images = {}
    runtimes = {}
    summaries = {}
    episode_names = {}
    
    for ep in showData:
        episodeNumber = ep["number"]
        episodes.append(episodeNumber)
        ratings.append(ep["rating"]["average"])
        images[episodeNumber] = ep["image"]["medium"]
        runtimes[episodeNumber] = ep["runtime"]
        episode_names[episodeNumber] =ep["name"]
        summaries[episodeNumber] = ep["summary"].replace("<p>", "").replace("</p>", "")
        
                    
    df = pd.DataFrame ({ "Episode": episodes, "Rating": ratings})
    st.header("Episode Rating Chart")
    st.line_chart(df.set_index("Episode"))
    st.write("**X-axis:** Episode Number  |  **Y-axis:** Rating")

    st.header("Display An Image For Your Favorite Episode")
    selectedEpisode = st.selectbox("Select Episode Number:", episodes)

    if images[selectedEpisode]:
        st.image(images[selectedEpisode], caption= f"Episode {selectedEpisode}")
    else:
        st.write("No image is available for this episode")

    st.header("Select the name of your favorite episode to show the summary")
    selectedEpisodeSummary = st.selectbox("Select an Episode Number to see the Summary:", episodes)
    if selectedEpisodeSummary:
        st.info(summaries[selectedEpisodeSummary])

    st.header("Chose an Episode to see a graph displaying how long each one is")
    st.write("**X-axis:** Episode Number  |  **Y-axis:** Run Time")
    chosenEpisode = st.multiselect("Choose Episode Name:", episodes)

    if "selected_runtime_episodes" not in st.session_state:
        st.session_state.selected_runtime_episodes = []
        st.session_state.selected_runtime_runtimes = []
        
    if chosenEpisode:
        for ep in chosenEpisode:
            st.session_state.selected_runtime_episodes.append(ep)
            st.session_state.selected_runtime_runtimes.append(runtimes[ep])
            
        runtime_df = pd.DataFrame({ "Episode": st.session_state.selected_runtime_episodes,
                                    "Runtime": st.session_state.selected_runtime_runtimes })
        st.bar_chart(runtime_df.set_index("Episode"))



paradise()



        



