# v0.1.0
# { "Depends": "py-genlayer:latest" }
from genlayer import *
import json
import typing


class WeatherPriceSentiment(gl.Contract):
    # Cities
    city1: str
    city2: str
    city3: str
    last_temp1: str
    last_temp2: str
    last_temp3: str
    last_condition1: str
    last_condition2: str
    last_condition3: str
    hottest_city: str

    # Prices
    last_btc: str
    last_eth: str
    last_sol: str

    # Trigger
    btc_target: str
    triggered: bool
    triggered_at_price: str

    def __init__(self, city1: str, city2: str, city3: str, btc_target: str):
        self.city1 = city1
        self.city2 = city2
        self.city3 = city3
        self.last_temp1 = ""
        self.last_temp2 = ""
        self.last_temp3 = ""
        self.last_condition1 = ""
        self.last_condition2 = ""
        self.last_condition3 = ""
        self.hottest_city = ""
        self.last_btc = ""
        self.last_eth = ""
        self.last_sol = ""
        self.btc_target = btc_target
        self.triggered = False
        self.triggered_at_price = ""

    @gl.public.write
    def evaluate(self) -> typing.Any:
        city1 = self.city1
        city2 = self.city2
        city3 = self.city3

        # --- City 1 ---
        def get_weather1() -> typing.Any:
            raw = gl.nondet.web.render(
                f"https://wttr.in/{city1}?format=j1", mode="text"
            )
            data = json.loads(raw)
            cc = data["current_condition"][0]
            return json.dumps({
                "temp": cc["temp_C"],
                "condition": cc["weatherDesc"][0]["value"],
            }, sort_keys=True)

        w1 = json.loads(gl.eq_principle.strict_eq(get_weather1))

        # --- City 2 ---
        def get_weather2() -> typing.Any:
            raw = gl.nondet.web.render(
                f"https://wttr.in/{city2}?format=j1", mode="text"
            )
            data = json.loads(raw)
            cc = data["current_condition"][0]
            return json.dumps({
                "temp": cc["temp_C"],
                "condition": cc["weatherDesc"][0]["value"],
            }, sort_keys=True)

        w2 = json.loads(gl.eq_principle.strict_eq(get_weather2))

        # --- City 3 ---
        def get_weather3() -> typing.Any:
            raw = gl.nondet.web.render(
                f"https://wttr.in/{city3}?format=j1", mode="text"
            )
            data = json.loads(raw)
            cc = data["current_condition"][0]
            return json.dumps({
                "temp": cc["temp_C"],
                "condition": cc["weatherDesc"][0]["value"],
            }, sort_keys=True)

        w3 = json.loads(gl.eq_principle.strict_eq(get_weather3))

        # --- BTC ---
        def get_btc() -> typing.Any:
            raw = gl.nondet.web.render(
                "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
                mode="text"
            )
            data = json.loads(raw)
            return str(int(round(float(data["price"]) / 100) * 100))

        btc = gl.eq_principle.strict_eq(get_btc)

        # --- ETH ---
        def get_eth() -> typing.Any:
            raw = gl.nondet.web.render(
                "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT",
                mode="text"
            )
            data = json.loads(raw)
            return str(int(round(float(data["price"]) / 10) * 10))

        eth = gl.eq_principle.strict_eq(get_eth)

        # --- SOL ---
        def get_sol() -> typing.Any:
            raw = gl.nondet.web.render(
                "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT",
                mode="text"
            )
            data = json.loads(raw)
            return str(int(round(float(data["price"]))))

        sol = gl.eq_principle.strict_eq(get_sol)

        # --- Hottest city ---
        temps = {
            city1: int(w1["temp"]),
            city2: int(w2["temp"]),
            city3: int(w3["temp"]),
        }
        hottest = max(temps, key=lambda c: temps[c])

        # --- BTC trigger ---
        if int(btc) >= int(self.btc_target) and not self.triggered:
            self.triggered = True
            self.triggered_at_price = btc

        # --- Save state ---
        self.last_temp1 = w1["temp"]
        self.last_condition1 = w1["condition"]
        self.last_temp2 = w2["temp"]
        self.last_condition2 = w2["condition"]
        self.last_temp3 = w3["temp"]
        self.last_condition3 = w3["condition"]
        self.hottest_city = hottest
        self.last_btc = btc
        self.last_eth = eth
        self.last_sol = sol

        return {"btc": btc, "eth": eth, "sol": sol, "hottest": hottest}

    @gl.public.write
    def reset_trigger(self, new_target: str) -> None:
        self.triggered = False
        self.triggered_at_price = ""
        self.btc_target = new_target

    @gl.public.view
    def get_result(self) -> dict:
        return {
            "weather": {
                self.city1: {"temp_c": self.last_temp1, "condition": self.last_condition1},
                self.city2: {"temp_c": self.last_temp2, "condition": self.last_condition2},
                self.city3: {"temp_c": self.last_temp3, "condition": self.last_condition3},
                "hottest": self.hottest_city,
            },
            "prices": {
                "btc_usd": self.last_btc,
                "eth_usd": self.last_eth,
                "sol_usd": self.last_sol,
            },
            "trigger": {
                "target_usd": self.btc_target,
                "triggered": self.triggered,
                "triggered_at": self.triggered_at_price,
            },
        }

    @gl.public.view
    def is_triggered(self) -> bool:
        return self.triggered
