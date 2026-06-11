import requests


# =====================================================
# FETCH COMPLETE ORCID PROFILE
# =====================================================

def get_orcid_profile(orcid_id):

    try:

        # =============================================
        # EMPTY ORCID CHECK
        # =============================================

        if orcid_id == "":

            return {

                "orcid": "",

                "affiliation": "",

                "department": "",

                "biography": ""
            }

        # =============================================
        # HEADERS
        # =============================================

        headers = {

            "Accept": "application/json"
        }

        # =============================================
        # FETCH EMPLOYMENT DATA
        # =============================================

        employment_url = (
            f"https://pub.orcid.org/v3.0/"
            f"{orcid_id}/employments"
        )

        employment_response = requests.get(

            employment_url,

            headers=headers
        )

        affiliation = ""

        department = ""

        if employment_response.status_code == 200:

            employment_data = (
                employment_response.json()
            )

            employment_summary = (
                employment_data.get(
                    "employment-summary",
                    []
                )
            )

            if len(employment_summary) > 0:

                first_employment = (
                    employment_summary[0]
                )

                organization = (

                    first_employment

                    .get(
                        "organization",
                        {}
                    )

                    .get(
                        "name",
                        ""
                    )
                )

                affiliation = organization

                department = (
                    first_employment.get(
                        "department-name",
                        ""
                    )
                )

        # =============================================
        # FETCH PERSON DETAILS
        # =============================================

        person_url = (
            f"https://pub.orcid.org/v3.0/"
            f"{orcid_id}/person"
        )

        person_response = requests.get(

            person_url,

            headers=headers
        )

        biography = ""

        if person_response.status_code == 200:

            person_data = (
                person_response.json()
            )

            biography_data = (
                person_data.get(
                    "biography",
                    {}
                )
            )

            if biography_data:

                biography = (
                    biography_data.get(
                        "content",
                        ""
                    )
                )

        # =============================================
        # FINAL RETURN
        # =============================================

        return {

            "orcid":
                orcid_id,

            "affiliation":
                affiliation,

            "department":
                department,

            "biography":
                biography
        }

    except Exception as e:

        print(e)

        return {

            "orcid": orcid_id,

            "affiliation": "",

            "department": "",

            "biography": ""
        }