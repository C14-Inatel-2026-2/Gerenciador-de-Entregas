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
                echo 'TODO: stage do integrante dos testes'
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