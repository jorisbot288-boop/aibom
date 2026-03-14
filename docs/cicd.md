# AIBOM CI/CD Integration Guide

AIBOM is a command-line tool that scans your Python projects to identify AI components like models, datasets, and APIs. It's designed to help you generate and maintain compliance documentation for the EU AI Act.

Integrating AIBOM into your CI/CD pipeline automates this documentation process. It ensures that your AI component inventory is always up-to-date with your latest code changes, making compliance a continuous and effortless practice.

This guide provides practical examples for integrating AIBOM into popular CI/CD platforms. All examples assume your project uses Python and has a `requirements.txt` or similar dependency management file.

**Prerequisites:**
- Your project must have Python and `pip` available in the CI environment.
- AIBOM is installed via `pip install aibom-cli`.

---

## GitHub Actions

For GitHub Actions, you can create a new workflow file (e.g., `.github/workflows/aibom.yml`) to run the scan on every push to your main branch. The generated reports are then uploaded as build artifacts.

### Example `.github/workflows/aibom.yml`

```yaml
name: AIBOM Scan

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  aibom-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install aibom-cli
          # Uncomment the following line if your project has its own dependencies
          # pip install -r requirements.txt

      - name: Run AIBOM Scan
        run: |
          mkdir -p aibom-reports
          aibom scan . --format markdown --output aibom-reports/aibom-report.md
          aibom scan . --format json --output aibom-reports/aibom-report.json

      - name: Upload AIBOM Reports
        uses: actions/upload-artifact@v4
        with:
          name: aibom-reports
          path: aibom-reports/
```

### Where is the output?

After the workflow run completes, you can find the `aibom-report.md` and `aibom-report.json` files in the "Artifacts" section of the workflow summary page.

---

## GitLab CI/CD

For GitLab, you can add a new job to your existing `.gitlab-ci.yml` file. This job will execute the scan and save the reports as artifacts, which can be browsed or downloaded directly from the GitLab UI.

### Example `.gitlab-ci.yml` snippet

```yaml
stages:
  - test # Or any other stage you prefer

aibom_scan:
  stage: test
  image: python:3.10-slim
  script:
    - pip install aibom-cli
    # Uncomment the following line if your project has its own dependencies
    # - pip install -r requirements.txt
    - mkdir -p aibom-reports
    - aibom scan . --format markdown --output aibom-reports/aibom-report.md
    - aibom scan . --format json --output aibom-reports/aibom-report.json
  artifacts:
    paths:
      - aibom-reports/
    when: on_success
```

### Where is the output?

The generated reports will be available in the "Job artifacts" section on the right-hand side of the pipeline or job view. You can browse the files directly or download them as a zip archive.

---

## Jenkins

For Jenkins, you can use a Declarative Pipeline in a `Jenkinsfile` to define the build process. This example uses a simple `sh` step within a Docker container to ensure a clean Python environment.

### Example `Jenkinsfile`

```groovy
pipeline {
    agent any

    stages {
        stage('AIBOM Scan') {
            steps {
                script {
                    // Using a Docker container ensures a consistent environment
                    docker.image('python:3.10-slim').inside {
                        sh 'pip install aibom-cli'
                        // Uncomment the following line if your project has dependencies
                        // sh 'pip install -r requirements.txt'
                        sh 'mkdir -p aibom-reports'
                        sh 'aibom scan . --format markdown --output aibom-reports/aibom-report.md'
                        sh 'aibom scan . --format json --output aibom-reports/aibom-report.json'
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'aibom-reports/**', fingerprint: true
        }
    }
}
```

### Where is the output?

Once the build is complete, the `aibom-reports` directory will be archived. You can access the `aibom-report.md` and `aibom-report.json` files from the build's main page under "Build Artifacts".
