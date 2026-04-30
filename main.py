import logging

import src.app as app

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s"
    )
    source_file = "data.json"
    output_file = "result.json"

    logger.info(f"Iniciando análise do arquivo {source_file}")

    try:
        app.run_analysis_and_save_results(source_file, output_file)
        logger.info(f"Análise concluída, resultado salvo em {output_file}")
    except Exception as e:
        logger.critical(f"Erro durante a análise: {e}")
