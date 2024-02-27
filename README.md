# PersonImageSaver

얼굴인식 모델 학습을 위한 이미지 저장기

<br>

## Getting Started 

ViusalStudioCode와 Python언어로 Anaconda 가상환경에서 진행되었습니다.
또한 selenium과 googleCSE, face_recognition 기술이 사용되었습니다.


<br>

### Prerequisites 

python과 anaconda 의 설치가 필요합니다.
conda 가상환경에서의 설치를 권장합니다.

<br>

### Installing 

window 프롬포트에 커맨드를 치서 설치를 진행하거나 conda 가상환경에 activate 해서 설치를 진행합니다.

각줄을 따라 입력합니다.

``` bash
$ conda install -c conda-forge dlib
$ conda install -c conda-forge/label/cf201901 dlib
$ conda install -c conda-forge/label/cf202003 dlib
$ pip install -r requirements.txt
```

# 실행

imagsaver.py의 위치에서 다음 커맨드를 칩니다.

``` bash
$ python imgsaver.py
```
<br>

![메인1](https://github.com/boyoung9020/PersonImageSaver/assets/154112385/21994ecb-8268-46ae-b23d-78a6109ec32f)


### 기능설명

1. 가장 상단의 왼쪽 리스트는 저장할 인물리스트입니다.
   
2. 인물리스트는 오른쪽의 칸에 이름을 입력하고 엔터키나 추가 버튼을 눌러서 추가가 가능합니다.
   
3. 삭제하고싶은 해당 인물의 이름을 누르고 삭제가 가능하고 전체삭제도 가능합니다.
4. 저장할 이미지의 갯수를 정합니다.
5. 이미지를 저장할 방법을 정합니다. <br>
  ▶️  selenium은 느리지만 정확성이있고 대규모로 저장이 가능 합니다. <br>
  ▶️  googleCSE는 빠르지만 최대 10장까지만 가능합니다.
      저장할 이미지의 갯수가 10개 초과면 googleCSE의 체크가 불가능 합니다.
6. 이미지 저장을 시작하는 버튼입니다. <br>
   이미지들은 스크립트의 실행위치의 Person_archive 디렉토리에 저장됩니다.
7. 저장되고있는 이미지의 진행률을 볼수있는 progressbar입니다.
8. 이미지 저장에 진행되고 있는 log를 볼수있는 loglist입니다.
9. 대표 이미지로 선택된 이미지를 보여줍니다. <br><br>
   대표 이미지로 선정되는 과정은 다음과 같습니다. <br>
   1. 이미지크기가 500x500이상만 가져옵니다.
   2. 이미지속 얼굴의 갯수가 한개만 가져옵니다.
   3. 이미지속 얼굴이 차지하는 비율이 큰 순으로 가져옵니다.
   4. 정면을 보고있는 얼굴을 가져옵니다. <br> 얼굴의 방향이 정면을 보고있는지 판단하기위해 코의 기울기나 두 눈의 위치를 비교합니다. (테스트 중)
10. 종료 버튼입니다.


<br><br>
### Filterling
저장된 이미지의 필터링 과정은 다음과 같습니다. <br>
1. crawling 하여 저장될때 빈파일로 저장되거나 해상도가 낮은 이미지들을 삭제합니다. <br>
2. 대표얼굴을 기준으로 다르다고 판단되는 얼굴들을 삭제합니다. <br> 또한 얼굴이 두개이상이거나 측면얼굴, 선글라스나 얼굴이 가린얼굴등 인식이 되지않는 이미지도 삭제합니다.






## Deployment / 배포

<br>

## Built With / 누구랑 만들었나요?

* [BoYoungJung](https://github.com/boyoung9020)

<br>

## Acknowledgments / 감사의 말

* [[face_recognition](https://github.com/ageitgey/face_recognition) ]






