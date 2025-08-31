# Вариант
`alg | risc | neum | hw | tick | binary | trap | mem | pstr | prob1 | vector`

#### Холин Никита Сергеевич, Р3217, 409801

### Оглавление

# Язык программирования
``` ebnf
<letter>        ::= "A"…"Z" | "a"…"z" | "_"
<digit>         ::= "0"…"9"
<identifier>    ::= <letter> { <letter> | <digit> }

<int>           ::= <digit> { <digit> }
<array>         ::= <digit> { <digit> }
<string>        ::= <int>'<любые печатные символы>'

<var>           ::= string <identifier> = <string>; | int <identifier> = <int>; 
                                                  | array <identifier> = <int>;

<print>         ::= print(<identifier>);
<if>            ::= if (<expression>) {<любой код>}
<while>         ::= while (<expression>) {<любой код>}

<interruption>  ::= interruption
```

## Семантика
### Стратегия вычисления:
- Программа выполняется последовательно 
- Переменные должны быть объявлены до использования
- Промежуточные результаты вычислений сохраняются в регистры G1 - G6
- При возникновении прерывания, начинает исполнятся код, расположенный после метки interruption
- Область видимости переменной - все переменные глобальные
- Переменные типа int - изменяемые, типа string - константы


## Организация памяти
- Общая память для команд и данных
- Размер машинного слова - 32 бита
- В памяти с адреса 0xС располагаются данные, сразу после начинаются команды
- Первые 12 ячеек занят под ввод/вывод и сохранение регистров при прерывании.
- Big-endian
- Ячейка 0x0 - ввод, 0х1 - вывод
- Виды адресации - прямая и косвенная
- Нет динамической памяти, вся память выделена до исполнения программы.


## Регистры
- `G1..G6,A,B,BR` - Регистры общего назначения
- `PC` - program counter
- `AR` - регистр адреса для обращения к памяти
- `INT` - регистр в котором всегда хранится начало обработчика прерывания
- `INTPC` - регистр в который сохраняется PC перед вызовом обработчика прерывания


# Система команд
- Длина инструкции 32 бита
### Форматы: 
Команды без обращения к памяти:
- `|4 bit OPCODE|20 bit 0|4 bit r1|4 bit r2|`

Команда JMP (безусловный переход):
- `|4 bit OPCODE|0111|24 bit address|`

Загрузка значения в регистр:
- `|4 bit OPCODE|1000|20 bit immediate value|4 bit registr|`

Загрузка в память:
- `|4 bit OPCODE|1110|20 bit memory address |4 bit registr|`

Чтение из памяти:
- `|4 bit OPCODE|1010|20 bit memory address |4 bit registr|`

Косвенная загрузка:
- `|4 bit OPCODE|1111|16 bit 0|4 bit address r1|4 bit r2|`

Косвенное чтение:
- `|4 bit OPCODE|1011|16 bit 0|4 bit address r1|4 bit r2|`




### Описание команд:
-    `JMPE r1 r2: if r1 == r2 -> PC += 1`
-    `JMP  addr: PC = addr  `
-    `JMPL r1 r2: if r1 < r2 -> PC += 1`
-    `AND  r1 r2: r1 = r1 & r2`
-    `NOT  r1:    r1 = ~r1`
-    `MUL  r1 r2: r1 = r1 * r2` 
-    `OR   r1 r2: r1 = r1 | r2`
-    `SUB  r1 r2: r1 = r1 - r2`
-    `ADD  r1 r2: r1 = r1 + r2`
-    `MOV  r1 r2: r1 = r2`
-    `DIV  r1 r2: r1 = r1/r2`
-    `LOAD r1 r2: r1 = MEM(r2)`
-    `LOAD r1 addr: r1 = MEM(addr)`
-    `STORE r1 r2: MEM(r2) = r1`
-    `STORE r1 addr: MEM(addr) = r1`
-    `LOADIM r1 val: r1 = val`
-    `HALT`

# Транслятор
### Запуск: 
`python translator.py [input_file] [out_file]`

### Пример:
![alt text](https://sun9-17.userapi.com/s/v1/if2/N3Bwhw3Pw9zTdJpNrZfr_rMgLfmGNPnGOi6pbX73H1_VaWwp5Jjtf90WQcs7vVO2Ak7ReeN6wfJNva9taEkhbd7d.jpg?quality=95&as=32x3,48x4,72x6,108x9,160x13,240x20,360x30,480x40,540x45,640x54,720x60,1080x90,1122x94&from=bu&cs=1122x0)

### Запуск транслятора:
![alt text](https://sun9-27.userapi.com/s/v1/if2/HOds2fCH_cnLEyC62r-LqvCATfwQH8__q-Xt1i1pQqmgJXIWAxFymXBkH_s9SVlfqWtJE_lMVxQe0V2YueGhJ_52.jpg?quality=95&as=32x5,48x7,72x10,108x15,160x23,240x34,360x52,480x69,540x78,640x92,720x103,822x118&from=bu&cs=822x0)

### Результат:

```
0. 3800000f - LOADIM
1. 380000b7 - LOADIM
2. 2E0000c7 - STORE
3. 38000487 - LOADIM
4. 2E0000d7 - STORE
5. 38000657 - LOADIM
6. 2E0000e7 - STORE
7. 380006c7 - LOADIM
8. 2E0000f7 - STORE
9. 380006c7 - LOADIM
10. 2E000107 - STORE
11. 380006f7 - LOADIM
12. 2E000117 - STORE
13. 38000207 - LOADIM
14. 2E000127 - STORE
15. 38000577 - LOADIM
16. 2E000137 - STORE
17. 380006f7 - LOADIM
18. 2E000147 - STORE
19. 38000727 - LOADIM
20. 2E000157 - STORE
21. 380006c7 - LOADIM
22. 2E000167 - STORE
23. 38000647 - LOADIM
24. 2E000177 - STORE
25. 1A0000c0 - LOAD
26. 380000c1 - LOADIM
27. 38000012 - LOADIM
28. 38000007 - LOADIM
29. 40000070 - JMPL
30. 97000024 - JMP
31. d0000072 - ADD
32. d0000012 - ADD
33. 1B000013 - LOAD
34. 2E000013 - STORE
35. 9700001d - JMP
36. 50000000 - HALT
```


### Принцип работы:
Весь данный код приводится к удобному для трансляции виду: между ключевыми словами и операторами ставятся пробелы, все выражения вида `a - b` заменяются на `a + -b` для простоты арифметики. После код разбивается на строчки, каждая строчка на токены и в соответсвии с этим происходит последовательный перевод каждой строки в машинный код.

# Модель процессора

## Data Path
![alt text](https://sun9-36.userapi.com/s/v1/if2/7jGG40CUcgE3XcT8pRzd736x5iGL5STZf7-5wEguCJPId2oJUbZHF2t_NJ9fKhN7SgqVd0iw7e-oHvSlyMXftLFC.jpg?quality=95&as=32x25,48x37,72x56,108x84,160x124,240x186,360x279,480x372,540x418,640x495,720x557,1054x816&from=bu&cs=1054x0)

## Control Unit
![alt text](https://sun9-31.userapi.com/s/v1/if2/DToA99Ceer3OgnY9LgHS2DBLEJEm_RKzzAM9nsLPFcYWvGcWL0i-Jyl--KhYfSGNbX5eX35aRY4-RBpoexq1WfHW.jpg?quality=95&as=32x27,48x40,72x60,108x89,160x133,240x199,360x298,480x398,540x448,640x530,720x597,870x721&from=bu&cs=870x0)
