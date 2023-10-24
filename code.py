import sys
import re
from copy import copy

class Inventory():
    def __init__(self):
        self.nums = []
        self.is_active = True
        self.current_working_num = []

    def param_parser(func):
        def wrapper(self, *args, **kwargs):
            self.current_working_num = copy(self.nums)
            modifiers = kwargs.get("modifiers", [])
            repeat = 1

            if any(item in modifiers for item in ['@once' , '@twice' , '@often']):
              repeat = 0

            commit = True
            sorted = False
            dryrun_flag = False

            for mod in modifiers:

                if mod == "@once":
                    repeat += 1

                elif mod == "@twice":
                    repeat += 2

                elif mod == "@often":
                    repeat += 10

                elif mod == "@dryrun":
                    commit = False
                    dryrun_flag = True

                elif mod == "@sorted":
                    sorted = True
                    commit = False
                    self.current_working_num.sort()

            for _ in range(repeat):
                result = func(self, *args, **kwargs)

            if commit:
                self.nums = copy(self.current_working_num)
                self.current_working_num = []
            elif dryrun_flag:
                print(self.current_working_num)

        return wrapper

    @param_parser
    def insert(self,*args, **kwargs):
        for i in args:
            self.current_working_num.append(int(i))
    @param_parser
    def pop(self, *args, **kwargs):
        if int(args[0]) < len(self.current_working_num):
            self.current_working_num = self.current_working_num[:-int(args[0])] if args else self.current_working_num[:-1]
        else:
            print("Invalid input")
    @param_parser
    def show(self, *args, **kwargs):
        print(self.current_working_num)

    @param_parser
    def exit(self, *args, **kwargs):
        self.is_active = False

    @param_parser
    def index(self, *args, **kwargs):
        if int(args[0]) in self.current_working_num :
            output = self.current_working_num.index(int(args[0]))
            print(output)
        else:
            print("Invalid element")

    @param_parser
    def get(self, *args, **kwargs):
        if int(args[0]) < len(self.current_working_num):
            print(self.current_working_num[int(args[0])])
        else:
            print('Invalid Index')

    @param_parser
    def remove(self, *args, **kwargs):
        if int(args[0]) < len(self.current_working_num):
            _ = self.current_working_num.pop(int(args[0]))
        else: 
            print('Invalid Index')
            
    @param_parser
    def insertFront(self, *args, **kwargs):
        self.current_working_num = [int(i) for i in args] + self.current_working_num

    @param_parser
    def popFront(self, num=1, *args, **kwargs):
        if int(num) <= len(self.current_working_num):
            self.current_working_num = self.current_working_num[int(num):]
        else:
            print('Invalid input')
    @param_parser
    def sort(self, *args, **kwargs):
        self.current_working_num = sorted(self.current_working_num)

    @param_parser
    def isSorted(self, *args, **kwargs):
        print('true') if self.current_working_num == sorted(self.current_working_num) else print('false')

    @param_parser
    def push(self, *args, **kwargs):
        for i in args:
          self.current_working_num.append(int(i))

    @param_parser
    def EOF(self, *args, **kwargs):
        self.is_active = False
        
        

inv = Inventory()

operations = {"insert":inv.insert, "pop":inv.pop, "show":inv.show,
              "exit":inv.exit, "index":inv.index, "get":inv.get, "remove":inv.remove,
              "insertFront":inv.insertFront, "popFront":inv.popFront,
              "sort":inv.sort, "isSorted":inv.isSorted, "push":inv.push, 'EOF':inv.EOF}

def excuter(operation, arguments, modifiers):
    operations[operation](*arguments, modifiers = modifiers)



while (inv.is_active):
  request = input('> ')

  operation = re.findall('^[a-zA-Z]*', request)[0]
  arguments = re.findall('\d+', request)
  modifiers = re.findall('@[a-z]+', request)

  if ((operation == 'exit') | (operation == 'EOF')):
    inv.exit()

  else:
    if operation not in list(operations.keys()):
      print("Operation unknown")

    else:
      excuter(operation, arguments, modifiers)
