import re
import ftfy

import yaml

unwanted_matches = ["noline", "separator", "end_of_file"]
permanent_matches = ["noline", "separator", "end_of_file", "matrix_sub_value"]

def parse_line(line, line_dict):
    line_entries = {}
    item, search_result = find_match(line, line_dict)
    if search_result:
        field, expression = item
        if field in unwanted_matches:
            pass
        elif field == "matrix_sub_value":
            # Exracting the submatrix
            sub_matrix = search_result.groupdict()
            for k, v in sub_matrix.items():
                new_field = k.lower()
                line_entries[new_field] = v
        else:
            line_entries[field] = search_result.group(field)

    return item, line_entries


def reset_check_items(lines_regexp):
    return list(lines_regexp.items())


def get_unmapped_values(remaining):
    return [i[0] for i in remaining if i[0] not in permanent_matches]


def find_match(string, check_entries):
    for item in check_entries:
        field, expression = item
        search_result = re.search(expression, string)
        if search_result:
            return item, search_result
    return None, None


def seal_result(value, to_check_items):
    unmapped_values = get_unmapped_values(to_check_items)
    return value, unmapped_values


def get_results_from_lines(lines, locale_template):
    # lines = []
    all_results = []
    to_check_items = list(locale_template.items())
    already_check_items = list()
    value = {}
    prev_field = None
    for line in lines:
        line = ftfy.fix_encoding(line)
        found_value, value_new_entries = parse_line(line, to_check_items)
        if found_value:
            field, expression = found_value

            if field == "matrix_sub_value":
                value_new_entries = {"{}{}".format(prev_field, k): v for k, v in value_new_entries.items()}

            value.update(value_new_entries)
            prev_field = field
            if field == "end_of_file":
                if value:
                    result = seal_result(value, to_check_items)
                    all_results.append(result)
                to_check_items = reset_check_items(locale_template)
                value = {}

            if field in permanent_matches:
                continue

            already_check_items.append(found_value)
            to_check_items.remove(found_value)
            if len(to_check_items) <= len(permanent_matches):
                # I don't need to check anyother field
                # print("No other field to check for filename {}", filename)
                all_results.append(seal_result(value, to_check_items))
                value = {}
        else:
            # potentially the line is unwanted so we need to reset the items and add results
            found_value, value_new_entries = parse_line(line, already_check_items)
            if found_value:
                # Something wrong in the format of the file
                # try create a new value starting from this line
                all_results.append(seal_result(value, to_check_items))
                value = value_new_entries
                to_check_items = reset_check_items(locale_template)
                to_check_items.remove(found_value)

    # This is the end of the file
    return all_results


def get_csv_document(lines, locale):
    with open("templates/{}.yaml".format(locale), 'r') as f:
        template_file = yaml.safe_load(f)
        fieldnames = [field for field in template_file.keys() if field not in permanent_matches]
        all_results = get_results_from_lines(lines, template_file)
        output = [fieldnames]
        for result_entry in all_results:
            result, unmapped_fields = result_entry
            result_keys = result.keys()
            new_row = [result[f] if f in result_keys else 'ERROR' for f in fieldnames]
            output.append(new_row)
        return output
