# CSI-Camera-H.265

[English](#english) | [中文](#中文)

---

<a name="english"></a>

RTSP streaming and recording tools for **NVIDIA Jetson** boards (Nano / Xavier / Orin) using a MIPI-CSI camera and Jetson hardware H.265 encoding (`nvv4l2h265enc`). A USB webcam alternative (`USB_H265.py`) is also included for non-Jetson devices.

Stream URL: `rtsp://<device-ip>:8080/test`

---

## Files

| File | Purpose |
|---|---|
| `CSI_H265.py` | RTSP server — streams CSI camera (NVIDIA Jetson hardware encoding) |
| `USB_H265.py` | RTSP server — streams USB camera with software x265enc (no NVIDIA required) |
| `tee_rtsp_recording.py` | RTSP server — streams **and** simultaneously records to `recorded_video.mkv` |
| `cv_gst.py` | OpenCV viewer — displays the RTSP stream in a window |
| `recording.py` | Recorder — pulls RTSP stream, saves split MKV segments |
| `recording_timeout.py` | Recorder — same as `recording.py`, with clean EOS shutdown on Ctrl+C |
| `rtsp_server.cpp` | C++ RTSP server for desktop NVIDIA GPU (USB camera + `nvh265enc`) |

---

## Installation

### GStreamer

```bash
sudo apt-get install \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
  libgstreamer-plugins-bad1.0-dev \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
  gstreamer1.0-libav gstreamer1.0-tools
```

Reference: https://gstreamer.freedesktop.org/documentation/installing/on-linux.html

### RTSP server

```bash
sudo apt-get install libgstrtspserver-1.0-0 libgstrtspserver-1.0-dev gir1.2-gst-rtsp-server-1.0
```

### x265 (for USB_H265.py only)

```bash
sudo apt-get install gstreamer1.0-plugins-ugly
```

### Build the C++ server (optional)

```bash
g++ rtsp_server.cpp -o rtsp_server \
  $(pkg-config --cflags --libs gstreamer-1.0 gstreamer-rtsp-server-1.0)
```

---

## Usage

### Stream only (Jetson CSI camera)

```bash
python CSI_H265.py
```

Pipeline: `nvarguscamerasrc → nvvidconv → nvv4l2h265enc → rtph265pay`

### Stream only (USB camera, no NVIDIA required)

```bash
python USB_H265.py
```

Pipeline: `v4l2src → jpegdec → videoconvert → x265enc → rtph265pay`

### Stream + simultaneous local recording

```bash
python tee_rtsp_recording.py
```

Uses a `tee` element to split the encoded stream: one branch goes to RTSP clients, the other is muxed into `recorded_video.mkv` at 8 Mbps.

### View the stream

```bash
python cv_gst.py
```

Decodes with `nvv4l2decoder` (Jetson hardware), displays in an OpenCV window. Press `q` or `ESC` to quit.

### Record from RTSP to split MKV files

```bash
python recording_timeout.py   # recommended — clean shutdown with Ctrl+C
python recording.py           # simpler version
```

Saves to `/home/ubuntu/CSI_Camera_H265/recordings/` as `recorded_video_<timestamp>_test_NNNN.mkv`. Files split every 100 seconds. `recording_timeout.py` sends an EOS event on `SIGINT` so the final segment is properly closed before exit.

---

## GStreamer Pipelines

**CSI_H265.py**
```
nvarguscamerasrc → video/x-raw(NVMM) → nvvidconv → nvv4l2h265enc → h265parse → rtph265pay
```

**USB_H265.py**
```
v4l2src → image/jpeg → jpegdec → videoconvert → x265enc → rtph265pay
```

**tee_rtsp_recording.py**
```
nvarguscamerasrc → tee ┬→ nvvidconv → nvv4l2h265enc → rtph265pay           (RTSP)
                        └→ nvvidconv → nvv4l2h265enc → h265parse → matroskamux → filesink  (MKV)
```

**recording.py / recording_timeout.py**
```
rtspsrc → rtph265depay → h265parse → splitmuxsink (MKV segments)
```

**cv_gst.py**
```
rtspsrc → rtph265depay → h265parse → nvv4l2decoder → nvvidconv → videoconvert → appsink
```

---

<a name="中文"></a>

# CSI-Camera-H.265（中文說明）

針對 **NVIDIA Jetson**（Nano / Xavier / Orin）開發板的 RTSP 串流與錄影工具組，使用 MIPI-CSI 攝影機與 Jetson 硬體 H.265 編碼（`nvv4l2h265enc`）。另附 `USB_H265.py` 供無 Jetson 硬體的設備使用。

串流網址：`rtsp://<裝置 IP>:8080/test`

---

## 檔案說明

| 檔案 | 用途 |
|---|---|
| `CSI_H265.py` | RTSP 伺服器 — 使用 NVIDIA Jetson 硬體編碼串流 CSI 攝影機 |
| `USB_H265.py` | RTSP 伺服器 — USB 攝影機，使用軟體 x265enc（不需 NVIDIA）|
| `tee_rtsp_recording.py` | RTSP 伺服器 — 串流的同時錄製至 `recorded_video.mkv` |
| `cv_gst.py` | OpenCV 播放器 — 在視窗中顯示 RTSP 串流畫面 |
| `recording.py` | 錄影程式 — 從 RTSP 拉流，存成分割 MKV 片段 |
| `recording_timeout.py` | 錄影程式 — 同上，Ctrl+C 時透過 EOS 正確關閉最後片段 |
| `rtsp_server.cpp` | 桌機 NVIDIA GPU 的 C++ RTSP 伺服器（USB 攝影機 + `nvh265enc`）|

---

## 安裝

### GStreamer

```bash
sudo apt-get install \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
  libgstreamer-plugins-bad1.0-dev \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
  gstreamer1.0-libav gstreamer1.0-tools
```

參考：https://gstreamer.freedesktop.org/documentation/installing/on-linux.html

### RTSP 伺服器套件

```bash
sudo apt-get install libgstrtspserver-1.0-0 libgstrtspserver-1.0-dev gir1.2-gst-rtsp-server-1.0
```

### x265（僅 USB_H265.py 需要）

```bash
sudo apt-get install gstreamer1.0-plugins-ugly
```

### 編譯 C++ 伺服器（選用）

```bash
g++ rtsp_server.cpp -o rtsp_server \
  $(pkg-config --cflags --libs gstreamer-1.0 gstreamer-rtsp-server-1.0)
```

---

## 使用方式

### 僅串流（Jetson CSI 攝影機）

```bash
python CSI_H265.py
```

### 僅串流（USB 攝影機，不需 NVIDIA）

```bash
python USB_H265.py
```

### 串流 + 同步本地錄影

```bash
python tee_rtsp_recording.py
```

透過 `tee` 元件將編碼後的串流一分為二：一路送給 RTSP 客戶端，另一路以 8 Mbps 封裝成 `recorded_video.mkv`。

### 播放串流

```bash
python cv_gst.py
```

使用 `nvv4l2decoder`（Jetson 硬體解碼）在 OpenCV 視窗中顯示畫面。按 `q` 或 `ESC` 離開。

### 從 RTSP 錄影成分割 MKV

```bash
python recording_timeout.py   # 建議使用 — Ctrl+C 時正確寫入結尾
python recording.py           # 簡化版本
```

檔案存至 `/home/ubuntu/CSI_Camera_H265/recordings/`，每 100 秒自動分割一個新檔案。`recording_timeout.py` 在收到 `SIGINT` 時會先送出 EOS 事件，確保最後一個片段正常關閉再退出。

---

## GStreamer Pipeline 示意圖

**CSI_H265.py**
```
nvarguscamerasrc → video/x-raw(NVMM) → nvvidconv → nvv4l2h265enc → h265parse → rtph265pay
```

**USB_H265.py**
```
v4l2src → image/jpeg → jpegdec → videoconvert → x265enc → rtph265pay
```

**tee_rtsp_recording.py**
```
nvarguscamerasrc → tee ┬→ nvvidconv → nvv4l2h265enc → rtph265pay           （RTSP 串流）
                        └→ nvvidconv → nvv4l2h265enc → h265parse → matroskamux → filesink  （MKV 錄影）
```

**recording.py / recording_timeout.py**
```
rtspsrc → rtph265depay → h265parse → splitmuxsink（分割 MKV）
```

**cv_gst.py**
```
rtspsrc → rtph265depay → h265parse → nvv4l2decoder → nvvidconv → videoconvert → appsink
```
