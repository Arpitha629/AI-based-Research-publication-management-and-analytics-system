package com.aiml.researchapp;

import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;

public class AnalyticsActivity extends AppCompatActivity {

    BarChart barChartAnalytics;

    PieChart domainChart;

    PieChart citationChart;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        setContentView(
                R.layout.activity_analytics
        );

        barChartAnalytics =
                findViewById(
                        R.id.barChartAnalytics
                );

        domainChart =
                findViewById(
                        R.id.domainChart
                );

        citationChart =
                findViewById(
                        R.id.citationChart
                );

        try {

            String analyticsString =

                    getIntent()
                            .getStringExtra(
                                    "analytics"
                            );

            if (analyticsString == null) {
                return;
            }

            JSONObject analytics =

                    new JSONObject(
                            analyticsString
                    );

            loadPublicationTrend(
                    analytics
            );

            loadCitationDistribution(
                    analytics
            );

            loadSourceDistribution(
                    analytics
            );

        }

        catch (Exception e) {

            e.printStackTrace();
        }
    }

    private void loadPublicationTrend(
            JSONObject analytics
    ) {

        try {

            JSONObject years =

                    analytics.getJSONObject(
                            "year_distribution"
                    );

            ArrayList<BarEntry> entries =
                    new ArrayList<>();

            JSONArray names =
                    years.names();

            int index = 0;

            for (
                    int i = 0;
                    i < names.length();
                    i++
            ) {

                String year =
                        names.getString(i);

                float count =
                        years.getInt(
                                year
                        );

                entries.add(

                        new BarEntry(
                                index,
                                count
                        )
                );

                index++;
            }

            BarDataSet set =

                    new BarDataSet(
                            entries,
                            "Publication Trend"
                    );

            BarData data =
                    new BarData(
                            set
                    );

            barChartAnalytics.setData(
                    data
            );

            barChartAnalytics.invalidate();

        }

        catch (Exception e) {

            e.printStackTrace();
        }
    }

    private void loadSourceDistribution(
            JSONObject analytics
    ) {

        try {

            JSONObject source =

                    analytics.getJSONObject(
                            "source_distribution"
                    );

            ArrayList<PieEntry> entries =
                    new ArrayList<>();

            JSONArray names =
                    source.names();

            for (
                    int i = 0;
                    i < names.length();
                    i++
            ) {

                String key =
                        names.getString(i);

                float value =
                        source.getInt(key);

                entries.add(

                        new PieEntry(
                                value,
                                key
                        )
                );
            }

            PieDataSet set =

                    new PieDataSet(
                            entries,
                            "Research Domains"
                    );

            PieData data =
                    new PieData(set);

            domainChart.setData(
                    data
            );

            domainChart.invalidate();

        }

        catch (Exception e) {

            e.printStackTrace();
        }
    }

    private void loadCitationDistribution(
            JSONObject analytics
    ) {

        try {

            JSONObject citations =

                    analytics.getJSONObject(
                            "citation_distribution"
                    );

            ArrayList<PieEntry> entries =
                    new ArrayList<>();

            JSONArray names =
                    citations.names();

            for (
                    int i = 0;
                    i < names.length();
                    i++
            ) {

                String key =
                        names.getString(i);

                float value =
                        citations.getInt(
                                key
                        );

                entries.add(

                        new PieEntry(
                                value,
                                key
                        )
                );
            }

            PieDataSet set =

                    new PieDataSet(
                            entries,
                            "Citation Distribution"
                    );

            PieData data =
                    new PieData(set);

            citationChart.setData(
                    data
            );

            citationChart.invalidate();

        }

        catch (Exception e) {

            e.printStackTrace();
        }
    }
}