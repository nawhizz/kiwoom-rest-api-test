is_paper_trading = True     # 모의투자 여부 : False 또는 True
api_key = "l8t1Yth3sQib3xho4dLAS7UlCSJhXA9RIEfqlFbDWI4"    # API KEY
api_secret_key = "5t6SvHqm2ZPzYAo5siM7bIwzQgVeP44WqvQhCACZMz8"  # API SECRET KEY

host = "https://mockapi.kiwoom.com" if is_paper_trading else "https://api.kiwoom.com"
websocket_url = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket" if is_paper_trading else "wss://api.kiwoom.com:10000/api/dostk/websocket"