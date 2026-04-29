import json


def load_json(file_name: str) -> list:
    """
    Carrega um arquivo JSON e retorna uma lista com os dados.

    Args:
        file_name (str): Nome do arquivo JSON a ser carregado.

    Returns:
        list: Lista com os dados do arquivo JSON.

    Raises:
        FileNotFoundError: Caso o arquivo não seja encontrado.
        json.JSONDecodeError: Caso o arquivo não seja um JSON válido.
    """
    try:
        with open(file=file_name, mode="r", encoding="utf-8") as file:
            return list(json.load(fp=file))
    except FileNotFoundError:
        print(f"Arquivo '{file_name}' não encontrado.")
        raise
    except json.JSONDecodeError:
        print(f"Arquivo '{file_name}' não é um JSON válido.")
        raise


def clear_invalid_records(data: list) -> tuple[int, list]:
    """
    Remove registros inválidos da lista de dados.

    Args:
        data (list): Lista de dados a ser filtrada.

    Returns:
        tuple[int, list]: Número de registros inválidos removidos e a lista de dados filtrada.
    """
    valid = [record for record in data if record["minutes"] > 0]
    ignored = len(data) - len(valid)
    return ignored, valid


if __name__ == "__main__":
    json_data = load_json(file_name="data.json")

    invalid_records, filtered_data = clear_invalid_records(data=json_data)

    assert len(filtered_data) == len(json_data) - invalid_records
    assert invalid_records == 41

    print("Testes passaram.")
