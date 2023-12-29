import csv
import random
import pymorphy3


def to_lowercase_without_symbols(s: str):
    new = ""
    for i in s:
        if i.isalpha() or i.isdigit() or i.isspace():
            new += i.lower()
    new = " ".join(new.strip().split())
    return new


def parse_lawers_from_txt(filename):
    lines = open(filename, "r", encoding="UTF-8").readlines()
    lawers_and_levels = set()
    locations = set()
    for l in lines:
        l = l.strip().lower()
        if " суд " in l:
            sp = l.split("суд")
            lw = sp[0].strip()
            loc = sp[1].strip()

            lawers_and_levels.add(lw)
            locations.add(loc)

        elif l.endswith("суд"):
            lawers_and_levels.add(l[:-4])
        else:
            pass

    lawers_splited = [[c.strip() for c in i.split()] for i in lawers_and_levels if len(i.split()) == 2]
    levels_noun = {i[1] for i in lawers_splited}
    lawers_noun = {i[0] for i in lawers_splited}

    return noun_to_ablt_set(lawers_noun), locations, noun_to_ablt_set(levels_noun)


def noun_to_ablt_set(words):
    morph = pymorphy3.MorphAnalyzer()
    res = set()
    try:
        res = {(l, morph.parse(l)[0].inflect({'ablt'}).word.capitalize()) for l in words}
    except:
        pass
    return res


def noun_to_gent_word(word):
    word = word.strip()
    morph = pymorphy3.MorphAnalyzer()
    return morph.parse(word)[0].inflect({'gent'}).word


def get_lawers_locations_levels_tp_pairs():
    lawers_with_pos = []
    with open("lawers.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        file_reader.__next__()
        for row in file_reader:
            lawers_with_pos.append((row[0].lower(), row[1].lower()))

    lawers_and_levels = set()
    locations = set()
    for l in lawers_with_pos:
        if " суд " in l[0]:
            sp = l[0].split("суд")
            lw = sp[0].strip()
            loc = sp[1].strip()

            sp_tp = l[1].split("судом")
            lw_tp = sp_tp[0].strip()
            lawers_and_levels.add((lw, lw_tp))
            locations.add(loc)

        elif "ас " in l[0]:
            locations.add(l[0].split("ас ")[1])

        elif l[0].endswith("суд"):
            lawers_and_levels.add((l[0][:-4], l[1][:-6]))

    levels = {(i[0].split()[1], i[1].split()[1]) for i in lawers_and_levels if len(i[0].split()) == 2}
    lawers = {(i[0].split()[0], i[1].split()[0]) for i in lawers_and_levels if len(i[0].split()) == 2}

    return lawers, locations, levels


def generate_full(lawers, locations, levels):
    dataset = []
    for location in locations:
        for level in levels:
            for lawer in lawers:
                lw = f"{lawer[0].capitalize()} {level[0]} суд {location}"
                lw_tp = f"{lawer[1].capitalize()} {level[1]} судом {location}"
                dataset.append((lw, lw_tp))
    return dataset


def generate_hardcoded(locations):
    dataset = []
    for location in locations:
        lw = f"Арбитражный суд {location}"
        lw_tp = f"Арбитражным судом {location}"
        dataset.append((lw, lw_tp))

        lw = f"АС {location}"
        lw_tp = f"АС {location}"
        dataset.append((lw, lw_tp))

        lw = f"А/С {location}"
        lw_tp = f"А/С {location}"
        dataset.append((lw, lw_tp))

        n = random.randint(1, 300)
        lw = f"Судебный участок №{n} {location}"
        lw_tp = f"Судебным участком №{n} {location}"
        dataset.append((lw, lw_tp))

        n = random.randint(1, 300)
        lw = f"СУ №{n} {location}"
        lw_tp = f"СУ №{n} {location}"
        dataset.append((lw, lw_tp))

        n = random.randint(1, 300)
        lw = f"С/У №{n} {location}"
        lw_tp = f"С/У №{n} {location}"
        dataset.append((lw, lw_tp))

        lw = f"Федеральный участок {location}"
        lw_tp = f"Федеральным участком {location}"
        dataset.append((lw, lw_tp))

        lw = f"ФУ {location}"
        lw_tp = f"ФУ {location}"
        dataset.append((lw, lw_tp))

        lw = f"Ф/У {location}"
        lw_tp = f"Ф/У {location}"
        dataset.append((lw, lw_tp))

        lw = f"Мировой суд {location}"
        lw_tp = f"Мировым судом {location}"
        dataset.append((lw, lw_tp))

        lw = f"МС {location}"
        lw_tp = f"МС {location}"
        dataset.append((lw, lw_tp))

        lw = f"М/С {location}"
        lw_tp = f"М/С {location}"
        dataset.append((lw, lw_tp))

        lw = f"Федеральный суд {location}"
        lw_tp = f"Федеральным судом {location}"
        dataset.append((lw, lw_tp))

        lw = f"ФС {location}"
        lw_tp = f"ФС {location}"
        dataset.append((lw, lw_tp))

        lw = f"Ф/С {location}"
        lw_tp = f"Ф/С {location}"
        dataset.append((lw, lw_tp))

        n = random.randint(1, 300)
        lw = f"МС СУ №{n} {location}"
        lw_tp = f"МС СУ №{n} {location}"
        dataset.append((lw, lw_tp))

        n = random.randint(1, 300)
        lw = f"МССУ №{n} {location}"
        lw_tp = f"МССУ №{n} {location}"
        dataset.append((lw, lw_tp))

    return dataset


def generate_once(lawers, locations, levels):
    dataset = []
    locations = list(locations)
    levels = list(levels)
    for lawer in lawers:
        level = random.choice(levels)
        location = random.choice(locations)
        lw = f"{lawer[0].capitalize()} {level[0]} суд {location}"
        lw_tp = f"{lawer[1].capitalize()} {level[1]} судом {location}"
        dataset.append((lw, lw_tp))
    return dataset


def capitalize_locations(loc, cities, regions):
    lowercased_input = loc.lower()  # Приводим всю строку к нижнему регистру
    prefixes = ["обл.", 'о.', 'г.', 'гор.', 'р.', "респ. и."]
    prefixes_without_dot = [i.replace(".", "") for i in prefixes]
    words = [i.strip() for i in lowercased_input.split() if i != ""]  # Разбиваем строку на слова
    result = []
    for word in words:
        is_prefix = False
        for pref in prefixes:
            if word.startswith(pref):
                if word == pref:
                    result.append(word)
                    is_prefix = True
                    break
                result.append(pref)
                word = word[len(pref):]

        if is_prefix:
            continue

        if len(word) <= 3 and word not in prefixes_without_dot:
            result.append(word.upper())
            continue

        if word in cities or word in regions:
                result.append(word.capitalize())
        else:
            result.append(word)  # Если слово не найдено в списке, добавляем его без изменений
    return ' '.join(result)  # Объединяем слова обратно в строку


def write_csv(filename, data):
    with open(filename, mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow(["lawer", "lawer_tp"])
        file_writer.writerows(data)
        print("Записано в файл: ", len(data))


#Парсинг всех токенов и объединение
lawers1, locations1, levels1 = parse_lawers_from_txt("реальные суды.txt")
lawers2, locations2, levels2 = get_lawers_locations_levels_tp_pairs()

levels_unhandled = {tuple((t.lower() for t in i)) for i in levels1 | levels2}
levels = {i for i in levels_unhandled if i[0].lower() != i[1].lower()}

lawers_unhandled = {tuple((t.capitalize() for t in i)) for i in lawers1 | lawers2}
lawers = {i for i in lawers_unhandled if i[0].lower() != i[1].lower()}

#Выделение городов
cities = [i.strip() for i in open("all_cities.txt", "r", encoding="windows-1251").readlines()]
regions = [i.strip() for i in open('regions.txt', "r", encoding="windows-1251").readlines()]
locations = {capitalize_locations(i, cities, regions) for i in locations1 | locations2}
print(f"Количество названий: {len(lawers)}")
print(f"Пример: {random.choice(list(lawers))}")
print()

print(f"Количество уровней: {len(levels)}")
print(f"Пример: {random.choice(list(levels))}")
print()

print(f"Количество местоположений: {len(locations)}")
print(f"Пример: {random.choice(list(locations))}")
print()

dataset_unique = generate_once(lawers, locations, levels)
print(f"Количество уникальных: {len(dataset_unique)}")

dataset_hardcoded = generate_hardcoded(locations)
print(f"Количество хардкода: {len(dataset_hardcoded)}")

unfiltered = dataset_unique + random.choices(dataset_hardcoded, k=len(dataset_unique))
balanced_dataset = list(set(unfiltered))

dataset_lowercased_without_symblos = []
for i in balanced_dataset:
    dataset_lowercased_without_symblos.append(
        (to_lowercase_without_symbols(i[0]),
         to_lowercase_without_symbols(i[1]))
    )

write_csv("datasets/hardcode.csv", dataset_hardcoded)
write_csv("datasets/unique.csv", dataset_unique)
write_csv("datasets/lowercased.csv", dataset_lowercased_without_symblos)