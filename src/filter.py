import json
import logging

logger = logging.getLogger(__name__)


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
        logger.info("Carregando arquivo '%s'", file_name)
        with open(file=file_name, mode="r", encoding="utf-8") as file:
            data = list(json.load(fp=file))
        logger.info("%d registros carregados de '%s'", len(data), file_name)
        return data
    except FileNotFoundError:
        logger.error("Arquivo '%s' não encontrado.", file_name)
        raise
    except json.JSONDecodeError:
        logger.error("Arquivo '%s' não é um JSON válido.", file_name)
        raise


def clear_invalid_records(data: list) -> tuple[int, list]:
    """
    Remove registros inválidos da lista de dados.

    Args:
        data (list): Lista de dados a ser filtrada.

    Returns:
        tuple[int, list]: Número de registros inválidos removidos e a lista de dados filtrada.
    """
    logger.info("Filtrando registros inválidos de %d entradas", len(data))
    valid = [record for record in data if record["minutes"] > 0]
    ignored = len(data) - len(valid)
    logger.info("%d registros válidos | %d registros ignorados", len(valid), ignored)
    return ignored, valid


if __name__ == "__main__":
    json_data = load_json(file_name="data.json")
    invalid_records, filtered_data = clear_invalid_records(data=json_data)
    assert len(filtered_data) == len(json_data) - invalid_records
    assert invalid_records == 41
    print("Testes passaram.")
