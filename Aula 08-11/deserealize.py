import yaml


def serializeyaml():
    #Serializando dados com yaml
    dados = {"nome": "Alice",
             "idade": "25",
             "cursos": ["Python","Data Science"]}

    with open("dados.yaml", "w") as file:
        yaml.dump(dados,file)

#Deserialização dos dados
def deserializeyaml():
    with open("dados.yaml", "r") as file:
        a = yaml.safe_load(file)
    return a

print(deserializeyaml())