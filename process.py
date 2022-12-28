import pandas as pd
import os

def title_extraction(titles:list):
    questions = []
    for i in range(len(titles)):
        titles[i] = titles[i].splitlines()
        questions += [titles[i][8].split(" - ")[2]]
    return questions

def image_extraction(title:str):
    title = title.splitlines()
    
    return title[8].split(" - ")[1]

def data_processing(input_file:str, output_file:str):
    raw_list = pd.read_csv(input_file, header=0, index_col=0).values.tolist()
    assert(len(raw_list) % 3 == 0)
    processed_list = [[None]*49 for _ in range(int(len(raw_list)/3*6))]
    questions = title_extraction(raw_list[0][1:43])
    for i in range(int(len(raw_list)/3)):
        for j in range(6):
            processed_list[i*6+j][0] = raw_list[i*3+2][253]
            processed_list[i*6+j][1] = raw_list[i*3+2][254]
            processed_list[i*6+j][2] = raw_list[i*3+2][255]
            processed_list[i*6+j][3] = raw_list[i*3+2][256]
            processed_list[i*6+j][4] = raw_list[i*3+2][0]
            processed_list[i*6+j][6] = 1 - j % 2
            for k in range(7, 49):
                processed_list[i*6+j][5] = image_extraction(raw_list[0][j*42+k-6])
                processed_list[i*6+j][k] = raw_list[i*3+2][j*42+k-6]
    title_list = raw_list[0][253:] + [raw_list[0][0], "Painting Name", "Eastern=1/Western=0"] + questions
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
