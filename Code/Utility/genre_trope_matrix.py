import pandas as pd
import numpy as np
from Utility.toolbox import find_repo_root

root = find_repo_root()


def get_genres():
    df = pd.read_csv(f"{root}/Data/general/2020_genre_counts_by_trope.csv")
    genres = df.columns[2:29].tolist()
    genres = genres[0:-1]
    print(genres)
    with open(f"{root}/Data/general/genre_list.txt", "w") as f:
        f.write("\n".join(genres))


def build_tf_idf_matrix():
    df = pd.read_csv(f"{root}/Data/general/2020_genre_counts_by_trope.csv")
    genres = df.columns[2:29].tolist()

    ## calculate IDF
    num_genres = len(genres)
    df_tropes = df[genres]  # Genre counts
    df['idf'] = np.log(num_genres / (df_tropes > 0).sum(axis=1))

    ## calculate tf
    df[genres] = df[genres].apply(lambda x: x / sum(x), axis=1)

    ## combine
    df[genres] = df[genres].multiply(df['idf'], axis=0)
    df.drop(columns=['idf'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(f"{root}/Data/general/genre_trope_tfidf_matrix.csv", index=False)
    df['Trope'] = df['Trope'].str.strip()
    df = df[['Trope'] + genres]
    df.dropna(how='all', inplace=True)
    return df


def build_prop_trope_matrix(norm='num_movies'):
    df = pd.read_csv(f"{root}/Data/general/2020_genre_counts_by_trope.csv")
    genres = df.columns[2:29].tolist()
    all_tropes = df.iloc[:, 1].tolist()

    # Create the matrix with normalized genre percentages
    matrix_maker = []

    # Iterate through rows (excluding the first column, which is 'trope')
    for index, row in df.iterrows():
        genre_counts = row.iloc[2:29].tolist()

        if norm == 'sum_tropes':
            normalization = sum(genre_counts)
        elif norm == "num_movies":
            normalization =  row['Number_movies']
        else:
            raise ValueError("Enter a valid normalization metric")

        try:
            # Normalize genre counts to percentages
            genre_percents = [genre_count / normalization for genre_count in genre_counts] if normalization > 0 else genre_counts
        except ZeroDivisionError:
            genre_percents = genre_counts  # Handle division by zero case

        matrix_maker.append(genre_percents)

    ## build the dataframe, transpose, save
    df_matrix = pd.DataFrame(np.array(matrix_maker).T, columns=all_tropes, index=genres)
    df_matrix = df_matrix.transpose()
    df_matrix.reset_index(names='Trope', inplace=True)
    df_matrix.to_csv(f"{root}/Data/general/genre_trope_matrix.csv", index=False)
    df_matrix['Trope'] = df_matrix['Trope'].str.strip()
    return df_matrix

if __name__ == "__main__":

    df=build_prop_trope_matrix()
    print(df)
    df =build_tf_idf_matrix()
    print(df)
    get_genres()