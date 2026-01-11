import re

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