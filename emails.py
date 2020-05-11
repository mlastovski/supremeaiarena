# -*- coding: utf-8 -*-
import sqlite3


def commit_to_text_file():
    conn = sqlite3.connect('newsletter.db')
    cur = conn.cursor()
    cur.execute("SELECT mail FROM mailing_group")

    rows = cur.fetchall()
    rows_list = [str(x) for x, in rows]
    string_from_tuple = ''.join(str(rows_list))
    remove_bad_char = string_from_tuple.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",",
                                                                                                                    "").replace(
        "'", "")
    # print(remove_bad_char)
    clear_emails = remove_bad_char.replace(" ", "\n")

    text_file = open("emails.txt", "wt")
    text_file.write(clear_emails)
    text_file.close()

    emails_with_coma = remove_bad_char.replace(" ", ", ")
    text_file_two = open("emails_with_coma.txt", "wt")
    text_file_two.write(emails_with_coma)
    text_file.close()


if __name__ == '__main__':
    commit_to_text_file()
