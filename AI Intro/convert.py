import pandas as pd
def convert(in_file,out_file):
    data=pd.read_excel(in_file)[["id","讲座名称","讲座时间"]]
    df = pd.DataFrame(columns=['唯一码', '媒体文件路径'])
    df["唯一码"]=data["id"]
    df["媒体文件路径"]="/home/media/Seminarposters/"+data["讲座时间"]+""+data["讲座名称"]+".jpg"
    #去掉媒体文件路径中的空格，并将冒号替换为下划线
    df["媒体文件路径"]=df["媒体文件路径"].str.replace(" ","").str.replace(":","_")
    df.to_excel(out_file,index=False)

# convert("result2 - dujuan.xlsx","宣传海报媒体资源.xlsx")