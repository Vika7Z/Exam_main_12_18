import unittest
from unittest.mock import mock_open, patch
# import sys
# import os

# Якщо у вашому проєкті є вкладені папки,
# то в кожній папці, з якої ви хочете імпортувати, і в кореневій папці проєкту
# потрібен файл __init__.py який вказує, що папка є Python-пакетом
#
# .. означає перехід на один рівень вище у файловій структурі.

from .main_12_18_exam import Resident, Apartment, ApartmentBuilding, FileManager, BuildingManager, InputHandler


# *****************************************************************************************

class TestResident(unittest.TestCase):
    @classmethod
    def setUpClass(cls):     # запускається один раз перед всіма тестами (фікстура)
        print('\n-->> Is setUpClass')
        cls.resident = Resident(resident_id=10, name='Sofiya')

    @classmethod
    def tearDownClass(cls):  # запускається один раз після всіх тестів (звільняємо пам'ять) (фікстура)
        print('-->> Is tearDownClass')


    # коли -> очікуємо вірні значення
    def test_resident_creation_true(self):
        print('\nIs test_resident_creation_true')
        self.assertEqual( self.resident.resident_id, 10)
        self.assertEqual(self.resident.name, 'Sofiya')

    def test_resident_str(self):
        print('\nIs test_resident_str')
        self.assertEqual(str(self.resident), 'Resident ID: 10, Name: Sofiya')

    # коли -> очікуємо не вірні значення
    def test_resident_creation_false(self):
        print('\nIs test_resident_creation_false')
        self.assertNotEqual(self.resident.resident_id, -2)
        self.assertNotEqual(self.resident.resident_id, 201)
        self.assertNotEqual(self.resident.resident_id, '')
        self.assertNotEqual(self.resident.resident_id, 'asd')

# **********************************************************************************************

class TestApartment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # запускається один раз перед всіма тестами (фікстура)
        print('\n-->> Is setUpClass')
        cls.resident = Resident(resident_id=10, name='Sofiya')
        cls.apartment = Apartment(apartment_number=101, floor=1, number_of_rooms=3, is_vacant=True)

    @classmethod
    def tearDownClass(cls):  # запускається один раз після всіх тестів (звільняємо пам'ять) (фікстура)
        print('-->> Is tearDownClass')

    # коли -> очікуємо вірні значення
    def test_apartment_creation_true(self):
        print('\nIs test_apartment_creation_true')
        self.assertEqual(self.apartment.apartment_number, 101)
        self.assertEqual(self.apartment.floor, 1)
        self.assertEqual(self.apartment.number_of_rooms, 3)
        self.assertTrue(self.apartment.is_vacant)

    def test_add_resident_in_apartment(self):
        print('\nIs test_add_resident_in_apartment')
        self.apartment.residents.append(self.resident)
        self.assertIn(self.resident, self.apartment.residents)

    # коли -> очікуємо не вірні значення
    def test_apartment_creation_false(self):
        print('\nIs test_apartment_creation_false')
        self.assertNotEqual(self.apartment.apartment_number, 0)
        self.assertNotEqual(self.apartment.apartment_number, -2)
        self.assertNotEqual(self.apartment.apartment_number, '')
        self.assertNotEqual(self.apartment.apartment_number, 'asd')
        self.assertNotEqual(self.apartment.floor, -3)
        self.assertNotEqual(self.apartment.floor, '')
        self.assertNotEqual(self.apartment.floor, 'asd')
        self.assertNotEqual(self.apartment.number_of_rooms, 3000)
        self.assertNotEqual(self.apartment.number_of_rooms, '')
        self.assertNotEqual(self.apartment.number_of_rooms, 'asd')
        self.assertNotEqual(self.apartment.is_vacant, 12)
        self.assertNotEqual(self.apartment.is_vacant, '')
        self.assertNotEqual(self.apartment.is_vacant, 'asd')
        self.assertNotEqual(self.apartment.is_vacant, False)

# **********************************************************************************************

class TestApartmentBuilding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # запускається один раз перед всіма тестами (фікстура)
        print('\n-->> Is setUpClass')
        cls.building2 = ApartmentBuilding(building_number=2, quantity_floor=3, rooms_per_floor=[2, 3, 4])
        cls.building3 = ApartmentBuilding(building_number=3, quantity_floor=2, rooms_per_floor=[2, 2])

    @classmethod
    def tearDownClass(cls):  # запускається один раз після всіх тестів (звільняємо пам'ять) (фікстура)
        print('-->> Is tearDownClass')


    # коли -> очікуємо вірні значення
    def test_building_creation_true(self):
        print('\nIs test_building_creation_true')
        self.assertEqual(self.building2.building_number, 2)
        self.assertEqual(len(self.building2.apartments), 9)

    def test_generate_apartments_true(self):
        print('\nIs test_generate_apartments_true')
        self.assertEqual(len(self.building3.apartments), 4)

    # коли -> очікуємо не вірні значення
    def test_building_creation_false(self):
        print('\nIs test_building_creation_false')
        self.assertNotEqual(self.building2.building_number, -3)
        self.assertNotEqual(self.building2.building_number, '')
        self.assertNotEqual(self.building2.building_number, 'asd')

    def test_generate_apartments_false(self):
        print('\nIs test_generate_apartments_false')
        self.assertNotEqual(len(self.building3.apartments), False)
        self.assertNotEqual(len(self.building2.apartments), 0)
        self.assertNotEqual(len(self.building2.apartments), 200)

# **********************************************************************************************

class TestBuildingManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # запускається один раз перед всіма тестами (фікстура)
        print('\n-->> Is setUpClass')
        cls.manager = BuildingManager()
        cls.resident = Resident(resident_id=10, name='Sofiya')
        cls.building1 = ApartmentBuilding(building_number=11, quantity_floor=2, rooms_per_floor=[1, 1, 2, 3])
        cls.building3 = ApartmentBuilding(building_number=10, quantity_floor=2, rooms_per_floor=[1, 1, 2, 3])
        cls.building4 = ApartmentBuilding(building_number=12, quantity_floor=2, rooms_per_floor=[1, 1, 2, 3])
        cls.building5 = ApartmentBuilding(building_number=13, quantity_floor=2, rooms_per_floor=[1, 1, 2, 3])

    @classmethod
    def tearDownClass(cls):  # запускається один раз після всіх тестів (звільняємо пам'ять) (фікстура)
        print('-->> Is tearDownClass')

    # коли -> очікуємо вірні значення
    def test_add_building_true(self):
        print('\nIs test_add_building_true')
        self.manager.add_building(self.building4)
        self.assertIn(self.building4, self.manager.buildings)

    def test_is_resident_already_assigned(self):
        print('\nIs test_is_resident_already_assigned')
        self.assertEqual(self.manager.is_resident_already_assigned(10), True)

    def test_find_resident_by_id(self):
        print('\nIs test_find_resident_by_id')
        self.assertEqual(self.manager.find_resident_by_id(self.resident.resident_id).resident_id, 10)

    # коли -> очікуємо не вірні значення
    def test_add_building_false_re_added(self):
        print('\nIs test_add_building_false_re_added')
        # Перевірка, що при спробі додати будинок з таким самим номером буде виключення
        with self.assertRaises(ValueError) as context:
            self.manager.add_building(self.building1)  # Спроба додати будинок з номером 11 повторно

        # Перевірка, що в контексті з'явився правильний текст помилки
        self.assertEqual(str(context.exception),
                         f"ValueError: Building with number {self.building1.building_number} already exists.")

    def test_add_building_re_added(self):
        print('\nIs test_add_building_re_added')
        # Додаємо перший будинок
        self.manager.add_building(self.building3)
        self.assertIn(self.building3, self.manager.buildings)

        # Додаємо другий будинок з іншим номером, перевіряємо що він додався
        self.manager.add_building(self.building5)
        self.assertIn(self.building5, self.manager.buildings)

        # Перевірка, що при спробі додати будинок з таким самим номером буде виключення
        with self.assertRaises(ValueError) as context:
            self.manager.add_building(self.building5)  # Спроба додати будинок з номером 11 повторно

        print(f'== ValueError: {context.exception=}')
        # Перевірка, що в контексті з'явився правильний текст помилки
        self.assertEqual(str(context.exception), f"ValueError: Building with number {self.building5.building_number} already exists.")

# **********************************************************************************************

class TestInputHandler(unittest.TestCase):
    # коли -> очікуємо вірні значення
    def test_valid_input(self):
        print('\nIs test_valid_input')
        with unittest.mock.patch('builtins.input', return_value="5"):
            result = InputHandler.get_input("Enter a number: ", int, range(1, 10))
            self.assertEqual(result, 5)

    # коли -> очікуємо не вірні значення
    def test_invalid_input_str(self):
        print('\nIs test_invalid_input_str')
        with unittest.mock.patch('builtins.input', side_effect=["abc", "5"]):
            result = InputHandler.get_input("Enter a number: ", int, range(1, 10))
            self.assertEqual(result, 5)

    def test_invalid_input_empty(self):
        print('\nIs test_invalid_input_empty')
        with unittest.mock.patch('builtins.input', side_effect=["", "5"]):
            result = InputHandler.get_input("Enter a number: ", int, range(1, 10))
            self.assertEqual(result, 5)

# **********************************************************************************************


if __name__ == '__main__':
    unittest.main()            # <<-- означає що цей файл є головним для запуску тестів:


