import numpy as np
import pandas as pd
import joblib
import streamlit as st

# 缓存加载模型
@st.cache_resource
def load_model():
    try:
        return joblib.load('best_stacking_classifier.pkl')
    except Exception as e:
        st.error(f"无法加载模型: {e}")
        return None

# 获取岩爆等级文本描述
def get_rock_burst_grade_text(grade):
    grades = {
        0: "无岩爆倾向",
        1: "弱岩爆倾向",
        2: "中等岩爆倾向",
        3: "强岩爆倾向"
    }
    return grades.get(grade, "未知等级")

# 特征工程函数
def feature_engineering(X):
    """
    增强特征工程
    """
    # 保存原始特征
    X_new = X.copy()

    # 创建更多的交互特征
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            X_new[f'{col1}_{col2}_ratio'] = X[col1] / (X[col2] + 1e-8)
            X_new[f'{col1}_{col2}_product'] = X[col1] * X[col2]
            X_new[f'{col1}_{col2}_sum'] = X[col1] + X[col2]

    # 添加多项式特征
    for col in numeric_cols:
        X_new[f'{col}_squared'] = X[col] ** 2
        X_new[f'{col}_cubed'] = X[col] ** 3
        X_new[f'{col}_sqrt'] = np.sqrt(np.abs(X[col]))
        X_new[f'{col}_log'] = np.log1p(np.abs(X[col]))

    return X_new

# 本地预测函数
def predict_locally(input_data):
    """
    使用本地模型进行预测
    """
    # 加载模型
    model = load_model()
    if model is None:
        raise Exception("模型加载失败")
    
    # 创建DataFrame
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
    
    # 应用特征工程
    input_df = feature_engineering(input_df)
    
    # 预测
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    
    # 构建结果
    result = {
        "prediction": int(prediction),
        "prediction_text": get_rock_burst_grade_text(prediction),
        "probabilities": {f"Class {i}": float(prob) for i, prob in enumerate(probabilities)}
    }
    
    return result
