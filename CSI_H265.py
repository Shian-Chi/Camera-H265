# -*- coding: UTF-8 -*-

#sudo apt-get update
#sudo apt-get install libgstrtspserver-1.0-0


import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer','1.0')
from gi.repository import Gst, GLib, GstRtspServer
import socket


def get_local_ip():
    # 建立一個臨時的 socket 連接以確定本地 IP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # 使用一個不存在的地址 8.8.8.8 進行嘗試連接
        try:
            s.connect(('8.8.8.8', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
    return IP


port = '8080'
factoryName = '/test'
host = get_local_ip()

# 初始化GStreamer
Gst.init(None)

# 创建GstRtspServer服务器
server = GstRtspServer.RTSPServer()
server.set_service(port)
# 创建GstRTSPMediaFactory
factory = GstRtspServer.RTSPMediaFactory()

factory.set_launch("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=720,height=480,framerate=25/1 ! nvvidconv ! nvv4l2h265enc ! h265parse ! rtph265pay name=pay0 pt=96")
# 開啓 CSI 鏡頭


#factory.set_launch("v4l2src device=/dev/video1 ! image/jpeg,width=1280,height=720,framerate=30/1 ! jpegdec ! nvvidconv ! nvv4l2h265enc ! h265parse ! rtph265pay name=pay0 pt=96")
# 開啓 USB 鏡頭

factory.set_shared(True)

# 设置RTSP媒体工厂的挂载点路径
server.get_mount_points().add_factory(factoryName, factory)

# 启动服务器
server.attach(None)

print(f"RTSP server is ready at rtsp://{host}:{port}{factoryName}")

# 设置GLib主循环，以处理GStreamer事件
main_loop = GLib.MainLoop()
try:
    main_loop.run()
except KeyboardInterrupt:
    pass
    pass

