# Designed by Prakash Srinivasan ( prarvy@gmail.com )
# Project Name: Vintage Cars App
# Version: 1.0: Base version by author
import requests
import json

local_host_path = "http://localhost:3000"
header_names = ["id", "brand", "model", "production_year", "convertible"]
header_widths = [8, 15, 18, 17, 13]


# returns True or False;
# when invoked without arguments simply checks if server responds;
# invoked with car ID checks if the ID is present in the database;
def check_server(cid=None):
    _path = '' if cid is None else '/vintage_cars/' + str(cid)
    try:
        reply = requests.get(local_host_path + _path)
        return reply.status_code in (requests.codes.ok, 204)
    except requests.RequestException:
        return False


# prints user menu - nothing else happens here;
def print_menu():
    print("""
+------------------------------------------------------------------------------+
|                         Vintage Cars Database:  M E N U                      |
+==============================================================================+
| 1. List cars  | 2. Add new car  | 3. Delete car  | 4. Update car  | 5. Exit  |        
+------------------------------------------------------------------------------+""")


# reads user choice and checks if it's valid;
# returns '1', '2', '3', '4' or '5'
def read_user_choice():
    while True:
        try:
            _choice = int(input('>>> Enter your choice (1 - 5): '))
        except ValueError:
            print('Your Choice is not an Integer. Please re-try.')
            continue
        if _choice not in range(1, 6):
            print('Your Choice entered is not in the range 1 to 5. Please re-try.')
            continue
        return _choice


# prints elegant cars table header;
def print_header():
    print('+' + '-' * 78 + '+')
    print(*[n.ljust(w).upper() for n, w in zip(header_names, header_widths)], sep='| ')
    print('+' + '-' * 78 + '+')


# prints one car's data in a way that fits the header;
def print_car(car):
    print(*[str(car[n]).ljust(w) for (n, w) in zip(header_names, header_widths)], sep='| ')


# gets all cars' data from server and prints it;
# if the database is empty prints diagnostic message instead;
def list_cars():
    try:
        reply = requests.get('http://localhost:3000/vintage_cars')
    except requests.RequestException:
        print('Error: Communication error occurred.')
    else:
        if reply.status_code == 200:
            if len(reply.json()) == 0:
                print('****** Database is empty ******')
            else:
                print_header()
                for car in reply.json():
                    print_car(car)
                print('+' + '-' * 78 + '+')
        elif reply.status_code == 400:
            print("Error: Resource not found.")
        else:
            print('Error: Server error occurred.')


# checks if name (brand or model) is valid;
# valid name is non-empty string containing
# digits, letters and spaces;
# returns True or False;
def name_is_valid(name):
    name_string = ''.join(list(map(lambda x: x.strip(), name.split())))
    if name == '':
        print('Info: Received an Empty String. Exiting from getting Input.')
        return False
    elif len(name_string) == 0 or not name_string.isalnum():
        print('You have entered an invalid data. Please Retry with proper input data.')
        return False
    else:
        return True


# allows user to enter car's ID and checks if it's valid;
# valid ID consists of digits only;
# returns int or None (if user enters an empty line);
def enter_id():
    input_id = input('Car ID (empty string to exit): ').strip()
    if input_id == '':
        print('Info: Received an Empty String. Exiting from getting Input.')
        return None
    else:
        try:
            return int(input_id)
        except ValueError:
            print('You have entered an invalid car ID. Please Retry with proper input data.')
            return None


# allows user to enter car's production year and checks if it's valid;
# valid production year is an int from range 1900..2000;
# returns int or None  (if user enters an empty line);
def enter_production_year():
    input_year = input('Car Production Year (empty string to exit): ').strip()
    if input_year == '':
        print('Info: Received an Empty String. Exiting from getting Input.')
        return None
    elif not input_year.isdigit() or not 1900 <= int(input_year) <= 2000:
        print('You have entered an invalid data. Please Retry with proper input data.')
        return None
    else:
        return int(input_year)


# allows user to enter car's name (brand or model) and checks if it's valid;
# uses name_is_valid() to check the entered name;
# returns string or None  (if user enters an empty line);
# argument describes which of two names is entered currently ('brand' or 'model');
def enter_name(what):
    name = input(what).strip()
    if name_is_valid(name):
        return name
    else:
        print('You have entered an invalid data. Please Retry with proper input data.')
        return None


# allows user to enter Yes/No answer determining if the car is convertible;
# returns True, False or None  (if user enters an empty line);
def enter_convertible():
    input_convertible = input('Is this Car Convertible? [ Y/N or Yes/No ] (empty string to exit): ').strip()
    if input_convertible == '':
        print('Info: Received an Empty String. Exiting from getting Input.')
        return None
    elif input_convertible.upper() in ['Y', 'YES', 'N', 'NO']:
        return input_convertible in ['Y', 'YES']
    else:
        print('You have entered an invalid data. Please Retry with proper input data.')
        return None


# asks user for car's ID and tries to delete it from database;
def delete_car():
    _id = enter_id()
    if not check_server(cid=_id):
        print('The Car ID is absent in Database. Please provide a different ID.')
        return None
    try:
        reply = requests.delete('http://localhost:3000/vintage_cars/' + str(_id))
        print("Status: Car ID: {} deleted Successfully. Status Code=".format(_id) + str(reply.status_code))
    except requests.RequestException:
        print('Error: Communication error occurred.')


# lets user enter car data;
# argument determines if the car's ID is entered (True) or not (False);
# returns None if user cancels the operation or a dictionary of the following structure:
# {'id': int, 'brand': str, 'model': str, 'production_year': int, 'convertible': bool }

def input_car_data(with_id):
    if with_id:
        _id = enter_id()
        if _id is None:
            return None
        if check_server(cid=_id):
            print('The Car ID already exists. Please provide a different ID.')
            return None
        brand = enter_name('Car Brand (empty string to exit): ')
        if brand is None:
            return None
        model = enter_name('Car Model (empty string to exit): ')
        if model is None:
            return None
        production_year = enter_production_year()
        if production_year is None:
            return None
        convertible = enter_convertible()
        if convertible is None:
            return None
        return {'id': _id,
                'brand': brand,
                'model': model,
                'production_year': production_year,
                'convertible': convertible}
    else:
        brand = enter_name('Car Brand (empty string to exit): ')
        if brand is None:
            return None
        model = enter_name('Car Model (empty string to exit): ')
        if model is None:
            return None
        production_year = enter_production_year()
        if production_year is None:
            return None
        convertible = enter_convertible()
        if convertible is None:
            return None
        return {'brand': brand,
                'model': model,
                'production_year': production_year,
                'convertible': convertible}


# invokes input_car_data(True) to gather car's info and adds it to the database;
def add_car():
    new_car_json = input_car_data(True)
    if new_car_json is None:
        return
    try:
        reply = requests.post('http://localhost:3000/vintage_cars', headers={'Content-Type': 'application/json'},
                              data=json.dumps(new_car_json))
        print("Status: New car added Successfully. Status Code=" + str(reply.status_code))
    except requests.RequestException:
        print('Error: Communication error occurred.')


# invokes enter_id() to get car's ID if the ID is present in the database;
# invokes input_car_data(False) to gather new car's info and updates the database;
def update_car():
    _id = enter_id()
    if _id is None:
        return
    if not check_server(cid=_id):
        print("The Car ID doesn't exists. Please provide a different ID.")
    updated_car_data = input_car_data(False)
    try:
        reply = requests.put('http://localhost:3000/vintage_cars/' + str(_id), headers={'Content-Type': 'application/json'},
                             data=json.dumps(updated_car_data))
        print("Status: Car ID: {} Updated Successfully. Status Code=".format(_id) + str(reply.status_code))
    except requests.RequestException:
        print('Error: Communication error occurred.')


while True:
    if not check_server():
        print("Server is not responding - quitting!")
        break
    print_menu()
    choice = read_user_choice()
    if choice == 1:
        list_cars()
    elif choice == 2:
        add_car()
    elif choice == 3:
        delete_car()
    elif choice == 4:
        update_car()
    elif choice == 5:
        print('The application is Exiting. Bye!')
        break
