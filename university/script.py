#!/usr/bin/env python

"""
Практическая работа №4: Расчет статистических параметров текста на Python
"""

import math
import heapq

# Получение входного сообщения от пользователя
# Если пользователь не ввел сообщение, используется значение по умолчанию
message = input("Введите сообщение (или нажмите Enter для ввода \"МАМА_МЫЛА_РАМУ\")\n> ") or "МАМА_МЫЛА_РАМУ"

# Создание словаря, где ключи - символы алфавита, значения - количество их появлений
# 1. set(message) создает множество уникальных символов
# 2. list() преобразует множество в список
# 3. sorted() сортирует список символов
# 4. dict comprehension создает словарь с подсчетом количества каждого символа
alphabet = { c: message.count(c) for c in sorted(list(set(message))) }

# Вычисление энтропии сообщения
# Для каждого символа вычисляется p_i * log2(p_i), где p_i - вероятность появления символа
# Вероятность вычисляется как количество появлений символа / общую длину сообщения
entropy = -sum( i / len(message) * math.log2(i / len(message)) for i in alphabet.values() )

# Вывод результатов анализа
print(f"""Сообщение:          {message}
Длина сообщения:    {len(message)}
Алфавит сообщения:  {''.join(alphabet.keys())}
Размер алфавита:    {len(alphabet)}
Количество:         {'  '.join(str(v) for v in alphabet.values())}
Символ:             {'  '.join(alphabet.keys())}
Количество информации на один символ сообщения:  H={entropy:.3f} бит""")

# Структура для узла дерева Хаффмана
class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char: str = char
        self.freq: int = freq
        self.left: HuffmanNode | None = left
        self.right: HuffmanNode | None = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(alphabet):
    # Создаем список узлов для каждого символа
    heap = [HuffmanNode(char=char, freq=freq) for char, freq in alphabet.items()]
    # Преобразуем список в кучу (min-heap)
    heapq.heapify(heap)
    
    # Пока в куче больше одного узла
    while len(heap) > 1:
        # Извлекаем два узла с наименьшей частотой
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        # Создаем новый узел с суммой частот и добавляем его обратно в кучу
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    
    # Возвращаем корневой узел дерева Хаффмана
    return heapq.heappop(heap)


def print_huffman_tree(node, prefix="", is_left=True, code=""):
    if node is not None:
        #  Обходим правое поддерево, добавляя '1' к коду
        print_huffman_tree(node.right, prefix + ("│   " if is_left else "    "), False, code + "1")
        # Вывод текущего узла с его двоичным кодом
        print(prefix + ("└── " if is_left else "┌── ") + (f"{node.char}:{code}" if node.char else code))
        # Обходим левое поддерево, добавляя '0' к коду
        print_huffman_tree(node.left, prefix + ("    " if is_left else "│   "), True, code + "0")

# Построение дерева Хаффмана
print("Дерево Хаффмана:")
print_huffman_tree(build_huffman_tree(alphabet))
