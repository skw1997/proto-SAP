import pdfplumber
import re
from decimal import Decimal

# 加载db_pdf_processor中的函数
from backend.db_pdf_processor import extract_wefaricate_data

def parse_decimal(value):
    """解析Decimal值，处理货币符号"""
    if not value:
        return None
    
    try:
        # 移除货币符号
        clean_value = re.sub(r'[€$£]', '', str(value))
        # 移除逗号
        clean_value = clean_value.replace(',', '')
        # 保留所有小数位
        return Decimal(clean_value)
    except:
        return None

# 重新定义parse_eur_price函数用于测试
def parse_eur_price(price_str):
    """解析欧元价格，提取数值并计算单价"""
    if not price_str:
        return "", ""
    
    # 清理字符串，移除换行符
    price_str = price_str.replace('\n', ' ').strip()
    
    # 提取价格数值
    price_match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', ''))
    if not price_match:
        return price_str, ""
    
    # 提取per后的数量
    per_match = re.search(r'per\s+(\d+)', price_str, re.IGNORECASE)
    quantity = int(per_match.group(1)) if per_match else 1
    
    # 计算单价
    try:
        price_value = float(price_match.group(0))
        unit_price = price_value / quantity
        # 保留更多小数位以确保精度
        unit_price_str = f"€{unit_price:.10f}".rstrip('0').rstrip('.')
        return unit_price_str, f"€{price_value:.10f}".rstrip('0').rstrip('.')
    except:
        return price_str, ""

def debug_pdf_processing():
    """调试PDF处理过程"""
    pdf_path = "pdf_samples/Purchase Order - 4500010045.pdf"
    
    print("=== 开始调试PDF处理 ===")
    print(f"PDF路径: {pdf_path}")
    
    # 使用extract_wefaricate_data函数处理PDF
    data = extract_wefaricate_data(pdf_path)
    
    print(f"提取到 {len(data)} 条数据")
    
    # 显示所有数据
    for i, entry in enumerate(data):
        print(f"\n{i+1}. PO: {entry['po']}, Line: {entry['line']}, PN: {entry['pn']}")
        print(f"    Qty: {entry['qty']}, Net Price: {entry['net_price']}, Total Price: {entry['total_price']}")
        print(f"    Req Date WF: {entry['req_date_wf']}")
    
    # 验证特定问题数据
    print("\n=== 验证特定问题数据 ===")
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        tables = page.extract_tables()
        
        if tables:
            table = tables[0]
            print(f"表格总行数: {len(table)}")
            
            # 查找line 30的数据
            for i, row in enumerate(table):
                if len(row) > 0 and str(row[0]).strip() == '00030':
                    print(f"\n发现问题行 (行 {i}):")
                    print(f"  Item: '{row[0]}'")
                    if len(row) > 1:
                        print(f"  ID: '{row[1]}'")
                    if len(row) > 4:
                        print(f"  Price Cell: '{row[4]}'")
                    if len(row) > 5:
                        print(f"  Value Cell: '{row[5]}'")
                    
                    # 解析价格
                    if len(row) > 4:
                        price_cell = str(row[4])
                        unit_price, total_price = parse_eur_price(price_cell)
                        print(f"  解析后的Net Price: '{unit_price}'")
                    
                    # 清理Net Value
                    if len(row) > 5:
                        net_value_raw = str(row[5])
                        net_value = net_value_raw  # 简单处理
                        print(f"  清理后的Net Value: '{net_value}'")
                    
                    # 转换为Decimal进行计算
                    qty_decimal = parse_decimal('480')  # 已知数量
                    price_decimal = parse_decimal(unit_price)
                    value_decimal = parse_decimal(net_value)
                    
                    print(f"  Quantity (Decimal): {qty_decimal}")
                    print(f"  Net Price (Decimal): {price_decimal}")
                    print(f"  Net Value (Decimal): {value_decimal}")
                    
                    # 验证计算
                    if qty_decimal and price_decimal:
                        calculated_total = qty_decimal * price_decimal
                        print(f"  计算得出的总价: {calculated_total}")
                        if value_decimal:
                            difference = abs(calculated_total - value_decimal)
                            print(f"  与实际总价的差值: {difference}")
                            
                            # 检查如果价格是0.033是否匹配
                            test_price = parse_decimal('0.033')
                            if test_price:
                                test_total = qty_decimal * test_price
                                print(f"  如果价格是0.033，计算结果: {test_total}")
                                test_difference = abs(test_total - value_decimal)
                                print(f"  与实际总价的差值: {test_difference}")

if __name__ == "__main__":
    debug_pdf_processing()