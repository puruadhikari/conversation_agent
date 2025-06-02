import concurrent.futures
import time


def add(a, b):
    """Simulate a time-consuming addition."""
    print(f"Starting add({a}, {b})")
    time.sleep(2)  # simulate delay
    result = a + b
    print(f"Finished add: {result}")
    return result


def multiply(a, b):
    """Simulate a time-consuming multiplication."""
    print(f"Starting multiply({a}, {b})")
    time.sleep(3)  # simulate delay
    result = a * b
    print(f"Finished multiply: {result}")
    return result


def parallel_all(funcs_with_args):
    """
    Runs multiple functions in parallel and returns their results
    after all have completed.

    :param funcs_with_args: List of tuples (func, args)
    :return: List of results in the same order
    """
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all functions to the executor
        futures = [executor.submit(func, *args) for func, args in funcs_with_args]
        # Wait for all of them to complete and collect results
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results


if __name__ == "__main__":
    # Define the functions and their arguments
    tasks = [
        (add, (5, 3)),
        (multiply, (5, 3))
    ]

    start_time = time.time()
    results = parallel_all(tasks)
    duration = time.time() - start_time

    print("\nAll tasks completed.")
    print(f"Results: {results}")
    print(f"Total time taken: {duration:.2f} seconds")
