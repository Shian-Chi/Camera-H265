# -*- coding: UTF-8 -*-
# USB camera RTSP server — for devices WITHOUT NVIDIA hardware encoding
# Uses software x265enc instead of nvv4l2h265enc
# Stream URL: rtsp://<device-ip>:8080/test

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GLib, GstRtspServer
import socket


def get_local_ip():
    # 建立一個臨時的 socket 連接以確定本地 IP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('8.8.8.8', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
    return IP


port = '8080'
factoryName = '/test'
host = get_local_ip()

# 初始化 GStreamer
Gst.init(None)

# 建立 RTSP 伺服器
server = GstRtspServer.RTSPServer()
server.set_service(port)

# 建立媒體工廠
factory = GstRtspServer.RTSPMediaFactory()
factory.set_launch(
    "v4l2src device=/dev/video1 ! "
    "image/jpeg,width=1280,height=720,framerate=30/1 ! "
    "jpegdec ! videoconvert ! "
    "x265enc tune=zerolatency ! "
    "rtph265pay name=pay0 pt=96"
)
factory.set_shared(True)

# 掛載路徑並啟動伺服器
server.get_mount_points().add_factory(factoryName, factory)
server.attach(None)

print(f"RTSP server is ready at rtsp://{host}:{port}{factoryName}")

# GLib 主迴圈
main_loop = GLib.MainLoop()
try:
    main_loop.run()
except KeyboardInterrupt:
    pass
