from llm_handler import extract_user_info
from parser import normalize_output

def process_query(user_input):
    raw = extract_user_info(user_input)
    structured = normalize_output(raw)
    return structured