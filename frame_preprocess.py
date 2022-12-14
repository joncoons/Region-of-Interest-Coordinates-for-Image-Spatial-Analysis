import numpy as np
import cv2
import math
        
def frame_resize(img, target, model):
    if model in ('acv', 'yolov5', 'classification'):
        padColor = [0,0,0]
        h, w = img.shape[:2]
        sh, sw = (target, target)
        if h > sh or w > sw: # shrinking 
            interp = cv2.INTER_AREA
        else: # stretching 
            interp = cv2.INTER_CUBIC
        aspect = w/h  
        # compute scaling and pad sizing
        if aspect > 1: # horizontal image
            new_w = sw
            new_h = np.round(new_w/aspect).astype(int)
            pad_vert = (sh-new_h)/2
            pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
            pad_left, pad_right = 0, 0
        elif aspect < 1: # vertical image
            new_h = sh
            new_w = np.round(new_h*aspect).astype(int)
            pad_horz = (sw-new_w)/2
            pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
            pad_top, pad_bot = 0, 0
        else: # square image
            new_h, new_w = sh, sw
            pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0
        scaled_frame = cv2.resize(img, (new_w, new_h), interpolation=interp)
        scaled_frame = cv2.copyMakeBorder(scaled_frame, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)        
        return scaled_frame
    elif model in ('faster_rcnn'):
        padColor = [0,0,0]
        h, w = img.shape[:2]
        sh, sw = (600, 800)
        if h > sh or w > sw: # shrinking 
            interp = cv2.INTER_AREA
        else: # stretching 
            interp = cv2.INTER_CUBIC
        aspect = w/h 
        if aspect > 1: # horizontal image
            new_w = sw
            new_h = np.round(new_w/aspect).astype(int)
            pad_vert = (sh-new_h)/2
            pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
            pad_left, pad_right = 0, 0
        elif aspect < 1: # vertical image
            new_h = sh
            new_w = np.round(new_h*aspect).astype(int)
            pad_horz = (sw-new_w)/2
            pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
            pad_top, pad_bot = 0, 0
        else: # square image
            new_h = sh
            new_w = np.round(new_h*aspect).astype(int)
            pad_horz = (sw-new_w)/2
            pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
            pad_top, pad_bot = 0, 0
        scaled_frame = cv2.resize(img, (new_w, new_h), interpolation=interp)
        scaled_frame = cv2.copyMakeBorder(scaled_frame, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)        
        return scaled_frame
    elif model in ('mask_rcnn'):
        padColor = [0,0,0]
        h, w = img.shape[:2]
        ratio = target / min(h, w)
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        if h > new_h or w > new_w: # shrinking 
            interp = cv2.INTER_AREA
        else: # stretching 
            interp = cv2.INTER_CUBIC
        aspect = w/h  
        scaled_frame = cv2.resize(img, (new_w, new_h), interpolation=interp)
        sh = int(math.ceil(scaled_frame.shape[0] / 32) * 32)
        sw = int(math.ceil(scaled_frame.shape[1] / 32) * 32)
        print (f'Original resize: {scaled_frame.shape[:2]}, Padded resize: {(sh, sw)}')
        # padded_frame = np.zeros((sh, sw, 3), dtype=np.float32)
        # padded_frame[:h, :w, :] = scaled_frame
        # scaled_frame = padded_frame

        # compute scaling and pad sizing
        
        if int(sw-new_w) > 0:
            pad_horz = (sw-new_w)/2
            pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        else:
            pad_left, pad_right = 0, 0
        
        if int(sh-new_h) > 0:
            pad_vert = (sh-new_h)/2
            pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        else:
            pad_top, pad_bot = 0, 0

        scaled_frame = cv2.copyMakeBorder(scaled_frame, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)        
        return scaled_frame

    elif model in ('ocr'):
        ocrGreyFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return ocrGreyFrame
    else:
        print('Model not supported for image resizing')
        pass