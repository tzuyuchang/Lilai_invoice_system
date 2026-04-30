import os
import sys
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color

def hex_to_color(hex_color):
    hex_color = hex_color.lstrip('#')
    return Color(*[int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4)])

def load_language_schools(file_path="language_schools.json"):
    """從JSON檔案讀取語言學校資訊"""
    schools = {}
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            for school in data:
                name = school.get('name', '')
                if name:
                    schools[name] = {
                        'name': name,
                        'address': school.get('address', ''),
                        'phone': school.get('phone', '')
                    }
    except FileNotFoundError:
        print(f"⚠️ 找不到檔案 {file_path}")
    except json.JSONDecodeError:
        print(f"⚠️ JSON格式錯誤 {file_path}")
    
    return schools

class InvoiceGenerator:
    def __init__(self, output_path="invoice.pdf"):
        self.output_path = output_path
        self.width, self.height = A4
        self.theme_color = hex_to_color('#EBF1DE')  # Light greenish
        self.text_red = hex_to_color('#E34234')
        self.load_fonts()
        self.language_schools = load_language_schools()

    def load_fonts(self):
        # 設定你的思源宋體檔案名稱 (請確認檔案有放在同一個資料夾)
        font_path = "ref/NotoSerifTC-Bold.ttf"
        
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont("ChineseFont", font_path))
        else:
            # 備用機制：如果找不到思源宋體，會提示並暫時使用微軟正黑體
            print(f"⚠️ 找不到字體檔 {font_path}，將暫時使用微軟正黑體做為替代。")
            fallback_font = "C:\\Windows\\Fonts\\msjh.ttc"
            if os.path.exists(fallback_font):
                pdfmetrics.registerFont(TTFont("ChineseFont", fallback_font))
            else:
                raise Exception("找不到任何支援的中文字體，請確認字體檔案路徑！")

    def draw_top_header(self, c):
        # Top-left polygon background
        c.setFillColor(self.theme_color)
        c.setStrokeColor(self.theme_color)
        p = c.beginPath()
        p.moveTo(0, self.height)
        p.lineTo(0, self.height - 120)
        p.lineTo(260, self.height - 120)
        p.lineTo(360, self.height)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

        # "INVOICE" Text
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 32)
        text = "INVOICE"
        x = 50
        for char in text:
            c.drawString(x, self.height - 80, char)
            x += c.stringWidth(char, "Helvetica-Bold", 32) + 6

        # Top-right Text (更整齊的排版)
        c.setFont("Times-Bold", 26)
        right_margin = self.width - 50
        c.drawRightString(right_margin, self.height - 65, "Lilaiireland")
        
        c.setFont("Times-Bold", 16)
        c.drawRightString(right_margin, self.height - 90, "(DreamÉire International)")
        
        c.setFont("ChineseFont", 14)
        c.drawRightString(right_margin, self.height - 115, "哩來愛爾蘭(築夢愛爾國際留遊學顧問)")

        # Address lines (更整齊的排版)
        c.setFont("ChineseFont", 9)
        c.drawString(50, self.height - 145, "Address：No. 130, Jianguo 2nd Rd., Sanmin Dist., Kaohsiung City 807, Taiwan")
        c.drawString(50, self.height - 160, "Business no.：00853881")
        c.drawString(50, self.height - 175, "Email: lilaiireland@gmail.com")

        # ==========================================
        # 改進版 LOGO 排版 - 更清晰的置中對齊
        # ==========================================
        logo_path = "ref/Lilaiireland_Logo_s.PNG"
        # 將logo放在更安全的位置，避免與其他元素重疊
        logo_x = self.width - 200  
        logo_y = self.height - 210 
        
        if os.path.exists(logo_path):
            # preserveAspectRatio=True 會保持你 Logo 的比例不變形
            # mask='auto' 會自動處理 PNG 圖片的透明背景
            c.drawImage(logo_path, logo_x, logo_y, width=160, height=80, preserveAspectRatio=True, mask='auto')
        else:
            c.setFont("Helvetica-Bold", 12)
            c.setFillColorRGB(1, 0, 0)
            c.drawString(logo_x, logo_y + 40, "[找不到 Logo 圖片]")
            c.setFillColorRGB(0, 0, 0)

    def draw_middle_banner(self, c, data):
        # Banner background
        c.setFillColor(self.theme_color)
        c.setStrokeColor(self.theme_color)
        banner_y = self.height - 330
        c.rect(0, banner_y, self.width, 100, fill=1, stroke=0)

        # Content (更整齊的排版)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Times-Roman", 11)
        
        # Left side - 客戶資訊
        c.drawString(50, banner_y + 70, "Bill to:")
        c.drawString(50, banner_y + 40, data.get("bill_to_name", "Erin School of English"))
        c.drawString(50, banner_y + 25, data.get("bill_to_address", "Archway House, Blessing Court, D07 PP30, Dublin"))
        c.drawString(50, banner_y + 10, "Phone/WhatsApp: " + data.get("bill_to_phone", "+353870312026"))

        # Right side - 發票資訊
        c.drawString(400, banner_y + 70, "Invoice details:")
        # 使用當前日期作為預設值
        c.drawString(400, banner_y + 40, "Date: " + data.get("invoice_date", datetime.now().strftime("%d/%m/%Y")))

    def draw_table(self, c, data):
        items = data.get("items", [])
        tax = data.get("tax", None)  # 改為None，方便判斷是否填寫
        total = data.get("total", 435.82)

        start_y = self.height - 370
        c.setFont("Times-Roman", 10)
        
        # Headers
        c.drawString(50, start_y, "DESCRIPTION")
        c.drawString(300, start_y, "ITEM")
        c.drawRightString(self.width - 50, start_y, "AMOUNT")

        # Line under header
        c.setLineWidth(0.5)
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.line(50, start_y - 10, self.width - 50, start_y - 10)

        current_y = start_y - 30
        
        # Items
        for item in items:
            c.setFillColorRGB(0, 0, 0)
            
            # 使用支援中文的字體繪製項目描述
            c.setFont("ChineseFont", 10)
            c.drawString(50, current_y, item["description"])
            
            c.setFont("Times-Roman", 10)
            c.drawString(300, current_y, item["item_type"])
            
            c.setFillColor(self.text_red)
            c.drawRightString(self.width - 50, current_y, f"EUR{item['amount']:.2f}")
            
            # Line under item
            c.setStrokeColorRGB(0.8, 0.8, 0.8)
            c.line(50, current_y - 10, self.width - 50, current_y - 10)
            
            current_y -= 30

        # Tax (只有在有填寫tax時才顯示)
        if tax is not None and tax != "" and tax != 0:
            # 將tax轉為數字以確保格式正確
            try:
                tax_value = float(tax)
                c.setFillColorRGB(0, 0, 0)
                c.drawString(300, current_y, "TAX")
                c.setFillColor(self.text_red)
                c.drawRightString(self.width - 50, current_y, f"EUR{tax_value:.2f}")
                c.setStrokeColorRGB(0.5, 0.5, 0.5)
                c.line(50, current_y - 10, self.width - 50, current_y - 10)
                
                current_y -= 30
            except (ValueError, TypeError):
                # 如果tax不是有效數字，則不顯示
                pass

        # Total
        c.setFillColorRGB(0, 0, 0)
        c.drawString(300, current_y, "Total:")
        c.setFillColor(self.text_red)
        c.drawRightString(self.width - 50, current_y, f"EUR{total:.2f}")
        c.line(300, current_y - 10, self.width - 50, current_y - 10)

    def draw_payment_info(self, c):
        start_y = self.height - 580
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Times-Roman", 11)
        
        c.drawString(50, start_y, "PAY TO:")
        c.setFont("Times-Bold", 11)
        c.drawString(50, start_y - 20, "DREAM EIRE INTERNATIONAL")
        
        # Underlined text
        c.setFont("Times-Roman", 11)
        c.drawString(50, start_y - 45, "Bank information:")
        c.line(50, start_y - 47, 130, start_y - 47)
        
        y = start_y - 65
        line_height = 16
        
        c.drawString(50, y, "Bank: TAIWAN COOPERATIVE BANK LTD")
        y -= line_height
        c.drawString(50, y, "Bank address: No.30, Bo-ai 1st Rd., Sanmin Dist., Kaohsiung City 807, Taiwan")
        y -= line_height
        c.drawString(50, y, "Bank code: TACB")
        y -= line_height
        c.drawString(50, y, "Branch: Sanmin Branch")
        y -= line_height
        
        # Bank account (bold part)
        c.drawString(50, y, "Bank account: ")
        c.setFont("Times-Bold", 11)
        c.drawString(125, y, "0590188029436")
        c.setFont("Times-Roman", 11)
        y -= line_height
        
        # Account name (bold part)
        c.drawString(50, y, "Account name: ")
        c.setFont("Times-Bold", 11)
        c.drawString(125, y, "DREAM EIRE INTERNATIONAL")
        c.setFont("Times-Roman", 11)
        y -= line_height
        
        c.drawString(50, y, "Swift code: TACBTWTP059")
        y -= line_height
        c.drawString(50, y, "Beneficiary address: No. 130, Jianguo 2nd Rd., Sanmin Dist., Kaohsiung City 807, Taiwan")

    def draw_footer(self, c):
        # 簽名區域放在銀行資訊後面，避免遮擋
        # 調整位置，確保與銀行資訊有足夠空間
        start_y = self.height - 800  # 向下移動更多空間
        
        # 簽名區域
        sign_x = 50
        sign_y = start_y
        
        sign_path = "ref/TzuYuChang_sign.png"
        
        # 繪製簽名圖片 (進一步縮小尺寸避免過大)
        if os.path.exists(sign_path):
            c.drawImage(sign_path, sign_x, sign_y, width=90, height=35, preserveAspectRatio=True, mask='auto')
        else:
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(1, 0, 0)
            c.drawString(sign_x, sign_y + 18, "[找不到簽名檔]")
            c.setFillColorRGB(0, 0, 0)
        
        # 繪製簽名的底線
        c.setLineWidth(2)
        c.setStrokeColorRGB(0.2, 0.2, 0.2)
        c.line(sign_x, sign_y + 2, sign_x + 90, sign_y + 2)
        
        # 繪製底線下方的文字
        c.setFont("Times-Roman", 10)
        c.drawString(sign_x, sign_y - 6, "Signature")
        c.drawString(sign_x, sign_y - 18, "DREAM EIRE INTERNATIONAL")

    def generate(self, data, custom_filename=None):
        # 如果提供了自訂檔名，則使用它；否則使用預設格式
        if custom_filename:
            self.output_path = custom_filename
        else:
            # 預設格式: invoice_YYYYMMDD.pdf
            date_str = datetime.now().strftime("%Y%m%d")
            self.output_path = f"invoice_output/invoice_{date_str}.pdf"
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(self.output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError:
                # If we can't create the directory, fall back to current directory
                print(f"Warning: Cannot create directory {output_dir}, saving to current directory")
                self.output_path = os.path.basename(self.output_path)
        
        c = canvas.Canvas(self.output_path, pagesize=A4)
        
        self.draw_top_header(c)
        self.draw_middle_banner(c, data)
        self.draw_table(c, data)
        self.draw_payment_info(c)
        self.draw_footer(c)
        
        c.save()
        return self.output_path

if __name__ == "__main__":
    # Ensure invoice_output directory exists
    if not os.path.exists("invoice_output"):
        os.makedirs("invoice_output")
        
    sample_data = {
        "bill_to_name": "Erin School of English",
        "bill_to_address": "Archway House, Blessing Court, D07 PP30, Dublin",
        "bill_to_phone": "+353870312026",
        "invoice_date": datetime.now().strftime("%d/%m/%Y"),  # 使用當前日期
        "items": [
            {"description": "PEI-TSO CHEN 代辦費", "item_type": "Commission", "amount": 273.00},
            {"description": "CHIH-CHUN KUO 代辦費", "item_type": "Commission", "amount": 293.00}
        ],
        "tax": -130.18,
        "total": 435.82
    }
    generator = InvoiceGenerator()
    output_file = generator.generate(sample_data)
    print(f"Generated invoice at {output_file}")