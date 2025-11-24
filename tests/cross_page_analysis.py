import pdfplumber
import re

def analyze_cross_page_issues(pdf_path):
    """分析PDF文件的跨页问题，特别是Schedule Lines与数据行的关联"""
    print(f"\n=== 分析PDF文件跨页问题: {pdf_path} ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"总页数: {len(pdf.pages)}")
        
        # 存储所有页面的信息
        all_pages_data = []
        
        # 处理每一页
        for page_num, page in enumerate(pdf.pages):
            print(f"\n--- 第 {page_num + 1} 页 ---")
            
            # 提取文本
            text = page.extract_text()
            if text:
                # 查找PO号码
                po_match = re.search(r'Purchase Order[^\d]*(\d+)', text)
                if po_match:
                    print(f"PO号码: {po_match.group(1)}")
                
                # 查找Created on日期
                created_on_match = re.search(r'Created on:\s*([A-Za-z]+\s*\d{1,2},\s*\d{4})', text)
                if created_on_match:
                    print(f"Created on: {created_on_match.group(1)}")
            
            # 提取表格
            tables = page.extract_tables()
            if tables:
                table = tables[0]
                print(f"表格有 {len(table)} 行")
                
                # 分析表格内容
                page_data = {
                    'page_num': page_num + 1,
                    'data_rows': [],
                    'schedule_lines_rows': [],
                    'other_rows': []
                }
                
                for i, row in enumerate(table):
                    if row and any(cell and str(cell).strip() for cell in row):
                        row_content = " ".join(str(cell) for cell in row if cell)
                        
                        # 检查是否为数据行（以数字开头）
                        if re.match(r'^\d+', row_content):
                            page_data['data_rows'].append((i, row_content, row))
                            print(f"  数据行 {i}: {row_content[:60]}...")
                        
                        # 检查是否为Schedule Lines行
                        elif 'Schedule Lines:' in row_content:
                            page_data['schedule_lines_rows'].append((i, row_content, row))
                            print(f"  Schedule Lines行 {i}: {row_content[:60]}...")
                            
                            # 查看下一行（可能包含日期）
                            if i + 1 < len(table):
                                next_row = table[i + 1]
                                if next_row:
                                    next_content = " ".join(str(cell) for cell in next_row if cell)
                                    print(f"    下一行 {i+1}: {next_content[:60]}...")
                                    
                                    # 检查是否有日期格式
                                    date_match = re.search(r'[A-Za-z]+\s*\d{1,2},\s*\d{4}', next_content)
                                    if date_match:
                                        print(f"      发现日期: {date_match.group(0)}")
                        
                        # 其他行
                        else:
                            page_data['other_rows'].append((i, row_content, row))
                
                all_pages_data.append(page_data)
                
                # 分析当前页面内的关联关系
                print(f"\n  分析第 {page_num + 1} 页内关联关系:")
                for schedule_idx, schedule_content, schedule_row in page_data['schedule_lines_rows']:
                    # 查找下一个数据行
                    next_data_row = None
                    for data_idx, data_content, data_row in page_data['data_rows']:
                        if data_idx > schedule_idx:
                            next_data_row = (data_idx, data_content, data_row)
                            break
                    
                    if next_data_row:
                        data_idx, data_content, data_row = next_data_row
                        print(f"    Schedule Lines行 {schedule_idx} -> 数据行 {data_idx}")
                    else:
                        print(f"    Schedule Lines行 {schedule_idx} -> 未找到对应数据行")
            else:
                print("  未找到表格")
        
        # 分析跨页关联关系
        print(f"\n=== 跨页关联分析 ===")
        for page_idx, page_data in enumerate(all_pages_data):
            if page_idx < len(all_pages_data) - 1:
                current_page = page_data
                next_page = all_pages_data[page_idx + 1]
                
                print(f"\n第 {current_page['page_num']} 页 -> 第 {next_page['page_num']} 页:")
                
                # 检查当前页面最后一个Schedule Lines是否应该关联到下一页第一个数据行
                if current_page['schedule_lines_rows'] and next_page['data_rows']:
                    last_schedule = current_page['schedule_lines_rows'][-1]
                    first_data = next_page['data_rows'][0]
                    
                    print(f"  当前页最后Schedule Lines行 {last_schedule[0]} 可能需要关联到下一页第一个数据行 {first_data[0]}")
                    
                    # 检查当前页Schedule Lines的下一行是否有日期
                    schedule_row_idx = last_schedule[0]
                    # 需要在原始表格中查找
                    table = pdf.pages[current_page['page_num'] - 1].extract_tables()[0]
                    if schedule_row_idx + 1 < len(table):
                        date_row = table[schedule_row_idx + 1]
                        if date_row:
                            date_content = " ".join(str(cell) for cell in date_row if cell)
                            date_match = re.search(r'[A-Za-z]+\s*\d{1,2},\s*\d{4}', date_content)
                            if date_match:
                                print(f"    日期行内容: {date_content[:60]}...")
                                print(f"    提取的日期: {date_match.group(0)}")

if __name__ == "__main__":
    # 分析两个有问题的PDF文件
    pdf_files = [
        'd:/GitHub/SAP_like/pdf_samples/Purchase Order - 4500008993.pdf',
        'd:/GitHub/SAP_like/pdf_samples/Purchase Order - 4500009645.pdf'
    ]
    
    for pdf_path in pdf_files:
        try:
            analyze_cross_page_issues(pdf_path)
        except Exception as e:
            print(f"分析 {pdf_path} 时出错: {e}")