import re
import yaml
from copy import deepcopy

def extract_response_character(response_text):
  """
  Extrai o caractere '0' ou '1' da resposta do modelo.
  Args:
    response_text (str): A string de resposta do modelo.
  Returns:
    str: '0' ou '1' se encontrado, caso contrário, None.
  """
  # Use regex to find '0' or '1' potentially preceded by whitespace at the beginning of the string
  match = re.search(r'^[\s]*([01])', response_text)
  if match:
    return match.group(1)
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