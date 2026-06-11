from serpapi import GoogleSearch
import pprint

# =====================================================
# SERPAPI KEY
# =====================================================

API_KEY = "cd9fbf593d4ac6adb49007ea5438614eff594fb3be7e20298c8ece041a068212"

# =====================================================
# FETCH SCHOLAR DATA
# =====================================================

def fetch_scholar_data(author_id):

    try:

        print(
            "\n========== SCHOLAR FETCH ==========\n"
        )

        print(
            "AUTHOR ID:",
            author_id
        )

        params = {

            "engine":
                "google_scholar_author",

            "author_id":
                author_id,

            "api_key":
                API_KEY
        }

        search = GoogleSearch(
            params
        )

        results = search.get_dict()

        # ============================================
        # NEW DEBUG BLOCK
        # ============================================

        print(
            "\n========== KEYS FOUND ==========\n"
        )

        print(
            results.keys()
        )

        print(
            "\n========== FULL RESPONSE ==========\n"
        )

        pprint.pp(results)

        # ============================================
        # AUTHOR BLOCK
        # ============================================

        author = results.get(
            "author",
            {}
        )

        print(
            "\nAUTHOR BLOCK:\n"
        )

        pprint.pp(author)

        name = author.get(
            "name",
            ""
        )

        affiliation = author.get(
            "affiliations",
            ""
        )

        # ============================================
        # METRICS
        # ============================================

        total_citations = 0
        h_index = 0
        i10_index = 0

        cited_by = results.get(
            "cited_by",
            {}
        )

        print(
            "\nCITED BY BLOCK:\n"
        )

        pprint.pp(cited_by)

        try:

            table = cited_by.get(
                "table",
                []
            )

            if len(table) >= 1:

                total_citations = int(

                    table[0]

                    .get(
                        "citations",
                        {}
                    )

                    .get(
                        "all",
                        0
                    )
                )

            if len(table) >= 2:

                h_index = int(

                    table[1]

                    .get(
                        "h_index",
                        {}
                    )

                    .get(
                        "all",
                        0
                    )
                )

            if len(table) >= 3:

                i10_index = int(

                    table[2]

                    .get(
                        "i10_index",
                        {}
                    )

                    .get(
                        "all",
                        0
                    )
                )

        except Exception as metric_error:

            print(
                "\nMETRIC ERROR:",
                metric_error
            )

        # ============================================
        # ARTICLES
        # ============================================

        articles = results.get(
            "articles",
            []
            
        )

        print(
            "\nARTICLES COUNT:",
            len(articles)
        )

        publications = []

        for article in articles:

            publications.append({

                "title":
                    article.get(
                        "title",
                        ""
                    ),

                "authors":
                    article.get(
                        "authors",
                        ""
                    ),

                "year":
                    article.get(
                        "year",
                        ""
                    ),

                "link":
                    article.get(
                        "link",
                        ""
                    ),

                "publication":
                    article.get(
                        "publication",
                        ""
                    ),

                "citations":

                    article.get(
                        "cited_by",
                        {}
                    ).get(
                        "value",
                        0
                    )
            })

        # ============================================
        # FINAL RESPONSE
        # ============================================

        return {

            "name":
                name,

            "affiliation":
                affiliation,

            "citations":
                total_citations,

            "h_index":
                h_index,

            "i10_index":
                i10_index,

            "publications":
                publications
        }

    except Exception as e:

        print(
            "\nSCHOLAR ENGINE ERROR:\n",
            e
        )

        return {

            "name": "",

            "affiliation": "",

            "citations": 0,

            "h_index": 0,

            "i10_index": 0,

            "publications": []
        }