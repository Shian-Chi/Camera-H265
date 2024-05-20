# -*- coding: UTF-8 -*-

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GLib, GstRtspServer

# 初始化 GStreamer
Gst.init(None)

# 创建 GstRtspServer 服务器
server = GstRtspServer.RTSPServer()
server.set_service('8080')
# 创建 GstRTSPMediaFactory
factory = GstRtspServer.RTSPMediaFactory()

# 设置 GStreamer 管道，用于同时进行 RTSP 传输和本地视频录制
gst_pipeline = (
    "nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1280,height=720,framerate=30/1 ! "
    "tee name=t "
    "t. ! queue ! nvvidconv ! nvv4l2h265enc ! h265parse ! rtph265pay name=pay0 pt=96 "
    "t. ! queue ! nvvidconv ! nvv4l2h265enc bitrate=8000000 ! h265parse ! matroskamux ! filesink location=recorded_video.mkv"
)

factory.set_launch(gst_pipeline)
factory.set_shared(True)

# 设置 RTSP 媒体工厂的挂载点路径
server.get_mount_points().add_factory("/test", factory)

# 启动服务器
server.attach(None)

print("RTSP server is ready and recording")

# 设置 GLib 主循环，以处理 GStreamer 事件
main_loop = GLib.MainLoop()
try:
    main_loop.run()
except KeyboardInterrupt:
    print("Shutting down...")
    main_loop.quit()
