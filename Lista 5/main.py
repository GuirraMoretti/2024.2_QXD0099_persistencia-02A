import os
import yaml
import json
import logging




def configure_logging(config):
    logging.basicConfig(
        level=config['level'],
        filename=config['file'],
        format=config['format'],
        filemode=config['filemode']
    )

def process_data(json_file):
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
            logging.info(f"Arquivo JSON '{json_file}' carregado com sucesso.")
    except FileNotFoundError:
        logging.error(f"Arquivo JSON '{json_file}' não encontrado.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao decodificar o JSON: {e}")
        return []

    # Simulação de processamento de dados
    for record in data:
        try:
            if "name" not in record or record["age"] is None:
                raise ValueError(f"Dado inválido: {record}")
            logging.info(f"Processando registro: {record}")
        except ValueError as e:
            logging.warning(f"Erro no registro: {e}")

    return data

def main():
    XML_FILE = 'config.yaml'
    if os.path.exists(XML_FILE):
        with open(XML_FILE,'r') as file:
            config = yaml.safe_load(file)   
    
    configure_logging(config['logging'])
    
    process_data(config["data"]["file"])

if __name__ == "__main__":
    main()
