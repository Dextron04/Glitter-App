import os
from django.shortcuts import render
import requests
import json
from django.core.paginator import Paginator
import datetime
from datetime import datetime, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')


def preTemplateView(request):
    return render(request, 'Home.html')

def display_home(request):
    return render(request,'Home.html')

def display_about(request):
    return render(request,'About.html')
    

def handle_invalid_url(request, invalid_url):
    return render(request, 'error.html', {'error_message': f'The URL "{invalid_url}" is not valid.'})

# Creates a list of available dates starting from the first upcoming friday
def create_friday_list(request):
    print("[DEBUG] CREATING FRIDAY LIST")
    currentDate = date.today()

    # increment until friday if it's not already friday
    while currentDate.weekday() != 4:
        currentDate += datetime.timedelta(days=1)
    
    friday_list = [currentDate.strftime("%A %B %d")]
    for i in range(0, 19): # up to 20 weeks in advance
        # add one week to date object
        currentDate += datetime.timedelta(days=7)

        # date format: %A = day of week, %B = month, %d = day of the month
        readableDate = currentDate.strftime("%A %B %d")
        print(readableDate)
        friday_list.append(readableDate)

    print("[DEBUG] PASSING FRIDAY LIST TO PAGE")

    context = {
        "dates": friday_list
    }

    return render(request, 'Filter.html', context)



# This is where the "heavy lifting" of the filtering process takes place.
# When the user hits submit, we retrieve the search parameters they entered with the "request" parameter.
# Based on the symbol and expiration parameters, we fetch company data and an options chain from Tradier API.
# Then, based on the price range the user entered, we filter the list of options.
# Once the options have been narrowed down, we render them in context back to the HTML page for the user to see.
# request: user input from the page
# returns: rendered context containing filtered options
def display_user_options(request):
    # user hits submit on form -> get tradier data -> filter -> return context -> render with context
    print("\n\n---------------------------------------------------------")
    print("[DEBUG] USER FORM RECEIVED")

    # get symbol and date
    symbol_query = request.GET.get("search-box-ticker")
    date_query = request.GET.get("search-box-exp")

    print("[DEBUG] SYMBOL:", symbol_query)
    print("[DEBUG] DATE:", date_query) # YYYY-MM-DD

    if(str(date_query) != "None"):
        date_format = "%A %B %d"
        date = datetime.strptime(date_query, date_format)
        date_correct_format = date.strftime("2023-%m-%d")
    else:
        date_correct_format = " "

    print("[DEBUG] DATE: ", date_correct_format)

    # get upper and lower bound for the price along with what type of search the user wants
    price_range_query = request.GET.get("price-range-select") # less than x, greater than x, or between x and y
    price_query_one = request.GET.get("price-entry-one") # first text box
    price_query_two = request.GET.get("price-entry-two") # second text box, only used for the "between" selection

    print("[DBUG] PRICE ENTRY ONE: ", price_query_one)
    print("[DBUG] PRICE ENTRY TWO: ", price_query_two)
    print("[DBUG] PRICE ENTRY RANGE: ", price_range_query)


    # price_range_query can be greater than value, less than value, or between values
    # need to make sure text boxes aren't empty first! this error checking may be changed later, this is just the easiest way for now
    if price_query_one: # text box not empty
        if price_range_query == "price-greater-than":
            price_lowerbound = int(price_query_one)
            price_upperbound = 9999999999
            print("[DEBUG] GREATER THAN ", price_lowerbound)

        elif price_range_query == "price-less-than":
            price_lowerbound = 0
            price_upperbound = int(price_query_one)
            print("[DEBUG] LESS THAN ", price_upperbound)

        else: # between
            if price_query_two: # text box not empty
                price_lowerbound = int(price_query_one)
                price_upperbound = int(price_query_two)
                print("[DEBUG] BETWEEN ", price_lowerbound, " AND ", price_upperbound)
            else:
                print("[ERROR] PRICE QUERY TWO EMPTY ")
                price_lowerbound = 0
                price_upperbound = 0
    else:
        print("[ERROR] PRICE QUERY ONE EMPTY ")
        price_lowerbound = 0
        price_upperbound = 0
    
    print("\n[DEBUG] RETRIEVING TRADIER DATA...")

    # get symbol, description, and options data from tradier API
    context = tradier_data(symbol_query, date_correct_format)

    valid_list = []
    
    # filter options list
    if(len(context['options_json']) != 0):
        valid_list = filter_options(context['options_json'], price_upperbound, price_lowerbound)

    # update context
    context['valid_options'] = valid_list

    print(len(valid_list))

    paginator = Paginator(valid_list, 10)  # 10 items per page
    page_number = request.GET.get('page')
    paginated_options = paginator.get_page(page_number)

    context['paginated_options'] = paginated_options

    # print("\n[DEBUG] CONTEXT:", context)
    print("\n[DEBUG] RENDERING CONTEXT TO TEMPLATE")
    print("---------------------------------------------------------\n\n")
    return render(request, 'Filter.html', context)


# Fetch options chain from tradier API using symbol and expiration date as parameters
# returns an API response in the form of a JSON
def create_options_response(symbol, expiration):
    return requests.get('https://api.tradier.com/v1/markets/options/chains',
                        params={
                            'symbol': symbol, 'expiration': expiration},
                        headers={'Authorization': 'Bearer 9A8RGSU01G1cq0KOvOoCmgFie4Ft',
                            'Accept': 'application/json'}
                        )


# Fetch information about a company from tradier API 
# returns an API response in the form of a JSON
# EXAMPLE: to lookup GOOG, type "goog" or similar. "alphabet" will not work.
def create_company_response(symbol):
    return requests.get('https://api.tradier.com/v1/markets/lookup',
                        params={
                            'q': symbol, 'exchanges': 'Q'},
                        headers={'Authorization': 'Bearer 9A8RGSU01G1cq0KOvOoCmgFie4Ft',
                            'Accept': 'application/json'}
                        )


# Given the entire options chain, narrow it down to options the user is interested in
# options_data: entire options chain JSON (see optionsData.json)
# max_price and min_price: the upper and lower bounds for a valid price
# returns: a list of dictionaries containing an option's strike price, volume, expiration date, price, and number
def filter_options(options_data, max_price, min_price):
    # if max_price and min_price are equal, the user is looking for an exact price
    print("[DEBUG] FILTERING WITH MAX PRICE: ", max_price, " AND MIN PRICE: ", min_price)

    valid_options_list = []

    # hard-coded filters:
    min_open_interest = 44 # open interest must be over 44
    
    number = 0 # keep track of amount of valid options found

    # Length of the fetched data
    options_size = len(options_data["options"]["option"])

    # odd numbers are call options
    for i in range(1, options_size, 2):
        try:
            bid = float(options_data["options"]["option"][i]["bid"])
            ask = float(options_data["options"]["option"][i]["ask"])
            price = (bid + ask) / 2
        except (ValueError, KeyError, TypeError) as e:
            print("Error:", e)
        # print("[DEBUG] OPTION PRICE: ", options_data["options"]["option"][i]["ask"])
        # print("[DEBUG] Volume: ", options_data["options"]["option"][i]["volume"])
        if (options_data["options"]["option"][i]["open_interest"] > min_open_interest) and (price < max_price and price > min_price): 
            print("[DEBUG] FOUND A VALID CALL OPTION")

            # extract relevant data
            number += 1
            strike = options_data["options"]["option"][i]["strike"]
            volume = options_data["options"]["option"][i]["volume"]
            exp = options_data["options"]["option"][i]["expiration_date"]
            symbol = options_data["options"]["option"][i]["root_symbol"]

            response_company = create_company_response(symbol)
            company_data = json.loads(response_company.text)

            if str(company_data['securities']) != "None" : 
                if(len(company_data['securities']) >= 1):
                    if(len(company_data['securities']['security']) == 4):
                        description = company_data['securities']['security']['description']
                    else:
                        description = company_data['securities']['security'][0]['description']
                else:
                    description = company_data['securities']['security']['description']
            else:
                print("[ERROR] COMPANY DATA FETCH FAILED")
                
            # create dictionary
            opt = {
                'number' : 0,
                'description' : description,
                'price' : ("$ %1.2f" % price),
                'max price': ("$ %1.2f" % (price * 100)),
                'strike price' : strike,
                'volume': volume,
                'expiration date' : exp,
            }

            # append to valid options list
            valid_options_list.append(opt)
        else:
            print("[DEBUG] DID NOT FIND A VALID CALL OPTION")

    # sort list of valid options by volume, high to low
    valid_options_list = sorted(valid_options_list, key=lambda d: d['volume'], reverse=True)

    # re-number options
    for i in range (0, number):
        valid_options_list[i]["number"] = i + 1 # numbering starts at 1, not 0

    return valid_options_list


# API request with Tradier
def tradier_data(given_symbol, expiration): 
    print("[DEBUG] REQUESTING OPTIONS WITH GIVEN SYMBOL: ", given_symbol, " AND EXPIRATION DATE: ", expiration)

    # default context of placeholder values. this is what context will look like in the case of an early return.
    context = {
        'valid_options' : [],
        'company_data' : "NO COMPANY DATA",
        'company_symbol' : "NO COMPANY SYMBOL",
        'options_json' : {}
    }

    print("[DEBUG] FETCHING COMPANY RESPONSE")
    # Creating a response to fetch the company details
    response_company = create_company_response(given_symbol)

    # Verify search returned a company
    if response_company.status_code == 200: # successful response
        print("[DEBUG] SUCCESSFUL COMPANY RESPONSE")

        # Load response into a JSON
        company_data = json.loads(response_company.text)

        # output JSON to file
        test_file_company = open("companyData.json", "w")
        json.dump(company_data, test_file_company, indent=2)
        test_file_company.close()

        if str(company_data['securities']) != "None" : # verify something was found
            # Checking if we have more company data than 1.
            if(len(company_data['securities']) >= 1):
                if(len(company_data['securities']['security']) == 4):
                    symbol = company_data['securities']['security']['symbol']
                    description = company_data['securities']['security']['description']
                else:
                    symbol = company_data['securities']['security'][0]['symbol']
                    description = company_data['securities']['security'][0]['description']
            else:
                symbol = company_data['securities']['security']['symbol']
                description = company_data['securities']['security']['description']
        else:
            print("[DEBUG] COULD NOT FIND A COMPANY WITH THAT SYMBOL. TRY REFINING SEARCH TERMS.")
            return context # early return with no results
    else:
        print("[ERROR] !!! UNSUCCESSFUL COMPANY RESPONSE. RESPONSE CODE: ", response_company.status_code)
        return context # early return with no results


    print("[DEBUG] FETCHING OPTIONS CHAIN RESPONSE WITH SYMBOL: ", symbol, " AND DATE: ", expiration)
    # Creating a response to fetch options chain
    response_options = create_options_response(symbol, expiration)


    # Verify options chain was found with at least one option
    if response_options.status_code == 200:
        print("[DEBUG] SUCCESSFUL OPTIONS RESPONSE")

        # Load response into a JSON
        options_data = json.loads(response_options.text)

        # output JSON to file
        test_file_options = open("optionsData.json", "w")
        json.dump(options_data, test_file_options, indent=2)
        test_file_options.close()
        
        if( str(options_data['options']) == "None" ):
            print("[DEBUG] OPTIONS FOUND BUT NO RESULTS. TRY REFINING SEARCH TERMS.")
            return context # early return with no results
    else:
        print("[ERROR] UNSUCCESSFUL OPTIONS RESPONSE. RESPONSE CODE: ", response_options.status_code)
        return context # early return with no results

    # update context to pass back to page
    context = {
        'company_data' : description,
        'company_symbol' : symbol,
        'valid_options' : [],
        'options_json' : options_data
    }


    return context


# [DEBUG] Function to print the options list to the console
def debug_print(options_list):
    print("\n[DEBUG] PRINTING OPTIONS LIST...\n")
    # iterate through list
    for item in options_list:
        # each item is a dictionary with number, strike price, volume, exp date, and price
        print(item['number'])
        print("\tSTRIKE PRICE: ", item['strike price'])
        print("\tVOLUME: ", item['volume'])
        print("\tEXPIRATION DATE: ", item['expiration date'])
        print("\tPRICE: ", item['price'])
        print()


# [DEBUG] Function to store the fetched data in a file
def debug_file(options_data, company_data):
    # For printing the data in a separate file
    test_file = open("optionsData.json", "w")
    json.dump(options_data, test_file, indent=2)
    test_file.close()

    test_file_2 = open("companyData.json", "w")
    json.dump(company_data, test_file_2, indent=2)
    test_file_2.close()

