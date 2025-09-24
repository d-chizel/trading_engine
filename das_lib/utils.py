class Utils:
    """
    Utilities for processing data retrieved from DAS.
    """
    
    def __init__(self):
        pass

    @staticmethod
    def get_bid_price(lv1_data):
        """
        Extracts the bid price from Level 1 data string.
        """
        parts = lv1_data.split()
        for part in parts:
            if part.startswith("B:"):
                try:
                    return float(part.split(":")[1])
                except ValueError:
                    print("Error converting B: price to float.")
                    return None
        print("B: price not found in Level 1 data.")
        return None
    
    @staticmethod
    def get_ask_price(lv1_data):
        """
        Extracts the ask price from Level 1 data string.
        """
        parts = lv1_data.split()
        for part in parts:
            if part.startswith("A:"):
                try:
                    return float(part.split(":")[1])
                except ValueError:
                    print("Error converting B: price to float.")
                    return None
        print("B: price not found in Level 1 data.")
        return None

    @staticmethod
    def get_shares_to_short(df):
        """
        Retrieves the number of shares to short for a given ticker from the DataFrame.
        """
        for index, row in df.iterrows():
            last_quote_bid = row['last_quote_bid']
            shares_to_locate = row['shares_to_locate']
            short_size = row['short_size']
            df.at[index, 'shares_to_short'] = min(round(short_size / last_quote_bid), shares_to_locate)
        return df