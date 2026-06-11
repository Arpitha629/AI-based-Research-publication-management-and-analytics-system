import pandas as pd
import requests
import re
import json

from analytics import generate_analytics
from orcid_engine import get_orcid_profile
from scholar_engine import fetch_scholar_data

# =====================================================
# SERP API KEY
# =====================================================

SERP_API_KEY = "cd9fbf593d4ac6adb49007ea5438614eff594fb3be7e20298c8ece041a068212"

# =====================================================
# LOAD FACULTY DATABASE
# =====================================================

FACULTY_JSON_PATH = (
    "backend/data/faculty_ids.json"
)

with open(
        FACULTY_JSON_PATH,
        "r",
        encoding="utf-8"
) as file:

    faculty_profiles = json.load(file)

# =====================================================
# LOAD EXCEL FILES
# =====================================================

faculty_excel = pd.read_excel(
    "backend/data/clean_publications.xlsx"
)

student_excel = pd.read_excel(
    "backend/data/Student publication 2021 to 2026.xlsx"
)

patent_excel = pd.read_excel(
    "backend/data/patents2021 to 2026.xlsx"
)

quartile_excel = pd.read_excel(
    "backend/data/q1 to q4 year 2021 to 2026.xlsx"
)

faculty_excel.fillna("", inplace=True)
student_excel.fillna("", inplace=True)
patent_excel.fillna("", inplace=True)
quartile_excel.fillna("", inplace=True)

# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    text = str(text).lower()

    text = re.sub(
        r'[^a-z0-9 ]',
        '',
        text
    )

    return text

# =====================================================
# REMOVE DUPLICATES
# =====================================================

def remove_duplicates(items):

    final_results = []

    seen_titles = set()

    for item in items:

        title = str(
            item.get(
                "Title",
                ""
            )
        ).lower().strip()

        title = (
            title
            .replace("-", "")
            .replace(",", "")
            .replace(".", "")
            .replace(":", "")
        )

        if title == "":
            continue

        if title in seen_titles:
            continue

        seen_titles.add(title)

        final_results.append(item)

    return final_results

# =====================================================
# SEARCH DATAFRAME
# =====================================================

def search_dataframe(df, query, source):

    results = []

    query = clean_text(query)

    for _, row in df.iterrows():

        row_text = clean_text(

            " ".join(
                row.astype(str)
            )
        )

        if query in row_text:

            item = row.to_dict()

            # Extract year from Remarks column

            remarks = str(
                item.get(
                    "Remarks",
                    ""
                )
            )

            year_match = re.search(
                r"(20\d{2})",
                remarks
            )

            if year_match:

                item["Year"] = (
                    year_match.group(1)
                )

            else:

                item["Year"] = ""

            item["source"] = source

            results.append(
                item
            )

    return results

# =====================================================
# SAVE NEW FACULTY
# =====================================================

def save_new_faculty(profile):

    try:

        faculty_profiles.append(profile)

        with open(
                FACULTY_JSON_PATH,
                "w",
                encoding="utf-8"
        ) as file:

            json.dump(
                faculty_profiles,
                file,
                indent=4
            )

    except Exception as e:

        print(
            "Save Faculty Error:",
            e
        )

# =====================================================
# AUTHOR SEARCH
# =====================================================

# =====================================================
# AUTHOR SEARCH
# =====================================================

def get_authors(query):

    authors = []

    query = query.lower().strip()

    for faculty in faculty_profiles:

        if (
            query in faculty.get("name", "").lower()
            or query in faculty.get("orcid", "").lower()
            or query in faculty.get("scopus_id", "").lower()
            or query in faculty.get("ieee_id", "").lower()
            or query in faculty.get("researchgate_id", "").lower()
        ):

            orcid_data = get_orcid_profile(
                faculty.get("orcid", "")
            )

            affiliation = orcid_data.get(
                "affiliation",
                ""
            )

            if affiliation == "":
                affiliation = faculty.get(
                    "college",
                    ""
                )

            authors.append({

                "name":
                    faculty.get("name", ""),

                "affiliation":
                    affiliation,

                "department":
                    orcid_data.get(
                        "department",
                        ""
                    ),

                "biography":
                    orcid_data.get(
                        "biography",
                        ""
                    ),

                "author_id":
                    faculty.get(
                        "scholar_id",
                        ""
                    ),

                "orcid":
                    faculty.get(
                        "orcid",
                        ""
                    )
            })

    return authors




# =====================================================
# FETCH PUBLICATIONS
# =====================================================

# =====================================================
# FETCH PUBLICATIONS
# =====================================================

def get_publications(author_id):

    try:

        print(
            "\n========== CALLING SCHOLAR ENGINE ==========\n"
        )

        data = fetch_scholar_data(
            author_id
        )

        publications = []

        for paper in data.get(
            "publications",
            []
        ):

            publications.append({

                "Title":
                    paper.get(
                        "title",
                        ""
                    ),

                "Authors":
                    paper.get(
                        "authors",
                        ""
                    ),

                "Year":
                    paper.get(
                        "year",
                        ""
                    ),

                "Link":
                    paper.get(
                        "link",
                        ""
                    ),

                "Citations":
                    paper.get(
                        "citations",
                        0
                    ),

                "source":
                    "Google Scholar"
            })

        # ==========================================
        # REMOVE DUPLICATES
        # ==========================================

        publications = remove_duplicates(
            publications
        )

        # ==========================================
        # ANALYTICS
        # ==========================================

        analytics = generate_analytics(
            publications
        )

        # ==========================================
        # FINAL RETURN
        # ==========================================

        return {

            "name":
                data.get(
                    "name",
                    ""
                ),

            "affiliation":
                data.get(
                    "affiliation",
                    ""
                ),

            "citations":
                data.get(
                    "citations",
                    0
                ),

            "h_index":
                data.get(
                    "h_index",
                    0
                ),

            "i10_index":
                data.get(
                    "i10_index",
                    0
                ),

            "analytics":
                analytics,

            "results":
                publications,

            "total_publications":
                len(
                    publications
                )
        }

    except Exception as e:

        print(
            "\nSEARCH ENGINE ERROR:\n",
            e
        )

        return {

            "name":"",

            "affiliation":"",

            "citations":0,

            "h_index":0,

            "i10_index":0,

            "analytics":{},

            "results":[],

            "total_publications":0
        }

# =====================================================
# UNIVERSAL SEARCH
# =====================================================

def universal_search(query):

    faculty_results = search_dataframe(
        faculty_excel,
        query,
        "Faculty Publication"
    )

    student_results = search_dataframe(
        student_excel,
        query,
        "Student Publication"
    )

    patent_results = search_dataframe(
        patent_excel,
        query,
        "Patent"
    )

    quartile_results = search_dataframe(
        quartile_excel,
        query,
        "Quartile"
    )

    combined = (

        faculty_results +

        student_results +

        patent_results +

        quartile_results
    )

    analytics = generate_analytics(
    combined
)

    return {

    "query":
        query,

    "total_results":
        len(combined),

    "analytics":
        analytics,

    "results":
        combined
}

if __name__ == "__main__":

    result = universal_search("cloud")

    print("\nFINAL RESULT:\n")

    print(result)