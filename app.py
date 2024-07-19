from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from pathlib import Path
import pandas as pd


def get_map_image_from_name(map_name):
    images_path = Path(r'.\image\\')
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

selected_map = st.sidebar.selectbox("マップ選択", maps)

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "マーカーの形式", ("point", "freedraw", "line", "rect", "circle", "transform")
)

stroke_width = st.sidebar.slider("マーカーの大きさ", 1, 25, 3)
if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider("点の大きさ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("マーカーの色", "#FF0000")

realtime_update = st.sidebar.checkbox("リアルタイム更新", True)

img = get_map_image_from_name(selected_map)

st.header("マップ", divider="blue")
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

st.header("必要アイテム登録", divider="blue")
df = pd.DataFrame(columns=['名前','個数','目的'])
purpose = ['task', 'market', 'hideout', 'other']
config = {
    '名前' : st.column_config.TextColumn('アイテム名', width='large', required=True),
    '個数' : st.column_config.NumberColumn('個', min_value=0, max_value=122),
    '目的' : st.column_config.SelectboxColumn('用途', options=purpose)
}

result = st.data_editor(df, column_config = config, num_rows='dynamic')

if st.button('登録'):
    st.header("アイテム一覧", divider="blue")
    st.write(result)
