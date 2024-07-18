from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from pathlib import Path


def get_map_image_from_name(map_name):
    images_path = Path("./image/")
    image_path = images_path.glob(map_name + ".*")
    return Image.open(next(image_path))

st.set_page_config(
    page_title="EFT Map Pointer",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🗺️ EFT Map Pointer")

maps = (
    "FACTORY",
    "WOODS",
    "CUSTOMS",
    "SHORELINE",
    "INTERCHANGE",
    "THE LAB",
    "RESERVE",
    "LIGHTHOUSE",
    "STREETS OF TARKOV",
    "GROUND ZERO"
)

selected_map = st.sidebar.selectbox("Map", maps)

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
)

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ", "#FF0000")

realtime_update = st.sidebar.checkbox("Update in realtime", True)

img = get_map_image_from_name(selected_map)

canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        width=1200,
        height=800,
        background_image=img if selected_map else None,
        update_streamlit=realtime_update,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
        key="canvas",
)

