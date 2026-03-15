# I Built a Smart Contract That Reads the Internet — No Oracles Needed

*How GenLayer lets you write Intelligent Contracts in Python that fetch live data, reason about the world, and reach consensus across AI validators*

---

If you've ever tried to build a smart contract that reacts to real-world data — a price feed, a weather event, a sports result — you know the pain. You need an oracle. You pay oracle fees. You trust that oracle not to fail. You write Solidity.

I wanted to build something different. A contract that fetches live Bitcoin prices, current weather conditions for multiple cities, and fires a trigger when BTC hits a target — all on-chain, all verified by consensus, with no oracle service in the middle.

This is how I built it on GenLayer.

---

## What is GenLayer?

GenLayer is the first AI-native blockchain. Instead of the usual deterministic execution model — where every node must compute exactly the same result — GenLayer lets smart contracts do things traditional blockchains cannot:

- **Fetch live data from the internet** directly inside the contract
- **Call LLMs** to reason about qualitative information
- **Reach consensus on non-deterministic results** through a mechanism called Optimistic Democracy

The contracts are written in Python (not Solidity), and they run inside GenVM — a sandboxed environment where each validator independently executes the contract and votes on the result.

Think of it this way:

> Bitcoin is trustless money. Ethereum is trustless applications. GenLayer is trustless decision-making.

---

## The problem with oracles

On Ethereum, if your contract needs the current BTC price, you call a Chainlink price feed. Chainlink fetches the data off-chain and pushes it on-chain. You pay for this. You trust Chainlink. If Chainlink goes down, your contract breaks.

GenLayer eliminates this entirely. Your contract fetches the data directly — and multiple independent validators verify it reached the same result.

---

## What I built

A single Intelligent Contract that does all of this on every call:

1. Fetches live weather for **3 cities** (Lagos, London, New York) from wttr.in
2. Fetches live prices for **BTC, ETH, and SOL** from Binance's public API
3. Compares city temperatures and reports the **hottest city**
4. Checks if BTC has crossed a **target price** and fires a trigger
5. Stores everything on-chain, validated by multiple AI-powered validators

Here is a sample result:

```json
{
  "prices": {
    "btc_usd": "71600",
    "eth_usd": "2110",
    "sol_usd": "89"
  },
  "weather": {
    "lagos":    { "temp_c": "29", "condition": "Patchy rain nearby" },
    "london":   { "temp_c": "3",  "condition": "Overcast" },
    "new york": { "temp_c": "4",  "condition": "Clear" },
    "hottest":  "lagos"
  },
  "trigger": {
    "target_usd": "75000",
    "triggered": false
  }
}
```

All of that — fetched live, validated on-chain, stored in contract state.

---

## How the code works

GenLayer contracts are Python classes that extend `gl.Contract`. Here is the core pattern:

```python
from genlayer import *
import json
import typing

class WeatherPriceSentiment(gl.Contract):
    city1: str
    last_btc: str
    triggered: bool

    def __init__(self, city1: str, btc_target: str):
        self.city1 = city1
        self.last_btc = ""
        self.triggered = False

    @gl.public.write
    def evaluate(self) -> typing.Any:

        def get_btc() -> typing.Any:
            raw = gl.nondet.web.render(
                "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
                mode="text"
            )
            data = json.loads(raw)
            return str(int(round(float(data["price"]) / 100) * 100))

        self.last_btc = gl.eq_principle.strict_eq(get_btc)
```

Two things to notice:

**1. Web fetches live inside the contract**
`gl.nondet.web.render()` fetches any URL directly. No oracle. No external service. The contract reaches out to the internet itself.

**2. The equivalence principle**
`gl.eq_principle.strict_eq()` wraps the fetch in a consensus check. Each validator independently runs the inner function and compares results. If they match exactly — consensus. If not — the appeal process kicks in with more validators.

This is how GenLayer handles non-determinism. The price might tick by $1 between validator calls, so I round BTC to the nearest $100 — all validators then agree on the same rounded value.

---

## The consensus mechanism

Every `evaluate()` call goes through this process:

1. A **Leader validator** is randomly selected
2. The Leader fetches the data and proposes a result
3. Multiple **Validator nodes** independently re-run the contract
4. If the majority agrees → **FINALIZED** → state saved on-chain
5. If they disagree → **appeal** → more validators added, bond posted

This is **Optimistic Democracy**, based on Condorcet's Jury Theorem: the more independent validators that agree, the more trustworthy the result.

In my testing, the weather data reached consensus easily. The BTC price required rounding to the nearest $100 to ensure validators fetching milliseconds apart got the same value.

---

## What surprised me

**No oracle fees.** I was used to paying for Chainlink calls. Here there's nothing — the data fetch is part of the contract execution.

**Python, not Solidity.** The barrier to entry is massively lower. Any Python developer can write an Intelligent Contract.

**The LLM layer.** You can call `gl.nondet.exec_prompt()` inside a contract to have an LLM reason about the data you've fetched. I used this to generate natural language summaries of conditions. The validators run the LLM call independently and reach consensus on the output using `prompt_non_comparative` — meaning they agree on the *meaning*, not the exact wording.

**The storage type system.** This caught me. GenLayer doesn't support plain Python `int` or `float` in contract storage fields. You need `u256`, `u64`, `f64` etc. I sidestepped this entirely by storing everything as `str` — numbers as strings — which works cleanly and avoids the type system entirely for now.

---

## How to try it yourself

1. Go to [studio.genlayer.com](https://studio.genlayer.com)
2. Create a new contract file
3. Paste the contract from the GitHub repo (link below)
4. Deploy with your chosen cities and BTC target
5. Call `evaluate()` and watch live data appear on-chain

The full contract code is on GitHub: **[link to your repo]**

---

## What's next

This is just the foundation. The same pattern can power:

- **Prediction markets** — resolve automatically when real-world events happen
- **Parametric insurance** — pay out when weather conditions are met
- **DeFi triggers** — execute trades when multiple market conditions align
- **DAO governance** — let AI validators reason about qualitative proposals

GenLayer mainnet isn't live yet — this is all on the simulator — but the programming model is already production-quality. When mainnet launches, the same contract deploys unchanged.

I'm building a frontend next so anyone can interact with the contract without touching the Studio. Follow along on GitHub.

---

*Built with GenLayer Studio · wttr.in · Binance Public API · Python*

*GitHub: [your repo link]*
*Twitter/X: [your handle]*
