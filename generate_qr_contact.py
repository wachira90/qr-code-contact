"""
generate_qr_contact.py
สร้าง QR Code นามบัตร (vCard) พร้อมข้อมูลติดต่อ
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# ===== กรอกข้อมูลนามบัตรที่นี่ =====
contact = {
    "name":       "สมชาย ใจดี",           # ชื่อ-นามสกุล
    "name_en":    "Somchai Jaidee",        # ชื่อภาษาอังกฤษ (สำหรับ vCard)
    "title":      "ผู้จัดการฝ่ายขาย",     # ตำแหน่ง
    "company":    "บริษัท ตัวอย่าง จำกัด",# บริษัท
    "phone":      "+66 81 234 5678",       # เบอร์โทรศัพท์
    "phone2":     "+66 02 123 4567",       # เบอร์โทรสำรอง (ว่างได้)
    "email":      "somchai@example.com",   # อีเมล
    "website":    "www.example.com",       # เว็บไซต์ (ว่างได้)
    "address":    "123 ถ.สุขุมวิท กรุงเทพฯ 10110",  # ที่อยู่
    "line_id":    "@somchai",              # LINE ID (ว่างได้)
}
# =====================================


def build_vcard(c: dict) -> str:
    """สร้าง vCard 3.0 string"""
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{c['name_en']}",
        f"N:{c['name_en'].split()[-1]};{' '.join(c['name_en'].split()[:-1])};;;",
        f"ORG:{c['company']}",
        f"TITLE:{c['title']}",
        f"TEL;TYPE=CELL:{c['phone']}",
    ]
    if c.get("phone2"):
        lines.append(f"TEL;TYPE=WORK:{c['phone2']}")
    lines.append(f"EMAIL:{c['email']}")
    if c.get("website"):
        lines.append(f"URL:{c['website']}")
    if c.get("address"):
        lines.append(f"ADR;TYPE=WORK:;;{c['address']};;;;")
    if c.get("line_id"):
        lines.append(f"X-SOCIALPROFILE;type=line:{c['line_id']}")
    lines.append("END:VCARD")
    return "\n".join(lines)


def generate_qr(vcard_text: str, size: int = 400) -> Image.Image:
    """สร้าง QR Code จาก vCard text"""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High — 30% recovery
        box_size=10,
        border=2,
    )
    qr.add_data(vcard_text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1a1a2e", back_color="white")
    return img.resize((size, size), Image.LANCZOS)


def make_business_card(c: dict, output_path: str = "business_card_qr.png"):
    """สร้างนามบัตรพร้อม QR Code"""

    # ขนาดนามบัตร (3.5 × 2 นิ้ว @ 200 dpi)
    W, H = 700, 400
    QR_SIZE = 280
    PADDING = 28

    card = Image.new("RGB", (W, H), color="#1a1a2e")
    draw = ImageDraw.Draw(card)

    # --- แถบสีด้านซ้าย ---
    draw.rectangle([0, 0, 8, H], fill="#e94560")

    # --- QR Code (ขวา) ---
    vcard = build_vcard(c)
    qr_img = generate_qr(vcard, QR_SIZE)

    # วาง QR บนพื้นขาวเล็กน้อย
    qr_x = W - QR_SIZE - PADDING
    qr_y = (H - QR_SIZE) // 2
    white_bg = Image.new("RGB", (QR_SIZE + 16, QR_SIZE + 16), "white")
    card.paste(white_bg, (qr_x - 8, qr_y - 8))
    card.paste(qr_img, (qr_x, qr_y))

    # --- ข้อความ (ซ้าย) ---
    try:
        font_lg  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        font_md  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_sm  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
        font_xs  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        font_lg = font_md = font_sm = font_xs = ImageFont.load_default()

    text_x = 28
    y = 42

    # ชื่อ
    draw.text((text_x, y), c["name"], font=font_lg, fill="#e94560")
    y += 38

    # ชื่อภาษาอังกฤษ (เล็กกว่า)
    draw.text((text_x, y), c["name_en"], font=font_md, fill="#aaaacc")
    y += 30

    # ตำแหน่ง
    draw.text((text_x, y), c["title"], font=font_md, fill="#ffffff")
    y += 26

    # บริษัท
    draw.text((text_x, y), c["company"], font=font_sm, fill="#ccccee")
    y += 36

    # เส้นคั่น
    draw.rectangle([text_x, y, qr_x - 24, y + 1], fill="#e94560")
    y += 14

    # ข้อมูลติดต่อ
    info_color = "#ddddff"
    icon_color = "#e94560"

    items = [
        ("📞", c["phone"]),
    ]
    if c.get("phone2"):
        items.append(("☎", c["phone2"]))
    items.append(("✉", c["email"]))
    if c.get("website"):
        items.append(("🌐", c["website"]))
    if c.get("line_id"):
        items.append(("LINE", c["line_id"]))
    if c.get("address"):
        items.append(("📍", c["address"]))

    for icon, val in items:
        draw.text((text_x, y), icon, font=font_xs, fill=icon_color)
        draw.text((text_x + 26, y), val, font=font_xs, fill=info_color)
        y += 22
        if y > H - 28:
            break

    # ข้อความ "Scan to save" ใต้ QR
    label = "Scan to save"
    bbox = draw.textbbox((0, 0), label, font=font_xs)
    lw = bbox[2] - bbox[0]
    draw.text((qr_x + (QR_SIZE - lw) // 2, qr_y + QR_SIZE + 10), label,
              font=font_xs, fill="#aaaacc")

    card.save(output_path, dpi=(200, 200))
    print(f"✅  บันทึกไฟล์: {output_path}")
    return output_path


def save_qr_only(c: dict, output_path: str = "qr_contact_only.png"):
    """บันทึก QR Code อย่างเดียว (ขนาดใหญ่ สำหรับพิมพ์)"""
    vcard = build_vcard(c)
    qr_img = generate_qr(vcard, 600)
    qr_img.save(output_path)
    print(f"✅  QR อย่างเดียว: {output_path}")
    return output_path


if __name__ == "__main__":
    make_business_card(contact, "/home/claude/business_card_qr.png")
    save_qr_only(contact,       "/home/claude/qr_contact_only.png")
    print("\nสแกน QR Code เพื่อบันทึกผู้ติดต่อในมือถือได้เลย 📱")
