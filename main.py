import csv
import re
from pprint import pprint

def new_contacts(contacts_list):
    pattern = r'([А-Я])'
    substitution = r' \1'

    for contact in contacts_list[1:]:
        full_name = contact[0] + contact[1] + contact[2]
        name_parts = re.sub(pattern, substitution, full_name).split()

        for i in range(3):
            try:
                contact.pop(i)
                contact.insert(i, name_parts[i])
            except:
                contact.insert(i, "")

    contact_dict = {}
    contacts_list_updated =[]
    for contacts in contacts_list[1:]:
        last_name = contacts[0]
        if last_name not in contact_dict:
            contact_dict[last_name] = contacts
        else:
            for id, item in enumerate(contact_dict[last_name]):
                if item == '':
                    contact_dict[last_name][id] = contacts[id]

    for last_name, contact in contact_dict.items():
        for contacts in contact:
            if contact not in contacts_list_updated:
                contacts_list_updated.append(contact)

    return new_phone_numbers(contacts_list_updated)


def new_phone_numbers(contacts_list):
    pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?\s*\D?(\d{3})[-\s+]?(\d{2})-?(\d{2})((\s)?\(?(доб.)?\s?(\d+)\)?)?')
    substitution = r'+7(\2)\3-\4-\5\7\8\9'

    for contact in contacts_list:
        contact[5] = pattern.sub(substitution, contact[5])

    return contacts_list


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    new_contacts_list = new_contacts(contacts_list)

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(new_contacts_list)