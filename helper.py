import logging
import sys


def set_logging(logging_level, logging_file):

	LOGGING_FILE = "UI.log"

	if logging_file:
		logging.basicConfig(
			filename=LOGGING_FILE, format="%(asctime)s - %(levelname)s - %(message)s"
		)

	root_logger = logging.getLogger()
	root_logger.setLevel(logging_level)
	handler = logging.StreamHandler(sys.stdout)
	handler.setLevel(logging_level)
	root_logger.addHandler(handler)
	formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
	handler.setFormatter(formatter)

	return root_logger
