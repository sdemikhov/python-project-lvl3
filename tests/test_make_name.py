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

    long_name = 'a' * (core.MAX_FILENAME_LENGTH + 1)
    expected_long = long_name[:core.MAX_FILENAME_LENGTH]
    assert core.make_short_name(long_name, '') == expected_long, (
        "name wrong cutted"
    )

    long_name2 = 'b' * core.MAX_FILENAME_LENGTH
    expected_long2 = (
        long_name2[:(core.MAX_FILENAME_LENGTH) - len(extension)] + extension
    )
    assert core.make_short_name(long_name2, extension) == expected_long2, (
        "name wrong cutted with extension"
    )

    long_extesion = 'c' * core.MAX_FILENAME_LENGTH
    assert core.make_short_name(name, long_extesion) == '', (
        'must return zero-string when long extension'
    )
    assert core.make_short_name(name, long_extesion) == '', (
        'must return zero-string when long extension every time'
    )

    short_name = 'd'
    extesion3 = 'e' * (core.MAX_FILENAME_LENGTH - 1)
    expected3 = short_name + extesion3
    assert core.make_short_name(short_name, extesion3) == expected3, (
        "name don't glued"
    )
    assert core.make_short_name(short_name, extesion3) == '', (
        "must return zero-string, can't cut name for numerate"
    )


def test_make_name_from_url():
    url_http = 'http://www.example.com'
    name_from_http = 'www-example-com'
    assert core.make_name_from_url(url_http) == name_from_http, (
        'must clear schema http://'
    )

    url_https = 'https://www.some-site.com'
    name_from_https = 'www-some-site-com'
    assert core.make_name_from_url(url_https) == name_from_https, (
        'must clear schema https://'
    )

    resource_url = 'https://www.some-site.com/images/logo.svg'
    resource_name = 'www-some-site-com-images-logo.svg'
    assert core.make_name_from_url(
        resource_url,
        search_extension=True
    ) == resource_name, ('must contain file extension')

    resource_url_long_ext = ('https://www.example.com/static/file.' + 
                             'a' * core.MAX_FILENAME_LENGTH)
    resource_name_long_ext = (
        'www-example-com-static-file-' + 'a' * core.MAX_FILENAME_LENGTH
    )[:core.MAX_FILENAME_LENGTH]
    assert core.make_name_from_url(
        resource_url_long_ext,
        search_extension=True
    ) == resource_name_long_ext, ('if long extension, skip search extension')

    url_encoded = (
        'https://ru.example.org/%D0%97%D0%B0%D0%B3%D0' + 
        '%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1' + 
        '%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
    )
    ru_name = 'ru-example-org-Заглавная-страница'
    assert core.make_name_from_url(url_encoded) == ru_name, (
        'must unquote chatacters'
    )
