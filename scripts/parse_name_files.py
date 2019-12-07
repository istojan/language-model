

FILES = {
    "../other/macedonian_male_names_raw.txt": "../other/male_names.txt",
    "../other/macedonian_female_names_raw.txt" : "../other/female_names.txt"
}

if __name__ == "__main__":

    print("Message=\"Starting to parse name files\"")

    for file_path in FILES:

        with open(file_path, 'r') as f_in, open(FILES[file_path], 'w') as f_out:
            for line in f_in:
                words = line.split(" ")
                if len(words) >= 2:
                    f_out.write(line.split(" ")[0] + "\n")

    print("Message=\"Finished parsing name files\"")
