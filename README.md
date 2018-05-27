# UCU Trapezna People Motion Heatmap

## Description
This project is created for visualizing and tracking people motion in UCU cafe Trapezna.
Based on amount of people and motion speed the program builds live video heatmap which
is simple for understanding. The project mostly is intended for UCU students who
want to avoid long queue when in Trapezna when they want to it. Heatmap will help to
find out how many people is currently in Trapezna.

## Installation
```bash
$ git clone https://github.com/andrwkoval/trapezna
$ cd trapezna
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

## Usage
```
$ cd .../trapezna
$ source venv/bin/activate
$ python3 VideoProcessor.py
```

## Input data
path_file - path to the video to get Heatmap.

## Output data
Live video heatmap.
![Example of heatmap](https://github.com/andrwkoval/trapezna/blob/master/examples/screenshot.jpg)

## Project Structure
1. Assets (screenshots and images of working examples)
2. config.py (specific configurations for people tracking)
3. PeopleDetector.py
    * detect_people (detects people in specific area and circles them using
    rectangles)
    * count_people (based on detected people returns amount of them)
4. utils.py (parses date and time from name of the file)
5. VideoProcessor.py (main module for image and video processing)
    * crop_interesting_region (specifies a region on the frame for better interaction)
    * leave_only_persons (colors the regions without people in black)
    * process_frame (thresholds a given frame to use in further processing)
    * adjust_gamma (brightens the frame)
    * prepare_frame (uses Gaussian Blur and histogram equalization to prepare frame for heatmap)
    * compare_with_prev (compares current frame with previous to get the difference in pixels thus get the motion trace)
    * make_heatmap (gets the frame and adds the previous motion, then colours the difference in pixels)
    * initialize (copies current frame)
    * get_next_frame (gets next frame)
    * show_video (visualizes the heatmap and resets traces every 220 frames)

## Contributing
- Fork it (https://github.com/andrwkoval/trapezna/fork)
- Create your feature branch (git checkout -b feature/fooBar)
- Commit your changes (git commit -am 'Add some fooBar')
- Push to the branch (git push origin feature/fooBar)
- Create a new Pull Request

## Contacts:
- Yuriy Yelisjejev
    * https://github.com/YuraYelisieiev/
    * yeliseev@ucu.edu.ua
- Andrii Koval
    * https://github.com/andrwkoval/
    * andykoval@ucu.edu.ua


