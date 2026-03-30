import cv2
import mediapipe as mp
mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
hands=mp_hands.Hands(min_detection_confidence=0.7,min_tracking_confidence=0.7)
cap=cv2.VideoCapture(0)
expression=''
result=''
buttons=[('7',50,100,110,160),('8',160,100,220,160),('9',270,100,330,160),('/',380,100,440,160),('4',50,170,110,230),('5',160,170,220,230),('6',270,170,330,230),('*',380,170,440,230),('1',50,240,110,300),('2',160,240,220,300),('3',270,240,330,300),('-',380,240,440,300),('0',50,310,110,370),('.',160,310,220,370),('=',270,310,330,370),('+',380,310,440,370)]
def get_label(x,y):
    for label,x1,y1,x2,y2 in buttons:
        if x1<x<x2 and y1<y<y2:return label
    return None
while True:
    ret,frame=cap.read()
    if not ret:break
    frame=cv2.flip(frame,1)
    h,w,_=frame.shape
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(rgb)
    for label,x1,y1,x2,y2 in buttons:
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(frame,label,(x1+20,y1+40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)
            tip=hand_landmarks.landmark[8]
            ix,iy=int(tip.x*w),int(tip.y*h)
            label=get_label(ix,iy)
            if label:
                if label=='=':
                    try:result=str(eval(expression));expression=result
                    except:result='Error'
                else:expression+=label
                cv2.putText(frame,f'Pressed:{label}',(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.putText(frame,expression,(10,420),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    cv2.putText(frame,result,(10,470),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)
    cv2.imshow('Hand Gesture Calculator',frame)
    if cv2.waitKey(1)&0xFF==ord('q'):break
cap.release()
cv2.destroyAllWindows()
