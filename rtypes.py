types_mapping = {
    "1": ("Нормальная ЭКГ"),
    "2": ("Вариант нормальной"),
    "3": ("Патологическая"),
    "4": ("Неинтерпретируемая"),
    "101": ("ЧСС(уд/мин)"),

    "11": ("Нормальное положение"),
    "12": ("Горизонтальное"),
    "13": ("Вертикальное"),
    "14": ("Вправо"),
    "15": ("Влево"),

    "21": ("Синусовый ритм"),
    "22": ("Синусовая тахикардия"),
    "23": ("Синусовая брадикардия"),
    "24": ("Экстрасистолия"),
    "25": ("Синусовая аритмия"),
    "26": ("Трепетание предсердий"),
    "27": ("Фибрилляция предсердий"),
    "28": ("Желудочковая тахикардия"),

    "31": ("Укорочённый PQ интервал"),
    "32": ("AV-блокада"),
    "33": ("Удлинённый QT интервал"),
    "34": ("зменение зубца T"),
    "35": ("(БЛНПГ)Блокада левой ножки пучка Гиса"),
    "36": ("(НБЛНПГ)Неполная блокада левой ножки пучка Гиса"),
    "37": ("(ПБПНПГ)Полная блокада правой ножки пучка Гиса"),
    "38": ("(НБПНПГ)Неполная блокада правой ножки пучка Гиса"),

    "41": ("Гипертрофия левого желудочка"),
    "42": ("Гипертрофия правого желудочка"),
    "43": ("Гипертрофия левого предсердия"),
    "44": ("Гипертрофия правого предсердия"),
    "45": ("Ишемические изменения"),
    "46": ("Смещение ST-сегмента"),
    "47": ("Кардиостимулятор (из заключения)")
}

default_data = [
    {'group_label': "Общее",
     'group_data': [{"view": "checkbox", "label": "Нормальная ЭКГ", "value": 0, "name": "1"},
                    {"view": "checkbox", "label": "Вариант нормальной", "value": 0, "name": "2"},
                    {"view": "checkbox", "label": "Патологическая", "value": 0, "name": "3"},
                    {"view": "checkbox", "label": "Неинтерпретируемая", "value": 0, "name": "4"},
                    {"view": "text", "label": "ЧСС(уд/мин)", "value": 0, "name": "101"},
                    ]},
    {'group_label': "Отклонение оси сердца",
     'group_data': [{"view": "checkbox", "label": "Нормальное положение", "value": 0, "name": "11"},
                    {"view": "checkbox", "label": "Горизонтальное", "value": 0, "name": "12"},
                    {"view": "checkbox", "label": "Вертикальное", "value": 0, "name": "13"},
                    {"view": "checkbox", "label": "Вправо", "value": 0, "name": "14"},
                    {"view": "checkbox", "label": "Влево", "value": 0, "name": "15"},
                    ]},
    {'group_label': "Ритм",
     'group_data': [{"view": "checkbox", "label": "Синусовый ритм", "value": 0, "name": "21"},
                    {"view": "checkbox", "label": "Синусовая тахикардия", "value": 0, "name": "22"},
                    {"view": "checkbox", "label": "Синусовая брадикардия", "value": 0, "name": "23"},
                    {"view": "checkbox", "label": "Экстрасистолия", "value": 0, "name": "24"},
                    {"view": "checkbox", "label": "Синусовая аритмия", "value": 0, "name": "25"},
                    {"view": "checkbox", "label": "Трепетание предсердий", "value": 0, "name": "26"},
                    {"view": "checkbox", "label": "Фибрилляция предсердий", "value": 0, "name": "27"},
                    {"view": "checkbox", "label": "Желудочковая тахикардия", "value": 0, "name": "28"},

                    ]},
    {'group_label': "Нарушения функции проводимости",
     'group_data': [{"view": "checkbox", "label": "Укорочённый PQ интервал", "value": 0, "name": "31"},
                    {"view": "checkbox", "label": "AV-блокада", "value": 0, "name": "32"},
                    {"view": "checkbox", "label": "Удлинённый QT интервал", "value": 0, "name": "33"},
                    {"view": "checkbox", "label": "Изменение зубца T", "value": 0, "name": "34"},
                    {"view": "checkbox", "label": "(БЛНПГ)Блокада левой ножки пучка Гиса", "value": 0, "name": "35"},
                    {"view": "checkbox", "label": "(НБЛНПГ)Неполная блокада левой ножки пучка Гиса", "value": 0,
                     "name": "36"},
                    {"view": "checkbox", "label": "(ПБПНПГ)Полная блокада правой ножки пучка Гиса", "value": 0,
                     "name": "37"},
                    {"view": "checkbox", "label": "(НБПНПГ)Неполная блокада правой ножки пучка Гиса", "value": 0,
                     "name": "38"}
                    ]},
    {'group_label': "Другие Показатели",
     'group_data': [{"view": "checkbox", "label": "Гипертрофия левого желудочка", "value": 0, "name": "41"},
                    {"view": "checkbox", "label": "Гипертрофия правого желудочка", "value": 0, "name": "42"},
                    {"view": "checkbox", "label": "Гипертрофия левого предсердия", "value": 0, "name": "43"},
                    {"view": "checkbox", "label": "Гипертрофия правого предсердия", "value": 0, "name": "44"},
                    {"view": "checkbox", "label": "Ишемические изменения", "value": 0, "name": "45"},
                    {"view": "checkbox", "label": "Смещение ST-сегмента", "value": 0, "name": "46"},
                    {"view": "checkbox", "label": "Кардиостимулятор (из заключения)", "value": 0, "name": "47"},
                    ]}

]
