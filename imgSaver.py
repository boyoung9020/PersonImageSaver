import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QSize, Qt
from qt import Ui_crawling  # Ui_carwling 클래스 임포트
from tqdm import tqdm
import face_check
from PyQt5.QtGui import QPixmap
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import sys


api_key = 'AIzaSyC9Va0fbqU86JvEOF2-ILwXdwPAf_DTtag'
cse_id = 'f3a2ae7ae0c6341f4'

class CrawlingThread(QThread):
    log_updated = pyqtSignal(str)
    progress_updated = pyqtSignal(int)


    def __init__(self, num_images, all_names, detected_image_label,use_selenium):
        super(CrawlingThread, self).__init__()
        self.num_images = num_images
        self.all_names = all_names
        self.detected_image_label = detected_image_label
        self.use_selenium = use_selenium  # True면 Selenium 사용, False면 GoogleCSE 사용

    def run(self):
        total_progress = 0

 
        for name in self.all_names:
            name = name.strip()
            if name == "":
                continue
            
            self.log_updated.emit(f"Crawling images for {name}...")

            if self.num_images > 10 or self.use_selenium:
                self.log_updated.emit("\n*** Select selenium")
                self.log_updated.emit("*"*40)

                self.seleniumCrawling(name, self.num_images)
            else:
                self.log_updated.emit("\n*** Select googleCSE")
                self.log_updated.emit("*"*40)

                self.googleCSE(name, self.num_images)

            self.log_updated.emit(f"Finished crawling images for {name}")
            self.log_updated.emit("*"*40)
            total_progress += 100 // len(self.all_names)
            self.progress_updated.emit(total_progress)


    def seleniumCrawling(self, person_name, num_images):


        def scroll_to_end(driver):
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height


        def remove_invalid_images(images_dir, name):
            log_message = "\n" +  "이미지 필터링"
            log_message += "\n1단계 필터링..(비정상적인 이미지 삭제)"

            deleted_count = 0

            for filename in os.listdir(images_dir):
                if filename.endswith('.jpg'):
                    file_path = os.path.join(images_dir, filename)
                    if os.path.getsize(file_path) < 10240:
                        log_message += f"\nrenmove: {file_path}"
                        os.remove(file_path)
                        deleted_count += 1
            log_message += "\n"+"2단계 필터링..(loaded face_cehck.py)"  
 


            self.log_updated.emit("\n" + f"{name}의 얼굴 분석중")
            representative_image_path = face_check.find_representative_image(name)
            self.log_updated.emit("분석 완료. 대표 얼굴 지정")
            self.detected_image_label.setPixmap(QPixmap(representative_image_path).scaled(self.detected_image_label.width(),self.detected_image_label.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
                        
                        
            fcdeleted_count,removelist = face_check.main(representative_image_path,name) 

        
            deleted_count += fcdeleted_count
            for removed_path in removelist:
                log_message += f"\nrenmove: {removed_path}"

       
            self.log_updated.emit(log_message)
            self.log_updated.emit("\n"+f"총 삭제된 이미지 수: {deleted_count}")
            
            

        script_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(script_dir, 'Person_archive', person_name)
        os.makedirs(images_dir, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(options=options)

        search_url = f"https://www.google.com/search?tbm=isch&q={person_name}"
        driver.get(search_url)
        time.sleep(1)

        num_scrolls = (num_images // 20) +1  

        starttime = time.time()
        self.log_updated.emit("이미지 로딩 중... (최대 25초)")
        for _ in range(num_scrolls):
            scroll_to_end(driver)
            try:
                more_results_button = driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')
                more_results_button.click()
                time.sleep(1)
            except Exception as e:
                self.log_updated.emit("이미지 로드 완료")
                break

        total = num_images
        current_progress = 0
        self.progress_updated.emit(current_progress)

        endtime = time.time()
        elapsed_time = endtime - starttime
        elapsed_time_seconds = int(elapsed_time)
        self.log_updated.emit(f"총 로드 시간: {elapsed_time_seconds} 초")
        self.log_updated.emit("\n" + "이미지 저장 준비중..")
        # self.log_updated.emit("\n" + "-" * 43 + f" {person_name} " + "-" * 43)
        image_elements = driver.find_elements(By.XPATH, '//*[@id="islrg"]//img[contains(@class,"rg_i")]')
        saved_images_count = 1  

        starttime = time.time()

        for i, image_element in enumerate(image_elements):
            try:
                if saved_images_count - 1 == total:
                    break
                image_element.click()
                time.sleep(1)
                detailed_image = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img')
                image_url = detailed_image.get_attribute('src')
                image_name = f"{person_name}_{saved_images_count}.jpg"
                image_path = os.path.join(images_dir, image_name)
                with open(image_path, 'wb') as f:
                    f.write(requests.get(image_url).content)
                saved_images_count += 1
                current_progress = saved_images_count * 100 // total
                self.progress_updated.emit(current_progress)
                QApplication.processEvents()
            except Exception as e:
                pass


        self.log_updated.emit(f"다운로드된 이미지 수: {saved_images_count - 1}")
        driver.quit()
        
        if saved_images_count -1 == 0:
            self.seleniumCrawling(self, person_name, num_images)
        else:
            pass

        endtime = time.time()
        elapsed_time = endtime - starttime
        elapsed_time_seconds = int(elapsed_time)
        self.log_updated.emit(f"총 저장 시간: {elapsed_time_seconds} 초")

        remove_invalid_images(images_dir, person_name)

    def googleCSE(self,person_name,num_images):

        def download_image(image_url, save_path):
            response = requests.get(image_url)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)  

                with open(save_path, 'wb') as file:
                    file.write(response.content)

        def remove_invalid_images(images_dir, name):
            log_message = "\n" +  "이미지 필터링"
            log_message += "\n1단계 필터링..(비정상적인 이미지 삭제)"

            deleted_count = 0

            for filename in os.listdir(images_dir):
                if filename.endswith('.jpg'):
                    file_path = os.path.join(images_dir, filename)
                    if os.path.getsize(file_path) < 10240:
                        log_message += f"\nrenmove: {file_path}"
                        os.remove(file_path)
                        deleted_count += 1
            log_message += "\n"+"2단계 필터링..(loaded face_cehck.py)"  

            self.log_updated.emit("\n"+f"{name}의 얼굴 분석중")
            representative_image_path = face_check.find_representative_image(name)
            self.log_updated.emit("분석 완료. 대표 얼굴 지정")
            self.detected_image_label.setPixmap(QPixmap(representative_image_path).scaled(self.detected_image_label.width(),self.detected_image_label.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
                        
                        
            fcdeleted_count,removelist = face_check.main(representative_image_path,name) 

            deleted_count += fcdeleted_count
            for removed_path in removelist:
                log_message += f"\nrenmove: {removed_path}"

            self.log_updated.emit(log_message)

            self.log_updated.emit("\n"+f"총 삭제된 이미지 수: {deleted_count}")



        def search_and_download_images(person_name, api_key, cse_id, num_images):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            images_dir = os.path.join(script_dir, 'Person_archive', person_name)
            os.makedirs(images_dir, exist_ok=True)
            
            starttime = time.time()
            search_url = f"https://www.googleapis.com/customsearch/v1?q={person_name}&cx={cse_id}&key={api_key}&searchType=image&num={num_images}"
            response = requests.get(search_url)
            search_results = response.json()
            saved_images_count = 0
            
            for idx, item in enumerate(search_results.get('items', []), start=1):
                if saved_images_count == num_images:
                    break
                
                image_url = item['link']
                image_name = f"{person_name}_{idx}.jpg"
                save_path = os.path.join(images_dir, image_name)
                download_image(image_url, save_path)
                saved_images_count += 1
                current_progress = saved_images_count * 100 // num_images
                self.progress_updated.emit(current_progress)  # PyQt progress bar에 진행 상황 업데이트

            self.log_updated.emit(f"다운로드된 이미지 수: {saved_images_count}")
            endtime = time.time()
            elapsed_time = endtime - starttime
            elapsed_time_seconds = int(elapsed_time)
            self.log_updated.emit(f"총 저장 시간: {elapsed_time_seconds}초")
            remove_invalid_images(images_dir, person_name)


        search_and_download_images(person_name, api_key, cse_id,  num_images)


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_crawling()
        self.ui.setupUi(self)


        self.detected_image_label = self.ui.detected_image_label

        self.ui.addButton.clicked.connect(self.add_name_to_list)
        self.ui.deleteButton.clicked.connect(self.delete_selected_item)
        self.ui.deleteallButton.clicked.connect(self.delete_all_items)
        self.ui.nameEdit.returnPressed.connect(self.add_name_to_list)
        self.ui.crawlingButton.clicked.connect(self.start_crawling)
        self.ui.ScheckBox.clicked.connect(self.check_selenium)
        self.ui.GcheckBox.clicked.connect(self.check_googlecse)
        self.ui.resetButton.clicked.connect(self.reset_window)


        # ScheckBox를 선택된 상태로 설정
        self.ui.ScheckBox.setChecked(True)
        self.load_names()
        self.crawling_thread = None
        self.use_selenium = True 


    def reset_window(self):
        try:
            # 현재 창을 숨김
            self.hide()

            # 새로운 MainWindow 객체 생성
            new_window = MainWindow()

            # 현재 QApplication의 인스턴스를 가져옴
            app = QApplication.instance()

            # 현재 창을 종료하고 새로운 창을 보여줌
            if app is not None:
                app.setActiveWindow(new_window)
                new_window.show()
        except Exception as e:
            import traceback
            traceback.print_exc()

            
    def check_selenium(self):
        self.use_selenium = self.ui.ScheckBox.isChecked()

    def check_googlecse(self):
        self.use_selenium = not self.ui.GcheckBox.isChecked()


    def add_name_to_list(self):
        name = self.ui.nameEdit.text().strip()
        if name:
            self.ui.namelist.addItem(name)
            self.ui.nameEdit.clear()
            self.save_names()

    def delete_selected_item(self):
        selected_item = self.ui.namelist.currentItem()
        if selected_item is not None:
            self.ui.namelist.takeItem(self.ui.namelist.row(selected_item))
            self.save_names()

    def delete_all_items(self):
        self.ui.namelist.clear()
        self.save_names()

    def load_names(self):
        try:
            with open("names.txt", "r") as f:
                names = f.readlines()
                for name in names:
                    self.ui.namelist.addItem(name.strip())
        except FileNotFoundError:
            pass

    def save_names(self):
        with open("names.txt", "w") as f:
            for i in range(self.ui.namelist.count()):
                f.write(self.ui.namelist.item(i).text() + "\n")

    def start_crawling(self):
        num_images = int(self.ui.imagenumEdit.text())
        all_names = [self.ui.namelist.item(i).text() for i in range(self.ui.namelist.count())]

        if not all_names:
            return

        self.ui.loglist.clear()
        self.ui.progressBar.setValue(0)

        if self.crawling_thread and self.crawling_thread.isRunning():
            self.crawling_thread.terminate()
        self.crawling_thread = CrawlingThread(num_images, all_names, self.detected_image_label, self.use_selenium)
        self.crawling_thread.log_updated.connect(self.update_log)
        self.crawling_thread.progress_updated.connect(self.update_progress)
        self.crawling_thread.start()

    def update_log(self, message):
        log_item = QListWidgetItem(message)
        self.ui.loglist.addItem(log_item)
        self.ui.loglist.scrollToBottom()

    def update_progress(self, progress):
        self.ui.progressBar.setValue(progress)
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())