import yaml
from typing import Literal
import subprocess
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import base64
import os

def execute_secure_properties(
    input_type: Literal["string", "yaml"],
    jar_path: str,
    encryption_key: str,
    data: str,
    is_encryption: bool,
    algorithm: str,
    mode: str,
    use_random_iv: bool,
) -> str:
    """
    Entrypoint function to execute the secure properties encryption/decryption process.

    Args:
        jar_path (str): The path to the JAR file that contains the encryption/decryption logic.
        encryption_key (str): The key used for encryption or decryption.
        data (str): The data to be encrypted or decrypted.
        is_encryption (bool): True if encryption is requested, False for decryption.
        algorithm (str): The encryption algorithm to use.
        mode (str): The encryption mode to use.
        use_random_iv (bool): Whether to use a random initialization vector.

    Returns:
        str: The result of the encryption or decryption process.
    """
    match input_type:
        case "string":
            return _run_secure_properties(
                jar_path=jar_path,
                encryption_key=encryption_key,
                data=data,
                is_encryption=is_encryption,
                algorithm=algorithm,
                mode=mode,
                use_random_iv=use_random_iv,
            )
        case "yaml":
            return _process_yaml_data(data, {
                "jar_path": jar_path,
                "encryption_key": encryption_key,
                "is_encryption": is_encryption,
                "algorithm": algorithm,
                "mode": mode,
                "use_random_iv": use_random_iv
            })
        case _:
            raise ValueError(f"Unsupported input type: {input_type}")

def _transform_yaml_data(input_data: dict, params: dict) -> dict:
    """
    Transforms YAML data by applying secure properties encryption/decryption to the values.

    Args:
        input_data (dict): The YAML data represented as a dictionary.
        params (dict): The parameters for secure properties processing.
    Returns:
        dict: The transformed YAML data with encrypted/decrypted values.
    """
    result = {}
    
    for key, value in input_data.items():
        if isinstance(value, dict):
            result[key] = _transform_yaml_data(value, params)
        else:
            result[key] = _run_secure_properties(**params, data=value)
    
    return result
    
def _process_yaml_data(yaml_data: str, params: dict) -> str:
    """
    Processes YAML data for secure properties encryption/decryption.

    Args:
        yaml_data (str): The YAML data to be processed.
        params (dict): The parameters for secure properties processing.
    Returns:
        str: The processed YAML data.
    """
    try:
        data_dict : dict = yaml.safe_load(yaml_data)
        output_dict = _transform_yaml_data(data_dict, params)
        processed_yaml = yaml.dump(output_dict)
        return processed_yaml
    except yaml.YAMLError as exc:
        return f"An error occurred while processing YAML data: {exc}"


def _clean_input_string(input_string: str) -> str:
    """
    Cleans the input string for secure properties processing.

    Args:
        input_string (str): The string to be cleaned.
    Returns:
        str: The cleaned string.
    """
    newstring = input_string.strip()
    if newstring.startswith('![') and newstring.endswith(']'):
        newstring = newstring[2:-1]
    return newstring

def _format_output_string(output_string: str) -> str:
    """
    Formats the output string from secure properties processing.

    Args:
        output_string (str): The string to be formatted.
    Returns:
        str: The formatted string.
    """
    newstring = output_string.strip()
    newstring = f"![{newstring}]"
    return newstring

def _run_secure_properties(
    jar_path: str,
    encryption_key: str,
    data: str,
    is_encryption: bool,
    algorithm: str,
    mode: str,
    use_random_iv: bool,
) -> str:
    """
    Executes the secure properties encryption/decryption process using the provided JAR file, encryption key, and properties.

    Args:
        jar_path (str): The path to the JAR file that contains the encryption/decryption logic.
        encryption_key (str): The key used for encryption or decryption.
        data (str): The data to be encrypted or decrypted.
        is_encryption (bool): True if encryption is requested, False for decryption.
        algorithm (str): The encryption algorithm to use.
        mode (str): The encryption mode to use.
        use_random_iv (bool): Whether to use a random initialization vector.
    Returns:
        str: The result of the encryption or decryption process.
    """
    
    if not is_encryption:
        data = _clean_input_string(data)
    try:
        action = "encrypt" if is_encryption else "decrypt"
        command = [
            "java",
            "-cp",
            jar_path,
            "com.mulesoft.tools.SecurePropertiesTool",
            "string",
            action,
            algorithm,
            mode,
            encryption_key,
            data,
        ]

        if use_random_iv:
            command.append("--use-random-iv")

        run_kwargs = {
            "check": True,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True,
        }

        # In packaged Windows GUI mode, this avoids opening a new console window.
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            run_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        result = subprocess.run(
            command,
            **run_kwargs,
        )
        output = result.stdout.strip()
        if is_encryption:
            output = _format_output_string(result.stdout)
        return output
    except subprocess.CalledProcessError as exc:
        return f"An error occurred in java secure properties tool execution: {exc.stderr}"
    
    
def _run_secure_properties_python(
    jar_path: str,
    encryption_key: str,
    data: str,
    is_encryption: bool,
    algorithm: str,
    mode: str,
    use_random_iv: bool,
) -> str:
    """
    A Python implementation of the secure properties encryption/decryption process for testing purposes.

    Args:
        jar_path (str): The path to the JAR file that contains the encryption/decryption logic (not used in this implementation).
        encryption_key (str): The key used for encryption or decryption.
        data (str): The data to be encrypted or decrypted.
        is_encryption (bool): True if encryption is requested, False for decryption.
        algorithm (str): The encryption algorithm to use (not used in this implementation).
        mode (str): The encryption mode to use (not used in this implementation).
        use_random_iv (bool): Whether to use a random initialization vector (not used in this implementation).
    Returns:
        str: The result of the encryption or decryption process.
    """
    
    match algorithm:
        case "AES":
            match mode:
                case "CBC":
                    mode = AES.MODE_CBC
                case _:
                    raise ValueError(f"Unsupported mode: {mode}")
            
            key = encryption_key.encode()
            if is_encryption:
                iv = os.urandom(16) if use_random_iv else b'\x00' * 16
                cipher = AES.new(key, mode, iv=iv)
                padded_message = pad(data.encode(), AES.block_size)
                ciphertext = cipher.encrypt(padded_message)
                return base64.b64encode(ciphertext).decode()
            else:
                raw_data = base64.b64decode(data)
                iv = raw_data[:16]
                ciphertext = raw_data[16:]
                cipher = AES.new(key, mode, iv=iv)
                decrypted_padded_message = cipher.decrypt(ciphertext).decode().strip() # Remove padding
                return decrypted_padded_message
        case _:
            raise ValueError(f"Unsupported algorithm: {algorithm}")