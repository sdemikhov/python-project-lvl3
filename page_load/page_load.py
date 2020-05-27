import requests


from page_load.tree import (
    make_tree, FILENAME, RESOURCES, RESOURCES_DIR, CONTENT
)
from page_load import file


def page_loader(target_url, destination=None):
    response = send_request(target_url)
    tree = make_tree(response)

    path = file.make_dir(destination)
    with open(path / tree[FILENAME], 'w') as page:
        page.write(tree[CONTENT])
    if tree[RESOURCES]:
        resources_path = file.make_dir(path / tree[RESOURCES_DIR])
        for filename, url_ in tree[RESOURCES]:
            resource_response = send_request(url_)
            with open(resources_path / filename, 'w') as resource:
                resource.write(resource_response.text)


MESSAGE_TEMPATE = "File '{url}' wasn't downloaded! Response code '{code}'"


def send_request(url):
    response = requests.get(url)
    if response.ok:
        return response
    else:
        raise ValueError(
            MESSAGE_TEMPATE.format(url=url, code=response.status_code)
        )
