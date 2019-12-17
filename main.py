#ROI 설정하기 : 사용자가 관심있어 하는 부위를 지정하는 것
import cv2
import numpy as np

video_path='bts.mp4'
cap=cv2.VideoCapture(video_path)

#핸드폰에 꽉차는 사이즈
#(width, height)
output_size=(93, 166)

#initialize writing video(영상 저장)
fourcc=cv2.VideoWriter_fourcc('m', 'p', '4', 'v') #mp4v형식으로 저장
#(저장될 파일이름, 코덱, FPS(1초당 몇 frame저장할지), 크기)
#우리가 불러온 영상과 똑같은 frame으로 저장(cap에 로드된 동영상의 FPS를 반환)
out=cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get
(cv2.CAP_PROP_FPS), output_size)

if not cap.isOpened():
    exit()

#csrt tracker초기화
tracker=cv2.TrackerCSRT_create()  

ret, img=cap.read()

cv2.namedWindow('Selct Window')
#첫번째 frame을 보여줘라
cv2.imshow('Select Windw', img)

#setting ROI
#ROI를 설정하여 rect로 반환(ROI정보가 rect에 저장)
#중심점을 시작하지 말고, 십자가 모양으로 보여라
rect=cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Window')

#설정한 ROI로 tracker 설정(초기화)
tracker.init(img, rect)

while True:
    ret, img=cap.read()

    if not ret:
        exit()

    #img에서 rect로 설정한 이미지와 비슷한 물체의 위치를 찾아 반환
    success, box=tracker.update(img)

    left, top, width, height=[int(v) for v in box]

    #중심점 구하기
    center_x=left+width/2
    center_y=top+height/2

    #출력 박스 점 구하기
    result_top=int(center_y-output_size[1]/2)
    result_bottom=int(center_y+output_size[1]/2)
    result_left=int(center_x-output_size[0]/2)
    result_right=int(center_x+output_size[0]/2)

    result_img=img[result_top:result_bottom, result_left:result_right].copy()   #numpy array 복사

    #비디오 저장
    out.write(result_img)

    #이미지에 사각형을 그림
    cv2.rectangle(img, pt1=(left, top), pt2=(left+width, top+height), color=(255, 255, 255), 
    thickness=3)

    cv2.imshow('result_img', result_img)
    cv2.imshow('img', img)
    if cv2.waitKey(1)==ord('q'):
        break;   
