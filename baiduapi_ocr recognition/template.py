import glob
from os import path
import os
from aip import AipOcr
from PIL import Image
def convertimg(picfile, outdir):
    '''调整图片大小，对于过大的图片进行压缩
    picfile:    图片路径
    outdir：    图片输出路径
    '''
    img = Image.open(picfile)
    width, height = img.size
    while(width*height > 4000000):  # 该数值压缩后的图片大约 两百多k
        width = width // 2
        height = height // 2
    new_img=img.resize((width, height),Image.BILINEAR)
    new_img.save(path.join(outdir,os.path.basename(picfile)))
def baiduOCR(picfile, outfile):
    """利用百度api识别文本，并保存提取的文字
    picfile:    图片文件名
    outfile:    输出文件
    """
    filename = path.basename(picfile)
    
    APP_ID = '20334748' # 刚才获取的 ID，下同
    API_KEY = 'fNgrhvgNBN8FZlHAGtbgUZHM'
    SECRECT_KEY = 'd96sIFy0ylQM66rXLnWthH7p8fcXeUw6'
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
    
    i = open(picfile, 'rb')
    img = i.read()
    print("正在识别图片：\t" + filename)
    message = client.basicGeneral(img)   # 通用文字识别，每天 50 000 次免费
    #message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费
    print("识别成功！")
    i.close();
    print(message.get('words_result'))
    print(message.get('words_result')[1].get('words'))
    with open(outfile, 'a+') as fo:
        fo.writelines("+" * 60 + '\n')
        fo.writelines("识别图片：\t" + filename + "\n" * 2)
        fo.writelines("文本内容：\n")
        # 输出文本内容
        for text in message.get('words_result'):
            fo.writelines(text.get('words') + '\n')
        fo.writelines('\n'*2)
    print("文本导出成功！")
    print()

if __name__=='__main__':
    outdir = 'tmp'
    outfile='out.txt.'
    if path.exists(outfile):
        os.remove(outfile)
    if not path.exists(outdir):
        os.mkdir(outdir)
   
    for picfile in glob.glob("picture/*"):
        convertimg(picfile,outdir)
    for picfile in glob.glob("tmp/*"):
        
        baiduOCR(picfile,outfile)
    print('图片文本提取结束！文本输出结果位于 %s 文件中。' % outfile)
    os.removedirs(outdir)
