import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import json
from PIL import Image
import io
import base64

# 设置页面
st.set_page_config(
    page_title="岩爆等级预测系统",
    page_icon="🪨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 苹果风格CSS */
    .main {
        background-color: #f5f5f7;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stButton>button {
        background-color: #0071e3;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0077ED;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        font-weight: 600;
    }
    .prediction-box {
        background-color: white;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        padding: 30px;
        margin: 20px 0;
        transition: all 0.3s ease;
    }
    .prediction-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    }
    .info-text {
        color: #86868b;
        font-size: 16px;
        line-height: 1.6;
    }
    .card {
        background-color: white;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.title("🪨 智能岩爆等级预测系统")
st.markdown('<p class="info-text">基于先进的机器学习算法，帮助您预测岩石的岩爆倾向等级</p>', unsafe_allow_html=True)

# 创建动画加载效果
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# 侧边栏配置
with st.sidebar:
    st.image("https://via.placeholder.com/150x80?text=岩爆预测", width=150)
    st.markdown("## 参数设置")
    st.markdown("请选择岩石样本的关键参数:")
    
    # 岩石种类选择
    rock_types = {
        "花岗岩": 1.0,
        "大理岩": 2.0,
        "石灰岩": 3.0,
        "砂岩": 4.0,
        "页岩": 5.0
    }
    selected_rock = st.selectbox("岩石种类", list(rock_types.keys()))
    rock_type_encoded = rock_types[selected_rock]
    
    # 其他参数
    sigma_theta = st.slider("σθ / Mpa (围岩应力)", 10.0, 200.0, 50.0, 0.1)
    sigma_c = st.slider("σc / Mpa (单轴抗压强度)", 20.0, 300.0, 100.0, 0.1)
    sigma_t = st.slider("σt / MPa (抗拉强度)", 1.0, 50.0, 10.0, 0.1)
    
    # 自动计算比率
    sigma_theta_c_ratio = sigma_theta / sigma_c
    sigma_c_t_ratio = sigma_c / sigma_t
    
    # 显示计算出的比率
    st.markdown(f"**σθ/σc 比值**: {sigma_theta_c_ratio:.2f}")
    st.markdown(f"**σc/σt 比值**: {sigma_c_t_ratio:.2f}")
    
    # 含水率
    wet = st.slider("含水率 (Wet)", 0.0, 1.0, 0.5, 0.01)
    
    st.markdown("---")
    st.markdown("### 关于")
    st.markdown("本系统使用堆叠分类器模型，基于多项特征对岩爆等级进行预测")

# 主要内容区
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("岩石参数汇总")
    
    # 创建参数表格
    data = {
        "参数": ["岩石种类", "σθ / Mpa (围岩应力)", "σc / Mpa (单轴抗压强度)", 
                "σt / MPa (抗拉强度)", "σθ/σc", "σc/σt", "含水率 (Wet)"],
        "数值": [selected_rock, sigma_theta, sigma_c, sigma_t, 
               sigma_theta_c_ratio, sigma_c_t_ratio, wet]
    }
    
    params_df = pd.DataFrame(data)
    st.table(params_df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 预测按钮
    if st.button("开始预测", key="predict_button"):
        with st.spinner("正在分析岩石参数，请稍候..."):
            # 显示进度条
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # 准备API请求数据
            input_data = {
                "rock_type": rock_type_encoded,
                "sigma_theta": sigma_theta,
                "sigma_c": sigma_c,
                "sigma_t": sigma_t,
                "sigma_theta_c_ratio": sigma_theta_c_ratio,
                "sigma_c_t_ratio": sigma_c_t_ratio,
                "wet": wet
            }
            
            # 替换为您的API地址
            API_URL = "http://localhost:8000/predict"
            
            try:
                # 发送API请求
                response = requests.post(API_URL, json=input_data)
                result = response.json()
                
                st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                st.success("分析完成!")
                
                # 结果展示
                grade_text = result["prediction_text"]
                prediction = result["prediction"]
                
                # 根据预测结果设置颜色
                colors = {0: "#4CAF50", 1: "#FFC107", 2: "#FF9800", 3: "#F44336"}
                grade_color = colors.get(prediction, "#9E9E9E")
                
                st.markdown(f"<h2 style='color:{grade_color}'>预测结果: {grade_text}</h2>", unsafe_allow_html=True)
                
                # 显示各类别概率
                probabilities = result["probabilities"]
                
                # 结果解释
                st.subheader("预测解释")
                st.markdown(f"""
                根据您提供的岩石参数，预测该样本的岩爆等级为**{grade_text}**。
                此预测基于样本的物理特性分析，包括围岩应力、抗压强度和抗拉强度等关键参数。
                """)
                
                # 显示概率详情
                st.markdown("### 各等级概率")
                probs_df = pd.DataFrame({
                    "岩爆等级": ["无岩爆倾向", "弱岩爆倾向", "中等岩爆倾向", "强岩爆倾向"],
                    "概率": [
                        probabilities.get("Class 0", 0),
                        probabilities.get("Class 1", 0),
                        probabilities.get("Class 2", 0),
                        probabilities.get("Class 3", 0)
                    ]
                })
                
                # 使用Plotly创建条形图
                fig = px.bar(
                    probs_df, 
                    x="岩爆等级", 
                    y="概率", 
                    color="岩爆等级",
                    color_discrete_map={
                        "无岩爆倾向": "#4CAF50",
                        "弱岩爆倾向": "#FFC107",
                        "中等岩爆倾向": "#FF9800",
                        "强岩爆倾向": "#F44336"
                    }
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=30, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"预测过程中出现错误: {str(e)}")
                st.markdown("请检查API服务是否正常运行，或联系系统管理员。")

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("岩爆等级说明")
    
    # 岩爆等级解释
    grade_info = {
        "无岩爆倾向 (0级)": "岩石在开挖过程中稳定性较好，不易发生岩爆现象。",
        "弱岩爆倾向 (1级)": "岩石可能会发生轻微的岩体破坏，但规模小，危害有限。",
        "中等岩爆倾向 (2级)": "岩石有较明显的岩爆倾向，可能会发生中等规模的岩爆事件，需要采取预防措施。",
        "强岩爆倾向 (3级)": "岩石具有强烈的岩爆倾向，极易发生大规模岩爆事件，需要严格的监测和防护措施。"
    }
    
    for grade, description in grade_info.items():
        st.markdown(f"**{grade}**")
        st.markdown(f"<p class='info-text'>{description}</p>", unsafe_allow_html=True)
        st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 添加建议卡片
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("岩爆防治建议")
    st.markdown("""
    <p class='info-text'>
    - 在进行隧道或地下工程开挖前，建议进行详细的岩体稳定性评估<br>
    - 对于中高岩爆倾向区域，应采用控制爆破技术<br>
    - 考虑使用预裂爆破、光面爆破等方法减小爆破震动<br>
    - 对于强岩爆倾向区域，可采用预应力释放钻孔等措施<br>
    - 加强监测工作，及时发现岩爆前兆
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown("---")
st.markdown("<center>© 2023 岩爆预测系统 | 技术支持: AI岩石力学实验室</center>", unsafe_allow_html=True)
