try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def convert_img(img,threshold):
    img = img.convert("L")  # 处理灰度
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0

    data = img.getdata()
    w, h = img.size
    count = 0
    for x in range(1, h - 1):
        for y in range(1, h - 1):
            # 找出各个像素方向
            mid_pixel = data[w * y + x]
            if mid_pixel == 0:
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]

                if top_pixel == 0:
                    count += 1
                if left_pixel == 0:
                    count += 1
                if down_pixel == 0:
                    count += 1
                if right_pixel == 0:
                    count += 1
                if count > 4:
                    img.putpixel((x, y), 0)
    return img
captcha = Image.open("640 (2).webp")
captcha=captcha.convert('RGB')
result = captcha.convert('L')
threshold=180
a=convert_img(result,threshold)



result = pytesseract.image_to_string(a)
print(result)

