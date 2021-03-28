import xml.etree.ElementTree as ET


def createSubElem(elem, tag, attrib=None):
    sub_elem = ET.SubElement(elem, tag)
    if attrib != None:
        for k, v in attrib.items():
            sub_elem.set(k, v)

    return sub_elem


def createSubElemWithText(elem, tag, attrib, text_str=None):
    sub_elem = createSubElem(elem, tag, attrib)
    text_elem = ET.SubElement(sub_elem, "text")
    if text_str != None:
        text_elem.text = text_str

    return sub_elem


def createSubElemWithVal(elem, tag, tag_val):
    sub_elem = createSubElem(elem, tag)
    sub_elem.text = tag_val


def createSubElems(elem, tags, format_attribs, text_strs, tag_vals):
    for tag in tags:
        if tag in format_attribs:
            format_att = {"format": format_attribs[tag]}
            _ = createSubElemWithText(elem, tag, format_att,
                    text_strs[tag])
        elif tag in tag_vals:
            createSubElemWithVal(elem, tag, tag_vals[tag])
        else:
            createSubElem(elem, tag)


class MoodleElement(ET.Element):
    pass


class Quiz(MoodleElement):
    """quiz element to populate with moodle categories and questions"""
    def __init__(self):
        """Create quiz element"""
        MoodleElement.__init__(self, "quiz")


class Category(MoodleElement):
    """Dummy question with category type to specify a moodle category"""
    def __init__(self, cat_name="Categoria sem nome"):
        """Create question element of category type"""
        MoodleElement.__init__(self, "question")
        self.set("type", "category")

        # Create category elem with text subelem with category_path
        text_str = "$course$/top/" + cat_name
        cat_att = {"format": "plain_text"}
        _ = createSubElemWithText(self, "category", cat_att, text_str)
        info_att = {"format": "html"}
        _ = createSubElemWithText(self, "info", info_att)
        createSubElem(self, "idnumber")


class Question(MoodleElement):
    """Question without type with tags common to all questions"""
    def __init__(self, qname="Nome da questão",
                qtext="<![CDATA[<p>Texto da questão</p>]]>"):
        """Create question element without type"""
        MoodleElement.__init__(self, "question")

        # List of tags to create
        tags = ["name", "questiontext", "generalfeedback",
                "defaultgrade", "penalty", "hidden", "idnumber"]

        # Dicts of tags that contain <text>
        plain, html = "plain_text", "html"
        format_attribs = {"name": plain, "questiontext": html,
                "generalfeedback": html}
        text_strs = {"name": qname, "questiontext": qtext,
                "generalfeedback": ""}

        # Dict of tags that do not contain <text> and their contents
        tag_vals = {"defaultgrade": "1", "penalty": "0.3333333",
                "hidden": "0", "idnumber": ""}

        # Create tags specified above
        createSubElems(self, tags, format_attribs, text_strs, tag_vals)


class Multichoice(Question):
    """Multichoice question with its standard tags"""
    def __init__(self, qname="Nome da questão",
                qtext="<![CDATA[<p>Texto da questão</p>]]>"):
        """Create question element of multichoice type"""
        Question.__init__(self, qname, qtext)
        self.set("type", "multichoice")

        # List of additional tags to create
        tags = ["single", "shuffleanswers", "answernumbering",
                "correctfeedback", "partiallycorrectfeedback",
                "incorrectfeedback", "shownumcorrect"]

        # Dicts of tags that contain <text>
        plain, html = "plain_text", "html"
        format_attribs = {"correctfeedback": html,
                "partiallycorrectfeedback": html,
                "incorrectfeedback": html}
        text_strs = {"correctfeedback":
                "<![CDATA[<p>Sua resposta está correta.</p>]]>",
                "partiallycorrectfeedback":
                "<![CDATA[<p>Sua resposta está parcialmente correta.</p>]]>",
                "incorrectfeedback":
                "<![CDATA[<p>Sua resposta está incorreta.</p>]]>"}

        # Dict of tags that do not contain <text> and their contents
        tag_vals = {"single": "true", "shuffleanswers": "true",
                "answernumbering": "abc", "shownumcorrect": ""}

        # Create tags specified above
        createSubElems(self, tags, format_attribs, text_strs, tag_vals)

        for i in range(2):
            ans_att = {"fraction": "0", "format": "html"}
            ans_str = "<![CDATA[<p>Texto da resposta</p>]]>"
            ans_elem = createSubElemWithText(self, "answer", ans_att, ans_str)
            fb_att = {"format": "html"}
            _ = createSubElemWithText(ans_elem, "feedback", fb_att)
