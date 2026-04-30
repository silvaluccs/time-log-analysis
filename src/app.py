import json
import logging

from . import aggregator, filter

logger = logging.getLogger(__name__)


def save_json(file_name: str, data: dict) -> None:
    """
    Salva um dicionário em um arquivo JSON.

    Args:
        file_name (str): Nome do arquivo JSON a ser salvo.
        data (dict): Dicionário a ser salvo.

    Raises:
        IOError: Caso não seja possível escrever o arquivo.
    """
    logger.info(f"Salvando resultado em {file_name}")

    try:
        with open(file=file_name, mode="w", encoding="utf-8") as file:
            json.dump(obj=data, fp=file, indent=2, ensure_ascii=False)
    except IOError:
        logger.error(f"Erro ao salvar o arquivo '{file_name}'.")
        raise


def run_analysis_and_save_results(source_file: str, output_file: str) -> None:
    """
    Orquestra a análise completa dos registros de timesheet e salva o resultado.

    Lê o arquivo de entrada, filtra registros inválidos, realiza todas as
    agregações e rankings, e salva o resumo analítico em um arquivo JSON.

    Args:
        source_file (str): Caminho do arquivo JSON de entrada com os registros.
        output_file (str): Caminho do arquivo JSON de saída com o resultado.

    Returns:
        None

    Raises:
        FileNotFoundError: Caso o arquivo de entrada não seja encontrado.
        json.JSONDecodeError: Caso o arquivo de entrada não seja um JSON válido.
        IOError: Caso não seja possível escrever o arquivo de saída.
    """

    logger.info("Iniciando pipeline de análise: %s → %s", source_file, output_file)

    json_data = filter.load_json(file_name=source_file)
    number_of_invalid_records, filtered_data = filter.clear_invalid_records(
        data=json_data
    )

    total_minutes = aggregator.calculate_total_minutes(filtered_data)
    grouped = aggregator.group_by_task(filtered_data)

    top_3_employees = aggregator.get_top_3_employees(grouped)
    most_distinct_user = aggregator.get_most_distinct_user_on_task(grouped)

    tasks = aggregator.sort_tasks(
        [
            aggregator.build_task(task_id, records, total_minutes)
            for task_id, records in grouped.items()
        ]
    )
    top_3_tasks = aggregator.build_top_3_tasks(tasks)

    result_analysis = {
        "totalMinutes": total_minutes,
        "tasks": tasks,
        "mostWorkedTask": tasks[0],
        "top3TasksPercentage": top_3_tasks,
        "top3Employees": top_3_employees,
        "mostDistinctUserOnTasks": most_distinct_user,
        "ignoredRecords": number_of_invalid_records,
    }

    save_json(file_name=output_file, data=result_analysis)
