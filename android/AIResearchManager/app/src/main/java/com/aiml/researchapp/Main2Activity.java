package com.aiml.researchapp;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.DefaultRetryPolicy;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

import android.content.Intent;
import com.google.android.material.card.MaterialCardView;

public class Main2Activity
        extends AppCompatActivity {

    EditText facultySearchBox;

    EditText orcidSearchBox;

    EditText publicationSearchBox;

    Button facultySearchButton;

    Button orcidSearchButton;

    Button publicationSearchButton;

    RecyclerView recyclerView;

    RecyclerView authorRecycler;

    TextView citationText;

    TextView hindexText;

    TextView i10Text;

    TextView nameText;

    TextView affiliationText;

    MaterialCardView analyticsCard;

    JSONObject analyticsData;

    PublicationAdapter publicationAdapter;

    AuthorAdapter authorAdapter;

    List<Publication> publicationList;

    List<Author> authorList;

    String BASE_URL =
            "https://ai-based-research-publication-management.onrender.com";
    @Override
    protected void onCreate(
            Bundle savedInstanceState
    ) {

        super.onCreate(
                savedInstanceState
        );

        setContentView(
                R.layout.activity_main2
        );

        facultySearchBox =
                findViewById(
                        R.id.facultySearchBox
                );

        orcidSearchBox =
                findViewById(
                        R.id.orcidSearchBox
                );

        publicationSearchBox =
                findViewById(
                        R.id.publicationSearchBox
                );

        facultySearchButton =
                findViewById(
                        R.id.facultySearchButton
                );

        orcidSearchButton =
                findViewById(
                        R.id.orcidSearchButton
                );

        publicationSearchButton =
                findViewById(
                        R.id.publicationSearchButton
                );
        recyclerView =
                findViewById(
                        R.id.recyclerView
                );

        authorRecycler =
                findViewById(
                        R.id.authorRecycler
                );

        citationText =
                findViewById(
                        R.id.citationText
                );

        hindexText =
                findViewById(
                        R.id.hindexText
                );

        i10Text =
                findViewById(
                        R.id.i10Text
                );

        nameText =
                findViewById(
                        R.id.nameText
                );

        affiliationText =
                findViewById(
                        R.id.affiliationText
                );


        analyticsCard =
                findViewById(
                        R.id.analyticsCard
                );

        recyclerView.setLayoutManager(

                new LinearLayoutManager(
                        this
                )
        );

        authorRecycler.setLayoutManager(

                new LinearLayoutManager(
                        this
                )
        );

        publicationList =
                new ArrayList<>();

        authorList =
                new ArrayList<>();

        publicationAdapter =
                new PublicationAdapter(
                        publicationList
                );

        recyclerView.setAdapter(
                publicationAdapter
        );

        facultySearchButton.setOnClickListener(v -> {

            searchFaculty();

        });

        orcidSearchButton.setOnClickListener(v -> {

            searchOrcid();

        });

        publicationSearchButton.setOnClickListener(v -> {

            searchPublication();

        });

        analyticsCard.setOnClickListener(v -> {

            try {

                if (analyticsData == null) {

                    Toast.makeText(
                            Main2Activity.this,
                            "Search Faculty First",
                            Toast.LENGTH_LONG
                    ).show();

                    return;
                }

                Intent intent =
                        new Intent(
                                Main2Activity.this,
                                AnalyticsActivity.class
                        );

                intent.putExtra(
                        "analytics",
                        analyticsData.toString()
                );

                startActivity(intent);

            } catch (Exception e) {

                e.printStackTrace();
            }

        });
    }


    private void searchAuthors(String query) {



        String url =

                BASE_URL +
                        "/authors?q=" +
                        query;

        RequestQueue queue =

                Volley.newRequestQueue(
                        this
                );

        JsonObjectRequest request =

                new JsonObjectRequest(

                        Request.Method.GET,

                        url,

                        null,

                        response -> {

                            try{

                                JSONArray results =

                                        response
                                                .getJSONArray(
                                                        "results"
                                                );

                                authorList.clear();

                                Gson gson =
                                        new Gson();

                                for(
                                        int i=0;
                                        i<results.length();
                                        i++
                                ){

                                    JSONObject obj =

                                            results
                                                    .getJSONObject(
                                                            i
                                                    );

                                    Author author =

                                            gson.fromJson(

                                                    obj.toString(),

                                                    Author.class
                                            );

                                    authorList.add(
                                            author
                                    );

                                }

                                authorAdapter =

                                        new AuthorAdapter(

                                                authorList,

                                                author -> {

                                                    loadPublications(

                                                            author.getAuthor_id()
                                                    );

                                                }
                                        );

                                authorRecycler.setAdapter(
                                        authorAdapter
                                );

                            }

                            catch(Exception e){

                                e.printStackTrace();
                            }

                        },

                        error -> {

                            String message = "";

                            if(error.networkResponse != null){

                                message =
                                        "CODE: " +
                                                error.networkResponse.statusCode;

                            }
                            else{

                                message =
                                        error.toString();

                            }

                            Toast.makeText(

                                    Main2Activity.this,

                                    message,

                                    Toast.LENGTH_LONG

                            ).show();

                        }

                );
        request.setRetryPolicy(

                new DefaultRetryPolicy(

                        2147483647,

                        0,

                        1f

                )
        );

        queue.add(
                request
        );

    }

    private void loadPublications(
            String authorId
    ){

        String url =

                BASE_URL +

                        "/publications?author_id=" +

                        authorId;

        RequestQueue queue =

                Volley.newRequestQueue(
                        this
                );

        JsonObjectRequest request =

                new JsonObjectRequest(

                        Request.Method.GET,

                        url,

                        null,

                        response -> {

                            Toast.makeText(
                                    Main2Activity.this,
                                    "Publication API Success",
                                    Toast.LENGTH_LONG
                            ).show();

                            try{
                                nameText.setText(

                                        response.getString(
                                                "name"
                                        )
                                );

                                affiliationText.setText(

                                        response.getString(
                                                "affiliation"
                                        )
                                );

                                citationText.setText(

                                        "Citations\n"+

                                                response.getInt(
                                                        "citations"
                                                )
                                );

                                hindexText.setText(

                                        "H Index\n"+

                                                response.getInt(
                                                        "h_index"
                                                )
                                );

                                i10Text.setText(

                                        "I10 Index\n"+

                                                response.getInt(
                                                        "i10_index"
                                                )
                                );

                                analyticsData =

                                        response.getJSONObject(
                                                "analytics"
                                        );

                                JSONArray results =

                                        response.getJSONArray(
                                                "results"
                                        );

                                publicationList.clear();

                                Gson gson =
                                        new Gson();

                                for(
                                        int i=0;
                                        i<results.length();
                                        i++
                                ){

                                    JSONObject obj =

                                            results
                                                    .getJSONObject(
                                                            i
                                                    );

                                    Publication publication =

                                            gson.fromJson(

                                                    obj.toString(),

                                                    Publication.class
                                            );

                                    publicationList.add(
                                            publication
                                    );

                                }

                                publicationAdapter
                                        .notifyDataSetChanged();

                            }

                            catch(Exception e){

                                Toast.makeText(
                                        Main2Activity.this,
                                        e.toString(),
                                        Toast.LENGTH_LONG
                                ).show();

                                e.printStackTrace();
                            }
                        },

                        error -> {

                            String message = "";

                            if(error.networkResponse != null){

                                message =
                                        "CODE : " +
                                                error.networkResponse.statusCode;

                            }else{

                                message =
                                        error.toString();
                            }

                            Toast.makeText(

                                    Main2Activity.this,

                                    message,

                                    Toast.LENGTH_LONG

                            ).show();

                        }

                );

        request.setRetryPolicy(

                new DefaultRetryPolicy(

                        2147483647,

                        0,

                        1f

                )
        );

        queue.add(
                request
        );
    }
    private void searchFaculty() {

        String query =
                facultySearchBox
                        .getText()
                        .toString();

        searchAuthors(query);
    }

    private void searchOrcid() {

        String query =
                orcidSearchBox
                        .getText()
                        .toString();

        searchAuthors(query);
    }

    private void searchPublication() {

        String query =
                publicationSearchBox
                        .getText()
                        .toString()
                        .trim();

        String url =
                BASE_URL +
                        "/search?q=" +
                        query;

        RequestQueue queue =
                Volley.newRequestQueue(this);

        JsonObjectRequest request =

                new JsonObjectRequest(

                        Request.Method.GET,
                        url,
                        null,

                        response -> {

                            try {

                                JSONArray results =
                                        response.getJSONArray(
                                                "results"
                                        );

                                publicationList.clear();

                                for (
                                        int i = 0;
                                        i < results.length();
                                        i++
                                ) {

                                    JSONObject obj =
                                            results.getJSONObject(i);

                                    Publication publication =
                                            new Publication();

                                    // TITLE

                                    // TITLE

                                    publication.Title =

                                            obj.optString(
                                                    "Title",
                                                    obj.optString(
                                                            "Title ",
                                                            obj.optString(
                                                                    "Unnamed: 1",
                                                                    obj.optString(
                                                                            "Faculty",
                                                                            "Unknown Title"
                                                                    )
                                                            )
                                                    )
                                            );

// AUTHORS

                                    publication.Authors =

                                            obj.optString(
                                                    "Authors",
                                                    obj.optString(
                                                            "Name of the Author/s",
                                                            obj.optString(
                                                                    "Unnamed: 6",
                                                                    obj.optString(
                                                                            "Faculty",
                                                                            "Unknown"
                                                                    )
                                                            )
                                                    )
                                            );

// YEAR

                                    publication.Year =

                                            obj.optString(
                                                    "Year",
                                                    obj.optString(
                                                            "Unnamed: 5",
                                                            "N/A"
                                                    )
                                            );

// SOURCE

                                    publication.source =

                                            obj.optString(
                                                    "source",
                                                    "Unknown"
                                            );

// CITATIONS

                                    publication.Citations = 0;

                                    publicationList.add(
                                            publication
                                    );
                                }

                                publicationAdapter
                                        .notifyDataSetChanged();

                                Toast.makeText(

                                        Main2Activity.this,

                                        "Found "
                                                + results.length()
                                                + " Results",

                                        Toast.LENGTH_LONG

                                ).show();

                            }

                            catch (Exception e) {

                                e.printStackTrace();

                                Toast.makeText(

                                        Main2Activity.this,

                                        e.toString(),

                                        Toast.LENGTH_LONG

                                ).show();
                            }

                        },

                        error -> {

                            Toast.makeText(

                                    Main2Activity.this,

                                    error.toString(),

                                    Toast.LENGTH_LONG

                            ).show();

                        }

                );

        request.setRetryPolicy(

                new DefaultRetryPolicy(

                        2147483647,

                        0,

                        1f

                )
        );

        queue.add(request);
    }
}