# -*- coding: utf-8 -*-

import gi
import signal
import sys
import os
import time

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# 初始化GStreamer
Gst.init(None)


# 確保輸出目錄存在
output_directory = "/home/ubuntu/CSI_Camera_H265/recordings"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# 建立錄製的輸出檔名基礎模板
current_time = time.strftime("%Y%m%d_%H%M%S")
output_file_template = os.path.join(output_directory, f"recorded_video_{current_time}_test_%04d.mkv")


# 定義GStreamer的管線，使用splitmuxsink來自動分割檔案
pipeline = Gst.parse_launch(
    f"rtspsrc location=rtsp://127.0.0.1:8080/test latency=0 name=source ! "
    f"queue ! rtph265depay ! h265parse ! "
    f"splitmuxsink location={output_file_template} max-size-time=100000000000" # 300秒轉換為 nanoseconds
)


# 管線狀態變化時的回調函數
def on_state_changed(bus, msg):
    old, new, pending = msg.parse_state_changed()
    if msg.src == pipeline and new == Gst.State.PLAYING:
        print("Recording started...")


# 設定訊號處理函數，以處理中斷訊號
def signal_handler(sig, frame):
    print('Stopping recording, please wait...')
    # 發送 EOS 訊號
    pipeline.send_event(Gst.Event.new_eos())

    # 等待 EOS 訊息處理完成
    bus.timed_pop_filtered(3000000000, Gst.MessageType.EOS)

    # 設置管線狀態為 NULL
    pipeline.set_state(Gst.State.NULL)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# 定義一個結束事件的回調函數
def on_eos(bus, msg):
    print("End-of-stream")
    loop.quit()


# 定義一個錯誤事件的回調函數
def on_error(bus, msg):
    error = msg.parse_error()
    print(f"Error: {error[1]}")
    loop.quit()


# 啟動管線
pipeline.set_state(Gst.State.PLAYING)
print("Starting recording...")  # 立即顯示，即使實際上的準備可能還在進行中


# 建立GLib主循環並監聽管線的事件
loop = GLib.MainLoop()
bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message::eos", on_eos)
bus.connect("message::error", on_error)
bus.connect("message::state-changed", on_state_changed)  # 監聽狀態變化事件

try:
    loop.run()
except KeyboardInterrupt:
    pass
finally:
    # 停止管線並進行清理
    pipeline.set_state(Gst.State.NULL)
