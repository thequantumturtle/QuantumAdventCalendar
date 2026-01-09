"""
Grader module for executing and testing quantum code submissions
"""

import sys
import io
from contextlib import redirect_stdout, redirect_stderr
import traceback

class CodeGrader:
    """Executes and grades user-submitted quantum code"""
    
    @staticmethod
    def execute_code(user_code, test_code, timeout=30):
        """
        Execute user code with test code and return results
        
        Args:
            user_code: User's submitted solution code
            test_code: Test code to validate the solution
            timeout: Maximum execution time in seconds
            
        Returns:
            Dictionary with execution results and test outcomes
        """
        results = {
            'passed': False,
            'output': '',
            'error': '',
            'test_results': []
        }
        
        try:
            # Create execution environment
            exec_globals = {
                '__builtins__': __builtins__,
            }
            
            # Import necessary libraries
            import_statements = """
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
"""
            
            # Combine code
            full_code = import_statements + "\n" + user_code
            
            # Execute user code
            exec(full_code, exec_globals)
            
            # Capture output and execute tests
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()
            
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                # Execute test code with user's functions in scope
                exec(test_code, exec_globals)
            
            results['output'] = output_buffer.getvalue()
            results['error'] = error_buffer.getvalue()
            results['passed'] = True
            
        except Exception as e:
            results['error'] = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            results['passed'] = False
        
        return results
    
    @staticmethod
    def validate_solution(user_code, test_code):
        """
        Validate a solution against test code
        
        Returns:
            Tuple of (passed: bool, results: dict)
        """
        results = CodeGrader.execute_code(user_code, test_code)
        return results['passed'], results
