'''
Copyright 2021 The Authors: Qingchao Shen, Haoyang Ma, Junjie Chen, Yongqiang Tian, Shing-Chi Cheung, Xiang Che

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''




def Red(string):
    return '\033[1;31m' + string + '\033[0m'

def Green(string):
    return '\033[1;32m' + string + '\033[0m'

def Yellow(string):
    return '\033[1;33m' + string + '\033[0m'

def Blue(string):
    return '\033[1;34m' + string + '\033[0m'

def Magenta(string):
    return '\033[1;35m' + string + '\033[0m'

def Cyan(string):
    return '\033[1;36m' + string + '\033[0m'