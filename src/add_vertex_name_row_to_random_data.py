name_row = ",".join(f"{i}" for i in range(1, 72))
name_row = name_row + "\n"

get_filename = lambda x: f"./resources/plant_genetics/random_2021-09-27/corr_random_{x}.csv"

for i in range(1, 101):
    with open(get_filename(i), "r+") as f:
        contents = f.readlines()
        contents.insert(0, name_row)
        f.seek(0)
        f.writelines(contents)
        f.truncate()