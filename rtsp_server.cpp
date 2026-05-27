#include <gst/gst.h>
#include <gst/rtsp-server/rtsp-server.h>

int main(int argc, char *argv[]) {
    gst_init(&argc, &argv);

    // Create the main loop
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);

    // Create RTSP server
    GstRTSPServer *server = gst_rtsp_server_new();
    g_object_set(server, "service", "8080", NULL);

    // Create a factory for the media
    GstRTSPMediaFactory *factory = gst_rtsp_media_factory_new();
    // USB webcam + NVIDIA NVENC H.265 (desktop/laptop with NVIDIA GPU)
    gst_rtsp_media_factory_set_launch(factory,
        "( "
        "v4l2src device=/dev/video0 do-timestamp=true ! "
        "image/jpeg,width=1280,height=720,framerate=30/1 ! "
        "queue leaky=downstream max-size-buffers=1 max-size-bytes=0 max-size-time=0 ! "
        "jpegdec ! videoconvert ! video/x-raw,format=NV12 ! "
        "queue leaky=downstream max-size-buffers=1 max-size-bytes=0 max-size-time=0 ! "
        "nvh265enc zerolatency=true preset=low-latency-hp rc-mode=cbr bitrate=4000 gop-size=30 rc-lookahead=0 ! "
        "h265parse config-interval=1 ! "
        "rtph265pay name=pay0 pt=96 config-interval=1 "
        ")");

    // Jetson CSI camera (nvarguscamerasrc + nvv4l2h265enc), not available on desktop:
    // gst_rtsp_media_factory_set_launch(factory,
    //     "( "
    //     "nvarguscamerasrc sensor-id=0 ! "
    //     "video/x-raw(memory:NVMM),width=1280,height=720,framerate=60/1 ! "
    //     "nvvidconv ! nvv4l2h265enc ! h265parse ! "
    //     "rtph265pay name=pay0 pt=96 "
    //     ")");

    gst_rtsp_media_factory_set_shared(factory, FALSE);
    gst_rtsp_media_factory_set_suspend_mode(factory, GST_RTSP_SUSPEND_MODE_NONE);

    // Attach the factory to a mount point
    GstRTSPMountPoints *mounts = gst_rtsp_server_get_mount_points(server);
    gst_rtsp_mount_points_add_factory(mounts, "/test", factory);
    g_object_unref(mounts);

    // Attach the server to the default main context
    guint source_id = gst_rtsp_server_attach(server, NULL);
    if (source_id == 0) {
        g_printerr("Failed to bind RTSP server on 0.0.0.0:8080\n");
        g_main_loop_unref(loop);
        g_object_unref(server);
        return 1;
    }

    g_print("RTSP server is ready at rtsp://127.0.0.1:8080/test\n");

    // Enter the main loop
    g_main_loop_run(loop);

    // Clean up
    g_main_loop_unref(loop);
    g_object_unref(server);

    return 0;
}
