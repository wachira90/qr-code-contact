# QR Code ใช้มาตรฐาน vCard 3.0 

**วิธีใช้งาน** แก้ข้อมูลในส่วน `contact = { ... }` ในไฟล์ Python:

```python
contact = {
    "name":    "ชื่อของคุณ",
    "name_en": "Your Name",
    "title":   "ตำแหน่ง",
    "company": "บริษัท",
    "phone":   "+66 8x xxx xxxx",
    "phone2":  "",          # ว่างได้
    "email":   "you@email.com",
    "website": "www.yoursite.com",
    "address": "ที่อยู่",
    "line_id": "@yourline",  # ว่างได้
}
```

แล้วรัน:
```bash
pip install qrcode[pil] pillow
python generate_qr_contact.py
```

**ไฟล์ที่ได้:**
- `business_card_qr.png` — นามบัตรพร้อม QR Code และข้อมูลติดต่อ
- `qr_contact_only.png` — QR Code อย่างเดียว ขนาดใหญ่ (สำหรับพิมพ์)

QR Code ใช้มาตรฐาน **vCard 3.0** — สแกนด้วยมือถือแล้วบันทึก Contact ได้เลย
