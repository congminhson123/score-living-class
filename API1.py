from elasticsearch import Elasticsearch

class user:
    def __init__(self, id):
        self.id = id
    infor = ''
    list_page = []
    list_group = []
    list_post = []
    list_pageId = []
    list_groupId = []

    es = Elasticsearch("http://103.74.122.196:9200")

    def get_user(self):
        res = self.es.search(index="dsminer_user_core", body={
            "query": {
                "match_phrase": {
                    "_id": self.id
                }
            },
        })
        self.infor = res["hits"]["hits"][0]['_source']
        try:
            self.list_pageId = res["hits"]["hits"][0]['_source']["pages"]
        except KeyError:
            self.list_pageId = []
        try:
            self.list_groupId = res["hits"]["hits"][0]['_source']["groups"]
        except KeyError:
            self.list_groupId = []

    def get_infor_page(self):
        self.get_user()
        for id in self.list_pageId:
            res = self.es.search(index="dsminer_page", body={
                "query": {
                    "match_phrase": {
                        "_id": id
                    }
                },
            })
            if res["hits"]["hits"] != []:
                self.list_page.append(res["hits"]["hits"][0]["_source"])

    def get_infor_group(self):
        self.get_user()
        for id in self.list_groupId:
            res = self.es.search(index="dsminer_group", body={
                "query": {
                    "match_phrase": {
                        "_id": id
                    }
                },
            })
            if res["hits"]["hits"] != []:
                self.list_group.append(res["hits"]["hits"][0]["_source"])

    def get_post(self):
        time_sleep = 2
        body = {
            'size': 10000,
            'query': {
                'bool': {
                    'must': [
                        {'bool': {
                            'should': [
                                {'match_phrase': {'userId': self.id}},
                            ]
                        }},
                        {'match_phrase': {
                            'docType': 'user_post'
                        }}
                    ]
                }
            },
            'track_total_hits': True,
            '_source': [
                'description',
                "message"
            ]
        }
        for month in range(8, 10):
            month = f'{month:02d}'
            for i in range(1, 31):
                day = i
                day = f'{day:02d}'
                index = f'dsminer_post_2021-{month}-{day}'
                try:
                    response = self.es.search(index=index, body=body)['hits']['hits']
                    for res in response:
                        self.list_post.append(res["_source"])
                except:
                    continue

    def get_all(self):
        self.get_post()
        self.get_infor_group()
        self.get_infor_page()
        user = {
            # to??n b??? th??ng tin ng?????i d??ng trong dsminer_user_core
            "infor": self.infor,
            # to??n b??? th??ng tin group c???a user
            "infor_group": self.list_group,
            # to??n b??? th??ng tin page c???a user
            "infor_page": self.list_page,
            # to??n b??? th??ng tin post trong v??ng 1 th??ng c???a user
            "infor_post": self.list_post
        }
        return user