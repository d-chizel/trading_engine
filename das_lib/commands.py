import socket
import uuid
import asyncio
from datetime import datetime, timedelta
import pandas as pd
from time import sleep


class CmdAPI:
    def __init__(self, df):
        self.uniq = uuid.uuid4()
        self.ticker_df = df
        self.positions_df = pd.DataFrame()

    async def check_for_input():
        try:
            while True:
                userInput = await asyncio.get_event_loop().run_in_executor(None, input, "\nTo leave enter: 1\n")
                if (userInput == "1"):
                    print("\nLeaving.\n")
                    return
        except Exception as e:
            print(f"\nException: {e}\n")

    #Method:get_bid_ask_price
    def get_bid_ask_price(self, connection, level="Lv1", symbol=""):
        quote = self.subscribe(connection, level, symbol)
        quote_array = quote.split(" ")
        for index, item in enumerate(quote_array):
            if item.find("$Quote") != -1:
                quote_index = index
                ask_price = float(quote_array[quote_index + 2].split(":")[1])
                bid_price = float(quote_array[quote_index + 4].split(":")[1])
        sleep(0.5)

        return {"ask_price": ask_price, "bid_price": bid_price}

    #Method:Subscribe
    def subscribe(self, connection, level="Lv1", symbol=""):
        actualLvl = ""
        
        if(level == "1" or level.upper() == "LV1" or level.upper() == "LEVEL1"):
            actualLvl = "Lv1"
        elif(level == "2" or level.upper() == "LV2" or level.upper() == "LEVEL2"):
            actualLvl = "Lv2"
        elif(level == "3" or level.upper() == "LV3" or level.upper() == "LEVEL3" or level.upper() == "TMS" or level.upper() == "T"):
            actualLvl = "tms"           
        else:
            print("\nPlease input a valid level, LV1, LV2, or LV3.\n")
            return

        script = f"ReturnFullLv1 YES\nSB {symbol.upper()} {actualLvl}\r\n"
        unsub_script = f"UNSB {symbol.upper()} {actualLvl}\r\n"
        retdata = ""
        
        try:
            found_a_quote = False
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            while not found_a_quote:
                quote_array = retdata.split(" ")
                for index, item in enumerate(quote_array):
                    if item.find("$Quote") != -1:
                        found_a_quote = True
                sleep(0.5)
            print(retdata)
            print("Unsubscribing...")
            retdata2 = connection.send_script(bytearray(unsub_script, encoding = "ascii"))
            return retdata
            
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")
            
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")
            
        except Exception as e:
            print(f"\nException: {e}")

        finally:
            return retdata
            #connection.send_script(bytearray(f"UNSB {symbol.upper()} {actualLvl}\r\n", encoding = "ascii")) #Unsub from symbol
        #End Block
    
    #Method:Subscribe Top List
    async def top_list(self, connection):
        script = "SB TOPLIST"
        print(f"\nSending {script}\nNOTE: May take a Minute to load.\nLOADING DATA...\n")
        checkInput = asyncio.create_task(self.check_for_input())
        datStream = True
        retdata = ""                             #Ensure buffer is empty
        
        try:
            while(datStream):
                if(retdata == ""):
                    retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                    if(retdata == ""):
                        print("...")
                else:
                    retdata += connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                    print(f"\n{retdata}")
                
                done, pending = await asyncio.wait([checkInput], timeout = 0, return_when=asyncio.FIRST_COMPLETED) #//First paramter - checkInput which holds the thread, timeout = 0 checks if the task is complete without blocking the loop, return_when first completed literally returns the result as soon as the task is completed.
                if(checkInput in done):
                    datStream = False
                    checkInput.cancel()
                    await checkInput
                            
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")
        except Exception as e:
            print(f"\nException: {e}")
        finally:
            checkInput.cancel()
            await checkInput
            retdata = ""                            #Empty the buffer
            connection.send_script(bytearray(f"UNSB TOPLIST\r\n", encoding = "ascii")) #// Unsubscribe from the symbol
        #End Block

    #Method:Get Account Details
    def account_details(self, connection, detail_type=""):
        inp = input("\nFor Buying Power\t\t(Enter: 1)\n    Positions\t\t\t(Enter: 2)\n    Orders\t\t\t(Enter: 3)\n    Trades\t\t\t(Enter: 4)\n    Route Status\t\t(Enter: 5)\n    LDLU\t\t\t(Enter: 6)\n    Symbol Status\t\t(Enter: 7)\n    Account Info\t\t(Enter: 8)\n\n    Input: ")
        script = ""

        if(detail_type == "1" or detail_type.upper() == "B" or detail_type.upper() == "P" or detail_type.upper() == "BP" or detail_type.upper() == "BUYINGPOWER"):
            script = "GET BP\r\n"
        elif(detail_type == "2" or detail_type.upper() == "P" or detail_type.upper() == "POS" or detail_type.upper() == "POSITION" or detail_type.upper() == "POSITIONS"):
            script = "GET POSITIONS\r\n"
        elif(detail_type == "3" or detail_type.upper() == "O" or detail_type.upper() == "ORD" or detail_type.upper() == "ORDER" or detail_type.upper() == "ORDERS"):
            script = "GET ORDERS\r\n"
        elif(detail_type == "4" or detail_type.upper() == "T" or detail_type.upper() == "TR" or detail_type.upper() == "TRADE" or detail_type.upper() == "TRADES"):
            script = "GET TRADES\r\n"
        elif(detail_type == "5" or detail_type.upper() == "R" or detail_type.upper() == "ROUTE" or detail_type.upper() == "ROUTESTATUS" or detail_type.upper() == "ROUTE STATUS"):
            script = "GET ROUTESTATUS\r\n"
        elif(detail_type == "6" or detail_type.upper() == "A" or detail_type.upper() == "AI" or detail_type.upper() == "ACC" or detail_type.upper() == "IFO" or detail_type.upper() == "INFO" or detail_type.upper() == "AINFO" or detail_type.upper() == "ACCINFO" or detail_type.upper() == "ACCOUNTINFO" or detail_type.upper() == "ACCOUNT INFO"):
            script = "GET AccountInfo\r\n"
        else:
            print("\nNot one of the options.\n")
            return

        try: 
            print(f"\nSending {script}")
            retdata = connection.send_script(bytearray(script, encoding = "ascii"))
        
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")
        except Exception as e:
            print(f"\nException: {e}")
        finally:
            if retdata:
                print(f"\nRecieved Data:\n{retdata}\n")
            else:
                print("")
                
    def update_positions(self, connection):
        script = "GET POSITIONS\r\n"

        try: 
            print(f"\nSending {script}")
            retdata = connection.send_script(bytearray(script, encoding = "ascii"))
            retdata_array = retdata.split()
            all_positions = [retdata_array[i:i+10] for i in range(0, len(retdata_array), 10)]
            headers = all_positions[:1][0]  # Remove the header row from data
            all_positions = all_positions[1:-1] # Remove the header row

            self.positions_df = pd.DataFrame(all_positions, columns=headers)
            self.positions_df['avgcost'] = self.positions_df['avgcost'].astype('float')
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")            
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")            
        except Exception as e:
            print(f"\nException: {e}")            
        finally:
            if retdata:
                print(f"Recieved Data:\n{self.positions_df}\n")
            else:
                print("")
                
    #Method: Update ticker_df with current positions
    def update_df_with_positions(self, connection):
        self.update_positions(connection)
        self.ticker_df['in_position'] = False
        self.ticker_df['ave_price'] = 0.0
        #self.ticker_df['ave_price'] = self.ticker_df['ave_price'].astype('float')
        self.ticker_df['shares_in_position'] = 0

        if self.positions_df is not None and not self.positions_df.empty:
            for idx, pos_row in self.positions_df.iterrows():
                ticker_in_position_not_in_ticker_df = True
                ticker = pos_row['symb'].upper()
                for idx2, ticker_row in self.ticker_df.iterrows():
                    if ticker == ticker_row['ticker']:
                        ticker_in_position_not_in_ticker_df = False
                        if int(pos_row['qty']) > 0:
                            self.ticker_df.at[idx2, 'in_position'] = True
                        else:
                            self.ticker_df.at[idx2, 'in_position'] = False
                        self.ticker_df.at[idx2, 'ave_price'] = (pos_row['avgcost'])
                        self.ticker_df.at[idx2, 'shares_in_position'] = int(pos_row['qty'])
                if ticker_in_position_not_in_ticker_df:
                    if int(pos_row['qty']) > 0:
                        ticker_in_position = True
                    else:
                        ticker_in_position = False
                    # Add a new row for a ticker that exists in positions_df but not in ticker_df
                    new_row = {
                        'ticker': ticker,
                        'in_position': ticker_in_position,
                        'ave_price': float(pos_row.get('avgcost', 0.0)),
                        'shares_in_position': int(pos_row.get('qty', 0)),
                        # sensible defaults for commonly referenced columns elsewhere in the class
                        'last_quote_bid': 0.0,
                        'last_quote_ask': 0.0,
                        'shares_to_locate': 0,
                        'short_size': 0.0,
                        'volume': 0,
                        'locate_order_status': 'Accepted!',
                        'total_locate_cost': 0.0,
                        'locate_price': 0.0,
                        'route': 'None',
                        'locate_available': False,
                        'shares_to_short': int(pos_row.get('qty', 0)),
                        'pre_locate_check_passed': False,
                        'pre_trade_check_passed': False
                    }

                    # Append the new row to the ticker_df
                    self.ticker_df = pd.concat([self.ticker_df, pd.DataFrame([new_row])], ignore_index=True)

    #Method:Get Symbol Status Details
    def symbol_status_details(self, connection, detail_type=""):
        inp = input("\nFor Buying Power\t\t(Enter: 1)\n    Positions\t\t\t(Enter: 2)\n    Orders\t\t\t(Enter: 3)\n    Trades\t\t\t(Enter: 4)\n    Route Status\t\t(Enter: 5)\n    LDLU\t\t\t(Enter: 6)\n    Symbol Status\t\t(Enter: 7)\n    Account Info\t\t(Enter: 8)\n\n    Input: ")
        script = ""

        if(detail_type == "1" or detail_type.upper() == "L" or detail_type.upper() == "LD" or detail_type.upper() == "LU" or detail_type.upper() == "LDLU"):
            symb = input("\n    Enter Symbol: ")
            script = f"GET LDLU {symb.upper()}\r\n"
        elif(detail_type == "2" or detail_type.upper() == "S" or detail_type.upper() == "SS" or detail_type.upper() == "SYM" or detail_type.upper() == "STAT" or detail_type.upper() == "SYMBOL" or detail_type.upper() == "STATUS" or detail_type.upper() == "SYMBOLSTATUS" or detail_type.upper() == "SYMBOL STATUS"):
            symb = input("\n    Enter Symbol: ")
            script = f"GET SymStatus {symb.upper()}\r\n"
        else:
            print("\nNot one of the options.\n")
            return

        try: 
            print(f"\nSending {script}")
            retdata = connection.send_script(bytearray(script, encoding = "ascii"))
        
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")
            
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")
            
        except Exception as e:
            print(f"\nException: {e}")
            
        finally:
            
            if retdata:
                print(f"Recieved Data:\n{retdata}\n")
            else:
                print("")
                
    #--------------------------------------------------TRADING COMMANDS--------------------------------------------------#
    #Method: New Order buy for testing
    def create_buy_new_order(self, connection, symbol, shares_to_short, price, route="XALL", tif="DAY+"):
            unID = int(self.uniq)
            script = f"NEWORDER {unID} B {symbol.upper()} {route} {shares_to_short} {price} {tif.upper()}"
            print (f"Sending {script}")
            try:
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                
            except socket.timeout as e:
                print(f"Timeout error: {e}")
            except socket.error as e:
                print(f"General socket error: {e}")
            except Exception as e:
                print(f"Exception: {e}")
            finally:
                print(f"{retdata}")
    
    #Method:NewOrder for short sell
    async def short_sell_market_new_order(self, connection, symbol, shares_to_short, route="SMAT", tif="DAY"):
        unID = int(self.uniq)
        script = f"NEWORDER {unID} SS {symbol.upper()} {route} {shares_to_short} MKT {tif.upper()}"
        print (f"Sending {script}")
        try:
            retdata = await connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            
        except socket.timeout as e:
            print(f"Timeout error: {e}")
        except socket.error as e:
            print(f"General socket error: {e}")
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            print(f"{retdata}")
            
    def short_sell_join_offer_new_order(self, connection, symbol, shares_to_short, price, route="XALL", tif="DAY+"):
        unID = int(self.uniq)
        script = f"NEWORDER {unID} SS {symbol.upper()} {route} {shares_to_short} {price} {tif.upper()}"
        print (f"Sending {script}")
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            
        except socket.timeout as e:
            print(f"Timeout error: {e}")
        except socket.error as e:
            print(f"General socket error: {e}")
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            print(f"{retdata}")
            
    def short_sell_open_auction_new_order(self, connection, symbol, shares_to_short, price, tif="DAY"):
        unID = int(self.uniq)
        script = f"NEWORDER {unID} SS {symbol.upper()} ALGO {shares_to_short} {price} FixTags=ALGO|Type=AUCT|OA=Y"
        print (f"Sending {script}")
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            #retdata = ["Simulated response: Order placed successfully."]
            
        except socket.timeout as e:
            print(f"Timeout error: {e}")
        except socket.error as e:
            print(f"General socket error: {e}")
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            print(f"{retdata}")

    #Method:Short Sell New Order for all Gapped Stocks
    def short_sell_market_at_open_for_all_gapped_stocks(self, connection, autorun):
        for index, row in self.ticker_df.iterrows():
            if row['pre_trade_check_passed']:  # Only place short sell order if locate is available or already shortable
                symbol = row['ticker']
                shares_to_short = row['shares_to_short']
                route = "XALL"
                tif = "DAY"
                print(f"\nPlacing market short sell order for ticker: {symbol}, for {shares_to_short} shares at route: {route}")
                if not autorun:
                    proceed = input("Type 'Yes' to proceed to place short sell market order or Enter to skip: ")
                    if proceed.lower() == 'yes':
                        self.short_sell_market_new_order(connection, symbol, shares_to_short, route, tif)                
                else:
                    self.short_sell_market_new_order(connection, symbol, shares_to_short, route, tif)
                    
    #Method:Short Sell New Order at offer for all Gapped Stocks 
    def short_sell_join_offer_for_all_gapped_stocks(self, connection, autorun):
        for index, row in self.ticker_df.iterrows():
            if row['pre_trade_check_passed']:  # Only place short sell order if locate is available or already shortable
                symbol = row['ticker']
                shares_to_short = row['shares_to_short']
                route = "XALL"
                tif = "DAY"
                print(f"Getting bid/ask prices for {symbol}, shares to short: {shares_to_short}")
                bid_price = row['last_quote_bid']
                ask_price = row['last_quote_ask']
                bid_ask_spread = (ask_price - bid_price)
                print(f"Bid Price: {bid_price}, Ask Price: {ask_price}")
                if bid_ask_spread / bid_price <= 0.005:
                    trade_price = ask_price
                else:
                    trade_price = bid_price + round(bid_ask_spread * 0.75, 2)
                print(f"\nPlacing market short sell order for ticker: {symbol}, for {shares_to_short} shares at price: {trade_price}, at route: {route}")
                if not autorun:
                    proceed = input("Type 'Yes' to proceed to place short sell join offer order or Enter to skip: ")
                    if proceed.lower() == 'yes':
                        self.short_sell_join_offer_new_order(connection, symbol, shares_to_short, trade_price, route, tif)                
                    proceed_2 = input("Type 'Yes' to proceed to next order: ")
                    if proceed_2.lower() == 'yes':
                        continue
                else:
                    self.short_sell_join_offer_new_order(connection, symbol, shares_to_short, trade_price, route, tif)

    #Method:Short Sell Open Auction Order for all Gapped Stocks
    def short_sell_open_auction_new_order_for_all_gapped_stocks(self, connection, autorun):
        for index, row in self.ticker_df.iterrows():
            if row['pre_trade_check_passed']:  # Only place short sell order if locate is available or already shortable
                symbol = row['ticker']
                shares_to_short = row['shares_to_short']
                price = row['last_quote_bid']
                route = "ALGO"
                print(f"\nPlacing market short sell order for ticker: {symbol}, for {shares_to_short} shares at route: {route}")
                if not autorun:
                    proceed = input("Type 'Yes' to proceed to place short sell market order or Enter to skip: ")
                    if proceed.lower() == 'yes':
                        self.short_sell_open_auction_new_order(connection, symbol, shares_to_short, price, "DAY")                
                else:
                    self.short_sell_open_auction_new_order(connection, symbol, shares_to_short, price, "DAY")


    #Method:NewOrder for stop loss
    def stop_loss_market_buy_new_order(self, connection, symbol, shares_to_cover, stop_price, route="SMAT", tif="DAY"):
            unID = int(self.uniq)
            script = f"NEWORDER {unID} B {symbol.upper()} {route} {shares_to_cover} STOPMKT {stop_price}"
            print (f"Sending {script}")
            try:
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                
            except socket.timeout as e:
                print(f"Timeout error: {e}")
            except socket.error as e:
                print(f"General socket error: {e}")
            except Exception as e:
                print(f"Exception: {e}")
            finally:
                print(f"{retdata}")
                
    #Method:Stop Loss New Order for all holdings in position
    def stop_loss_new_order_for_all_stocks_in_position(self, connection, autorun = False):
        for index, row in self.ticker_df.iterrows():
            if row['in_position']:  # Only place short sell order if locate is available or already shortable
                symbol = row['ticker']
                shares_to_cover = row['shares_to_cover']
                route = "SMAT"
                stop_price = row['ave_price']
                print(f"\nPlacing market stop loss order for ticker: {symbol}, for {shares_to_cover} shares at route: {route}")
                if not autorun:
                    proceed = input("Type 'Yes' to proceed to place stop loss market order or Enter to skip: ")
                    if proceed.lower() == 'yes':
                        self.stop_loss_market_buy_new_order(connection, symbol, shares_to_cover, stop_price, route, "DAY")                
                else:
                    self.stop_loss_market_buy_new_order(connection, symbol, shares_to_cover, stop_price, route, "DAY")

    #Method:Submit Order
    def submit_order(self, connection):
        # The code is attempting to convert the variable `self.uniq` to an integer using the `int()`
        # function and store the result in the variable `unID`.
        unID = int(self.uniq)
        inp = input("\nSubmit Limit Order\t\t\t\t(Enter: 1)\n       Market Order\t\t\t\t(Enter: 2)\n       Stop Limit Order\t\t\t\t(Enter: 3)\n       Stop Market Order\t\t\t(Enter: 4)\n       Stop Range Order\t\t\t\t(Enter: 5)\n       Stop Range Market Order\t\t\t(Enter: 6)\n       Stop Trailing Order\t\t\t(Enter: 7)\n       Complex Order\t\t\t\t(Enter: 8)\n\n       Input: ")
        script = ""

        try:
            
            if(inp == "1" or inp.upper() == "L" or inp.upper() == "LMT" or inp.upper() == "LIMIT" or inp.upper() == "LIMITORDER" or inp.upper() == "LIMIT ORDER"):
                dataInp = input(f"\nLimit order: (B/S/SS) (Symbol) (Shares) (Price)\n\nInput:\t")
                hold = dataInp.split(" ") #// Holds all the words delimited by the space; so for example hold[0]=B hold[1]=HMC etc.
                hold.insert(2, "SMAT") #// Insert the route after the index 1, so after the symbol in this case.

                delimt = " " #// Need to put the string back into server readable form, so we need to add the spaces," ", back.
                dat = delimt.join(hold) #// After each index in the list, add the delimiter


                #script = f"NEWORDER {unID} B C SMAT 15 20.3 Display=100" #Syntax for new limit order = "NEWORDER" + " " + token + " " + "borS.upper()" + " " + "symbol.upper() + " " + "route.upper()" + " " + shares + " " + price + " " + TIF="time.upper()" + "\r\n" 
                script = f"NEWORDER {unID} {dat.upper()} Display=100"

                print("\n---------------- Submitting New Limit Order ----------------\n")
                print(script)
        
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\n{retdata}")
                print("\n------------------------------------------------------------")
            
            elif(inp == "2" or inp.upper() == "M" or inp.upper() == "MKT" or inp.upper() == "MARKET" or inp.upper() == "MARKETORDER" or inp.upper() == "MARKET ORDER"):
                dataInp = input(f"\nMarket order: (B/S/SS) (Symbol) (Shares)\n\nInput:\t")                      
                hold = dataInp.split(" ") #// Holds all the words delimited by the space; so for example hold[0]=B hold[1]=HMC etc.
                hold.insert(2, "SMAT") #// Insert the route after the index 1, so after the symbol in this case.

                delimt = " " #// Need to put the string back into server readable form, so we need to add the spaces," ", back.
                dat = delimt.join(hold) #// After each index in the list, add the delimiter

                #script = f"NEWORDER {unID} B GOOG SMAT 100 MKT" #Only needs the amount of shares you want + MKT for market; FOR WHATEVER PRICE
                script = f"NEWORDER {unID} {dat.upper()} MKT"

                print("\n---------------- Submitting New Market Order ----------------\n")
                print(script)
        
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\n{retdata}")
                print("\n-----------------------------------------------------------")
            
            elif(inp == "3" or inp.upper() == "SL" or inp.upper() == "STPLMT" or inp.upper() == "STOPLIMIT" or inp.upper() == "STOPLIMITORDER" or inp.upper() == "STOP LIMIT ORDER"):
                #script = f"NEWORDER {unID} B TSLA SMAT 100 STOPLMT 150 145.6" #After the amount of shares, in this case 100, include 'STOPLMT' followed by the desired stopprice and than the desired price
                
                dataInp = input(f"\nStop Limit order: (B/S/SS) (Symbol) (Shares) (Stop Price) (Price)\n\nInput:\t")                      
                hold = dataInp.split(" ")
                hold.insert(2, "SMAT") 
                hold.insert(4, "STOPLMT")

                delimt = " " 
                dat = delimt.join(hold)

                script = f"NEWORDER {unID} {dat.upper()}"


                print("\n---------------- Submitting Stop Limit Order ----------------\n")
                print(script)
        
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\n{retdata}")
                print("\n-----------------------------------------------------------")
            
            elif(inp == "4" or inp.upper() == "SM" or inp.upper() == "STPMKT" or inp.upper() == "STOPMARKET" or inp.upper() == "STOPMARKETORDER" or inp.upper() == "STOP MARKET ORDER"):
                #script = f"NEWORDER {unID} B MSFT SMAT 100 STOPMKT 205.5" #After the amount of shares, include 'STOPMKT' followed by the desired stopprice.
               
                dataInp = input(f"\nStop Market order: (B/S/SS) (Symbol) (Shares) (Stop Price)\n\nInput:\t")                      
                hold = dataInp.split(" ")
                hold.insert(2, "SMAT") 
                hold.insert(4, "STOPMKT")

                delimt = " " 
                dat = delimt.join(hold)

                script = f"NEWORDER {unID} {dat.upper()}"


                print("\n---------------- Submitting Stop Market Order ----------------\n")
                print(script)
        
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\n{retdata}")
                print("\n-----------------------------------------------------------")
            
            elif(inp == "5" or inp.upper() == "R" or inp.upper() == "RNG" or inp.upper() == "STPR" or inp.upper() == "RANGE" or inp.upper() == "STOPRANGE" or inp.upper() == "STOPRANGEORDER" or inp.upper() == "STOP RANGE ORDER"):
                #script = f"NEWORDER {unID} B MSFT SMAT 100 STOPRANGE 205.5 205.9" #After the amount of shares, include 'STOPRANGE'.
                
                dataInp = input(f"\nStop Range order: (B/S/SS) (Symbol) (Shares) (Low Price) (High Price)\n\nInput:\t")                      
                hold = dataInp.split(" ")
                hold.insert(2, "SMAT") 
                hold.insert(4, "STOPRANGE")

                delimt = " " 
                dat = delimt.join(hold)

                script = f"NEWORDER {unID} {dat.upper()}"

                print("\n---------------- Submitting Stop Range Order ----------------\n")
                print(script)
        
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\n{retdata}")
                print("\n-----------------------------------------------------------")
            
            elif(inp == "6" or inp.upper() == "RR" or inp.upper() == "RM" or inp.upper() == "RMKT" or inp.upper() == "STPRMKT" or inp.upper() == "RANGEMARKET" or inp.upper() == "STOPRANGEMARKET" or inp.upper() == "STOPRANGEMARKETORDER" or inp.upper() == "STOP RANGE MARKET ORDER"):
                #script = f"NEWORDER {unID} B MSFT SMAT 100 STOPRANGEMKT 205.5 205.9" #After the amount of shares, include 'STOPRANGEMKT'.
               
                dataInp = input(f"\nStop Range Market order: (B/S/SS) (Symbol) (Shares) (Low Price) (High Price)\n\nInput:\t")                      
                hold = dataInp.split(" ")
                hold.insert(2, "SMAT") 
                hold.insert(4, "STOPRANGEMKT")

                delimt = " " 
                dat = delimt.join(hold)

                script = f"NEWORDER {unID} {dat.upper()}"


                print("\n---------------- Submitting Stop Range Market Order ----------------\n")
                print(script)
        
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\n{retdata}")
                print("\n-----------------------------------------------------------")
            
            elif(inp == "7"  or inp.upper() == "T" or inp.upper() == "TR" or inp.upper() == "TRAILING" or inp.upper() == "TRAILINGORD"  or inp.upper() == "TRAILINGORDER" or inp.upper() == "STOPTRAILINGORDER" or inp.upper() == "STOP TRAILING ORDER"):
                #script = f"NEWORDER {unID} S MSFT SMAT 100 STOPTRAILING 0.2" #After the amount of shares, include 'STOPTRAILING' followed by trail price.
               
                dataInp = input(f"\nStop Trailing order: (B/S/SS) (Symbol) (Shares) (Trail Price)\n\nInput:\t")                      
                hold = dataInp.split(" ")
                hold.insert(2, "SMAT") 
                hold.insert(4, "STOPTRAILING")

                delimt = " " 
                dat = delimt.join(hold)

                script = f"NEWORDER {unID} {dat.upper()}"

                print("\n---------------- Submitting Stop Trailing Order ----------------\n")
                print(script)
        
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii")) 
                print(f"\n{retdata}")
                print("\n-----------------------------------------------------------") 
            
            elif(inp == "8" or inp.upper() == "C" or inp.upper() == "CO" or inp.upper() == "CMPLX" or inp.upper() == "CMPLXORD" or inp.upper() == "COMPLEXORDER" or inp.upper() == "COMPLEX ORDER"):
                #COMPLEXORDER Route=SMATL TIF=DAY NetPrice=0.5 AON=Y LegSym=+MSFT^E3I412 LegToken={unID} Side=BO Share=1 LegSym=+MSFT*E3I412 LegToken={unID - 1} Side=SO Share=1 //////////////////// Route = route + M or L; TIF; NetPrice; AON; LegSymbol where complex order has multiple legs and where each leg represents a symbol. Must be in DAS format like +SPY^EBT535 where its denoted as SPY 535 CALL 20241129; LegToken = Unique ID; Side = BO(Buy to Open), BC(Buy to Close), SO(Sell to Open), SC(Sell to Close); Equity Leg Side(Not used in this example) = B / S; Shares
                script = f"SB MSFT Lv1\nCOMPLEXORDER Route=SMATL TIF=DAY NetPrice=0.5 AON=Y LegSym=+MSFT^E8U400 LegToken={unID} Side=BO Share=1 LegSym=+MSFT*E8U400 LegToken={unID - 1} Side=SO Share=1\nUNSB MSFT Lv1"
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\nSending {script}")
                print(f"\n{retdata}")
            
            else:
                print("\nNot one of the options.\n")
                return
            
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")
            
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")
            
        except Exception as e:
            print(f"\nException: {e}")
            
        finally:
            
            script = ""
            retdata = ""
    
    #Method:Get Short Info
    def get_short_info(self, connection):
        symbol = input("\nEnter Symbol: ")
        script = f"GET SHORTINFO {symbol.upper()}"
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")
            
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")
            
        except Exception as e:
            print(f"\nException: {e}")
            
        finally:
            if retdata:
                print(f"\nRecieved Short Info - {symbol.upper()}:\n\n{retdata}\n")
            else:
                print("\nTimed out / No Data Recieved\n")

    #Method:Replace Order
    def replace_order(self, connection):
        cmd = cmdAPI()
        unID = int(self.uniq) #Unique ID
        ans = input("\nWould you like to replace an order?(Y/N) ")
        
        if(ans.upper() == 'YES' or ans.upper() == 'Y' or ans == "1"):
            retdata = connection.send_script(bytearray("GET ORDERS\r\n", encoding = "ascii")) # View Orders
            print(f"\n{retdata}")
            
            ordId = input(f"\nPlease enter the Order ID for the Order you want to replace: ")
            newOrd = input("\nPlease Enter Details according to the selected Order Type\n\nFORMAT (Space Sensitive):\n\nLimit Order - Shares Price\nMarket Order - Shares MKT\nStop Market Order - Shares STOPMKT EntryPrice\nStop Limit Order - Shares STOPLMT EntryPrice Price\nStop Trailing Order - Shares STOPTRAILING TrailPrice\nStop Range Order - Shares STOPRANGE LowPrice HighPrice\nStop Range Market Order - Shares STOPRANGEMKT LowPrice HighPrice\n\n:")
            print(f"\nReplacing Order: {ordId}\n")
            try:
                script = f"REPLACE {ordId} {newOrd}"
                print(f"Sending {script}")
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"{retdata}\n")
                retdata = connection.send_script(bytearray("GET ORDERS\r\n", encoding = "ascii")) # View Orders
                print(f"\n{retdata}")
            except:
                print(f"\n{ordId} is not listed in your orders.\n")
        elif(ans.upper() == "NO" or ans.upper() == "N" or ans == "0"):
            print("\nNo Orders were replaced.\n")
            retdata = connection.send_script(bytearray("GET ORDERS\r\n", encoding = "ascii")) # View Orders
            print(f"\n{retdata}")
        else:
            print("Please enter yes or no.")      

    #Method:Cancel Order
    def cancel_order(self, connection):
        ans = input("\nWould you like to cancel an order?(Y/N) ")
        
        if(ans.upper() == 'YES' or ans.upper() == 'Y' or ans == "1"):
            retdata = connection.send_script(bytearray("GET ORDERS\r\n", encoding = "ascii")) # View Orders
            print(f"\n{retdata}")
            
            ordId = input(f"\nPlease enter the Order ID for the Order you want to cancel: ")
            print(f"\nCanceling Order: {ordId}\n")
            try:
                script = f"CANCEL {ordId}"
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"{retdata}\n")
                #print(f"\nOrder {ordId} canceled.\n")
                retdata = connection.send_script(bytearray("GET ORDERS\r\n", encoding = "ascii")) # View Orders
                print(f"\n{retdata}")
            except:
                print(f"\n{ordId} is not listed in your orders.\n")
        elif(ans.upper() == "NO" or ans.upper() == "N" or ans == "0"):
            print("\nNo Orders were canceled.\n")
            retdata = connection.send_script(bytearray("GET ORDERS\r\n", encoding = "ascii")) # View Orders
            print(f"\n{retdata}")
        else:
            print("Please enter yes or no.")  

    #Method:Cancel All Open Orders
    def cancel_all_open_orders(self, connection):
        cmd = cmdAPI()
        ans = input("\nWould you like to cancel all open orders?(Y/N) ")
        
        if(ans.upper() == 'YES' or ans.upper() == 'Y' or ans == "1"):
            script = "CANCEL ALL"
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            print(f"\n{retdata}")
            print("\nAll Orders Canceled.\n")
        elif(ans.upper() == "NO" or ans.upper() == "N" or ans == "0"):
            print("\nNo Orders were not canceled.\n")
            retdata = connection.send_script(bytearray("GET ORDERS\r\n", encoding = "ascii")) # View Orders
            print(f"\n{retdata}")
        else:
            print("Please enter yes or no.")
        pass
    
    #Method:UnSubscribe
    def unsubscribe(self, connection):
        symbol = input("\nEnter a symbol to unsubscribe: ")
        script = f"UNSB {symbol.upper()} Lv1\nUNSB {symbol.upper()} Lv2\nUNSB {symbol.upper()} tms\r\n"
        print(f"\nSending \n{script}")
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")
            
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")
            
        except Exception as e:
            print(f"\nException: {e}")
        
        finally:
            print(retdata)
        #End Block

    #Method:Daychart
    def day_chart(self,connection):
        symbol = input("\nPlease enter a Symbol for the Daychart: ")
        curr = datetime.today()
        script = f"SB {symbol.upper()} DAYCHART {(curr - timedelta(days=50)).strftime('%Y/%m/%d')} {(curr - timedelta(days=1)).strftime('%Y/%m/%d')}" #For Daychart, subscribe to a symbol followed by 'DAYCHART' and after that enter a start date followed by an end date.

        print(f"\nSending {script}")
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
         
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")
            
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")
            
        except Exception as e:
            print(f"\nException: {e}")
           
        finally:
            print(f"\n{retdata}")
    
    #Method:Minchart
    def minute_chart(self, connection):
        symbol = input("\nPlease enter a Symbol for the Minchart: ")
        curr = datetime.today()
        script = f"SB {symbol.upper()} MINCHART {(curr - timedelta(days=8)).strftime('%Y/%m/%d')}-00:00 {(curr - timedelta(days=7)).strftime('%Y/%m/%d')}-00:00" #Similiar to Daychart, Instead replace with 'MINCHART'. after the date '00:00' indicates 12am of that date.
        
        print(f"\nSending {script}")
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
        
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")
            
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")
            
        except Exception as e:
            print(f"\nException: {e}")
            
        finally:
            print(f"\n{retdata}")
        
    #--------------------------------------------------SHORT LOCATE COMMANDS--------------------------------------------------#
    
    def get_shares_to_short(self):
        """
        Retrieves the number of shares to short for a given ticker from the DataFrame.
        """
        for index, row in self.ticker_df.iterrows():
            last_quote_bid = row['last_quote_bid']
            shares_to_locate = row['shares_to_locate']
            short_size = row['short_size']
            self.ticker_df.at[index, 'shares_to_short'] = min(round(short_size / last_quote_bid), shares_to_locate)
        return self.ticker_df

    def inquire_short_locate_for_all_gapped_stocks(self, connection):
        for index, row in self.ticker_df.iterrows():
            ticker = row['ticker']
            shares_to_locate = row.get('shares_to_locate', 0)
            print(f"\nProcessing ticker: {ticker}, locating {shares_to_locate} shares")
            self.ticker_df.at[index, 'locate_available'] = False
            self.ticker_df.at[index, 'total_locate_cost'] = 0
            self.ticker_df.at[index, 'locate_price'] = 0
            self.ticker_df.at[index, 'route'] = 'None'
            if row['locate_order_status'] == 'No Locate Order':
                short_locate_results = self.short_locate_price_inquire_lowest(connection, ticker, shares_to_locate)    
                self.ticker_df.at[index, 'total_locate_cost'] = short_locate_results['total_locate_cost']
                self.ticker_df.at[index, 'locate_price'] = short_locate_results['locate_price']
                self.ticker_df.at[index, 'route'] = short_locate_results['route']
                self.ticker_df.at[index, 'locate_available'] = short_locate_results['locate_available']
        return self.ticker_df
    
    #Method:SLPriceInquire   
    def short_locate_price_inquire_lowest(self, connection, symbol, shares_to_locate):
        locate_routes = ["ATLAS2", "ATLAS1", "ATLAS3", "ATLAS6", "ATLAS7"]
        #script = f"SLPRICEINQUIRE {symbol.upper()} {shares_to_locate} ATLAS2"
        
        locate_price = 100  # Default locate price
        locate_shares_available = 0 # Default available shares
        lowest_price_route = ""
        for route in locate_routes:
            script = f"SLPRICEINQUIRE {symbol.upper()} {shares_to_locate} {route}"
            #print(f"Sending {script}")
            try:
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(retdata)
                if retdata is None or retdata == "Socket error: timed out":
                    print(f"Failed to get data for route {route}.")
                    #retdata = ["%SLRET", "0", f"{symbol.upper()}", "100", "0", "0", "NotShortable", "0"]
                elif retdata.split(" ")[6] == "AlreadyShortable":
                    print("Already shortable, no locate needed.")
                    return {"locate_price": 0, "total_locate_cost": 0, "route": "ALL", "locate_available": True}
                elif float(retdata.split(" ")[3]) < locate_price and float(retdata.split(" ")[4]) >= shares_to_locate:
                    locate_price = float(retdata.split(" ")[3])  # Assuming the price is the fourth element
                    locate_shares_available = float(retdata.split(" ")[4])  # Assuming the available shares is the fifth element
                    lowest_price_route = route
                    #print(f"Route: {route}, Price: {locate_price}, Available Shares: {locate_shares_available}")
                
            except socket.timeout as e:
                print(f"Timeout error: {e}")
            except socket.error as e:
                print(f"General socket error: {e}")
            except Exception as e:
                print(f"Exception: {e}")

        if locate_shares_available < shares_to_locate:
            print("Not shortable, insufficient shares available to locate.")
            return {"locate_price": 100, "total_locate_cost": 1000, "route": "None", "locate_available": False}
        
        total_locate_cost = locate_price * shares_to_locate
        print(f"Lowest Price Route: {lowest_price_route}, Price: {locate_price}, Available Shares: {locate_shares_available}, Total Cost: {total_locate_cost}")
        return ({"locate_price": locate_price, "total_locate_cost": total_locate_cost, "route": lowest_price_route, "locate_available": True})

    #Method:Pre Trade Checks
    def pre_locate_checks(self):
        print("Performing Pre-Locate Checks:")
        print("ticker, locate_available_check, locate_cost_check, no_existing_locate_check, volume_check")
        for index, row in self.ticker_df.iterrows():
            locate_available_check = row['locate_available']
            locate_cost_check = row['total_locate_cost'] <= row['short_size'] * 0.004
            no_existing_locate_check = row['locate_order_status'] != 'Accepted!' and row['route'] != 'ALL'
            volume_check = row['volume'] >= 0
            self.ticker_df.at[index, 'pre_locate_check_passed'] = bool(
                locate_available_check
                and locate_cost_check
                and no_existing_locate_check
                and volume_check
            )
            print(row['ticker'], locate_available_check, locate_cost_check, no_existing_locate_check, volume_check)
    
    #Method:Pre Trade Checks
    def pre_trade_checks(self):
        print("Performing Pre-Trade Checks:")
        print("ticker, locate_available_check, locate_cost_check, locate_accepted_check, volume_check, already_in_position_check")
        for index, row in self.ticker_df.iterrows():
            locate_available_check = row['locate_available']
            locate_cost_check = row['total_locate_cost'] <= row['short_size'] * 0.004 # Total locate cost less than 40bps
            locate_accepted_check = row['locate_order_status'] == 'Accepted!' or row['route'] == 'ALL' # Locates exist for shorting
            if locate_accepted_check:
                locate_cost_check = True  # Bypass cost check if locate is already accepted
                locate_available_check = True  # Bypass availability check if locate is already accepted
            volume_check = row['volume'] >= 0
            already_in_position_check = row['shares_in_position'] == 0  # Ensure not already in position
            self.ticker_df.at[index, 'pre_trade_check_passed'] = bool(
                locate_available_check
                and locate_cost_check
                and locate_accepted_check
                and volume_check
                and already_in_position_check
            )
            print(row['ticker'], locate_available_check, locate_cost_check, locate_accepted_check, volume_check, already_in_position_check)

    #Method:Inquire Short Locate for all Gapped Stocks
    def short_locate_new_order_for_all_gapped_stocks(self, connection, autorun = False):
        for index, row in self.ticker_df.iterrows():
            route = row['route']
            # Checks if passed pre-locate checks and route is not 'ALL'
            if row['pre_locate_check_passed'] and route != 'ALL':
                ticker = row['ticker']
                shares_to_locate = row['shares_to_locate']
                print(f"\nPlacing locate order for ticker: {ticker}, locating {shares_to_locate} shares at route {route} with total cost {row['total_locate_cost']}")
                if not autorun:
                    proceed = input("Type 'Yes' to proceed to locate the order or Enter to skip: ")
                    if proceed.lower() == 'yes':
                        self.short_locate_new_order(connection, ticker, shares_to_locate, route)
                else:
                    self.short_locate_new_order(connection, ticker, shares_to_locate, route)

    #Method:SLNewOrder
    def short_locate_new_order(self, connection, symbol, locate_shares, route):
        script = f"SLNEWORDER {symbol.upper()} {locate_shares} {route}"
        print (f"Sending {script}")
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            
        except socket.timeout as e:
            print(f"Timeout error: {e}")
        except socket.error as e:
            print(f"General socket error: {e}")
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            print(f"{retdata}")
        
    #Method:SLCancelOrder
    def short_locate_cancel_order(self, connection):
        self.get_short_locate_orders(connection)
        ordID = input("\nEnter the locate order ID for cancelation: ")
        script = (f"SLCANCELORDER {ordID}")
        print(f"\nCanceling Order: {ordID}")
        
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            
        except Exception:
            print(f"\n{ordID} is not listed in your orders.\n")
        finally:
            print(f"\n{retdata}")
            
    #Method:SLOfferOperation
    def short_locate_offer_operation(self, connection):     #// To Accept or Reject an offer
        ans = input("\nAccept or Reject:(A/R) ")
        try:
            if(ans.upper() == "A" or ans.upper() == "ACCEPT" or ans == "1" or ans.upper() == "Y" or ans.upper() == "YES"):
                self.get_short_locate_orders(connection)
            
                ordID = input("\nEnter the order ID for offer acceptance: ")
                script = f"SLOFFEROPERATION {ordID} Accept"
                print(f"\nSending {script}")
            
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\n{retdata}")
            elif(ans.upper() == "R" or ans.upper() == "REJECT" or ans == "0" or ans.upper() == "N" or ans.upper() == "NO"):
                self.get_short_locate_orders(connection)

                ordID = input("\nEnter the order ID for offer rejection: ")
                script = f"SLOFFEROPERATION {ordID} Reject"
                print(f"\nSending {script}")
            
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\n{retdata}")
            else:
                print("\nNot one of the options.\n")
        except Exception as e:
            print(f"\nException: {e}")
            
    #Method:get_short_locate_orders gets short locate orders
    def get_short_locate_orders(self,connection):
        script = "GET LOCATES"
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
        
        except socket.timeout as e:
            print(f"Timeout error: {e}")
            
        except socket.error as e:
            print(f"General socket error: {e}")
            
        except Exception as e:
            print(f"Exception: {e}")
         
        finally:
            if retdata:
                print(f"Recieved Data:\n{retdata}\n")
            else:
                print("Timed out / No Data Recieved\n")
            return retdata
    
    def get_short_locate_orders_df(self,connection):
        locate_orders = self.get_short_locate_orders(connection)
        locate_orders_array = locate_orders.split()
        grouped_orders_temp = []
        grouped_orders = []
        for index, value in enumerate(locate_orders_array):
            if value == "#SLOrderEnd":
                grouped_orders.append(grouped_orders_temp)
                break
            elif value == "%SLOrder" and index != 0:
                grouped_orders.append(grouped_orders_temp)
                grouped_orders_temp = ["%SLOrder"]
            else:
                grouped_orders_temp.append(value)
        headers = grouped_orders[:1][0]  # Remove the header row from data
        grouped_orders = grouped_orders[1:] # Remove the header row
        for index, value in enumerate(grouped_orders):
            if len(value) > len(headers):
                grouped_orders[index][len(headers)-1] = ' '.join(value[len(headers)-1:])
                grouped_orders[index] = value[:len(headers)-1]
                
        return pd.DataFrame(grouped_orders, columns=headers)
    
    def update_df_with_short_locate_orders(self, connection):
        grouped_orders_df = self.get_short_locate_orders_df(connection)
        for index, row in self.ticker_df.iterrows():
            self.ticker_df.at[index, 'locate_order_status'] = 'No Locate Order'
            for index2, row2 in grouped_orders_df.iterrows():
                if row['ticker'] == row2['symb']:
                    if row2['notes'] is None or row2['notes'] == '':
                        self.ticker_df.at[index, 'locate_order_status'] = 'No Locate Order'
                    else:
                        self.ticker_df.at[index, 'locate_order_status'] = row2['notes']

        return self.ticker_df

    #Method:PositionRefresh
    def PositionRefresh(self,connection):
        script = "POSREFRESH"
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            print(f"\nSending {script}")
            
        except socket.timeout as e:
            print(f"\nTimeout error: {e}")
            
        except socket.error as e:
            print(f"\nGeneral socket error: {e}")
            
        except Exception as e:
            print(f"\nException: {e}")
            
        finally:
            if retdata:
                print(f"\nRecieved Data:\n{retdata}\n")
            else:
                print("\nTimed out / No Data Recieved\n")