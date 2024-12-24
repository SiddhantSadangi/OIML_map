import pandas as pd
import plotly.express as px
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
from streamlit_geolocation import streamlit_geolocation

st.title("Odias in AI/ML Community Map ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️🗺️")

st_supabase_client = st.connection(
    name="SupabaseConnection",
    type=SupabaseConnection,
    ttl=None,
)


def get_data():
    return execute_query(st_supabase_client.table("users").select("*"), ttl=0)


def view_map():
    users = pd.DataFrame.from_dict(get_data().data, orient="columns")
    fig = px.scatter_map(
        users,
        lat="latitude",
        lon="longitude",
        hover_name="name",
        hover_data={"latitude": False, "longitude": False},
        zoom=1,
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        selection_mode=["box", "lasso"],
        on_select="rerun",
    )


def add_data():
    lcol, rcol = st.columns([2, 1])
    name = lcol.text_input("Name")
    with rcol:
        st.write("Click to get your location")
        location = streamlit_geolocation()

    if location["latitude"]:
        st.write(location)
        st.info("Location will be rounded to 2 decimal places for obscurity")
        if name and st.button("Add to map", type="primary", use_container_width=True):
            execute_query(
                st_supabase_client.table("users").insert(
                    [
                        {
                            "name": name,
                            # Round coordinates to 2 decimal places for obscurity
                            "latitude": round(location["latitude"], 2),
                            "longitude": round(location["longitude"], 2),
                        }
                    ]
                )
            )

            st.success(f"{name} added to the map")


page = st.navigation([st.Page(view_map, title="View Map"), st.Page(add_data, title="Add Data")])
page.run()
