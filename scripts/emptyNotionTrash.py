'''
Requirements:
beautifulsoup4>=4.7.1
bs4>=0.0.1
cached-property>=1.5.1
certifi>=2019.6.16
chardet>=3.0.4
commonmark>=0.9.0
dictdiffer>=0.8.0
future>=0.17.1
idna>=2.8
notion>=0.0.23
python-slugify>=3.0.2
pytz>=2019.1
requests>=2.22.0
soupsieve>=1.9.2
text-unidecode>=1.2
tzlocal>=1.5.1
urllib3>=1.25.3
'''
# unverified

from notion.client import NotionClient

def get_trash(client):
    query = {
              "type": "BlocksInSpace",
              "query": "",
              "filters": {
                "isDeletedOnly": True,
                "excludeTemplates": False,
                "isNavigableOnly": True,
                "requireEditPermissions": False,
                "ancestors": [],
                "createdBy": [],
                "editedBy": [],
                "lastEditedTime": {},
                "createdTime": {}
              },
              "sort": "Relevance",
              "limit": 1000,
              "spaceId": client.current_space.id,
              "source": "trash"
            }
    results = client.post('/api/v3/search', query)
    block_ids = results.json()['results']

    return [block_id['id'] for block_id in block_ids]


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def delete_permanently(client, block_ids):
    for block_batch in chunks(block_ids, 10):
        try:
            client.post("deleteBlocks", {"blockIds": block_batch, "permanentlyDelete": True})
        except Exception as err:
            print(err)
            print(block_batch)


if __name__== "__main__":
    token = input('Please enter your auth token: ')
    client = NotionClient(token_v2=token)

    block_ids = get_trash(client)
    delete_permanently(client, block_ids)
    print('Successfully cleared all trash blocks.')