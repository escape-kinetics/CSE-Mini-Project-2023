import tkinter as tk
from tkinter import messagebox
import time
from PIL import Image, ImageTk
import pandas as pd
import webbrowser
import os
import csv

pd.set_option('display.max_columns', None)
root=tk.Tk()
def background():
    global photo_img
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}')
    img = Image.open('background.jpg')
    img = img.resize((screen_width, screen_height))
    photo_img = ImageTk.PhotoImage(img)
    background_label = tk.Label(root, image=photo_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
background()

def dateandtime_update():
    current_time = time.strftime('%H:%M:%S')
    current_date = time.strftime('%Y-%m-%d')
    label_time.config(text=current_time)
    label_date.config(text=current_date)
    root.after(1000,dateandtime_update)
label_time = tk.Label(root, font=("Segoe UI", 10), bg='#90e0fd')
label_time.pack(anchor='nw')
label_date = tk.Label(root, font=("Segoe UI", 10), bg='#90e0fd')
label_date.pack(anchor='nw')
dateandtime_update()





def search_csv(name, file_path="A_Z_medicines_dataset_of_India.csv"):
    if not os.path.exists(file_path):
        return "File does not exist."
    
    result_dict = {}
    if len(name) >= 3:
        # Use pandas to read the CSV file into a DataFrame
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # Use csv module's DictReader to convert DataFrame to a list of dictionaries
        data = list(csv.DictReader(df.to_csv(index=False).splitlines()))
        
        for row in data:
            if name.lower() in row['name'].lower() or \
               name.lower() in row['short_composition1'].lower() or \
               name.lower() in row['short_composition2'].lower():
                result_dict = row
                if result_dict.get('Is_discontinued') == 'TRUE':
                    messagebox.showinfo("Notice", "This medicine is discontinued.")
                break
        if not result_dict:
            return "Not found"
        else:
            return result_dict
    else:
        return '0'




def display_output():
    medicine_name = entry_box_drug.get()
    result = search_csv(medicine_name)
    if result == "Not found":
        result_text_widget.insert(tk.END, "Medicine not found please enter the exact name to recieve appropriate result\n------\n")
    elif result=='0':
        result_text_widget.insert(tk.END, "Enter more than 3 letters to help the engine search more accurately\n------\n")
    elif isinstance(result, dict):
        result_text = ""
        for key, value in result.items():
            if key.lower() == 'price' and isinstance(value, (int, float)):
                value = f'₹ {value}'
            result_text += f"{key}: {value}\n"
        result_text += "-----------------------------\n\n"
        result_text_widget.insert(tk.END, result_text)

medicine_list=[]
def add_to_list():
    medicine_name = entry_box_drug.get()
    result = search_csv(medicine_name)
    if result == "Not found":
        messagebox.showinfo("Error", "Medicine not found")
    else:
        
        medicine_to_add = {key: result[key] for key in ['name', 'short_composition1', 'short_composition2']}
        for medicine in medicine_list:
            if medicine['name'] == medicine_to_add['name']:
                messagebox.showinfo("Success", "Medicine already in the list")
                return
        medicine_list.append(medicine_to_add)
        messagebox.showinfo("Success", "Medicine added to list")

def display_list():
    new_window = tk.Toplevel(root)
    new_window.title("Medicine List")
    

    list_frame = tk.Frame(new_window)
    list_frame.pack(anchor='w')

    
    def clear_list():
        for widget in list_frame.winfo_children():
            widget.destroy()

   
    clear_button = tk.Button(new_window, text="Clear", command=clear_list)
    clear_button.pack(anchor='w')

   
    for medicine in medicine_list:
        for key, value in medicine.items():
          
            label = tk.Label(list_frame, text=f"{key}: {value}")
            label.pack(anchor='w')
        
        
        separator = tk.Label(list_frame, text="----------------")
        separator.pack(anchor='w')

def open_browser():
    base_url = "https://www.1mg.com/search/all?name="
    search_term = entry_box_drug.get()
    url = base_url + search_term
    webbrowser.open(url)
def clear_text():
    result_text_widget.delete(1.0, tk.END)

text_widget = tk.Text(root)


# Create a frame for the entry box and the buttons
frame = tk.Frame(root)
frame.pack()





frame = tk.Frame(root)
frame.pack(anchor='center')

drug_search_label = tk.Label(frame, text="Drug Search", font=("Segoe UI", 50), bg='#c7eefd')
drug_search_label.pack()
entry_box_drug= tk.Entry(frame, font=("Segoe UI", 10))
entry_box_drug.pack()

search_button = tk.Button(frame, text="Search", command=display_output)
search_button.pack(side='left')

online_store_button = tk.Button(frame, text="Search online store", command=open_browser)
online_store_button.pack(side='left')

add_button = tk.Button(frame, text="Add to list", command=add_to_list)
add_button.pack(side='left')

displaylist_button=tk.Button(frame,text="Display list",command=display_list)
displaylist_button.pack(side='left')

result_text_widget = tk.Text(root)
result_text_widget.pack(anchor='center')

clear_button = tk.Button(root, text="Clear", command=clear_text)
clear_button.pack(anchor='center')



def open_info_window():
    info_window = tk.Toplevel(root)
    info_window.title("Why Trust Our Search Engine?")
    
    info_text = """
    Why Trust Our Search Engine?

    1. Reliable Information: We ensure accuracy in our drug search engine, providing trustworthy details about generic drugs.
    2. Up-to-Date Data: Our platform is regularly updated, offering the latest information on generic drugs.
    3.User-Friendly Interface: Our drug search engine is designed to be intuitive and easy to navigate, making information readily accessible.
    4.Transparency: We believe in clear and concise presentation of drug information, fostering trust with our users.
    5.Comprehensive Database: Our wide-ranging database provides a detailed overview of each medication, making us a one-stop solution for drug-related queries.
    6.Privacy Commitment: We respect your privacy. Your search queries and personal information are kept confidential.
    7.Informed Decision-Making: Our platform empowers you with critical drug-related insights, facilitating informed decisions. Whether you're a healthcare professional or an individual exploring options, we're here to help.
    """
    
    info_label = tk.Label(info_window, text=info_text, justify=tk.LEFT)
    info_label.pack()


info_button = tk.Button(root, text="ⓘ", command=open_info_window)
info_button.pack(anchor='s')
root.mainloop()
