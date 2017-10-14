import csv
import re
import json

fieldnames = ["name", "TR", "TRb", "TRi", "TRa", "AP", "APb", "APi", "APa", "DV", "DVb", "DVi", "DVa", "NU", "NUb",
                "NUi", "NUa", "SR", "SRb", "SRi", "SRa", "B", "I", "A", "M", "SD", "HIT", "LOT", "T"]

lines_regexp = {
    "noline": "^>?\s*$",
    "separator": ">?\s*-{3,}",
    "end_of_file": ">?\s*Regards,$",
    "matrix_sub_value": ">?\s*B*\s*=\s*(?P<B>\d+);\s*I\s*=\s*(?P<I>\d+);\s*A\s*= (?P<A>\d+)\.?$",
    "name": ">?\s*Greetings (?P<name>.*),$",
    "date": ">?\s*Thanks for taking the TPI Survey on (?P<date>\d{2}/\d{2}/\d{4})\.?$",
    "group": ">?\s*Group: (?P<group>.*)\.?$",
    "learners": ">?\s*Specific learners focused on: (?P<learners>.*)\.?$",
    "group_size": ">?\s*Group Size: (?P<group_size>.*)\.?$",
    "primary_role": ">?\s*A. Primary role or function: (?P<primary_role>.*)\.?$",
    "instructive_perc": ">?\s*B. Approximate percentage of normal work routine "
                        "involves instructing others: (?P<instructive_perc>\d{1,2}\%)\.?$",
    "org_name": ">?\s*C. Name of organization or institutional affiliation: (?P<org_name>.*)\.?$",
    "employment_sector": ">?\s*D. Employment sector: (?P<employment_sector>.*)\.?$",
    "prompt": ">?\s*E. What prompted to take the TPI: (?P<prompt>.*)\.?$",
    "location": ">?\s*F. Location: (?P<location>.*)\.?$",
    "country": ">?\s*Country: (?P<country>.*)\.?$",
    "province": ">?\s*Province/State/Territory: (?P<province>.*)\.?$",
    "city": ">?\s*City: (?P<city>.*)\.?$",
    "highest_qual": ">?\s*G. Highest educational qualifications: (?P<highest_qual>.*)\.?$",
    "years_teaching": ">?\s*H. Approximate years instructing, educating, or teaching: (?P<years_teaching>.*)\.?$",
    "years_practicing": ">?\s*Years practicing specialty: (?P<years_practicing>.*)\.?$",
    "gender": ">?\s*J. Gender: (?P<gender>\w+)\.?$",
    "TR": ">?\s*Transmission Total: \(Tr\) (?P<TR>\d+)\.?$",
    "AP": ">?\s*Apprenticeship Total: \(Ap\) (?P<AP>\d+)\.?$",
    "DV": ">?\s*Developmental Total: \(Dv\) (?P<DV>\d+)\.?$",
    "NU": ">?\s*Nurturing Total: \(Nu\) (?P<NU>\d+)\.?$",
    "SR": ">?\s*Social Reform Total: \(SR\) (?P<SR>\d+)\.?$",
    "B": ">?\s*Beliefs total: \(B\) (?P<B>\d+)$",
    "I": ">?\s*Intentions total: \(I\) (?P<I>\d+)$",
    "A": ">?\s*Action total: \(A\) (?P<A>\d+)$",
    "M": ">?\s*Mean: \(M\) (?P<M>.*)$",
    "SD": ">?\s*Standard Deviation: \(SD\) (?P<SD>.*)$",
    "HIT": ">?\s*Dominant Threshold: \(HIT\) (?P<HIT>.*)$",
    "LOT": ">?\s*Recessive Threshold: \(LOT\) (?P<LOT>.*)$",
    "T": ">?\s*Overall Total: \(T\) (?P<T>.*)$"
}

unwanted_matches = ["noline", "separator", "end_of_file"]
permanent_matches = ["noline", "separator", "end_of_file", "matrix_sub_value"]
matrix_matches = ["TR", "AP", "DV", "NU", "SR"]


def parse_line(line, line_dict, matrix_value=None):
    line_entries = {}
    item, search_result = find_match(line, check_entries=line_dict)
    if search_result:
        field, expression = item
        if field in unwanted_matches:
            pass
        elif field is "matrix_sub_value":
            # Exracting the submatrix
            b = search_result.group('B'), "b"
            i = search_result.group('I'), "i",
            a = search_result.group('A'), "a"
            for val in [b, i, a]:
                new_field = matrix_value + val[1]
                line_entries[new_field] = val[0]
        else:
            line_entries[field] = search_result.group(field)

    return item, line_entries


def reset_check_items():
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


def get_results_from_lines(lines):
    # lines = []
    all_results = []
    to_check_items = list(lines_regexp.items())
    already_check_items = list()
    value = {}
    matrix_value = None
    for line in lines:
        found_value, value_new_entries = parse_line(line, line_dict=to_check_items, matrix_value=matrix_value)
        value.update(value_new_entries)
        if found_value:
            field, expression = found_value
            if field is "end_of_file":
                if value:
                    result = seal_result(value, to_check_items)
                    all_results.append(result)
                to_check_items = reset_check_items()
                value = {}
            elif field in matrix_matches:
                matrix_value = field

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
            found_value, value_new_entries = parse_line(line, line_dict=already_check_items, matrix_value=matrix_value)
            if found_value:
                # Something wrong in the format of the file
                # try create a new value starting from this line
                all_results.append(seal_result(value, to_check_items))
                value = value_new_entries
                to_check_items = reset_check_items()
                to_check_items.remove(found_value)

    # This is the end of the file
    return all_results


def get_csv_document(lines):
    all_results = get_results_from_lines(lines)
    output = []
    output.append(fieldnames)
    for result_entry in all_results:
        result, unmapped_fields = result_entry
        result_keys = result.keys()
        new_row = [result[f] if f in result_keys else 'ERROR' for f in fieldnames]
        output.append(new_row)
    return output
