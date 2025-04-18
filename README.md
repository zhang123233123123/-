# 岩爆等级预测系统

## 项目简介

这是一个基于机器学习的岩爆等级预测系统，可以根据岩石的物理特性预测其岩爆倾向等级。该系统使用了堆叠分类器模型，结合了多种先进的机器学习算法，提供高精度的预测结果。

开发单位：中南大学岩土安全与可持续研究实验室

## 特点

- 美观的苹果风格用户界面
- 直观的参数输入和结果展示
- 详细的预测概率分析
- 岩爆等级解释和防治建议

## 使用方法

1. 选择岩石种类
2. 输入岩石的物理参数：
   - 围岩应力 (σθ / Mpa)
   - 单轴抗压强度 (σc / Mpa)
   - 抗拉强度 (σt / MPa)
   - 含水率 (Wet)
3. 点击"开始预测"按钮
4. 查看预测结果和建议

## 本地运行

```bash
# 克隆仓库
git clone https://github.com/yourusername/rock-burst-prediction.git
cd rock-burst-prediction

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run streamlit_app.py
```

## 岩爆等级说明

- **无岩爆倾向 (0级)**: 岩石在开挖过程中稳定性较好，不易发生岩爆现象。
- **弱岩爆倾向 (1级)**: 岩石可能会发生轻微的岩体破坏，但规模小，危害有限。
- **中等岩爆倾向 (2级)**: 岩石有较明显的岩爆倾向，可能会发生中等规模的岩爆事件，需要采取预防措施。
- **强岩爆倾向 (3级)**: 岩石具有强烈的岩爆倾向，极易发生大规模岩爆事件，需要严格的监测和防护措施。

## 模型说明

该预测系统使用了堆叠分类器模型，结合了以下算法：
- 极限树分类器 (Extra Trees)
- XGBoost
- LightGBM
- 随机森林
- 梯度提升

## 许可证

MIT
