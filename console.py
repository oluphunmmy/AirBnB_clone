#!/usr/bin/python3

"""This Console module for entry into the command interpreter"""
import cmd
import sys
import shlex
import json
=======
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
>>>>>>> b4570ada73a30fbca91937ac1aa48ab239adfc8e
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
<<<<<<< HEAD
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """This module commands Interpreter class for Airbnb"""
    prompt = "(hbnb) "

    class_dict = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
            }

    def do_quit(self, arg):
        """This module quits command to exit the program"""
        return True

    def emptyline(self):
        """This module ensures empty line does nothing"""
        pass

    def do_EOF(self, arg):
        """This is the EOF to exit program"""
        return True

    def do_create(self, arg):
        """
       This module  creates a new instance of a class, saves it to Json file
        Usage: create <class name>
        """
        arg_list = shlex.split(arg)
        if len(arg_list) < 1:
            print("** class name missing **")
            return

        if (arg_list[0] in HBNBCommand.class_dict.keys()):
            obj = HBNBCommand.class_dict[arg_list[0]]()
            obj.save()
            print(obj.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """This module Prints the string representation of an instance based on class name
        and id"""
        storage.reload()
        stored_obj = storage.all()
        arg_list = shlex.split(arg)

        if len(arg_list) < 1:
            print("** class name missing **")
            return

        if arg_list[0] not in HBNBCommand.class_dict.keys():
            print("** class doesn't exist **")
            return

        if len(arg_list) == 1:
            print("** instance id missing **")
            return

        key = arg_list[0] + "." + arg_list[1]
        try:
            stored_obj[key]
        except KeyError:
            print("** no instance found **")
            return
        print(str(stored_obj[key]))

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""

        arg_list = shlex.split(arg)
        stored_obj = storage.all()

        if len(arg_list) < 1:
            print("** class name missing **")
            return

        if arg_list[0] not in HBNBCommand.class_dict.keys():
            print("** class doesn't exist **")
            return

        if len(arg_list) == 1:
            print("** instance id missing **")
            return

        key = arg_list[0] + "." + arg_list[1]
        try:
            stored_obj[key]
        except KeyError:
            print("** no instance found **")
            return
        del stored_obj[key]
        storage.save()

    def do_all(self, arg):
        """
        This module Prints all string representation of all instances
        based or not on the class name.
        Eg: all BaseModel or all
        Usage:(1) all
              (2) all <class name>
        """
        storage.reload()
        obj_list = []
        objects = storage.all()
        if arg == "":
            for key, value in objects.items():
                obj_list.append(str(value))
            print(json.dumps(obj_list))
            return
        arg_list = shlex.split(arg)
        if (arg_list[0] not in HBNBCommand.class_dict.keys()):
            print("** class doesn't exist **")
            return
        for key, value in objects.items():
            if arg_list[0] in key:
                obj_list.append(str(value))
        print(json.dumps(obj_list))

    def do_count(self, arg):
        """ count the number of objects of a particulasr class instance"""
        storage.reload()
        obj = storage.all()
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.class_dict.keys():
            print("** class doesn't exist **")
            return

        count = 0
        for key in obj:
            if args[0] in key:
=======
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
>>>>>>> b4570ada73a30fbca91937ac1aa48ab239adfc8e
                count += 1
        print(count)

    def do_update(self, arg):
<<<<<<< HEAD
        """
        This Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com
        update <class name> <id> <attribute name> "<attribute value>"
        """
        arg_list = shlex.split(arg)
        arg_len = len(arg_list)
        if arg_len < 1:
            print("** class name missing **")
            return
        if arg_list[0] not in HBNBCommand.class_dict.keys():
            print("** class doesn't exist **")
            return
        if arg_len == 1:
            print("** instance id missing **")
            return
        storage.reload()
        objects = storage.all()
        key = arg_list[0] + "." + arg_list[1]
        try:
            objects[key]
        except KeyError:
            print("** no instance found **")
            return
        if arg_len == 2:
            print("** attribute name missing **")
            return
        try:
            eval(arg_list[2])
        except NameError:
            if arg_len == 3:
                print("** value missing **")
                return
        obj_dict = objects[key].__dict__
        try:
            eval(arg_list[2])
        except NameError:
            if arg_list[2] in obj_dict.keys():
                obj_dict[arg_list[2]] = type(
                        obj_dict[arg_list[2]])(arg_list[3])
            else:
                try:
                    obj_dict[arg_list[2]] = int(arg_list[3])
                except ValueError:
                    obj_dict[arg_list[2]] = arg_list[3]
            storage.save()
            return
        if type(eval(arg_list[2])) == dict:
            dict_kwarg = eval(arg_list[2])
            for key in dict_kwarg:
                if key in obj_dict.keys():
                    obj_dict[key] = type(obj_dict[key])(dict_kwarg[key])
                else:
                    try:
                        obj_dict[key] = int(dict_kwarg[key])
                    except ValueError:
                        obj_dict[key] = dict_kwarg[key]
            storage.save()
            return

    def default(self, args):
        """defines action on objects using -
        <class name>.all() : retrieves all object of specified class name
        """
        cmd_dict = {
                "all": self.do_all,
                "count": self.do_count,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "update": self.do_update
                }
        arg = args.strip()
        val = arg.split(".")
        if len(val) != 2:
            cmd.Cmd.default(self, args)
            return
        class_name = val[0]
        method_call = val[1].split("(")[0]
        var = ""
        try:
            var = val[1].split("(")[1][-2]
        except IndexError:
            pass
        if var == "}":
            try:
                a = val[1].split("(")[1][:-1].split("{")
                _id = a[0][1:-3]
                dict_obj = "{" + a[1]
                copy = _id + " " + "'" + dict_obj.replace("'", '"', -1) + "'"
                if method_call == "update":
                    cmd_dict[method_call](class_name + " " + copy)
                return
            except IndexError:
                pass
        elif method_call == "update" and len(val[1].split("(")[1][:-1]) > 1:
            params = val[1].split("(")[1][:-1].split(",")
            line = "".join(params)[:]
            cmd_dict[method_call](class_name + " " + line)
        elif len(val[1].split("(")[1][:-1]) > 1:
            if method_call in cmd_dict.keys():
                p = val[1].split("(")[1][:-1]
                cmd_dict[method_call](class_name + " " + p)
        else:
            if method_call in cmd_dict.keys():
                cmd_dict[method_call](class_name)


if __name__ == '__main__':
=======
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
>>>>>>> b4570ada73a30fbca91937ac1aa48ab239adfc8e
    HBNBCommand().cmdloop()
