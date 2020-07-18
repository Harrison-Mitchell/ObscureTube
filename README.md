# ObscureTube
Generates a montage of [action-packed](https://github.com/Harrison-Mitchell/Interestingness) 1.5s videos about the supplied topic for youtube videos uploaded today that have less than 50 views.

### The pipeline:
1. A selenium (automated) browser goes to `m.youtube.com/search`, sets results to today only, and collects youtube video IDs from the first 25 pages that:
	1. Are less than 4 minutes
	2. Have less than 50 views
	3. Are limited to one video per user

2. Loops over all collected youtube IDs and:
	1. Downloads the video
	2. Extracts the framerate
	3. Extracts the size of each frame (as in bytes)
	4. Finds the 1.5s window with the most action [(see `interestingness`)](https://github.com/Harrison-Mitchell/Interestingness)
	5. Slices the full video to this 1.5s slice
	6. Ensures the 1.5s slice has sufficient audio

3. 1.5s clips are joined into a single video

### Dependencies
* \*nix with Bash
* Python >= 3.5
* dateutil, xmltodict, requests (`pip install python-dateutil xmltodict requests`)
* youtube-dl, ffmpeg (`sudo apt install youtube-dl ffmpeg`)

### Usage
`./ObscureTube "search term"`

### Example output
[Resulting Video](https://youtu.be/QNlleACB3fI)
```
$ ./ObscureTube cockatoo
Spinning up a browser > Searching...
Downloading pUh-oW5iG2E > Sucking Frames > Finding Actionest 1.5s > Writing Slice > Saved
Downloading 4dttNoJ5Vd8 > Sucking Frames > Finding Actionest 1.5s > Writing Slice > Too quiet, deleted.
...
Downloading 4LSWnekuXSE > Sucking Frames > Finding Actionest 1.5s > Writing Slice > Saved
Done! joined.mkv ready

```