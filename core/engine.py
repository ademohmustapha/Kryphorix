from concurrent.futures import ThreadPoolExecutor, as_completed
from core.config_loader import load_config

def run_parallel(tasks):
    findings = []
    config = load_config()
    max_threads = config.get("threads", 5)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_task = {executor.submit(task): task for task in tasks}

        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                result = future.result()
                if result:
                    findings.extend(result)
            except Exception as e:
                print(f"[!] Task {task.__name__} failed: {e}")

    return findings

