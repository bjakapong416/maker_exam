import cv2 as cv
import numpy as np
import os  # สำหรับการจัดการไฟล์และโฟลเดอร์
from Myclassbot import Classbot  # Import Classbot จาก Myclassbot.py

# กำหนดพาธโฟลเดอร์
input_folder = 'unwarped'  # โฟลเดอร์ที่เก็บภาพต้นฉบับ
template_folder = 'template'  # โฟลเดอร์ที่เก็บ Template
output_folder = 'results'  # โฟลเดอร์สำหรับบันทึกผลลัพธ์

# สร้างโฟลเดอร์สำหรับบันทึกผลลัพธ์หากยังไม่มี
os.makedirs(output_folder, exist_ok=True)

# โหลด Template (แนวนอนและแนวตั้ง)
templates = {
    'horizontal': os.path.join(template_folder, 'M1.JPG'),
    'vertical': os.path.join(template_folder, 'M3.JPG'),
}

# อ่านไฟล์ทั้งหมดในโฟลเดอร์ภาพต้นฉบับ
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.png'))]

# ประมวลผลแต่ละภาพในโฟลเดอร์
for image_file in image_files:
    print(f"Processing image: {image_file}")  # อ่านภาพทีละภาพ
    image_path = os.path.join(input_folder, image_file)

    # โหลดภาพต้นฉบับ
    main_image = cv.imread(image_path, cv.IMREAD_COLOR)
    if main_image is None:
        print(f"Error: Cannot load the image: {image_path}")
        continue

    # ปรับขนาดภาพต้นฉบับ
    resize_width, resize_height = 1024, 900
    main_image_resized = cv.resize(main_image, (resize_width, resize_height))

    # สร้างตัวแปรเก็บเส้นแนวนอนและแนวตั้ง
    horizontal_lines = []
    vertical_lines = []

    # เริ่มการประมวลผล Template ทั้งสองประเภท
    for name, pathimg in templates.items():
        print(f"Using template: {pathimg}")

        # โหลด Template
        template_image = cv.imread(pathimg, cv.IMREAD_COLOR)
        if template_image is None:
            print(f"Error: Cannot load the template image: {pathimg}")
            continue

        # ทดลองจับคู่หลายขนาด
        for scale in np.linspace(0.8, 1.2, 10):  # ทดลองปรับ Template หลายขนาด
            template_resized = cv.resize(template_image, (0, 0), fx=scale, fy=scale)

            # เรียกใช้ Classbot
            search = Classbot(main_image_resized, template_resized)
            points = search.search(debug=False, mytxt=name, threshold=0.7)  # ไม่ใช้ putText

            # เก็บเส้นแนวนอนหรือแนวตั้ง
            if points:
                print(f"Points found for {name}: {points}")
                if name == "horizontal":
                    for point in points:
                        # วาดเส้นแนวนอน
                        cv.line(main_image_resized, (0, point[1]), (resize_width, point[1]), (255, 0, 0), 1)
                        horizontal_lines.append(point[1])  # เก็บตำแหน่ง y
                elif name == "vertical":
                    for point in points:
                        # วาดเส้นแนวตั้ง
                        cv.line(main_image_resized, (point[0], 0), (point[0], resize_height), (0, 255, 0), 1)
                        vertical_lines.append(point[0])  # เก็บตำแหน่ง x
                break  # ออกจากการวนลูปเมื่อพบผลลัพธ์
            else:
                print(f"No matches found for scale {scale}")

    # หาและแสดงจุดตัด
    for x in vertical_lines:
        for y in horizontal_lines:
            # วาดจุดตัด
            cv.circle(main_image_resized, (x, y), 5, (0, 0, 255), -1)

    # บันทึกผลลัพธ์
    output_path = os.path.join(output_folder, f"result_{image_file}")
    cv.imwrite(output_path, main_image_resized)
    print(f"Result saved to: {output_path}")

# เสร็จสิ้น
print("Processing completed!")
