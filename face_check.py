import matplotlib.pyplot as plt 
import numpy as np 
import argparse 
import imutils 
import dlib 
import cv2 
import face_recognition 
import pickle
from PIL import ImageFont, ImageDraw, Image
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox

from glob import glob


font_path = './font/gothic.ttf'

font = ImageFont.truetype(font_path, 80)

known_face_encodings = [] 
known_face_names = []
deleted_image_count = 0

def draw_text(img, text, position, color):
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    draw.text(position, text, font=font, fill=color)
    cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return cv2_img

def plt_imshow(title='image', img=None, figsize=(8 ,5)):
    plt.figure(figsize=figsize)
    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            titles = []
            for i in range(len(img)):
                titles.append(title)
        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)
            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
        plt.show()
    else:
        if len(img.shape) < 3:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(rgbImg)
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()

def name_labeling(img, image_path, deleted_image_count, removelist):
    deleted_image_count = deleted_image_count
    try:
        if img is not None:  # 이미지가 None이 아닌 경우에만 처리
            image = img.copy()
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            if face_locations == []:
                removelist.append(image_path)
                os.remove(image_path)
                print(f"remove {image_path}")
                deleted_image_count += 1
            face_names = []
    
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                name = "Unknown"
    
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
    
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
    
                face_names.append(name)
            
            for (top, right, bottom, left), name in zip(face_locations, face_names):

                if name != "Unknown":
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                    removelist.append(image_path)
                    os.remove(image_path)
                    print(f"remove {image_path}")
                    deleted_image_count += 1
                    break
    
                cv2.rectangle(image, (left, top), (right, bottom), color, 1)
                cv2.rectangle(image, (left, bottom - 20), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
    
                image = draw_text(image, name, (left + 3,  bottom - 15), (0, 0, 0))
        else:  # 이미지가 None인 경우 처리
            print(f"Error: 이미지가 None입니다. Deleting image: {image_path}")
            removelist.append(image_path)
            os.remove(image_path)
            print(f"remove {image_path}")
            deleted_image_count += 1
    except RuntimeError as e:
        if 'out of memory' in str(e):
            print(f"Error: {e}. Deleting image: {image_path}")
            removelist.append(image_path)
            os.remove(image_path)
            print(f"remove {image_path}")
            deleted_image_count += 1
        else:
            raise e

    # plt_imshow("detect", image, figsize=(24, 15))

    return deleted_image_count, removelist

def draw_label(img, coordinates, label):
    image = img.copy()
    (top, right, bottom, left) = coordinates
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 5)
    # cv2.putText() 대신 draw_text() 함수 사용
    image = draw_text(image, label, (left - 5, top -80 ), (0, 255, 0))
    
    return image




def add_known_face(face_image_path, name):


    face_image = imread(face_image_path)
    if face_image is None:
        # print("-"*40)
        print(f"Failed to load image from {face_image_path}.")
        return
    face_location = face_recognition.face_locations(face_image)
    
    if len(face_location) == 0:
        print(f"{face_image_path}에서 얼굴을 찾을 수 없습니다.")
        return
    
    face_location = face_location[0]  # 첫 번째 얼굴만 사용
    face_encoding = face_recognition.face_encodings(face_image)[0]
    
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)

    # top, right, bottom, left = face_location
    # cropped_face = face_image[top:bottom, left:right]
    # print(cropped_face)
    
    # current_directory = os.getcwd()
    # saved_path = os.path.join(current_directory, f"{name}.jpg")

    landmarks = face_recognition.face_landmarks(face_image)
    # for idx, face_landmark in enumerate(landmarks):
    #     print(f"얼굴 {idx+1}의 특징:")
    #     for feature, coordinates in face_landmark.items():
    #         print(f"{feature}: {coordinates}")
    
    
    # cv2.imwrite(saved_path, cropped_face)
    # success = cv2.imwrite(saved_path, cropped_face)
    # if success:
    #     print("이미지가 성공적으로 저장되었습니다.")
    # else:
    #     print("이미지 저장에 실패했습니다.")

    detected_face_image = draw_label(face_image, face_location, name)
    # plt_imshow(["Input Image", "Detected Face"], [face_image, detected_face_image])

    return detected_face_image


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None
 
import os
def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

# def select_image_and_show(name):
#     messagebox.showinfo("대표얼굴 선택",f"{name}의 대표 얼굴을 선택해주세요")

#     options = {
#         'title': f'{name}의 대표 얼굴을 선택하세요', 
#         'filetypes': [('이미지 파일', '*.jpg;*.jpeg;*.png;*.gif')],  
#         'initialdir': f'D:\FaceWorkspace\Person_archive\{name}',
#     }

#     file_path = filedialog.askopenfilename(**options)

#     if file_path:
#         pass
#     else:
#         select_image_and_show(name)

#     return file_path


def calculate_face_area(face_landmarks):
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = 0, 0
    
    for landmarks in face_landmarks:
        for _, coordinates in landmarks.items():
            for x, y in coordinates:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    
    width = max_x - min_x
    height = max_y - min_y
    
    return width * height


def find_representative_image(name):
    directory = f'./Person_archive/{name}/'    
    min_size=(500, 500)
    
    image_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.jpg') or f.endswith('.png')]

    representative_image_path = None
    max_face_area_ratio = 0.0
    
    for image_path in image_paths:
        image = face_recognition.load_image_file(image_path)
        
        height, width, _ = image.shape
        
        if height < min_size[0] or width < min_size[1]:
            continue
        
        face_landmarks = face_recognition.face_landmarks(image)
        
        if face_landmarks and len(face_landmarks) == 1:
            total_area = width * height
            
            face_area = calculate_face_area(face_landmarks)
            
            face_area_ratio = face_area / total_area
            
            if face_area_ratio > max_face_area_ratio:
                max_face_area_ratio = face_area_ratio
                representative_image_path = image_path

    return representative_image_path










def main(selected_image_path,name):
    deleted_image_count = 0  # 로컬 변수로 초기화
    removelist = []

    root = tk.Tk()
    root.withdraw()  
    root.attributes('-topmost', True)
    directory_path = f'./Person_archive/{name}/'    
    # file_path = select_image_and_show(name)
    
    


    add_known_face(selected_image_path, name)

    
    image_paths = glob(os.path.join(directory_path, '*.jpg'))

    image_paths = sorted(image_paths, key=lambda x: (x.split('/')[-1].split('_')[0], int(x.split('/')[-1].split('_')[-1].split('.')[0])))

    for image_path in image_paths :
        image = imread(image_path)
        deleted_image_count,removelist = name_labeling(image,image_path,deleted_image_count,removelist)  

    return deleted_image_count,removelist


# if __name__ == "__main__":
#     main('정국')