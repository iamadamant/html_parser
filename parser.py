from dc import *
from typing import List
from tokens.html_tokens import *
from minimalizer.html_minimalizer import squeeze
from constants.logic_constant import *


class Parser:
    def __init__(self, text: str):
        self.__stack: List[Token] = []
        self.__text = squeeze(text)
        self.__pointer = 0
        self.__id_tree = {}
        self.__name_tree = {}
        self.__forms = []
        self.__body = None
        self.__head = None
        self.__html = None
        self.__title = None
        self.__metas = []
        self.__scripts = []

    def shift(self, shft: int):
        self.__pointer = shft

    def get_next_tag(self):
        match = re.search(r'<.*?>', self.__text[self.__pointer :])
        tg = re.search(r'[^ ]*', match.group(0)).group()
        return tg, (match.start() + self.__pointer, match.end() + self.__pointer)

    def get_all_tags(self) -> None:
        while True:
            try :
                tg, pos = self.get_next_tag()
                name = re.search('[a-z]+[0-9]*', tg).group()
                if tg.startswith('</'):
                    self.__stack.append(Token(name, pos, 'close'))
                else:
                    self.__stack.append(Token(name, pos, 'open'))
                self.shift(pos[1])
            except AttributeError:
                break

    def form_stack(self) :
        self.get_all_tags()
        return self.__stack

    def get_child(self, child_tags: List):
        answ = []
        while len(child_tags) != 0:
            element = self.create_element(child_tags)
            answ.append(element)
        return answ

    def register_element(self, element: Element):
        name = element.get('name')
        id = element.get('id')
        tag_name = element.name
        if name is not None:
            self.__name_tree[name] = element
        if id is not None:
            self.__id_tree[id] = element

        if tag_name == 'body':
            self.__body = element
        elif tag_name == 'form':
            self.__forms.append(element)
        elif tag_name == 'head':
            self.__head = element
        elif tag_name == 'html':
            self.__html = element
        elif tag_name == 'title':
            self.__title = element
        elif tag_name == 'meta':
            self.__metas.append(element)
        elif tag_name == 'script':
            self.__scripts.append(element)


    def create_element(self, tags):
        start = tags.pop(0)
        property = self.__text[start.start():start.end()]
        name = start.name
        if name in Tag.SINGLE:
            return Element([], name, property)
        balance = 1
        end = None
        child_elements = []
        while true:
            next = tags.pop(0)
            if next.type == TokenType.Opening:
                balance += 1
                if next.name in Tag.SINGLE:
                    balance -= 1
                    child_elements.append(next)
            else:
                balance -= 1

            if balance == 0:
                end = next
                break

            child_elements.append(next)
        if start.name != end.name:
            raise Exception('Количество открывающих тегов не совпадает с количеством закрывающих!')


        children = self.get_child(child_elements)
        html_element = Element(children, name, property)
        self.register_element(html_element)
        return html_element

    def get_dom(self):
        stack = self.form_stack()
        self.print_stack()
        try:
            roof = self.create_element(stack)
        except IndexError:
            raise Exception('Количество открывающих тегов не совпадает с количеством закрывающих!')
        return Document(roof, self.__id_tree, self.__name_tree, self.__metas, self.__head, self.__body, self.__forms, self.__scripts, self.__html)

    def print_stack(self):
        for tag in self.__stack:
            print(tag.name)


html: str = '''
<html id='p'>
<head id="h">
     <title class='new'>ngnghrh</title>
</head>



<body border='3'>
<script type="text/javascript">
	kljnrl
</script >
<a class="link" href="#"><span class="dark"></span><br><br><span class="light"></span></a>
</body>
</html>
'''

p = Parser(html)
document = p.get_dom()
p.print_stack()
roof = document.roof
print('Questions ************')
print(roof.children[1].children[1].children[0].get('class'))
print(document.getElementById('p'))
print('-' * 40)
print(document.id_tree['h'])
print(document.formSet)
