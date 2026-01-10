"""
Grader module for executing and testing quantum code submissions
"""

import sys
import io
from contextlib import redirect_stdout, redirect_stderr
import traceback
import types
import unittest

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

            # First, execute the test code in its own module namespace so
            # unittest can discover TestCase classes defined there.
            test_module = types.ModuleType("submission_tests")

            # Provide the same globals (including user code) to the test module
            test_module.__dict__.update(exec_globals)

            # Execute tests code to define TestCase classes / functions
            try:
                exec(test_code, test_module.__dict__)
            except Exception as e:
                # If tests themselves error during definition, capture and return
                results['error'] = f"Test definition error: {type(e).__name__}: {e}\n{traceback.format_exc()}"
                results['passed'] = False
                return results

            # Load tests from the test_module
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(test_module)

            # Run the tests and capture their output
            runner_stream = io.StringIO()
            runner = unittest.TextTestRunner(stream=runner_stream, verbosity=2)

            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                result = runner.run(suite)

            # Aggregate results
            results['output'] = output_buffer.getvalue() + "\n" + runner_stream.getvalue()
            results['error'] = error_buffer.getvalue()
            results['test_results'] = {
                'testsRun': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'skipped': len(getattr(result, 'skipped', [])),
                'failures_info': [ (str(case), tb) for case, tb in result.failures ],
                'errors_info': [ (str(case), tb) for case, tb in result.errors ],
            }
            results['passed'] = result.wasSuccessful()
            
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
