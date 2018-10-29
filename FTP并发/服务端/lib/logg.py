def logg(info):
    import logging
    logger = logging.getLogger('info')
    logger.setLevel(logging.DEBUG)
    log_file = '服务端.log'
    file_log = logging.FileHandler(log_file)
    logger.addHandler(file_log)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_log.setFormatter(file_formatter)
    logger.debug(info)