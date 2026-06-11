import pandas as pd
import re

# =====================================================
# LOAD EXCEL DATASETS
# =====================================================

faculty_df = pd.read_excel(
    "backend/data/clean_publications.xlsx"
)

student_df = pd.read_excel(
    "backend/data/Student publication 2021 to 2026.xlsx"
)

quartile_df = pd.read_excel(
    "backend/data/q1 to q4 year 2021 to 2026.xlsx"
)

patent_df = pd.read_excel(
    "backend/data/patents2021 to 2026.xlsx"
)

faculty_df.columns = faculty_df.columns.str.strip()

student_df.columns = student_df.columns.str.strip()

# =====================================================
# FIX COLUMN ISSUE
# =====================================================

if "Remrks" in student_df.columns:

    student_df.rename(

        columns={

            "Remrks":
                "Remarks"

        },

        inplace=True
    )

# =====================================================
# YEAR EXTRACTION
# =====================================================

def extract_year(text):

    text = str(text)

    match = re.search(

        r"(20\d{2})",

        text
    )

    if match:

        return int(

            match.group(1)
        )

    return None

# =====================================================
# FACULTY YEARS
# =====================================================

faculty_years = []

if "Remarks" in faculty_df.columns:

    for remark in faculty_df["Remarks"]:

        year = extract_year(
            remark
        )

        if year:

            faculty_years.append(
                year
            )

faculty_year_df = pd.DataFrame({

    "Year":
        faculty_years
})

# =====================================================
# STUDENT YEARS
# =====================================================

student_years = []

if "Remarks" in student_df.columns:

    for remark in student_df["Remarks"]:

        year = extract_year(
            remark
        )

        if year:

            student_years.append(
                year
            )

student_year_df = pd.DataFrame({

    "Year":
        student_years
})

# =====================================================
# FACULTY ANALYTICS
# =====================================================

def get_faculty_analytics():

    yearly = (

        faculty_year_df["Year"]

        .value_counts()

        .sort_index()
    )

    return {

        "years":
            yearly.index.tolist(),

        "counts":
            yearly.values.tolist()
    }

# =====================================================
# STUDENT ANALYTICS
# =====================================================

def get_student_analytics():

    yearly = (

        student_year_df["Year"]

        .value_counts()

        .sort_index()
    )

    return {

        "years":
            yearly.index.tolist(),

        "counts":
            yearly.values.tolist()
    }

# =====================================================
# QUARTILE ANALYTICS
# =====================================================

def get_quartile_analytics():

    return quartile_df.to_dict(

        orient="records"
    )

# =====================================================
# PATENT ANALYTICS
# =====================================================

def get_patent_analytics():

    return patent_df.to_dict(

        orient="records"
    )

# =====================================================
# TOP FACULTY AUTHORS
# =====================================================

def get_top_faculty_authors():

    authors = faculty_df[

        "Name of the Author/s"

    ].dropna()

    names = []

    for row in authors:

        split_names = str(
            row
        ).split(",")

        for name in split_names:

            name = name.strip()

            if len(name) > 3:

                names.append(
                    name
                )

    author_series = pd.Series(
        names
    )

    top = (

        author_series

        .value_counts()

        .head(10)
    )

    return {

        "authors":
            top.index.tolist(),

        "counts":
            top.values.tolist()
    }

# =====================================================
# TOP STUDENTS
# =====================================================

def get_top_students():

    authors = student_df[

        "Name of the Author/s"

    ].dropna()

    names = []

    for row in authors:

        split_names = str(
            row
        ).split(",")

        for name in split_names:

            name = name.strip()

            if len(name) > 3:

                names.append(
                    name
                )

    author_series = pd.Series(
        names
    )

    top = (

        author_series

        .value_counts()

        .head(10)
    )

    return {

        "students":
            top.index.tolist(),

        "counts":
            top.values.tolist()
    }

# =====================================================
# DASHBOARD GENERATOR
# =====================================================

def generate_dashboard(data):

    dashboard = {

        "faculty_name":

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

            data.get(
                "analytics",
                {}
            ),

        "publications":

            data.get(
                "results",
                []
            ),

        "faculty_chart":

            get_faculty_analytics(),

        "student_chart":

            get_student_analytics(),

        "quartiles":

            get_quartile_analytics(),

        "patents":

            get_patent_analytics(),

        "top_faculty":

            get_top_faculty_authors(),

        "top_students":

            get_top_students()
    }

    return dashboard