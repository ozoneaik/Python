import cv2
import pytesseract
import re
import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Rest of your code here...
month_mapping = {
    "Jan": "ม.ค.","Feb": "ก.พ.","Mar": "มี.ค.","Apr": "เม.ย.","May": "พ.ค.","Jun": "มิ.ย.",
    "Jul": "ก.ค.","Aug": "ส.ค.","Sep": "ก.ย.","Oct": "ต.ค.","Nov": "พ.ย.","Dec": "ธ.ค."
}

# Create a function to process the uploaded image and display the data
def process_image():
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename()
    
    if file_path:


        img = cv2.imread(file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Rest of your image processing code here...

        month_mapping = {
            "Jan": "ม.ค.","Feb": "ก.พ.","Mar": "มี.ค.","Apr": "เม.ย.","May": "พ.ค.","Jun": "มิ.ย.",
            "Jul": "ก.ค.","Aug": "ส.ค.","Sep": "ก.ย.","Oct": "ต.ค.","Nov": "พ.ย.","Dec": "ธ.ค."
        }
        path=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = path
        def show(img):
            cv2.imshow(file_path, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        def sort_zip(var1, var2):
            sorted_pairs = sorted(zip(var1, var2), key=lambda pair: pair[0])
            var3 = [pair[1] for pair in sorted_pairs]
            return var3
        
        def findID(datas):   
            integer = ['0','1','2','3','4','5','6','7','8','9', ' ']
            for data in datas:
                data = data.replace('\n', '')
                if all(char in integer for char in ''.join(data)) and len(data) > 0:
                    return data
            return 'Detection Identification is failed'

        def findName(datas, mode = ''):
            fullName = []
            for i,data in enumerate(datas):
                data = data.replace('\n', '')
                data = data.replace(' ', '')
                if mode == 'th':
                    if data == 'ชื่อตัวและชื่อสกุล':
                        if i != len(datas)-1:
                            new_data = datas[i+1]
                            new_data = new_data.replace('\n', '')
                            new_data = new_data.split(' ')
                            return new_data
                else: 
                    if data == 'Name' or data == 'LastName':
                        if i != len(datas)-1:
                            name = datas[i+1]
                            name = name.replace('\n','')
                            name = name.split(' ')
                            for i in name: 
                                fullName.append(i)
                            if len(fullName) == 3:
                                return fullName
            return 'Detection Name is failed'
        
        def findBirthDay(datas, mode = ''): 
            for i,data in enumerate(datas): 
                data = data.replace('\n', '')
                if data == 'Date of Birth':
                    if i != len(datas)-1:
                        if mode == 'en':
                            return datas[i+1].replace('\n','')
                        else :
                            date = datas[i+1].split(' ')
                            thai_date = f'{date[0]} {month_mapping.get(date[1], "Unknown")} {int(date[2])+543}'
                            return thai_date
            return 'Detection Date of Birht is failed'
        
        def findaddress(dates):
            key = 'ที่อยู่'
            for i,data in enumerate(dates):
                if key in data:
                    return data.replace('\n','')
            return 'Detection address is failed'

        def findDate(dates, key= '', mode = ''):
            for i,data in enumerate(dates):
                if key in data:
                    date_pattern = r'\d{1,2} [A-Za-z]{3} \d{4}'
                    date = re.findall(date_pattern, data)
                    if mode == 'en':
                        return date[0]
                    if mode == 'th':
                        dateTH = date[0]
                        dateTH = dateTH.split(' ')
                        return f'{dateTH[0]} {month_mapping.get(dateTH[1], "Unknown")} {int(dateTH[2])+543}'
            return f'Detection Data of {key} is failed'
        
        def findMaker(datas):
            key = 'เจ้าพนักงานออกบัตร'
            for i,data in enumerate(datas):
                if key in data:
                    makerName = data.split('\n')
                    makerName = makerName[0].replace('(','')
                    makerName = makerName.replace(')','')
                    return makerName
            return f'Detection Maker Name is failed'
        
        img = cv2.imread(file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        print(h,w)
        gray_resize = cv2.resize(gray, (int(w*3), int(h*3)))
        k_size = (3, 3)
        sigma_x = 0
        blur = cv2.GaussianBlur(gray_resize, k_size, sigma_x)  # Apply Gaussian blur to the grayscale image
        ret, thresh1 = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 15))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        im2 = gray_resize.copy()
        rect = None
        x_ = []
        y_=[]
        w_ =[]
        h_=[]
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            x_.append(x)
            y_.append(y)
            w_.append(w)
            h_.append(h)
        x_ = sort_zip(y_, x_)
        w_ = sort_zip(y_, w_)
        h_ = sort_zip(y_, h_)
        y_.sort()
        for i in range(len(x_)-1):
            if x_[i] > x_[i+1] and y_[i] < y_[i+1] and  y_[i+1] - y_[i] < 10 :
                tempx = x_[i]
                tempy = y_[i]
                temph = h_[i]
                tempw = w_[i]
                x_[i] = x_[i+1]
                y_[i]= y_[i+1]
                h_[i]= h_[i+1]
                w_[i]= w_[i+1]
                x_[i+1] = tempx
                y_[i+1]= tempy
                h_[i+1]= temph
                w_[i+1]= tempw
        data_thai = []
        data_en = []
        for i in range(len(x_)):
            im2 = cv2.rectangle(im2, (x_[i], y_[i]), (x_[i] + w_[i], y_[i] + h_[i]), (0, 255, 0), 2)
            # show(im2)
            cropped = thresh1[y_[i]:y_[i]+h_[i], x_[i]:x_[i]+w_[i]]
            h, w = cropped.shape
            cropped = cv2.resize(cropped, (int(w*2), int(h*2)))
            # show(cropped)
            thai = pytesseract.image_to_string(cropped, lang='tha')
            en = pytesseract.image_to_string(cropped, lang='eng')
            if thai != '' and thai != '\n':
                data_thai.append(thai)
            if en != '' and en != '\n' :
                data_en.append(en)

        show(im2)
        idCard = findID(data_thai)
        nameTH = findName(data_thai, mode = 'th')
        nameEN = findName(data_en, mode = 'en')
        birthDayTH = findBirthDay(data_en, mode = 'th')
        birthDayEN = findBirthDay(data_en, mode = 'en')
        address = findaddress(data_thai)
        dateOfIssueEN = findDate(data_en, key= 'Date of Issue' , mode = 'en')
        dateOfIssueTH = findDate(data_en, key= 'Date of Issue' , mode = 'th')
        dateOfExpiryEN = findDate(data_en, key= 'Date of Expiry',mode = 'en')
        dateOfExpiryTH = findDate(data_en, key= 'Date of Expiry',mode = 'th')
        makerName = findMaker(data_thai)

        profile = {
            'idCard' : idCard,
            'nameTH':{
                'namePrefix': nameTH[0],
                'firstName': nameTH[1],
                'lastName': nameTH[2] 
            },
            'nameEN':{
                'namePrefix': nameEN[0],
                'firstName': nameEN[1],
                'lastName': nameEN[2] 
            },
            'brithdayTH': birthDayTH,
            'brithdayEN' :birthDayEN,
            'address' : address,
            'dateOfIssueTH':dateOfIssueTH,
            'dateOfIssueEN' : dateOfIssueEN,
            'dateOfExpiryTH':dateOfExpiryTH,
            'dateOfExpiryEN':dateOfExpiryEN,
            'MakerName' : makerName
        }
        json_profile = json.dumps(profile, ensure_ascii=False)
        # print(json_profile)

        print(idCard)
        print(nameTH)
        print(nameEN)
        print(birthDayTH)
        print(birthDayEN)
        print(address)
        print(dateOfIssueTH)
        print(dateOfExpiryTH)
        print(dateOfIssueEN)
        print(dateOfExpiryEN)
        print('เจ้าพนักงานออกบัตร : '+makerName)

        # Update the labels with extracted data
        idCard_label.config(text=f'รหัสบัตรประจำตัว : {idCard}')
        nameTH_label.config(text=f'ชื่อ (ภาษาไทย): {" ".join(nameTH)}')
        nameEN_label.config(text=f'ชื่อ (ภาษาอังกฤษ): {" ".join(nameEN)}')
        birthDayTH_label.config(text=f'วันเดือนปีเกิด (ภาษาไทย): {birthDayTH}')
        birthDayEN_label.config(text=f'วันเดือนปีเกิด (ภาษาอังกฤษ): {birthDayEN}')
        address_label.config(text=f'ที่อยู่ : {address}')
        dateOfIssueTH_label.config(text=f'วันออกบัตร (ภาษาไทย): {dateOfIssueTH}')
        dateOfIssueEN_label.config(text=f'วันออกบัตร (ภาษาอังกฤษ): {dateOfIssueEN}')
        dateOfExpiryTH_label.config(text=f'วันบัตรหมดอายุ (ภาษาไทย): {dateOfExpiryTH}')
        dateOfExpiryEN_label.config(text=f'วันบัตรหมดอายุ (ภาษาไทย): {dateOfExpiryEN}')
        makerName_label.config(text=f'เจ้าพนักงานออกบัตร: {makerName}')

# Create a Tkinter window
window = tk.Tk()
window.title("ID Card Data Extraction")
window.geometry("500x500")
label_font = ("Helvetica", 36) 

# Create a button to upload an image
upload_button = tk.Button(window, text="Upload Image", command=process_image)
upload_button.pack()

# Create labels to display the extracted data
# Create labels to display titles on the left with font size 24
label_font = ("Helvetica", 16)  # Define the font

idCard_label = tk.Label(window, text="รหัสบัตรประจำตัว :", font=label_font, anchor="w")
idCard_label.pack(fill="x")  # Use fill to stretch the label horizontally

nameTH_label = tk.Label(window, text="ชื่อ (ภาษาไทย):", font=label_font, anchor="w")
nameTH_label.pack(fill="x")

nameEN_label = tk.Label(window, text="ชื่อ (ภาษาอังกฤษ):", font=label_font, anchor="w")
nameEN_label.pack(fill="x")

birthDayTH_label = tk.Label(window, text="วันเดือนปีเกิด (ภาษาไทย):", font=label_font, anchor="w")
birthDayTH_label.pack(fill="x")

birthDayEN_label = tk.Label(window, text="วันเดือนปีเกิด (ภาษาอังกฤษ):", font=label_font, anchor="w")
birthDayEN_label.pack(fill="x")

address_label = tk.Label(window, text="ที่อยู่ :", font=label_font, anchor="w")
address_label.pack(fill="x")

dateOfIssueTH_label = tk.Label(window, text="วันออกบัตร (ภาษาไทย):", font=label_font, anchor="w")
dateOfIssueTH_label.pack(fill="x")

dateOfIssueEN_label = tk.Label(window, text="วันออกบัตร (ภาษาอังกฤษ):", font=label_font, anchor="w")
dateOfIssueEN_label.pack(fill="x")

dateOfExpiryTH_label = tk.Label(window, text="วันบัตรหมดอายุ (ภาษาไทย):", font=label_font, anchor="w")
dateOfExpiryTH_label.pack(fill="x")

dateOfExpiryEN_label = tk.Label(window, text="วันบัตรหมดอายุ (ภาษาไทย):", font=label_font, anchor="w")
dateOfExpiryEN_label.pack(fill="x")

makerName_label = tk.Label(window, text="เจ้าพนักงานออกบัตร:", font=label_font, anchor="w")
makerName_label.pack(fill="x")







window.mainloop()
