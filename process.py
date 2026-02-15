## This is a repo helping Kitty process her research dataset

import pandas as pd
import os

question_cnt = 42
input_bundled_row_cnt = 3
input_interviewee_info_column_cnt = 5
output_interviewee_info_column_cnt = 7

def title_extraction(titles:list):
    questions = []
    for i in range(len(titles)):
        titles[i] = titles[i].splitlines()
        questions += [titles[i][8].split(" - ")[2]]
    return questions

def image_extraction(title:str):
    if title == "Login ID":
        return ""
    title = title.splitlines()
    return title[8].split(" - ")[1]

def data_processing(input_file:str, output_file:str):
    raw_list = pd.read_csv(input_file, header=0, index_col=0).values.tolist()
    assert(len(raw_list) % input_bundled_row_cnt == 0)
    img_cnt = int((len(raw_list[0]) - input_interviewee_info_column_cnt) / question_cnt)
    processed_list = [[None]*int(output_interviewee_info_column_cnt+question_cnt) for _ in range(int(len(raw_list)/input_bundled_row_cnt*img_cnt))]
    questions = title_extraction(raw_list[0][1:1+question_cnt])
    for i in range(int(len(raw_list)/input_bundled_row_cnt)):
        img_title = ""
        for j in range(img_cnt):
            processed_list[i*img_cnt+j][0] = raw_list[i*input_bundled_row_cnt+2][-4]
            processed_list[i*img_cnt+j][1] = raw_list[i*input_bundled_row_cnt+2][-3]
            processed_list[i*img_cnt+j][2] = raw_list[i*input_bundled_row_cnt+2][-2]
            processed_list[i*img_cnt+j][3] = raw_list[i*input_bundled_row_cnt+2][-1]
            processed_list[i*img_cnt+j][4] = raw_list[i*input_bundled_row_cnt+2][0]
            processed_list[i*img_cnt+j][6] = 1 - j % 2
            for k in range(7, 7+question_cnt):
                img_title = image_extraction(raw_list[i*input_bundled_row_cnt][j*question_cnt+k-6])
                if img_title == "":
                    break
                processed_list[i*img_cnt+j][5] = img_title
                processed_list[i*img_cnt+j][k] = raw_list[i*input_bundled_row_cnt+2][j*question_cnt+k-6]
            if img_title == "":
                break
    title_list = raw_list[0][-4:] + [raw_list[0][0], "Painting Name", "Eastern=1/Western=0"] + questions
    processed_dataframe = pd.DataFrame(processed_list, columns =title_list)
    processed_dataframe.to_csv(output_file)



if __name__ == "__main__":
    root = os.getcwd()
    input_folder = os.path.join(root, "raw_data")
    output_folder = os.path.join(root, "filtered_data")
    assert(os.path.exists(input_folder))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for _, _, files in os.walk(input_folder):
        for file in files:
            if not (len(file) > 3 and file[-3:] == "csv"):
                continue
            data_processing(os.path.join(input_folder, file),
                            os.path.join(output_folder, "filtered-"+file))
