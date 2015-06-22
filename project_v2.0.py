#5130379065 Zhou Weijie
#this is my project
from graphics import *
from button import Button
import random
import time
import winsound
import threading
import copy
#this is a finished 2.0 version and it reconstruct the whole game    


class Block:#a block which controls the image in the game
    def __init__(self,num,xVal,yVal):
        self.num = num
        self.path = "./image/" + str(num) + ".gif"
        self.Bg_clPath = "./image/di.gif"
        self.x = xVal
        self.y = yVal
        self.state = 0
        self.f = Image(Point(xVal,yVal),self.path)
        self.bg_cl = Image(Point(xVal,yVal),self.Bg_clPath)
    def draw(self,wVal):#the draw logic
        #self.bg.draw(wVal)
        self.f.draw(wVal)
    def undraw(self):#the undraw logic
        self.f.undraw()
        #self.bg.undraw()
    def gui_clicked(self,wVal):#manage the image when clicked
        self.undraw()
        self.bg_cl.draw(wVal)
        self.f.draw(wVal)
        self.state = 1
    def gui_recover(self,wVal):#manage the image when recovered
        self.f.undraw()
        self.bg_cl.undraw()
        self.draw(wVal)
        self.state = 0
    def getNum(self):#return the num of pictures
        return self.num
    def getX(self):#return x
        return self.x
    def getY(self):#return y
        return self.y
    def clicked(self,xVal,yVal):#judge whether is clicked
        if (xVal <= self.x + 0.25 and xVal >= self.x - 0.25):
            if (yVal <= self.y + 0.25 and yVal >= self.y - 0.25):
                return True
        return False

class Box:# a box which manage whole blocks
    def __init__(self,wVal,length,width):
        self.condition = -1
        self.w = wVal
        self.len = length
        self.wid = width
        self.all = length*width
        self.last_x = -2
        self.last_y = -2
        self.blocks = []
        self.flags = []#a flag controls the all block logic
        self.sound_threads = []

    def HaveAnswer(self):#decide the whole box can be solved
        all_num = self.all
        tmp = []
        tmp = copy.deepcopy(self.flags)
        f_len = self.len+2
        f_wid = self.wid+2
        while (True):
            if (all_num == 0):
                self.flags = copy.deepcopy(tmp)
                del tmp
                return True
            answer = []
            if (self.CheckAnswer(answer) == True):
                size = len(answer)
                x1 = answer[0][0]
                y1 = answer[0][1]
                x2 = answer[size-1][0]
                y2 = answer[size-1][1]
                self.flags[x1][y1] = 0
                self.flags[x2][y2] = 0
                all_num -= 2
            else:
                return False

    def getAll(self):#return the number of remaining all blocks
        return self.all
            
    def undraw(self):#undraw all the block
        for i in range(0,self.len):
            for j in range(0,self.wid):
                if (self.flags[i+1][j+1] > 0):
                    self.blocks[i][j].undraw()
                if (self.flags[i+1][j+1] == -2):
                    self.blocks[i][j].gui_recover(self.w)
                    self.blocks[i][j].undraw()
    def init_flag(self):#a init of flag
        f_len = self.len+2
        f_wid = self.wid+2
        while (True):
            for i in range(0,f_len):
                tmp_flag = []
                for j in range(0,f_wid):
                    tmp_flag.append(0)
                self.flags.append(tmp_flag)
            for i in range(1,f_len-1):
                for j in range(1,f_wid-1,2):
                    tmp = random.randint(1,30)
                    self.flags[i][j] = tmp
                    self.flags[i][j+1] = tmp
            for i in range(0,1000):#a contrel logic to mess up the all block
                self.exchange()
            if (self.HaveAnswer() == True):
                break
    def exchange(self):#exchange function to mess up the block
        x1 = random.randint(1,self.len)
        y1 = random.randint(1,self.wid)
        x2 = random.randint(1,self.len)
        y2 = random.randint(1,self.wid)
        tmp = self.flags[x2][y2]
        self.flags[x2][y2] = self.flags[x1][y1]
        self.flags[x1][y1] = tmp
    def init_block(self):#to init all the block according the flag
        beginY = 5.25
        for i in range(0,self.len):
            beginX = 0.75
            tmp_blocks = []
            for j in range(0,self.wid):
                tmp_blocks.append(Block(self.flags[i+1][j+1],beginX,beginY))
                beginX += 0.5
            self.blocks.append(tmp_blocks)
            beginY -= 0.5
            
    def draw(self):#a draw logic to draw all the block
        for i in range(0,self.len):
            for j in range(0,self.wid):
                self.blocks[i][j].draw(self.w)

    def CheckAnswer(self,answer):#an auto function to find an answer to play
        for i in range(0,self.len):
            for j in range(0,self.wid):
                for k in range(0,self.len):
                    for t in range(0,self.wid):
                        if (i != k or j != t):
                            if (self.flags[i+1][j+1] == self.flags[k+1][t+1]
                                and self.flags[i+1][j+1] != 0 and self.flags[k+1][t+1] != 0):
                                if (self.check_clear(i+1,j+1,k+1,t+1,answer) == True):
                                    return True
        return False
    
    def FindAnswer(self,answer):#an auto function to find an answer to play
        for i in range(0,self.len):
            for j in range(0,self.wid):
                for k in range(0,self.len):
                    for t in range(0,self.wid):
                        if (i != k or j != t):
                            if (self.blocks[i][j].getNum() == self.blocks[k][t].getNum()
                                and self.flags[i+1][j+1] != 0 and self.flags[k+1][t+1] != 0):
                                if (self.check_clear(i+1,j+1,k+1,t+1,answer) == True):
                                    return True
        return False
    
    def Clicked(self,xVal,yVal,tmp):#judge which block is clicked
        for i in range(0,self.len):
            for j in range(0,self.wid):
                if (self.blocks[i][j].clicked(xVal,yVal) == True and self.flags[i+1][j+1] > 0):
                    self.flags[i+1][j+1] = -2
                    tmp.append([i,j])
                    return True
        return False
    def GetLast(self,tmp):#return the last_clicked block num
        tmp.append([self.last_x,self.last_y])

    def NotClear(self,x1,y1):#the logic of 2 blocks not clear
        self.flags[self.last_x+1][self.last_y+1] = self.blocks[self.last_x][self.last_y].getNum()
        self.last_x = x1
        self.last_y = y1

    def Clear(self,x1,y1):#the logic of 2 blocks clear
        self.all -= 2
        self.flags[x1+1][y1+1] = 0
        self.flags[self.last_x+1][self.last_y+1] = 0
        self.last_x = -2
        self.last_y = -2

    def Check(self,x1,y1,answer):#check whether 2 blocks can clear
        if (self.last_x != -2):
            if (self.blocks[x1][y1].getNum() == self.blocks[self.last_x][self.last_y].getNum()
                and self.check_clear(x1+1,y1+1,self.last_x+1,self.last_y+1,answer) == True):
                return True
        return False

    def Render(self,is_clicked,is_clear,x1,y1,x2,y2,answer):#a gui drawing logic to do the all rendering 
        if (is_clicked == True):
            self.blocks[x1][y1].gui_clicked(self.w)
        else:
            return
        if (is_clear == True):
            time.sleep(0.25)
            self.gui_draw_line(answer)#
            self.blocks[x2][y2].gui_recover(self.w)#
            self.blocks[x2][y2].undraw()#
            self.blocks[x1][y1].gui_recover(self.w)#
            self.blocks[x1][y1].undraw()#
        elif (x2 >= 0):
            self.blocks[x2][y2].gui_recover(self.w)#
    
    def gui_draw_line(self,answer):#a function to draw the line between 2 blocks
        size = len(answer)
        lines = []
        for i in range(0,size-1):
            x1 = answer[i][1]*0.5+0.25
            y1 = 5.75-answer[i][0]*0.5
            x2 = answer[i+1][1]*0.5+0.25
            y2 = 5.75-answer[i+1][0]*0.5
            #line = Line(Point(self.blocks[x1][y1].getX(),self.blocks[x1][y1].getY()),
                        #Point(self.blocks[x2][y2].getX(),self.blocks[x2][y2].getY()))
            lines.append(Line(Point(x1,y1),Point(x2,y2)))
        for ele in lines:
            ele.setWidth(3)
            ele.setOutline("red")
            ele.draw(self.w)
        time.sleep(0.3)
        for ele in lines:
            ele.undraw()
    
    def check_clear(self,x1,y1,x2,y2,answer):#check whther 2 blocks can clear
        if (self.is_straight(x1,y1,x2,y2,answer) == True):
            answer.append([x1,y1])
            return True
        if (self.is_double_straight(x1,y1,x2,y2,answer) == True):
            answer.append([x1,y1])
            return True
        if (self.is_triple_straight(x1,y1,x2,y2,answer) == True):
            answer.append([x1,y1])
            return True
        else:
            return False
        
    def is_straight(self,x1,y1,x2,y2,answer):#check whether 2 blocks can be straight
        if (x1 == x2):
            off = y2 - y1
            if (abs(off) == 1):
                answer.append([x2,y2])
                return True
            off = off/abs(off)
            for j in range(y1+off,y2,off):
                if (self.flags[x1][j] != 0):
                    return False
            answer.append([x2,y2])
            return True
        if (y1 == y2):
            off = x2 - x1
            if (abs(off) == 1):
                answer.append([x2,y2])
                return True
            off = off/abs(off)
            for i in range(x1+off,x2,off):
                if (self.flags[i][y1] != 0):
                    return False
            answer.append([x2,y2])
            return True
        return False

    def is_double_straight(self,x1,y1,x2,y2,answer):#check whether 2 block can be a double_straight
        for i in range(x1-1,-1,-1):
            if (self.flags[i][y1] != 0):
                break
            if (self.is_straight(i,y1,x2,y2,answer) == True):
                answer.append([i,y1])
                return True
        for i in range(x1+1,self.len+2,1):
            if (self.flags[i][y1] != 0):
                break
            if (self.is_straight(i,y1,x2,y2,answer) == True):
                answer.append([i,y1])
                return True
        for j in range(y1-1,-1,-1):
            if (self.flags[x1][j] != 0):
                break
            if (self.is_straight(x1,j,x2,y2,answer) == True):
                answer.append([x1,j])
                return True
        for j in range(y1+1,self.wid+2,1):
            if (self.flags[x1][j] != 0):
                break
            if (self.is_straight(x1,j,x2,y2,answer) == True):
                answer.append([x1,j])
                return True
        return False

    def is_triple_straight(self,x1,y1,x2,y2,answer):#check whether 2 block can be a triple_staright
        for i in range(x1-1,-1,-1):
            if (self.flags[i][y1] != 0):
                break
            if (self.is_double_straight(i,y1,x2,y2,answer) == True):
                answer.append([i,y1])
                return True
        for i in range(x1+1,self.len+2,1):
            if (self.flags[i][y1] != 0):
                break
            if (self.is_double_straight(i,y1,x2,y2,answer) == True):
                answer.append([i,y1])
                return True
        for j in range(y1-1,-1,-1):
            if (self.flags[x1][j] != 0):
                break
            if (self.is_double_straight(x1,j,x2,y2,answer) == True):
                answer.append([x1,j])
                return True
        for j in range(y1+1,self.wid+2,1):
            if (self.flags[x1][j] != 0):
                break
            if (self.is_double_straight(x1,j,x2,y2,answer) == True):
                answer.append([x1,j])
                return True
class Game:#the game controller to manage the whole game
    def __init__(self,win):
        self.w = win
        self.level = 3
        self.len = 10
        self.wid = 14
        self.time = 150
        self.help_num = 24
        self.real_time = time.time()
        self.box = Box(win,self.len,self.wid)
        self.box.init_flag()
        self.box.init_block()
        self.box.draw()
        self.hButton = Button(win,Point(8.5,4.5),1,0.3, "High Level")
        #self.hButton.activate()
        self.lButton = Button(win,Point(8.5,4.0),1,0.3, "Low Level")
        self.lButton.activate()
        self.rButton = Button(win,Point(8.5,3.5),1,0.3, "Restart")
        self.rButton.activate()
        self.qButton = Button(win,Point(8.5,2.5),1,0.3, "Quit")
        self.qButton.activate()
        self.tButton = Button(win,Point(8.5,3.0),1,0.3, "Help")
        self.tButton.activate()
        self.tip = Text(Point(8.5,1.0),"Gaming")
        self.help_info = Text(Point(8.5,1.5),"Remain: 24")
        self.winning_info = Text(Point(4.0,3.0),"")
        self.winning_info.draw(win)
        self.timing = Text(Point(8.5,2.0),"150 second")
        self.help_info.draw(win)
        self.tip.draw(win)
        self.timing.draw(win)
    def setLevel(self):#a set level function to decide which level to take
        if (self.level == 1):
            self.len = 6
            self.wid = 8
        elif (self.level == 2):
            self.len = 8
            self.wid = 10
        elif (self.level == 3):
            self.len = 10
            self.wid = 14
        self.Restart()
    def ClickedMusic(self):#music logic but not taken for it can low down the whole program
        winsound.PlaySound("./music/1.wav",winsound.SND_ASYNC)
    def ClearMusic(self):
        winsound.PlaySound("./music/2.wav",0)
    def CancelMusic(self):
        winsound.PlaySound("./music/3.wav",0)
    def Restart(self):#restart the game
        self.help_num = self.level*8
        self.time = 50*self.level
        self.real_time = time.time()
        self.box.undraw()
        del self.box
        self.box = Box(self.w,self.len,self.wid)
        self.box.init_flag()
        self.box.init_block()
        self.box.draw()
        help_info_str = "Remain: "+str(self.help_num)
        self.help_info.setText(help_info_str)
        self.tip.setText("Gaming")
        self.winning_info.setText("")
        self.tButton.activate()

    def wait_for_command(self):#a logic which the game ends
        while (True):
            q = self.w.checkMouse()
            if (q):
                if (self.qButton.clicked(q)):
                    return 1
                if (self.rButton.clicked(q)):
                    self.Restart()
                    break
                if (self.hButton.clicked(q)):
                    self.level += 1
                    self.setLevel()
                    if (self.level == 3):
                        self.hButton.deactivate()
                    self.lButton.activate()
                    break
                if (self.lButton.clicked(q)):
                    self.level -= 1
                    self.setLevel()
                    if (self.level == 1):
                        self.lButton.deactivate()
                    self.hButton.activate()
                    break
        return 0
        
    def Run(self):#the main logic to run the game
        while (True):
            try:
                time_tmp = time.time()
                if (time_tmp - self.real_time >= 1.0):
                    self.time -= 1
                    self.real_time = time_tmp
                    tmp_info = str(self.time)+" second"
                    self.timing.setText(tmp_info)
            #=======================Game Logic=========================#
                if (self.time < 0):#lose
                    self.tip.setText("Game over!!!")
                    flag = self.wait_for_command()
                    if (flag == 1):
                        break
                answer = []
                if (self.box.FindAnswer(answer) == False):
                    self.tip.setText("Game over!!!")
                    flag = self.wait_for_command()
                    if (flag == 1):
                        break
                q = self.w.checkMouse()
                if (q):
                    x1 = -1
                    y1 = -1
                    x2 = -1
                    y2 = -1
                    xVal = q.getX()
                    yVal = q.getY()
                    answer = []
                    tmp = []
                    is_clicked = self.box.Clicked(xVal,yVal,tmp)
                    is_clear = False
                    if (is_clicked == True):
                        x1 = tmp[0][0]
                        y1 = tmp[0][1]
                        tmp = []
                        self.box.GetLast(tmp)
                        x2 = tmp[0][0]
                        y2 = tmp[0][1]
                        is_clear = self.box.Check(x1,y1,answer)
                        if (is_clear == True):
                            self.time += 2
                            self.box.Clear(x1,y1)
                        else:
                            self.box.NotClear(x1,y1)
            #=========================Logic Part========================#
            #=========================Render Part========================#
                    self.box.Render(is_clicked,is_clear,x1,y1,x2,y2,answer)
            #=========================Button Logic========================#
                    if (self.qButton.clicked(q)):
                        break
                    if (self.rButton.clicked(q)):
                        self.Restart()
                    if (self.hButton.clicked(q)):
                        self.level += 1
                        self.setLevel()
                        if (self.level == 3):
                            self.hButton.deactivate()
                        self.lButton.activate()
                    if (self.lButton.clicked(q)):
                        self.level -= 1
                        self.setLevel()
                        if (self.level == 1):
                            self.lButton.deactivate()
                        self.hButton.activate()
                    if (self.tButton.clicked(q)):#control the help logic
                        answer = []
                        if (self.box.FindAnswer(answer) == True):
                            self.box.gui_draw_line(answer)
                            self.help_num -= 1
                            help_info_str = "Remain: "+str(self.help_num)
                            self.help_info.setText(help_info_str)
                            if (self.help_num == 0):
                                self.tButton.deactivate()
            #==========================Game Logic========================#
                    if (self.box.getAll() == 0):#win
                        self.winning_info.setText("Congratulation, you win!!!")
                        self.tip.setText("You Win!!!")
                        flag = self.wait_for_command()
                        if (flag == 1):
                            break
            except e:
                print "a error has existed",e
                break
                
def main():
    win = GraphWin("Project",1000, 600)
    win.setCoords(0.0, 0.0, 9.0, 6.0)
    game = Game(win)
    #run_time = threading.Thread(target=game.Run_time)
    #run_time.start()
    game.Run()
    #run_time.join()
    win.close()

main()
