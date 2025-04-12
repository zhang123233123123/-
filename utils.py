import numpy as np
import pandas as pd
import joblib
import streamlit as st
import os

# 缓存加载模型
@st.cache_resource
def load_model():
    try:
        # 固定使用best_stacking_classifier.pkl
        model_file = 'best_stacking_classifier.pkl'
        
        # 加载模型
        if os.path.exists(model_file):
            return joblib.load(model_file)
        else:
            raise FileNotFoundError(f"找不到模型文件: {model_file}")
    except Exception as e:
        st.warning(f"无法加载模型: {e}")
        raise e  # 重新抛出异常，不使用备用模型

# 修改特征工程函数以匹配训练时的特征工程
def feature_engineering(X):
    """特征工程 - 必须与训练模型时使用的完全相同"""
    # 保存原始特征的副本
    X_engineered = X.copy()
    
    # 确保列名正确
    expected_columns = ['岩石种类', 'σθ / Mpa', 'σc / Mpa', 'σt / MPa', 'σθ/σc', 'σc/σt', 'Wet']
    if not all(col in X_engineered.columns for col in expected_columns):
        raise ValueError(f"输入数据缺少必要的列，期望的列: {expected_columns}，实际的列: {list(X_engineered.columns)}")
    
    # 1. 创建交互特征
    numeric_cols = X_engineered.select_dtypes(include=[np.number]).columns
    
    # 确保按照固定的顺序处理列，以保证特征名称的一致性
    numeric_cols = sorted(numeric_cols)
    
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            X_engineered[f'{col1}_{col2}_ratio'] = X_engineered[col1] / (X_engineered[col2] + 1e-8)  # 防止除零
            X_engineered[f'{col1}_{col2}_product'] = X_engineered[col1] * X_engineered[col2]
            X_engineered[f'{col1}_{col2}_sum'] = X_engineered[col1] + X_engineered[col2]
    
    # 2. 创建多项式特征
    for col in numeric_cols:
        X_engineered[f'{col}_squared'] = X_engineered[col] ** 2
        X_engineered[f'{col}_cubed'] = X_engineered[col] ** 3
        X_engineered[f'{col}_sqrt'] = np.sqrt(np.abs(X_engineered[col]))
        X_engineered[f'{col}_log'] = np.log1p(np.abs(X_engineered[col]))
    
    # 输出转换后的特征数
    print(f"特征工程后的特征数: {X_engineered.shape[1]}")
    return X_engineered

# 获取岩爆等级文本描述
def get_rock_burst_grade_text(grade):
    grades = {
        0: "无岩爆倾向",
        1: "弱岩爆倾向",
        2: "中等岩爆倾向",
        3: "强岩爆倾向"
    }
    return grades.get(grade, "未知等级")

# 创建自定义岩爆风险可视化函数
def create_risk_gauge(risk_level, risk_text):
    import plotly.graph_objects as go
    
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
    import plotly.express as px
    
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
    import plotly.graph_objects as go
    
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

# 修改预测函数
def predict_locally(input_data):
    """使用本地模型进行预测"""
    try:
        # 加载模型 - 如果失败会直接抛出异常
        model = load_model()
        
        # 创建DataFrame，确保列名正确
        input_df = pd.DataFrame([input_data])
        
        # 列名映射
        column_mapping = {
            'rock_type': '岩石种类',
            'sigma_theta': 'σθ / Mpa',
            'sigma_c': 'σc / Mpa',
            'sigma_t': 'σt / MPa',
            'sigma_theta_c_ratio': 'σθ/σc',
            'sigma_c_t_ratio': 'σc/σt',
            'wet': 'Wet'
        }
        
        # 重命名列
        input_df = input_df.rename(columns=column_mapping)
        
        # 应用与训练时完全相同的特征工程
        input_df_engineered = feature_engineering(input_df)
        
        # 检查模型所需的特征
        model_features = None
        # 尝试获取模型所需的特征名称
        if hasattr(model, 'feature_names_in_'):
            model_features = model.feature_names_in_
        
        # 如果能获取到模型特征，则确保输入数据包含所有这些特征
        if model_features is not None:
            missing_features = set(model_features) - set(input_df_engineered.columns)
            extra_features = set(input_df_engineered.columns) - set(model_features)
            
            if missing_features:
                print(f"缺少模型所需的特征: {missing_features}")
                
            # 仅保留模型所需的特征，按正确顺序
            input_df_final = pd.DataFrame(index=input_df_engineered.index)
            for feature in model_features:
                if feature in input_df_engineered.columns:
                    input_df_final[feature] = input_df_engineered[feature]
                else:
                    # 对于缺失的特征，填充0
                    input_df_final[feature] = 0
            
            input_df_engineered = input_df_final
        
        # 使用模型进行预测
        prediction = model.predict(input_df_engineered)[0]
        probabilities = model.predict_proba(input_df_engineered)[0]
        
        # 构建结果
        result = {
            "prediction": int(prediction),
            "prediction_text": get_rock_burst_grade_text(prediction),
            "probabilities": {f"Class {i}": float(prob) for i, prob in enumerate(probabilities)}
        }
        
        return result
        
    except Exception as e:
        print(f"预测过程中出现错误: {str(e)}")
        # 在这里我们不提供备用模型，而是直接向用户展示错误
        raise e
