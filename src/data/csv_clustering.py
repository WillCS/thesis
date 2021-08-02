import csv

def get_clusterings_from_csv(filename: str):
    clusters = {}
        
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)

        top_row = next(reader)
        for l in top_row[2:]:
            n_clusters = int(l[1:])
            clusters[n_clusters] = list([] for i in range(n_clusters))
        
        row_index = 0
        for row in reader:
            for i in range(2, len(row)):
                label      = top_row[i]
                n_clusters = int(label[1:])

                cluster_id = int(row[i]) - 1

                clusters[i][cluster_id].append(row_index)

            row_index += 1

    return clusters