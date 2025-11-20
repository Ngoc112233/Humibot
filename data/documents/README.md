# Thư mục Documents

Đặt các file tài liệu của trường vào đây.

## Định dạng được hỗ trợ

- ✅ PDF (`.pdf`)
- ✅ Word (`.docx`)
- ✅ Text (`.txt`)
- ✅ Markdown (`.md`)

## Cấu trúc khuyến nghị

Bạn có thể tổ chức documents theo cấu trúc:

```
documents/
├── dao_tao/
│   ├── quy_che_dao_tao.pdf
│   ├── chuong_trinh_hoc.pdf
│   └── quy_dinh_thi.pdf
├── sinh_vien/
│   ├── quy_dinh_hoc_vu.pdf
│   ├── huong_dan_dang_ky_hoc.docx
│   └── quy_dinh_hoc_phi.pdf
├── phong_ban/
│   ├── gioi_thieu_phong_dao_tao.txt
│   └── thong_tin_lien_he.txt
└── khac/
    └── quy_dinh_ky_tuc_xa.pdf
```

## Ví dụ nội dung

### File mẫu: `quy_dinh_tot_nghiep.txt`

```
QUY ĐỊNH VỀ XÉT TỐT NGHIỆP

1. ĐIỀU KIỆN TỐT NGHIỆP

Sinh viên được xét tốt nghiệp khi đáp ứng đủ các điều kiện sau:

a) Tích lũy đủ số tín chỉ theo chương trình đào tạo (tối thiểu 120 tín chỉ)
b) Điểm trung bình tích lũy (GPA) từ 2.0 trở lên
c) Không vi phạm quy chế sinh viên ở mức phải buộc thôi học
d) Hoàn thành các môn giáo dục quốc phòng, giáo dục thể chất
e) Không nợ học phí

2. PHÂN LOẠI TỐT NGHIỆP

- Xuất sắc: GPA >= 3.6
- Giỏi: 3.2 <= GPA < 3.6
- Khá: 2.5 <= GPA < 3.2
- Trung bình: 2.0 <= GPA < 2.5
```

## Sau khi thêm documents

Chạy script để xử lý:

```bash
python scripts/process_documents.py
```

Hoặc update vectorstore hiện tại:

```bash
python scripts/update_vectorstore.py
```

## Tips

1. **Tên file rõ ràng**: Đặt tên file dễ hiểu, có dấu
   - ✅ `quy_che_dao_tao_2024.pdf`
   - ❌ `document1.pdf`

2. **Chất lượng OCR**: Nếu PDF là scan, đảm bảo đã OCR
   - Sử dụng Adobe Acrobat hoặc online tools để OCR

3. **Encoding**: File TXT nên dùng UTF-8 encoding

4. **Kích thước**: Không giới hạn số lượng file, nhưng:
   - Mỗi file nên < 50MB
   - Tổng < 1GB để tối ưu performance

5. **Cập nhật thường xuyên**: Khi có tài liệu mới, chạy update script







