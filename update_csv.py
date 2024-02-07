import gradio as gr
import pandas as pd

# 记录是否已加载过头部信息
state_file_path = "./header_state.txt"
def load_header_state():
    try:
        with open(state_file_path, 'r') as file:
            return bool(file.read().strip())
    except FileNotFoundError:
        return False
def save_header_state(state):
    with open(state_file_path, 'w') as file:
        file.write(str(state))

# 初始化 header_loaded 状态
header_loaded = load_header_state()
def load_csv():

    csv_data = pd.read_csv(r"../landmark_1_updated.csv",)
    df_data = pd.DataFrame(csv_data)

    return df_data


# 处理数据
# def process_csv():
#     count = 0
#     df_data = load_csv()
#     for index, row in df_data.iterrows():
#         qa_dict = {}
#         # print(index, row)
#         if int(index) % 3 == 0:
#             qa_dict["id"] = count
#             count += 1
#             qa_dict["kind_question"] = str(row["问题"])
#             qa_dict["kind_answer"] = str(row["肯定回答"])
#             kind_list.append(str(row["问题"]))
#         elif int(index) % 3 == 1:
#             qa_dict["question_1"] = str(row["问题"])
#             qa_dict["answer_yes_1"] = str(row["肯定回答"])
#             qa_dict["answer_no_1"] = str(row["否定回答或多个回答"]) if str(row["否定回答或多个回答"]) != "nan" else "none"
#         elif int(index) % 3 == 2:
#             qa_dict["question_2"] = str(row["问题"])
#             qa_dict["answer_yes_2"] = str(row["肯定回答"])
#             qa_dict["answer_no_2"] = str(row["否定回答或多个回答"]) if str(row["否定回答或多个回答"]) != "nan" else "none"
#         qa_list.append(qa_dict)
#     print(qa_list)
#     print(kind_list)
#     print(len(qa_list))

def update_csv(*args):
    dataframe = args[0]
    dataframe.to_csv("../landmark_1_updated.csv", index=False, encoding="utf_8_sig")
    print("数据已更新并保存成功!")
    return "数据已更新并保存成功!"

button = gr.Button("提交更新", update_csv)
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
