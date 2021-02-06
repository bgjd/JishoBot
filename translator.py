import requests


class Jisho:
    search_url_base = "https://jisho.org/api/v1/search/words?keyword="

    def __init__(self, logger=None):
        self.logger = logger

    def log(self, log_msg, log_level='INFO'):
        if self.logger:
            if log_level == 'WARN':
                self.logger.warn(log_msg)
            else:
                self.logger.info(log_msg)
        else:
            print(log_msg)

    def get_status(self, json_resp):
        return json_resp["meta"]["status"]

    def get_definition(self, json_resp):
        try:
            data_0 = json_resp["data"][0]
        except:
            return "Definition not found"

        ret = ""
        try:
            ret += data_0["japanese"][0]["word"] + " - "
        except KeyError:
            pass

        try:
            ret += data_0["japanese"][0]["reading"]
        except KeyError:
            pass

        for definition in data_0["senses"][0]["english_definitions"]:
            ret += " - " + definition

        return ret

    def translate(self, word):
        msg = ""

        try:
            response = requests.get(self.search_url_base + word).json()
            status_code = self.get_status(response)

            if status_code != 200:
                self.log("Query failed http code: " + status_code, 'WARN')
                raise requests.HTTPError(
                    "API returned non-200 status code:" + status_code)

            msg = self.get_definition(response)
        except Exception as e:
            self.log("Translation failed " + str(e), 'WARN')
            msg = "Translation failed, please try again."

        return msg


if __name__ == "__main__":
    test_words = ["japan", '"japan"', "tasty", "green", "baka", "karaoke",
                  " ", ".", "馬鹿", "fdsjjfjsdkfjsdkfjsjlj", "???", "お前", "カラオケ"]
    jisho = Jisho()

    for w in test_words:
        print(jisho.translate(w))
