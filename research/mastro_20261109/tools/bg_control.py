#!/usr/bin/env python3
"""Screen/keyboard/mouse control restricted to the private Xvfb session."""
import argparse
import ctypes as C
import json
import os
from pathlib import Path
import time
import subprocess


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--session", type=Path, required=True)
    p.add_argument("operation", choices=("capture", "click", "right-click", "key", "text"))
    p.add_argument("arguments", nargs="*")
    a = p.parse_args()
    state = json.loads(a.session.read_text())
    env = state["environment"]
    display = env["DISPLAY"]
    if int(display.removeprefix(":")) < 50 or display != env.get("MASTRO_BACKGROUND_DISPLAY"):
        raise ValueError("Refusing a non-background display")
    os.environ.update(env)
    if a.operation == "capture":
        from PIL import ImageGrab
        ImageGrab.grab(xdisplay=display).save(a.arguments[0])
        return
    x = C.CDLL("libX11.so.6")
    xt = C.CDLL("libXtst.so.6")
    x.XOpenDisplay.argtypes = [C.c_char_p]; x.XOpenDisplay.restype = C.c_void_p
    x.XStringToKeysym.argtypes = [C.c_char_p]; x.XStringToKeysym.restype = C.c_ulong
    x.XKeysymToKeycode.argtypes = [C.c_void_p, C.c_ulong]; x.XKeysymToKeycode.restype = C.c_uint
    x.XFlush.argtypes = [C.c_void_p]; x.XCloseDisplay.argtypes = [C.c_void_p]
    xt.XTestFakeMotionEvent.argtypes = [C.c_void_p, C.c_int, C.c_int, C.c_int, C.c_ulong]
    xt.XTestFakeButtonEvent.argtypes = [C.c_void_p, C.c_uint, C.c_int, C.c_ulong]
    xt.XTestFakeKeyEvent.argtypes = [C.c_void_p, C.c_uint, C.c_int, C.c_ulong]
    d = x.XOpenDisplay(display.encode())
    if not d:
        raise RuntimeError("Cannot reach isolated display")
    def key(name, down):
        symbol = x.XStringToKeysym(name.encode())
        code = x.XKeysymToKeycode(d, symbol)
        if not code:
            raise ValueError("Unknown key: " + name)
        xt.XTestFakeKeyEvent(d, code, int(down), 0)
    try:
        if a.operation in {"click", "right-click"}:
            px, py = map(int, a.arguments)
            if not 0 <= px < 1920 or not 0 <= py < 1080:
                raise ValueError("Point outside background framebuffer")
            xt.XTestFakeMotionEvent(d, -1, px, py, 0)
            button = 3 if a.operation == "right-click" else 1
            xt.XTestFakeButtonEvent(d, button, 1, 0); xt.XTestFakeButtonEvent(d, button, 0, 0)
        elif a.operation == "key":
            pressed = []
            try:
                for name in a.arguments:
                    key(name, True); pressed.append(name)
            finally:
                for name in reversed(pressed):
                    key(name, False)
        elif a.operation == "text":
            for char in a.arguments[0]:
                if not 32 <= ord(char) <= 126:
                    raise ValueError("Use native text controls for non-ASCII input")
                shift = char.isupper() or char in '~!@#$%^&*()_+{}|:"<>?'
                name = "space" if char == " " else char
                if shift: key("Shift_L", True)
                try: key(name, True); key(name, False)
                finally:
                    if shift: key("Shift_L", False)
        x.XFlush(d)
        time.sleep(.2)
        from PIL import ImageGrab
        ImageGrab.grab(xdisplay=display).save(a.session.parent / "last-screen.png")
        helper = Path(__file__).with_name("wine_controls.py")
        check = subprocess.run(["python3", str(helper), "--prefix", env["WINEPREFIX"], "list"],
                               env=dict(os.environ), capture_output=True, text=True, timeout=20)
        if check.returncode:
            raise RuntimeError("Background UI check failed: " + check.stderr[:2000])
    finally:
        x.XCloseDisplay(d)


if __name__ == "__main__":
    main()
