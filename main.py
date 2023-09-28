import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import convertText as ct
import threading
import time

# custom_font = ("Arial", 16, "bold")
# custom_font = ("Helvetica", 12, "italic")
# custom_font = ("Times New Roman", 14)

def tk_start():
    for widget in root.winfo_children():
        widget.destroy()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1600
    window_height = 800
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate - 100))

# def run_ocr():
#     file_path = filedialog.askopenfilename(title="Open File", filetypes=[("All files", ".")])
#     if file_path:
#         # Disable the Open File button while OCR is running
#         open_file_button.config(state=tk.DISABLED)
#         def ocr_task(): 
#             try:
#                 profile = ct.start(path=file_path)
#                 update_ui(profile)
#             except Exception as e:
#                 update_ui(f"Error: {str(e)}")
#             finally:
#                 # Re-enable the Open File button when OCR is done
#                 open_file_button.config(state=tk.NORMAL)

#         ocr_thread = threading.Thread(target=ocr_task)
#         ocr_thread.start()

def run_ocr():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Disable the Open File button while OCR is running
        open_file_button.config(state=tk.DISABLED)

        def ocr_task():
            try:
                

                profile = ct.start(path=file_path)
                for step in range(101):
                    time.sleep(0.01)  # Simulate some work being done
                    progress_var.set(step)  

                update_ui(profile)
            except Exception as e:
                update_ui(f"Error: {str(e)}")
            finally:
                # Re-enable the Open File button when OCR is done
                open_file_button.config(state=tk.NORMAL)

        ocr_thread = threading.Thread(target=ocr_task)
        ocr_thread.start()

def update_ui(profile):
    custom_font = ("Times New Roman", 30)
    if isinstance(profile, list):
        label1.config(text=f"รหัสประจำตัวประชาชน : {profile[0]}", font=custom_font)
        label2.config(text=f"ชื่อ : {profile[1][0]} {profile[1][1]}", font=custom_font)
        label3.config(text=f"นามสกุล : {profile[1][2]}", font=custom_font)
        label4.config(text=f"Name : {profile[2][0]} {profile[2][1]}", font=custom_font)
        label5.config(text=f"Last Name : {profile[2][2]}", font=custom_font)
        label6.config(text=f"เกิดเมื่อวันที่ : {profile[3]}", font=custom_font)
        label7.config(text=f"Date of Birth : {profile[4]}", font=custom_font)
        label8.config(text=f"ที่อยู่ : {profile[5]}", font=custom_font)
        label9.config(text=f"ออกบัตรเมื่อวันที่ : {profile[6]}", font=custom_font)
        label10.config(text=f"Date of Issue : {profile[7]}", font=custom_font)
        label11.config(text=f"วันบัตรหมดอายุ : {profile[8]}", font=custom_font)
        label12.config(text=f"Date of Expiry : {profile[9]}", font=custom_font)
        label13.config(text=f"เจ้าพนักงานออกบัตร : {profile[10]}", font=custom_font)
    else:
        file_label.config(text=f"Error: {profile}")

root = tk.Tk()
root.title("Identification Card")

tk_start()

# Create buttons to open file and folder dialogs
open_file_button = tk.Button(root, text="Open File", command=run_ocr)
open_file_button.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.pack(pady=10)

label1 = tk.Label(root, text="")
label1.pack()
label2 = tk.Label(root, text="")
label2.pack()
label3 = tk.Label(root, text="")
label3.pack()
label4 = tk.Label(root, text="")
label4.pack()
label5 = tk.Label(root, text="")
label5.pack()
label6 = tk.Label(root, text="")
label6.pack()
label7 = tk.Label(root, text="")
label7.pack()
label8 = tk.Label(root, text="")
label8.pack()
label9 = tk.Label(root, text="")
label9.pack()
label10 = tk.Label(root, text="")
label10.pack()
label11 = tk.Label(root, text="")
label11.pack()
label12 = tk.Label(root, text="")
label12.pack()
label13 = tk.Label(root, text="")
label13.pack()

# Create labels to display selected file and folder paths
file_label = tk.Label(root, text="")
file_label.pack()

root.mainloop()