# videoconverter
Wrapper around ffmpeg to convert a batch of raw MTS videos

# Requires
ffmpeg

# What does it do
Launch multiple ffmpeg child process to convert group of video files.

# Configuration
Number of FORK should match the number of CPU cores on the system.

# How to use it
Convert all the MTS files in source_dir:
  python2 convert.py [-d <destination_directory>] <source_dir>
