pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -e ".[dev]"
                    python -m compileall src
                '''
            }
        }
        stage('Lint') {
            steps {
                echo 'TODO: stage do integrante do lint'
            }
        }
        stage('Testes') {
    steps {
        sh '''
            . .venv/bin/activate
            pytest --junitxml=relatorio-testes.xml --cov=gestao_frotas --cov-report=html --cov-report=xml
        '''
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'relatorio-testes.xml'
            archiveArtifacts artifacts: 'htmlcov/**,coverage.xml', allowEmptyArchive: true
        }
    }
}
        stage('Deploy') {
            steps {
                echo 'TODO: stage do integrante do deploy'
            }
        }
    }
}
