import logging
import os
import pathlib
import sys
import time
import typing

if __name__ != '__main__':
    from __main__ import __file__ as __main_file__
else:
    __main_file__ = __file__

logger = logging.getLogger("livoxsdk")

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.getLogger().critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


level_width = max([len(v) for v in logging._levelToName.values()] + [len(k) for k in logging._nameToLevel.keys()])
DefaultFormatter = logging_formater = logging.Formatter("[%(levelname){}s] %(asctime)s | %(name)s: %(message)s".format(level_width))
SimpleFormatter = logging.Formatter("%(name)s: %(message)s")

def SetupDefaultLogger(log_file_prefix: typing.Optional[pathlib.Path] = None,
                       ostream_level: typing.Optional[int] = logging.INFO,
                       logfile_level: typing.Optional[int] = logging.INFO,
                       remove_existing_file_handlers: bool = False,
                       use_simple_console_format: bool = False):
    if ostream_level is not None or logfile_level is not None:
        levels = [logging.getLogger().level]
        if ostream_level is not None:
            levels.append(ostream_level)
        if logfile_level is not None:
            levels.append(logfile_level)
        logging.getLogger().setLevel(min(levels))

    if ostream_level is not None:
        if not any([isinstance(h, logging.StreamHandler) for h in logging.getLogger().handlers]):
            ostream_handler = logging.StreamHandler(sys.stdout)
            if use_simple_console_format:
                ostream_handler.setFormatter(SimpleFormatter)
            else:
                ostream_handler.setFormatter(DefaultFormatter)
            logging.getLogger().addHandler(ostream_handler)
        [h.setLevel(ostream_level) for h in logging.getLogger().handlers if isinstance(h, logging.StreamHandler)]

    if remove_existing_file_handlers:
        logging.getLogger().handlers = [h for h in logging.getLogger().handlers
                                        if not isinstance(h, logging.FileHandler)]
    if logfile_level is not None and (len(logging.getLogger().handlers) > 0 or log_file_prefix is not None):
        if log_file_prefix.suffix == ".log":
            if log_file_prefix.exists():
                logging.getLogger("SetupLogging").warning("Overwriting existing logfile {}".format(log_file_prefix))
            file_handler = logging.FileHandler(log_file_prefix)
            file_handler.setFormatter(logging_formater)
            logging.getLogger().addHandler(file_handler)
        else:
            timed_logfile = log_file_prefix.joinpath(
                time.strftime("{}_%Y%m%d-%H%M%S.log".format(pathlib.Path(__main_file__).stem)))
            logfile_symlink = log_file_prefix.joinpath("{}.log".format(pathlib.Path(__main_file__).stem))
            file_handler = logging.FileHandler(timed_logfile)
            file_handler.setFormatter(logging_formater)
            logging.getLogger().addHandler(file_handler)
            if logfile_symlink.exists() and logfile_symlink.is_symlink():
                logfile_symlink.unlink()
            if os.name != "nt":  # Windows does not support soft links
                logfile_symlink.symlink_to(timed_logfile)
        [h.setLevel(logfile_level) for h in logging.getLogger().handlers if isinstance(h, logging.FileHandler)]
