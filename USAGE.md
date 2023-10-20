# 使用方法

Windows下Python的多线程有点问题，所以最好在Linux下运行......

## 环境配置

直接 `bash create_env.sh` 就行。

## 数据生成

运行 `paper code/generate_synthetic_data.py` 生成数据，例：

```bash
python paper\ code/generate_synthetic_data.py --window-size 5 --variables 5 --cluster-list 0 1 1 0 2 2 2 0 --segment-samples 500 --sparsity 0.2 --seed 0 --data_dir ./data
```

- 使用窗口大小5生成数据
- 变量数为5
- 时间序列每一段对应的簇的编号分别为0,1,1,0,2,2,2,0
- 每段的长度为500
- 两个变量间不独立的概率为0.2
- 随即种子为0
- 数据输出至 `./data` 目录下

输出的 `*_seq.csv` 文件为多变量时间序列，`*_clusterN_cov.csv` 为第N个簇的协方差矩阵，`*_clusterN_inv.csv` 为第N个簇的逆协方差矩阵。

## 聚类

运行 `main.py` 进行聚类，例：

```bash
python main.py --window-size 5 --clusters 3 --lambda 11e-2 --beta 600 --max-iters 100 --threshold 2e-5 --processes 1 --data ./data/10191201_w\=1\&v\=5\&cl\=0\,1\,1\,0\,2\,2\,2\,0\&ss\=500\&sp\=0.2_seq.csv --out ./out
```

- 使用窗口大小5进行聚类
- 设置簇个数为3
- 优化目标中的正则项系数 $\lambda$ 设置为11e-2
- 优化目标中的时间不变性平衡因子 $\beta$ 设置为600
- 最大迭代次数为100
- 收敛阈值设置为2e-5
- 使用1个线程计算
- 输入数据为 `./data/10191201_w=1&v=5&cl=0,1,1,0,2,2,2,0&ss=500&sp=0.2_seq.csv`
- 结果输出至 `./out` 目录下

输出的 `.jpg` 图像为最终时间序列在各个簇的分布情况，`assignment.out` 为分配的簇标号，`mrf_N.out` 为第N个簇所估计的MRF的逆协方差矩阵。