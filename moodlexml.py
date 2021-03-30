import xml.etree.ElementTree as ET


def createSubElem(elem, tag, attribs=None):
    sub_elem = ET.SubElement(elem, tag)
    if attribs != None:
        for k, v in attribs.items():
            sub_elem.set(k, v)

    return sub_elem


def createSubElemWithText(elem, tag, attribs, text_str=None):
    sub_elem = createSubElem(elem, tag, attribs)
    text_elem = ET.SubElement(sub_elem, "text")
    if text_str != None:
        text_elem.text = text_str

    return sub_elem


def createSubElemWithVal(elem, tag, val):
    sub_elem = createSubElem(elem, tag)
    sub_elem.text = val


def createSubElems(elem, tags, formats, text_strs, vals):
    for t in tags:
        if t in formats:
            attrib = {"format": formats[t]}
            _ = createSubElemWithText(elem, t, attrib, text_strs[t])
        elif t in vals:
            createSubElemWithVal(elem, t, vals[t])
        else:
            createSubElem(elem, t)


def putCD(s):
    return "<![CDATA[" + s + "]]>"


class MoodleElement(ET.Element):
    pass


class Quiz(MoodleElement):
    """Quiz element to populate with moodle categories and questions"""
    def __init__(self):
        """Create quiz element"""
        MoodleElement.__init__(self, "quiz")


class Category(MoodleElement):
    """Dummy question with category type to specify a moodle category"""
    def __init__(self, name):
        """Create question element of category type"""
        MoodleElement.__init__(self, "question")
        self.set("type", "category")

        # Create category elem with text subelem with category name
        text_str = "$course$/top/" + name
        cat_att = {"format": "plain_text"}
        _ = createSubElemWithText(self, "category", cat_att, text_str)

        # Create info element with (empty) text subelem
        info_att = {"format": "html"}
        _ = createSubElemWithText(self, "info", info_att)

        # Create idnumber element
        createSubElem(self, "idnumber")


class Question(MoodleElement):
    """Question without type with tags common to all questions"""
    def __init__(self, name, text):
        """Create question element without type"""
        MoodleElement.__init__(self, "question")

        # List of tags to create
        tags = ["name", "questiontext", "generalfeedback",
                "defaultgrade", "penalty", "hidden", "idnumber"]

        # Dicts of tags that contain <text>
        plain, html = "plain_text", "html"
        formats = {"name": plain, "questiontext": html,
                "generalfeedback": html}
        text_strs = {"name": putCD(name), "questiontext": putCD(text),
                "generalfeedback": ""}

        # Dict of tags that do not contain <text> and their contents
        vals = {"defaultgrade": "1", "penalty": "0.3333333",
                "hidden": "0", "idnumber": ""}

        # Create tags specified above
        createSubElems(self, tags, formats, text_strs, vals)


class Multichoice(Question):
    """Multichoice question with its standard tags"""
    def __init__(self, name, text, answers):
        """Create question element of multichoice type"""
        Question.__init__(self, name, text)
        self.set("type", "multichoice")

        # List of additional tags to create
        tags = ["single", "shuffleanswers", "answernumbering",
                "correctfeedback", "partiallycorrectfeedback",
                "incorrectfeedback", "shownumcorrect"]

        # Dicts of tags that contain <text>
        plain, html = "plain_text", "html"
        formats = {"correctfeedback": html,
                "partiallycorrectfeedback": html,
                "incorrectfeedback": html}
        text_strs = {"correctfeedback":
            putCD("<p>Sua resposta está correta.</p>"),
            "partiallycorrectfeedback":
            putCD("<p>Sua resposta está parcialmente correta.</p>"),
            "incorrectfeedback":
            putCD("<p>Sua resposta está incorreta.</p>")}

        # Dict of tags that do not contain <text> and their contents
        vals = {"single": "true", "shuffleanswers": "true",
                "answernumbering": "abc", "shownumcorrect": ""}

        # Create tags specified above
        createSubElems(self, tags, formats, text_strs, vals)

        for a in answers:
            ans_att = {"fraction": a[0], "format": "html"}
            ans_str = putCD(a[1])
            ans_elem = createSubElemWithText(self, "answer", ans_att,
                    ans_str)
            fb_att = {"format": "html"}
            _ = createSubElemWithText(ans_elem, "feedback", fb_att)
