import argparse
import config
import requests

moztrap_base_url = config.moztrap_url
testrail_base_url = config.testrail_url

class TestCaseEntry(object):

    def __init__(self, name, steps):
        self.name = name
        self.steps = steps

    def __str__(self):
        return "{{testcase: {0}, steps:[{1}]}}".format(self.name, self.steps)


def get_moztrap_test_cases(test_suite_id):
    result = requests.get("{base}/api/v1/caseversion".format(base=moztrap_base_url), params = {
        "format": "json",
        "case__suites": test_suite_id
    })
    testcases = []
    for testcase_entry in result.json()["objects"]:
        testcases.append(int(testcase_entry["id"]))

    print("TestCase ID's in suite: {0}".format(testcases))
    return testcases


def get_moztrap_test_case_details(test_case_id):
    result = requests.get("{base}/api/v1/caseversion/{id}".format(base=moztrap_base_url, id=test_case_id),
        params={
        "format": "json"
        }
    )
    result_json = result.json()
    steps = []
    for step in result_json["steps"]:
        # append a tuple of (instruction, expected)
        steps.append((step["instruction"], step["expected"]))

    testcase_details = TestCaseEntry(result_json["name"], steps)
    return testcase_details




def add_testcase_to_testrail(testrail_section_id, testcase_data):
    print("importing test case {0}".format(testcase_data))

    processed_steps = process_steps(testcase_data.steps)

    result = requests.post("{base}/api/v2/add_case/{section}".format(base=config.testrail_url, section=testrail_section_id),
                           data={
                               "title": testcase_data.name,
                               "type_id": 1,
                               "priority_id": 3,
                               "estimate":"",
                               "refs":"",
                               "custom_steps_separated":processed_steps
                           },
                           auth=(config.testrail_user, config.testrail_api_key)
                           )
    if(result.status_code == 200):
        print("Successfully imported: {0}".format(testcase_data.name))
    else:
        raise RuntimeError("Failed to import test case {0}".format(testcase_data.name))



def process_steps(steps):
    processed_steps = []
    for step in steps:
        processed_steps.append({
            "content": step[0],
            "expected": step[1]
        })


"""
Main program entry point.
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('mzid', type=int, help='MozTrap Test Suite ID', metavar="MozTrap_Suite_ID")
    parser.add_argument('trid', type=int, help='TestRail Suite ID', metavar="TestRail_Section_ID")
    args = parser.parse_args()

    print("Getting test cases for {0}...".format(args.mzid))
    testcases = get_moztrap_test_cases(args.mzid)


    for testcase in testcases:
        testcase_details = get_moztrap_test_case_details(testcase)
        add_testcase_to_testrail(args.trid, testcase_details)
