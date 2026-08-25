import json
import unittest
from pathlib import Path
from backend.data.sql_client import configured_object, validate_case_id, connection_options

ROOT=Path(__file__).parents[1]

class DeploymentContractTests(unittest.TestCase):
    def test_trusted_sql_uses_native_parameters_and_closed_catalog_placeholders(self):
        for path in (ROOT/'sql'/'trusted').glob('*.sql'):
            sql=path.read_text(encoding='utf-8')
            self.assertNotIn(':case_id', sql, path.name)
            self.assertNotIn(':limit', sql, path.name)
            self.assertNotIn('mad_data_lab_private', sql, path.name)
            self.assertIn('{{CURATED}}', sql, path.name)
    def test_identifiers_and_case_ids_fail_closed(self):
        self.assertEqual(validate_case_id('CASE_0042'), 'CASE_0042')
        with self.assertRaises(ValueError): validate_case_id('CASE_../')
        self.assertEqual(configured_object('catalog','schema','view'), 'catalog.schema.view')
        with self.assertRaises(ValueError): configured_object('catalog;DROP','schema','view')
    def test_sql_connection_options_use_oauth_and_never_pat(self):
        host, path, options = connection_options({'DATABRICKS_HOST':'https://example.cloud.databricks.com','DATABRICKS_HTTP_PATH':'/sql/1.0/warehouses/test'})
        self.assertEqual(host, 'example.cloud.databricks.com')
        self.assertEqual(path, '/sql/1.0/warehouses/test')
        self.assertEqual(options, {'auth_type':'databricks-oauth'})
        self.assertNotIn('access_token', options)
    def test_seed_plan_is_reproducible_and_not_apply(self):
        import subprocess, sys
        result=subprocess.run([sys.executable,'scripts/seed_databricks.py','--target','local'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        payload=json.loads((ROOT/'release-report/MDL-2/seed-manifest.json').read_text())
        self.assertEqual(payload['mode'],'plan'); self.assertEqual(payload['case_id'],'CASE_0042')
        apply=subprocess.run([sys.executable,'scripts/seed_databricks.py','--target','staging','--apply'], cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(apply.returncode,0)
    def test_seed_cli_exposes_locked_plan_apply_verify_contract(self):
        import subprocess, sys
        plan=subprocess.run([sys.executable,'scripts/seed_databricks.py','--target','staging','--case','CASE_0042','--plan'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(plan.returncode,0,plan.stderr)
        bad_case=subprocess.run([sys.executable,'scripts/seed_databricks.py','--target','staging','--case','CASE_0001','--plan'], cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(bad_case.returncode,0)
        bad_combo=subprocess.run([sys.executable,'scripts/seed_databricks.py','--target','local','--verify'], cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(bad_combo.returncode,0)
    def test_seed_sql_is_case_scoped_and_public_only(self):
        import subprocess, sys
        result=subprocess.run([sys.executable,'scripts/seed_databricks.py','--target','local','--sql-out','release-report/MDL-2/test-seed.sql'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        sql=(ROOT/'release-report/MDL-2/test-seed.sql').read_text(encoding='utf-8')
        self.assertIn("CASE_0042",sql); self.assertIn('DELETE FROM',sql); self.assertNotIn('case_truth',sql); self.assertNotIn('truth_json',sql)

if __name__=='__main__': unittest.main()
