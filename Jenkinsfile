pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Downloading Sales ETL project from GitHub'
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat 'py -3.11 -m venv .venv'
                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements-ci.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running automated tests'
                bat '.venv\\Scripts\\python.exe -m pytest -v'
            }
        }

        stage('Run Sales ETL') {
            steps {
                echo 'Executing Sales ETL'
                bat '.venv\\Scripts\\python.exe etl.py'
            }
        }

        stage('Archive Output') {
            steps {
                archiveArtifacts artifacts: 'processed_sales.csv,rejected_sales.csv',
                                 fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'Sales ETL CI Pipeline completed successfully!'
        }

        failure {
            echo 'Sales ETL CI Pipeline failed. Check the console output.'
        }
    }
}