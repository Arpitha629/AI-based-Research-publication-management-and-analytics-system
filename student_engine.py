import pandas as pd


# =====================================================
# STUDENT IEEE DATABASE
# =====================================================

student_profiles = {

    "Sagari S M": {

        "ieee_id":
            "411442439492329"
    },

    "Aditya N Awati": {

        "ieee_id":
            "304548071212451"
    },

    "Nishank Satish": {

        "ieee_id":
            "37086080161"
    },

    "Kausthub Kannan": {

        "ieee_id":
            "523684549523892"
    },

    "Smruthi S Rao": {

        "ieee_id":
            "127616408222812"
    }
}


# =====================================================
# REMOVE DUPLICATES
# =====================================================

def remove_duplicates(publications):

    unique_titles = set()

    cleaned = []

    for paper in publications:

        title = (
            paper["title"]
            .strip()
            .lower()
        )

        if title not in unique_titles:

            unique_titles.add(title)

            cleaned.append(paper)

    return cleaned


# =====================================================
# SEARCH STUDENT PUBLICATIONS
# =====================================================

def get_student_publications(search_query):

    file_path = (
        "backend/data/Student publication 2021 to 2026.xlsx"
    )

    df = pd.read_excel(file_path)

    results = []

    ieee_id = ""

    matched_student = ""

    # =================================================
    # FIND MATCHED STUDENT
    # =================================================

    for student_name, data in student_profiles.items():

        if search_query.lower() in student_name.lower():

            matched_student = student_name

            ieee_id = data.get(
                "ieee_id",
                ""
            )

            break

    # =================================================
    # SEARCH EXCEL DATA
    # =================================================

    for _, row in df.iterrows():

        title = str(
            row.get(
                "Paper Title",
                ""
            )
        )

        authors = str(
            row.get(
                "Authors",
                ""
            )
        )

        keywords = str(
            row.get(
                "Keywords",
                ""
            )
        )

        if (

                search_query.lower()
                in authors.lower()

                or

                search_query.lower()
                in title.lower()

                or

                search_query.lower()
                in keywords.lower()
        ):

            results.append({

                "title":
                    title,

                "authors":
                    authors,

                "journal":
                    row.get(
                        "Journal",
                        ""
                    ),

                "year":
                    str(
                        row.get(
                            "Year",
                            ""
                        )
                    ),

                "department":
                    row.get(
                        "Department",
                        ""
                    ),

                "guide":
                    row.get(
                        "Guide",
                        ""
                    ),

                "doi":
                    row.get(
                        "DOI",
                        ""
                    ),

                "keywords":
                    keywords
            })

    # =================================================
    # REMOVE DUPLICATES
    # =================================================

    results = remove_duplicates(results)

    # =================================================
    # ANALYTICS
    # =================================================

    publication_count = len(results)

    yearly_counts = {}

    for paper in results:

        year = paper["year"]

        if year not in yearly_counts:

            yearly_counts[year] = 0

        yearly_counts[year] += 1

    # =================================================
    # RETURN DATA
    # =================================================

    return {

        "student":
            matched_student,

        "ieee_id":
            ieee_id,

        "ieee_profile":
            f"https://ieeexplore.ieee.org/author/{ieee_id}",

        "total_publications":
            publication_count,

        "yearly_counts":
            yearly_counts,

        "results":
            results
    }