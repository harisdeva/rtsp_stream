## Instruction for streaming the video

### with Ubuntu 20.04

### Step 1: Install FFmpeg with ```sudo apt install ffmpeg```

### Step 2: Download the the latest release of MediaMTX (formerly rtsp-simple-server) from https://github.com/bluenviron/mediamtx/releases

### Step 3: Extract the mediamtx_v1.4.2_linux_amd64.tar.gz file and start the streaming server with ```./mediamtx```

### Step 4: Now open a new terminal and publish the test video using ```ffmpeg -re -stream_loop -1 -i test.mp4 -c copy -f rtsp rtsp://localhost:8554/mystream```

### Step 5: Another new terminal, try running the code by ```./rtsp_stream.py```
