# Designed by Prakash Srinivasan ( prarvy@gmail.com )
# Project Name: Vintage Cars App
# Version: 1.0: Base version by author

import requests
import json

menu_msg = """
+------------------------------------------------------------------------------+
|                         Vintage Cars Database:  M E N U                      |
+==============================================================================+
| 1. List cars  | 2. Add new car  | 3. Delete car  | 4. Update car  | 5. Exit  |        
+------------------------------------------------------------------------------+"""
choice_msg = """>>> Enter your choice (1 - 5): """
header_names = ["id", "brand", "model", "production_year", "convertible"]
header_widths = [8, 15, 18, 17, 13]


def check_server(cid=None):
    if cid is None:
        try:
            reply = requests.get("http://localhost:3000")
        except requests.RequestException:
            return False
        else:
            if reply.status_code == requests.codes.ok:
                return True
            else:
                print("Server responded with Status Code: ", reply.status_code)
                return False
    else:
        try:
            reply = requests.get('http://localhost:3000/vintage_cars/' + str(cid))
        except requests.RequestException:
            return False
        else:
            if reply.status_code == requests.codes.ok:
                return True
            elif reply.status_code == requests.codes.not_found:
                return False
            else:
                print("Server responded with Status Code: ", reply.status_code)
                return False


# returns True or False;
# when invoked without arguments simply checks if server responds;
# invoked with car ID checks if the ID is present in the database;


# prints user menu - nothing else happens here;
def print_menu():
    print(menu_msg)


def read_user_choice():
    try:
        _choice = int(input(choice_msg))
        if _choice in [1, 2, 3, 4, 5]:
            return _choice
        else:
            print('Your Choice entered is not in the range 1 to 5. Please re-try.')
            _choice = read_user_choice()
            return _choice
    except ValueError:
        print('Your Choice is not an Integer. Please re-try.')
        _choice = read_user_choice()
        return _choice
    except BaseException as e:
        print('Unknown Error Occurred. Error Details: ', e)
        exit(0)


# reads user choice and checks if it's valid;
# returns '0', '1', '2', '3' or '4' or '5'


def print_header():
    print('+' + ('-' * 78) + '+')
    for (n, w) in zip(header_names, header_widths):
        print(n.ljust(w).upper(), end='| ')
    print()
    print('+' + ('-' * 78) + '+')


# prints elegant cars table header;


def print_car(car):
    for (n, w) in zip(header_names, header_widths):
        print(str(car[n]).ljust(w), end='| ')
    print()


# prints one car's data in a way that fits the header;


def list_cars():
    try:
        reply = requests.get('http://localhost:3000/vintage_cars')
    except requests.RequestException:
        print('Communication error')
    else:
        if reply.status_code == requests.codes.ok:
            # pass
            print_header()
            # print(reply.json())
            for car in reply.json():
                print_car(car)
        elif reply.status_code == requests.codes.not_found:
            print("Resource not found")
        else:
            print('Server error')


# gets all cars' data from server and prints it;
# if the database is empty prints diagnostic message instead;


def name_is_valid(name):
    try:
        if name == '':
            print('Info: Received an Empty String. Exiting from getting Input.')
            return None
        elif name == ' ':
            print('You have entered an invalid data. Please Retry with proper input data.')
            return None
        else:
            return True
    except ValueError:
        print('You have entered an invalid data. Please Retry with proper input data.')
        return None
    except BaseException as e:
        print(e)
        return None


# checks if name (brand or model) is valid;
# valid name is non-empty string containing
# digits, letters and spaces;
# returns True or False;

def enter_id():
    try:
        input_id = int(input('Car ID (empty string to exit): '))
        if input_id == '':
            print('Info: Received an Empty String. Exiting from getting Input.')
            return None
        else:
            return input_id
    except ValueError:
        print('You have entered an invalid car ID. Please Retry with proper input data.')
        return None
    except BaseException as e:
        print(e)
        return None


# allows user to enter car's ID and checks if it's valid;
# valid ID consists of digits only;
# returns int or None (if user enters an empty line);


def enter_production_year():
    try:
        input_year = int(input('Car Production Year (empty string to exit): '))
        if 1900 <= input_year <= 2000:
            return input_year
        elif input_year == '':
            print('Info: Received an Empty String. Exiting from getting Input.')
            return None
        else:
            print('You have entered an invalid data. Please Retry with proper input data.')
            return None
    except ValueError:
        print('You have entered an invalid data. Please Retry with proper input data.')
        return None
    except BaseException as e:
        print(e)
        return None


# allows user to enter car's production year and checks if it's valid;
# valid production year is an int from range 1900..2000;
# returns int or None  (if user enters an empty line);


def enter_name(what):
    try:
        input_name = input(what)
        if name_is_valid(input_name):
            return input_name
        else:
            print('You have entered an invalid data. Please Retry with proper input data.')
            return None
    except ValueError:
        print('You have entered an invalid data. Please Retry with proper input data.')
        return None
    except BaseException as e:
        print(e)
        return None


# allows user to enter car's name (brand or model) and checks if it's valid;
# uses name_is_valid() to check the entered name;
# returns string or None  (if user enters an empty line);
# argument describes which of two names is entered currently ('brand' or 'model');

def enter_convertible():
    try:
        input_convertible = input('Is this Car Convertible? [ Y/N ] (empty string to exit): ')
        if input_convertible == 'Y':
            return True
        elif input_convertible == 'N':
            return False
        elif input_convertible == '':
            print('Info: Received an Empty String. Exiting from getting Input.')
            return None
        else:
            print('You have entered an invalid data. Please Retry with proper input data.')
            return None
    except ValueError:
        print('You have entered an invalid data. Please Retry with proper input data.')
        return None
    except BaseException as e:
        print(e)
        return None


# allows user to enter Yes/No answer determining if the car is convertible;
# returns True, False or None  (if user enters an empty line);


# asks user for car's ID and tries to delete it from database;
def delete_car():
    _id = enter_id()
    if _id is None:
        return None
    else:
        if check_server(cid=_id):
            try:
                reply = requests.delete('http://localhost:3000/vintage_cars/' + str(_id))
                print("Status: Car ID: {} deleted Successfully. Status Code=".format(_id) + str(reply.status_code))
            except requests.RequestException:
                print("Error: Connection Failed.")
        else:
            print('The Car ID is absent in Database. Please provide a different ID.')
            return None


def input_car_data(with_id):
    if with_id:
        _id = enter_id()
        if _id is None:
            return None
        else:
            if not check_server(cid=_id):
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
                new_car_data = {'id': _id,
                                'brand': brand,
                                'model': model,
                                'production_year': production_year,
                                'convertible': convertible}
                return new_car_data
            else:
                print('The Car ID already exists. Please provide a different ID.')
                return None

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
        updated_car_data = {'brand': brand,
                            'model': model,
                            'production_year': production_year,
                            'convertible': convertible}
        return updated_car_data


# lets user enter car data;
# argument determines if the car's ID is entered (True) or not (False);
# returns None if user cancels the operation or a dictionary of the following structure:
# {'id': int, 'brand': str, 'model': str, 'production_year': int, 'convertible': bool }


def add_car():
    new_car_json = input_car_data(True)
    h_content = {'Content-Type': 'application/json'}
    try:
        if new_car_json is None:
            pass
        else:
            reply = requests.post('http://localhost:3000/vintage_cars', headers=h_content,
                                  data=json.dumps(new_car_json))
            print("Status: New car added Successfully. Status Code=" + str(reply.status_code))
    except requests.RequestException:
        print("Error: Connection Failed.")


# invokes input_car_data(True) to gather car's info and adds it to the database;


def update_car():
    _id = enter_id()
    if _id is None:
        return None
    else:
        if check_server(cid=_id):
            updated_car_data = input_car_data(False)
            try:
                # h_close = {'Connection': 'Close'}
                h_content = {'Content-Type': 'application/json'}
                reply = requests.put('http://localhost:3000/vintage_cars/' + str(_id), headers=h_content,
                                     data=json.dumps(updated_car_data))
                print("res=" + str(reply.status_code))
                # reply = requests.get('http://localhost:3000/cars/', headers=h_close)
            except requests.RequestException:
                print('Communication error')
        else:
            print("The Car ID doesn't exists. Please provide a different ID.")


# invokes enter_id() to get car's ID if the ID is present in the database;
# invokes input_car_data(False) to gather new car's info and updates the database;


while True:
    if not check_server():
        print("Server is not responding - quitting!")
        exit(1)
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
        exit(0)
