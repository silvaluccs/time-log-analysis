import src.app as app

if __name__ == "__main__":
    source_file = "data.json"
    output_file = "result.json"

    app.run_analysis_and_save_results(source_file, output_file)
    print(f"Analise concluída, veja o resultado em {output_file}")
