def get_logger(module_name: str):  # type: ignore
    from structlog import get_logger

    logger_object = get_logger(module_name)
    return logger_object.bind(module=module_name)