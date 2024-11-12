import google.generativeai as genai
import os
from datetime import datetime

# Configure API key from a file
with open("API_KEY.txt", "r") as f:
    api_key = f.read()
genai.configure(api_key=api_key)


def get_response(context, model_name="gemini-1.5-flash", max_tokens=100):
    """
    Generates a response from the generative model using the provided context.

    Parameters:
    - context (str): The input text or prompt.
    - model_name (str): The name of the model to use.
    - max_tokens (int): Maximum number of tokens in the response.

    Returns:
    - str: The generated response text.
    """
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(context, max_tokens=max_tokens)
    return response.text


def save_response_to_file(context, filename, model_name="gemini-1.5-flash"):
    """
    Generates a response and saves it to a specified file.

    Parameters:
    - context (str): The input context text.
    - filename (str): The file to save the response text to.
    - model_name (str): The model name to use for generation.
    """
    response_text = get_response(context, model_name=model_name)
    with open(filename, "w") as file:
        file.write(response_text)


def load_context_from_file(filename):
    """
    Loads context text from a specified file.

    Parameters:
    - filename (str): The file from which to read the context.

    Returns:
    - str: The content of the file.
    """
    with open(filename, "r") as file:
        context = file.read()
    return context


def get_response_from_file(input_filename, output_filename, model_name="gemini-1.5-flash"):
    """
    Loads context from a file, generates a response, and saves it to another file.

    Parameters:
    - input_filename (str): The input file with the context.
    - output_filename (str): The file to save the response text to.
    - model_name (str): The model name to use for generation.
    """
    context = load_context_from_file(input_filename)
    save_response_to_file(context, output_filename, model_name=model_name)


def append_response_with_timestamp(context, output_dir="responses", model_name="gemini-1.5-flash"):
    """
    Generates a response and saves it to a timestamped file in the specified directory.

    Parameters:
    - context (str): The input context text.
    - output_dir (str): The directory to save the response files.
    - model_name (str): The model name to use for generation.

    Returns:
    - str: The path of the saved file.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"response_{timestamp}.txt")
    save_response_to_file(context, filename, model_name=model_name)
    return filename


def handle_file_upload_and_generate_response(uploaded_file, model_name="gemini-1.5-flash"):
    """
    Handles an uploaded file, reads its content as context, generates a response, and returns it.

    Parameters:
    - uploaded_file (str): Path to the uploaded file to use as context.
    - model_name (str): The model name to use for generation.

    Returns:
    - str: The generated response text.
    """
    context = load_context_from_file(uploaded_file)
    return get_response(context, model_name=model_name)


def log_response(context, response_text, log_file="response_log.txt"):
    """
    Logs a context and its corresponding response to a log file with a timestamp.

    Parameters:
    - context (str): The input context text.
    - response_text (str): The generated response text.
    - log_file (str): The file to which the log entry will be written.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Context: {context}\nResponse: {response_text}\n{'-'*50}\n"
    with open(log_file, "a") as file:
        file.write(log_entry)


def get_and_log_response(context, log_file="response_log.txt", model_name="gemini-1.5-flash"):
    """
    Generates a response, logs it, and returns the response text.

    Parameters:
    - context (str): The input context text.
    - log_file (str): The file to log the response to.
    - model_name (str): The model name to use for generation.

    Returns:
    - str: The generated response text.
    """
    response_text = get_response(context, model_name=model_name)
    log_response(context, response_text, log_file=log_file)
    return response_text
