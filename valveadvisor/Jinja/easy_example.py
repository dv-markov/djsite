from jinja2 import Template

name = "Fedor"

tm = Template("Привет, {{ name }}!")
msg = tm.render(name=name)

print(msg)


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


per = Person("Petr", 36)

tm = Template("Мне {{ p.age }} лет и меня зовут {{ p.name }} 😁")
msg = tm.render(p=per)

print(msg)


pp = {'name': 'Ivan', 'age': 34}
tm = Template("А меня зовут {{ p.name }}, мне {{ p.age }} 😎")
msg = tm.render(p=pp)
print(msg)
