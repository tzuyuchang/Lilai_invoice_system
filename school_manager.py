#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
語言學校資訊維護工具
用於簡單地添加、編輯和刪除語言學校資訊
"""

import json
import sys
from pathlib import Path

def load_schools(file_path="language_schools.json"):
    """載入學校資料"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("JSON格式錯誤，將建立新的檔案")
        return []

def save_schools(schools, file_path="language_schools.json"):
    """儲存學校資料"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(schools, f, ensure_ascii=False, indent=2)
    print(f"✅ 學校資料已儲存至 {file_path}")

def list_schools(schools):
    """列出所有學校"""
    if not schools:
        print("目前沒有學校資料")
        return
    
    print("\n📚 現有學校資料:")
    for i, school in enumerate(schools, 1):
        print(f"{i}. {school['name']}")
        print(f"   地址: {school['address']}")
        print(f"   電話: {school['phone']}")
        print()

def add_school(schools):
    """新增學校"""
    print("\n➕ 新增學校:")
    name = input("學校名稱: ").strip()
    if not name:
        print("❌ 學校名稱不能為空")
        return schools
    
    address = input("地址: ").strip()
    phone = input("電話/WhatsApp: ").strip()
    
    new_school = {
        "name": name,
        "address": address,
        "phone": phone
    }
    
    schools.append(new_school)
    print(f"✅ 已新增學校: {name}")
    return schools

def edit_school(schools):
    """編輯學校"""
    if not schools:
        print("❌ 沒有學校資料可編輯")
        return schools
    
    list_schools(schools)
    try:
        index = int(input("請輸入要編輯的學校編號: ")) - 1
        if 0 <= index < len(schools):
            school = schools[index]
            print(f"\n編輯學校: {school['name']}")
            
            name = input(f"學校名稱 [{school['name']}]: ").strip()
            if name:
                school['name'] = name
                
            address = input(f"地址 [{school['address']}]: ").strip()
            if address:
                school['address'] = address
                
            phone = input(f"電話/WhatsApp [{school['phone']}]: ").strip()
            if phone:
                school['phone'] = phone
                
            print(f"✅ 已更新學校: {school['name']}")
        else:
            print("❌ 編號超出範圍")
    except ValueError:
        print("❌ 請輸入有效的數字")
    
    return schools

def delete_school(schools):
    """刪除學校"""
    if not schools:
        print("❌ 沒有學校資料可刪除")
        return schools
    
    list_schools(schools)
    try:
        index = int(input("請輸入要刪除的學校編號: ")) - 1
        if 0 <= index < len(schools):
            deleted = schools.pop(index)
            print(f"✅ 已刪除學校: {deleted['name']}")
        else:
            print("❌ 編號超出範圍")
    except ValueError:
        print("❌ 請輸入有效的數字")
    
    return schools

def main():
    """主程式"""
    file_path = "language_schools.json"
    schools = load_schools(file_path)
    
    print("🎓 語言學校資訊維護工具")
    print("=" * 30)
    
    while True:
        print("\n📋 選擇操作:")
        print("1. 查看所有學校")
        print("2. 新增學校")
        print("3. 編輯學校")
        print("4. 刪除學校")
        print("5. 儲存並退出")
        
        choice = input("\n請選擇 (1-5): ").strip()
        
        if choice == '1':
            list_schools(schools)
        elif choice == '2':
            schools = add_school(schools)
        elif choice == '3':
            schools = edit_school(schools)
        elif choice == '4':
            schools = delete_school(schools)
        elif choice == '5':
            save_schools(schools, file_path)
            print("👋 再見!")
            break
        else:
            print("❌ 請輸入有效的選項 (1-5)")

if __name__ == "__main__":
    main()