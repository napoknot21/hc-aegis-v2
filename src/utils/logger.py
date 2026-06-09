from __future__ import annotations

import functools
import logging
import datetime as dt
from pathlib import Path
from typing import Any, Callable, Optional

from src.config.parameters import (
    AEGIS_LOGGER_DATE_FORMAT, AEGIS_LOGGER_FILE_PREFIX,
    AEGIS_LOGGER_FORMAT, AEGIS_LOGGER_LOGS_DIR_NAME, AEGIS_LOGGER_NAME,
)


def get_project_root () -> Path :
    """
    
    """
    return Path(__file__).resolve().parents[2]


def get_logs_directory (
        
        logs_dir : Optional[str | Path] = None,
    
    ) -> Path :
    """
    
    """
    if logs_dir is None :
        logs_path = get_project_root() / AEGIS_LOGGER_LOGS_DIR_NAME
    else :
        logs_path = Path(logs_dir)

    logs_path.mkdir(parents=True, exist_ok=True)
    
    return logs_path


def get_log_file_path (
        
        logs_dir : Optional[str | Path] = None,
    
    ) -> Path :
    """
    
    """
    today = get_today_str()
    
    return get_logs_directory(logs_dir) / f"{AEGIS_LOGGER_FILE_PREFIX}_{today}.log"


def get_today_str () -> str :
    """
    
    """
    return dt.date.today().strftime("%Y-%m-%d")


def setup_logger (
        
        name : str = AEGIS_LOGGER_NAME,
        level : int = logging.INFO,
        logs_dir : Optional[str | Path] = None,
        console : bool = True,
        force : bool = False,
    
    ) -> logging.Logger :
    """
    
    """
    app_logger = logging.getLogger(name)
    app_logger.setLevel(level)
    app_logger.propagate = False

    if app_logger.handlers and not force :
        return app_logger

    if force :
        clear_handlers(app_logger)

    formatter = get_formatter()
    
    file_handler = get_file_handler(
        
        logs_dir=logs_dir,
        level=level,
        formatter=formatter,
    
    )
    app_logger.addHandler(file_handler)

    if console :
    
        console_handler = get_console_handler(
            
            level=level,
            formatter=formatter,
        
        )
        app_logger.addHandler(console_handler)

    return app_logger


def get_logger (
        
        module : Optional[str] = None,
    
    ) -> logging.Logger :
    """
    
    """
    setup_logger()
    
    if module is None :
        return logging.getLogger(AEGIS_LOGGER_NAME)
    
    return logging.getLogger(f"{AEGIS_LOGGER_NAME}.{module}")


def get_formatter () -> logging.Formatter :
    """
    
    """
    return logging.Formatter(
        
        fmt=AEGIS_LOGGER_FORMAT,
        datefmt=AEGIS_LOGGER_DATE_FORMAT,
    
    )


def get_file_handler (
        
        logs_dir : Optional[str | Path],
        level : int,
        formatter : logging.Formatter,
    
    ) -> logging.FileHandler :
    """
    
    """
    handler = logging.FileHandler(
        
        filename=get_log_file_path(logs_dir),
        encoding="utf-8",
    
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)
    
    return handler


def get_console_handler (
        
        level : int,
        formatter : logging.Formatter,
    
    ) -> logging.StreamHandler :
    """
    
    """
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)
    
    return handler


def clear_handlers (
        
        app_logger : logging.Logger,
    
    ) -> None :
    """
    
    """
    for handler in app_logger.handlers[:] :
    
        handler.close()
        app_logger.removeHandler(handler)

    return None


def log (
        
        message : Any,
        module : Optional[str] = None,
        level : int = logging.INFO,
        **context : Any,
    
    ) -> None :
    """
    
    """
    event_logger = get_logger(module)
    log_message = build_log_message(
        
        action=str(message),
        context=context,
    
    )
    
    event_logger.log(level, log_message)
    
    return None


def log_event (
        
        action : str,
        module : Optional[str] = None,
        level : int = logging.INFO,
        **context : Any,
    
    ) -> None :
    """
    
    """
    log(
        
        message=action,
        module=module,
        level=level,
        **context,
    
    )
    
    return None


def build_log_message (
        
        action : str,
        context : dict[str, Any],
    
    ) -> str :
    """
    
    """
    if not context :
        return action

    context_message = " | ".join(
        
        f"{key}={value}"
        for key, value in context.items()
    
    )
    
    return f"{action} | {context_message}"


def log_function_call (
        
        module : Optional[str] = None,
        level : int = logging.INFO,
    
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]] :
    """
    
    """
    def decorator (
            
            function : Callable[..., Any],
        
        ) -> Callable[..., Any] :
        """
        
        """
        @functools.wraps(function)
        def wrapper (
                
                *args : Any,
                **kwargs : Any,
            
            ) -> Any :
            """
            
            """
            event_logger = get_logger(module or function.__module__)
            event_logger.log(level, f"start | function={function.__name__}")
            
            try :
            
                result = function(*args, **kwargs)
                event_logger.log(level, f"success | function={function.__name__}")
                
                return result
            
            except Exception :
            
                event_logger.exception(f"error | function={function.__name__}")
                raise
        
        return wrapper
    
    return decorator


logger = setup_logger()
