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

class MapPointer:
    def __init__(self):
        self.map_pointer = st.empty()
        self.map_pointer.image = None
        self.map_pointer.image_path = None
        self.map_pointer.image_url = None
        self.map_pointer.image_file
    
    def main(self):
        st.title("Map Pointer")
        st.write("Coming soon...")