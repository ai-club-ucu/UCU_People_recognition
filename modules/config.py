# VideoProccessor
max_contour_area_to_be_a_person =  5000
min_contour_area_to_be_a_person =  50


interesting_region_x_1 = 0
interesting_region_x_2 = 704

interesting_region_y_1 = 360
interesting_region_y_2 = 576


# PeopleDetector
frames_to_skip = 10
detector_images_parameters = {"winStride": (2, 2), "padding":(8, 8), "scale":1.05, "img_width": 400}
detector_video_parameters = {"winStride": (4, 4), "padding":(0, 0), "scale":1.05, "img_width": 600}