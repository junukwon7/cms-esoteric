# 엄준식(umjunsik-lang)의 CMS용 애드온입니다.
[CMS](http://cms-dev.github.io/) 1.5.0dev0를 기반으로 작성되었으며, 1.4.rc1에서의 작동을 보장합니다. </br>

![image](https://user-images.githubusercontent.com/48399106/154005905-b00f0298-b5a2-483f-b588-390c6ecd55fd.png)

# 1. CMS 설치 스크립트 수정
CMS 설치 스크립트인 `cms/setup.py`를 본 repo의 것으로 대체하거나, [184번 줄](https://github.com/cms-dev/cms/blob/0401c5336b34b1731736045da4877fef11889274/setup.py#L184)에 다음과 같이 umlang을 추가합니다.

```python3
"cms.grading.languages": [
            "Umlang2=cms.grading.languages.umlang2:Umlang2",
            "C++11 / g++=cms.grading.languages.cpp11_gpp:Cpp11Gpp",
            "C++14 / g++=cms.grading.languages.cpp14_gpp:Cpp14Gpp",
            "C++17 / g++=cms.grading.languages.cpp17_gpp:Cpp17Gpp",
            "C11 / gcc=cms.grading.languages.c11_gcc:C11Gcc",
            "C# / Mono=cms.grading.languages.csharp_mono:CSharpMono",
            "Haskell / ghc=cms.grading.languages.haskell_ghc:HaskellGhc",
            "Java / JDK=cms.grading.languages.java_jdk:JavaJDK",
            "Pascal / fpc=cms.grading.languages.pascal_fpc:PascalFpc",
            "PHP=cms.grading.languages.php:Php",
            "Python 2 / CPython=cms.grading.languages.python2_cpython:Python2CPython",
            "Python 3 / CPython=cms.grading.languages.python3_cpython:Python3CPython",
            "Rust=cms.grading.languages.rust:Rust",
        ],
```
이후 수정사항을 반영하기 위해서 `python3 setup.py install` 작업이 필요합니다.

# 2. umjunsik-lang-cc 컴파일러 사용 (권장)


## 2.1. 엄준식 컴파일러 설치
[엄준식 컴파일러](https://github.com/rycont/umjunsik-lang/tree/master/umjunsik-lang-cc)를 cmake를 사용해 `/usr/bin/umcc`에 설치합니다.

## 2.2. 엄준식 grader 설정
아래 내용을 `cms/cms/grading/languages/umlang2.py`에 저장합니다.
```python3
#!/usr/bin/env python3

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2022 Junu Kwon <junukwon7@gmail.com>

"""Umjunsik-lang v2 programming language definition."""

from cms.grading import CompiledLanguage


__all__ = ["Umlang2"]


class Umlang2(CompiledLanguage):
    """This defines the Umjunsik programming language, compiled with umcc (the
    version available on the system) using the Umjunsik-lang v2 standard.

    """

    @property
    def name(self):
        """See Language.name."""
        return "Umjunsik-lang 2"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".umm"]


    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""


        command = ["/usr/bin/umcc"]
        command += ["-o", executable_filename]
        command += source_filenames
        return [command]
        
        """강제로 EOL을 생성하려면 아래 부분을 주석 해제하세요"""
        # encode = ["/usr/bin/umcode.py"]
        # encode += ["--src", source_filenames[0]]
        # return [encode, command]
```
이후 수정사항을 반영하기 위해서 `python3 setup.py install` 작업이 필요합니다.

## 2.3. 강제 EOL 생성
제출된 소스코드의 마지막 줄에 EOL(개행)이 있어야 하며, 아닌 경우 컴파일 에러가 발생합니다. Grader 설정에서 개행을 추가하도록 하면 회피할 수 있습니다.


아래 내용을 `/usr/bin/umcode.py`에 저장합니다.
```python3
#!/usr/bin/env python3

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2022 Junu Kwon <junukwon7@gmail.com>

"""Umjunsik-lang v2 programming language for cms."""
"""For Korean Umjunsik-lang encoding and decoding"""

import base64
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--src", type=str, default="", help="Source Code")
opt = parser.parse_args()

code = ''
with open(opt.src, 'rt') as file:
            code = ''.join(file.readlines())

os.remove(opt.src)

fout = open(opt.src,'w', encoding='utf8')

for line in code:
    print(line, file=fout, end="")

print("", file=fout)
```

# 3. umjunsik-lang-python 인터프리터 사용
전반적으로 잘 작동하지만, 간헐적으로 0이 아닌 값을 리턴해 프로그램이 종료되는 이슈가 있습니다.

## 3.1. 엄준식 grader 설정
아래 내용을 `cms/cms/grading/languages/umlang2.py`에 저장합니다.
```python3
#!/usr/bin/env python3

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2022 Junu Kwon <junukwon7@gmail.com>

"""Umjunsik-lang v2 programming language definition."""

from cms.grading import Language


__all__ = ["Umlang2"]


class Umlang2(Language):
    """This defines the Umjunsik-lang programming language, interpreted with the
    standard Umjunsik-lang interpreter available in the system.

    Umjunsik-lang v2 standard

    """

    @property
    def name(self):
        """See Language.name."""
        return "Umjunsik-lang 2"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".umm"]

    @property
    def executable_extension(self):
        """See Language.executable_extension."""
        return ".umm"

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        if source_filenames[0] != executable_filename:
            return [["/bin/cp", source_filenames[0], executable_filename]]
        else:
            # We need at least one command to collect execution stats.
            return [["/bin/true"]]

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""
        args = args if args is not None else []
        return [["/usr/bin/umlang_runtime.py", "--source="+executable_filename]]
```
이후 수정사항을 반영하기 위해서 `python3 setup.py install` 작업이 필요합니다.

## 3.2. 엄랭 인터프리터 설정
아래 내용을 `/usr/bin/umlang_runtime.py`에 저장합니다. 아래 예시는 [Python umjunsik-lang 구현체](https://github.com/rycont/umjunsik-lang/blob/master/umjunsik-lang-python/runtime.py)를 기반으로 작성했으나, 다른 방식의 구현 역시 가능합니다.
```python3
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import argparse

class Umjunsik:
    def __init__(self):
        self.data = [0]*256

    def toNumber(self, code):
        return eval('*'.join(list(map(lambda cmd:str((self.data[cmd.count('어')-1] if cmd.count('어') else 0) + cmd.count('.') - cmd.count(',')), code.split(' ')))))

    @staticmethod
    def type(code):
        if '동탄' in code:
            return 'IF'
        if '준' in code:
            return 'MOVE'
        if '화이팅!' in code:
            return 'END'
        if '식' in code and '?' in code:
            return 'INPUT'
        if '식' in code and '!' in code:
            return 'PRINT'
        if '식' in code and 'ㅋ' in code:
            return 'PRINTASCII'
        if '엄' in code:
            return 'DEF'

    def compileLine(self, code):
        if code == '':
            return None
        TYPE = self.type(code)
        
        if TYPE == 'DEF':
            var, cmd = code.split('엄')
            self.data[var.count('어')] = self.toNumber(cmd)
        elif TYPE == 'END':
            print(self.toNumber(code.split('화이팅!')[1]), end='')
            sys.exit()
        elif TYPE == 'INPUT':
            self.data[code.replace('식?', '').count('어')] = int(input())
        elif TYPE == 'PRINT':
            print(self.toNumber(code[1:-1]), end='')
        elif TYPE == 'PRINTASCII':
            value = self.toNumber(code[1:-1])
            print(chr(value) if value else '\n', end='')
        elif TYPE == 'IF':
            cond, cmd = code.replace('동탄', '').split('?')
            if self.toNumber(cond) == 0:
                return cmd
        elif TYPE == 'MOVE':
            return self.toNumber(code.replace('준', ''))

    def compile(self, code, check=True, errors=100000):
        jun = False
        recode = ''
        spliter = '\n' if '\n' in code else '~'
        code = code.rstrip().split(spliter)
        if check and (code[0].replace(" ","") != '어떻게' or code[-1] != '이 사람이름이냐ㅋㅋ' or not code[0].startswith('어떻게')):
            raise SyntaxError('어떻게 이게 엄랭이냐!')
        index = 0
        error = 0
        while index < len(code):
            errorline = index
            c = code[index].strip()
            res = self.compileLine(c)
            if jun:
                jun = False
                code[index] = recode                
            if isinstance(res, int):
                index = res-2
            if isinstance(res, str):
                recode = code[index]
                code[index] = res
                index -= 1
                jun = True

            index += 1
            error += 1
            if error == errors:
                raise RecursionError(str(errorline+1) + '번째 줄에서 무한 루프가 감지되었습니다.')
        return

    def compilePath(self, path):
        with open(path, 'rt', encoding='UTF8') as file:
            code = ''.join(file.readlines())
            self.compile(code)
        return




runtime = Umjunsik()
parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str, default="", help="Source Code")
opt = parser.parse_args()
runtime.compilePath(opt.source)
```

