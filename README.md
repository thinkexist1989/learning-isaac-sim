# 运行步骤

假设isaac sim的安装位置在`~/.local/share/ov/pkg/isaac_sim-2022.1.0`

假设本目录放置在`~/Desktop/isaac_assets`

1. 进入issac sim的安装目录

```bash
$ cd ~/.local/share/ov/pkg/isaac_sim-2022.1.0
```

2. 加载python环境变量

```bash
$ source setup_python_env.sh
```

3. 进入本目录

```bash
$ cd ~/Desktop/isaac_assets
```

4. 运行test1.py，注意：要用isaac_sim目录下的pyhon.sh运行，且运行目录必须在本目录下

```bash
$ ~/.local/share/ov/pkg/isaac_sim-2022.1.0/python.sh test1.py
```
