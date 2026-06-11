package com.aiml.researchapp;

public class Publication {

    public String Title;
    public String Authors;
    public String Year;
    public String source;
    public String Link;
    public Integer Citations;

    public Publication() {
    }

    public Publication(
            String title,
            String authors,
            String year,
            String source
    ) {

        this.Title = title;
        this.Authors = authors;
        this.Year = year;
        this.source = source;
    }

    public String getTitle() {

        if (Title == null || Title.trim().isEmpty()) {
            return "Untitled";
        }

        return Title;
    }

    public String getAuthors() {

        if (Authors == null || Authors.trim().isEmpty()) {
            return "Unknown";
        }

        return Authors;
    }

    public String getYear() {

        if (Year == null || Year.trim().isEmpty()) {
            return "N/A";
        }

        return Year;
    }

    public String getSource() {

        if (source == null) {
            return "";
        }

        return source;
    }

    public String getLink() {

        if (Link == null) {
            return "";
        }

        return Link;
    }

    public Integer getCitations() {

        if (Citations == null) {
            return 0;
        }

        return Citations;
    }

    public void setTitle(String title) {
        this.Title = title;
    }

    public void setAuthors(String authors) {
        this.Authors = authors;
    }

    public void setYear(String year) {
        this.Year = year;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public void setLink(String link) {
        this.Link = link;
    }

    public void setCitations(Integer citations) {
        this.Citations = citations;
    }
}