import os
import tkinter as tk
from tkinter import filedialog
from visualize import wordcloud
from update import update
from get import get
import pandas as pd
import ttkbootstrap as ttk


def process_input():
    start_id = entry_start_id.get()
    end_id = entry_end_id.get()
    selected_model = combobox.get()
    data_output_path = entry_data_output.get()
    pic_output_path = entry_pic_output_0.get()
    print("data_out_path:", data_output_path)
    print("pic_out_path:", pic_output_path)
    if os.path.isdir(data_output_path):
        # path is a directory
        data_output_path = os.path.join(data_output_path, '元数据.xlsx')
        with open(data_output_path, 'w') as f:
            f.write('')

    print("选择的选项:", selected_model)
    
    get(data_output_path, selected_model, pic_output_path, int(start_id), int(end_id))


def visual():
    ds = start_date.entry.get()
    de = end_date.entry.get()
    print(ds, de)
    input_path = entry_data_input.get()
    list_ouput_path = entry_list_output.get()
    list_ouput_path = os.path.join(list_ouput_path, '关键词.txt')
    outpath = entry_pic_output.get()
    outpath = os.path.join(outpath, '词云.png')
    print(input_path, outpath)
    stop_words = entry_cloud_stopword.get()
    stop_words = stop_words.split('，')
    stop_words = [item for sublist in stop_words for item in sublist.split(',')]
    stop_words = [item.strip() for item in stop_words]
    # read keywords from excel and only consider date between ds and de, the df['讲座时间']'s format is "2023年12月29日 16:20"
    df = pd.read_excel(input_path)
    # 将讲座时间转换为时间格式：YYYY/MM/DD
    df['讲座时间'] = pd.to_datetime(df['讲座时间'])
    df = df[(df['讲座时间'] >= ds) & (df['讲座时间'] <= de)]
    print(df)
    df = df['关键词']
    df = df.dropna()
    # save keywords to txt
    with open(list_ouput_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(df.tolist()))
    wordcloud(stop_words, "".join(df.tolist()), outpath)
    
    

# 按钮控件
def get_file(entry_text):
    path = filedialog.askopenfilename(title='请选择文件')
    entry_text.set(path)


def get_dic(entry_text):
    path = filedialog.askdirectory(title='请选择文件')
    entry_text.set(path)
 


if __name__ == "__main__":
    # 创建主窗口
    window = tk.Tk()
    style = ttk.Style()
    
    # 设置窗口标题
    window.title("图书馆海报分类系统")

    # 设置窗口大小
    window_width = 800
    window_height = 750
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    label = tk.Label(window, text="学术讲座海报资源管理系统", font=("宋体 (正文)", 20))
    label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    # 添加标签和输入框
    label = tk.Label(window, text="元数据及海报:", font=("宋体 (正文)", 16))
    label.grid(row=1, column=0, padx=10, pady=10)
    label = tk.Label(window, text="起始页码：")
    label.grid(row=1, column=1, padx=10, pady=10)
    entry_start_id = tk.Entry(window)
    entry_start_id.grid(row=1, column=2, padx=10, pady=10)
    label = tk.Label(window, text="终止页码：")
    label.grid(row=2, column=1, padx=10, pady=10)
    entry_end_id = tk.Entry(window)
    entry_end_id.grid(row=2, column=2, padx=10, pady=10)

    label = tk.Label(window, text="语言模型：")
    label.grid(row=4, column=1, padx=10, pady=10)
    options = ["chatGPT", "文心一言"]
    combobox = ttk.Combobox(window, values=options)
    combobox.current(0)  # 设置默认选项
    combobox.bind("<<ComboboxSelected>>")  # 绑定选项选择事件
    combobox.grid(row=4, column=2, padx=10, pady=10)

    label1 = tk.Label(window, text="元数据输出路径：")
    label1.grid(row=5, column=1, padx=10, pady=10)
    entry_text = tk.StringVar()
    entry_data_output = tk.Entry(window, textvariable=entry_text, font=('FangSong', 10))
    entry_data_output.grid(row=5, column=2, padx=10, pady=10)
    button_data_output = tk.Button(window, text='选择路径', command=lambda: get_dic(entry_text=entry_text))
    button_data_output.grid(row=5, column=3, padx=10, pady=10)

    label1 = tk.Label(window, text="海报图片输出路径：")
    label1.grid(row=6, column=1, padx=10, pady=10)
    entry_text1 = tk.StringVar()
    entry_pic_output_0 = tk.Entry(window, textvariable=entry_text1, font=('FangSong', 10))
    entry_pic_output_0.grid(row=6, column=2, padx=10, pady=10)
    button_data_output = tk.Button(window, text='选择路径', command=lambda: get_dic(entry_text=entry_text1))
    button_data_output.grid(row=6, column=3, padx=10, pady=10)

    button = tk.Button(window, text="导出", command=process_input)
    button.grid(row=7, column=1, columnspan=2, padx=10, pady=10)

    separator1 = ttk.Separator(window, orient='horizontal', style="blue.Horizontal.TSeparator")
    separator1.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

#######################################################################################################

    label1 = tk.Label(window, text="统计分析:", font=("宋体 (正文)", 16))
    label1.grid(row=9, column=0, padx=10, pady=10)

    label1 = tk.Label(window, text="起始日期:")
    label1.grid(row=9, column=1, padx=10, pady=10)
    start_date = ttk.DateEntry(window)
    start_date.grid(row=9, column=2, padx=10, pady=10)

    label1 = tk.Label(window, text="终止日期：")
    label1.grid(row=10, column=1, padx=10, pady=10)
    end_date = ttk.DateEntry(window)
    end_date.grid(row=10, column=2, padx=10, pady=10)

#######################################################################################################

    label1 = tk.Label(window, text="热点词:", font=("宋体 (正文)", 16))
    label1.grid(row=11, column=0, padx=10, pady=10)
    label1 = tk.Label(window, text="元数据输入路径：")
    label1.grid(row=11, column=1, padx=10, pady=10)
    entry_text2 = tk.StringVar()
    entry_data_input = tk.Entry(window, textvariable=entry_text2, font=('FangSong', 10))
    entry_data_input.grid(row=11, column=2, padx=10, pady=10)
    button_data_output = tk.Button(window, text='选择路径', command=lambda: get_file(entry_text=entry_text2))
    button_data_output.grid(row=11, column=3, padx=10, pady=10)

    label1 = tk.Label(window, text="热点词列表输出路径：")
    label1.grid(row=12, column=1, padx=10, pady=10)
    entry_text3 = tk.StringVar()
    entry_list_output = tk.Entry(window, textvariable=entry_text3, font=('FangSong', 10))
    entry_list_output.grid(row=12, column=2, padx=10, pady=10)
    button_data_output = tk.Button(window, text='选择路径', command=lambda: get_dic(entry_text=entry_text3))
    button_data_output.grid(row=12, column=3, padx=10, pady=10)

    label1 = tk.Label(window, text="词云图输出路径：")
    label1.grid(row=13, column=1, padx=10, pady=10)
    entry_text4 = tk.StringVar()
    entry_pic_output = tk.Entry(window, textvariable=entry_text4, font=('FangSong', 10))
    entry_pic_output.grid(row=13, column=2, padx=10, pady=10)
    button_data_output = tk.Button(window, text='选择路径', command=lambda: get_dic(entry_text=entry_text4))
    button_data_output.grid(row=13, column=3, padx=10, pady=10)

    label1 = tk.Label(window, text="添加停用词：（，分隔）")
    label1.grid(row=14, column=1, padx=10, pady=10)
    entry_cloud_stopword = tk.Entry(window)
    entry_cloud_stopword.grid(row=14, column=2, padx=10, pady=10)

    button = tk.Button(window, text="导出", command=visual)
    button.grid(row=15, column=1, columnspan=2, padx=10, pady=10)

    # 开启主循环
    window.mainloop()