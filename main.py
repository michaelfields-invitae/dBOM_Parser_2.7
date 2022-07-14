import argparse
import sys
from os import listdir
import os
from os.path import isfile, join
import xml.etree.ElementTree as ET

def returnAllFiles(root_directory):
    ROOT_DIR = root_directory
    onlyfiles = [f for f in listdir(ROOT_DIR) if isfile(join(ROOT_DIR, f))]

    return onlyfiles


def parse_cmdline_params(arg_list=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("-f",
                        "--folder",
                        nargs='+',
                        type=str,
                        help="folder containing dboms",
                        required=False)

    opts = parser.parse_args(args=arg_list)

    return opts


def parse_xml(file, root_dir, dbom_name):
    erp_part_nums = []
    dx_part_nums = []

    output_file = join(root_dir, dbom_name + "_output_parts.txt")

    with open(file, 'r') as xml_file:
        root = ET.parse(xml_file).getroot()
        for element in root.findall('BOM/ProcessSegments/ProcessSegment/Components/Component/CustomProperties'):
            for sub_ele in element.findall("Property"):
                # output = sub_ele.text  # .encode('UTF-8')
                # erp_part_nums.append(output)
                # print(output)
                if sub_ele.attrib["Name"] == "ERP Part Number":
                    erp_part_nums.append(sub_ele.text)
                elif sub_ele.attrib["Name"] == "GLI Tag":
                    dx_part_nums.append(sub_ele.text)


    max_arr_len = max(len(erp_part_nums), len(dx_part_nums))

    with open(output_file, "w") as text_file:
        text_file.write("DX1577 Parts, ERP Parts\n")
        for i in range(max_arr_len):
            if i > len(erp_part_nums):
                text_file.write(str(dx_part_nums[i]) + ",-\n")
            elif i > len(dx_part_nums):
                text_file.write(str("-, " + str(erp_part_nums[i]) + "\n"))
            else:
                text_file.write(str(dx_part_nums[i]) + ", " + str(erp_part_nums[i]) + "\n")



opts = parse_cmdline_params(sys.argv[1:])
root_bom_dir = opts.folder[0]
test_files = returnAllFiles(root_bom_dir)
print(test_files)

for file in test_files:
    filepath = join(root_bom_dir, file)
    print(filepath)
    parse_xml(filepath, root_bom_dir, file)