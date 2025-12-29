__all__ = (
    "EXIFileElement",
    "EXIFileContentsElement",
)

from zxptools.type import XMLElementData, XMLElementLike


class EXIFileElement:
    __slots__ = (
        "archive_path",
        "destination",
        "source",
    )

    def __init__(
        self,
        *,
        source: str,
        destination: str,
        archive_path: str | None = None,
    ) -> None:
        self.source = source
        self.destination = destination
        self.archive_path = archive_path

    @classmethod
    def load(cls, xml_element: XMLElementLike) -> "EXIFileElement":
        attrib = xml_element.attrib

        return EXIFileElement(
            source=attrib["source"],
            archive_path=attrib["archive-path"],
            destination=attrib["destination"],
        )

    def dump(self) -> XMLElementData:
        attrib = {
            "source": self.source,
            "destination": self.destination,
        }

        if self.archive_path is not None:
            attrib["archive_path"] = self.archive_path

        return {"attrib": attrib, "tag": "file", "text": None}


class EXIFileContentsElement:
    __slots__ = (
        "archive_path",
        "destination",
        "contents",
    )

    def __init__(
        self,
        *,
        contents: str,
        archive_path: str,
        destination: str,
    ) -> None:
        self.contents = contents
        self.archive_path = archive_path
        self.destination = destination

    # @classmethod
    # def load(
    #     cls, context: Context, xml_element: XMLElementLike
    # ) -> "EXIFileContentsElement":
    #     if (text := xml_element.text) is not None:
    #         contents = text

    #     preprocessor_element = xml_element.find("preprocessor")
    #     if preprocessor_element is not None:
    #         preprocessor_name = preprocessor_element.attrib["name"]
    #         preprocessor = context.get_preprocessor(preprocessor_name)
    #         contents = preprocessor.run(tuple(preprocessor_element))
    #         if isinstance(contents, bytes):
    #             contents = contents.decode()

    #     attrib = xml_element.attrib

    #     return EXIFileContentsElement(
    #         contents=contents,
    #         archive_path=attrib["archive-path"],
    #         destination=attrib["destination"],
    #     )

    @classmethod
    def load(cls, xml_element: XMLElementLike) -> "EXIFileContentsElement":
        attrib = xml_element.attrib

        return EXIFileContentsElement(
            contents=xml_element.text,
            archive_path=attrib["archive-path"],
            destination=attrib["destination"],
        )

    def dump(self) -> XMLElementData:
        return {
            "attrib": {
                "archive-path": self.archive_path,
                "destination": self.destination,
            },
            "tag": "file-contents",
            "text": self.contents,
        }
