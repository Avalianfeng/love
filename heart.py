import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # 确保打包后图形正常显示
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import sys
import io
import random
import time
ti = 0
print("程序开始运行，正在生成 3D 爱心动画...\r")
love_txt=['I LOVE YOU', '我的宝贝', '亲爱的', 'jenny', 'SAYANG', 'dear', 'Sayang', 'satang', 'Forever Yours',
 '心动时刻', '小可爱', 'Baby', 'Darling', 'My Heart', 'Jenny', 'JENNYLove', 'Sweetie', '爱你永远',
 'Baby', 'SISTER LOVE', 'My Only', '心肝宝贝', '最爱', '宝贝', 'Honey', 'Jenny Forever', 'jenny Dear',
 '真爱', 'My Sweet', '可爱jee', 'Dear 珍妮', 'I’m Yours', '宝贝儿', 'Jee爱', 'JEE Baby', 'J Love',
 'jee Sweet', 'Baby', 'Eternal Love', '心跳为你', '小甜心', 'sayang亲亲', 'My Darling', '爱你到老', 'Heart',
 'Mine', 'Forever', 'My Love', '甜蜜宝贝', '亲爱的你', '心', 'jenny Sweetie', 'My Dear', ' sweet sister', 'our Heart',
 'Always Yours', '心动', '宝贝可爱', 'My Angel', '爱你不变', '520 Darling', '1314 Baby', 'jee Sweetie', 'Forever Love',
 '甜甜的你', '亲爱的you', 'jee宝', 'sayang Mine', 'my Heart', 'JENNY Dear', 'JENNY Love', 'My Everything', '心动不已', '小宝贝',
 'Jee甜心', 'Dear One', '爱你一生', 'SAYANG Love', 'JENNY Forever', 'JENNY Darling', 'My Treasure', '宝贝Jee', '亲爱的宝', 'JENNY亲',
 'SAYANG Sweet', 'SAYANG Baby', 'JENNY Heart', 'JENNY Mine', 'True Love', '心跳时刻', '可爱宝贝', 'Jee我的', 'My Beloved', '爱你无尽',
 'SAYANG Dear', 'JENNY Sweet', 'JENNY Baby', 'My Soulmate', '甜蜜Jee', '亲爱的爱', 'JENNY甜', 'SAYANG Heartbeat']


# 设置 UTF-8 编码以支持中文输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 初始化图形
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# 爱心参数方程
def heart_3d(t, z):
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    return x, y, z


# 数据准备
t = np.linspace(0, 2 * np.pi, 100)
z = np.linspace(-5, 5, 50)
T, Z = np.meshgrid(t, z)  # 创建网格
X, Y, _ = heart_3d(T, Z)  # 计算 3D 坐标

points = []
for zi in z:
    x, y, _ = heart_3d(t, zi)
    for xi, yi in zip(x, y):
        points.append([xi, yi, zi])
points = np.array(points)

# 初始化进度条
text="生成动画帧"
total_frames = 360 // 2  # frames=range(0, 360, 2)
pbar = tqdm(total=total_frames, desc=text,
            bar_format='{l_bar}{bar:30} {n_fmt}/{total_fmt} [{percentage:3.0f}%] ',
            colour='green')

#生成帧
def update(frame):
    global ti
    ti += 1
    ax.cla()  # 清除上一帧
    ax.view_init(elev=10, azim=frame / 2)

    # 绘制管状爱心
    for zi in z:
        x, y, _ = heart_3d(t, zi)
        # 增加厚度：绘制多层偏移曲线
        ax.plot(x, y , zi, c=plt.cm.hot((zi + 5) / ti), alpha=0.5, linewidth=2)
    # 添加动态文字
    text_x = 10 * np.cos(frame / 20)
    text_y = 10 * np.sin(frame / 20)
    text_z = np.sin(frame / 20) * 2  # 文字在 z 轴上缓慢上下移动
    text_color1 = plt.cm.inferno((frame+100) / 360)  # 颜色渐变
    text_color2 = plt.cm.inferno(frame / 360)  # 颜色渐变
    fontsize = 30 + 5 * np.sin(frame / 20)  # 字体大小随帧变化
    alpha = abs(np.sin(frame / 10))  # 透明度随帧变化
    ax.text(text_x, text_y, text_z + 5, "LOVE YOU", fontsize=fontsize, fontfamily='SimHei',
            color=text_color1, ha='center', va='center', fontweight='bold',
            bbox=dict(facecolor='none', edgecolor='none', alpha=alpha))

    for offset in [-1, 1]:
        fontsize = 20 - 5 * np.sin(frame / 20)
        for text in love_txt:
            text_x=10 * np.cos(frame / 20+random.random())
            text_y=10 * np.sin(frame / 20+random.random())
            ax.text(text_x+random.randint(-200,200),text_y+random.randint(-100,100), text_z + 5, text.strip(), fontsize=fontsize+random.randint(-int(fontsize)+10,10), fontfamily='SimHei',
                color=text_color2, ha='center', va='center', alpha=0.3)
    ax.set_axis_off()
    pbar.update(1)  # 更新进度条
    if(ti>=180):
        if(ti<181):
            pbar.close()
    return ax,
random.seed(time.time())
# 创建动画

ani = FuncAnimation(fig, update, frames=range(0, 360, 2), interval=50)
plt.show()
