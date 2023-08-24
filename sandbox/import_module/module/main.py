from sandbox.import_module.settings import S, create_logger
log = create_logger(__file__, S.LOG_LEVEL)
log.info("Hello")