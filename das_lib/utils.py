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
