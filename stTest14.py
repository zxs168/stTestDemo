import streamlit as st
import pandas as pd

# 缓存数据加载函数，避免重复读取文件
@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    return data

# 初始化 session_state 中的筛选条件
if "filter_column" not in st.session_state:
    st.session_state["filter_column"] = None
if "filter_value" not in st.session_state:
    st.session_state["filter_value"] = None

# 页面标题
st.title("缓存与状态管理示例")

# 文件上传组件
uploaded_file = st.file_uploader("上传一个 CSV 文件", type=["csv"])

# 检查文件是否已上传
if uploaded_file:
    # 加载并缓存数据
    data = load_data(uploaded_file)
    st.write("数据加载成功！")
    st.write(data.head())  # 显示前几行数据

    # 选择列进行筛选
    filter_column = st.selectbox("选择一个列进行筛选", data.columns, index=0)
    filter_value = st.text_input("输入筛选值", value="")

    # 更新 session_state 中的筛选条件
    st.session_state["filter_column"] = filter_column
    st.session_state["filter_value"] = filter_value

    # 筛选数据
    if filter_value:
        filtered_data = data[data[filter_column].astype(str) == filter_value]
        st.write(f"筛选后的数据 (列: {filter_column}, 值: {filter_value})：")
        st.write(filtered_data)
    else:
        st.write("未应用筛选条件")

    # 重置筛选条件按钮
    if st.button("重置筛选条件"):
        st.session_state["filter_column"] = None
        st.session_state["filter_value"] = None
        st.query_params.update()  # 重新运行页面，应用重置效果
