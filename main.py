from json import loads, dumps
from lxml import etree

class DigitalBook:
    def __init__(self, title=None, author=None):
        self._title = title
        self._author = author

    def _build_struct(self, data):
        if "title" in data:
            self._title = data["title"]
        else:
            return self._throw_key_error("title")

        if "author" in data:
            self._author = data["author"]
        else:
            return self._throw_key_error("author")

    def load_json(self, string):
        data = loads(string)
        self._build_struct(data)

    def load_xml(self, string):
        root = etree.fromstring(string)
        data = {}

        for elem in root.iter():
            data[elem.tag] = elem.text

        self._build_struct(data)

    def dump_json(self):
        data = {
            "title": self._title,
            "author": self._author
        }

        return dumps(data)

    def dump_xml(self):
        root = etree.Element("root")

        etree.SubElement(root, "title").text = self._title
        etree.SubElement(root, "author").text = self._author

        string = etree.tostring(root, pretty_print=True).decode()

        return string

    def read_from_file(self, filename):
        file_extension = filename.split(".")[-1].lower()
        file = open(filename, "r")

        if file_extension != "xml" and file_extension != "json":
            return self._throw_extension_error()

        string = file.read()

        if file_extension == "xml":
            self.load_xml(string)

        if file_extension == "json":
            self.load_json(string)

    def write_in_file(self, filename):
        file_extension = filename.split(".")[-1].lower()
        file = open(filename, "w")

        if file_extension != "xml" and file_extension != "json":
            return self._throw_extension_error()

        if file_extension == "xml":
            file.write(self.dump_xml())

        if file_extension == "json":
            file.write(self.dump_json())

    def _throw_extension_error(self):
        error = "File extension must be xml or json"
        raise RuntimeError(error)

    def _throw_key_error(self, key):
        error = f"Input data is incorrect. Missing required key '{key}'"
        raise KeyError(error)

    def data(self):
        return {
            "title": self._title,
            "author": self._author
        }

    def _break_book(self):
        while True:
            inp = input()

            if inp == "break":
                print("Closed")
                break

class ElectronicBook(DigitalBook):
    def open(self):
        print(f"The book '{self._title}' by {self._author} is opened"
              f"\n"
              f"Please type 'break' to close")

        self._break_book()

class AudioBook(DigitalBook):
    def play(self):
        print(f"The book '{self._title}' by {self._author} is playing"
              f"\n"
              f"Please type 'break' to stop")

        self._break_book()