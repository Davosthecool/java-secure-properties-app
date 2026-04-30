from typing import Callable
from secure_properties_executor import _run_secure_properties, _run_secure_properties_python

def compare_results(f1 : Callable, f2 : Callable, *args) -> bool:
    """
    Compare the results of two functions with the same arguments.
    
    Args:
        f1: The first function to compare.
        f2: The second function to compare.
        *args: The arguments to pass to both functions.
    
    Returns:
        True if the results are the same, False otherwise.
    """
    result1 = f1(*args)
    result2 = f2(*args)
    print("-" * 50)
    print(f"Comparing results of two functions with the following arguments:\n{args}\n")
    
    print("Results are " + ("the same" if result1 == result2 else "different") + ".\n")
    
    print(f"Result from function 1: {result1}\n")
    print(f"Result from function 2: {result2}\n")
    
args_list = [
    ("./ressources/secure-properties-tool-j17.jar", "encryption_key12", "data_to_encrypt", True, "AES", "CBC", False),
    # ("./ressources/secure-properties-tool-j17.jar", "encryption_key12", "![encrypteddata]", False, "AES", "CBC", True),
]

for args in args_list:
    compare_results(_run_secure_properties, _run_secure_properties_python, *args)