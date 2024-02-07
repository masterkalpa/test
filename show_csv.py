# -*- coding: utf-8 -*-
import threading

import gradio as gr
import pandas as pd

# 读取数据
def load_csv():
    csv_data = pd.read_csv(r"../landmark_1_updated.csv", )
    df_data = pd.DataFrame(csv_data, )
    print(df_data)
    return df_data
# qa_mapping

qa_show_list = []
kind_list = []
kind_list.clear()

# 处理数据
def process_show_data():
    df_data = load_csv()
    count = 0
    for i, row in df_data.iterrows():
        if int(i) % 3 == 0:
            qa_dict = {}
            qa_dict["id"] = count
            count += 1
            qa_dict["kind_question"] = str(row["问题"])
            qa_dict["kind_answer"] = str(row["肯定回答"])
            kind_list.append(str(row["问题"]))
        elif int(i) % 3 == 1:
            qa_dict["question_1"] = str(row["问题"])
            qa_dict["answer_yes_1"] = str(row["肯定回答"])
            qa_dict["answer_no_1"] = str(row["否定回答或多个回答"]) if str(row["否定回答或多个回答"]) != "nan" else "none"
        elif int(i) % 3 == 2:
            qa_dict["question_2"] = str(row["问题"])
            qa_dict["answer_yes_2"] = str(row["肯定回答"])
            qa_dict["answer_no_2"] = str(row["否定回答或多个回答"]) if str(row["否定回答或多个回答"]) != "nan" else "none"
        qa_dict.update(qa_dict)

        if int(i) % 3 == 2:
            qa_show_list.append(qa_dict)
        if int(i)+1 == len(df_data):
            qa_show_list.append(qa_dict)
    print(qa_show_list)
    print(kind_list)
    print(len(qa_show_list))
process_show_data()

# 更新数据
def update_csv(*args):
    dataframe = args[0]
    dataframe.to_csv("../landmark_1_updated.csv", index=False, encoding="utf_8_sig")
    print("数据已更新并保存成功!")
    return "数据已更新并保存成功!"


def vqa(kind):
    for i in range(len(qa_show_list)):

        if kind == qa_show_list[i]["kind_question"]:
            question_1 = qa_show_list[i]["question_1"]
            answer_yes_1 = qa_show_list[i]["answer_yes_1"]
            answer_no_1 = qa_show_list[i]["answer_no_1"]
            try:
                question_2 = qa_show_list[i]["question_2"]
                answer_yes_2 = qa_show_list[i]["answer_yes_2"]
                answer_no_2 = qa_show_list[i]["answer_no_2"]
                return question_1, answer_yes_1+"\n"+answer_no_1, question_2, answer_yes_2+"\n"+answer_no_2
            except Exception as error:
                return question_1, answer_yes_1+"\n"+answer_no_1, None, None
def launch_demo():
    demo = gr.Interface(
        vqa,
        inputs=gr.Radio(kind_list, label="可选择问题类型"),
        outputs=[gr.Textbox(label="提问示例1", lines=2), gr.Textbox(label="回答示例1", lines=5),
                 gr.Textbox(label="提问示例2", lines=2), gr.Textbox(label="回答示例2", lines=5)],
        examples=[
            [],
        ],
        title="Landmark类型问答关系示例",
        description="从这些例子中寻找灵感",
        live=True,
    )
    demo.launch(server_port=7860, share=True)
button = gr.Button("提交更新", update_csv)
def launch_demo_2():
    demo_2 = gr.Interface(
        update_csv,
        [
            gr.DataFrame(
                value=load_csv(),
                datatype=["str", "str", "str"],
                row_count=15,
                col_count=(3, "fixed"),
                wrap=True,
                line_breaks=True,

            ),
            button,
        ],
        outputs=None,
        title="关系问答对更新",
        live=True,
    )
    demo_2.launch(server_port=7861, share=True)

# launch_demo_2()
launch_demo()

# if __name__ == "__main__":
#     threading.Thread(target=launch_demo()).start()
#     threading.Thread(target=launch_demo_2()).start()


