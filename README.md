# 🌤 GenLayer Weather + Price Sentinel

> A live Intelligent Contract on GenLayer that fetches real-world weather and crypto prices on-chain — no oracles, no middlemen, validated by AI-powered consensus.

---

## What is this?

This is an **Intelligent Contract** deployed on [GenLayer](https://genlayer.com) — the first AI-native blockchain that lets smart contracts directly access the internet and reason about real-world data.

In one contract, it:
- 🌍 Fetches **live weather** for 3 cities simultaneously (temperature + conditions)
- ₿ Fetches **live BTC, ETH, SOL prices** from Binance's public API
- 🎯 Fires a **price trigger** when BTC crosses a target — stored on-chain
- 🏆 Compares cities and reports the **hottest one**
- ✅ All data is validated by multiple independent AI validators via **Optimistic Democracy consensus** — no single point of failure

No Chainlink. No oracle fees. No API keys in the contract. Just Python + GenLayer.

---

## Why GenLayer?

Traditional smart contracts (Ethereum, Solana) cannot access the internet. They rely on oracles like Chainlink — external services that fetch data and push it on-chain, adding cost, latency, and trust assumptions.

GenLayer eliminates this:

| | Traditional Contracts | GenLayer Intelligent Contracts |
|---|---|---|
| Internet access | ❌ Needs oracle | ✅ Native |
| Real-world data | ❌ Oracle fees | ✅ Free |
| AI reasoning | ❌ Not possible | ✅ Built in |
| Language | Solidity / Rust | Python |
| Consensus | Deterministic only | Deterministic + Non-deterministic |

---

## Contract overview

```python
class WeatherPriceSentiment(gl.Contract):
    # Stores weather for 3 cities
    # Stores BTC, ETH, SOL prices
    # Fires trigger when BTC crosses target price
```

### Methods

| Method | Type | Description |
|---|---|---|
| `evaluate()` | write | Fetch all live data and update state |
| `get_result()` | view | Read latest weather + prices + trigger status |
| `is_triggered()` | view | Returns `true` if BTC crossed the target |
| `reset_trigger(new_target)` | write | Reset trigger with a new target price |

### Constructor args

| Arg | Type | Example |
|---|---|---|
| `city1` | str | `"Lagos"` |
| `city2` | str | `"London"` |
| `city3` | str | `"NewYork"` |
| `btc_target` | str | `"75000"` |

---

## Sample output

```json
{
  "prices": {
    "btc_usd": "71600",
    "eth_usd": "2110",
    "sol_usd": "89"
  },
  "trigger": {
    "target_usd": "75000",
    "triggered": false,
    "triggered_at": ""
  },
  "weather": {
    "lagos": { "temp_c": "29", "condition": "Patchy rain nearby" },
    "london": { "temp_c": "3",  "condition": "Overcast" },
    "new york": { "temp_c": "4",  "condition": "Clear" },
    "hottest": "lagos"
  }
}
```

---

## How consensus works

Every time `evaluate()` is called, here is what happens:

1. A **Leader validator** is selected randomly
2. The Leader fetches weather + prices and proposes a result
3. Multiple **Validator nodes** independently fetch the same data
4. If they agree → **consensus reached** → state is saved on-chain
5. If they disagree → **appeal process** → more validators are added

This is GenLayer's **Optimistic Democracy** — inspired by Condorcet's Jury Theorem. The more validators that agree, the more trustworthy the result.

Prices are rounded to the nearest $100 (BTC), $10 (ETH), and $1 (SOL) so that minor price ticks between validator calls don't break consensus.

---

## How to deploy

### 1. Open GenLayer Studio
Go to [studio.genlayer.com](https://studio.genlayer.com)

### 2. Create a new contract
Click **New Contract** in the sidebar and paste the contents of `weather_price_sentiment.py`

### 3. Deploy
Fill in constructor args and click **Deploy**

### 4. Run evaluate
Click **Send Transaction** under `evaluate` and wait for **FINALIZED**

### 5. Read results
Click **Call Contract** under `get_result`

---

## Files

```
├── weather_price_sentiment.py   # Main Intelligent Contract
└── README.md                    # This file
```

---

## Tech stack

- [GenLayer](https://genlayer.com) — AI-native blockchain
- [GenLayer Studio](https://studio.genlayer.com) — browser-based IDE
- [wttr.in](https://wttr.in) — free weather API
- [Binance Public API](https://api.binance.com) — free crypto prices
- Python — contract language

---

## What's next

- [ ] Frontend web app (genlayer-js)
- [ ] Social sentiment layer (HackerNews)
- [ ] Multi-asset trigger conditions
- [ ] Mainnet deployment when GenLayer launches

---

## License

MIT
