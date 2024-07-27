from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import io
from pathlib import Path
import requests
import cv2
import base64
import uuid
import re
import os
import time

class MapDrawer:
    def __init__(self):
        st.session_state["button_id"] = ""

    def get_map_image_from_name(self, map_name):
        image_path_dict = {
            "FACTORY": "image/FACTORY.webp",
            "WOODS": "image/WOODS.webp",
            "CUSTOMS": "image/CUSTOMS.jpg",
            "SHORELINE": "image/SHORELINE.webp",
            "INTERCHANGE": "image/INTERCHANGE.webp",
            "THE LAB": "image/THE LAB.webp",
            "RESERVE": "image/RESERVE.webp",
            "LIGHTHOUSE": "image/LIGHTHOUSE.webp",
            "STREETS OF TARKOV": "image/STREETS OF TARKOV.webp",
            "GROUND ZERO": "image/GROUND ZERO.webp"
        }
        # images_path = Path(dir)
        # image_path = images_path.glob(map_name + ".*")
        try:
            return Image.open(image_path_dict[map_name])
        except StopIteration:
            st.error(f"{map_name} に対応する画像が見つかりません。")
            return None

    # def get_map_image_from_name(self, map_name):
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

    def png_export(self, data, bg_img):
        try:
            Path("tmp/").mkdir()
        except FileExistsError:
            pass

        # Regular deletion of tmp files
        # Hopefully callback makes this better
        now = time.time()
        N_HOURS_BEFORE_DELETION = 1
        for f in Path("tmp/").glob("*.png"):
            # st.write(f, os.stat(f).st_mtime, now)
            if os.stat(f).st_mtime < now - N_HOURS_BEFORE_DELETION * 3600:
                Path.unlink(f)

        if st.session_state["button_id"] == "":
            st.session_state["button_id"] = re.sub(
                "\d+", "", str(uuid.uuid4()).replace("-", "")
            )

        button_id = st.session_state["button_id"]
        file_path = f"tmp/{button_id}.png"

        custom_css = f""" 
            <style>
                #{button_id} {{
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    background-color: rgb(255, 255, 255);
                    color: rgb(38, 39, 48);
                    padding: .25rem .75rem;
                    position: relative;
                    text-decoration: none;
                    border-radius: 4px;
                    border-width: 1px;
                    border-style: solid;
                    border-color: rgb(230, 234, 241);
                    border-image: initial;
                }} 
                #{button_id}:hover {{
                    border-color: rgb(246, 51, 102);
                    color: rgb(246, 51, 102);
                }}
                #{button_id}:active {{
                    box-shadow: none;
                    background-color: rgb(246, 51, 102);
                    color: white;
                    }}
            </style> """

        if data is not None and data.image_data is not None:
            img_data = data.image_data
            im = Image.fromarray(img_data.astype("uint8"), mode="RGBA")

            # Convert background image to RGBA 
            bg_img = bg_img.convert("RGBA") 

            # Check and resize if necessary
            if im.size != bg_img.size:
                bg_img = bg_img.resize(im.size) 

            im = Image.composite(im, bg_img, im)
            im.save(file_path, "PNG")

            buffered = io.BytesIO()
            im.save(buffered, format="PNG")
            img_data = buffered.getvalue()
            try:
                # some strings <-> bytes conversions necessary here
                b64 = base64.b64encode(img_data.encode()).decode()
            except AttributeError:
                b64 = base64.b64encode(img_data).decode()

            dl_link = (
                custom_css
                + f'<a download="{file_path}" id="{button_id}" href="data:file/txt;base64,{b64}">画像ダウンロード</a><br></br>'
            )
            st.markdown(dl_link, unsafe_allow_html=True)

    def main(self):

        if "memo" not in st.session_state:
            st.session_state.memo = ""

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
            # "マーカーの形式", ("point", "freedraw", "line", "rect", "circle", "transform")
            "マーカーの形式", ('freedraw', 'transform', 'line', 'rect', 'circle', 'polygon')
        )

        stroke_width = st.sidebar.slider("マーカーの大きさ", 1, 25, 3)
        # if drawing_mode == 'point':
        #     point_display_radius = st.sidebar.slider("点の大きさ", 1, 25, 3)
        stroke_color = st.sidebar.color_picker("マーカーの色", "#FF0000")

        realtime_update = st.sidebar.checkbox("リアルタイム更新", True)

        img = self.get_map_image_from_name(selected_map)

        st.header("マップ", divider="blue")
        with st.spinner("マップを読み込んでいます..."):
            canvas_result = st_canvas(
                    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                    stroke_width=stroke_width,
                    stroke_color=stroke_color,
                    width=1200,
                    height=800,
                    background_image=img if selected_map else None,
                    update_streamlit=realtime_update,
                    drawing_mode=drawing_mode,
                    # point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
                    key="canvas",
            )
        self.png_export(canvas_result, img)

        col1, col2 = st.columns([2, 1])
        with col1:
            st.header("必要アイテム登録", divider="orange")
            df = pd.DataFrame(columns=['名前','個数','目的','色', 'チェック'])
            purpose = ['task', 'market', 'hideout', 'other']
            number = [str(i) for i in range(1, 101)]
            colors = ['赤', '青', '緑', '黄', '紫', 'オレンジ', 'ピンク', '黒', '白', '茶', 'なし']
            config = {
                '名前' : st.column_config.TextColumn('アイテム名', width='large', required=True),
                '個数' : st.column_config.SelectboxColumn('個数', options=number, default="1"),
                '目的' : st.column_config.SelectboxColumn('用途', options=purpose, default='task'),
                '色' : st.column_config.SelectboxColumn('色', options=colors, default='なし'),
                'チェック' : st.column_config.CheckboxColumn('チェック', default=False)
            }

            search_item = st.data_editor(df, column_config = config, num_rows='dynamic')

            # if st.button('登録') and st.session_state.flag == False:
            #     with st.spinner("登録中..."):
            #         st.header("アイテム一覧", divider="blue")
            #         st.write(st.session_state.search_item)

        with col2:
            st.header("メモ", divider="green")
            df = pd.DataFrame(
                [
                {"メモ": "memo", "備考": "xxx", "チェック": True},
            ]
            )
            edited_df = st.data_editor(df, num_rows="dynamic")

        st.header("リンク集", divider="red")
        col3, col4 = st.columns([1, 1])
        with col3:
            st.markdown(
                """
                - English
                    - [Wiki Home](https://escapefromtarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki)
                    - [Maps](https://mapgenie.io/tarkov/maps/woods)
                    - [Item Database](https://tarkov.dev/items)
                    - [Goon Tracker](https://www.goon-tracker.com/pvetracker)
                    - [Tarkov Help](https://tarkov.help/en/)
                """
            )

        with col4:
            st.markdown(
                """
                - 日本語
                    - [納品アイテムまとめ](https://gamelabs.jp/games/tarkov/202402013859/#index_id1)
                    - [Wiki ホーム](https://wikiwiki.jp/eft/)
                    - [Wiki PvE情報](https://wikiwiki.jp/eft/PvE%20ZONE)
                    - [Praporのタスク](https://wikiwiki.jp/eft/Prapor)
                    - [Therapistのタスク](https://wikiwiki.jp/eft/Therapist)
                    - [Skierのタスク](https://wikiwiki.jp/eft/Skier)
                    - [Peacekeeperのタスク](https://wikiwiki.jp/eft/Peacekeeper)
                    - [Mechanicのタスク](https://wikiwiki.jp/eft/Mechanic)
                    - [Jaegerのタスク](https://wikiwiki.jp/eft/Jaeger)
                """
            )