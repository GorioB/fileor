# fileor
File Organizing Framework

The idea behind this project is to create a framework that takes a cluttered data storage (local or remote) and arranges it based on a set of filters. Duplicates are detected by taking the md5 hash of the file and comparing it with other processed files.
Data stores and filters can be added as libraries in the stores and filters folders, respectively.
Currently, the only supported data store is the local filesystem and only the music and pictures filters work.
Several instances of the program should be able to run concurrently, but right now there may be collisions when dealing with the hash record-keeping.

Requirements
------------
`pip install -r requirements.txt`

Some dependencies are only required for the movie filter, which isn't working.

Usage
-----

Set path of the folder to be organized and the directory to move organized files in stores/local_store/config.py.

Then it's just a simple matter of running main.py
