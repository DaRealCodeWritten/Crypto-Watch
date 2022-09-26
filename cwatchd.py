from json import load, dump
from flask import Flask, request


DAEMON_VERSION="v0.0.1"
urls = {
    True: "https://sandbox-api.coinmarketcap.com",
    False: "https://pro-api.coinmarketcap.com"
}
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

app.run("127.0.0.1", 5880)
