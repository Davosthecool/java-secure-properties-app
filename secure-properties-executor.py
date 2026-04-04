import subprocess


def execute_secure_properties(
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
        return result.stdout.strip()
    except subprocess.CalledProcessError as exc:
        return f"An error occurred in java secure properties tool execution: {exc.stderr}"