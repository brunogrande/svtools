from unittest import TestCase, main
import os
import svtools.vcfpaste
import glob 
import sys
import tempfile
import difflib

class IntegrationTest_vcfpaste(TestCase):
    # FIXME We really don't need to have this stuff run with every test. Run once...
    def setUp(self):
        test_directory = os.path.dirname(os.path.abspath(__file__))
        self.test_data_dir = os.path.join(test_directory, 'test_data', 'vcfpaste')
        # glob vcfs
        vcfs = glob.glob(os.path.join(self.test_data_dir, 'NA*vcf'))
        # write out list since we have the paths and have to get those right
        temp_descriptor, self.list_of_vcfs = tempfile.mkstemp()
        temp_handle = os.fdopen(temp_descriptor, 'w') 
        for vcf_path in vcfs:
            temp_handle.write(vcf_path + '\n')
        temp_handle.close()

        self.master = glob.glob(os.path.join(self.test_data_dir, 'master.vcf'))

    def tearDown(self):
        os.remove(self.list_of_vcfs)

    def run_integration_test_without_master(self):
        expected_result = os.path.join(self.test_data_dir, 'expected_no_master.vcf')
        temp_descriptor, temp_output_path = tempfile.mkstemp(suffix='.vcf')
        output_handle = os.fdopen(temp_descriptor, 'w')
        try:
            paster = svtools.vcfpaste.Vcfpaste(self.list_of_vcfs, master=None, sum_quals=True)
            paster.execute(output_handle)
        finally:
            output_handle.close()
        expected_lines = open(expected_result).readlines()
        produced_lines = open(temp_output_path).readlines()
        diff = difflib.unified_diff(produced_lines, expected_lines, fromfile=temp_output_path, tofile=expected_result)
        result = '\n'.join(diff)
        if result != '':
            for line in result:
                sys.stdout.write(line)
            self.assertFalse(result)

class Test_vcfpaste(TestCase):

    def test_init_w_defaults(self):
        paster = svtools.vcfpaste.Vcfpaste('a_file_o_vcf_filenames')
        self.assertEqual(paster.vcf_list, 'a_file_o_vcf_filenames')
        self.assertIsNone(paster.master)
        self.assertIsNone(paster.sum_quals)

    def test_init_w_specified(self):
        paster = svtools.vcfpaste.Vcfpaste('some_file', 'master_blaster', True)
        self.assertEqual(paster.vcf_list, 'some_file')
        self.assertEqual(paster.master, 'master_blaster')
        self.assertTrue(paster.sum_quals)

    def test_read_filenames(self):
        pass

    def test_open_files(self):
        pass

    def test_write_header(self):
        pass

    def test_write_variants(self):
        pass

    def test_close_files(self):
        pass

if __name__ == "__main__":
    main()

