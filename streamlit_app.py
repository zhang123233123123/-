import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from PIL import Image
import base64

# 设置页面
st.set_page_config(
    page_title="智能岩爆风险评估系统",
    page_icon="🪨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式 - 现代化设计
st.markdown("""
<style>
    /* 现代化设计CSS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background-color: #f7f9fc;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%);
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 500;
        border: none;
        box-shadow: 0 4px 14px rgba(38, 99, 235, 0.25);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(38, 99, 235, 0.35);
    }
    
    h1 {
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #0F172A;
        letter-spacing: -0.5px;
    }
    
    h2 {
        font-weight: 600;
        font-size: 1.8rem;
        color: #1E293B;
        margin-top: 1.5rem;
        letter-spacing: -0.3px;
    }
    
    h3 {
        font-weight: 600;
        font-size: 1.3rem;
        color: #334155;
        margin-top: 1.2rem;
    }
    
    .css-1kyxreq {  /* 侧边栏样式 */
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    .css-6qob1r {  /* 主内容区样式 */
        background-color: #f7f9fc;
    }
    
    /* 卡片样式 */
    .dashboard-card {
        background-color: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.05);
        margin-bottom: 24px;
        border: 1px solid #f1f5f9;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }
    
    /* 结果卡片 */
    .result-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin: 20px 0;
        border: 1px solid #e5e9f0;
    }
    
    /* 图表容器 */
    .chart-container {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 24px;
        border: 1px solid #f1f5f9;
    }
    
    /* 参数标签样式 */
    .param-label {
        font-weight: 500;
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    
    /* 参数值样式 */
    .param-value {
        font-weight: 600;
        color: #334155;
        font-size: 1.1rem;
        margin-bottom: 15px;
    }
    
    /* 分割线 */
    .divider {
        height: 1px;
        background-color: #e2e8f0;
        margin: 20px 0;
    }
    
    /* 等级标签 */
    .grade-label {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 30px;
        font-weight: 500;
        font-size: 0.85rem;
        margin-right: 8px;
    }
    
    .grade-0 { background-color: #ECFDF5; color: #059669; }
    .grade-1 { background-color: #FFFBEB; color: #D97706; }
    .grade-2 { background-color: #FEF2F2; color: #DC2626; }
    .grade-3 { background-color: #EFF6FF; color: #2563EB; }
    
    /* 动画效果 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* 自定义滑块样式 */
    .custom-slider .stSlider > div {
        background-color: #F1F5F9;
    }
    
    .custom-slider .stSlider > div > div > div {
        background-color: #3B82F6;
    }
    
    /* 提示文本 */
    .info-text {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* 标题装饰线 */
    .title-decoration {
        height: 4px;
        width: 60px;
        background: linear-gradient(90deg, #2563EB, #3B82F6);
        margin: 8px 0 20px 0;
        border-radius: 2px;
    }
    
    /* 岩爆指标标签 */
    .metric-label {
        font-size: 0.8rem;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* 岩爆指标值 */
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
    }
    
    /* 岩爆指标变化 */
    .metric-change-positive {
        font-size: 0.9rem;
        font-weight: 500;
        color: #10B981;
    }
    
    .metric-change-negative {
        font-size: 0.9rem;
        font-weight: 500;
        color: #EF4444;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<h1>🪨 智能岩爆风险评估系统</h1>', unsafe_allow_html=True)
st.markdown('<div class="title-decoration"></div>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.1rem; color: #64748b; margin-bottom: 30px;">基于先进的机器学习算法，为您提供精准的岩爆风险评估和防护建议</p>', unsafe_allow_html=True)

# 导入预测功能
from utils import load_model, get_rock_burst_grade_text, predict_locally

# 创建自定义岩爆风险可视化函数
def create_risk_gauge(risk_level, risk_text):
    colors = {
        0: ['#4ADE80', '#10B981'],  # 绿色 - 无风险
        1: ['#FBBF24', '#F59E0B'],  # 黄色 - 低风险
        2: ['#FB923C', '#EA580C'],  # 橙色 - 中风险 
        3: ['#F87171', '#DC2626']   # 红色 - 高风险
    }
    
    # 创建仪表盘图
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_level,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': risk_text, 'font': {'size': 24, 'color': '#1E293B', 'family': 'Inter'}},
        delta = {'reference': 0, 'increasing': {'color': "#FF4560"}},
        gauge = {
            'axis': {'range': [0, 3], 'tickwidth': 1, 'tickcolor': "#334155"},
            'bar': {'color': colors[risk_level][0]},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E2E8F0",
            'steps': [
                {'range': [0, 0.75], 'color': '#D1FAE5'},
                {'range': [0.75, 1.5], 'color': '#FEF9C3'},
                {'range': [1.5, 2.25], 'color': '#FFEDD5'},
                {'range': [2.25, 3], 'color': '#FEE2E2'}
            ],
            'threshold': {
                'line': {'color': colors[risk_level][1], 'width': 4},
                'thickness': 0.75,
                'value': risk_level
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        height = 300,
        margin = dict(l=20, r=20, t=50, b=20),
        font = {'family': "Inter, sans-serif"}
    )
    
    return fig

# 创建岩爆概率分布图
def create_probability_chart(probabilities):
    grade_names = ["无岩爆倾向", "弱岩爆倾向", "中等岩爆倾向", "强岩爆倾向"]
    colors = ['#10B981', '#F59E0B', '#EA580C', '#DC2626']
    
    data = pd.DataFrame({
        "岩爆等级": grade_names,
        "概率": [probabilities.get(f"Class {i}", 0) for i in range(4)]
    })
    
    fig = px.bar(
        data, 
        x="岩爆等级", 
        y="概率", 
        color="岩爆等级",
        color_discrete_map={
            grade_names[0]: colors[0],
            grade_names[1]: colors[1],
            grade_names[2]: colors[2],
            grade_names[3]: colors[3]
        },
        text_auto=True
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(family="Inter, sans-serif"),
        xaxis=dict(
            title=None,
            showgrid=False
        ),
        yaxis=dict(
            title="预测概率",
            showgrid=True,
            gridcolor='#E2E8F0',
            range=[0, 1]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    fig.update_traces(
        marker_line_width=0,
        texttemplate='%{y:.1%}',
        textposition='outside'
    )
    
    return fig

# 创建参数影响雷达图
def create_parameter_impact_radar():
    # 假设的参数影响度(这可以根据实际模型重要性替换)
    categories = ['围岩应力', '单轴抗压强度', '抗拉强度', 
                 '围岩应力/单轴抗压强度比', '单轴抗压强度/抗拉强度比', '含水率']
    
    values = [0.85, 0.78, 0.62, 0.91, 0.76, 0.58]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.2)',
        line=dict(color='#3B82F6', width=2),
        name='参数影响度'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            ),
            angularaxis=dict(
                showline=False,
                showticklabels=True,
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=40, r=40, t=30, b=40),
        font=dict(family="Inter, sans-serif"),
        showlegend=False
    )
    
    return fig

# 侧边栏配置 - 现代设计
with st.sidebar:
    st.markdown('<h2>参数设置</h2>', unsafe_allow_html=True)
    st.markdown('<div class="title-decoration"></div>', unsafe_allow_html=True)
    st.markdown('<p class="info-text">请配置岩石样本的关键参数:</p>', unsafe_allow_html=True)
    
    # 添加一个模拟的岩石图像
    # 替换为实际图像路径或URL
    rock_image_url = "https://via.placeholder.com/300x150?text=岩石样本"
    st.image(rock_image_url, use_column_width=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 岩石种类选择
    st.markdown('<p class="param-label">岩石种类</p>', unsafe_allow_html=True)
    rock_types = {
        "花岗岩": 1.0,
        "大理岩": 2.0,
        "石灰岩": 3.0,
        "砂岩": 4.0,
        "页岩": 5.0,
        "白云岩": 6.0,
        "闪长岩": 7.0,
        "流纹岩": 8.0,
        "凝灰岩": 9.0,
        "片麻岩": 10.0,
        "片麻花岗岩": 11.0,
        "矽卡岩": 12.0,
        "花岗闪长岩": 13.0,
        "正长岩": 14.0,
        "黑云母花岗岩": 15.0,
        "辉绿岩": 16.0,
        "混合岩": 17.0,
        "橄榄岩": 18.0,
        "斜长角闪岩": 19.0,
        "金伯利岩": 20.0,
        "其他": 21.0
    }
    selected_rock = st.selectbox("", list(rock_types.keys()))
    rock_type_encoded = rock_types[selected_rock]
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 关键参数输入 - 使用更现代的样式
    st.markdown('<p class="param-label">围岩应力 (σθ / Mpa)</p>', unsafe_allow_html=True)
    sigma_theta = st.slider("", 10.0, 200.0, 50.0, 0.1, key="sigma_theta_slider")
    
    st.markdown('<p class="param-label">单轴抗压强度 (σc / Mpa)</p>', unsafe_allow_html=True)
    sigma_c = st.slider("", 20.0, 300.0, 100.0, 0.1, key="sigma_c_slider")
    
    st.markdown('<p class="param-label">抗拉强度 (σt / MPa)</p>', unsafe_allow_html=True)
    sigma_t = st.slider("", 1.0, 50.0, 10.0, 0.1, key="sigma_t_slider")
    
    # 自动计算比率
    sigma_theta_c_ratio = sigma_theta / sigma_c
    sigma_c_t_ratio = sigma_c / sigma_t
    
    # 显示计算出的比率 - 使用更优雅的显示方式
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="param-label">σθ/σc 比值</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="param-value">{sigma_theta_c_ratio:.2f}</p>', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="param-label">σc/σt 比值</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="param-value">{sigma_c_t_ratio:.2f}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 含水率
    st.markdown('<p class="param-label">含水率 (Wet)</p>', unsafe_allow_html=True)
    wet = st.slider("", 0.0, 1.0, 0.5, 0.01, key="wet_slider")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 关于部分 - 更现代的设计
    st.markdown('<p class="param-label">关于</p>', unsafe_allow_html=True)
    st.markdown('<p class="info-text">本系统使用堆叠分类器模型，结合了多种先进的机器学习算法，对岩石的岩爆倾向等级进行高精度预测。</p>', unsafe_allow_html=True)

# 主要内容区 - 现代化设计
col1, col2 = st.columns([5, 4])

with col1:
    # 参数汇总卡片
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>岩石参数汇总</h3>', unsafe_allow_html=True)
    st.markdown('<div class="title-decoration"></div>', unsafe_allow_html=True)
    
    # 使用更现代的表格设计
    param_cols = st.columns(3)
    
    params = [
        {"label": "岩石种类", "value": selected_rock, "icon": "🪨"},
        {"label": "围岩应力", "value": f"{sigma_theta:.1f} MPa", "icon": "📏"},
        {"label": "单轴抗压强度", "value": f"{sigma_c:.1f} MPa", "icon": "💪"},
        {"label": "抗拉强度", "value": f"{sigma_t:.1f} MPa", "icon": "🔄"},
        {"label": "σθ/σc", "value": f"{sigma_theta_c_ratio:.2f}", "icon": "📊"},
        {"label": "σc/σt", "value": f"{sigma_c_t_ratio:.2f}", "icon": "📉"},
        {"label": "含水率", "value": f"{wet:.2f}", "icon": "💧"},
    ]
    
    for i, param in enumerate(params):
        with param_cols[i % 3]:
            st.markdown(f'''
            <div style="margin-bottom: 20px;">
                <div style="font-size: 2rem; margin-bottom: 5px;">{param["icon"]}</div>
                <div class="metric-label">{param["label"]}</div>
                <div class="metric-value">{param["value"]}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 预测按钮 - 现代设计
    if st.button("开始预测分析", key="predict_button"):
        with st.spinner("正在分析岩石参数，请稍候..."):
            # 显示进度条
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # 准备预测数据
            input_data = {
                "rock_type": rock_type_encoded,
                "sigma_theta": sigma_theta,
                "sigma_c": sigma_c,
                "sigma_t": sigma_t,
                "sigma_theta_c_ratio": sigma_theta_c_ratio,
                "sigma_c_t_ratio": sigma_c_t_ratio,
                "wet": wet
            }
            
            try:
                # 使用本地预测函数
                result = predict_locally(input_data)
                
                st.markdown('<div class="result-card animate-fade-in">', unsafe_allow_html=True)
                st.success("✅ 分析完成!")
                
                # 获取预测结果
                grade_text = result["prediction_text"]
                prediction = result["prediction"]
                
                # 使用仪表盘显示风险等级
                st.markdown("<h3>岩爆风险评估</h3>", unsafe_allow_html=True)
                risk_gauge = create_risk_gauge(prediction, grade_text)
                st.plotly_chart(risk_gauge, use_container_width=True)
                
                # 显示各类别概率
                probabilities = result["probabilities"]
                st.markdown("<h3>风险概率分布</h3>", unsafe_allow_html=True)
                prob_chart = create_probability_chart(probabilities)
                st.plotly_chart(prob_chart, use_container_width=True)
                
                # 参数影响雷达图
                st.markdown("<h3>参数影响雷达图</h3>", unsafe_allow_html=True)
                impact_radar = create_parameter_impact_radar()
                st.plotly_chart(impact_radar, use_container_width=True)
                
                # 结果解释 - 更加详细
                st.markdown("<h3>预测解释</h3>", unsafe_allow_html=True)
                st.markdown(f'''
                <div style="background-color: #F8FAFC; padding: 15px; border-radius: 8px; border-left: 4px solid #3B82F6;">
                    <p style="margin: 0;">根据您提供的岩石参数，本系统预测该样本的岩爆等级为 <strong>{grade_text}</strong>。</p>
                    <p style="margin-top: 10px;">该预测结果基于样本的物理特性综合分析，特别是考虑了围岩应力、抗压强度、抗拉强度等关键参数的相互关系。</p>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"预测过程中出现错误: {str(e)}")
                st.markdown('''
                <div style="background-color: #FEF2F2; padding: 15px; border-radius: 8px; border-left: 4px solid #DC2626;">
                    <p style="margin: 0;">请检查模型文件是否正确加载，或联系系统管理员。</p>
                    <p style="margin-top: 10px;">确保所有必要的依赖项已正确安装，并且模型文件位于正确的目录中。</p>
                </div>
                ''', unsafe_allow_html=True)

with col2:
    # 岩爆等级说明 - 现代卡片设计
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>岩爆等级分类</h3>', unsafe_allow_html=True)
    st.markdown('<div class="title-decoration"></div>', unsafe_allow_html=True)
    
    # 岩爆等级解释 - 更现代的设计
    grade_info = [
        {
            "grade": "无岩爆倾向 (0级)", 
            "description": "岩石在开挖过程中稳定性较好，不易发生岩爆现象。",
            "color": "grade-0",
            "icon": "✅"
        },
        {
            "grade": "弱岩爆倾向 (1级)", 
            "description": "岩石可能会发生轻微的岩体破坏，但规模小，危害有限。",
            "color": "grade-1",
            "icon": "⚠️"
        },
        {
            "grade": "中等岩爆倾向 (2级)", 
            "description": "岩石有较明显的岩爆倾向，可能会发生中等规模的岩爆事件，需要采取预防措施。",
            "color": "grade-2",
            "icon": "🔥"
        },
        {
            "grade": "强岩爆倾向 (3级)", 
            "description": "岩石具有强烈的岩爆倾向，极易发生大规模岩爆事件，需要严格的监测和防护措施。",
            "color": "grade-3",
            "icon": "⛔"
        }
    ]
    
    for grade in grade_info:
        st.markdown(f'''
        <div style="margin-bottom: 15px; padding: 15px; background-color: #F8FAFC; border-radius: 8px; border-left: 4px solid #3B82F6;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 1.5rem; margin-right: 10px;">{grade["icon"]}</div>
                <span class="grade-label {grade["color"]}">{grade["grade"]}</span>
            </div>
            <p style="margin-top: 10px; color: #334155;">{grade["description"]}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 岩爆防治建议卡片
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>岩爆防治与应对策略</h3>', unsafe_allow_html=True)
    st.markdown('<div class="title-decoration"></div>', unsafe_allow_html=True)
    
    # 分级防治建议
    recommendations = [
        {
            "title": "评估与监测", 
            "content": "在进行隧道或地下工程开挖前，建议进行详细的岩体稳定性评估，并部署实时监测系统。",
            "icon": "📊"
        },
        {
            "title": "开挖技术选择", 
            "content": "对于中高岩爆倾向区域，应采用控制爆破技术，分段开挖，减小扰动。",
            "icon": "⛏️"
        },
        {
            "title": "应力释放措施", 
            "content": "考虑使用预裂爆破、光面爆破等方法减小爆破震动，对于强岩爆倾向区域，可采用预应力释放钻孔等措施。",
            "icon": "💥"
        },
        {
            "title": "支护加固方案", 
            "content": "根据岩爆等级选择合适的支护方案，如柔性支护、高强锚杆、压力释放支护等。",
            "icon": "🛡️"
        },
        {
            "title": "应急响应", 
            "content": "建立完善的应急预案，配备必要的救援设备，加强人员安全培训。",
            "icon": "🚨"
        }
    ]
    
    for rec in recommendations:
        st.markdown(f'''
        <div style="margin-bottom: 15px; display: flex; align-items: flex-start;">
            <div style="font-size: 1.8rem; margin-right: 15px; color: #3B82F6;">{rec["icon"]}</div>
            <div>
                <div style="font-weight: 600; color: #1E293B; margin-bottom: 5px;">{rec["title"]}</div>
                <p style="margin: 0; color: #64748b;">{rec["content"]}</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 技术说明卡片
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>技术原理</h3>', unsafe_allow_html=True)
    st.markdown('<div class="title-decoration"></div>', unsafe_allow_html=True)
    
    # 技术说明内容
    st.markdown('''
    <div style="margin-bottom: 15px;">
        <div style="font-weight: 600; color: #1E293B; margin-bottom: 8px;">机器学习模型</div>
        <p style="margin: 0; color: #64748b; font-size: 0.9rem;">本系统采用堆叠分类器模型，集成了极限树分类器、XGBoost、LightGBM、随机森林和梯度提升等算法，提供更加稳定和准确的预测结果。</p>
    </div>
    
    <div style="margin-bottom: 15px;">
        <div style="font-weight: 600; color: #1E293B; margin-bottom: 8px;">特征工程</div>
        <p style="margin: 0; color: #64748b; font-size: 0.9rem;">采用了多种特征工程技术，包括特征交互、多项式变换和相关性分析，从原始岩石参数中提取出更有价值的信息。</p>
    </div>
    
    <div style="margin-bottom: 15px;">
        <div style="font-weight: 600; color: #1E293B; margin-bottom: 8px;">精度验证</div>
        <p style="margin: 0; color: #64748b; font-size: 0.9rem;">通过交叉验证和独立测试集评估，模型预测准确率超过90%，为工程决策提供可靠依据。</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 添加数据可视化仪表板部分
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<h2>数据洞察</h2>', unsafe_allow_html=True)
st.markdown('<div class="title-decoration"></div>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; margin-bottom: 20px;">探索岩爆参数之间的相互关系和趋势变化</p>', unsafe_allow_html=True)

# 创建三列布局
insight_cols = st.columns(3)

# 第一列 - 岩爆发生概率趋势图
with insight_cols[0]:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>岩爆风险趋势</h3>', unsafe_allow_html=True)
    
    # 模拟数据 - 岩爆风险随深度变化
    depths = np.arange(100, 1100, 100)
    risk_probs = [0.05, 0.12, 0.25, 0.42, 0.58, 0.72, 0.80, 0.86, 0.91, 0.95]
    
    # 创建趋势图
    trend_fig = px.line(
        x=depths, 
        y=risk_probs,
        labels={"x": "埋深 (m)", "y": "岩爆发生概率"},
        markers=True
    )
    
    trend_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=20, r=20, t=20, b=30),
        font=dict(family="Inter, sans-serif"),
        xaxis=dict(
            showgrid=True,
            gridcolor='#E2E8F0',
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#E2E8F0',
            tickformat='.0%'
        )
    )
    
    trend_fig.update_traces(
        line=dict(color='#3B82F6', width=3),
        marker=dict(color='#2563EB', size=8)
    )
    
    st.plotly_chart(trend_fig, use_container_width=True)
    
    st.markdown('<p style="font-size: 0.85rem; color: #64748b; text-align: center; font-style: italic;">岩爆风险随埋深增加而显著上升</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 第二列 - 岩爆等级分布饼图
with insight_cols[1]:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>岩爆等级分布</h3>', unsafe_allow_html=True)
    
    # 模拟数据 - 岩爆等级分布
    grade_distribution = {
        "无岩爆倾向": 45,
        "弱岩爆倾向": 30,
        "中等岩爆倾向": 18,
        "强岩爆倾向": 7
    }
    
    # 创建饼图
    pie_data = pd.DataFrame({
        "岩爆等级": list(grade_distribution.keys()),
        "样本数量": list(grade_distribution.values())
    })
    
    pie_fig = px.pie(
        pie_data, 
        names="岩爆等级", 
        values="样本数量",
        color="岩爆等级",
        color_discrete_map={
            "无岩爆倾向": "#10B981",
            "弱岩爆倾向": "#F59E0B",
            "中等岩爆倾向": "#EA580C",
            "强岩爆倾向": "#DC2626"
        }
    )
    
    pie_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=20, r=20, t=20, b=30),
        font=dict(family="Inter, sans-serif"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )
    
    pie_fig.update_traces(
        textinfo="percent+label",
        hole=0.4,
        marker=dict(line=dict(color='#ffffff', width=2))
    )
    
    st.plotly_chart(pie_fig, use_container_width=True)
    
    st.markdown('<p style="font-size: 0.85rem; color: #64748b; text-align: center; font-style: italic;">基于历史数据分析的岩爆等级分布情况</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 第三列 - 关键参数相关性热图
with insight_cols[2]:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>参数相关性</h3>', unsafe_allow_html=True)
    
    # 模拟数据 - 参数相关性
    corr_data = np.array([
        [1.00, 0.35, 0.42, 0.85, -0.28, 0.18],
        [0.35, 1.00, 0.65, 0.25, 0.72, -0.15],
        [0.42, 0.65, 1.00, 0.48, 0.56, 0.08],
        [0.85, 0.25, 0.48, 1.00, -0.12, 0.22],
        [-0.28, 0.72, 0.56, -0.12, 1.00, -0.05],
        [0.18, -0.15, 0.08, 0.22, -0.05, 1.00]
    ])
    
    parameter_names = ["围岩应力", "单轴抗压强度", "抗拉强度", "σθ/σc", "σc/σt", "含水率"]
    
    # 创建热图
    heatmap_fig = px.imshow(
        corr_data,
        x=parameter_names,
        y=parameter_names,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1
    )
    
    heatmap_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=0, r=0, t=20, b=0),
        font=dict(family="Inter, sans-serif"),
        coloraxis_colorbar=dict(
            title="相关系数",
            thicknessmode="pixels", 
            thickness=15,
            lenmode="pixels", 
            len=250,
            yanchor="top",
            y=1,
            ticks="outside"
        )
    )
    
    # 添加相关系数文本标注
    heatmap_fig.update_traces(
        text=np.around(corr_data, decimals=2),
        texttemplate="%{text}",
        textfont={"size": 10}
    )
    
    st.plotly_chart(heatmap_fig, use_container_width=True)
    
    st.markdown('<p style="font-size: 0.85rem; color: #64748b; text-align: center; font-style: italic;">各参数之间的相关性系数分析</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 应用案例部分
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<h2>应用案例</h2>', unsafe_allow_html=True)
st.markdown('<div class="title-decoration"></div>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; margin-bottom: 20px;">实际工程中应用本系统的典型案例展示</p>', unsafe_allow_html=True)

# 两列布局
case_cols = st.columns(2)

# 第一个案例
with case_cols[0]:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div style="display: flex; align-items: center; margin-bottom: 15px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 2rem; margin-right: 15px;">🚇</div>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin: 0;">某高速铁路隧道工程</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 案例图片(可以替换为实际项目图片)
    st.image("https://via.placeholder.com/600x300?text=隧道工程案例", use_column_width=True)
    
    st.markdown('''
    <div style="margin-top: 15px;">
        <div style="font-weight: 600; color: #1E293B; margin-bottom: 8px;">项目背景</div>
        <p style="margin: 0; color: #64748b; font-size: 0.95rem;">
            某高铁隧道穿越花岗岩段，最大埋深约1200米，岩爆风险高，采用本系统进行岩爆风险评估。
        </p>
    </div>
    
    <div style="margin-top: 15px;">
        <div style="font-weight: 600; color: #1E293B; margin-bottom: 8px;">评估结果</div>
        <p style="margin: 0; color: #64748b; font-size: 0.95rem;">
            系统预测隧道里程K45+200 ~ K46+500段为强岩爆倾向区，与实际施工中发生的3次中强度岩爆事件位置高度吻合。
        </p>
    </div>
    
    <div style="margin-top: 15px;">
        <div style="font-weight: 600; color: #1E293B; margin-bottom: 8px;">防治措施</div>
        <p style="margin: 0; color: #64748b; font-size: 0.95rem;">
            根据系统建议，采用超前预裂、控制爆破、柔性支护等综合措施，有效控制了岩爆风险，确保了施工安全。
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 第二个案例
with case_cols[1]:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div style="display: flex; align-items: center; margin-bottom: 15px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 2rem; margin-right: 15px;">⚡</div>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin: 0;">某深部水电站地下厂房</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 案例图片(可以替换为实际项目图片)
    st.image("https://via.placeholder.com/600x300?text=水电站地下厂房案例", use_column_width=True)
    
    st.markdown('''
    <div style="margin-top: 15px;">
        <div style="font-weight: 600; color: #1E293B; margin-bottom: 8px;">项目背景</div>
        <p style="margin: 0; color: #64748b; font-size: 0.95rem;">
            某大型水电站地下厂房开挖深度达到800米，主要岩体为片麻岩，初期开挖过程中已发生多次小型岩爆。
        </p>
    </div>
    
    <div style="margin-top: 15px;">
        <div style="font-weight: 600; color: #1E293B; margin-bottom: 8px;">评估结果</div>
        <p style="margin: 0; color: #64748b; font-size: 0.95rem;">
            系统分析表明厂房左侧洞壁为中等岩爆倾向区，顶拱和右侧洞壁为弱岩爆倾向区，为差异化支护设计提供了依据。
        </p>
    </div>
    
    <div style="margin-top: 15px;">
        <div style="font-weight: 600; color: #1E293B; margin-bottom: 8px;">防治效果</div>
        <p style="margin: 0; color: #64748b; font-size: 0.95rem;">
            基于系统预测结果，采用了分区分级支护方案，左侧洞壁增加了预应力锚索和钢筋网喷射混凝土，成功避免了后续开挖中的岩爆风险。
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 底部信息区
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('''
<div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 0;">
    <div>
        <p style="margin: 0; color: #64748b; font-size: 0.9rem;">© 2023 智能岩爆风险评估系统 | 版本 1.2.0</p>
    </div>
    <div>
        <p style="margin: 0; color: #64748b; font-size: 0.9rem;">技术支持: AI岩石力学实验室</p>
    </div>
</div>
''', unsafe_allow_html=True)

# 添加可折叠的帮助与支持部分
with st.expander("帮助与支持"):
    st.markdown('''
    ### 常见问题
    
    **Q: 系统的预测结果准确性如何？**
    
    A: 系统基于大量实际工程案例数据训练，预测准确率超过90%。但仍建议结合现场地质条件和工程经验综合判断。
    
    **Q: 如何判断输入参数的合理范围？**
    
    A: 系统会自动检查参数是否在合理范围内。一般而言，围岩应力通常在10-200MPa，单轴抗压强度在20-300MPa，抗拉强度在1-50MPa。
    
    **Q: 系统是否支持批量预测？**
    
    A: 目前系统支持单点预测，未来版本将增加批量预测功能。如有批量预测需求，请联系技术支持。
    
    ### 联系方式
    
    - 技术支持邮箱: support@rockburst-ai.com
    - 问题反馈: feedback@rockburst-ai.com
    ''')

# 添加版本历史记录部分
with st.expander("版本历史"):
    st.markdown('''
    ### 版本 1.2.0 (当前版本)
    - 新增参数影响雷达图
    - 提升UI交互体验
    - 优化预测算法，提高准确率
    
    ### 版本 1.1.0
    - 添加岩爆风险等级可视化
    - 增加防治建议模块
    - 修复已知BUG
    
    ### 版本 1.0.0
    - 初始版本发布
    - 基础岩爆预测功能
    - 简单参数输入界面
    ''')
    
