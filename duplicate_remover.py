# =====================================================
# REMOVE DUPLICATE PUBLICATIONS
# =====================================================

def remove_duplicates(publications):

    unique_titles = set()

    final_results = []

    for paper in publications:

        title = str(
            paper.get(
                "Title",
                ""
            )
        ).lower().strip()

        title = (
            title
            .replace(".", "")
            .replace(",", "")
            .replace("-", "")
            .replace(":", "")
        )

        if title == "":
            continue

        if title not in unique_titles:

            unique_titles.add(title)

            final_results.append(paper)

    return final_results