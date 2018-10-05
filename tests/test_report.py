#!/usr/bin/env python3

import argparse
from junit_xml import TestSuite, TestCase
import glob
import os
import re

def report(args):
    ext = args.extension
    folder = args.output_dir
    file_dict = {}
    for file in glob.glob(os.path.abspath(folder) + "/*."+ext):
        fname = os.path.splitext(os.path.basename(file))[0]
        suite, suffix, test_name = fname.split('-')
        file_dict[(suite + '-' + suffix, test_name)] = file
    suite_name = ""
    test_suites = []
    suite = None
    regex = None
    if ext == "riscvemu":
        regex = re.compile("Power off")
    test_cases = []
    for test_key in sorted(file_dict):
        filename = file_dict[test_key]
        status = False
        with open(filename, 'r') as ifile:
            for line in ifile:
                if re.search(regex, line):
                    status = True
                    break
        test_case = TestCase(test_key[1], status=status, category=test_key[0],
                             file=filename)
        if suite == test_key[0]:
            test_cases.append(test_case)
        else:
            test_suites.append(TestSuite(suite, test_cases))
            test_cases = []
        suite = test_key[0]
    with open(args.output_xml, 'w') as out:
        TestSuite.to_file(out, test_suites)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helper script for generating "
                                     "junit xml test reprot files")
    parser.add_argument("--output-dir", required=True,
                        help="Test regression output directory")
    parser.add_argument("--output-xml", required=True,
                        help="Path to the output xml file")
    parser.add_argument("extension",
                        help="Test output file extension to parse")

    args = parser.parse_args()
    report(args)