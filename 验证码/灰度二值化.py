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
    return img
captcha = Image.open("640 (1).webp")
captcha=captcha.convert('RGB')
result = captcha.convert('L')
threshold=180
a=convert_img(result,threshold)



result = pytesseract.image_to_string(a)
print(result)

