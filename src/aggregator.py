from collections import defaultdict

from . import filter


def group_by_task(data: list) -> dict:
    """
    Agrupa os registros de timesheet por taskId.

    Args:
        data (list): Lista de registros válidos de timesheet.

    Returns:
        dict: Dicionário com taskId como chave e lista de registros como valor.
    """
    tasks = defaultdict(list)
    for record in data:
        tasks[record["taskId"]].append(record)
    return dict(tasks)


def calculate_total_minutes(data: list) -> int:
    """
    Calcula o total de minutos de uma lista de registros.

    Args:
        data (list): Lista de registros de timesheet.

    Returns:
        int: Soma total dos minutos.
    """
    return sum(record["minutes"] for record in data)


def calculate_task_percentage(task_minutes: int, total_minutes: int) -> str:
    """
    Calcula o percentual de minutos de uma tarefa sobre o total geral.

    Args:
        task_minutes (int): Total de minutos da tarefa.
        total_minutes (int): Total geral de minutos de todas as tarefas.

    Returns:
        str: Percentual formatado com duas casas decimais (ex: "14.25%").
    """
    return f"{round((task_minutes / total_minutes) * 100, 2):.2f}%"


def build_task(task_id: int, records: list, total_minutes: int) -> dict:
    """
    Constrói o dicionário analítico de uma tarefa.

    Args:
        task_id (int): Identificador da tarefa.
        records (list): Lista de registros pertencentes à tarefa.
        total_minutes (int): Total geral de minutos para cálculo do percentual.

    Returns:
        dict: Dicionário com taskId, taskName, totalMinutes e percentage.
    """
    task_minutes = calculate_total_minutes(records)
    return {
        "taskId": task_id,
        "taskName": records[0]["taskName"],
        "totalMinutes": task_minutes,
        "percentage": calculate_task_percentage(task_minutes, total_minutes),
    }


def sort_tasks(tasks: list) -> list:
    """
    Ordena as tarefas por totalMinutes decrescente e taskId crescente em empate.

    Args:
        tasks (list): Lista de dicionários de tarefas.

    Returns:
        list: Lista ordenada de tarefas.
    """
    return sorted(tasks, key=lambda t: (-t["totalMinutes"], t["taskId"]))


def build_top_3_tasks(tasks: list) -> list:
    """
    Retorna as 3 tarefas com maior totalMinutes sem o campo totalMinutes.

    Args:
        tasks (list): Lista de tarefas já ordenadas.

    Returns:
        list: Top 3 tarefas contendo apenas taskId, taskName e percentage.
    """
    return [
        {k: v for k, v in task.items() if k != "totalMinutes"} for task in tasks[:3]
    ]


def group_by_employee(tasks: dict) -> dict:
    """
    Agrupa os registros por userId acumulando minutos e tarefas distintas.

    Args:
        tasks (dict): Dicionário de tarefas agrupadas por taskId.

    Returns:
        dict: Dicionário com userId como chave e dados do funcionário como valor,
              incluindo totalMinutes e lista de taskIds distintos.
    """
    employees = {}
    for task_id, records in tasks.items():
        for record in records:
            user_id = record["userId"]
            if user_id not in employees:
                employees[user_id] = {
                    "userId": user_id,
                    "userName": record["userName"],
                    "totalMinutes": record["minutes"],
                    "taskIds": [task_id],
                }
            else:
                employees[user_id]["totalMinutes"] += record["minutes"]
                if task_id not in employees[user_id]["taskIds"]:
                    employees[user_id]["taskIds"].append(task_id)
    return employees


def sort_employees(employees: dict) -> list:
    """
    Ordena os funcionários por totalMinutes decrescente e userId crescente em empate.

    Args:
        employees (dict): Dicionário de funcionários agrupados por userId.

    Returns:
        list: Lista ordenada de funcionários.
    """
    return sorted(employees.values(), key=lambda e: (-e["totalMinutes"], e["userId"]))


def build_top_3_employees(employees: list) -> list:
    """
    Retorna os 3 funcionários com maior totalMinutes sem o campo taskIds.

    Args:
        employees (list): Lista de funcionários já ordenados.

    Returns:
        list: Top 3 funcionários contendo userId, userName e totalMinutes.
    """
    return [
        {k: v for k, v in employee.items() if k != "taskIds"}
        for employee in employees[:3]
    ]


def get_top_3_employees(tasks: dict) -> list:
    """
    Retorna o ranking dos 3 funcionários com maior total de minutos trabalhados.

    Args:
        tasks (dict): Dicionário de tarefas agrupadas por taskId.

    Returns:
        list: Top 3 funcionários ordenados por totalMinutes.
    """
    employees = group_by_employee(tasks)
    employees = sort_employees(employees)[:3]
    return build_top_3_employees(employees)


def sort_most_distinct_user(employees: dict) -> list:
    """
    Ordena os funcionários por quantidade de tarefas distintas decrescente
    e userId crescente em empate.

    Args:
        employees (dict): Dicionário de funcionários agrupados por userId.

    Returns:
        list: Lista ordenada de funcionários por tarefas distintas.
    """
    return sorted(employees.values(), key=lambda e: (-len(e["taskIds"]), e["userId"]))


def get_most_distinct_user_on_task(tasks: dict) -> dict:
    """
    Retorna o funcionário que trabalhou no maior número de tarefas distintas.

    Args:
        tasks (dict): Dicionário de tarefas agrupadas por taskId.

    Returns:
        dict: Dicionário com userId, userName, distinctTasks e lista de taskIds.
    """
    employees = group_by_employee(tasks)
    sorted_employees = sort_most_distinct_user(employees)
    top = sorted_employees[0]

    return {
        "userId": top["userId"],
        "userName": top["userName"],
        "distinctTasks": len(top["taskIds"]),
        "taskIds": top["taskIds"],
    }


if __name__ == "__main__":
    json_data = filter.load_json(file_name="data.json")
    invalid_records, filtered_data = filter.clear_invalid_records(data=json_data)

    grouped = group_by_task(filtered_data)
    tasks = sort_tasks(
        [
            build_task(tid, recs, calculate_total_minutes(filtered_data))
            for tid, recs in grouped.items()
        ]
    )

    total = calculate_total_minutes(filtered_data)
    assert total == 28408, f"Esperado 28408, obtido {total}"

    assert tasks[0]["taskId"] == 103, (
        f"Esperado taskId 103, obtido {tasks[0]['taskId']}"
    )
    assert tasks[0]["totalMinutes"] == 4047, (
        f"Esperado 4047, obtido {tasks[0]['totalMinutes']}"
    )
    assert tasks[0]["percentage"] == "14.25%", (
        f"Esperado 14.25%, obtido {tasks[0]['percentage']}"
    )

    assert tasks[1]["taskId"] == 110
    assert tasks[2]["taskId"] == 106

    top3_tasks = build_top_3_tasks(tasks)
    assert len(top3_tasks) == 3
    assert "totalMinutes" not in top3_tasks[0], "totalMinutes não deveria estar no top3"

    top3_employees = get_top_3_employees(grouped)
    assert len(top3_employees) == 3
    assert "taskIds" not in top3_employees[0], (
        "taskIds não deveria estar no top3 employees"
    )

    most_distinct = get_most_distinct_user_on_task(grouped)
    assert "userId" in most_distinct
    assert "userName" in most_distinct
    assert "distinctTasks" in most_distinct
    assert "taskIds" in most_distinct
    assert most_distinct["distinctTasks"] == len(most_distinct["taskIds"])

    print("Todos os testes passaram.")
