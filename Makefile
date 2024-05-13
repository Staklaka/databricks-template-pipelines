# Clean
deploy-clean:
	databricks bundle deploy -t no-prod

run-clean:
	databricks bundle run databricks_dab_test_clean

deploy-run-clean: deploy-clean run-clean

