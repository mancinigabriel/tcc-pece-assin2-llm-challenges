import re
import yaml
from copy import deepcopy
from datetime import datetime, timezone, timedelta
from pathlib import Path
import json

def extract_response_character(response_text):
  """
  Extrai o caractere '0' ou '1' da resposta do modelo.
  Args:
    response_text (str): A string de resposta do modelo.
  Returns:
    str: '0' ou '1' se encontrado, caso contrário, None.
  """
  # Use regex to find '0' or '1' potentially preceded by whitespace at the beginning of the string
  match = re.search(r'^[^a-z]*([01])', response_text)
  if match:
    return int(match.group(1))
  return None

def load_config(base_path, model_path):
    with open(base_path) as f:
        base = yaml.safe_load(f)

    with open(model_path) as f:
        model_cfg = yaml.safe_load(f)

    final_cfg = deepcopy(base)

    overrides = model_cfg.get("overrides", {})
    for section, params in overrides.items():
        final_cfg[section].update(params)

    final_cfg["model"] = model_cfg["model"]
    return final_cfg


def time_log():
  return datetime.now(timezone(timedelta(hours=-3)))


def log(model: str, gpu: str, quantized: bool, generation_args: dict, 
  metrics_dict: dict, timing: dict):
    """
    Inicializa o log de um experimento.
    Retorna um dicionário de estado que deve ser passado ao final.
    """

    log_state = {
      "log": {
          "model": model,
          "gpu": gpu,
          "quantized": quantized,
          "execution": {
            "inicio": 
              timing['inicio'].strftime("%Y-%m-%d %H:%M:%S"),
            "inicio_teste_consistencia": 
              timing['inicio_cons'].strftime("%Y-%m-%d %H:%M:%S"),
            "fim_teste_consistencia":
              timing['fim_cons'].strftime("%Y-%m-%d %H:%M:%S"),
            "inicio_aplicacao_completa": 
              timing['inicio_aplicacao_total'].strftime("%Y-%m-%d %H:%M:%S"),
            "fim":
              timing['fim'].strftime("%Y-%m-%d %H:%M:%S"),
            "duracao total": 
              (timing['fim'] - timing['inicio']).total_seconds(),
            "duracao_teste_consistencia":
              (timing['fim_cons'] - timing['inicio_cons']).total_seconds(),
            "duracao_aplicacao_total":
              (timing['fim'] - timing['inicio_aplicacao_total']).total_seconds(),
            },
          "generation": generation_args.copy(),
          "metrics": metrics_dict,
      }
    }

    return log_state


def export_log(log: dict, model_name: str):
    """
    Salva um dicionário de log em formato JSON.
    """
    file_time = time_log().strftime("%Y%m%d_%H%M%S")

    path_str = f'/content/drive/MyDrive/Mestrado/TCC Pós/Dados/logs/log_{model_name}_{file_time}.json'
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    return f'Arquivo salvo em {path_str} às {time_log().strftime("%Y-%m-%d %H:%M:%S")}'
