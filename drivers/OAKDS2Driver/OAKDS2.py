#!/usr/bin/env python3
import depthai as dai


class OAKDS2:

    def __init__(self):
        self.visualizer = dai.RemoteConnection()
        # Create pipeline
        self.pipeline = dai.Pipeline()

        # Create camera node
        # Build method without arguments will use the default camera
        rgb_cam = self.pipeline.create(dai.node.Camera).build()

        # Request NV12 stream from the camera
        rgb_stream = rgb_cam.requestOutput(size=(1980, 1080), type=dai.ImgFrame.Type.NV12)

        # Add camera stream as a topic to the Visualizer
        self.visualizer.addTopic("rgb", rgb_stream)

        # Build and start the pipeline
        self.pipeline.start()

        # Register the pipeline graph to be visualized in the Visualizer
        self.visualizer.registerPipeline(self.pipeline)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pipeline.stop()