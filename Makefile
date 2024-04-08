.PHONY: init plan apply destroy test

# Initialize the project
init:
	cd terraform && terraform init

# Plan the Terraform deployment
plan:
	cd terraform && terraform plan

# Apply the Terraform deployment
apply:
	cd terraform && terraform apply

# Destroy the Terraform-managed infrastructure
destroy:
	cd terraform && terraform destroy

# Install Python dependencies for the Lambda function
install-deps:
	pip install -r src/requirements.txt

# Convenience command to deploy everything (after dependencies installation)
deploy: init apply

# Convenience command to tear down everything
teardown: destroy
