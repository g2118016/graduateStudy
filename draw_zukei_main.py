# -*- coding: utf-8 -*-
import cv2
import my_module
import numpy as np
import math
import copy
import os

if __name__ == "__main__":
    #sx, syは線の始まりの位置
    zukei=""
    zukei=""
    sx, sy=0, 0
    tri=[]
    squ=[]
    ell=[]
    tri_s=[]
    squ_s=[]
    ell_hand=[]
    Ox=0
    Oy=0
    count=0
    RHO_MAX = 800
    RHO_MIN = 100
    count_ell=0
    end_flag=False
    mouse_flag=False

    #線の太さ
    stroke=2
    #点の大きさ
    hankei=5

    path2 = "wiss\\"
    current_path=os.getcwd()
    outFolderName = current_path+"\\wiss"

    #画像を読み込む
    img = cv2.imread("cat_photo_mini.jpg")

    # カラーとグレースケールで場合分け
    if len(img.shape) == 3:
        height, width, channels = img.shape[:3]
    else:
        height, width = img.shape[:2]
        channels = 1
    white=np.full((height,width,3), 255, np.uint8)
    img = cv2.addWeighted(img,0.6,white,0.4,0)
    img2=copy.deepcopy(img)

    #楕円のフィッティング用
    canvas=np.zeros((height, width, 3), np.uint8)

    #ボタン用のウインドウ
    tool=np.full((400,300,3), 255, np.uint8)
    tool_h, tool_w, tool_ch = tool.shape[:3]
    #ボタン配置
    #幅と高さ
    print(tool_h, tool_w)
    button_w, button_h=int(0.8*tool_w), int(0.2*tool_h)
    #ボタンの左上のx座標
    button_x=int(0.1*tool_w)
    #ボタン同士の間隔（下端と上端の間隔）
    space=int(0.2*tool_h*0.2)
    #一番上のボタンのy座標
    topButton_y=space
    #1つ前のボタンの上端と次のボタンの上端の間隔
    button_space=button_h+space
    button_x, button1_y=button_x, topButton_y
    button2_y=topButton_y+button_space
    button3_y=topButton_y+button_space*2
    #CreateOrderだけ少し話す
    button4_y=topButton_y+button_space*3+10
    # フォント指定
    fontType = cv2.FONT_HERSHEY_SIMPLEX
    fontSize = 1.5
    fontBold = 2
    #四角の左下からだと文字はみ出るから少し文字の位置を上に
    font_space=int(button_h*0.2)
    cv2.rectangle(tool, (button_x, button1_y), (button_x+button_w, button1_y+button_h), (0, 0, 0), 2)
    cv2.putText(tool, "Triangle", (button_x+font_space, button1_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
    cv2.rectangle(tool, (button_x, button2_y), (button_x+button_w, button2_y+button_h), (0, 0, 0), 2)
    cv2.putText(tool, "tetragon", (button_x+font_space, button2_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
    cv2.rectangle(tool, (button_x, button3_y), (button_x+button_w, button3_y+button_h), (0, 0, 0), 2)
    cv2.putText(tool, "Ellipse", (button_x+font_space, button3_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
    cv2.rectangle(tool, (button_x, button4_y), (button_x+button_w, button4_y+button_h), (0, 0, 0), 2)
    cv2.putText(tool, "Create Order", (button_x+font_space, button4_y+button_h-font_space*2), fontType, 1, (0, 0, 0), fontBold)

    #マウスの操作があるとき呼ばれる関数
    def callback(event, x, y, flags, param):
        global img, sx, sy, zukei, tri, squ, ell, count, tri_s, squ_s, ell_hand, canvas, mouse_flag
        #マウスの左ボタンがクリックされたとき
        if event == cv2.EVENT_LBUTTONDOWN and mouse_flag==False:
            if zukei=="tri":
                mouse_flag=True
                sx, sy=x, y
                tri_s.append([sx, sy])
                count=0
                cv2.circle(img,(sx,sy), hankei, (0,0,255), -1)
            if zukei=="squ":
                mouse_flag=True
                sx, sy=x, y
                squ_s.append([sx, sy])
                count=0
                cv2.circle(img,(sx,sy), hankei, (0,0,255), -1)
            if zukei=="ell":
                sx, sy = x, y

        #マウスの左ボタンがクリックされていて、マウスが動いたとき
        #cv2.imshow("img", img2)

        if flags == cv2.EVENT_FLAG_RBUTTON and event != cv2.EVENT_MOUSEMOVE and zukei=="tri":
            count+=1
            temp_x, temp_y=x, y
            if count==3:
                mouse_flag=False
                dis=my_module.search_tri_squ_module.distance(tri_s[0][0], tri_s[0][1], temp_x, temp_y)
                tri_s=[]
                if dis<=30:
                    temp_x, temp_y=tri[-1][0][0], tri[-1][0][1]
            if count<4:
                cv2.line(img, (sx, sy), (temp_x, temp_y), (0, 0, 0), stroke)
                cv2.circle(img,(temp_x,temp_y), hankei, (255,0,0), -1)
                sx, sy = temp_x, temp_y
            if count<3:
                tri_s.append([temp_x, temp_y])
            #print("tri_s", tri_s)
            if count==2:
                tri.append(tri_s)
            #print(tri)
            #print(count)

        if flags == cv2.EVENT_FLAG_RBUTTON and event != cv2.EVENT_MOUSEMOVE and zukei=="squ":
            count+=1
            temp_x, temp_y=x, y
            if count==4:
                mouse_flag=False
                dis=my_module.search_tri_squ_module.distance(squ_s[0][0], squ_s[0][1], temp_x, temp_y)
                squ_s=[]
                if dis<=30:
                    temp_x, temp_y=squ[-1][0][0], squ[-1][0][1]
            if count<5:
                cv2.line(img, (sx, sy), (temp_x, temp_y), (0, 0, 0), stroke)
                cv2.circle(img,(temp_x,temp_y), hankei, (255,0,0), -1)
                sx, sy = temp_x, temp_y
            if count<4:
                squ_s.append([temp_x, temp_y])
            if count==3:
                squ.append(squ_s)

        if flags == cv2.EVENT_FLAG_LBUTTON and event == cv2.EVENT_MOUSEMOVE and zukei=="ell":
            #canvas[y][x]=255
            ell_hand.append([x, y])
            #こっちは処理用配列に記入
            cv2.line(canvas, (sx, sy), (x, y), (255, 0, 0), 1)
            #こっちは表示している配列
            cv2.line(img, (sx, sy), (x, y), (0, 0, 0), stroke)
            sx, sy = x, y

    def callback_tool(event, x, y, flags, param):
        global img, img2, zukei, end_flag
        if event == cv2.EVENT_LBUTTONDOWN:
            if button_x<x and x<button_x+button_w:
                #Triangleボタンが押されたとき
                if button1_y<y and y<button1_y+button_h:
                    #押されたボタンをの表示を変える
                    cv2.rectangle(tool, (button_x, button1_y), (button_x+button_w, button1_y+button_h), (0, 0, 255), 2)
                    cv2.putText(tool, "Triangle", (button_x+font_space, button1_y+button_h-font_space), fontType, fontSize, (0, 0, 255), fontBold)
                    #他のボタンは元に戻す
                    cv2.rectangle(tool, (button_x, button2_y), (button_x+button_w, button2_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "tetragon", (button_x+font_space, button2_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
                    cv2.rectangle(tool, (button_x, button3_y), (button_x+button_w, button3_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "Ellipse", (button_x+font_space, button3_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
                    cv2.rectangle(tool, (button_x, button4_y), (button_x+button_w, button4_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "Create Order", (button_x+font_space, button4_y+button_h-font_space*2), fontType, 1, (0, 0, 0), fontBold)
                    zukei="tri"
                #tetragonボタンが押されたとき
                if button2_y<y and y<button2_y+button_h:
                    #押されたボタンをの表示を変える
                    cv2.rectangle(tool, (button_x, button2_y), (button_x+button_w, button2_y+button_h), (0, 0, 255), 2)
                    cv2.putText(tool, "tetragon", (button_x+font_space, button2_y+button_h-font_space), fontType, fontSize, (0, 0, 255), fontBold)
                    #他のボタンは元に戻す
                    cv2.rectangle(tool, (button_x, button1_y), (button_x+button_w, button1_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "Triangle", (button_x+font_space, button1_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
                    cv2.rectangle(tool, (button_x, button3_y), (button_x+button_w, button3_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "Ellipse", (button_x+font_space, button3_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
                    cv2.rectangle(tool, (button_x, button4_y), (button_x+button_w, button4_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "Create Order", (button_x+font_space, button4_y+button_h-font_space*2), fontType, 1, (0, 0, 0), fontBold)
                    zukei="squ"
                #Ellipseボタンが押されたとき
                if button3_y<y and y<button3_y+button_h:
                    #押されたボタンをの表示を変える
                    cv2.rectangle(tool, (button_x, button3_y), (button_x+button_w, button3_y+button_h), (0, 0, 255), 2)
                    cv2.putText(tool, "Ellipse", (button_x+font_space, button3_y+button_h-font_space), fontType, fontSize, (0, 0, 255), fontBold)
                    #他のボタンは元に戻す
                    cv2.rectangle(tool, (button_x, button1_y), (button_x+button_w, button1_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "Triangle", (button_x+font_space, button1_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
                    cv2.rectangle(tool, (button_x, button2_y), (button_x+button_w, button2_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "tetragon", (button_x+font_space, button2_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
                    cv2.rectangle(tool, (button_x, button4_y), (button_x+button_w, button4_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "Create Order", (button_x+font_space, button4_y+button_h-font_space*2), fontType, 1, (0, 0, 0), fontBold)
                    zukei="ell"
                    #これまでの画像をコピー
                    img2=copy.deepcopy(img)
                #CreateOrderボタンが押されたとき
                if button4_y<y and y<button4_y+button_h:
                    #押されたボタンをの表示を変える
                    cv2.rectangle(tool, (button_x, button4_y), (button_x+button_w, button4_y+button_h), (0, 0, 255), 2)
                    cv2.putText(tool, "Create Order", (button_x+font_space, button4_y+button_h-font_space*2), fontType, 1, (0, 0, 255), fontBold)
                    #他のボタンは元に戻す
                    cv2.rectangle(tool, (button_x, button1_y), (button_x+button_w, button1_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "Triangle", (button_x+font_space, button1_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
                    cv2.rectangle(tool, (button_x, button2_y), (button_x+button_w, button2_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "tetragon", (button_x+font_space, button2_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
                    cv2.rectangle(tool, (button_x, button3_y), (button_x+button_w, button3_y+button_h), (0, 0, 0), 2)
                    cv2.putText(tool, "Ellipse", (button_x+font_space, button3_y+button_h-font_space), fontType, fontSize, (0, 0, 0), fontBold)
                    #triクラス，squクラス，ellクラス生成
                    tri_class=[]
                    squ_class=[]
                    ell_class=[]
                    for i in range(len(tri)):
                        tri_class.append(my_module.triangle.Triangle(tri[i]))
                    for i in range(len(squ)):
                        squ_class.append(my_module.tetragon.tetragon(squ[i]))
                    for i in range(len(ell)):
                        ell_class.append(my_module.ellipse.Ellipse(ell[i]))

                    #描画順設定
                    draw_order=my_module.draw_order_module.ordering(tri_class, squ_class, ell_class)

                    #出力する前にフォルダ内の画像消しとく
                    top = path2
                    for root, dirs, files in os.walk(top, topdown=False):
                        for name in files:
                            os.remove(os.path.join(root, name))
                        for name in dirs:
                            os.rmdir(os.path.join(root, name))

                    #draw_orderを出力
                    #描画手順をgif化するため紙は最初に1つだけ作る
                    #白背景作成
                    img = np.full((height,width,3), 255, np.uint8)
                    for i in range(len(draw_order)):
                        if i==0:
                            cv2.imwrite(path2+"\\"+str(i)+".jpg", img)
                        #print(draw_order[i].label)
                        if draw_order[i].label=="tri":
                            # Create a black image
                            #img = np.zeros((height,width,3), np.uint8)
                            #白背景作成
                            #img = np.full((height,width,3), 255, np.uint8)
                            #多角形を記述
                            #contours = np.array([list(map(int, draw_order[i].edges[0])),list(map(int, draw_order[i].edges[1])),list(map(int, draw_order[i].edges[2]))])
                            contours = np.array(draw_order[i].points, dtype=int)
                            #fillConvexPolyで多角形を描画
                            #print(contours)
                            #cv2.fillConvexPoly(img, points =contours, color=(255, 255, 255))
                            #塗りつぶしできないのでlineで描きこみ
                            cv2.line(img, tuple(contours[0]), tuple(contours[1]), 0, stroke)
                            cv2.line(img, tuple(contours[1]), tuple(contours[2]), 0, stroke)
                            cv2.line(img, tuple(contours[2]), tuple(contours[0]), 0, stroke)
                            cv2.imwrite(path2+"\\"+str(i+1)+".jpg", img)

                        elif draw_order[i].label=="squ":
                            # Create a black image
                            #img = np.zeros((height,width,3), np.uint8)
                            #img = np.full((height,width,3), 255, np.uint8)
                            #多角形を記述
                            #contours = np.array([list(map(int, draw_order[i].edges[0])), list(map(int, draw_order[i].edges[1])),list(map(int, draw_order[i].edges[2])),list(map(int, draw_order[i].edges[3]))])
                            contours = np.array(draw_order[i].points, dtype=int)
                            #fillConvexPolyで多角形を描画
                            #cv2.fillConvexPoly(img, points =contours, color=(255, 255, 255))
                            cv2.line(img, tuple(contours[0]), tuple(contours[1]), 0, stroke)
                            cv2.line(img, tuple(contours[1]), tuple(contours[2]), 0, stroke)
                            cv2.line(img, tuple(contours[2]), tuple(contours[3]), 0, stroke)
                            cv2.line(img, tuple(contours[3]), tuple(contours[0]), 0, stroke)

                            cv2.imwrite(path2+"\\"+str(i+1)+".jpg", img)

                        elif draw_order[i].label=="ell":
                            #img = np.zeros((height,width,3), np.uint8)
                            #img = np.full((height,width,3), 255, np.uint8)
                            img = cv2.ellipse(img,(int(draw_order[i].points[0]),int(draw_order[i].points[1])),(int(draw_order[i].points[2]),int(draw_order[i].points[3])),int(draw_order[i].points[4]),0,360,(0, 0, 0),stroke)
                            cv2.imwrite(path2+"\\"+str(i+1)+".jpg", img)
                    my_module.create_animation.create_gif(outFolderName, height, width)
                    end_flag=True

    #ウィンドウの名前を設定
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    #コールバック関数の設定
    cv2.setMouseCallback("img", callback)

    #ウィンドウの名前を設定
    cv2.namedWindow("toolbar", cv2.WINDOW_NORMAL)
    #コールバック関数の設定
    cv2.setMouseCallback("toolbar", callback_tool)
    while(1):
        cv2.imshow("img", img)
        cv2.imshow("toolbar", tool)
        k = cv2.waitKey(1)
        if end_flag == True:
            break
        #Escキーを押すと終了
        if k == 27:
            break
        #tを押すと三角形描画モード
        if k == ord("t"):
            zukei="tri"
        #sを押すと四角形描画モード
        if k == ord("s"):
            zukei="squ"

        #eを押すと楕円描画モード
        if k == ord("e"):
            zukei="ell"
            #これまでの画像をコピー
            img2=copy.deepcopy(img)
        #Enterキーで楕円処理
        if k == 13 and zukei=="ell":
            #ell = my_module.ellipse_one_search_module.search_ellipse(width, height, canvas, RHO_MAX, RHO_MIN)
            #print(ell)
            #処理のために始点と終点を線で結んでおく
            cv2.line(canvas, (ell_hand[0][0], ell_hand[0][1]), (ell_hand[-1][0], ell_hand[-1][1]), (255, 0, 0), 1)
            imgray = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
            ret,thresh = cv2.threshold(imgray,10,255,0)
            imgEdge,contours,hierarchy = cv2.findContours(thresh, 1, 2)
            cnt = contours[0]

            #手書きの重心を算出
            #こっちのほうが楕円の中心っぽい
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            #外接矩形を計算
            #rect = cv2.minAreaRect(cnt)
            #矩形の四点を求める
            #box = cv2.boxPoints(rect)
            #Ox=int((box[0][0]+box[2][0])/2)
            #Oy=int((box[0][1]+box[2][1])/2)
            #box = np.int0(box)
            #canvas = cv2.drawContours(canvas,[box],0,(0,0,255),2)

            ellipse = cv2.fitEllipse(cnt)
            #print(ellipse)
            #print("center", cx, cy)
            #cv2.circle(canvas,(cx,cy), 2, (255,255,0), -1)
            #cv2.circle(canvas,(Ox,Oy), 2, (255,0,0), -1)
            #cv2.ellipse(canvas,ellipse,(0,255,0),2)
            #cv2.imshow("img2", canvas)
            canvas=np.zeros((height, width, 3), np.uint8)
            ell_hand=[]
            ell.append([int(ellipse[0][0]), int(ellipse[0][1]), int(ellipse[1][0]/2), int(ellipse[1][1]/2), ellipse[2]])
            cv2.ellipse(img2,(ell[count_ell][0], ell[count_ell][1]),(ell[count_ell][2],ell[count_ell][3]),ell[count_ell][4],0,360,(0,0,0),stroke)
            count_ell+=1
            img=copy.deepcopy(img2)

        if k == 32:
            #triクラス，squクラス，ellクラス生成
            tri_class=[]
            squ_class=[]
            ell_class=[]
            for i in range(len(tri)):
                tri_class.append(my_module.triangle.Triangle(tri[i]))
            for i in range(len(squ)):
                squ_class.append(my_module.tetragon.tetragon(squ[i]))
            for i in range(len(ell)):
                ell_class.append(my_module.ellipse.Ellipse(ell[i]))

            #描画順設定
            draw_order=my_module.draw_order_module.ordering(tri_class, squ_class, ell_class)

            #出力する前にフォルダ内の画像消しとく
            top = path2
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

            #draw_orderを出力
            #描画手順をgif化するため紙は最初に1つだけ作る
            #白背景作成
            img = np.full((height,width,3), 255, np.uint8)
            for i in range(len(draw_order)):
                #print(draw_order[i].label)
                if draw_order[i].label=="tri":
                    # Create a black image
                    #img = np.zeros((height,width,3), np.uint8)
                    #白背景作成
                    #img = np.full((height,width,3), 255, np.uint8)
                    #多角形を記述
                    #contours = np.array([list(map(int, draw_order[i].edges[0])),list(map(int, draw_order[i].edges[1])),list(map(int, draw_order[i].edges[2]))])
                    contours = np.array(draw_order[i].points, dtype=int)
                    #fillConvexPolyで多角形を描画
                    #print(contours)
                    #cv2.fillConvexPoly(img, points =contours, color=(255, 255, 255))
                    #塗りつぶしできないのでlineで描きこみ
                    cv2.line(img, tuple(contours[0]), tuple(contours[1]), 0, stroke)
                    cv2.line(img, tuple(contours[1]), tuple(contours[2]), 0, stroke)
                    cv2.line(img, tuple(contours[2]), tuple(contours[0]), 0, stroke)
                    cv2.imwrite(path2+"\\"+str(i)+".jpg", img)

                elif draw_order[i].label=="squ":
                    # Create a black image
                    #img = np.zeros((height,width,3), np.uint8)
                    #img = np.full((height,width,3), 255, np.uint8)
                    #多角形を記述
                    #contours = np.array([list(map(int, draw_order[i].edges[0])), list(map(int, draw_order[i].edges[1])),list(map(int, draw_order[i].edges[2])),list(map(int, draw_order[i].edges[3]))])
                    contours = np.array(draw_order[i].points, dtype=int)
                    #fillConvexPolyで多角形を描画
                    #cv2.fillConvexPoly(img, points =contours, color=(255, 255, 255))
                    cv2.line(img, tuple(contours[0]), tuple(contours[1]), 0, stroke)
                    cv2.line(img, tuple(contours[1]), tuple(contours[2]), 0, stroke)
                    cv2.line(img, tuple(contours[2]), tuple(contours[3]), 0, stroke)
                    cv2.line(img, tuple(contours[3]), tuple(contours[0]), 0, stroke)

                    cv2.imwrite(path2+"\\"+str(i)+".jpg", img)

                elif draw_order[i].label=="ell":
                    #img = np.zeros((height,width,3), np.uint8)
                    #img = np.full((height,width,3), 255, np.uint8)
                    img = cv2.ellipse(img,(int(draw_order[i].points[0]),int(draw_order[i].points[1])),(int(draw_order[i].points[2]),int(draw_order[i].points[3])),int(draw_order[i].points[4]),0,360,(0, 0, 0),stroke)
                    cv2.imwrite(path2+"\\"+str(i)+".jpg", img)

            my_module.create_animation.create_gif(outFolderName)
            break
