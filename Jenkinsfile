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
                sh '''
                    . .venv/bin/activate
                    flake8 . --format=pylint > flake8.log || true
                '''
            }
            post {
                always {
                    recordIssues (
                        tools: [flake8(pattern: 'flake8.log')],
                        qualityGates: [[threshold: 1, type: 'TOTAL', unstable: true]]
                    )
                }
                unsuccessful {
                    mail to: 'williamandrade003@gmail.com',
                         subject: "Lint com problemas: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                         body: "O lint encontrou problemas.\n\nVeja os detalhes: ${env.BUILD_URL}"
                    }
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
            when { branch 'main' }
            steps {
                echo 'Disparando deploy no Render...'
                withCredentials([string(credentialsId: 'render-deploy-hook', variable: 'RENDER_HOOK')]) {
                    sh 'curl -fsS -X POST "$RENDER_HOOK"'
                }
            }
        }
    }
}
