from .core import calculate_all_tariffs


def process_query(query):
    return calculate_all_tariffs(query)

if __name__ == "__main__":
    sample_input = """
        Calculate the different tariffs payable by the following vessel berthing at the port of Durban:\n
        Vessel Details:

        General
        Vessel Name: SUDESTADA
        Built: 2010
        Flag: MLT - Malta
        Classification Society: Registro Italiano Navale
        Call Sign: [Not provided]
        
        Main Details
        Lloyds / IMO No.: [Not provided]
        Type: Bulk Carrier
        DWT: 93,274
        GT / NT: 51,300 / 31,192
        LOA (m): 229.2
        Beam (m): 38
        Moulded Depth (m): 20.7
        LBP: 222
        Drafts SW S / W / T (m): 14.9 / 0 / 0
        Suez GT / NT: - / 49,069
        
        Communication
        E-mail: [Not provided]
        Commercial E-mail: [Not provided]
        
        DRY
        Number of Holds: 7
        
        Cargo Details
        Cargo Quantity: 40,000 MT
        Days Alongside: 3.39 days
        Arrival Time: 15 Nov 2024 10:12
        Departure Time: 22 Nov 2024 13:00
        
        Activity/Operations
        Activity: Exporting Iron Ore
        Number of Operations: 2
    """
    result = calculate_all_tariffs(sample_input)
    print(result)
