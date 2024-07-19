# -*- mode: python ; coding: utf-8 -*-
import site
import os

block_cipher = None

assert len(site.getsitepackages()) > 0

package_path = site.getsitepackages()[0]
for p in site.getsitepackages():
    if "site-package" in p:
        package_path = p
        break

a = Analysis(
    ['run_main.py'],
    pathex=[],
    binaries=[],
    datas=[(os.path.join(package_path, "streamlit/static"), "./streamlit/static"),
        (os.path.join(package_path, "streamlit/runtime"), "./streamlit/runtime")],
    hiddenimports=['streamlit_drawable_canvas'],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='run_main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
