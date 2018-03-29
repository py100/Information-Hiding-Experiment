import os
import matplotlib.pyplot as plt


percentRange = range(0, 101, 5)
# 进行隐写，i是隐写率
for i in percentRange:
    os.system("python LSB.py -H -p huidu.bmp -s HideInfo.bmp -c %d" % i)

# 进行RS分析并画图
bili = 70
Rm = []
R_m = []
Sm = []
S_m = []
percentRange2 = []
files = os.listdir("out")
for file in files:
    percentRange2.append(int(file.strip()[3:-4]))
percentRange2.sort()
for i in percentRange2:
    print("开始RS分析图片out%d.bmp" % i, end="\t\t", flush=True)
    result = os.popen("python RS.py out\\out%d.bmp %d" % (i, bili)).read()
    print("结束")
    [r1, r2, r3, r4] = result.strip().split(" ")
    Rm.append(float(r1))
    R_m.append(float(r2))
    Sm.append(float(r3))
    S_m.append(float(r4))

xaxis = list(percentRange2)
plt.plot(xaxis, Rm, 'b-', xaxis, R_m, 'b--', xaxis, Sm, 'g-', xaxis, S_m, 'g--')
print("Rm蓝色实线，R-m蓝色虚线，Sm绿色实线，S-m绿色虚线")
plt.axis([0, 100, 0, 1])
plt.show()
