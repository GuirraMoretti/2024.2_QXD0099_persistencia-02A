import zipfile as zip

'''
Slide da aula
https://docs.google.com/presentation/d/1ZghcJiw4bQMa-MfGIqXuZaVf0h4GN9MkFIvEwXoDUBY/edit?usp=sharing


'''

#Leitura de arquivo ZIP
zip_file_path = "arquivoZip.zip"

with zip.ZipFile(zip_file_path, 'r') as zip_ref:
    for file_name in zip_ref.namelist():
        with zip_ref.open(file_name) as file:
            for line in file:
                print(line.decode('utf-8').strip())
