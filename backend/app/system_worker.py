import os
import subprocess
import json
import logging

# Configure structured logging to standard output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_disk_usage():
    """
    Checks disk usage of the container's root filesystem using the 'df' command.
    Demonstrates secure use of the subprocess module.
    """
    try:
        # We pass arguments as a list (shell=False) to prevent shell injection vulnerabilities
        result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, check=True)
        
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            # Parse the second line of the df output
            parts = lines[1].split()
            return {
                "filesystem": parts[0],
                "size": parts[1],
                "used": parts[2],
                "available": parts[3],
                "use_percentage": parts[4]
            }
    except (subprocess.SubprocessError, IndexError) as e:
        logging.error(f"Failed to fetch disk usage: {e}")
        return {"error": "Could not retrieve disk metrics"}

def get_environment_metadata():
    """
    Reads specific non-sensitive environment configuration via the 'os' module.
    """
    return {
        "app_env": os.getenv("APP_ENV", "production"),
        "python_version": os.getenv("PYTHON_VERSION", "Unknown"),
        "container_role": "backend-api"
    }

def generate_health_report():
    """
    Aggregates metrics into a single cohesive system report.
    """
    logging.info("Generating system health payload.")
    report = {
        "status": "UP",
        "disk": get_disk_usage(),
        "metadata": get_environment_metadata()
    }
    return report

# Quick local testing block
if __name__ == "__main__":
    print(json.dumps(generate_health_report(), indent=4))