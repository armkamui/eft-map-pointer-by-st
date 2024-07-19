from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import io
from pathlib import Path

def get_map_image_from_name(map_name):
    dir = "main/image/"
    images_path = Path(dir)
    image_path = images_path.glob(map_name + ".*")
    print(images_path)
    try:
        return Image.open(next(image_path))
    except StopIteration:
        st.error(f"{map_name} に対応する画像が見つかりません。")
        return None

# def get_map_image_from_name(map_name):
#     map_dict = {
#         "FACTORY": "https://cdn.wikiwiki.jp/to/w/eft/img/::ref/FACTORY-MAP-2D_12.22.jpg.webp?rev=fe55ee0547237280a20632b6468d695d&t=20231011221810",
#         "WOODS": "https://cdn.wikiwiki.jp/to/w/eft/img/::ref/WOODS-ESC-MAP-2D_2023_05_27-JPNwiki_Ver1.2.jpg.webp?rev=c28f09ac1cb0fd773cd7897ab7b35439&t=20231122222812",
#         "CUSTOMS": "https://cdn.wikiwiki.jp/to/w/eft/img/::ref/CUSTOMS-ESC-MAP-2D_Ver0.12.12.jpg.webp?rev=672662095b34f61594db9b86cbfc27b4&t=20231021133946",
#         "SHORELINE": "https://cdn.wikiwiki.jp/to/w/eft/SHORELINE/::ref/Shoreline2DMapByMonkiUpdatedByJindouz%20%282%29.webp.webp?rev=7d2f3e62251e8895932e1e4ec8288286&t=20240624024459",
#         "INTERCHANGE": "https://cdn.wikiwiki.jp/to/w/eft/img/::ref/INTERCHANGE-ESC-MAP-2D_2022_04_09-%E8%84%B1%E5%87%BA%E5%9C%B0%E7%82%B9%E5%90%8D%E7%A7%B0%E4%BF%AE%E6%AD%A3%E7%89%88v1.0.jpg.webp?rev=1a6b87d9a672496fdcd15ff109db286b&t=20231105225004",
#         "THE LAB": "https://cdn.wikiwiki.jp/to/w/eft/img/::ref/LabsMapByMonkimonkimonk.webp.webp?rev=e36c8a165a15de38e30d5ecbf63753fe&t=20240304212758",
#         "RESERVE": "https://cdn.wikiwiki.jp/to/w/eft/img/::ref/RESERVE-ESC-MAP-2D_2023_02_28.jpg.webp?rev=6103dc0d0206c64a10600aef82536034&t=20231110161710",
#         "LIGHTHOUSE": "https://cdn.wikiwiki.jp/to/w/eft/img/::ref/lighthouse-task.jpg.webp?rev=c8eca19e92472b1b84654ffd47ce61bb&t=20220217214715",
#         "STREETS OF TARKOV": "https://cdn.wikiwiki.jp/to/w/eft/STREETS%20OF%20TARKOV/::ref/StreetsOfTarkov2DMapByJindouzV5_4.webp.webp?rev=6b5cbcb59d1d6ffeff993adcd6991ae5&t=20240514030539",
#         "GROUND ZERO": "https://preview.redd.it/hope-this-helps-my-ground-zero-map-v0-6ls2fw0hs39c1.jpg?width=1494&format=pjpg&auto=webp&s=d46f32273bb418c23d4380dec84233f63d82ff93"
#     }
#     return Image.open(io.BytesIO(requests.get(map_dict[map_name]).content))

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
