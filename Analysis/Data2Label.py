#!/mnt/storagedata1/renjj/anaconda3/bin/python
# -*- coding:utf-8 -*-

'''
Copyright (C) 2019  CCLI GROUP, PKU
Copyright (C) 2019  Jingjing Ren
NAME
        Data2Label.py
PURPOSE

PROGRAMMER(S)
        Ren Jingjing
REVISION HISTORY

REFERENCES

----------------------------------------------------------
If you have any question, please email:renjj@pku.edu.cn
----------------------------------------------------------
'''

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image,ImageEnhance,ImageDraw,ImageFont
import xlrd
import os

f = open('./dummy-data.txt','r')
lines = f.readlines()
f.close()
Type = []
Brand = []
Category = []
Model = []
Barcode = []
Date = []
EE = []
Metal = [] 
Elec = []
Plastic = []
Lifetime =[]
Water = []
Recycle = []
CO2 = []
GHG = []
Repair = []

for line in lines[1:]:
    Type.append(line.strip().split(',')[0])
    Brand .append(line.strip().split(',')[1])
    Category.append(line.strip().split(',')[2])
    Model.append(line.strip().split(',')[3])
    Barcode.append((line.strip().split(',')[4]))
    Date.append(line.strip().split(',')[5])
    EE.append(int(line.strip().split(',')[6]))
    Metal.append(float(line.strip().split(',')[7]))
    Elec.append(float(line.strip().split(',')[8]))
    Plastic.append(float(line.strip().split(',')[9]))
    Lifetime.append(float(line.strip().split(',')[10]))
    Water.append(float(line.strip().split(',')[11]))
    Recycle.append(int(line.strip().split(',')[12]))
    CO2.append(float(line.strip().split(',')[13]))
    GHG.append(float(line.strip().split(',')[14]))
    Repair.append(int(line.strip().split(',')[15]))


EE = np.array(EE)
Metal =   np.array(Metal) 
Elec =  np.array(Elec)
Plastic =  np.array(Plastic)
Lifetime = np.array(Lifetime)
Water =  np.array(Water)
Recycle = np.array(Recycle) 
CO2 = np.array(CO2)
GHG = np.array(GHG)
Repair = np.array(Repair)


Gas =[(((CO2[i]-np.min(CO2))/(np.max(CO2)-np.min(CO2)) + (GHG[i]-np.min(GHG[i]))/(np.max(GHG)-np.min(GHG)))/Lifetime[i]) for i in range(len(CO2))]
GasNor = [(((Gas[i]-np.min(Gas))/(np.max(Gas)-np.min(Gas)))*0.9+0.1) for i in range(len(CO2))]
Energy =[(((Metal[i]-np.min(Metal))/(np.max(Metal)-np.min(Metal))+(Elec[i]-np.min(Elec))/(np.max(Elec)-np.min(Elec)))/Lifetime[i]) for i in range(len(Metal))]
EnergyNor = [(((Energy[i] - np.min(Energy))/(np.max(Energy)-np.min(Energy)))*0.9+0.1) for i in range(len(Energy))]
Waste =[(((Plastic[i]-np.min(Plastic))/(np.max(Plastic)-np.min(Plastic))+(Water[i]-np.min(Water))/(np.max(Water)-np.min(Water)))/Lifetime[i]) for i in range(len(Plastic))]
WasteNor = [(((Waste[i]-np.min(Waste))/(np.max(Waste)-np.min(Waste)))*0.9+0.1) for i in range(len(Waste))]

#Lable Input
LevelLabel = xlrd.open_workbook('./LevelPic/LevelLabel.xlsx')
sheet = LevelLabel.sheet_by_name('Sheet2')
Trees = sheet.col_values(8)[1:]
FamilyWater = sheet.col_values(11)[1:]
Running = sheet.col_values(15)[1:]


#barcode = input('Product Barcode:')
#if barcode =='':
#    barcode = '0125551234501'
#
#input_str = input('Loveness of variable:Gas,(water+plastic),energy,energy efficiency,recycle and repair:')
# read out.json as barcode and input_str
#os.system("move C:\\Users\\任静静\\Downloads\\out.json .\\out.json")
f = open('out.json','r')
barcode = f.readlines()[1].strip().split(",")[0].split("\"")[1]
ind = Barcode.index(barcode)
print (barcode)
f.close()
f= open("out.json",'r')
wei_gas= f.readlines()[5].strip()
f.close()
f= open("out.json",'r')
wei_water= f.readlines()[9].strip()
f.close()
f= open("out.json",'r')
wei_ener= f.readlines()[13].strip()
f.close()
f= open("out.json",'r')
wei_ee= f.readlines()[17].strip()
f.close()
f= open("out.json",'r')
wei_rr= f.readlines()[21].strip()
f.close()

a = []
#if input_str =='':
#    a = [0.2] * 5
#else:
a.append(float(wei_gas)/100)
a.append(float(wei_water)/100)
a.append(float(wei_ener)/100)
a.append(float(wei_ee)/100)
a.append(float(wei_rr)/100)
    #a = [float(x) for x in input_str.split(",")]
print (sum(a))
if sum(a) <=1.0:
    a1, a2, a3, a4, a5 = a
    CIR =np.multiply(a1,GasNor[ind])+np.multiply(a2,WasteNor[ind])+np.multiply(a3,EnergyNor[ind])+np.multiply(a4/4.0,EE[ind])+np.multiply(a5/18.0,18-Recycle[ind]-Repair[ind])  
    CIRAll =np.multiply(a1,GasNor)+np.multiply(a2,WasteNor)+np.multiply(a3,EnergyNor)+np.multiply(a4/4.0,EE)+np.multiply(a5/18.0,18-Recycle-Repair)  
    #Cir 在24个产品中的顺序
    indcirsort = np.argsort(CIRAll)
    SortCir = indcirsort.tolist().index(ind)

    # 雷达图绘制
    # meshgrid draw

    lables = np.array(['Gas\n%.2f(kg/year)'%((CO2[ind]+GHG[ind])/Lifetime[ind]),'Water,Plastic\n%.2f(kg/year)'%((Water[ind]+Plastic[ind])/Lifetime[ind]),'Energy\n%.2f(MJ/year)'%((Elec[ind]+Metal[ind])/Lifetime[ind]),'Energy efficiency','Repair + Recycle'])#\n(%d/9 %d/9)'%(Repair[ind],Recycle[ind])])
    print (CO2[ind],GHG[ind],Lifetime[ind])
    nAttr = 5
    data = np.array([np.multiply(a1,GasNor[ind]),np.multiply(a2,WasteNor[ind]),np.multiply(a3,EnergyNor[ind]),np.multiply(a4/4.0,EE[ind]),np.multiply(a5/18.0,18-Recycle[ind]-Repair[ind])])  
    datamax = np.max(data)
    data = data/datamax
    angles = np.linspace(0,2*np.pi,nAttr,endpoint = False)
    radius = np.linspace(0,1,5)
    #angles,radius = np.meshgrid(radius,angles)
    data = np.concatenate((data,[data[0]]))
    angles = np.concatenate((angles,[angles[0]]))
    fig = plt.figure(figsize = (16,16),facecolor = 'white',dpi = 100)
    ax = fig.add_subplot(1,1,1,polar = True)
    plt.subplots_adjust(bottom = 0.3,top = 0.7,left = 0.2,right = 0.6)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('NW')
    ax.plot(angles,data,'o-',color = 'y',linewidth = 2)
    ax.fill(angles,data,alpha = 0.25)
    font1 = {'family':'Times','weight':'bold','size':24}
    
    ax.text(0,1.7,lables[0],font1)
    ax.text(2.0*np.pi/5.0,1.1,lables[1],font1)
    ax.text(2*2.0*np.pi/5.0,1.1,lables[2],font1)
    ax.text(3*2.0*np.pi/5.0,1.1,lables[3],font1) 
    ax.text(4*2.0*np.pi/5.0,2,lables[4],font1)
    #ax.set_thetagrids(angles*180/np.pi,lables,fontsize = 20)
    ax.set_rgrids(np.linspace(0,np.max(data),5),fontsize = 18)
    ax.set_rlabel_position(15)
    #ax.set_thetalabel_position(1.5)
    #ax.set_title('CIR of Container',fontsize =24)
    if SortCir >=19:
        ax.text(1.5,2.2,'ModelNo:%s'%(Model[ind]),fontsize = 30,weight = 'bold')
        ax.text(4.7,2.4,'CIR: %.2f\n\nLevel:5'%(CIR),fontsize = 30,weight = 'semibold',color = 'black',bbox = dict(facecolor = 'r',alpha = 0.2))
    if SortCir <19 and SortCir >=14:
        ax.text(1.5,2.2,'ModelNo:%s'%(Model[ind]),fontsize = 30,weight = 'bold')
        ax.text(4.7,2.4,'CIR: %.2f\n\nLevel:4'%(CIR),fontsize = 30,weight = 'semibold',color = 'black',bbox = dict(facecolor = 'orange',alpha = 0.2))
    if SortCir <14 and SortCir >=9:
        ax.text(1.5,2.2,'ModelNo:%s'%(Model[ind]),fontsize = 30,weight = 'bold')
        ax.text(4.7,2.4,'CIR: %.2f\n\nLevel:3'%(CIR),fontsize = 30,weight = 'semibold',color = 'black',bbox = dict(facecolor = 'yellow',alpha = 0.2))
    if SortCir <9 and SortCir >=4:
        ax.text(1.5,2.2,'ModelNo:%s'%(Model[ind]),fontsize = 30,weight = 'bold')
        ax.text(4.7,2.4,'CIR: %.2f\n\nLevel:2'%(CIR),fontsize = 30,weight = 'semibold',color = 'black',bbox = dict(facecolor = 'green',alpha = 0.2))
    if SortCir <4:
        ax.text(1.5,2.2,'ModelNo:%s'%(Model[ind]),fontsize = 30,weight = 'bold')
        ax.text(4.7,2.4,'CIR: %.2f\n\nLevel:1'%(CIR),fontsize = 30,weight = 'semibold',color = 'black',bbox = dict(facecolor = 'blue',alpha = 0.2))

    plt.savefig('cir_radar.jpg',dpi = 100)

    im = Image.open('cir_radar.jpg')
    if im.mode !='RGBA':
        im.convert('RGBA')
    print (im.size)
    # 导入图片
    if EE[ind]==1:
        EEpic = Image.open('./LevelPic/EE/EE1.png')
    if EE[ind]==2:
        EEpic = Image.open('./LevelPic/EE/EE2.png')
    if EE[ind]==3:
        EEpic = Image.open('./LevelPic/EE/EE3.png')
    if EE[ind]==4:
        EEpic = Image.open('./LevelPic/EE/EE4.png')
    EEpic = EEpic.resize((300,300))
    im.paste(EEpic,(900,1132,900+EEpic.size[0],1132+EEpic.size[1]))


    EnergyPic = Image.open('./LevelPic/Energy/Energy.jpg')
    EnergyPic = EnergyPic.resize((150,150))
    im.paste(EnergyPic,(1250,760,1250+EnergyPic.size[0],760+EnergyPic.size[1]))
    draw = ImageDraw.Draw(im)
    ttfont = ImageFont.truetype('PloverExtrabold Italic.ttf',32)
    draw.text((1300,920),'%d km'%(Running[ind]),font = ttfont,fill = (0,0,0))
    WaterPic = Image.open('./LevelPic/Water/Water.jpg')
    WaterPic = WaterPic.resize((150,150))
    im.paste(WaterPic,(750,230,750+WaterPic.size[0],230+WaterPic.size[1]))
    draw.text((770,390),'%.1f Months'%FamilyWater[ind],font = ttfont,fill = (0,0,0))
    GasPic = Image.open('./LevelPic/Gas/Tree.jpg')
    GasPic = GasPic.resize((150,150))
    im.paste(GasPic,(90,450,90+GasPic.size[0],450+GasPic.size[1]))
    draw.text((210,570),'%.1f'%Trees[ind],font =ttfont,fill = (0,0,0))
    draw.text((255,1095),'%d/9'%(Recycle[ind]),font = ttfont,fill = (0,0,0))
    draw.text((255,1135),'%d/9'%(Repair[ind]),font = ttfont,fill = (0,0,0))
    #draw.rectangle((10,10,1590,1590),fill = (0,0,0))
    CycPic = Image.open('./LevelPic/recycle.jpg')
    CycPic = CycPic.resize((30,30))
    im.paste(CycPic,(220,1095,220+CycPic.size[0],1095+CycPic.size[1]))
    PairPic = Image.open('./LevelPic/repair.jpg')
    PairPic = PairPic.resize((30,30))
    im.paste(PairPic,(220,1135,220+PairPic.size[0],1135+PairPic.size[1]))
    im.save('cir_radar2.png')


'''
# CIR 升序排列
CIRlabel = np.argsort(CIR)
ModelSort = [Model[CIRlabel[i]] for i in range(len(CIRlabel))]

print ('气候影响评级空调排序结果【环境最友好型--环境最不友好型】:')
print (ModelSort)
print ('气候影响评级数据：')
print (np.sort(CIR))

# 写出到txt
f1 = open('SortedDummyData.txt','w')
f1.write(lines[0])
for i in range(len(lines)-1):
    f1.writelines([Type[CIRlabel[i]],',',Brand[CIRlabel[i]],',',Category[CIRlabel[i]],',',Model[CIRlabel[i]],',',\
                   Barcode[CIRlabel[i]],',',Date[CIRlabel[i]],',',\
                   str(EE[CIRlabel[i]]),',',str(Metal[CIRlabel[i]]),',',\
                   str(Elec[CIRlabel[i]]),',',str(Plastic[CIRlabel[i]]),',',str(Lifetime[CIRlabel[i]]),',',str(Water[CIRlabel[i]]),\
                   str(Recycle[CIRlabel[i]]),',',str(CO2[CIRlabel[i]]),',',str(GHG[CIRlabel[i]]),',',str(Repair[CIRlabel[i]])])

    f1.write('\n')

f1.close()

# 将排序结果放在最后一列
H = np.zeros(24)
for i in range(24):
    hh = CIRlabel.tolist().index(i)
    H[i] = int(hh+1)
print (H)
f2 = open('SortedDummyData2.txt','w')
f2.write(lines[0])
for i in range(len(lines)-1):
    f2.write(lines[i+1])
    f2.write(str(H[i]))
    f2.write('\n')
f2.close()
'''
