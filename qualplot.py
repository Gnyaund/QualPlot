import glob
import subprocess
import os
import shutil
import sqlite3
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2

from matplotlib import rcParams
rcParams.update({"figure.autolayout": True})

class Qualnet:
    def __init__(self, start, end, node, PATH):
        self.start = start
        self.end = end
        self.node = node
        self.QUALNET_PATH = PATH
    
    def checkCasename(self):
        self.qualnetfiles_path = []
        self.basenames = []
        for name in glob.glob(".\\qualnetfiles\\*.config"):
            configfile = name
        basename_ext = os.path.splitext(os.path.basename(configfile))[0]
        self.casename = basename_ext

        for name in glob.glob(".\\qualnetfiles\\" + basename_ext + "*"):
            self.qualnetfiles_path.append(name)

        for name in self.qualnetfiles_path:
            self.basenames.append(os.path.basename(name))
    
    def qualFilesCopy(self):
        for (qualfile, base) in zip(self.qualnetfiles_path, self.basenames):
            shutil.copy2(qualfile, ".\\" + base)
    
    def deleteCopyFiles(self):
            for base in self.basenames:
                os.remove(".\\" + base)
  
    def executeQualnet(self):
        print("Not Available on University VPN or Network")
        print("Are you sure?    yes(y)/ or no(n)")
        check = input()
        if (check == "n"):
            self.deleteCopyFiles()
            exit()
        elif (check == "y"):
                QUALNET_PATH = self.QUALNET_PATH 
                print("RUNNING QUALNET")
                i = self.start - 1
                while i < self.end:
                    i += 1
                    z = QUALNET_PATH + (" {0}.config seed{1} -seed {1}" .format(self.casename, i))
                    returncode = subprocess.Popen(z, shell=True)
                    returncode.wait()
                print("PROCESS END")
        else:
            self.executeQualnet()
    
    def moveArchives(self):
        if os.path.exists(".\\qualnetfiles\\archives") == False:
            os.mkdir(".\\qualnetfiles\\archives")
        if os.path.exists(".\\qualnetfiles\\archives\\" + self.casename) == False:
            os.mkdir((".\\qualnetfiles\\archives\\" + self.casename))
        start = self.start
        end = self.end
        for i in range(start, end + 1):
            shutil.move("seed{0}.db" .format(i), ".\\qualnetfiles\\archives\\" + self.casename + "\\" + "seed{0}.db" .format(i))          
            shutil.move("seed{0}.stat" .format(i), ".\\qualnetfiles\\archives\\" + self.casename + "\\" + "seed{0}.stat" .format(i))

        for file in self.basenames:
            shutil.move(".\\qualnetfiles\\" + file,".\\qualnetfiles\\archives\\"+ self.casename + "\\" + file)

class MakeCSV(Qualnet):
    def __init__(self, start, end, node, PATH):
         super().__init__(start, end, node, PATH)

    def makeCsvFolder(self):
        if os.path.exists("csv") == False:
            os.mkdir("csv")
    
    def extractSendingPacket(self):
        i=self.start-1
        #seed毎に各nodeの送信パケットを抽出
        while i<self.end:
            i+=1
            con = sqlite3.connect("seed{0}.db" .format(i))
            c=con.cursor()
            j=0
            while j<self.node:
                j+=1
                c.execute('select * from NETWORK_Events where (NodeID is {0}) and (EventType is "NetworkSendToLower")' .format(j))
                list = c.fetchall()
                with open('csv/Seed{0}-Node{1}.csv' .format(i, j),'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(list)
            con.close()

    def moveArchives(self):
        super().moveArchives()
        shutil.move(".\\csv",".\\qualnetfiles\\archives\\" + self.casename)


class DataPlot(MakeCSV):
    def __init__(self, start, end, node, PATH):
        super().__init__(start, end, node, PATH)

    def makeAnalysisFolder(self):
        if os.path.exists("analysis") == False:
            os.mkdir("analysis")
        
    def executePlot(self):
        a = self.start
        b = self.end
        n = self.node
        i=0
        s=a-1

        #name=['no','time','c','d','src','dst','size','h','i','j','k','l','m','n','o','p']
        name=['time','size']

        #seed回数実行
        while s<b:
            s+=1
            #Node回数実行
            while i<n:
                j=0
                i+=1
                #csvの読み込み
                node=pd.read_csv("csv/Seed{0}-Node{1}.csv" .format(s, i), header=None, usecols=[1,6], names=name)
                #空行を埋めるために各秒数にsize0の行を挿入
                while j<181:
                    node = node.append(pd.DataFrame({'time' :[j]}))
                    j+=1
                node['time'] = np.ceil(node['time'])
                #整数値に直してる
                #グループ化してcsvに書き出し
                node=node.groupby('time')[['size']].sum()
                #合計してる
                #kbpsに直す
                node['size']*=8
                node['size']/=1000
                #グラフをプロットして保存
                node.plot(legend=False, color='black')
                plt.xlabel("Time(Second)", fontsize=15)
                plt.ylabel("Size(KBit)", fontsize=15)
                plt.xlim([0,180])
                plt.ylim([0,180])
                plt.xticks(fontsize=15)
                plt.yticks(fontsize=15)
                plt.savefig("analysis/Seed{0}-Node{1}graph.png" .format(s, i))
                #これやらないとメモリがやばい
                plt.close('all')
                node.to_csv("analysis/Seed{0}-Node{1}group.csv" .format(s, i))
                
            i=0


    def makeCombinegraphFolder(self):
            if os.path.exists("combinegraph") == False:
                os.mkdir("combinegraph")

    def combinePlot(self):
        a = self.end
        n = self.node

        s=0
        im=[]
        i=0

        while s<a:
            s+=1
            while i<n:
                i+=1
                im.append(cv2.imread("analysis/Seed{0}-Node{1}graph.png" .format(s, i)))
            
            i=0
            im.append(cv2.imread("white.png"))
            im1 = cv2.vconcat([im[3],im[2],im[1],im[0]])
            im2 = cv2.vconcat([im[7],im[6],im[5],im[4]])
            im3 = cv2.vconcat([im[11],im[10],im[9],im[8]])
            im4 = cv2.vconcat([im[15],im[14],im[13],im[12]])
            im5 = cv2.hconcat([im1, im2, im3, im4])

            cv2.imwrite("combinegraph/Seed{0}CombineGraph.jpg" .format(s), im5)
            im.clear()

            print("DONE")

    def moveArchives(self):
        super().moveArchives()
        shutil.move(".\\analysis", ".\\qualnetfiles\\archives\\" + self.casename)
        shutil.move(".\\combinegraph", ".\\qualnetfiles\\archives\\" + self.casename)


if __name__ == "__main__":
    QUALNET_PATH = "..\\..\\..\\..\\..\\..\\qualnet\\7.4\\bin\\qualnet.exe"

    print("SEED START Number ->")
    start = int(input())
    print("SEED END Number ->")
    end = int(input())
    print("MAX NODE Number ->")
    node = int(input())


    c = DataPlot(start, end, node, QUALNET_PATH)
    
    c.checkCasename()
    c.qualFilesCopy()
    c.executeQualnet()
    
    c.makeCsvFolder()
    c.extractSendingPacket()

    c.makeAnalysisFolder()
    c.executePlot()

    c.makeCombinegraphFolder()
    c.combinePlot()

    c.deleteCopyFiles()
    c.moveArchives()