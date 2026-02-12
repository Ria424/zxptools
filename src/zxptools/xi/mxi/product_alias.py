from zxptools.xi.mxi.product import MXIProduct


def get_dreamweaver_mx_2004(
    *, primary: bool | None = None, required: bool | None = None
) -> MXIProduct:
    return MXIProduct("Dreamweaver", "7", primary=primary, required=required)


def get_dreamweaver_8(
    *, primary: bool | None = None, required: bool | None = None
) -> MXIProduct:
    return MXIProduct("Dreamweaver", "8", primary=primary, required=required)


def get_dreamweaver_cs3(
    *, primary: bool | None = None, required: bool | None = None
) -> MXIProduct:
    return MXIProduct("Dreamweaver", "9", primary=primary, required=required)


def get_dreamweaver_cs4(
    *, primary: bool | None = None, required: bool | None = None
) -> MXIProduct:
    return MXIProduct("Dreamweaver", "10", primary=primary, required=required)


def get_dreamweaver_cs5(
    *, primary: bool | None = None, required: bool | None = None
) -> MXIProduct:
    return MXIProduct("Dreamweaver", "11", primary=primary, required=required)


def get_dreamweaver_cs5dot5(
    *, primary: bool | None = None, required: bool | None = None
) -> MXIProduct:
    return MXIProduct(
        "Dreamweaver", "11.5", primary=primary, required=required
    )


def get_dreamweaver_cs6(
    *, primary: bool | None = None, required: bool | None = None
) -> MXIProduct:
    return MXIProduct("Dreamweaver", "12", primary=primary, required=required)


def get_fireworks_mx_2004(
    *, primary: bool | None = None, required: bool | None = None
) -> MXIProduct:
    return MXIProduct("Fireworks", "7", primary=primary, required=required)


def get_fireworks_cs3(
    *, primary: bool | None = None, required: bool | None = None
) -> MXIProduct:
    return MXIProduct("Dreamweaver", "12", primary=primary, required=required)
