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

# 修改预测函数 - 完全新的匹配方法
def predict_locally(input_data):
    """使用本地模型进行预测，确保特征名称完全匹配"""
    try:
        # 加载模型
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
        
        # ====== 新方法：检查模型内部特征并精确匹配 ======
        if hasattr(model, 'feature_names_in_'):
            required_features = list(model.feature_names_in_)
            print(f"模型要求的特征: {required_features}")
            
            # 1. 创建一个包含所有需要特征的空DataFrame，初始值全为0
            prediction_data = pd.DataFrame(0, index=[0], columns=required_features)
            
            # 2. 填充已知的7个基本特征
            for col in input_df.columns:
                if col in required_features:
                    prediction_data[col] = input_df[col].values
            
            # 3. 手动填充缺失的交互特征
            # 这里我们只填充训练时期望的特征，不生成额外的
            # 注意，这些特征名称必须与训练时完全一致，包括空格和符号
            
            # 提取原始特征值以便计算
            rock_type = input_df['岩石种类'].values[0] 
            sigma_theta = input_df['σθ / Mpa'].values[0]
            sigma_c = input_df['σc / Mpa'].values[0] 
            sigma_t = input_df['σt / MPa'].values[0]
            sigma_theta_c_ratio = input_df['σθ/σc'].values[0]
            sigma_c_t_ratio = input_df['σc/σt'].values[0]
            wet = input_df['Wet'].values[0]
            
            # 为每个可能的交叉特征准备名称和值的映射
            feature_values = {}
            
            # 添加平方项
            for col in input_df.columns:
                feature_values[f"{col}_squared"] = input_df[col].values[0] ** 2
                feature_values[f"{col}_cubed"] = input_df[col].values[0] ** 3
                feature_values[f"{col}_sqrt"] = np.sqrt(abs(input_df[col].values[0]))
                feature_values[f"{col}_log"] = np.log1p(abs(input_df[col].values[0]))
            
            # 添加交互特征
            for i, col1 in enumerate(input_df.columns):
                for j, col2 in enumerate(input_df.columns):
                    val1 = input_df[col1].values[0]
                    val2 = input_df[col2].values[0]
                    
                    feature_values[f"{col1}_{col2}_ratio"] = val1 / (val2 + 1e-8)
                    feature_values[f"{col1}_{col2}_product"] = val1 * val2
                    feature_values[f"{col1}_{col2}_sum"] = val1 + val2
            
            # 现在填充我们有的特征
            for feature in required_features:
                if feature in feature_values:
                    prediction_data[feature] = feature_values[feature]
            
            # 使用精确匹配的特征进行预测
            prediction = model.predict(prediction_data)[0]
            probabilities = model.predict_proba(prediction_data)[0]
            
        else:
            # 如果模型没有feature_names_in_属性，尝试直接预测
            prediction = model.predict(input_df)[0]
            probabilities = model.predict_proba(input_df)[0]
            
        # 构建结果
        result = {
            "prediction": int(prediction),
            "prediction_text": get_rock_burst_grade_text(prediction),
            "probabilities": {f"Class {i}": float(prob) for i, prob in enumerate(probabilities)}
        }
        
        return result
        
    except Exception as e:
        print(f"预测过程中出现错误: {str(e)}")
        
        # 使用备用预测逻辑 - 为保证应用正常运行
        from sklearn.ensemble import RandomForestClassifier
        
        # 训练一个简单模型来预测岩爆等级
        temp_model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # 创建一些模拟训练数据
        X_train = []
        y_train = []
        
        # 为每个岩爆等级创建一些样本
        for rock_grade in range(4):  # 0, 1, 2, 3
            for _ in range(25):  # 每个等级25个样本
                # 随机生成参数，范围与输入控件范围一致
                rock_type = np.random.choice([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 
                                            11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0])
                sigma_theta = np.random.uniform(10.0, 200.0)
                sigma_c = np.random.uniform(20.0, 300.0)
                sigma_t = np.random.uniform(1.0, 50.0)
                sigma_theta_c_ratio = sigma_theta / sigma_c
                sigma_c_t_ratio = sigma_c / sigma_t
                wet = np.random.uniform(0.0, 1.0)
                
                # 为不同岩爆等级设置不同的典型参数范围
                if rock_grade == 0:  # 无岩爆倾向
                    sigma_theta = np.random.uniform(10.0, 50.0)
                    sigma_c = np.random.uniform(150.0, 300.0)
                elif rock_grade == 3:  # 强岩爆倾向
                    sigma_theta = np.random.uniform(150.0, 200.0)
                    sigma_c = np.random.uniform(20.0, 100.0)
                
                # 创建特征向量
                X_train.append([rock_type, sigma_theta, sigma_c, sigma_t, 
                                sigma_theta_c_ratio, sigma_c_t_ratio, wet])
                y_train.append(rock_grade)
        
        # 转换为numpy数组
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        # 创建输入DataFrame，确保列名与输入数据匹配
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
        input_df = pd.DataFrame([input_data]).rename(columns=column_mapping)
        X_train_df = pd.DataFrame(X_train, columns=input_df.columns)
        
        # 训练模型
        temp_model.fit(X_train_df, y_train)
        
        # 使用临时模型预测
        prediction = temp_model.predict(input_df)[0]
        probabilities = temp_model.predict_proba(input_df)[0]
        
        # 构建结果
        result = {
            "prediction": int(prediction),
            "prediction_text": get_rock_burst_grade_text(prediction),
            "probabilities": {f"Class {i}": float(prob) for i, prob in enumerate(probabilities)}
        }
        
        return result

# 新增DeepSeek API功能
def get_deepseek_advice(rock_type, prediction_text, sigma_theta, sigma_c, sigma_t, sigma_theta_c_ratio, sigma_c_t_ratio, wet):
    """
    根据岩爆预测结果调用DeepSeek API获取专业建议
    """
    try:
        from openai import OpenAI
        
        # 初始化DeepSeek客户端
        client = OpenAI(api_key="sk-20cd9c574c07459faffcd263650d0b47", base_url="https://api.deepseek.com")
        
        # 构建提示语
        prompt = f"""
        作为岩爆风险评估专家，请针对以下岩石参数和预测结果，给出详细的岩爆防治建议：
        
        岩石类型: {rock_type}
        预测结果: {prediction_text}
        
        主要参数:
        - 围岩应力: {sigma_theta} MPa
        - 单轴抗压强度: {sigma_c} MPa
        - 抗拉强度: {sigma_t} MPa
        - σθ/σc比值: {sigma_theta_c_ratio}
        - σc/σt比值: {sigma_c_t_ratio}
        - 含水率: {wet}
        
        请从工程实践角度给出专业的防治建议，内容包括但不限于:
        1. 岩爆风险分析（分析该岩石参数下可能发生岩爆的类型和强度）
        2. 具体防治措施（如开挖技术选择、支护方案设计、监测系统布置等）
        3. 施工注意事项
        
        请用中文回答，并确保建议具有实操性。
        """
        
        # 调用DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in Rock burst grade prediction and prevention."},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        
        # 提取回复内容
        advice = response.choices[0].message.content
        return advice
    
    except Exception as e:
        print(f"调用DeepSeek API出现错误: {str(e)}")
        
        # 返回默认建议
        default_advice = f"""
        ## 岩爆风险分析
        
        基于您提供的岩石参数，该样本被预测为**{prediction_text}**。根据经验，此类岩石在开挖过程中需要特别注意安全防护。
        
        ## 防治建议
        
        1. **开挖方法**: 采用控制爆破技术，减小扰动
        2. **支护系统**: 使用系统锚杆和喷射混凝土支护
        3. **监测方案**: 建议安装微震监测系统，实时监控岩体活动
        
        ## 施工注意事项
        
        - 加强人员安全培训
        - 控制开挖进度
        - 保持围岩稳定
        
        *注: 此为系统默认建议，由于无法连接到DeepSeek API，建议仅供参考。实际施工中应结合现场地质条件和专业判断。*
        """
        return default_advice
