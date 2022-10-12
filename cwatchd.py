import sys
import logging
from configfileio import filectl
from rich.logging import RichHandler
from asyncio import run, Lock
from aiohttp import ClientSession
from json import load, dump
from flask import Flask, request
format = "%(message)s"
logging.basicConfig(
    level=logging.DEBUG,
    format=format,
    datefmt="[%X]",
    handlers=[RichHandler(),]
)


async def deinit_ws():
    global api
    logging.info("Deinitializing API ClientSession")
    await api.close()


async def init_ws(url):
    logging.info("Initializing aiohttp ClientSession")
    return ClientSession(url)


DAEMON_VERSION="v0.0.1"
urls = {
    True: "https://sandbox-api.coinmarketcap.com",
    False: "https://pro-api.coinmarketcap.com"
}
filelock = Lock()

apiurl = urls["--test" in sys.argv]
logging.info(f"Set API url to {apiurl}")
api = run(init_ws(apiurl))
app = Flask(__name__)


@app.route("/version")
async def version():
    return DAEMON_VERSION, 200


@app.route("/interact/bought", methods=["POST",])
async def bought():
    data = request.json
    quantity = data.get("quantity")
    currency = data.get("currency")
    if None in [quantity, currency]:
        return {"message": "Invalid JSON data or format"}, 400
    # TODO: Add DB handler
    return "NOT_IMPLEMENTED", 501


@app.route("/compatibility")
async def check_compatibility():
    client = request.json.get("version")
    if client is None:
        return {"message": "Invalid JSON data or format"}, 400
    try:
        major, minor, patch = (client.strip("v")).split(".")
    except:
        return {"message": "Client version format not valid"}, 400
    daemon = DAEMON_VERSION.split(".")
    if daemon[0].strip("v") != major:
        return {
            "message": "Version check failed, MAJOR is out of date",
            "result": "MAJOR_MISMATCH"
        }, 200
    elif daemon[1] != minor:
        return {
            "message": "Version check warning, MINOR is out of date",
            "result": "MINOR_MISMATCH"
        }, 200
    return {
        "message": "Version check OK",
        "result": "OK"
    }, 200


@app.route("/debug/fileerror")
async def filereaderror():
    await filectl.read_file(filelock, "Joe Mama")
    return "", 204


logging.info("Spinning up webserver...")
app.run("127.0.0.1", 5880)
run(deinit_ws())
