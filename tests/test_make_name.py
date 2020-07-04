from page_loader import core


def test_make_short_name():
    name = 'not_so_long_name'
    extension = '.svg'
    assert core.make_short_name(name, extension) == name + extension, (
        "name don't glued"
    )
    assert core.make_short_name(name, extension) == name + str(1) + extension, (
        "name don't numerated"
    )
    assert core.make_short_name(name, extension) == name + str(2) + extension, (
        "name wrong numerated"
    )

    long_name = 'a' * 300
    expected_long = long_name[:core.MAX_FILENAME_LENGTH]
    assert core.make_short_name(long_name, '') == expected_long, (
        "name wrong cutted"
    )

    long_name2 = 'b' * 300
    expected_long2 = (
        long_name2[:(core.MAX_FILENAME_LENGTH) - len(extension)] + extension
    )
    assert core.make_short_name(long_name2, extension) == expected_long2, (
        "name wrong cutted with extension"
    )

    long_extesion = 'c' * 300
    assert core.make_short_name(name, long_extesion) == '', (
        'must return zero-string when long extension'
    )
    assert core.make_short_name(name, long_extesion) == '', (
        'must return zero-string when long extension every time'
    )

    short_name = 'd'
    long_extesion3 = 'e' * 254
    expected_long3 = short_name + long_extesion3
    assert core.make_short_name(short_name, long_extesion3) == expected_long3, (
        "name don't glued"
    )
    assert core.make_short_name(short_name, long_extesion3) == '', (
        "must return zero-string, can't cut name for numerate"
    )
