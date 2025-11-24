import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.db_pdf_processor import extract_wefaricate_data

def test_cross_page_pdfs():
    """测试跨页PDF处理"""
    pdf_files = [
        'd:/GitHub/SAP_like/pdf_samples/Purchase Order - 4500008993.pdf',
        'd:/GitHub/SAP_like/pdf_samples/Purchase Order - 4500009645.pdf'
    ]
    
    for pdf_path in pdf_files:
        print(f"\n=== 测试PDF文件: {pdf_path} ===")
        try:
            data = extract_wefaricate_data(pdf_path)
            print(f"成功提取 {len(data)} 条数据")
            
            # 检查是否有数据行丢失了req_date_wf
            missing_dates = 0
            for i, row in enumerate(data):
                if not row.get('req_date_wf'):
                    missing_dates += 1
                    print(f"  数据行 {i+1} 缺少req_date_wf: Item={row.get('line')}, ID={row.get('pn')}")
                else:
                    print(f"  数据行 {i+1} 有req_date_wf: {row.get('req_date_wf')}")
            
            print(f"总共 {len(data)} 条数据，其中 {missing_dates} 条缺少req_date_wf")
            
            # 显示前几条数据的详细信息
            print("\n前5条数据详情:")
            for i, row in enumerate(data[:5]):
                print(f"  {i+1}. Item: {row.get('line')}, ID: {row.get('pn')}, Date: {row.get('req_date_wf')}")
                
        except Exception as e:
            print(f"处理 {pdf_path} 时出错: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_cross_page_pdfs()