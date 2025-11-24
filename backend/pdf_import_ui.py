import streamlit as st
import pandas as pd
import os
import tempfile
import time
import hashlib
from backend.db_pdf_processor import extract_wefaricate_data, extract_centurion_data, insert_wf_open_data, insert_non_wf_open_data
from enhanced_db_manager import db_manager
from backend.pdf_import_processor import PDFImportProcessor

# 创建PDF导入处理器实例
pdf_processor = PDFImportProcessor()

# 设置页面配置
st.set_page_config(
    page_title="PDF采购订单导入系统",
    page_icon="📄",
    layout="wide"
)

# 页面标题
st.title("📄 PDF采购订单导入系统")
st.markdown("---")

# 创建标签页
tab1, tab2 = st.tabs(["PDF导入", "数据库管理"])

# Tab 1: PDF导入
with tab1:
    # 侧边栏
    st.sidebar.header("操作选项")
    st.sidebar.info("请选择PDF文件并指定所属公司")

    # 使用session_state存储上传的文件，避免重复上传问题
    if 'uploaded_files' in st.session_state:
        # 保留已上传的文件
        uploaded_files_history = st.session_state.uploaded_files
    else:
        st.session_state.uploaded_files = []
        uploaded_files_history = []
    
    # 文件上传
    new_uploaded_files = st.file_uploader("选择PDF文件", type=["pdf"], accept_multiple_files=True, key=f"uploader_{len(uploaded_files_history)}")
    
    # 更新session_state，将新文件添加到历史记录中
    if new_uploaded_files:
        # 如果是单个文件，将其转换为列表
        if not isinstance(new_uploaded_files, list):
            new_uploaded_files = [new_uploaded_files]
        
        # 将新文件添加到历史记录中（避免重复）
        for new_file in new_uploaded_files:
            # 检查文件是否已存在于历史记录中
            file_exists = False
            for existing_file in uploaded_files_history:
                if existing_file.name == new_file.name and existing_file.size == new_file.size:
                    file_exists = True
                    break
            
            # 如果文件不存在，则添加到历史记录中
            if not file_exists:
                uploaded_files_history.append(new_file)
        
        # 更新session_state
        st.session_state.uploaded_files = uploaded_files_history
    
    # 公司选择
    company_options = {
        "Wefaricate": "wf_open",
        "Centurion Safety Products": "non_wf_open"
    }

    selected_company = st.selectbox(
        "选择PDF所属公司",
        options=list(company_options.keys())
    )

    # 处理按钮
    if st.button("处理并导入数据", type="primary", key="process_button"):
        if st.session_state.uploaded_files:
            # 创建一个列表来跟踪成功处理的文件
            processed_files = []
            
            for uploaded_file in st.session_state.uploaded_files:
                with st.spinner(f"正在处理PDF文件: {uploaded_file.name}..."):
                    try:
                        # 创建临时文件
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_file_path = tmp_file.name
                        
                        # 根据选择的公司处理PDF并检查重复数据
                        company_name = "wefabricate" if selected_company == "Wefaricate" else "centurion"
                        result = pdf_processor.process_pdf_with_duplicate_check(tmp_file_path, company_name)
                        
                        if result["success"]:
                            # 显示提取的数据
                            st.subheader(f"提取的数据预览 - {uploaded_file.name}")
                            df = pd.DataFrame(result["data"])
                            st.dataframe(df)
                            
                            # 检查是否有重复数据
                            if result["duplicates"]:
                                st.warning(f"⚠️ 检测到 {len(result['duplicates'])} 条重复数据")
                                # 显示重复数据详情
                                dup_df = pd.DataFrame([dup['data'] for dup in result['duplicates']])
                                st.dataframe(dup_df)
                            
                            # 插入数据
                            insert_result = pdf_processor.insert_data_with_check(result["table_name"], result["data"])
                            if insert_result["success"]:
                                st.success(f"✅ 成功导入 {insert_result['count']} 条数据到 {result['table_name']} 表")
                                processed_files.append(uploaded_file.name)  # 标记为已处理
                            else:
                                st.error(f"❌ 插入数据时出错: {insert_result['error']}")
                        else:
                            st.warning(f"⚠️ 处理PDF {uploaded_file.name} 时出错: {result['error']}")
                        
                        # 删除临时文件
                        os.unlink(tmp_file_path)
                        
                    except Exception as e:
                        st.error(f"❌ 处理文件 {uploaded_file.name} 时出现错误: {str(e)}")
                        # 确保删除临时文件
                        if 'tmp_file_path' in locals():
                            try:
                                os.unlink(tmp_file_path)
                            except:
                                pass
            
            # 从session_state中移除已处理的文件
            if processed_files:
                st.session_state.uploaded_files = [f for f in st.session_state.uploaded_files if f.name not in processed_files]
                
                # 显示处理完成信息
                st.success(f"✅ 已处理 {len(processed_files)} 个文件")
                
                # 添加一个重新加载按钮，让用户可以继续上传更多文件
                if st.button("继续上传更多文件"):
                    st.rerun()
        else:
            st.warning("⚠️ 请先选择一个PDF文件")
    
    # 显示已上传的文件列表
    if st.session_state.uploaded_files:
        st.subheader("已上传的文件")
        for i, file in enumerate(st.session_state.uploaded_files):
            st.write(f"{i+1}. {file.name} ({file.size} bytes)")

    # 显示使用说明
    st.markdown("---")
    st.subheader("使用说明")
    st.markdown("""
    1. 点击"选择PDF文件"按钮上传采购订单PDF文件
    2. 从下拉菜单中选择PDF所属的公司
    3. 点击"处理并导入数据"按钮开始处理
    4. 系统将自动解析PDF并导入到相应的数据库表中

    **注意事项:**
    - 确保PDF文件格式正确
    - 系统会验证数据的一致性（qty × net_price = total_price）
    - 重复的记录将被更新而不是插入
    """)

    # 显示示例文件信息
    st.markdown("---")
    st.subheader("示例文件")
    st.markdown("""
    - **Wefaricate PDF**: `Purchase Order - 4500010647.pdf`
    - **Centurion PDF**: `Centurion Safety Products Purchase Order PO-100130.pdf`
    """)

# Tab 2: 数据库管理
with tab2:
    st.header("数据库管理")
    
    # 选择要管理的表
    table_options = {
        "WF Open": "wf_open",
        "WF Closed": "wf_closed",
        "Non-WF Open": "non_wf_open",
        "Non-WF Closed": "non_wf_closed"
    }
    
    selected_table_display = st.selectbox(
        "选择要管理的表",
        options=list(table_options.keys())
    )
    
    selected_table = table_options[selected_table_display]
    
    # 添加一个刷新按钮，让用户可以手动刷新数据
    if st.button("刷新数据"):
        st.session_state.refresh_trigger = time.time() if 'refresh_trigger' not in st.session_state else st.session_state.refresh_trigger + 1
    
    # 查询并显示表数据
    colnames, records = db_manager.query_table(selected_table)
    
    if colnames is not None and records is not None:
        st.subheader(f"{selected_table_display} 表数据")
        
        # 将数据转换为DataFrame
        df = pd.DataFrame(records, columns=colnames)
        
        # 为每行数据添加版本哈希
        row_hashes = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            row_hash = db_manager.generate_row_hash(row_dict)
            row_hashes.append(row_hash)
        
        # 将哈希值添加到DataFrame中（隐藏列）
        df['_row_hash'] = row_hashes
        
        # 添加自定义CSS样式确保检索框与表格列宽一致
        st.markdown("""
        <style>
        /* 确保检索框容器与表格列对齐 */
        div[data-testid="column"] > div {
            width: 100% !important;
        }
        div[data-testid="column"] > div > div {
            width: 100% !important;
        }
        div[data-testid="column"] input[type="text"] {
            width: 100% !important;
            box-sizing: border-box !important;
        }
        /* 确保表格和检索框使用相同的列宽 */
        .stDataFrame {
            width: 100% !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 添加列检索功能 - 将检索框放在表格上方并与列宽保持一致
        search_values = {}
        
        # 创建检索框行，与表格列数保持一致
        search_cols = st.columns(len(colnames))
        for i, col_name in enumerate(colnames):
            if col_name != '_row_hash':  # 跳过哈希列
                with search_cols[i]:
                    # 使用label_visibility="collapsed"隐藏标签但仍提供非空标签
                    search_values[col_name] = st.text_input(
                        "搜索", 
                        key=f"search_{col_name}_{int(time.time() * 1000000)}",  # 添加唯一标识符
                        placeholder=col_name,
                        label_visibility="collapsed"
                    )
         
        # 应用检索过滤
        # 根据搜索值过滤数据
        filtered_df = df.drop('_row_hash', axis=1).copy()  # 移除哈希列用于显示
        for col_name, search_value in search_values.items():
            if search_value:  # 如果搜索值不为空
                # 使用字符串包含匹配（非全文搜索）
                filtered_df = filtered_df[filtered_df[col_name].astype(str).str.contains(search_value, na=False, case=False)]
        
        # 显示过滤后的数据
        st.write(f"显示 {len(filtered_df)} 条记录（总共 {len(df)} 条）")
        
        # 为日期字段创建特殊处理
        date_columns = ['req_date_wf', 'eta_wfsz', 'latest_departure_date', 'po_placed_date']
        
        # 显示数据表格
        edited_df = st.data_editor(
            filtered_df,
            width='stretch',
            num_rows="dynamic",
            key=f"editor_{selected_table}_{int(time.time() * 1000000)}"  # 使用时间戳确保唯一key
        )
        
        # 检查是否有修改
        # 使用更严格的方法比较数据框
        if not filtered_df.reset_index(drop=True).equals(edited_df.reset_index(drop=True)):
            # 找出修改的行
            modified_rows = []
            # 确保两个数据框有相同的索引
            filtered_df_reset = filtered_df.reset_index(drop=True)
            edited_df_reset = edited_df.reset_index(drop=True)
            
            for i in range(min(len(filtered_df_reset), len(edited_df_reset))):
                # 使用更严格的比较方法
                original_row = filtered_df_reset.iloc[i]
                edited_row = edited_df_reset.iloc[i]
                
                # 检查是否有任何列不同
                row_changed = False
                for col_name in filtered_df_reset.columns:
                    if col_name in edited_row and str(original_row[col_name]) != str(edited_row[col_name]):
                        row_changed = True
                        break
                
                if row_changed:
                    modified_rows.append(i)
            
            # 处理修改
            if modified_rows:
                update_success_count = 0
                update_failed_count = 0
                for row_idx in modified_rows:
                    original_row = filtered_df_reset.iloc[row_idx]
                    edited_row = edited_df_reset.iloc[row_idx]
                    
                    # 找出修改的列
                    updates = {}
                    for col_name in colnames:
                        if col_name in edited_row and col_name in original_row:
                            original_value = original_row[col_name]
                            edited_value = edited_row[col_name]
                            
                            # 如果值不同，则添加到更新列表
                            if str(original_value) != str(edited_value):
                                # 特殊处理日期字段，确保格式正确
                                if col_name in date_columns:
                                    # 对于日期字段，确保空值正确处理
                                    if edited_value == '' or edited_value == 'None' or edited_value == 'nan':
                                        updates[col_name] = None
                                    else:
                                        # 保持日期字符串格式
                                        updates[col_name] = edited_value
                                else:
                                    # 处理其他字段
                                    if edited_value == 'None' or edited_value == 'nan':
                                        updates[col_name] = None
                                    else:
                                        updates[col_name] = edited_value
                    
                    # 如果有更新，则执行更新操作
                    if updates:
                        # 获取该行的哈希值（需要从原始df中获取）
                        original_full_row = df[df['pn'] == edited_row['pn']]
                        if not original_full_row.empty:
                            row_hash = original_full_row.iloc[0]['_row_hash']
                            
                            # 显示调试信息
                            st.info(f"正在更新 PN={edited_row['pn']} 的记录，更新字段: {list(updates.keys())}")
                            
                            # 更新数据库（带版本控制）
                            success, message = db_manager.update_row_with_version(
                                selected_table, 
                                edited_row['pn'], 
                                updates,
                                row_hash
                            )
                            if success:
                                st.success(f"已更新 PN={edited_row['pn']} 的记录: {message}")
                                update_success_count += 1
                            else:
                                st.error(f"更新 PN={edited_row['pn']} 的记录失败: {message}")
                                update_failed_count += 1
                        else:
                            st.error(f"未找到 PN={edited_row['pn']} 的原始记录")
                            update_failed_count += 1
                
                # 所有更新完成后重新加载数据
                if update_success_count > 0 or update_failed_count > 0:
                    if update_success_count > 0:
                        st.success(f"成功更新 {update_success_count} 条记录")
                    if update_failed_count > 0:
                        st.error(f"更新失败 {update_failed_count} 条记录")
                    time.sleep(1)  # 等待数据库更新完成
                    st.rerun()  # 使用新的rerun方法
        
        # 添加删除功能
        st.subheader("删除记录")
        pn_to_delete = st.text_input("输入要删除的记录的PN号")
        if st.button("删除记录"):
            if pn_to_delete:
                # 查找要删除行的哈希值
                row_to_delete = df[df['pn'] == pn_to_delete]
                if not row_to_delete.empty:
                    row_hash = row_to_delete.iloc[0]['_row_hash']
                    success, message = db_manager.delete_row_with_version(selected_table, pn_to_delete, row_hash)
                    if success:
                        st.success(f"已删除 PN={pn_to_delete} 的记录: {message}")
                        # 删除后重新加载数据
                        time.sleep(1)  # 等待数据库更新完成
                        st.rerun()  # 使用新的rerun方法
                    else:
                        st.error(f"删除 PN={pn_to_delete} 的记录失败: {message}")
                else:
                    st.warning("未找到指定的PN号")
            else:
                st.warning("请输入要删除的PN号")
                
        # 添加插入功能
        st.subheader("插入新记录")
        with st.form("insert_form"):
            # 创建输入字段（根据表结构动态创建）
            new_record = {}
            for col_name in colnames:
                if col_name != '_row_hash':  # 跳过哈希列
                    # 对日期字段使用日期输入控件
                    if col_name in date_columns:
                        # 如果有默认值且是日期格式，则解析它
                        default_value = None
                        new_record[col_name] = st.date_input(f"{col_name}", value=default_value, key=f"insert_{col_name}")
                    else:
                        new_record[col_name] = st.text_input(f"{col_name}", key=f"insert_{col_name}")
            
            submit_button = st.form_submit_button("插入记录")
            
            if submit_button:
                # 检查必填字段（PN作为主键是必需的）
                if new_record.get('pn'):
                    # 清理空值并转换日期格式
                    cleaned_record = {}
                    for k, v in new_record.items():
                        if v:
                            # 处理日期字段
                            if k in date_columns:
                                # 处理日期对象
                                if hasattr(v, 'strftime'):
                                    cleaned_record[k] = v.strftime('%Y-%m-%d')
                                else:
                                    # 如果已经是字符串格式，直接使用
                                    cleaned_record[k] = str(v)
                            else:
                                cleaned_record[k] = v
                        else:
                            # 保留空值字段
                            cleaned_record[k] = None
                    
                    success, message = db_manager.insert_row(selected_table, cleaned_record)
                    if success:
                        st.success(f"插入记录成功: {message}")
                        # 插入后重新加载数据
                        time.sleep(1)  # 等待数据库更新完成
                        st.rerun()  # 使用新的rerun方法
                    else:
                        st.error(f"插入记录失败: {message}")
                else:
                    st.warning("PN字段是必需的")
    else:
        st.warning("无法加载表数据")