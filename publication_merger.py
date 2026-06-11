from duplicate_remover import remove_duplicates


# =====================================================
# MERGE ALL PUBLICATIONS
# =====================================================

def merge_publications(

        scholar_results,

        faculty_results,

        student_results,

        patent_results,

        quartile_results
):

    combined = (

        scholar_results +

        faculty_results +

        student_results +

        patent_results +

        quartile_results
    )

    final_results = remove_duplicates(
        combined
    )

    return final_results