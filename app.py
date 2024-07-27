from tabs import map_drawer
import streamlit as st
import shutil  # Import shutil for directory removal

map_drawer = map_drawer.MapDrawer()

st.set_page_config(
    page_title="EFT Helper Tool",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def remove_tempfiles():
    try:
        shutil.rmtree("./tmp/")  # Use shutil.rmtree for removing directories
        st.success("Removed temp files", icon="🗑️")
    except FileNotFoundError:
        st.warning("No temp files to remove", icon="🗑️")

def main():
    tab1, tab2 = st.tabs(["🗺️ Map Drawer", "🗺️ Map Pointer"])
    with tab1:
        map_drawer.main()
        btn_clear = st.button("累積データ削除")
        if btn_clear:
            remove_tempfiles()
    with tab2:
        # map_pointer.main()
        st.write("Coming soon...")
    

if __name__ == "__main__":
    main() # Call asyncio.run(main()) to execute the coroutine