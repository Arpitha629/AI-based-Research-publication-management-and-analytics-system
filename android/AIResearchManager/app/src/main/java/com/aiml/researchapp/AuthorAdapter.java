package com.aiml.researchapp;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class AuthorAdapter
        extends RecyclerView.Adapter<
        AuthorAdapter.AuthorViewHolder> {

    List<Author> authorList;

    OnAuthorClickListener listener;

    public interface OnAuthorClickListener {

        void onAuthorClick(
                Author author
        );
    }

    public AuthorAdapter(

            List<Author> authorList,

            OnAuthorClickListener listener

    ) {

        this.authorList =
                authorList;

        this.listener =
                listener;
    }

    @NonNull
    @Override
    public AuthorViewHolder onCreateViewHolder(

            @NonNull ViewGroup parent,

            int viewType
    ) {

        View view = LayoutInflater
                .from(parent.getContext())
                .inflate(

                        R.layout.author_item,

                        parent,

                        false
                );

        return new AuthorViewHolder(
                view
        );
    }

    @Override
    public void onBindViewHolder(

            @NonNull AuthorViewHolder holder,

            int position
    ) {

        Author author =
                authorList.get(position);

        holder.authorName.setText(

                author.getName()
        );

        holder.authorAffiliation
                .setText(

                        author.getAffiliation()
                );

        holder.orcidText
                .setText(

                        "ORCID : " +

                                author.getOrcid()
                );

        holder.itemView
                .setOnClickListener(v -> {

                    listener.onAuthorClick(
                            author
                    );

                });

    }

    @Override
    public int getItemCount() {

        return authorList.size();
    }

    static class AuthorViewHolder
            extends RecyclerView.ViewHolder {

        TextView authorName;

        TextView authorAffiliation;

        TextView orcidText;

        public AuthorViewHolder(
                @NonNull View itemView
        ) {

            super(itemView);

            authorName =
                    itemView.findViewById(
                            R.id.authorName
                    );

            authorAffiliation =
                    itemView.findViewById(
                            R.id.authorAffiliation
                    );

            orcidText =
                    itemView.findViewById(
                            R.id.orcidText
                    );

        }

    }

}