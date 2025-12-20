#!/bin/bash
# Stereo capture for two AITRIOS IMX500 cameras on Raspberry Pi 5

# Output files
CAM0_OUTPUT="/home/pi/cam0.h264"
CAM1_OUTPUT="/home/pi/cam1.h264"

# Start CAM0 (index 0)
rpicam-vid --camera 0 --mode 2028:1520:10:P --framerate 30 -t 0 -o "$CAM0_OUTPUT" &
CAM0_PID=$!

# Start CAM1 (index 1)
rpicam-vid --camera 1 --mode 2028:1520:10:P --framerate 30 -t 0 -o "$CAM1_OUTPUT" &
CAM1_PID=$!

echo "Both cameras running..."
echo "CAM0 PID: $CAM0_PID"
echo "CAM1 PID: $CAM1_PID"
echo "Press CTRL+C to stop recording"

# Wait for both processes
wait $CAM0_PID $CAM1_PID
