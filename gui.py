import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from invoice_generator_fixed import InvoiceGenerator, load_language_schools
import os
from datetime import datetime

class InvoiceSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("報價單生成系統 - DreamÉire International")
        self.root.geometry("600x750")
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # 讀取語言學校資訊
        self.language_schools = load_language_schools()
        self.school_names = list(self.language_schools.keys())
        
        # --- Variables ---
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.school_var = tk.StringVar()
        self.bill_name_var = tk.StringVar()
        self.bill_address_var = tk.StringVar()
        self.bill_phone_var = tk.StringVar()
        self.tax_var = tk.StringVar()
        self.filename_var = tk.StringVar(value=f"invoice_{datetime.now().strftime('%Y%m%d')}.pdf")
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # --- School Selection ---
        school_lf = ttk.LabelFrame(main_frame, text="語言學校選擇 (School Selection)", padding="10")
        school_lf.pack(fill="x", pady=5)
        
        ttk.Label(school_lf, text="選擇學校 (Select School):").grid(row=0, column=0, sticky="w", pady=2)
        
        # 下拉選單
        self.school_combo = ttk.Combobox(school_lf, textvariable=self.school_var, 
                                        values=[""] + self.school_names, width=50)
        self.school_combo.grid(row=0, column=1, sticky="ew", pady=2)
        self.school_combo.bind('<<ComboboxSelected>>', self.on_school_selected)
        
        # 手動輸入按鈕
        ttk.Button(school_lf, text="手動輸入 (Manual Input)", command=self.enable_manual_input).grid(row=1, column=0, columnspan=2, sticky="w", pady=2)
        
        # --- Basic Info ---
        info_lf = ttk.LabelFrame(main_frame, text="基本資訊 (Basic Info)", padding="10")
        info_lf.pack(fill="x", pady=5)
        
        ttk.Label(info_lf, text="日期 (Date):").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Entry(info_lf, textvariable=self.date_var).grid(row=0, column=1, sticky="ew", pady=2)
        
        ttk.Label(info_lf, text="客戶名稱 (Bill To Name):").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(info_lf, textvariable=self.bill_name_var).grid(row=1, column=1, sticky="ew", pady=2)
        
        ttk.Label(info_lf, text="客戶地址 (Bill To Address):").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(info_lf, textvariable=self.bill_address_var).grid(row=2, column=1, sticky="ew", pady=2)
        
        ttk.Label(info_lf, text="聯絡電話 (Phone/WhatsApp):").grid(row=3, column=0, sticky="w", pady=2)
        ttk.Entry(info_lf, textvariable=self.bill_phone_var).grid(row=3, column=1, sticky="ew", pady=2)
        
        # --- Filename ---
        filename_lf = ttk.LabelFrame(main_frame, text="檔名設定 (Filename)", padding="10")
        filename_lf.pack(fill="x", pady=5)
        
        ttk.Label(filename_lf, text="輸出檔名 (Output Filename):").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Entry(filename_lf, textvariable=self.filename_var).grid(row=0, column=1, sticky="ew", pady=2)
        
        # --- Items ---
        items_lf = ttk.LabelFrame(main_frame, text="項目 (Items)", padding="10")
        items_lf.pack(fill="both", expand=True, pady=5)
        
        # Treeview for items
        columns = ("desc", "type", "amount")
        self.tree = ttk.Treeview(items_lf, columns=columns, show="headings", height=5)
        self.tree.heading("desc", text="說明 (Description)")
        self.tree.heading("type", text="類別 (Item Type)")
        self.tree.heading("amount", text="金額 (Amount)")
        
        self.tree.column("desc", width=200)
        self.tree.column("type", width=100)
        self.tree.column("amount", width=100)
        
        self.tree.pack(fill="both", expand=True, pady=5)
        
        # Item Entry Form
        item_entry_frame = ttk.Frame(items_lf)
        item_entry_frame.pack(fill="x", pady=5)
        
        self.desc_var = tk.StringVar()
        self.type_var = tk.StringVar(value="Commission")
        self.amount_var = tk.StringVar()
        
        ttk.Entry(item_entry_frame, textvariable=self.desc_var, width=20).pack(side="left", padx=2)
        ttk.Entry(item_entry_frame, textvariable=self.type_var, width=15).pack(side="left", padx=2)
        ttk.Entry(item_entry_frame, textvariable=self.amount_var, width=10).pack(side="left", padx=2)
        
        ttk.Button(item_entry_frame, text="新增 (Add)", command=self.add_item).pack(side="left", padx=5)
        ttk.Button(item_entry_frame, text="刪除所選 (Delete)", command=self.delete_item).pack(side="left")
        
        # --- Summary ---
        summary_lf = ttk.LabelFrame(main_frame, text="總計 (Summary)", padding="10")
        summary_lf.pack(fill="x", pady=5)
        
        ttk.Label(summary_lf, text="稅金/扣除額 (Tax/Deduction):").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Entry(summary_lf, textvariable=self.tax_var).grid(row=0, column=1, sticky="w", pady=2)
        
        # --- Action ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", pady=10)
        
        ttk.Button(action_frame, text="瀏覽 (Browse)", command=self.browse_file).pack(side="left", padx=5)
        ttk.Button(action_frame, text="生成報價單 (Generate PDF)", command=self.generate_pdf).pack(side="right")
        
        info_lf.columnconfigure(1, weight=1)
        filename_lf.columnconfigure(1, weight=1)
        school_lf.columnconfigure(1, weight=1)
        
    def on_school_selected(self, event):
        """當選擇學校時自動填入資訊"""
        selected_school = self.school_var.get()
        if selected_school and selected_school in self.language_schools:
            school_data = self.language_schools[selected_school]
            self.bill_name_var.set(school_data.get('name', ''))
            self.bill_address_var.set(school_data.get('address', ''))
            self.bill_phone_var.set(school_data.get('phone', ''))
            
    def enable_manual_input(self):
        """啟用手動輸入模式"""
        self.school_var.set("")
        self.bill_name_var.set("")
        self.bill_address_var.set("")
        self.bill_phone_var.set("")
        
    def add_item(self):
        desc = self.desc_var.get()
        itype = self.type_var.get()
        amt = self.amount_var.get()
        if desc and itype and amt:
            try:
                float(amt)
                self.tree.insert("", "end", values=(desc, itype, amt))
                self.desc_var.set("")
                self.amount_var.set("")
            except ValueError:
                messagebox.showerror("Error", "金額必須是數字 (Amount must be a number)")
                
    def delete_item(self):
        selected = self.tree.selection()
        for item in selected:
            self.tree.delete(item)
            
    def browse_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=self.filename_var.get()
        )
        if filename:
            self.filename_var.set(os.path.basename(filename))
            
    def generate_pdf(self):
        try:
            items = []
            total = 0.0
            for item in self.tree.get_children():
                val = self.tree.item(item)['values']
                amt = float(val[2])
                items.append({
                    "description": val[0],
                    "item_type": val[1],
                    "amount": amt
                })
                total += amt
                
            tax = float(self.tax_var.get()) if self.tax_var.get() else None
            if tax is not None:
                total += tax
            
            # 獲取客戶資訊
            bill_to_name = self.bill_name_var.get() or "Erin School of English"
            bill_to_address = self.bill_address_var.get() or "Archway House, Blessing Court, D07 PP30, Dublin"
            bill_to_phone = self.bill_phone_var.get() or "+353870312026"
            
            data = {
                "invoice_date": self.date_var.get(),
                "bill_to_name": bill_to_name,
                "bill_to_address": bill_to_address,
                "bill_to_phone": bill_to_phone,
                "items": items,
                "tax": tax,
                "total": total
            }
            
            output_file = self.filename_var.get()
            # 確保檔名以.pdf結尾
            if not output_file.endswith('.pdf'):
                output_file += '.pdf'
                
            gen = InvoiceGenerator()
            output_path = gen.generate(data, output_file)
            
            messagebox.showinfo("Success", f"報價單已成功生成！\n(Saved as {output_path})")
            # 在Windows中開啟檔案
            os.startfile(output_path) 
        except Exception as e:
            messagebox.showerror("Error", f"生成失敗 (Failed to generate):\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceSystemApp(root)
    root.mainloop()