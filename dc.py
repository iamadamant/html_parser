import re


class Tag:
    SINGLE = ['input', 'br', 'hr', 'link', 'meta', 'area', 'base', 'col', 'command', 'embed', 'img', 'keygen', 'param',
              'track', 'wbr']

    @staticmethod
    def is_html(html):
        res = html.strip()
        template = '<[a-z]+[0-9]*.*>'
        if re.search(template, res) is not None:
            return True
        else:
            return False

    @staticmethod
    def is_single(tag) :
        for single in Tag.SINGLE:
            res = re.search('<' + single, tag)
            try :
                if res.group(0) is not None:
                    return True
            except AttributeError as e:
                pass
        return False

    @staticmethod
    def get_content(el):
        answ = None
        template = '' if Tag.is_single(el) else r'(?<=>).*(?=<)'
        if template == "":
            return None
        sh = re.compile(
            template
        )
        try :
            answ = sh.findall(el)[0]
        except IndexError:
            return None
        return answ

    @staticmethod
    def get_property(el):
        answ = {}
        text = ''
        template = r'<[a-z]+[0-9]* *(.*)>'
        sh = re.compile(
            template
        )
        try :
            res = sh.findall(el)[0]
            arr = re.split(r'''["']+ *''', res)
            arr = [i for i in arr if i.strip() != '']
            for i in range(0, len(arr), 2) :
                answ[arr[i].replace('=', '').strip()] = arr[i + 1]
        except IndexError:
            return None
        return answ

    @staticmethod
    def get_tag_name(el):
        answ = None
        template = r'<([a-z]+[0-9]*).*>' if Tag.is_single(el) else r'<([a-z]+[0-9]*).*>.*</[a-z]+[0-9]*>'
        sh = re.compile(
            template
        )
        try :
            answ = sh.findall(el)[0]
        except IndexError:
            return None
        return answ

    @staticmethod
    def all_tags(source) :
        res = source.split('><')
        for i in range(len(res)):
            if i % 2 == 0 :
                res[i] = res[i] + '>'
            else:
                res[i] = '<' + res[i]
        return res


class Element :

    def __init__(self, children: object, name: object, props: object, text: str = None):
        self.children = children
        self.name = name
        self.__properties = Tag.get_property(props)
        self.text = text

    def get(self, property_name: str):
        if property_name == "children":
            return self.children
        return self.__properties.get(property_name.lower(), None)

    def __str__(self):
        return self.name


class Text:

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return str(self.content)


class Document:

    def __init__(self, roof='', id_tree: dict = {}, name_tree: dict = {}, meta_set=[], head=None, body=None, forms=[], scripts=[], html=None):
        self.roof = roof
        self.formSet = forms
        self.id_tree = id_tree
        self.name_tree = name_tree
        self.scriptSet = scripts
        self.body = body
        self.head = head
        self.html = html
        self.metaSet = meta_set


    def getElementById(self, el_id):
        return self.id_tree.get(el_id, None)

    def getElementByNme(self, name):
        return self.name_tree.get(name, None)
