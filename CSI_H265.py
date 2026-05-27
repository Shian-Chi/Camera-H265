# -*- coding: UTF-8 -*-

import sys
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GLib, GstRtspServer
import socket


def get_local_ip():
    """建立臨時 socket 連線以取得本機 IP 位址"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('8.8.8.8', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
    return ip


PORT = '8554'
FACTORY_NAME = '/test'
HOST = get_local_ip()

# 初始化 GStreamer，失敗時立即終止
ok, _ = Gst.init_check(None)
if not ok:
    print("錯誤：GStreamer 初始化失敗", file=sys.stderr)
    sys.exit(1)

# 建立 RTSP 伺服器
server = GstRtspServer.RTSPServer()
server.set_service(PORT)

# 建立媒體工廠
factory = GstRtspServer.RTSPMediaFactory()

# CSI 攝影機 pipeline（MIPI-CSI，H.265 編碼）
factory.set_launch(
    "nvarguscamerasrc sensor-id=0 ! "
    "video/x-raw(memory:NVMM),width=720,height=480,framerate=25/1 ! "
    "nvvidconv ! nvv4l2h265enc ! h265parse ! rtph265pay name=pay0 pt=96"
)

# USB 攝影機 pipeline（備用，取消下方註解並將上方 pipeline 註解掉即可切換）
# factory.set_launch(
#     "v4l2src device=/dev/video1 ! "
#     "image/jpeg,width=1280,height=720,framerate=30/1 ! "
#     "jpegdec ! nvvidconv ! nvv4l2h265enc ! h265parse ! rtph265pay name=pay0 pt=96"
# )

factory.set_shared(True)

# 設定掛載點並啟動伺服器
server.get_mount_points().add_factory(FACTORY_NAME, factory)
server.attach(None)

print(f"RTSP 伺服器已就緒：rtsp://{HOST}:{PORT}{FACTORY_NAME}")

# 啟動 GLib 主迴圈以處理 GStreamer 事件
main_loop = GLib.MainLoop()
try:
    main_loop.run()
except KeyboardInterrupt:
    print("\n伺服器已停止")
