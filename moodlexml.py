import xml.etree.ElementTree as ET


def createSubElem(elem, tag, attribs=None, text=None):
    sub_elem = ET.SubElement(elem, tag)
    if attribs != None:
        for k, v in attribs.items():
            sub_elem.set(k, v)

    if text != None:
        sub_elem.text = text

    return sub_elem


def createSubElemWithText(elem, tag, attribs=None, text_str=None):
    sub_elem = createSubElem(elem, tag, attribs)
    text_elem = ET.SubElement(sub_elem, "text")
    if text_str != None:
        text_elem.text = text_str

    return sub_elem


def cdata(s):
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

        # Create <category> with <text> containing name
        cat_att = {"format": "plain_text"}
        text_str = "$course$/top/" + name
        _ = createSubElemWithText(self, "category", cat_att, text_str)

        # Create <info> with <text> (empty)
        info_att = {"format": "html"}
        _ = createSubElemWithText(self, "info", info_att)

        # Create <idnumber>
        createSubElem(self, "idnumber")


class Question(MoodleElement):
    """Question without type with tags common to all questions"""
    def __init__(self, name, text):
        """Create question element without type"""
        MoodleElement.__init__(self, "question")

        # Dict of tags that contain <text>
        plain, html = "plain_text", "html"
        texts = {"name": [plain, cdata(name)],
                "questiontext": [html, cdata(text)],
                "generalfeedback": [html, ""]}
        for k, v in texts.items():
            createSubElemWithText(self, k, {"format": v[0]}, v[1])

        # Dict of tags that do not contain <text> and their contents
        vals = {"defaultgrade": "1", "penalty": "0.3333333",
                "hidden": "0", "idnumber": ""}
        for k, v in vals.items():
            createSubElem(self, k, None, v)


class Multichoice(Question):
    """Multichoice question with its standard tags"""
    def __init__(self, name, text, answers):
        """Create question element of multichoice type"""
        Question.__init__(self, name, text)
        self.set("type", "multichoice")

        # Dicts of tags that contain <text>
        plain, html = "plain_text", "html"
        cor_msg = cdata("<p>Your answer is correct.</p>")
        pco_msg = cdata("<p>Your answer is partially correct.</p>")
        inc_msg = cdata("<p>Your answer is incorrect.</p>")
        texts = {"correctfeedback": [html, cor_msg],
                "partiallycorrectfeedback": [html, pco_msg],
                "incorrectfeedback": [html, inc_msg]}
        for k, v in texts.items():
            createSubElemWithText(self, k, {"format": v[0]}, v[1])

        # Dict of tags that do not contain <text> and their contents
        vals = {"single": "true", "shuffleanswers": "true",
                "answernumbering": "abc", "shownumcorrect": ""}
        for k, v in vals.items():
            createSubElem(self, k, None, v)

        for a in answers:
            ans_att = {"fraction": a[0], "format": "html"}
            ans_str = cdata(a[1])
            ans_elem = createSubElemWithText(self, "answer", ans_att,
                    ans_str)
            fb_att = {"format": "html"}
            _ = createSubElemWithText(ans_elem, "feedback", fb_att)
