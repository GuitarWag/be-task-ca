import subprocess
import uvicorn


def start():
    uvicorn.run("be_task_ca.drivers.rest.app:app", host="0.0.0.0", port=8000, reload=True)


def auto_format():
    subprocess.call(["black", "be_task_ca"])


def run_linter():
    subprocess.call(["flake8", "be_task_ca"])


def run_tests():
    subprocess.call(["pytest", "-vv"])


def create_dependency_graph():
    subprocess.call(["pydeps", "be_task_ca", "--cluster"])


def check_types():
    subprocess.call(["mypy", "be_task_ca"])
