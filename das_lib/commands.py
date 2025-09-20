import socket
import uuid
import asyncio
from datetime import datetime, timedelta

class CmdAPI:
    def __init__(self):
        self.uniq = uuid.uuid4()

    async def check_for_input():
        try:
            while True:
                userInput = await asyncio.get_event_loop().run_in_executor(None, input, "\nTo leave enter: 1\n")
                if (userInput == "1"):
                    print("\nLeaving.\n")
                    return
        except Exception as e:
            print(f"\nException: {e}\n")
    
    #Method:Subscribe
    async def subscribe(self, connection, level="Lv1", symbol=""):
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
        
        checkInput = asyncio.create_task(self.check_for_input())
        print(f"\nSending:\n{script}\nNOTE: Depending on the Market Time and Symbol, data retrieval may take some time.")
        datStream = True
        retdata = ""
        
        try:
            while(datStream):        

                if(retdata == ""):
                    retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                    #if(retdata == ""):
                    #    print("")
                else:
                    retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                    print(retdata)
            
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
            retdata = "" #Empty the buffer
            checkInput.cancel()
            await checkInput
            connection.send_script(bytearray(f"UNSB {symbol.upper()} {actualLvl}\r\n", encoding = "ascii")) #Unsub from symbol
        #End Block
    
    #Method:Subscribe Top List
    async def topList(self, connection):
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
    def accountDetails(self, connection, detailType=""):
        inp = input("\nFor Buying Power\t\t(Enter: 1)\n    Positions\t\t\t(Enter: 2)\n    Orders\t\t\t(Enter: 3)\n    Trades\t\t\t(Enter: 4)\n    Route Status\t\t(Enter: 5)\n    LDLU\t\t\t(Enter: 6)\n    Symbol Status\t\t(Enter: 7)\n    Account Info\t\t(Enter: 8)\n\n    Input: ")
        script = ""

        if(detailType == "1" or detailType.upper() == "B" or detailType.upper() == "P" or detailType.upper() == "BP" or detailType.upper() == "BUYINGPOWER"):
            script = "GET BP\r\n"
        elif(detailType == "2" or detailType.upper() == "P" or detailType.upper() == "POS" or detailType.upper() == "POSITION" or detailType.upper() == "POSITIONS"):
            script = "GET POSITIONS\r\n"
        elif(detailType == "3" or detailType.upper() == "O" or detailType.upper() == "ORD" or detailType.upper() == "ORDER" or detailType.upper() == "ORDERS"):
            script = "GET ORDERS\r\n"
        elif(detailType == "4" or detailType.upper() == "T" or detailType.upper() == "TR" or detailType.upper() == "TRADE" or detailType.upper() == "TRADES"):
            script = "GET TRADES\r\n"
        elif(detailType == "5" or detailType.upper() == "R" or detailType.upper() == "ROUTE" or detailType.upper() == "ROUTESTATUS" or detailType.upper() == "ROUTE STATUS"):
            script = "GET ROUTESTATUS\r\n"
        elif(detailType == "6" or detailType.upper() == "L" or detailType.upper() == "LD" or detailType.upper() == "LU" or detailType.upper() == "LDLU"):
            symb = detailTypeut("\n    Enter Symbol: ")
            script = f"GET LDLU {symb.upper()}\r\n"
        elif(detailType == "7" or detailType.upper() == "S" or detailType.upper() == "SS" or detailType.upper() == "SYM" or detailType.upper() == "STAT" or detailType.upper() == "SYMBOL" or detailType.upper() == "STATUS" or detailType.upper() == "SYMBOLSTATUS" or detailType.upper() == "SYMBOL STATUS"):
            symb = detailTypeut("\n    Enter Symbol: ")
            script = f"GET SymStatus {symb.upper()}\r\n"
        elif(detailType == "8" or detailType.upper() == "A" or detailType.upper() == "AI" or detailType.upper() == "ACC" or detailType.upper() == "IFO" or detailType.upper() == "INFO" or detailType.upper() == "AINFO" or detailType.upper() == "ACCINFO" or detailType.upper() == "ACCOUNTINFO" or detailType.upper() == "ACCOUNT INFO"):
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
        
    #Method:Submit Order
    def submitOrder(self, connection):
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
    def GetShortInfo(self, connection):
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
    def ReplaceOrder(self, connection):
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
    def CancelOrder(self, connection):
        cmd = cmdAPI()
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
    def CancelAllOpenOrder(self, connection):
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
    def Daychart(self,connection):
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
    def Minchart(self, connection):
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
    
    #Method:SLPriceInquire
    def SLPriceInquire(self, connection):
        symbol = input("\nPlease enter a symbol for a short locate inquery: ")
        script = f"SLPRICEINQUIRE {symbol.upper()} 100 TESTSL"
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
    
    #Method:SLNewOrder
    def SLNewOrder(self, connection):
        symbol = input("\nPlease enter a symbol for a short order: ")
        script = f"SLNEWORDER {symbol.upper()} 100 TESTSL"
        print (f"\nSending {script}")
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
        
    #Method:SLCancelOrder
    def SLCancelOrder(self, connection):
        cmd = cmdAPI()
        cmd.GetSLOrders(connection)
        ordID = input("\nEnter the locate order ID for cancelation: ")
        script = (f"SLCANCELORDER {ordID}")
        print(f"\nCanceling Order: {ordID}")
        
        try:
            retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
            
        except:
                print(f"\n{ordID} is not listed in your orders.\n")
        finally:
            print(f"\n{retdata}")
            
    #Method:SLOfferOperation
    def SLOfferOperation(self, connection):     #// To Accept or Reject an offer
        cmd = cmdAPI()
        ans = input("\nAccept or Reject:(A/R) ")
        try:
            if(ans.upper() == "A" or ans.upper() == "ACCEPT" or ans == "1" or ans.upper() == "Y" or ans.upper() == "YES"):
                cmd.GetSLOrders(connection)
            
                ordID = input("\nEnter the order ID for offer acceptance: ")
                script = f"SLOFFEROPERATION {ordID} Accept"
                print(f"\nSending {script}")
            
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\n{retdata}")
            elif(ans.upper() == "R" or ans.upper() == "REJECT" or ans == "0" or ans.upper() == "N" or ans.upper() == "NO"):
                cmd.GetSLOrders(connection)

                ordID = input("\nEnter the order ID for offer rejection: ")
                script = f"SLOFFEROPERATION {ordID} Reject"
                print(f"\nSending {script}")
            
                retdata = connection.send_script(bytearray(script + "\r\n", encoding = "ascii"))
                print(f"\n{retdata}")
            else:
                print("\nNot one of the options.\n")
        except Exception as e:
            print(f"\nException: {e}")
            
    #Method:GetSLOrders
    def GetSLOrders(self,connection):
        script = "GET LOCATES"
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
                print(f"\nRecieved Data:\n{retdata}\n")
            else:
                print("\nTimed out / No Data Recieved\n")
            
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