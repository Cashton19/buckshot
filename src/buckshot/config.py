from pathlib import Path
import pygame as py

py.display.init()
_display_info = py.display.Info()
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR.parent / "assets"
SCREEN_WIDTH = _display_info.current_w
SCREEN_HEIGHT = _display_info.current_h
FPS = 60