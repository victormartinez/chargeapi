import asyncio

from infrastructure import logging
from chargeapi.exec.main import get_filepaths, load_file, parse_args

logger = logging.get_logger(__name__)


async def run_forever(job):  # type: ignore
    while True:
        try:
            logger.info("running job", job=job)
            await job.process()
        except Exception as exc:
            logger.error("error while executing worker", exc=exc)


if __name__ == "__main__":
    args = parse_args()
    folder_name, file_name = args.popitem()
    jobs = get_filepaths(folder_name)
    found_script = {name: fpath for name, fpath in jobs.items() if file_name == name}
    if not found_script:
        raise ValueError("Executable not found")

    name, path = found_script.popitem()
    job = load_file(name, path)
    if folder_name == "worker":
        logger.info("starting worker process", name=file_name)
        asyncio.run(run_forever(job))  # type: ignore
    else:
        logger.info("starting script", name=file_name)
        asyncio.run(job.process())  # type: ignore
