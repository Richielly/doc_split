from rank_bm25 import BM25Okapi, BM25Plus
class DocumentRank:

    def rank_manager(self, ensemble, question):
        list_resp=[]
        for resp_2 in ensemble:
            list_resp.append(resp_2.page_content)

        tokenized_list_resp = [doc.split(" ") for doc in list_resp]

        bm25 = BM25Plus(tokenized_list_resp)

        tokenized_question = question.split(" ")

        # doc_scores = bm25.get_scores(tokenized_question)
        # print("-------------")
        # print(doc_scores)

        resp_rank=bm25.get_top_n(tokenized_question, list_resp, n=4)

        # for resp_3 in resp_rank:
        #     print("-------------")
        #     print(resp_3)

        return resp_rank
