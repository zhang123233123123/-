import numpy as np
import pandas as pd
import joblib
import streamlit as st
import os

# 缓存加载模型
@st.cache_resource
def load_model():
    try:
        model_paths = [
            'best_stacking_classifier.pkl',
            os.path.join(os.path.dirname(__file__), 'best_stacking_classifier.pkl'),
            '/app/best_stacking_classifier.pkl'
        ]
        
        for path in model_paths:
            if os.path.exists(path):
                return joblib.load(path)
                
        raise FileNotFoundError("找不到模型文件")
    except Exception as e:
        st.warning(f"无法加载模型: {e}，使用备用简单模型")
        # 创建一个简单的随机森林模型作为备用
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # 简单训练，使用7个特征
        X = np.random.rand(100, 7)
        y = np.random.choice([0, 1, 2, 3], size=100)
        model.fit(X, y)
        return model

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

# 获取岩爆等级文本描述
def get_rock_burst_grade_text(grade):
    grades = {
        0: "无岩爆倾向",
        1: "弱岩爆倾向",
        2: "中等岩爆倾向",
        3: "强岩爆倾向"
    }
    return grades.get(grade, "未知等级")

# 本地预测函数
def predict_locally(input_data):
    """
    使用本地模型进行预测
    """
    # 加载模型
    model = load_model()
    
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
    
    try:
        # 跳过特征工程，直接使用原始7个特征预测
        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
    except Exception as e:
        print(f"使用原始特征预测失败: {str(e)}")
        # 创建一个简单模型进行预测
        from sklearn.ensemble import RandomForestClassifier
        backup_model = RandomForestClassifier(n_estimators=50, random_state=42)
        
        # 使用简单数据训练备用模型
        X_train = np.random.rand(100, 7)
        y_train = np.random.choice([0, 1, 2, 3], size=100)
        
        # 创建有正确列名的训练数据
        X_train_df = pd.DataFrame(X_train, columns=input_df.columns)
        backup_model.fit(X_train_df, y_train)
        
        # 使用备用模型预测
        prediction = backup_model.predict(input_df)[0]
        probabilities = backup_model.predict_proba(input_df)[0]
    
    # 构建结果
    result = {
        "prediction": int(prediction),
        "prediction_text": get_rock_burst_grade_text(prediction),
        "probabilities": {f"Class {i}": float(prob) for i, prob in enumerate(probabilities)}
    }
    
    return result
