def compare_output(output_location, sample_location):
    with open(output_location, "r") as output_file:
        with open(sample_location, "r") as sample_file:
            ofls = output_file.readlines()
            sfls = sample_file.readlines()
            if len(ofls) == 0:
                return 0
            for ofl, sfl in zip(ofls, sfls):
                if ofl != sfl:
                    return 0
    return 10
