import matplotlib.pyplot as plt

# 读取文件
file_path = "eta_small"  # 替换为你的文件路径
with open(file_path, 'r') as f:
    lines = f.readlines()

# 解析数据
x = list(map(float, lines[0].strip().split()))  # 第一行为x坐标
curves = []
for line in lines[1:]:
    if line.strip():  # 跳过空行
        curves.append(list(map(float, line.strip().split())))

# 验证数据长度一致性
for i, y in enumerate(curves, 1):
    if len(y) != len(x):
        raise ValueError(f"第{i+1}行的数据长度({len(y)})与x坐标长度({len(x)})不一致")

# 绘制图形
plt.figure(figsize=(10, 6))
for idx, y in enumerate(curves, 1):
    plt.plot(x, y, label=f'Curve {idx}')

plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Multiple Curves Visualization')
plt.grid(True)
plt.legend()
plt.savefig(file_path + 'output.png', dpi=300, bbox_inches='tight')  # <-- 新增的保存命令
plt.show()
