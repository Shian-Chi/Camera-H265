# CSI-Camera-H26

Use MIPI-CSI camera read image use H.265 transmission

# Installation
GStreamer
Reference: https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c
```shell
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

RTSP server
```shell
sudo apt-get update
sudo apt-get install libgstrtspserver-1.0-0
sudo apt-get install gir1.2-gst-rtsp-server-1.0
```
