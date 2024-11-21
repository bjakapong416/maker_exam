import cv2 as cv
import numpy as np
from Myclassbot import Classbot  # Import Classbot จาก Myclassbot.py

# กำหนดข้อมูลภาพที่ต้องการประมวลผล
myduckdata = {
    'horizontal': 'M1.JPG',
    'vertical': 'M3.JPG',
}

# โหลดภาพต้นฉบับ (Main Image)
main_image_path = 'unwarped_IMG_7646.jpg'
main_image = cv.imread(main_image_path, cv.IMREAD_COLOR)
if main_image is None:
    raise ValueError(f"Error: Cannot load the main image: {main_image_path}")

# ปรับขนาดภาพต้นฉบับ
resize_width, resize_height = 1024, 900
main_image_resized = cv.resize(main_image, (resize_width, resize_height))

# สร้างตัวแปรเก็บเส้นแนวนอนและแนวตั้ง
horizontal_lines = []
vertical_lines = []

# เริ่มการประมวลผล
for name, pathimg in myduckdata.items():
    print(f"Processing {name}: {pathimg}")

    # โหลด Template และปรับขนาด
    template_image = cv.imread(pathimg, cv.IMREAD_COLOR)
    if template_image is None:
        raise ValueError(f"Error: Cannot load the template image: {pathimg}")
    
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

# แสดงผลลัพธ์
cv.imshow("Result", main_image_resized)

# รอให้ผู้ใช้กด 'q' เพื่อปิดหน้าต่าง
cv.waitKey(0)
cv.destroyAllWindows()
