import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import qrcode
import io
import os

# Uygulama penceresi
root = tk.Tk()
root.title("QR Kodu Oluşturucu")
root.geometry("400x550")
root.config(bg="#1e1e2f")
root.resizable(False, False)

# Başlık etiketi
title_label = tk.Label(root, text="Linkten QR Kodu Oluştur", font=("Helvetica", 16, "bold"), bg="#1e1e2f", fg="white")
title_label.pack(pady=20)

# Giriş alanı
entry = tk.Entry(root, width=40, font=("Helvetica", 12))
entry.pack(pady=10)

# Görsel alanı
qr_label = tk.Label(root, bg="#1e1e2f")
qr_label.pack(pady=20)

# Global QR image değişkeni
current_qr_img = None

# QR kod üretim fonksiyonu
def generate_qr():
    global current_qr_img
    link = entry.get()
    if not link:
        messagebox.showerror("Hata", "Lütfen bir bağlantı girin!")
        return
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    current_qr_img = img  # Kaydetme için referans

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    pil_img = Image.open(buffer).resize((200, 200))
    tk_img = ImageTk.PhotoImage(pil_img)
    qr_label.config(image=tk_img)
    qr_label.image = tk_img

# QR kodu kaydetme fonksiyonu
def save_qr():
    global current_qr_img
    if current_qr_img is None:
        messagebox.showwarning("Uyarı", "Önce bir QR kodu oluşturun.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                             filetypes=[("JPEG dosyası", "*.jpg")],
                                             title="QR kodu kaydet",
                                             initialfile="qr_kod.jpg")
    if file_path:
        current_qr_img.save(file_path, format="JPEG")
        messagebox.showinfo("Başarılı", f"QR kodu başarıyla kaydedildi:\n{file_path}")

# QR oluşturma butonu
generate_button = tk.Button(root, text="QR Kod Oluştur", command=generate_qr,
                            font=("Helvetica", 12, "bold"), bg="#4caf50", fg="white", padx=10, pady=5)
generate_button.pack(pady=10)

# QR kaydetme butonu
save_button = tk.Button(root, text="QR Kod JPG Olarak Kaydet", command=save_qr,
                        font=("Helvetica", 12, "bold"), bg="#2196f3", fg="white", padx=10, pady=5)
save_button.pack(pady=5)

# Alt etiket
footer_label = tk.Label(root, text="Created by Enes Burak Polat - QR Code", font=("Helvetica", 9), bg="#1e1e2f", fg="#999")
footer_label.pack(side="bottom", pady=10)

# Uygulama döngüsü
root.mainloop()
