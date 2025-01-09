pipeline {
    agent {
        label 'docker'
    }

    environment {
        DOCKER_CREDENTIALS_ID = 'docker'
        BUILD_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('clean workspace') {
            steps {
                cleanWs()
                echo 'workspace cleaned'
                script {
                    sh"""
                        if [ \$(sudo docker ps -aq) ]; then
                            sudo docker rm -f \$(sudo docker ps -aq)
                        else
                            echo "No containers to remove"
                        fi
                        # Create network or ignore if exists
                        sudo docker network create test-network || true
                    """
                }
                echo 'docker container removed and network created'
            }
        }

        stage('Clone Repository') {
            steps {
                dir('MonitoringApp') {
                    script {
                        git branch: 'raziel_jenkins', url: 'https://github.com/ilya-work1/domain-monitoring-project.git'
                        COMMIT_ID = sh(script: 'git rev-parse HEAD', returnStdout: true).trim().take(5)
                    }
                }
            }
        }

        stage('Docker Build & Run Monitoring App') {
            steps {
                dir('MonitoringApp') {
                    script {
                        sh """
                            sudo docker build -t razielrey/domainmonitoring:${BUILD_TAG} .
                            sudo docker run --network test-network -d --name monitoring-app-${BUILD_TAG} razielrey/domainmonitoring:${BUILD_TAG}
                            sleep 5  # Wait for app to start
                        """
                    }
                }
            }
        }

        stage('Selenium Test') {
            steps {
                script {
                    sh """
                        # Run selenium container in the same network
                        sudo docker run --network test-network \\
                            -d \\
                            --name selenium-test \\
                            -e APP_URL=http://monitoring-app-${BUILD_TAG}:8080 \\
                            razielrey/selenium-tests:latest \\
                            tail -f /dev/null
                        
                        sleep 5  # Wait for container to be ready
                        
                        # Run tests
                        if ! sudo docker exec selenium-test python3 run_tests.py; then
                            echo "Selenium tests failed"
                            exit 1
                        fi
                    """
                }
            }
        }
    }

    post {
        success {
            script {
                withCredentials([usernamePassword(credentialsId: 'docker', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo ${DOCKER_PASS} | sudo docker login -u ${DOCKER_USER} --password-stdin
                        sudo docker tag razielrey/domainmonitoring:${BUILD_TAG} razielrey/domainmonitoring:latest
                        sudo docker push razielrey/domainmonitoring:${BUILD_TAG}
                        sudo docker push razielrey/domainmonitoring:latest
                    """
                }
            }
        }

        always {
            sh """
                sudo docker rm -f \$(sudo docker ps -aq --filter name=monitoring-app-${BUILD_TAG}) || true
                sudo docker rm -f \$(sudo docker ps -aq --filter name=selenium-test) || true
                sudo docker network rm test-network || true
            """
        }
    }
}
