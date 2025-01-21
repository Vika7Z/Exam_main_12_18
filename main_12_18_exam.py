# Створити додаток "Домовий менеджмент".
# Основне завдання проєкту — надати користувачеві можливість зберігати інформацію про мешканців будинку.
# Інтерфейс додатка має надавати такі можливості:
# ● Додавання мешканців будинку.
# ● Видалення мешканців будинку.
# ● Додавання квартир (обов'язкова наявність можливості додавати інформацію про поверх).
# ● Видалення квартир.
# ● Закріплення мешканців за квартирою.
# ● Відкріплення мешканців від квартири.
#
# ● Збереження інформації у файл.
# ● Завантаження інформації з файлу.
#
# ● Створення звітів за такими параметрами:
# ■ Відображення повного списку мешканців;
# ■ Відображення повного списку квартир;
# ■ Відображення інформації про конкретну квартиру;
# ■ Відображення інформації про квартири на конкретному поверсі;
# ■ Відображення інформації про квартири одного типу (наприклад, відобразити всі однокімнатні квартири).


class Resident:
    def __init__(self, resident_id: int, name: str):
        self.resident_id = resident_id
        self.name = name

    def to_dict(self):
        # Додати об'єкт Resident у словник для збереження в JSON
        return {
            'resident_id': self.resident_id,
            'name': self.name
        }

    @classmethod
    def from_dict(cls, data: dict):
        # Відновити об'єкт Resident зі словника JSON
        resident = cls(resident_id=data['resident_id'],name=data['name'])
        return resident

    def __str__(self):
        return f"Resident ID: {self.resident_id}, Name: {self.name}"

    def __repr__(self):
        return self.__str__()


class Apartment:
    def __init__(self, apartment_number: int, floor: int, number_of_rooms: int, is_vacant: bool = True):
        self.apartment_number = apartment_number
        self.floor = floor
        self.number_of_rooms = number_of_rooms
        self.is_vacant = is_vacant
        self.residents: list[Resident] = []
        self.main_resident: Resident | None = None

    def to_dict(self):
        # Додати об'єкт Apartment у словник для збереження в JSON
        return {
            'apartment_number': self.apartment_number,
            'floor': self.floor,
            'number_of_rooms': self.number_of_rooms,
            'is_vacant': self.is_vacant,
            'residents': [resident.to_dict() for resident in self.residents],
            'main_resident': self.main_resident.to_dict() if self.main_resident else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        # Відновити об'єкт Apartment зі словника JSON
        apartment = cls(data['apartment_number'], data['floor'], data['number_of_rooms'], data['is_vacant'])
        apartment.residents = [Resident.from_dict(resident_data) for resident_data in data['residents']]
        apartment.main_resident = Resident.from_dict(data['main_resident']) if data.get('main_resident') else None
        return apartment

    def __str__(self):
        is_vacant_str = "Vacant" if self.is_vacant else 'Occupied'
        residents_str = ', '.join(str(resident) for resident in self.residents)
        main_resident_str = str(self.main_resident) if self.main_resident else 'None'
        return (f"Apartment no.{self.apartment_number}, floor: {self.floor}, "
                f"{self.number_of_rooms} rooms: {is_vacant_str}, "
                f"Residents: {residents_str}, Main Resident: {main_resident_str}")

    def __repr__(self):
        return self.__str__()


class ApartmentBuilding:
    def __init__(self, building_number: int, quantity_floor=2, rooms_per_floor: list[int]=None):
        if not isinstance(building_number, int) or building_number <= 0:
            raise ValueError("Building number must be a positive integer.")
        if not isinstance(quantity_floor, int) or quantity_floor <= 0:
            raise ValueError("Building must have at least one floor (quantity_floor >= 1).")
        if rooms_per_floor is not None and (
                not isinstance(rooms_per_floor, list)
                or not all(isinstance(room, int) and room > 0 for room in rooms_per_floor)
        ):
            raise ValueError("Rooms_per_floor must be a list of only positive integers.")
        if rooms_per_floor is None:
            rooms_per_floor = [1, 1, 2, 3]

        self.building_number = building_number
        self.quantity_floor = quantity_floor
        self.rooms_per_floor = rooms_per_floor
        self.apartments: list[Apartment] = []
        self._generate_apartments()

    def _generate_apartments(self):
        if self.apartments:  # Якщо список не порожній, Запобігаємо дублюванню квартир - пропустити генерацію
            return
        apartment_number = 1
        for floor in range(1, self.quantity_floor + 1):
            for rooms in self.rooms_per_floor:
                apartment = Apartment(apartment_number=apartment_number, floor=floor, number_of_rooms=rooms) # , is_vacant=True
                self.apartments.append(apartment)
                apartment_number += 1

    def to_dict(self):
        # Додати об'єкт ApartmentBuilding у словник для збереження в JSON
        return {
            'building_number': self.building_number,
            'quantity_floor': self.quantity_floor,
            'rooms_per_floor': self.rooms_per_floor,
            'apartments': [apartment.to_dict() for apartment in self.apartments]
        }

    @classmethod
    def from_dict(cls, data: dict):
        # Відновити об'єкт ApartmentBuilding зі словника JSON

        # Перевірка наявності обов'язкових полів
        if 'building_number' not in data or 'quantity_floor' not in data:
            raise KeyError("Missing required fields: 'building_number' or 'quantity_floor'.")

        # Перевірка типів
        if not isinstance(data['building_number'], int) or not isinstance(data['quantity_floor'], int):
            raise ValueError("'building_number' and 'quantity_floor' must be integers.")

        building = cls(data['building_number'], data['quantity_floor'], data.get('rooms_per_floor'))

        # Відновлення квартир
        if 'apartments' in data and isinstance(data['apartments'], list):
            building.apartments = [Apartment.from_dict(apartment)
                                   for apartment in data['apartments']
                                   if isinstance(apartment, dict)]
        else:
            raise ValueError("'apartments' must be a list of dictionaries.")

        return building

    def __str__(self):
        vacant_apartments = sum(1 for apt in self.apartments if apt.is_vacant)
        return (f"Building no.{self.building_number}, Floors: {self.quantity_floor}, "
                f"Apartments: {len(self.apartments)} "
                f"({vacant_apartments} vacant)")

    def __repr__(self):
        return self.__str__()



import json

class FileManager:
    @staticmethod
    def save_to_file(filename: str, data: dict):
        with open(filename, 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_from_file(filename: str):  # , cls: Type[object]
        try:
            with open(filename, 'r', encoding='UTF-8') as file:
                return json.load(file)  # Зчитуємо весь файл як один великий об'єкт
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print(f"Error: File '{filename}' is corrupted.")
            return {}



class BuildingManager:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls, *args, **kwargs)
        return cls._instances[cls]

    def __init__(self):
        self.buildings: list[ApartmentBuilding] = []
        self.residents: list[Resident] = []
        self.residents_by_id: dict[int, Resident] = {}
        self.residents_by_name: dict[str, Resident] = {}

        # Завантаження даних з одного файлу
        self.load_data()

    def add_building(self, building: ApartmentBuilding):
        # Перевіряємо, чи вже є будинок з таким номером
        if any(b.building_number == building.building_number for b in self.buildings):
            print(f"Building with number {building.building_number} already exists.")
            raise ValueError(f"ValueError: Building with number {building.building_number} already exists.")
        else:
            self.buildings.append(building)
            print(f"Building {building.building_number} added successfully.")

    def load_data(self):
        try:
            # Завантажуємо будинки та мешканців з файлу JSON
            data = FileManager.load_from_file('buildings_and_residents_1.json') # , dict

            # Відновлюємо будинки з їхніми квартирами та мешканцями
            buildings_data = data.get('buildings', [])
            self.buildings = [ApartmentBuilding.from_dict(building) for building in buildings_data]

            # Створення мешканців
            self.residents = {resident: resident
                                for building in self.buildings
                                for apartment in building.apartments
                                for resident in apartment.residents}

            # Створення by_id по мешканцях
            self.residents_by_id = {resident.resident_id: resident
                                    for building in self.buildings
                                    for apartment in building.apartments
                                    for resident in apartment.residents}
            # Створення by_name по мешканцях
            self.residents_by_name = {resident.name: resident
                                      for building in self.buildings
                                      for apartment in building.apartments
                                      for resident in apartment.residents}
        except Exception as e:
            print(f"Failed to load data: {e}")
            self.buildings = []
            self.residents_by_id = {}
            self.residents_by_name = {}

    # Пошук мешканця по id
    def find_resident_by_id(self, resident_id: int):
        return self.residents_by_id.get(resident_id, None)
    # Пошук мешканця по імені
    def find_resident_by_name(self, name: str):
        return self.residents_by_name.get(name, None)

    def save_data(self):
        # Збереження даних про  будинки та мешканців в один файл JSON
        data = {
            'buildings': [building.to_dict() for building in self.buildings]
        }
        FileManager.save_to_file('buildings_and_residents_1.json', data)

    # ***************************************************************************

    # Знайти будинок за його номером
    def get_building_by_number(self, building_number: int):   #  -> ApartmentBuilding:
        return next((building for building in self.buildings if building.building_number == building_number), None)

    # Знайти квартиру за її номером у конкретному будинку
    def get_apartment_by_number(self, building_number: int, apartment_number: int):
        # Знаходимо будинок за номером
        building = self.get_building_by_number(building_number)
        if building:
            # Шукати квартиру в знайденому будинку
            return next((apartment for apartment in building.apartments
                         if apartment.apartment_number == apartment_number),None)
        else:
            print(f"Building no.{building_number} not found.")
            return None  # Якщо будинок не знайдено

    # ***************************************************************************

    # Перевіряє, чи мешканець з вказаним resident_id вже заселений у будь-якій квартирі
    def is_resident_already_assigned(self, resident_id: int) -> bool:
        for building in self.buildings:
            for apartment in building.apartments:
                if any(existing_resident.resident_id == resident_id for existing_resident in apartment.residents):
                    print(f"Resident with ID {resident_id} is already assigned to another apartment.")
                    return True
        return False

    # ***************************************************************************

    def add_resident_to_apartment(self, building_number: int, apartment_number: int, resident: Resident,
                                  is_main_resident: bool = False):
        # Перевірка, чи мешканець вже заселений
        if self.is_resident_already_assigned(resident.resident_id):
            return

        # Знаходимо квартиру за номером будинку і квартири
        building = self.get_building_by_number(building_number)
        if building:
            apartment = next((apt for apt in building.apartments if apt.apartment_number == apartment_number), None)
            if apartment:
                apartment.residents.append(resident)

                # Якщо потрібно, встановлюємо головного мешканця
                if is_main_resident:
                    apartment.main_resident = resident

                apartment.is_vacant = False  # Квартира тепер зайнята

                self.save_data()  # Зберігаємо актуальні дані
            else:
                print(f"Apartment no.{apartment_number} not found in building {building_number}.")
        else:
            print(f"Building no.{building_number} not found.")

    # ***************************************************************************

    def remove_resident_from_apartment(self, building_number: int, apartment_number: int, resident_id: int):  # resident: Resident
        # Знаходимо квартиру за номером будинку і квартири
        building = self.get_building_by_number(building_number)
        if building:
            apartment = next((apt for apt in building.apartments if apt.apartment_number == apartment_number), None)
            if apartment:
                # Знаходимо мешканця за ID
                resident = next((r for r in apartment.residents if r.resident_id == resident_id), None)
                if resident in apartment.residents:
                    apartment.residents.remove(resident)
                    print(f"Resident ID {resident_id} removed from apartment no.{apartment_number}.")  # resident.resident_id

                    # Якщо видаляється головний мешканець, потрібно призначити нового головного
                    if apartment.main_resident and apartment.main_resident.resident_id == resident_id:
                        if apartment.residents:  # Якщо є інші мешканці, встановлюємо головним першого
                            apartment.main_resident = apartment.residents[0]
                        else:
                            apartment.main_resident = None  # Якщо мешканців немає, головний мешканець стає None

                    # Якщо більше немає мешканців, квартира стає вільною
                    if not apartment.residents:  # Якщо список мешканців порожній
                        apartment.is_vacant = True

                    self.save_data()  # Зберігаємо актуальні дані
                else:
                    print(f"Resident ID {resident_id} not found in apartment no.{apartment_number}.") # resident.resident_id
            else:
                print(f"Apartment no.{apartment_number} not found in building no.{building_number}.")
        else:
            print(f"Building no.{building_number} not found.")

    # ***************************************************************************

    # Відображення повного списку головних мешканців будинку:
    def show_all_main_residents(self, building_number: int):
        # Знаходимо будинок за номером
        building = self.get_building_by_number(building_number)
        if building:
            # Створюємо список головних мешканців
            residents = [apartment.main_resident for apartment in building.apartments if apartment.main_resident]

            if residents:
                for resident in residents:
                    print(resident)  # Виводимо кожного головного мешканця
            else:
                print(f"No main residents in building no.{building_number}.")
        else:
            print(f"Building no.{building_number} not found.")
            return []

    # Відображення повного списку мешканців будинку:
    def show_all_residents(self, building_number: int):
        # Знаходимо будинок за номером
        building = self.get_building_by_number(building_number)
        if building:
            residents = []
            for apartment in building.apartments:
                residents.extend(apartment.residents)  # Додаємо всіх мешканців з кожної квартири
            # return residents
            if residents:
                for resident in residents:
                    print(resident)
            else:
                print(f"No residents in building no.{building_number}.")
        else:
            print(f"Building no.{building_number} not found.")
            return []

    # Відображення повного списку квартир будинку:
    def show_all_apartments(self, building_number: int):
        # Знаходимо будинок за номером
        building = self.get_building_by_number(building_number)
        if building:
            # return building.apartments
            if building.apartments:
                for apartment in building.apartments:
                    print(apartment)
            else:
                print(f"No apartments in building no.{building_number}.")
        else:
            print(f"Building no.{building_number} not found.")
            return []

    # Відображення інформації про конкретну квартиру по номеру квартири будинку:
    def show_apartment_info(self, building_number: int, apartment_number: int):
        # Знаходимо будинок за номером
        building = self.get_building_by_number(building_number)
        if building:
            # Знаходимо квартиру за номером
            apartment = next((apt for apt in building.apartments if apt.apartment_number == apartment_number), None)
            if apartment:
                # return apartment
                print(apartment)
            else:
                print(f"Apartment no.{apartment_number} not found in Building no.{building_number}.")
                return None
        else:
            print(f"Building no.{building_number} not found.")
            return None

    # Відображення інформації про квартири на конкретному поверсі будинку:
    def show_apartments_by_floor(self, building_number: int, floor: int):
        # Знаходимо будинок за номером
        building = self.get_building_by_number(building_number)
        if building:
            apartments_on_floor = [apt for apt in building.apartments if apt.floor == floor]
            # return apartments_on_floor
            if apartments_on_floor:
                for apartment in apartments_on_floor:
                    print(apartment)
            else:
                print(f"No apartments on {floor} floor found in building no.{building_number}.")
        else:
            print(f"Building no.{building_number} not found.")
            return []

    # Відображення інформації про квартири одного типу (за кількістю кімнат) будинку:
    def show_apartments_by_room_type(self, building_number: int, number_of_rooms: int):
        # Знаходимо будинок за номером
        building = self.get_building_by_number(building_number)
        if building:
            apartments_of_type = [apt for apt in building.apartments if apt.number_of_rooms == number_of_rooms]
            # return apartments_of_type
            if apartments_of_type:
                for apartment in apartments_of_type:
                    print(apartment)
            else:
                print(f"No apartments with {number_of_rooms} rooms found in building no.{building_number}.")
        else:
            print(f"Building no.{building_number} not found.")
            return []

# ***************************************************************************

class InputHandler:
    # Загальний метод для обробки вводу користувача з перевіркою типу даних і допустимого діапазону.
    @staticmethod
    def get_input(prompt: str, expected_type: type, valid_range=None):
        while True:
            user_input = input(prompt).strip()
            if not user_input:  # Перевіряємо, чи введення порожнє
                print("Input cannot be empty. Please try again.")
                continue
            try:
                # Перевірка на тип
                value = expected_type(user_input)

                # Перевірка на допустимий діапазон
                if valid_range and value not in valid_range:
                    # print(f"Value must be in range {valid_range}. You entered {value}.")
                    print(f"Value must be in range {list(valid_range)}. You entered {value}.")
                    continue

                return value

            except ValueError as e:
                print(f"Invalid input: Expected {expected_type.__name__}. Please try again.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

# ***************************************************************************


def main():
    manager = BuildingManager()

    while True:
        print("\nMenu:")
        print("1. Add building to the records")                # Додати будинок до обліку
        print("2. Add new resident to apartment")              # Додати нового мешканця будинку у квартиру
        print("3  Add family members resident to apartment")   # Додати членів родини мешканця будинку у квартиру
        print("4. Remove resident from apartment")             # Видалити мешканця будинку з квартири
        print("5. Show all main residents")                    # Відображення повного списку головних мешканців будинку
        print("6. Show all residents")                         # Відображення повного списку мешканців
        print("7. Show all apartments")                        # Відображення повного списку квартир
        print("8. Show apartment details by apartment number") # Відображення інформації про конкретну квартиру по номеру квартири
        print("9. Show apartments on a specific floor")        # Відображення інформації про квартири на конкретному поверсі
        print("10. Show apartments by how many rooms")         # Відображення інформації про квартири одного типу (за кількістю кімнат).
        print("11. Перевірка")
        print("12. Exit")


        choice = input("Enter your choice (1-11): ")

        # Додати будинок до обліку
        if choice == '1':
            try:
                building_number = InputHandler.get_input("Enter building number (1-14): ", int, range(1, 15))
                building = ApartmentBuilding(building_number)
                manager.add_building(building)
                print(f"Building no.{building_number} added.")
            except ValueError as e:
                print(f'Error: {e}')
            except Exception as e:
                print(f'Error: {e}')

        # Додати нового мешканця будинку у квартиру
        elif choice == '2':
            resident_id = InputHandler.get_input("Enter resident ID (1-200): ", int, range(1, 201))
            if manager.is_resident_already_assigned(resident_id):
                continue
            else:
                print(f"Resident with ID {resident_id}, document verification confirmed, continue...")

            name = InputHandler.get_input("Enter resident name: ", str)
            resident = Resident(resident_id, name)

            building_number = InputHandler.get_input("Enter building number(1 or 11) for the apartment: (1-14): ",
                                                     int, range(1, 15))

            # Крок 1: Питання про кількість кімнат
            number_of_rooms = InputHandler.get_input("How many rooms does the resident need? (1/2/3): ", int, range(1, 4))

            # Крок 2: Знайдемо всі вільні квартири з потрібною кількістю кімнат
            available_apartments = [
                apartment for apartment in manager.get_building_by_number(building_number).apartments
                if apartment.is_vacant and apartment.number_of_rooms == number_of_rooms
            ]

            # Крок 3: Якщо є вільні квартири, запропонуємо вибір
            if available_apartments:
                print(f"Available apartments with {number_of_rooms} rooms:")
                for idx, apartment in enumerate(available_apartments, start=1):
                    print(f"{idx}.apartment no.{apartment.apartment_number}: {apartment}")

            # Крок 4: Вибір квартири користувачем
            count_apartments = len(manager.get_building_by_number(building_number).apartments) + 1
            apartment_number = InputHandler.get_input("Select an apartment  -> Enter apartment number: ",
                                                      int, range(1, count_apartments))

            is_main_resident = InputHandler.get_input("Is the resident the primary responsible person for this apartment? (yes/no): ",
                                                      str, ['yes', 'no']).lower()

            manager.add_resident_to_apartment(building_number, apartment_number, resident, is_main_resident)

            print(f"Resident {name} added to apartment no.{apartment_number} in building no.{building_number}.")

        # Додати членів родини мешканця будинку у квартиру
        elif choice == '3':
            resident_id = InputHandler.get_input("Enter resident ID (1-200): ", int, range(1, 201))
            if manager.is_resident_already_assigned(resident_id):
                continue
            else:
                print(f"Resident with ID {resident_id}, document verification confirmed, continue...")

            name = InputHandler.get_input("Enter resident name: ", str)
            resident = Resident(resident_id, name)

            building_number = InputHandler.get_input("Enter building number(1 or 11) for the apartment: (1-14): ",
                                                     int, range(1, 15))

            count_apartments = len(manager.get_building_by_number(building_number).apartments) + 1
            apartment_number = InputHandler.get_input("Enter apartment number: ", int,
                                                      range(1, count_apartments))

            manager.add_resident_to_apartment(building_number, apartment_number, resident)

            print(f"Resident {name} added to apartment no.{apartment_number} in building no.{building_number}.")


        # Видалити мешканця будинку з квартири
        elif choice == '4':
            resident_id = InputHandler.get_input("Enter resident ID (1-200): ", int, range(1, 201))
            building_number = InputHandler.get_input("Enter building number(1 or 11) for the apartment: (1-14): ",
                                                     int, range(1, 15))

            count_apartments = len(manager.get_building_by_number(building_number).apartments) + 1
            apartment_number = InputHandler.get_input("Enter apartment number: ", int,
                                                      range(1, count_apartments))

            # Викликаємо метод з ID мешканця
            manager.remove_resident_from_apartment(building_number, apartment_number, resident_id)

        # Відображення повного списку головних мешканців будинку
        elif choice == '5':
            building_number = InputHandler.get_input("Enter building number(1 or 11) for the apartment: (1-14): ",
                                                     int, range(1, 15))
            print('---------------------')
            manager.show_all_main_residents(building_number)
            print('---------------------')

        # Відображення повного списку мешканців
        elif choice == '6':
            building_number = InputHandler.get_input("Enter building number(1 or 11) for the apartment: (1-14): ",
                                                     int, range(1, 15))
            print('---------------------')
            manager.show_all_residents(building_number)
            print('---------------------')

        # Відображення повного списку квартир
        elif choice == '7':
            building_number = InputHandler.get_input("Enter building number(1 or 11) for the apartment: (1-14): ",
                                                     int, range(1, 15))
            print('---------------------')
            manager.show_all_apartments(building_number)
            print('---------------------')

        # Відображення інформації про конкретну квартиру по номеру квартири
        elif choice == '8':
            building_number = InputHandler.get_input("Enter building number(1 or 11) for the apartment: (1-14): ",
                                                     int, range(1, 15))
            count_apartments = len(manager.get_building_by_number(building_number).apartments) + 1
            apartment_number = InputHandler.get_input("Enter apartment number: ", int,
                                                      range(1, count_apartments))
            print('---------------------')
            manager.show_apartment_info(building_number, apartment_number)
            print('---------------------')

        # Відображення інформації про квартири на конкретному поверсі
        elif choice == '9':
            building_number = InputHandler.get_input("Enter building number(1 or 11) for the apartment: (1-14): ",
                                                     int, range(1, 15))
            floor = InputHandler.get_input("Enter floor number: ",
                                           int, range(1, manager.get_building_by_number(building_number).quantity_floor+1))
            print('---------------------')
            manager.show_apartments_by_floor(building_number, floor)
            print('---------------------')

        # Відображення інформації про квартири одного типу (за кількістю кімнат).
        elif choice == '10':
            building_number = InputHandler.get_input("Enter building number(1 or 11) for the apartment: (1-14): ",
                                                     int, range(1, 15))
            apartment_type = InputHandler.get_input("How many rooms apartment type? (1/2/3): ", int,
                                                     range(1, 4))
            print('---------------------')
            manager.show_apartments_by_room_type(building_number, apartment_type)
            print('---------------------')


        elif choice == '11':
            print("перевірка resident ->>")
            # Перевірка мешканців у кожній квартирі
            for building in manager.buildings:
                print(f"Building {building.building_number}:")
                for apartment in building.apartments:
                    print(f"  Apartment {apartment.apartment_number}:")
                    for resident in apartment.residents:
                        print(f"    Resident ID: {resident.resident_id}, Name: {resident.name}")

            print("перевірка is_vacant ->>")
            # Перевірка які квартири вільні
            for building in manager.buildings:
                print(f"Building {building.building_number}:")
                for apartment in building.apartments:
                    if apartment.is_vacant:
                        print(f"  Apartment {apartment.apartment_number} is vacant")

        elif choice == '12':
            print("Exiting program.")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    main()



