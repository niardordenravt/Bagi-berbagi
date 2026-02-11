# Bagi-berbagi
Bersama membangun negeri

# Nge-SpriteSheet

Addon Blender untuk membuat sprite sheet dari image sequence dengan grid otomatis atau custom.

Cocok untuk:
- Roblox VFX
- Unity / Unreal
- Game 2D
- Stylized combat effects
- Asset pipeline real-time

---

## Fitur

- Auto Quadratic Grid (otomatis hitung grid dari jumlah gambar)
- Custom Rows & Columns
- Auto sort berdasarkan nama file
- Export PNG otomatis
- Nama file output mengikuti nama folder

---


## Target Penggunaan

Addon ini dibuat untuk mempermudah pipeline VFX dan sprite animation di game engine.

Sangat cocok untuk:
- Smoke
- Fire
- Explosion
- Magic FX
- Stylized effect

---

## Cara Pakai

1. Install addon:
   - Edit > Preferences > Add-ons > Install
   - Pilih `Nge-SpriteSheet.py`
   - Centang untuk aktifkan

2. Buka:
   - View3D > Sidebar (N) > Tab "Nge-SpriteSheet"

3. Klik **Pick Image Sequence**
4. Pilih semua frame (contoh: Smoke_0000 – Smoke_0015)
5. Pilih mode:
   - Centang **Quadratic** untuk auto grid
   - Atau matikan dan isi Rows & Columns manual
6. Klik **Build Sprite Sheet**

File akan tersimpan di folder yang sama dengan format <Nama Folder>_Spritesheet

---

## 🧠 Dibuat Oleh

Run-D

Jika addon ini membantu workflow kamu, feel free untuk share atau kasih feedback, donasi ke [QRIS](https://github.com/user-attachments/assets/3ae5db0d-159d-4b67-b417-222899391426) juga bole dan makasih banget 🙌





---QUICKTIPS---

##  Rekomendasi Ukuran

Disarankan:
- 512x512 per frame
- 4x4 grid → hasil akhir 2048x2048 (2K)

Kenapa?

Karena:
- Lebih ringan untuk real-time engine
- Cocok untuk Roblox & mobile
- Tidak terlalu berat di GPU

Contoh:
- 16 frame 512px → 4x4 → 2K spritesheet
- 16 frame 1024px → 4x4 → 4K spritesheet
- 16 frame 2048px → 4x4 → God Bless Indonesia

Gunakan ukuran sesuai kebutuhan project dan kapabilitas hardware.

---

## Catatan

Mode Quadratic membutuhkan jumlah gambar perfect square:
- 4
- 9
- 16
- 25
- dst

Jika tidak, gunakan mode custom Rows & Columns.

---
