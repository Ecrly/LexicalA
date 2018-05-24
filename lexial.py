from setting import *
import re

class Parser:

    def __init__(self):
        self._row = 1
        self._col = 1
        self._buffer = ""
        self._state = 'A'
        self._wrong = 0
        self._input = []
        self._input_map = []


    def tokenize(self, ch):
        while(True):
            # ********************       起始状态        ******************* #
            if(self._state == 'A'):

                if re.match(r'( |\n|\t|\r)', ch):
                    return
                elif re.match(r'[A-Za-z]|_', ch):
                    self._buffer += ch
                    self._state = 'B'
                    return
                elif re.match(r'[0-9]', ch):
                    self._buffer += ch
                    self._state = 'C'
                    return
                elif ch == "'":
                    self._state = 'E'
                    return
                elif ch == '"':
                    self._state = 'F'
                    return
                elif ch == '#':
                    self._state = 'G'
                    return
                elif ch in DELIMITER or ch in PUNCTUNTION:
                    print(self._row ,'(', ch, ' , ', '分隔符）')
                    self._input.append(ch)
                    self._input_map.append(self._row)
                    self._state = 'A'
                    return
                elif ch in OPERATOR:
                    self._buffer += ch
                    self._state = 'A+'
                    return
                else:
                    self._wrong = 1
                    self._buffer += ch
                    return

            if(self._state == 'A+'):

                if ch == '+':
                    self._buffer += '+'
                    print(self._row ,'(', self._buffer, ' , ', '双目操作符）')
                    self._input_map.append(self._row)
                    self._input.append(self._buffer)
                    self._buffer = ""
                    self._state = 'A'
                    return
                elif ch == '-':
                    self._buffer += '-'
                    print(self._row ,'(', self._buffer, ' , ', '双目操作符）')
                    self._input_map.append(self._row)
                    self._input.append(self._buffer)
                    self._buffer = ""
                    self._state = 'A'
                    return
                else:
                    print(self._row ,'(', self._buffer, ' , ', '操作符）')
                    self._input_map.append(self._row)
                    self._input.append(self._buffer)
                    self._buffer = ""
                    self._state = 'A'


            # ********************     状态B(关键词)     ******************* #

            if(self._state == 'B'):

                if re.match(r'[A-Za-z0-9]|_', ch):
                    self._buffer += ch
                    self._state = 'B'
                    return
                else:
                    if self._buffer in KEYWORDS_C:
                        print(self._row ,'(', self._buffer, ' , ', '关键词）')
                        self._input_map.append(self._row)
                        self._input.append(KEYWORDS_C_MAP[self._buffer])
                    else:
                        print(self._row ,'(', self._buffer, ' , ', '标识符）')
                        self._input_map.append(self._row)
                        self._input.append('ID')
                    self._buffer = ""
                    self._state = 'A'

            # ********************     状态C(无符号整数)     ******************* #

            if(self._state == 'C'):

                if re.match(r'[0-9]', ch):
                    self._buffer += ch
                    self._state = 'C'
                    return
                elif ch == '.':
                    self._buffer += ch
                    self._state = 'D'
                    return
                elif re.match(r'[A-Za-z]', ch):
                    self._buffer += ch
                    self._wrong = 2
                    return
                else:
                    print(self._row ,'(', self._buffer, ' , ', '无符号整型）')
                    self._input_map.append(self._row)
                    self._input.append('DIGIT')
                    self._buffer = ""
                    self._state = 'A'

            # ********************     状态D(浮点型)         ******************* #

            if(self._state == 'D'):

                if re.match(r'[0-9]', ch):
                    self._buffer += ch
                    self._state = 'D'
                    return
                else:
                    print(self._row ,'(', self._buffer, ' , ', '浮点型）')
                    self._input_map.append(self._row)
                    self._input.append('DIGIT')
                    self._buffer = ""
                    self._state = 'A'

            # ********************     状态E(字符类型)         ******************* #

            if(self._state == 'E'):

                if ch == "'":
                    print(self._row ,'(', self._buffer, ' , ', '字符型）')
                    self._input_map.append(self._row)
                    self._input.append('CHARR')
                    self._buffer = ""
                    self._state = 'A'
                    return
                else:
                    self._buffer += ch
                    self._state = 'E'
                    return

            # ********************     状态F(字符串类型)         ******************* #

            if(self._state == 'F'):

                if ch == '"':
                    print(self._row ,'(', self._buffer, ' , ', '字符串）')
                    self._input_map.append(self._row)
                    self._input.append("String")
                    self._buffer = ""
                    self._state = 'A'
                    return
                else:
                    self._buffer += ch
                    self._state = 'F'
                    return

            # ********************     状态G(单行注释)         ******************* #

            if(self._state == 'G'):

                if ch == '\n':
                    print(self._row , '(', self._buffer, ' , ', '单行注释）')
                    self._input_map.append(self._row)
                    self._buffer = ""
                    self._state = 'A'
                    return
                else:
                    self._buffer += ch
                    self._state = 'G'
                    return


    def wrong(self, type):
        if type == 1:
            print('Error:',self._row , '行' ,self._col , '列' ,self._buffer, "不可识别字符")
        if type == 2:
            print('Error:',self._row , '行' ,self._col , '列' ,self._buffer, "数字中含有字母")


    def parser(self, code):

        self._state = 'A'
        for i in range(0, len(code)):
            self._col += 1
            self.tokenize(code[i])
            if self._wrong != 0:
                self.wrong(self._wrong)
                return 'wrong'
            if code[i] == '\n':
                self._row += 1
                self._col = 0
        return self._input, self._input_map