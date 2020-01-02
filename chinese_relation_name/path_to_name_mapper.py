'''
Map codes
- Parent
= Partner
+ Offspring
F Female
M Male
O Other
* Gender Wildcard

https://omniglot.com/language/kinship/cantonese.htm
https://en.wikipedia.org/wiki/Chinese_kinship
https://www.oakton.edu/user/4/billtong/chinaclass/chinesekin.htm

'''
map_codes = {
    # == 1 relation apart ==
    '-F': (lambda path: ['Mother']),
    '-M': (lambda path: ['Father']),
    '-O': (lambda path: ['Mother', 'Father']),
    '+F': (lambda path: ['Daughter']),
    '+M': (lambda path: ['Son']),
    '+O': (lambda path: ['Daughter', 'Son']),
    '=F': (lambda path: ['Wife']),
    '=M': (lambda path: ['Husband']),
    '=O': (lambda path: ['Wife', 'Husband']),

    # == 2 relations apart ==

    # Grandparents
    '-F,-F': (lambda path: ['Maternal Grandmother']),
    '-F,-M': (lambda path: ['Maternal Grandfather']),
    '-F,-O': (lambda path: ['Maternal Grandmother', 'Maternal Grandfather']),
    '-M,-F': (lambda path: ['Paternal Grandmother']),
    '-M,-M': (lambda path: ['Paternal Grandfather']),
    '-M,-O': (lambda path: ['Paternal Grandmother', 'Paternal Grandfather']),
    '-O,-F': (lambda path: ['Maternal Grandmother', 'Paternal Grandmother']),
    '-O,-M': (lambda path: ['Maternal Grandfather', 'Paternal Grandfather']),
    '-O,-O': (lambda path: ['Maternal Grandmother', 'Maternal Grandfather', 'Paternal Grandmother', 'Paternal Grandfather']),

    # Steparents
    '-*,=F': (lambda path: ['Stepmother']),
    '-*,=M': (lambda path: ['Stepfather']),
    '-*,=O': (lambda path: ['Stepmother', 'Stepfather']),


    # Siblings
    '-*,+F': (lambda path: get_sister(path)),
    '-*,+M': (lambda path: get_brother(path)),
    '-*,+O': (lambda path: get_sister(path) + get_brother(path)),

    # Parents in law
    '=F,-F': (lambda path: ["Wife's Mother"]),
    '=F,-M': (lambda path: ["Wife's Father"]),
    '=F,-O': (lambda path: ["Wife's Mother", "Wife's Father"]),
    '=M,-F': (lambda path: ["Husband's Mother"]),
    '=M,-M': (lambda path: ["Husband's Father"]),
    '=M,-O': (lambda path: ["Husband's Mother", "Husband's Father"]),
    '=O,-F': (lambda path: ["Wife's Mother","Husband's Mother"]),
    '=O,-M': (lambda path: ["Wife's Father","Husband's Father"]),
    '=O,-O': (lambda path: ["Wife's Mother", "Wife's Father", "Husband's Mother", "Husband's Father"]),

    # Partner's Partner (not defined)

    # Step Children
    '=*,+F': (lambda path: ["Stepdaughter"]),
    '=*,+M': (lambda path: ["Stepson"]),
    '=*,+O': (lambda path: ["Stepdaughter", "Stepson"]),

    # Child's parent / ex-partner
    '+*,-*': (lambda path: ["Child's Parent/ex-Partner"]),

    # Son/Daughter in law (do we have different terms for same sex relationships? e.g. +F,=F)
    '+*,=F': (lambda path: ["Daughter In Law"]),
    '+*,=M': (lambda path: ["Son In Law"]),
    '+*,=O': (lambda path: ["Daughter In Law", "Son in Law"]),

    # Grandchildren
    '+F,+F': (lambda path: ["Grandaughter Daughter's Side"]),
    '+F,+M': (lambda path: ["Grandson Daughter's Side"]),
    '+F,+O': (lambda path: ["Grandaughter Daughter's Side", "Grandson Daughter's Side"]),
    '+M,+F': (lambda path: ["Grandaughter Son's Side"]),
    '+M,+M': (lambda path: ["Grandson Son's Side"]),
    '+M,+O': (lambda path: ["Grandaughter Son's Side", "Grandson Son's Side"]),
    '+O,+F': (lambda path: ["Grandaughter Daughter's Side", "Grandaughter Son's Side"]),
    '+O,+M': (lambda path: ["Grandson Daughter's Side", "Grandson Son's Side"]),
    '+O,+O': (lambda path: ["Grandaughter Daughter's Side", "Grandson Daughter's Side",
                                "Grandaughter Son's Side", "Grandson Son's Side"]),

    # --- Great Grandparents
    '-F,-*,-F': (lambda path: ["Maternal Great Grandmother"]),
    '-F,-*,-M': (lambda path: ["Maternal Great Grandfather"]),
    '-F,-*,-O': (lambda path: ["Maternal Great Grandmother", "Maternal Great Grandfather"]),
    '-M,-*,-F': (lambda path: ["Paternal Great Grandmother"]),
    '-M,-*,-M': (lambda path: ["Paternal Great Grandfather"]),
    '-M,-*,-O': (lambda path: ["Paternal Great Grandmother", "Paternal Great Grandfather"]),
    '-O,-*,-F': (lambda path: ["Maternal Great Grandmother", "Paternal Great Grandmother"]),
    '-O,-*,-M': (lambda path: ["Maternal Great Grandfather", "Paternal Great Grandfather"]),
    '-O,-*,-O': (lambda path: ["Maternal Great Grandmother", "Maternal Great Grandfather",
                                    "Paternal Great Grandmother", "Paternal Great Grandfather"]),

    # --= Step Grandparents (not defined)

    # --+ Aunt/Uncles
    '-F,-*,+F': (lambda path: get_mothers_sister(path)),
    '-F,-*,+M': (lambda path: get_mothers_brother(path)),
    '-F,-*,+O': (lambda path: get_mothers_sister(path) + get_mothers_brother(path)),
    '-M,-*,+F': (lambda path: get_fathers_sister(path)),
    '-M,-*,+M': (lambda path: get_fathers_brother(path)),
    '-M,-*,+O': (lambda path: get_fathers_sister(path) + get_fathers_brother(path)),
    '-O,-*,+F': (lambda path: get_mothers_sister(path) + get_fathers_sister(path)),
    '-O,-*,+M': (lambda path: get_mothers_brother(path) + get_fathers_brother(path)),
    '-O,-*,+O': (lambda path: get_mothers_sister(path) + get_mothers_brother(path)
                                + get_fathers_sister(path) + get_fathers_brother(path)),

    # -=- Parents of step parents (not defined)
    # -== Step Step Parents (not defined)
    # -=+ Step siblings / children of step parents (not defined)
    # -+- Not directly related parent of sibling (not defined)

    # -+= Partner of sibling (sibling in law)
    '-*,+*,=F': (lambda path: get_siblings_wife(path)),
    '-*,+*,=M': (lambda path: get_siblings_husband(path)),
    '-*,+*,=O': (lambda path: get_siblings_wife(path) + get_siblings_husband(path)),

    # -++ Nieces/Nephews
    '-*,+F,+F': (lambda path: ["Sister's Daughter"]),
    '-*,+F,+M': (lambda path: ["Sister's Son"]),
    '-*,+F,+O': (lambda path: ["Sister's Daughter", "Sister's Son"]),
    '-*,+M,+F': (lambda path: ["Brother's Daughter"]),
    '-*,+M,+M': (lambda path: ["Brother's Son"]),
    '-*,+M,+O': (lambda path: ["Brother's Daughter", "Brother's Son"]),
    '-*,+O,+F': (lambda path: ["Sister's Daughter", "Brother's Daughter"]),
    '-*,+O,+M': (lambda path: ["Sister's Son", "Brother's Son"]),
    '-*,+O,+O': (lambda path: ["Sister's Daughter", "Sister's Son",
                                "Brother's Daughter", "Brother's Son"]),

    # =-- Grandparents in law (not defined)
    # =-= Stepparents in law (not defined)

    # =-+ Brother/Sister in Law
    '=F,-*,+F': (lambda path: get_wifes_sister(path)),
    '=F,-*,+M': (lambda path: get_wifes_Brother(path)),
    '=F,-*,+O': (lambda path: get_wifes_sister(path) + get_wifes_Brother(path)),
    '=M,-*,+F': (lambda path: get_husbands_sister(path)),
    '=M,-*,+M': (lambda path: get_husbands_Brother(path)),
    '=M,-*,+O': (lambda path: get_husbands_sister(path) + get_husbands_Brother(path)),
    '=O,-*,+F': (lambda path: get_wifes_sister(path) + get_husbands_sister(path)),
    '=O,-*,+M': (lambda path: get_wifes_Brother(path) + get_husbands_Brother(path)),
    '=O,-*,+O': (lambda path: get_wifes_sister(path) + get_wifes_Brother(path)
                                + get_husbands_sister(path) + get_husbands_Brother(path)),

    # ==- Partner's Partner's Parents (not defined)
    # === Partner's Partner's Partner (not defined)
    # ==+ Partner's Step Child (not defined)
    # =+- Partner's Ex-Partner (not defined)
    # =+= Stepchild in law (not defined)
    # =++ Stepchild's child (not defined)

    # +-- Ex-partner's parents (not defined)
    # +-= Ex-partner's partner (not defined)
    # +-+ Ex-partner's Child (not defined)


    # +=- Child in law's Parents (not defined)
    '+*,=*,-F': (lambda path: ["Child's Mother In Law"]),
    '+*,=*,-M': (lambda path: ["Child's Father In Law"]),
    '+*,=*,-O': (lambda path: ["Child's Mother In Law", "Child's Father In Law"]),

    # +== Child in law's other partner (not defined)
    # +=+ Child in law's child (not defined)
    # ++- Grandchild's other parent (not defined)

    # ++= Grandchild in law (not defined)

    # +++ Great Grandchildren
    '+M,+M,+*': (lambda path: ["Child of Son's Son"]),
    '+M,+F,+*': (lambda path: ["Great Grandchild"]),
    '+M,+O,+*': (lambda path: ["Child of Son's Son", "Great Grandchild"]),
    '+F,+*,+*': (lambda path: ["Great Grandchild"]),
    '+O,+*,+*': (lambda path: ["Child of Son's Son", "Great Grandchild"]),

    # --+= Partners of aunts and uncles
    # Same sex couple provide all options
    '-F,-*,+F,=F': (lambda path: ["Mother Sister's Husband", "Mother Brother's Wife"]),
    '-F,-*,+F,=M': (lambda path: ["Mother Sister's Husband"]),
    '-F,-*,+F,=O': (lambda path: ["Mother Sister's Husband", "Mother Brother's Wife"]),
}


def replace_wildcards():

    max_key_length = max(map(len, map_codes))
    return replace_wildcard_iteration(0, map_codes, max_key_length)



def replace_wildcard_iteration(n, rel_map, max_key_length):

    if max_key_length < n:
        return rel_map

    new_rel_map = {}

    for key in rel_map:
        if n < len(key) and key[n] == '*':
            f_key = key.replace('*', 'F', 1)
            m_key = key.replace('*', 'M', 1)
            o_key = key.replace('*', 'O', 1)

            new_rel_map[f_key] = rel_map[key]
            new_rel_map[m_key] = rel_map[key]
            new_rel_map[o_key] = rel_map[key]

        else:
            new_rel_map[key] = rel_map[key]

    return replace_wildcard_iteration(n + 1, new_rel_map, max_key_length)


def get_name(path):

    path_key = ','.join(s.code for s in path.steps)
    full_map = replace_wildcards()

    #import pprint
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(full_map)

    if path_key in full_map:
        path_formatter = full_map[path_key]
        return path_formatter(path)

    else:
        return []


def get_sister(path):
    if path.age_diff < 0:
        return ["Elder Sister"]
    elif path.age_diff > 0:
        return ["Younger Sister"]
    else:
        return ["Sister", "Elder Sister", "Younger Sister"]


def get_brother(path):
    if path.age_diff < 0:
        return ["Elder Brother"]
    elif path.age_diff > 0:
        return ["Younger Brother"]
    else:
        return ["Brother", "Elder Brother", "Younger Brother"]


def get_mothers_sister(path):

    parent = path.steps[0].to_node

    # Elder
    if parent.compare_ages(path.goal) == -1:
        return ["Mother's Elder Sister", "Mother's Sister"]

     # Younger
    elif parent.compare_ages(path.goal) == 1:
        return ["Mother's Younger Sister", "Mother's Sister"]

    # Unknown Age
    else:
        return ["Mother's Elder Sister", "Mother's Younger Sister", "Mother's Sister"]


def get_mothers_brother(path):

    parent = path.steps[0].to_node

    # Elder
    if parent.compare_ages(path.goal) == -1:
        return ["Mother's Elder Brother", "Mother's Brother"]

     # Younger
    elif parent.compare_ages(path.goal) == 1:
        return ["Mother's Younger Brother", "Mother's Brother"]

    # Unknown Age
    else:
        return ["Mother's Elder Brother", "Mother's Younger Brother", "Mother's Brother"]


def get_fathers_sister(path):

    parent = path.steps[0].to_node

    # Elder
    if parent.compare_ages(path.goal) == -1:
        return ["Father's Elder Sister", "Father's Sister"]

     # Younger
    elif parent.compare_ages(path.goal) == 1:
        return ["Father's Younger Sister", "Father's Sister"]

    # Unknown Age
    else:
        return ["Father's Elder Sister", "Father's Younger Sister", "Father's Sister"]


def get_fathers_brother(path):

    parent = path.steps[0].to_node

    # Elder
    if parent.compare_ages(path.goal) == -1:
        return ["Father's Elder Brother", "Father's Brother"]

     # Younger
    elif parent.compare_ages(path.goal) == 1:
        return ["Father's Younger Brother", "Father's Brother"]

    # Unknown Age
    else:
        return ["Father's Elder Brother", "Father's Younger Brother", "Father's Brother"]


def get_siblings_wife(path):

    sibling =path.steps[1].to_node

    # Elder sibling
    if path.start.compare_ages(sibling) == -1:
        return ["Elder Sibling's Wife"]

    # Younger
    elif path.start.compare_ages(sibling) == 1:
        return ["Younger Sibling's Wife"]

    # Unknown Age
    else:
        return ["Elder Sibling's Wife", "Younger Sibling's Wife"]


def get_siblings_husband(path):

    sibling = path.steps[1].to_node

    # Elder sibling
    if path.start.compare_ages(sibling) == -1:
        return ["Elder Sibling's Husband"]

    # Younger
    elif path.start.compare_ages(sibling) == 1:
        return ["Younger Sibling's Husband"]

    # Unknown Age
    else:
        return ["Elder Sibling's Husband", "Younger Sibling's Husband"]


def get_wifes_sister(path):

    wife = path.steps[0].to_node

    # Elder sister
    if wife.compare_ages(path.goal) == -1:
        return ["Wife's Elder Sister"]

    # Younger
    elif wife.compare_ages(path.goal) == 1:
        return ["Wife's Younger Sister"]

    # Unknown Age
    else:
        return ["Wife's Elder Sister", "Wife's Younger Sister"]


def get_wifes_Brother(path):

    wife = path.steps[0].to_node

    # Elder sister
    if wife.compare_ages(path.goal) == -1:
        return ["Wife's Elder Brother"]

    # Younger
    elif wife.compare_ages(path.goal) == 1:
        return ["Wife's Younger Brother"]

    # Unknown Age
    else:
        return ["Wife's Elder Brother", "Wife's Younger Brother"]

def get_husbands_sister(path):

    husband = path.steps[0].to_node

    # Elder sister
    if husband.compare_ages(path.goal) == -1:
        return ["Husband's Elder Sister"]

    # Younger
    elif husband.compare_ages(path.goal) == 1:
        return ["Husband's Younger Sister"]

    # Unknown Age
    else:
        return ["Husband's Elder Sister", "Husband's Younger Sister"]


def get_husbands_Brother(path):

    husband = path.steps[0].to_node

    # Elder sister
    if husband.compare_ages(path.goal) == -1:
        return ["Husband's Elder Brother"]

    # Younger
    elif husband.compare_ages(path.goal) == 1:
        return ["Husband's Younger Brother"]

    # Unknown Age
    else:
        return ["Husband's Elder Brother", "Husband's Younger Brother"]

