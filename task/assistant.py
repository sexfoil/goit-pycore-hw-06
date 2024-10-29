from collections import UserDict


class RequiredFieldError(Exception):
    pass

class FieldFormatError(Exception):
    pass


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)        
        except (RequiredFieldError, FieldFormatError) as e:
            print(f"[ERROR] Validation failed: {e}")        
        except ValueError:            
            print("Phone number not found.")
        except KeyError:            
            print("Contact not found.")
        except Exception as e:
            print(f"[ERROR] Unknown exception: {e}")

    return inner


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if len(value.strip()) == 0:
            raise RequiredFieldError("Required not empty field.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        if len(value) != 10 or not all(c.isdigit() for c in value):
            raise FieldFormatError("Must be exactly 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    @error_handler
    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        if phone:
            self.phones.append(Phone(phone_number))
    
    @error_handler
    def remove_phone(self, phone_number: str):
        index = self.__get_phone_index(phone_number)
        if index >= 0:
            return self.phones.pop()

    @error_handler
    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        index = self.__get_phone_index(old_phone_number)
        if index >= 0:
            new_phone = Phone(new_phone_number)
            if new_phone:
                self.phones[index] = new_phone

    @error_handler    
    def find_phone(self, phone_number: str):    
        index = self.__get_phone_index(phone_number)
        if index >= 0:        
            return self.phones[index]

    def __get_phone_index(self, phone_number: str):
        for index in range(0, len(self.phones)):
            if self.phones[index].value == phone_number:
                return index
        raise ValueError


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    @error_handler
    def find(self, name):
        return self.data[name]
    
    @error_handler
    def delete(self, name):
        self.data.pop(name)




# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

for name, record in book.data.items():
    print(record)
