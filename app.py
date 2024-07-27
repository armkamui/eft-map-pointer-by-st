from tabs import map_drawer
import streamlit as st
import time, os, asyncio
import shutil  # Import shutil for directory removal

map_drawer = map_drawer.MapDrawer()

async def remove_tempfiles():
    try:
        shutil.rmtree("./tmp/")  # Use shutil.rmtree for removing directories
        st.success("Removed temp files", icon="🗑️")
    except FileNotFoundError:
        st.warning("No temp files to remove", icon="🗑️")

async def main():
    st.set_page_config(
        page_title="EFT Helper Tool",
        page_icon="🛠️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    tab1, tab2 = st.tabs(["🗺️ Map Drawer", "🗺️ Map Pointer"])
    with tab1:
        map_drawer.main()
        btn_clear = st.button("累積データ削除")
        if btn_clear:
            await remove_tempfiles()
    with tab2:
        st.write("Map Pointer")
        st.write("Coming soon...")
    

if __name__ == "__main__":
    asyncio.run(main())  # Call asyncio.run(main()) to execute the coroutine