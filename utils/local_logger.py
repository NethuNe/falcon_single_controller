import os
from datetime import datetime
import json
#only imports local logging, as gCloud logging is prohibitively expensive
import logging as local_logging

logger = local_logging.getLogger(__name__)
logger.setLevel(10)


#Payload Struct {
#   "module": `module_name`
#   "code": `error_code`
#   "input": `user_input`
# }
#only one module initially, but good for scalability
def log(module, payload, level):
    payload["module"] = module
    content = json.dumps(payload)
    logger = local_logging.getLogger(module)
    if level == 50:
        logger.critical(content)
    elif level == 40:
        logger.error(content)
    elif level == 30:
        logger.warning(content)
    elif level == 20:
        logger.info(content)
    elif level == 10:
        logger.debug(content)
    else:
        logger.info(content)
