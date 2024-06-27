import os
def generate_corpus(directory_path: str, create_txt_file: bool = True) -> (str):
    
    book_list = []
    for folder, _, files in os.walk(directory_path):  
        folderpath = os.path.join(directory_path, folder)
        for file in files:
            if not file.startswith('.') and file.endswith('.txt'):
                bookpath = os.path.join(folderpath, file)
                book_list.append(bookpath)
    
    text_corpus = ''
    for path in book_list:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f: temp = f.read()
        text_corpus += temp
        
    if create_txt_file:
        from paths import SOURCE
        file_name = 'text_corpus.txt'
        destination = os.path.join(SOURCE, file_name)
        with open(destination, 'w', encoding='utf-8') as f:
            f.write(text_corpus)
            
    return text_corpus