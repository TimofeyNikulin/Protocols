import eel
import sqlite3
from docxtpl import DocxTemplate
import os
from datetime import date


db = sqlite3.connect("db.db")
sql = db.cursor()


eel.init("web")


@eel.expose
def get_committee(name=None):
    if name == None:
        return 'Не передано название комитета'
    else:
        committee, chapter, deputy = sql.execute(
            """SELECT Committee, Chapter, Deputy FROM Committee WHERE Committee = ?""", (name, )).fetchone()
        return committee, chapter, deputy


@eel.expose
def get_activist(job_title=None, class_of_education=None, committee=None):
    if job_title == None or class_of_education == None or committee == None:
        return 'Не переданы должность, комитет или класс обучения'
    else:
        name_surname = sql.execute(
            """SELECT Name_Surname FROM Activist WHERE Class = ? AND Job_title = ? AND Committee = ?""", (class_of_education, job_title, committee, )).fetchone()[0]
        return f"{name_surname} {class_of_education}"


@eel.expose
def convert_to_doc(number, date_value: str, present, agenda, discussion, solution, committee):
    if committee != "BSP":
        template = r'./Шаблоны протоколов/Шаблон протокола собрания комитета.docx'
    else:
        template = r'./Шаблоны протоколов/Шаблон протокола собрания БСП.docx'
    activists = present["activists"]
    present_activists = []
    if committee != "BSP":
        for activist_code in activists:
            job_title = activist_code[0]
            class_of_education = activist_code[1:]
            activist = get_activist(job_title, class_of_education, committee)
            present_activists.append(activist)
            if activist == 'Не переданы должность, комитет или класс обучения':
                return 'Не переданы должность, комитет или класс обучения'
    else:
        for activist_code in activists:
            committee_for_get_activist = activist_code[1:]
            if activist_code[0] == "C":
                activist, header_committee_name = sql.execute(
                    """SELECT Chapter, Russian_name_for_header FROM Committee WHERE Committee = ?""", (committee_for_get_activist, )).fetchone()
                activist = f"{activist} председатель {header_committee_name}"
            else:
                activist, header_committee_name = sql.execute(
                    """SELECT Deputy, Russian_name_for_header FROM Committee WHERE Committee = ?""", (committee_for_get_activist, )).fetchone()
                activist = f"{activist} заместитель {header_committee_name}"
            present_activists.append(activist)
    committee_name, header_committee_name = sql.execute(
        """SELECT Russian_name, Russian_name_for_header FROM Committee WHERE Committee = ?""", (committee, )).fetchone()
    chapter = present["chapter"]
    deputy = present["deputy"]
    if committee != "BSP":
        if deputy != '':
            present_activists.insert(0,
                                     f"{deputy}, заместитель председателя {header_committee_name}")
        if chapter != '':
            present_activists.insert(0,
                                     f"{chapter}, председатель {header_committee_name}")
        else:
            chapter = sql.execute(
                """SELECT Chapter FROM Committee WHERE Committee = ?""", (committee, )).fetchone()[0]
    else:
        if deputy != '':
            present_activists.insert(0,
                                     f"{deputy}, заместитель главы БСП")
        if chapter != '':
            present_activists.insert(0,
                                     f"{chapter}, глава БСП")
        else:
            chapter = sql.execute(
                """SELECT Chapter, Russian_name_for_header FROM Committee WHERE Committee = ?""", (committee, )).fetchone()[0]
    present_activists = '\n'.join(present_activists)
    if date_value == '':
        return 'Заполните поле даты'
    else:
        date_value = date(int(date_value[:date_value.index(
            '-')]), int(date_value[date_value.index('-') + 1:date_value.rindex('-')]), int(date_value[date_value.rindex('-') + 1:])).strftime('%d.%m.%Y')
    context = {
        "header_committee": header_committee_name,
        "number": number,
        "date": date_value,
        "present": present_activists,
        "agenda": agenda,
        "discussion": discussion,
        "solution": solution,
        "committee": committee_name.upper(),
        "chapter": chapter
    }
    if '' in context.values():
        return 'Заполните все поля'
    else:
        doc = DocxTemplate(template)
        doc.render(context)
        doc.save(
            fr"Готовые протоколы/Протокол собрания {committee_name} №{number}.docx")
        return


if __name__ == "__main__":
    eel.start("index.html", size=(600, 925))
