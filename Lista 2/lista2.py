"""
1. Leitura dos Arquivos: O código lê todos os arquivos .txt da pasta textos.
Processamento: Remover linhas em branco, calcular a quantidade de palavras e caracteres.
Escrita Consolidada: Escreve o nome do arquivo e as estatísticas no arquivo consolidado.txt.
Compactação ZIP: Compacta o arquivo consolidado.txt no arquivo saida.zip.
"""
import os
import zipfile

#00. Diretorio do arquivo

files = []


def generate_output_file(input_file,ext):
    #Gerando o nome do arquivo e seu caminho
    dir_name , base_name = os.path.split(input_file)
    file_name , ext_name = os.path.splitext(base_name)
    output_file = f'{dir_name}/{file_name}_consolidado{ext}'
    return output_file


def file_read(input_file):
    #Lê o texto contido no arquivo
    with open(input_file, 'r', encoding='utf-8') as input:
        text = input.read()
        output_file_path = generate_output_file(input_file,".txt")
        #Escreve em um novo arquivo o texto passando por strip e a quantidade de caracteres
        with open(output_file_path, 'w',encoding='utf-8') as output:
            for line in text.splitlines():
                output.write(f'{line.strip()}\n')
            num_char = len(text)
            num_words = len(text.split())
            output.write(f'Quantidade de caracteres: {num_char}\n')
            output.write(f'Quantidade de palavras: {num_words}\n')
            compress_output_file(output_file_path)

def storage_file_path_in_list():
    #Estou armazenando todos os arquivos da pasta em uma lista
    dir = os.getcwd() + '/textos'
    for item in os.listdir(dir):
        file_path = os.path.join(dir,item)
        files.append(file_path)

def verify_if_exist_txt():
    # Verifico se os arquivos contidos na lista são txt e não contêm '_consolidado' no nome
    for item in files:
        if '_consolidado' not in item and item.endswith('.txt'):
            file_read(item)
        else:
            print('Não contém arquivo .txt')

def compress_output_file(output_file):
    # Cria um arquivo ZIP com o mesmo nome do arquivo de saída
    zip_file = f"{os.path.splitext(output_file)[0]}.zip"
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(output_file, os.path.basename(output_file))

storage_file_path_in_list()
verify_if_exist_txt()