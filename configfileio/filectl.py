from json import load, dump
import logging
async def read_file(lock, file):
    await lock.acquire()
    logging.debug(f"Acquired lock for file {file}")
    try:
        with open(file) as stream:
            output = load(stream)
    except Exception:
        logging.error(f"Error occurred trying to read {file}, aborting...")
        return
    finally:
        logging.debug(f"Lock for {file} released")
        lock.release()
    return output
