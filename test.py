import os
from machine import main


def collect_files(directory, tp):
    txt_files = []
    for filename in os.listdir(directory):
        if filename.endswith(tp):
            txt_files.append(filename)
    return txt_files


if __name__ == "__main__":
    inpts = [file for file in collect_files("tests", ".txt") if "out" not in file]
    algs = collect_files("tests", ".alg")
    cnt = 0
    for alg in algs:
        inpt = "tests/empty.txt"
        out = alg.split(".")[0] + "_out.txt"
        if alg.split(".")[0] + ".txt" in inpts:
            inpt = "tests/" + alg.split(".")[0] + ".txt"
        main("tests/" + alg, inpt)
        with open("output.txt", "r") as output:
            res = output.read()
            with open("tests/" + out, "r") as expected:
                if res == expected.read():
                    print(f"TEST {alg.split('.')[0]} - PASSED")
                    cnt += 1
                else:
                    print(f"TEST {alg.split('.')[0]} - FAILED")
    with open("test_result.txt", "w") as test_file:
        if cnt == len(algs):
            test_file.write("PASSED")
        else:
            test_file.write("FAILED!")
