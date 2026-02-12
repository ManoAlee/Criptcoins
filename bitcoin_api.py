#!/usr/bin/env python3
"""
Bitcoin Real-Time API Integration
Integração com APIs reais de Bitcoin para preços, blockchain e trading
"""
import requests
import json
import time
from typing import Dict, Optional, List
import websocket
import threading

class BitcoinAPI:
    """API para dados Bitcoin em tempo real"""
    
    def __init__(self):
        self.base_urls = {
            'coinbase': 'https://api.coinbase.com/v2',
            'blockchain': 'https://blockchain.info',
            'coingecko': 'https://api.coingecko.com/api/v3',
            'binance': 'https://api.binance.com/api/v3'
        }
        self.ws_url = 'wss://stream.binance.com:9443/ws/btcusdt@ticker'
        self.current_price = None
        self.ws = None
        self.ws_thread = None
    
    def get_current_price(self, currency: str = 'USD') -> Optional[float]:
        """Obtém preço atual do Bitcoin"""
        try:
            # Tentar múltiplas APIs para redundância
            
            # 1. CoinGecko (sem necessidade de API key)
            url = f"{self.base_urls['coingecko']}/simple/price"
            params = {
                'ids': 'bitcoin',
                'vs_currencies': currency.lower()
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data['bitcoin'][currency.lower()]
            
            # 2. Blockchain.info
            url = f"{self.base_urls['blockchain']}/ticker"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data[currency]['last']
            
            # 3. Coinbase
            url = f"{self.base_urls['coinbase']}/prices/BTC-{currency}/spot"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return float(data['data']['amount'])
                
        except Exception as e:
            print(f"[⚠️] Erro ao obter preço: {e}")
            return None
    
    def get_market_data(self) -> Optional[Dict]:
        """Obtém dados completos do mercado"""
        try:
            url = f"{self.base_urls['coingecko']}/coins/bitcoin"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'community_data': 'false',
                'developer_data': 'false'
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                market = data['market_data']
                
                return {
                    'price_usd': market['current_price']['usd'],
                    'price_brl': market['current_price']['brl'],
                    'market_cap': market['market_cap']['usd'],
                    'volume_24h': market['total_volume']['usd'],
                    'change_24h': market['price_change_percentage_24h'],
                    'change_7d': market['price_change_percentage_7d'],
                    'change_30d': market['price_change_percentage_30d'],
                    'high_24h': market['high_24h']['usd'],
                    'low_24h': market['low_24h']['usd'],
                    'ath': market['ath']['usd'],
                    'ath_date': market['ath_date']['usd'],
                    'circulating_supply': market['circulating_supply'],
                    'total_supply': market['total_supply'],
                    'max_supply': market['max_supply']
                }
        except Exception as e:
            print(f"[⚠️] Erro ao obter dados de mercado: {e}")
            return None
    
    def get_blockchain_stats(self) -> Optional[Dict]:
        """Obtém estatísticas da blockchain Bitcoin"""
        try:
            url = f"{self.base_urls['blockchain']}/stats"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'hash_rate': data.get('hash_rate', 0),
                    'difficulty': data.get('difficulty', 0),
                    'total_btc': data.get('totalbc', 0) / 1e8,
                    'n_btc_mined': data.get('n_btc_mined', 0) / 1e8,
                    'miners_revenue': data.get('miners_revenue_usd', 0),
                    'market_price': data.get('market_price_usd', 0),
                    'total_transactions': data.get('n_tx', 0),
                    'blocks_size': data.get('blocks_size', 0),
                    'avg_block_size': data.get('avgblocksize', 0),
                    'next_retarget': data.get('nextretarget', 0)
                }
        except Exception as e:
            print(f"[⚠️] Erro ao obter stats blockchain: {e}")
            return None
    
    def get_latest_blocks(self, limit: int = 10) -> Optional[List[Dict]]:
        """Obtém últimos blocos minerados"""
        try:
            url = f"{self.base_urls['blockchain']}/blocks"
            params = {'format': 'json'}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                blocks = []
                for block in data['blocks'][:limit]:
                    blocks.append({
                        'hash': block['hash'],
                        'height': block['height'],
                        'time': block['time'],
                        'tx_count': block['n_tx'],
                        'size': block['size'],
                        'miner': block.get('relayed_by', 'Unknown')
                    })
                return blocks
        except Exception as e:
            print(f"[⚠️] Erro ao obter blocos: {e}")
            return None
    
    def start_websocket(self, callback):
        """Inicia WebSocket para preços em tempo real"""
        def on_message(ws, message):
            try:
                data = json.loads(message)
                price = float(data.get('c', 0))  # Current price
                if price > 0:
                    self.current_price = price
                    callback(price, data)
            except Exception as e:
                print(f"[⚠️] Erro WebSocket message: {e}")
        
        def on_error(ws, error):
            print(f"[⚠️] WebSocket error: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            print("[ℹ️] WebSocket fechado. Reconectando em 5s...")
            time.sleep(5)
            self.start_websocket(callback)
        
        def on_open(ws):
            print("[✅] WebSocket Bitcoin conectado!")
        
        def run_ws():
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            self.ws.run_forever()
        
        self.ws_thread = threading.Thread(target=run_ws, daemon=True)
        self.ws_thread.start()
    
    def stop_websocket(self):
        """Para o WebSocket"""
        if self.ws:
            self.ws.close()
    
    def get_historical_data(self, days: int = 30) -> Optional[Dict]:
        """Obtém dados históricos de preço"""
        try:
            url = f"{self.base_urls['coingecko']}/coins/bitcoin/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'prices': data['prices'],
                    'market_caps': data['market_caps'],
                    'volumes': data['total_volumes']
                }
        except Exception as e:
            print(f"[⚠️] Erro ao obter dados históricos: {e}")
            return None
    
    def search_transaction(self, tx_hash: str) -> Optional[Dict]:
        """Busca uma transação na blockchain real"""
        try:
            url = f"{self.base_urls['blockchain']}/rawtx/{tx_hash}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'hash': data['hash'],
                    'size': data['size'],
                    'time': data['time'],
                    'block_height': data.get('block_height', 0),
                    'inputs': len(data['inputs']),
                    'outputs': len(data['out']),
                    'value': sum(out['value'] for out in data['out']) / 1e8
                }
        except Exception as e:
            print(f"[⚠️] Erro ao buscar transação: {e}")
            return None


class TradingEngine:
    """Motor de trading automatizado"""
    
    def __init__(self, api: BitcoinAPI):
        self.api = api
        self.positions = []
        self.balance_usd = 10000.0  # Saldo inicial simulado
        self.balance_btc = 0.0
        self.trade_history = []
    
    def buy_bitcoin(self, amount_usd: float) -> bool:
        """Compra Bitcoin"""
        try:
            price = self.api.get_current_price()
            if not price:
                return False
            
            btc_amount = amount_usd / price
            
            if self.balance_usd >= amount_usd:
                self.balance_usd -= amount_usd
                self.balance_btc += btc_amount
                
                trade = {
                    'type': 'BUY',
                    'amount_usd': amount_usd,
                    'amount_btc': btc_amount,
                    'price': price,
                    'timestamp': time.time()
                }
                self.trade_history.append(trade)
                print(f"[✅] COMPRA: ${amount_usd:.2f} = {btc_amount:.8f} BTC @ ${price:.2f}")
                return True
            
            return False
        except Exception as e:
            print(f"[❌] Erro na compra: {e}")
            return False
    
    def sell_bitcoin(self, btc_amount: float) -> bool:
        """Vende Bitcoin"""
        try:
            price = self.api.get_current_price()
            if not price:
                return False
            
            usd_amount = btc_amount * price
            
            if self.balance_btc >= btc_amount:
                self.balance_btc -= btc_amount
                self.balance_usd += usd_amount
                
                trade = {
                    'type': 'SELL',
                    'amount_btc': btc_amount,
                    'amount_usd': usd_amount,
                    'price': price,
                    'timestamp': time.time()
                }
                self.trade_history.append(trade)
                print(f"[✅] VENDA: {btc_amount:.8f} BTC = ${usd_amount:.2f} @ ${price:.2f}")
                return True
            
            return False
        except Exception as e:
            print(f"[❌] Erro na venda: {e}")
            return False
    
    def get_portfolio_value(self) -> float:
        """Retorna valor total do portfólio"""
        price = self.api.get_current_price() or 0
        return self.balance_usd + (self.balance_btc * price)
    
    def get_profit_loss(self) -> float:
        """Retorna lucro/prejuízo"""
        initial = 10000.0
        current = self.get_portfolio_value()
        return current - initial


# Exemplo de uso
if __name__ == '__main__':
    print("🌌 Galaxy Bitcoin API - Teste de Integração\n")
    
    api = BitcoinAPI()
    
    # Testar preço atual
    print("📊 Obtendo preço atual...")
    price = api.get_current_price()
    if price:
        print(f"   Bitcoin: ${price:,.2f} USD\n")
    
    # Testar dados de mercado
    print("📈 Obtendo dados de mercado...")
    market = api.get_market_data()
    if market:
        print(f"   Preço: ${market['price_usd']:,.2f}")
        print(f"   Market Cap: ${market['market_cap']:,.0f}")
        print(f"   Volume 24h: ${market['volume_24h']:,.0f}")
        print(f"   Mudança 24h: {market['change_24h']:.2f}%\n")
    
    # Testar blockchain stats
    print("⛓️ Obtendo stats da blockchain...")
    stats = api.get_blockchain_stats()
    if stats:
        print(f"   Total BTC: {stats['total_btc']:,.0f}")
        print(f"   Dificuldade: {stats['difficulty']:,.0f}")
        print(f"   Hash Rate: {stats['hash_rate']:,.0f} TH/s\n")
    
    # Testar últimos blocos
    print("🔨 Últimos blocos minerados...")
    blocks = api.get_latest_blocks(3)
    if blocks:
        for block in blocks:
            print(f"   Bloco #{block['height']}: {block['tx_count']} txs, {block['size']} bytes")
    
    print("\n✅ Testes concluídos!")
