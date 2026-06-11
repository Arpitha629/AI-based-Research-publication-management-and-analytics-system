package com.aiml.researchapp;

import android.content.Intent;
import android.net.Uri;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class PublicationAdapter
        extends RecyclerView.Adapter<
        PublicationAdapter.PublicationViewHolder> {

    List<Publication> publicationList;

    public PublicationAdapter(

            List<Publication> publicationList
    ) {

        this.publicationList =
                publicationList;
    }

    @NonNull
    @Override
    public PublicationViewHolder onCreateViewHolder(

            @NonNull ViewGroup parent,

            int viewType
    ) {

        View view =
                LayoutInflater
                        .from(
                                parent.getContext()
                        )
                        .inflate(

                                R.layout.publication_item,

                                parent,

                                false
                        );

        return new PublicationViewHolder(
                view
        );

    }

    @Override
    public void onBindViewHolder(

            @NonNull PublicationViewHolder holder,

            int position
    ) {

        Publication publication =

                publicationList.get(
                        position
                );

        holder.titleText.setText(

                publication.getTitle()
        );

        holder.authorsText.setText(

                "Authors : " +

                        publication.getAuthors()
        );

        holder.yearText.setText(

                "Year : " +

                        publication.getYear()
        );

        holder.sourceText.setText(

                "Source : " +

                        publication.getSource()
        );

        holder.citationCount.setText(

                "Citations : " +

                        publication.getCitations()
        );

        holder.itemView
                .setOnClickListener(v -> {

                    String url =
                            publication.getLink();

                    if(

                            url != null &&

                                    !url.isEmpty()

                    ){

                        Intent intent =
                                new Intent(

                                        Intent.ACTION_VIEW,

                                        Uri.parse(url)
                                );

                        v.getContext()
                                .startActivity(
                                        intent
                                );

                    }

                });

    }

    @Override
    public int getItemCount() {

        return publicationList.size();
    }

    static class PublicationViewHolder
            extends RecyclerView.ViewHolder {

        TextView titleText;

        TextView authorsText;

        TextView yearText;

        TextView sourceText;

        TextView citationCount;

        public PublicationViewHolder(

                @NonNull View itemView
        ) {

            super(itemView);

            titleText =
                    itemView.findViewById(
                            R.id.titleText
                    );

            authorsText =
                    itemView.findViewById(
                            R.id.authorsText
                    );

            yearText =
                    itemView.findViewById(
                            R.id.yearText
                    );

            sourceText =
                    itemView.findViewById(
                            R.id.sourceText
                    );

            citationCount =
                    itemView.findViewById(
                            R.id.citationCount
                    );

        }

    }

}