from collections import Counter


# =====================================================
# GENERATE ANALYTICS
# =====================================================

def generate_analytics(results):

    # =============================================
    # BASIC COUNTS
    # =============================================

    total_publications = len(results)

    total_citations = 0

    # =============================================
    # COUNTERS
    # =============================================

    year_distribution = Counter()

    source_distribution = Counter()

    faculty_distribution = Counter()

    citation_distribution = Counter()

    # =============================================
    # PROCESS EACH PUBLICATION
    # =============================================

    for item in results:

        # =========================================
        # CITATIONS
        # =========================================

        try:

            citations = int(

                item.get(
                    "Citations",
                    0
                )
            )

        except:

            citations = 0

        total_citations += citations

        # =========================================
        # YEAR
        # =========================================

        year = str(

            item.get(
                "Year",
                "Unknown"
            )
        ).strip()

        if year == "":

            year = "Unknown"

        year_distribution[year] += 1

        # =========================================
        # SOURCE
        # =========================================

        source = str(

            item.get(
                "source",
                "Unknown"
            )
        ).strip()

        if source == "":

            source = "Unknown"

        source_distribution[source] += 1

        # =========================================
        # AUTHORS
        # =========================================

        authors = str(

            item.get(
                "Authors",
                ""
            )
        )

        for author in authors.split(","):

            author = author.strip()

            if author == "":
                continue

            faculty_distribution[author] += 1

        # =========================================
        # CITATION RANGE ANALYTICS
        # =========================================

        if citations >= 100:

            citation_distribution["100+"] += 1

        elif citations >= 50:

            citation_distribution["50-99"] += 1

        elif citations >= 10:

            citation_distribution["10-49"] += 1

        else:

            citation_distribution["0-9"] += 1

    # =============================================
    # FINAL ANALYTICS JSON
    # =============================================

    return {

        "total_publications":
            total_publications,

        "total_citations":
            total_citations,

        "year_distribution":
            dict(year_distribution),

        "source_distribution":
            dict(source_distribution),

        "faculty_distribution":
            dict(faculty_distribution),

        "citation_distribution":
            dict(citation_distribution)
    }