import argparse
import glob
import importlib.util
from pathlib import Path
from typing import Any, Dict

_ROOT_DIR = Path(Path(__file__).absolute())
_BASE_FOLDER = _ROOT_DIR.cwd() / "chargeapi/exec/"


def load_file(name: str, filepath: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(module)  # type: ignore
    return module


def get_filepaths(folder_name: str) -> Dict[str, str]:
    job_paths = glob.glob(f"{_BASE_FOLDER}/{folder_name}/[!_]*.py")
    return {Path(filepath).stem: filepath for filepath in job_paths}


def parse_args() -> Dict[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument("-worker", required=False, type=str)
    parser.add_argument("-script", required=False, type=str)
    result = vars(parser.parse_args())
    return {k: v for k, v in result.items() if v}
