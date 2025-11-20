#!/usr/bin/env python3
"""
Script để OCR các PDF scan trong thư mục documents
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
from tqdm import tqdm


def is_pdf_scanned(pdf_path):
    """
    Kiểm tra xem PDF có phải là scan (không có text) không
    
    Returns:
        True nếu là scan, False nếu có text
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Check first page
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            
            # Nếu không có text hoặc text rất ít, coi như là scan
            if not text or len(text.strip()) < 50:
                return True
    except:
        return True
    
    return False


def ocr_pdf(pdf_path, output_path, lang='vie+eng'):
    """
    OCR một PDF scan và tạo PDF mới có text layer
    
    Args:
        pdf_path: Đường dẫn PDF gốc
        output_path: Đường dẫn PDF output
        lang: Ngôn ngữ OCR (vie cho tiếng Việt, eng cho tiếng Anh)
    """
    print(f"📄 OCR file: {os.path.basename(pdf_path)}")
    
    try:
        # Convert PDF to images
        print("   - Converting PDF to images...")
        images = convert_from_path(pdf_path, dpi=300)
        
        # OCR each page and create text file
        all_text = []
        
        for i, image in enumerate(tqdm(images, desc="   - OCR pages")):
            # Perform OCR
            text = pytesseract.image_to_string(image, lang=lang)
            all_text.append(f"--- Trang {i+1} ---\n{text}\n\n")
        
        # Save as text file (easier to process than PDF with text layer)
        txt_path = output_path.replace('.pdf', '.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.writelines(all_text)
        
        print(f"   ✅ OCR hoàn tất: {os.path.basename(txt_path)}")
        return txt_path
        
    except Exception as e:
        print(f"   ❌ Lỗi OCR: {e}")
        return None


def main():
    """
    Main function
    """
    print("=" * 70)
    print("🔍 OCR PDF SCAN TOOL")
    print("=" * 70)
    
    docs_dir = "data/documents"
    
    if not Path(docs_dir).exists():
        print(f"❌ Thư mục {docs_dir} không tồn tại!")
        return
    
    # Find all PDFs
    pdf_files = list(Path(docs_dir).glob("*.pdf"))
    
    if not pdf_files:
        print(f"⚠️  Không tìm thấy file PDF nào trong {docs_dir}")
        return
    
    print(f"\n📚 Tìm thấy {len(pdf_files)} file PDF")
    print("\n🔍 Kiểm tra PDF nào là scan...")
    
    scanned_pdfs = []
    for pdf_file in pdf_files:
        if is_pdf_scanned(str(pdf_file)):
            scanned_pdfs.append(pdf_file)
            print(f"   📄 {pdf_file.name} - PDF scan (cần OCR)")
        else:
            print(f"   ✅ {pdf_file.name} - Đã có text")
    
    if not scanned_pdfs:
        print("\n✅ Tất cả PDF đều có text, không cần OCR!")
        return
    
    print(f"\n⚡ Bắt đầu OCR {len(scanned_pdfs)} file...")
    print("   (Ngôn ngữ: Tiếng Việt + Tiếng Anh)")
    print()
    
    success_count = 0
    
    for pdf_file in scanned_pdfs:
        # OCR and save as .txt
        output_path = str(pdf_file).replace('.pdf', '_ocr.txt')
        
        result = ocr_pdf(str(pdf_file), output_path, lang='vie+eng')
        
        if result:
            success_count += 1
            print()
    
    print("=" * 70)
    print(f"✅ Hoàn tất! OCR thành công {success_count}/{len(scanned_pdfs)} file")
    print("=" * 70)
    
    if success_count > 0:
        print("\n📝 Các file TXT đã được tạo từ PDF scan:")
        for pdf_file in scanned_pdfs:
            txt_file = str(pdf_file).replace('.pdf', '_ocr.txt')
            if Path(txt_file).exists():
                print(f"   - {os.path.basename(txt_file)}")
        
        print("\n🚀 Bước tiếp theo:")
        print("   1. Kiểm tra các file TXT vừa tạo")
        print("   2. Chạy: python scripts/process_documents.py")
        print("   3. Chatbot sẽ sử dụng text từ các file này!")


if __name__ == "__main__":
    main()





