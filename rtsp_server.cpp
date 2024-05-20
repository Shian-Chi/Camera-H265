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
    gst_rtsp_media_factory_set_launch(factory,
        "( "
        "nvarguscamerasrc sensor-id=0 ! "
        "video/x-raw(memory:NVMM),width=1280,height=720,framerate=60/1 ! "
        "nvvidconv ! "
        "nvv4l2h265enc ! "
        "h265parse ! "
        "rtph265pay name=pay0 pt=96 "
        ")");

    // For USB camera, you would replace the factory set_launch call with something like:
    // gst_rtsp_media_factory_set_launch(factory,
    //     "( "
    //     "v4l2src device=/dev/video0 ! "
    //     "image/jpeg,width=1280,height=720,framerate=30/1 ! "
    //     "jpegdec ! "
    //     "nvvidconv ! "
    //     "nvv4l2h265enc ! "
    //     "h265parse ! "
    //     "rtph265pay name=pay0 pt=96 "
    //     ")");

    gst_rtsp_media_factory_set_shared(factory, TRUE);

    // Attach the factory to a mount point
    GstRTSPMountPoints *mounts = gst_rtsp_server_get_mount_points(server);
    gst_rtsp_mount_points_add_factory(mounts, "/test", factory);
    g_object_unref(mounts);

    // Attach the server to the default main context
    gst_rtsp_server_attach(server, NULL);

    g_print("RTSP server is ready at rtsp://127.0.0.1:8080/test\n");

    // Enter the main loop
    g_main_loop_run(loop);

    // Clean up
    g_main_loop_unref(loop);
    g_object_unref(server);
    g_object_unref(factory);

    return 0;
}

