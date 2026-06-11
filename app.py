from flask import Flask
from flask import jsonify
from flask import request

from flask_cors import CORS

from search_engine import (
    get_authors,
    get_publications,
    universal_search
)

app = Flask(__name__)

CORS(app)

# =====================================================
# HOME API
# =====================================================

@app.route("/")

def home():

    return jsonify({

        "message":
            "AI Research Publication Management API",

        "status":
            "Running Successfully"
    })


# =====================================================
# AUTHORS API
# =====================================================

@app.route("/authors")

def authors():

    try:

        query = request.args.get(
            "q",
            ""
        ).strip()

        results = get_authors(
            query
        )

        return jsonify({

            "total_authors":
                len(results),

            "results":
                results
        })

    except Exception as e:

        return jsonify({

            "error":
                str(e)
        }), 500


# =====================================================
# FACULTY API
# =====================================================

@app.route("/faculty")

def faculty():

    try:

        query = request.args.get(
            "q",
            ""
        ).strip()

        results = get_authors(
            query
        )

        return jsonify({

            "total_authors":
                len(results),

            "results":
                results
        })

    except Exception as e:

        return jsonify({

            "error":
                str(e)
        }), 500


# =====================================================
# PUBLICATIONS API
# =====================================================

@app.route("/publications")

def publications():

    try:

        author_id = request.args.get(
            "author_id",
            ""
        ).strip()

        if author_id == "":

            return jsonify({

                "error":
                    "No author_id provided"
            }), 400

        results = get_publications(
            author_id
        )

        # IMPORTANT FIX:
        # RETURN DIRECTLY
        # NO EXTRA NESTED "results"

        return jsonify(
            results
        )

    except Exception as e:

        return jsonify({

            "error":
                str(e)
        }), 500


# =====================================================
# UNIVERSAL SEARCH API
# =====================================================

@app.route("/search")

def search():

    try:

        query = request.args.get(
            "q",
            ""
        ).strip()

        if query == "":

            return jsonify({

                "error":
                    "No search query provided"
            }), 400

        results = universal_search(
            query
        )

        return jsonify(
            results
        )

    except Exception as e:

        return jsonify({

            "error":
                str(e)
        }), 500


# =====================================================
# HEALTH CHECK
# =====================================================

@app.route("/health")

def health():

    return jsonify({

        "server":
            "running",

        "backend":
            "connected",

        "status":
            "healthy"
    })


# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True
    )